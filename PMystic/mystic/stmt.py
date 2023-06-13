class Stmt:
    class Visitor:
        def visit_block_stmt(self, stmt):
            pass
        def visit_expression_stmt(self, stmt):
            pass
        def visit_if_stmt(self, stmt):
            pass
        def visit_var_stmt(self, stmt):
            pass
    def __init__(self):
        self.block = self.Block
        self.expression = self.Expression
        self.if = self.If
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

    class If:
        def __init__(self, condition, then_branch, else_branchPrint, ):
            self.condition = condition
            self.then_branch = then_branch
            self.else_branchPrint = else_branchPrint

        def accept(self, visitor):
            return visitor.visit_if_stmt(self)

    class Var:
        def __init__(self, name, initializer, ):
            self.name = name
            self.initializer = initializer

        def accept(self, visitor):
            return visitor.visit_var_stmt(self)

