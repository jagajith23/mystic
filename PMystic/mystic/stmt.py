class Stmt:
    class Visitor:
        def visit_block_stmt(self, stmt):
            pass
        def visit_expression_stmt(self, stmt):
            pass
        def visit_print_stmt(self, stmt):
            pass
        def visit_var_stmt(self, stmt):
            pass
    def __init__(self):
        self.block = self.Block
        self.expression = self.Expression
        self.print = self.Print
        self.var = self.Var

    class Block:
        def __init__(self, statements, ):
            self.statements = statements

        def accept(self, visitor):
            return visitor.visit_block_stmt(self)

    class Expression:
        def __init__(self, expression, ):
            self.expression = expression

        def accept(self, visitor):
            return visitor.visit_expression_stmt(self)

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

