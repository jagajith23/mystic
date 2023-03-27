from token import TOKEN_TYPE
from error import RunTimeError

class RunTimeResult:
    def __init__(self):
        self.error = None
        self.value = None

    def register(self, res):
        # if isinstance(res, RunTimeResult):
        if res.error: self.error = res.error
        return res.value
        # return res

    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self

class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos

class Number:
    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.set_context()
    
    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def plus(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None

    def minus(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None

    def times(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None

    def div_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RunTimeError(other.pos_start, other.pos_end, "Division by zero", self.context)
            return Number(self.value / other.value).set_context(self.context), None

    def __repr__(self):
        return f"{self.value}"

class Interpreter:
    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    def visit_NumberNode(self, node, context):
        return RunTimeResult().success(Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end))

    def visit_BinOpNode(self, node, context):
        res = RunTimeResult()
        left = res.register(self.visit(node.left_node, context))
        if res.error: return res
        right = res.register(self.visit(node.right_node, context))
        if res.error: return res

        error = None

        if node.op_tok.type == TOKEN_TYPE['Plus']:
            result, error = left.plus(right)
        elif node.op_tok.type == TOKEN_TYPE['Minus']:
            result, error = left.minus(right)
        elif node.op_tok.type == TOKEN_TYPE['Times']:
            result, error = left.times(right)
        elif node.op_tok.type == TOKEN_TYPE['Div']:
            result, error = left.div_by(right)

        if error:
            return res.failure(error)
        return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res = RunTimeResult()
        number = res.register(self.visit(node.node), context)
        if res.error: return res

        error = None

        if node.op_tok.type == TOKEN_TYPE['Minus']:
            number, error = number.times(Number(-1))

        if error:
            return res.failure(error)
        return res.success(number.set_pos(node.pos_start, node.pos_end))