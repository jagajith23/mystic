class Stmt:
    class Visitor:
        def visit_block_stmt(self, stmt):
            pass
        def visit_break_stmt(self, stmt):
            pass
        def visit_expression_stmt(self, stmt):
            pass
        def visit_if_stmt(self, stmt):
            pass
        def visit_print_stmt(self, stmt):
            pass
        def visit_print_stmt(self, stmt):
            pass
        def visit_var_stmt(self, stmt):
            pass
        def visit_while_stmt(self, stmt):
            pass
    def __init__(self):
        self._block = self.Block
        self._break = self.Break
        self._expression = self.Expression
        self._if = self.If
        self._print = self.Print
        self._print = self.Print
        self._var = self.Var
        self._while = self.While

    class Block:
        def __init__(self, statements, ):
            self.statements = statements

        def accept(self, visitor):
            return visitor.visit_block_stmt(self)

    class Break:
        def accept(self, visitor):
            return visitor.visit_break_stmt(self)

    class Expression:
        def __init__(self, expression, ):
            self.expression = expression

        def accept(self, visitor):
            return visitor.visit_expression_stmt(self)

    class If:
        def __init__(self, condition, then_branch, else_branch, ):
            self.condition = condition
            self.then_branch = then_branch
            self.else_branch = else_branch

        def accept(self, visitor):
            return visitor.visit_if_stmt(self)

    class Print:
        def __init__(self, expression, ):
            self.expression = expression

        def accept(self, visitor):
            return visitor.visit_print_stmt(self)

    class Print:
        def __init__(self, expression, ):
            self.expression = expression

        def accept(self, visitor):
            return visitor.visit_print_stmt(self)

    class Var:
        def __init__(self, name, initializer, ):
            self.name = name
            self.initializer = initializer

        def accept(self, visitor):
            return visitor.visit_var_stmt(self)

    class While:
        def __init__(self, condition, body, ):
            self.condition = condition
            self.body = body

        def accept(self, visitor):
            return visitor.visit_while_stmt(self)

