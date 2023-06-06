from token_type import *
from expr import Expr
from stmt import Stmt
from token import Token


class MysticParser:
    class ParseError(Exception):
        pass

    def parse(self):
        statements = []
        while not self.__is_at_end():
            statements.append(self.__statement())
        return statements

    def __init__(self, tokens: list, mystic):
        self.__current = 0
        self.__tokens = tokens
        self.__mystic = mystic

    def __peek(self) -> Token:
        return self.__tokens[self.__current]

    def __previous(self) -> Token:
        return self.__tokens[self.__current - 1]

    def __is_at_end(self) -> bool:
        return self.__peek().token_type == TokenType.EOF

    def __check(self, type: TokenType) -> bool:
        if self.__is_at_end():
            return False

        return self.__peek().token_type == type

    def __advance(self) -> Token:
        if not self.__is_at_end():
            self.__current += 1

        return self.__previous()

    def __match(self, *types: TokenType) -> bool:
        for type in types:
            if self.__check(type):
                self.__advance()
                return True

        return False

    def __error(self, token: Token, message: str) -> ParseError:
        self.__mystic.error_at(token, message)
        return self.ParseError()

    def __synchronize(self):
        self.__advance()

        while not self.__is_at_end():
            if self.__previous().token_type == TokenType.SEMICOLON:
                return

            if self.__peek().token_type in (
                TokenType.CLASS,
                TokenType.FUN,
                TokenType.STORE,
                TokenType.FOR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.PRINT,
                TokenType.RETURN,
            ):
                return

            self.__advance()

    def __consume(self, type: TokenType, message: str):
        if self.__check(type):
            return self.__advance()

        raise self.__error(self.__peek(), message)

    def __statement(self):
        if self.__match(TokenType.PRINT):
            return self.__print_statement()

        return self.__expression_statement()

    def __print_statement(self):
        value = self.__expression()
        self.__consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Stmt.Print(value)

    def __expression_statement(self):
        expr = self.__expression()
        self.__consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return Stmt.Expression(expr)

    def __expression(self):
        return self.__ternary()

    def __ternary(self):
        expr = self.__equality()

        if self.__match(TokenType.QUESTION):
            true_expr = self.__equality()
            self.__consume(TokenType.COLON, "Expect ':' after expression.")
            false_expr = self.__equality()
            expr = Expr.Ternary(expr, true_expr, false_expr)

        return expr

    def __equality(self):
        expr = self.__comparison()

        while self.__match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.__previous()
            right = self.__comparison()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def __comparison(self):
        expr = self.__term()

        while self.__match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.__previous()
            right = self.__term()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def __term(self):
        expr = self.__factor()

        while self.__match(TokenType.MINUS, TokenType.PLUS):
            operator = self.__previous()
            right = self.__factor()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def __factor(self):
        expr = self.__unary()

        while self.__match(TokenType.SLASH, TokenType.STAR):
            operator = self.__previous()
            right = self.__unary()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def __unary(self):
        if self.__match(TokenType.BANG, TokenType.MINUS):
            operator = self.__previous()
            right = self.__unary()
            return Expr.Unary(operator, right)

        return self.__primary()

    def __primary(self):
        if self.__match(TokenType.FALSE):
            return Expr.Literal(False)
        if self.__match(TokenType.TRUE):
            return Expr.Literal(True)
        if self.__match(TokenType.NIL):
            return Expr.Literal(None)

        if self.__match(TokenType.NUMBER, TokenType.STRING):
            return Expr.Literal(self.__previous().literal)

        if self.__match(TokenType.LEFT_PAREN):
            expr = self.__expression()
            self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Expr.Grouping(expr)

        raise self.__error(self.__peek(), "Expect expression.")
