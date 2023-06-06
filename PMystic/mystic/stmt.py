class Stmt:
    class Visitor:
        def visit_expression_stmt(self, stmt):
            pass

        def visit_print_stmt(self, stmt):
            pass

    def __init__(self):
        self.expression = self.Expression
        self.print = self.Print

    class Expression:
        def __init__(self, expression):
            self.expression = expression

        def accept(self, visitor):
            return visitor.visit_expression_stmt(self)

    class Print:
        def __init__(
            self,
            expression,
        ):
            self.expression = expression

        def accept(self, visitor):
            return visitor.visit_print_stmt(self)
