from expr import Expr
from stmt import Stmt
from token_type import TokenType
from runtime_error import RTE


class Interpreter(Expr.Visitor, Stmt.Visitor):
    def __init__(self, mystic):
        self.__mystic = mystic

    def interpret(self, statements):
        try:
            for statement in statements:
                self.__execute(statement)
        except RTE as e:
            self.__mystic.runtime_error(e)

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

    def __execute(self, statement):
        statement.accept(self)

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

    def visit_expression_stmt(self, stmt):
        self.__evaluate(stmt.expression)
        return None

    def visit_print_stmt(self, stmt):
        value = self.__evaluate(stmt.expression)
        print(self.__stringify(value))
        return None

    def visit_literal_expr(self, expr):
        return expr.value

    def visit_grouping_expr(self, expr):
        return self.__evaluate(expr.expression)

    def visit_unary_expr(self, expr):
        right = self.__evaluate(expr.right)

        if expr.operator.token_type == TokenType.MINUS:
            self.__check_number_operand(expr.operator, right)
            return -right
        elif expr.operator.token_type == TokenType.BANG:
            return not self.__is_truthy(right)

        return None

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

    def visit_ternary_expr(self, expr):
        condition = self.__evaluate(expr.condition)

        if self.__is_truthy(condition):
            return self.__evaluate(expr.left)
        else:
            return self.__evaluate(expr.right)
