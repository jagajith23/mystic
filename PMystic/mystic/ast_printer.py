from expr import Expr
from token import Token
from token_type import TokenType


class AstPrinter(Expr.Visitor):
    def print(self, expr: Expr):
        return expr.accept(self)

    def visit_binary_expr(self, expr: Expr.Binary):
        return self.__parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: Expr.Grouping):
        return self.__parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr: Expr.Literal):
        if expr.value == None:
            return "nil"
        return str(expr.value)

    def visit_unary_expr(self, expr: Expr.Unary):
        return self.__parenthesize(expr.operator.lexeme, expr.right)

    def __parenthesize(self, name: str, *exprs: Expr):
        builder = ""
        builder += "(" + name
        for expr in exprs:
            builder += " "
            builder += expr.accept(self)
        builder += ")"
        return builder

    def main(self):
        expression = Expr.Binary(
            Expr.Unary(
                Token(TokenType.MINUS, "-", None, 1),
                Expr.Literal(value=123),
            ),
            Token(TokenType.STAR, "*", None, 1),
            Expr.Grouping(
                Expr.Literal(value=45.67),
            ),
        )

        print(self.print(expression))


AstPrinter().main()
