from collections import deque
from stmt import Stmt
from expr import Expr
from enum import Enum


class Resolver(Stmt.Visitor, Expr.Visitor):
    def __init__(self, mystic):
        self.scopes = deque()
        self.__mystic = mystic
        self.__curr_function = self.FunctionType.NONE
        self.__curr_loop = self.LoopType.NONE

    class FunctionType(Enum):
        NONE = 0
        FUNCTION = 1

    class LoopType(Enum):
        NONE = 0
        LOOP = 1

    def resolve(self, statements):
        for statement in statements:
            self.__resolve_statement(statement)

    def __resolve_function(self, stmt, type):
        enclosing_func = self.__curr_function
        self.__curr_function = type

        self.__begin_scope()

        for param in stmt.params:
            self.__declare(param)
            self.__define(param)

        self.resolve(stmt.body)
        self.__end_scope()

        self.__curr_function = enclosing_func

    def __resolve_loop(self, stmt, type):
        enclosing_loop = self.__curr_loop
        self.__curr_loop = type

        self.__resolve_expr(stmt.condition)
        self.__resolve_statement(stmt.body)

        self.__curr_loop = enclosing_loop

    def visit_block_stmt(self, stmt):
        self.__begin_scope()
        self.resolve(stmt.statements)
        self.__end_scope()

    def visit_if_stmt(self, stmt):
        self.__resolve_expr(stmt.condition)
        self.__resolve_statement(stmt.then_branch)
        if stmt.else_branch is not None:
            self.resolve(stmt.else_branch)

    def visit_print_stmt(self, stmt):
        self.__resolve_expr(stmt.expression)

    def visit_return_stmt(self, stmt):
        if self.__curr_function == self.FunctionType.NONE:
            self.__mystic.error(stmt.keyword, "Can't return from top-level code.")

        if stmt.value is not None:
            self.__resolve_expr(stmt.value)

    def visit_expression_stmt(self, stmt):
        self.__resolve_expr(stmt.expression)

    def visit_function_stmt(self, stmt):
        self.__declare(stmt.name)
        self.__define(stmt.name)

        self.__resolve_function(stmt, self.FunctionType.FUNCTION)

    def visit_var_stmt(self, stmt):
        self.__declare(stmt.name)
        if stmt.initializer is not None:
            self.__resolve_expr(stmt.initializer)
        self.__define(stmt.name)

    def visit_while_stmt(self, stmt):
        self.__resolve_loop(stmt, self.LoopType.LOOP)

    def visit_break_stmt(self, stmt):
        if self.__curr_loop == self.LoopType.NONE:
            self.__mystic.error(stmt.keyword, "'break' outside loop")

    def visit_continue_stmt(self, stmt):
        if self.__curr_loop == self.LoopType.NONE:
            self.__mystic.error(stmt.keyword, "'continue' outside loop")

    def visit_assign_expr(self, expr):
        self.__resolve_expr(expr.value)
        self.__resolve_local(expr, expr.name)

    def visit_ternary_expr(self, expr):
        self.__resolve_expr(expr.condition)
        self.__resolve_expr(expr.then_branch)
        self.__resolve_expr(expr.else_branch)

    def visit_binary_expr(self, expr):
        self.__resolve_expr(expr.left)
        self.__resolve_expr(expr.right)

    def visit_call_expr(self, expr):
        self.__resolve_expr(expr.callee)

        for argument in expr.arguments:
            self.__resolve_expr(argument)

    def visit_grouping_expr(self, expr):
        self.__resolve_expr(expr.expression)

    def visit_literal_expr(self, expr):
        pass

    def visit_logical_expr(self, expr):
        self.__resolve_expr(expr.left)
        self.__resolve_expr(expr.right)

    def visit_unary_expr(self, expr):
        self.__resolve_expr(expr.right)

    def visit_variable_expr(self, expr):
        if len(self.scopes) != 0 and self.scopes[-1].get(expr.name.lexeme) is False:
            raise Exception("Cannot read local variable in its own initializer.")
        self.__resolve_local(expr, expr.name)

    def __resolve_statement(self, stmt):
        stmt.accept(self)

    def __resolve_expr(self, expr):
        expr.accept(self)

    def __begin_scope(self):
        self.scopes.append({})

    def __end_scope(self):
        self.scopes.pop()

    def __declare(self, name):
        if len(self.scopes) == 0:
            return

        if self.scopes[-1].get(name.lexeme) is None:
            self.__mystic.error(
                name, "Already a variable with this name in this scope."
            )

        self.scopes[-1][name.lexeme] = False

    def __define(self, name):
        if len(self.scopes) == 0:
            return

        self.scopes[-1][name.lexeme] = True

    def __resolve_local(self, expr, name):
        for i in range(len(self.scopes) - 1, 0, -1):
            if self.scopes[i].get(name.lexeme) is not None:
                self.__mystic.interpreter.resolve(expr, len(self.scopes) - 1 - i)
                return
