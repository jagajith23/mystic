class Stmt:
    class Visitor:
        def visit_block_stmt(self, stmt):
            pass

        def visit_break_stmt(self, stmt):
            pass

        def visit_continue_stmt(self, stmt):
            pass

        def visit_expression_stmt(self, stmt):
            pass

        def visit_function_stmt(self, stmt):
            pass

        def visit_if_stmt(self, stmt):
            pass

        def visit_print_stmt(self, stmt):
            pass

        def visit_return_stmt(self, stmt):
            pass

        def visit_var_stmt(self, stmt):
            pass

        def visit_while_stmt(self, stmt):
            pass

    def __init__(self):
        self._block = self.Block
        self._break = self.Break
        self._continue = self.Continue
        self._expression = self.Expression
        self._function = self.Function
        self._if = self.If
        self._print = self.Print
        self._return = self.Return
        self._var = self.Var
        self._while = self.While

    class Block:
        def __init__(
            self,
            statements,
        ):
            self.statements = statements

        def accept(self, visitor):
            return visitor.visit_block_stmt(self)

    class Break:
        def __init__(
            self,
            keyword,
        ):
            self.keyword = keyword

        def accept(self, visitor):
            return visitor.visit_break_stmt(self)

    class Continue:
        def __init__(
            self,
            keyword,
        ):
            self.keyword = keyword

        def accept(self, visitor):
            return visitor.visit_continue_stmt(self)

    class Expression:
        def __init__(
            self,
            expression,
        ):
            self.expression = expression

        def accept(self, visitor):
            return visitor.visit_expression_stmt(self)

    class Function:
        def __init__(
            self,
            name,
            params,
            body,
        ):
            self.name = name
            self.params = params
            self.body = body

        def accept(self, visitor):
            return visitor.visit_function_stmt(self)

    class If:
        def __init__(
            self,
            condition,
            then_branch,
            else_branch,
        ):
            self.condition = condition
            self.then_branch = then_branch
            self.else_branch = else_branch

        def accept(self, visitor):
            return visitor.visit_if_stmt(self)

    class Print:
        def __init__(
            self,
            expression,
        ):
            self.expression = expression

        def accept(self, visitor):
            return visitor.visit_print_stmt(self)

    class Return:
        def __init__(
            self,
            keyword,
            value,
        ):
            self.keyword = keyword
            self.value = value

        def accept(self, visitor):
            return visitor.visit_return_stmt(self)

    class Var:
        def __init__(
            self,
            name,
            initializer,
        ):
            self.name = name
            self.initializer = initializer

        def accept(self, visitor):
            return visitor.visit_var_stmt(self)

    class While:
        def __init__(
            self,
            condition,
            body,
        ):
            self.condition = condition
            self.body = body

        def accept(self, visitor):
            return visitor.visit_while_stmt(self)
