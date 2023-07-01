from token_type import *
from expr import Expr
from stmt import Stmt
from mystic_token import Token


class MysticParser:
    class ParseError(Exception):
        pass

    def parse(self):
        statements = []
        while not self.__is_at_end():
            statements.append(self.__declaration())
        return statements

    def __init__(self, tokens: list, mystic):
        self.__current = 0
        self.__loop_depth = 0
        self.__tokens = tokens
        self.__mystic = mystic

    # ------- Helper Functions ------- #

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

    # ------- Grammar Functions ------- #

    """
    program         → declaration* EOF
    declaration     → funDecl | varDecl | statement
    funDecl         → "fun" function
    function        → IDENTIFIER "(" parameters? ")" block
    parameters      → IDENTIFIER ( "," IDENTIFIER )*
    varDecl         → "store" IDENTIFIER ( "=" expression )?
    statement       → printStmt | expressionStmt | block | ifStmt | whileStmt | forStmt | returnStmt
    returnStmt      → "return" expression? ";"
    whileStmt       → "while" "(" expression ")" statement
    forStmt         → "for" "(" ( varDecl | expressionStmt | ";" ) expression? ";" expression? ")" statement
    printStmt       → "print" expression
    expressionStmt  → expression
    expression      → assignment
    assignment      → IDENTIFIER "=" assignment | logic_or
    logic_or        → logic_and ( "or" logic_and )*
    logic_and       → ternary ( "and" ternary )*
    ternary         → equality ( "?" equality ":" equality )?
    equality        → comparison ( ( "!=" | "==" ) comparison )*
    comparison      → term ( ( ">" | ">=" | "<" | "<=" ) term )*
    term            → factor ( ( "-" | "+" ) factor )*
    factor          → unary ( ( "/" | "*" ) unary )*
    unary           → ( "!" | "-" ) unary | call
    call            → primary ( "(" arguments? ")" )*
    arguments       → expression ( "," expression )*
    primary         → NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")" | IDENTIFIER
    """

    def __declaration(self):
        try:
            if self.__match(TokenType.FUN):
                return self.__fun_declaration("function")
            if self.__match(TokenType.STORE):
                return self.__var_declaration()
            return self.__statement()
        except self.ParseError:
            self.__synchronize()
            return None

    def __fun_declaration(self, kind: str):
        name = self.__consume(TokenType.IDENTIFIER, f"Expect {kind} name.")

        self.__consume(TokenType.LEFT_PAREN, f"Expect '(' after {kind} name.")
        parameters = []
        if not self.__check(TokenType.RIGHT_PAREN):
            parameters.append(
                self.__consume(TokenType.IDENTIFIER, "Expect parameter name.")
            )
            while self.__match(TokenType.COMMA):
                if len(parameters) >= 255:
                    self.__error(self.__peek(), "Cannot have more than 255 arguments.")
                parameters.append(
                    self.__consume(TokenType.IDENTIFIER, "Expect parameter name.")
                )
        self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")

        self.__consume(TokenType.LEFT_BRACE, f"Expect '{{' before {kind} body.")
        body = self.__block()
        return Stmt.Function(name, parameters, body)

    def __var_declaration(self):
        name = self.__consume(TokenType.IDENTIFIER, "Expect variable name.")

        initializer = None
        if self.__match(TokenType.EQUAL):
            initializer = self.__expression()

        self.__consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return Stmt.Var(name, initializer)

    def __statement(self):
        if self.__match(TokenType.IF):
            return self.__if_statement()

        if self.__match(TokenType.BREAK):
            return self.__break_statement()

        if self.__match(TokenType.CONTINUE):
            return self.__continue_statement()

        if self.__match(TokenType.WHILE):
            return self.__while_statement()

        if self.__match(TokenType.FOR):
            return self.__for_statement()

        if self.__match(TokenType.PRINT):
            return self.__print_statement()

        if self.__match(TokenType.RETURN):
            return self.__return_statement()

        if self.__match(TokenType.LEFT_BRACE):
            return Stmt.Block(self.__block())

        return self.__expression_statement()

    def __expression_statement(self):
        expr = self.__expression()
        self.__consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return Stmt.Expression(expr)

    def __if_statement(self):
        self.__consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.__expression()
        self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")

        then_branch = self.__statement()
        else_branch = None

        if self.__match(TokenType.ELSE):
            else_branch = self.__statement()

        return Stmt.If(condition, then_branch, else_branch)

    def __break_statement(self):
        if self.__loop_depth == 0:
            self.__error(self.__previous(), "Cannot use 'break' outside of a loop.")
        self.__consume(TokenType.SEMICOLON, "Expect ';' after 'break'.")
        return Stmt.Break()

    def __continue_statement(self):
        if self.__loop_depth == 0:
            self.__error(self.__previous(), "Cannot use 'continue' outside of a loop.")
        self.__consume(TokenType.SEMICOLON, "Expect ';' after 'continue'.")
        return Stmt.Continue()

    def __while_statement(self):
        self.__consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.__expression()
        self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")

        try:
            self.__loop_depth += 1
            body = self.__statement()

            return Stmt.While(condition, body)
        finally:
            self.__loop_depth -= 1

    def __for_statement(self):
        self.__consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")

        initializer = None
        if self.__match(TokenType.SEMICOLON):
            initializer = None
        elif self.__match(TokenType.STORE):
            initializer = self.__var_declaration()
        else:
            initializer = self.__expression_statement()

        condition = None
        if not self.__match(TokenType.SEMICOLON):
            condition = self.__expression()
        self.__consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")

        increment = None
        if not self.__match(TokenType.RIGHT_PAREN):
            increment = self.__expression()
        self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")

        try:
            self.__loop_depth += 1
            body = self.__statement()

            if increment is not None:
                body = Stmt.Block([body, Stmt.Expression(increment)])

            if condition is None:
                condition = Expr.Literal(True)
            body = Stmt.While(condition, body)

            if initializer is not None:
                body = Stmt.Block([initializer, body])

            return body
        finally:
            self.__loop_depth -= 1

    def __print_statement(self):
        value = self.__expression()
        self.__consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Stmt.Print(value)

    def __return_statement(self):
        keyword = self.__previous()
        value = None

        if not self.__check(TokenType.SEMICOLON):
            value = self.__expression()

        self.__consume(TokenType.SEMICOLON, "Expect ';' after return value.")
        return Stmt.Return(keyword, value)

    def __block(self):
        statements = []

        while not (self.__check(TokenType.RIGHT_BRACE) or self.__is_at_end()):
            statements.append(self.__declaration())

        self.__consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def __expression(self):
        return self.__assignment()

    def __assignment(self):
        expr = self.__or()

        if self.__match(TokenType.EQUAL):
            equals = self.__previous()
            value = self.__assignment()

            if isinstance(expr, Expr.Variable):
                name = expr.name
                return Expr.Assign(name, value)

            self.__error(equals, "Invalid assignment target.")

        return expr

    def __or(self):
        expr = self.__and()

        if self.__match(TokenType.OR):
            operator = self.__previous()
            right = self.__and()
            expr = Expr.Logical(expr, operator, right)

        return expr

    def __and(self):
        expr = self.__ternary()

        if self.__match(TokenType.AND):
            operator = self.__previous()
            right = self.__ternary()
            expr = Expr.Logical(expr, operator, right)

        return expr

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

        while self.__match(
            TokenType.LESS,
            TokenType.LESS_EQUAL,
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
        ):
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

        return self.__call()

    def __call(self):
        expr = self.__primary()

        while True:
            if self.__match(TokenType.LEFT_PAREN):
                expr = self.__finish_call(expr)
            else:
                break

        return expr

    def __finish_call(self, callee):
        args = []

        if not self.__check(TokenType.RIGHT_PAREN):
            args.append(self.__expression())
            while self.__match(TokenType.COMMA):
                if len(args) >= 255:
                    self.__error(self.__peek(), "Cannot have more than 255 arguments.")
                args.append(self.__expression())

        paren = self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments.")

        return Expr.Call(callee, paren, args)

    def __primary(self):
        if self.__match(TokenType.FALSE):
            return Expr.Literal(False)
        if self.__match(TokenType.TRUE):
            return Expr.Literal(True)
        if self.__match(TokenType.NIL):
            return Expr.Literal(None)

        if self.__match(TokenType.NUMBER, TokenType.STRING):
            return Expr.Literal(self.__previous().literal)

        if self.__match(TokenType.IDENTIFIER):
            return Expr.Variable(self.__previous())

        if self.__match(TokenType.LEFT_PAREN):
            expr = self.__expression()
            self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Expr.Grouping(expr)

        raise self.__error(self.__peek(), "Expect expression.")
