class Expr:
    class Visitor:
        def visit_assign_expr(self, expr):
            pass
        def visit_ternary_expr(self, expr):
            pass
        def visit_binary_expr(self, expr):
            pass
        def visit_call_expr(self, expr):
            pass
        def visit_grouping_expr(self, expr):
            pass
        def visit_literal_expr(self, expr):
            pass
        def visit_logical_expr(self, expr):
            pass
        def visit_unary_expr(self, expr):
            pass
        def visit_variable_expr(self, expr):
            pass
    def __init__(self):
        self._assign = self.Assign
        self._ternary = self.Ternary
        self._binary = self.Binary
        self._call = self.Call
        self._grouping = self.Grouping
        self._literal = self.Literal
        self._logical = self.Logical
        self._unary = self.Unary
        self._variable = self.Variable

    class Assign:
        def __init__(self, name, value, ):
            self.name = name
            self.value = value

        def accept(self, visitor):
            return visitor.visit_assign_expr(self)

    class Ternary:
        def __init__(self, condition, true_expr, false_expr, ):
            self.condition = condition
            self.true_expr = true_expr
            self.false_expr = false_expr

        def accept(self, visitor):
            return visitor.visit_ternary_expr(self)

    class Binary:
        def __init__(self, left, operator, right, ):
            self.left = left
            self.operator = operator
            self.right = right

        def accept(self, visitor):
            return visitor.visit_binary_expr(self)

    class Call:
        def __init__(self, callee, paren, arguments, ):
            self.callee = callee
            self.paren = paren
            self.arguments = arguments

        def accept(self, visitor):
            return visitor.visit_call_expr(self)

    class Grouping:
        def __init__(self, expression, ):
            self.expression = expression

        def accept(self, visitor):
            return visitor.visit_grouping_expr(self)

    class Literal:
        def __init__(self, value, ):
            self.value = value

        def accept(self, visitor):
            return visitor.visit_literal_expr(self)

    class Logical:
        def __init__(self, left, operator, right, ):
            self.left = left
            self.operator = operator
            self.right = right

        def accept(self, visitor):
            return visitor.visit_logical_expr(self)

    class Unary:
        def __init__(self, operator, right, ):
            self.operator = operator
            self.right = right

        def accept(self, visitor):
            return visitor.visit_unary_expr(self)

    class Variable:
        def __init__(self, name, ):
            self.name = name

        def accept(self, visitor):
            return visitor.visit_variable_expr(self)

