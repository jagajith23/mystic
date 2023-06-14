from expr import Expr
from stmt import Stmt
from token_type import TokenType
from runtime_error import RTE
from environment import Environment


class Interpreter(Expr.Visitor, Stmt.Visitor):
    def __init__(self, mystic):
        self.__mystic = mystic
        self.__env = Environment()

    def interpret(self, statements):
        try:
            for statement in statements:
                self.__execute(statement)
        except RTE as e:
            self.__mystic.runtime_error(e)

    # ------- Helper Functions ------- #

    def __stringify(self, obj):
        if obj is None:
            return "nil"

        if isinstance(obj, float):
            text = str(obj)
            if text[-2:] == ".0":
                text = text[:-2]
            return text

        return str(obj)

    def __evaluate(self, expr):
        return expr.accept(self)

    def __execute(self, stmt):
        stmt.accept(self)

    def __execute_block(self, statements, env):
        previous = self.__env
        try:
            self.__env = env
            for statement in statements:
                self.__execute(statement)
        finally:
            self.__env = previous

    def __is_truthy(self, obj):
        if obj is None:
            return False
        elif isinstance(obj, bool):
            return obj
        elif isinstance(obj, float):
            return obj != 0
        elif isinstance(obj, str):
            return len(obj) > 0
        elif isinstance(obj, char):
            return obj != "\0"

        return True

    def __is_equal(self, left, right):
        if left is None and right is None:
            return True
        if left is None:
            return False

        return left == right

    def __check_number_operand(self, operator, operand):
        if isinstance(operand, float):
            return

        raise RTE(expr.operator, "Operand must be a number.")

    def __check_number_operands(self, operator, left, right):
        if isinstance(left, float) and isinstance(right, float):
            return

        raise RTE(expr.operator, "Operands must be numbers.")

    # ------- Visitor Functions ------- #

    def visit_block_stmt(self, stmt):
        self.__execute_block(stmt.statements, Environment(self.__env))
        return None

    def visit_expression_stmt(self, stmt):
        value = self.__evaluate(stmt.expression)
        if self.__mystic.is_repl:
            if value is not None:
                print(self.__stringify(value))
        return None

    def visit_if_stmt(self, stmt):
        if self.__is_truthy(self.__evaluate(stmt.condition)):
            self.__execute(stmt.then_branch)
        elif stmt.else_branch != None:
            self.__execute(stmt.else_branch)
        return None

    def visit_while_stmt(self, stmt):
        while self.__is_truthy(self.__evaluate(stmt.condition)):
            self.__execute(stmt.body)
        return None

    def visit_print_stmt(self, stmt):
        value = self.__evaluate(stmt.expression)
        print(self.__stringify(value))
        return None

    def visit_var_stmt(self, stmt):
        value = None
        if stmt.initializer != None:
            value = self.__evaluate(stmt.initializer)
        self.__env.define(stmt.name.lexeme, value)
        return None

    def visit_assign_expr(self, expr):
        value = self.__evaluate(expr.value)
        self.__env.assign(expr.name, value)
        return value

    def visit_variable_expr(self, expr):
        value = self.__env.get(expr.name)

        if value is None:
            raise RTE(
                expr.name,
                "Undefined variable '"
                + expr.name.lexeme
                + "'"
                + "at line "
                + str(expr.name.line)
                + ".",
            )

        return value

    def visit_literal_expr(self, expr):
        return expr.value

    def visit_logical_expr(self, expr):
        left = self.__evaluate(expr.left)

        if expr.operator.token_type == TokenType.OR:
            if self.__is_truthy(left):
                return left
        else:
            if not self.__is_truthy(left):
                return left

        return self.__evaluate(expr.right)

    def visit_grouping_expr(self, expr):
        return self.__evaluate(expr.expression)

    def visit_ternary_expr(self, expr):
        condition = self.__evaluate(expr.condition)

        if self.__is_truthy(condition):
            return self.__evaluate(expr.true_expr)
        return self.__evaluate(expr.false_expr)

    def visit_binary_expr(self, expr):
        left = self.__evaluate(expr.left)
        right = self.__evaluate(expr.right)

        if expr.operator.token_type == TokenType.MINUS:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) - float(right)
        elif expr.operator.token_type == TokenType.SLASH:
            self.__check_number_operands(expr.operator, left, right)
            if float(right) == 0:
                raise RTE(expr.operator, "Cannot divide by zero.")
            return float(left) / float(right)
        elif expr.operator.token_type == TokenType.STAR:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) * float(right)
        elif expr.operator.token_type == TokenType.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return float(left) + float(right)
            elif isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)
            elif isinstance(left, float) and isinstance(right, str):
                return self.__stringify(left) + str(right)
            elif isinstance(left, str) and isinstance(right, float):
                return str(left) + self.__stringify(right)
        elif expr.operator.token_type == TokenType.GREATER:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) > float(right)
        elif expr.operator.token_type == TokenType.GREATER_EQUAL:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) >= float(right)
        elif expr.operator.token_type == TokenType.LESS:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) < float(right)
        elif expr.operator.token_type == TokenType.LESS_EQUAL:
            self.__check_number_operands(expr.operator, left, right)
            return float(left) <= float(right)
        elif expr.operator.token_type == TokenType.EQUAL_EQUAL:
            self.__check_number_operands(expr.operator, left, right)
            return self.__is_equal(left, right)
        elif expr.operator.token_type == TokenType.BANG_EQUAL:
            self.__check_number_operands(expr.operator, left, right)
            return not self.__is_equal(left, right)

        return None

    def visit_unary_expr(self, expr):
        right = self.__evaluate(expr.right)

        if expr.operator.token_type == TokenType.MINUS:
            self.__check_number_operand(expr.operator, right)
            return -right
        elif expr.operator.token_type == TokenType.BANG:
            return not self.__is_truthy(right)

        return None
