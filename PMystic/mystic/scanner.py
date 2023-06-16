from token_type import *
from mystic_token import Token


class Scanner:
    keywords = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "parent": TokenType.PARENT,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "store": TokenType.STORE,
        "while": TokenType.WHILE,
        "break": TokenType.BREAK,
    }

    def __init__(self, source: str, mystic: object):
        self.__source = source
        self.__mystic = mystic
        self.__tokens = []
        self.__start = 0
        self.__current = 0
        self.__line = 1
        self.__source_len = len(source)

    def scan_tokens(self) -> list:
        while not self.__is_at_end():
            # Beginning of the next lexeme.
            self.__start = self.__current
            self.__scan_token()

        self.__add_token(TokenType.EOF)
        return self.__tokens

    def __is_at_end(self) -> bool:
        return self.__current >= self.__source_len

    def __scan_token(self):
        char = self.__advance()

        if char == "(":
            self.__add_token(TokenType.LEFT_PAREN, "(")
        elif char == ")":
            self.__add_token(TokenType.RIGHT_PAREN, ")")
        elif char == "{":
            self.__add_token(TokenType.LEFT_BRACE, "{")
        elif char == "}":
            self.__add_token(TokenType.RIGHT_BRACE, "}")
        elif char == ",":
            self.__add_token(TokenType.COMMA, ",")
        elif char == ".":
            self.__add_token(TokenType.DOT, ".")
        elif char == "-":
            self.__add_token(TokenType.MINUS, "-")
        elif char == "+":
            self.__add_token(TokenType.PLUS, "+")
        elif char == ";":
            self.__add_token(TokenType.SEMICOLON, ";")
        elif char == "*":
            self.__add_token(TokenType.STAR, "*")
        elif char == "!":
            self.__add_token(
                TokenType.BANG_EQUAL if self.__match("=") else TokenType.BANG, "!="
            )
        elif char == "=":
            self.__add_token(
                TokenType.EQUAL_EQUAL if self.__match("=") else TokenType.EQUAL, "=="
            )
        elif char == "<":
            self.__add_token(
                TokenType.LESS_EQUAL if self.__match("=") else TokenType.LESS, "<="
            )
        elif char == ">":
            self.__add_token(
                TokenType.GREATER_EQUAL if self.__match("=") else TokenType.GREATER,
                ">=",
            )
        elif char == "/":
            if self.__match("/"):
                while self.__peek() != "\n" and not self.__is_at_end():
                    self.__advance()
            elif self.__match("*"):
                while (
                    self.__peek() != "*"
                    and self.__peek_next() != "/"
                    and not self.__is_at_end()
                ):
                    if self.__peek() == "\n":
                        self.__line += 1
                    self.__advance()

                if self.__is_at_end():
                    self.__mystic.error(self.__line, "Unterminated comment.")
                    return

                # The closing '*/'.
                self.__advance()
                self.__advance()
            else:
                self.__add_token(TokenType.SLASH, "/")
        elif char == "?":
            self.__add_token(TokenType.QUESTION, "?")
        elif char == ":":
            self.__add_token(TokenType.COLON, ":")
        elif char == " " or char == "\r" or char == "\t":
            pass
        elif char == "\n":
            self.__line += 1
        elif char == '"':
            self.__string()
        elif self.__is_digit(char):
            self.__number()
        elif self.__is_alpha(char):
            self.__identifier()
        else:
            self.__mystic.error(self.__line, "Unexpected character.")

    def __is_alpha(self, char: str) -> bool:
        return (
            (char >= "a" and char <= "z")
            or (char >= "A" and char <= "Z")
            or char == "_"
        )

    def __identifier(self):
        while self.__is_alpha_numeric(self.__peek()):
            self.__advance()
        text = self.__source[self.__start : self.__current]
        type = None
        if text in self.keywords:
            type = self.keywords[text]
        else:
            type = TokenType.IDENTIFIER
        self.__add_token(type, text)

    def __is_alpha_numeric(self, char: str) -> bool:
        return self.__is_alpha(char) or self.__is_digit(char)

    def __is_digit(self, char: str) -> bool:
        return char >= "0" and char <= "9"

    def __number(self):
        while self.__is_digit(self.__peek()):
            self.__advance()

        # Look for a fractional part.
        if self.__peek() == "." and self.__is_digit(self.__peek_next()):
            # Consume the "."
            self.__advance()

            while self.__is_digit(self.__peek()):
                self.__advance()

        self.__add_token(
            TokenType.NUMBER,
            self.__parse_double(self.__source[self.__start : self.__current]),
        )

    def __string(self):
        while self.__peek() != '"' and not self.__is_at_end():
            if self.__peek() == "\n":
                self.__line += 1
            self.__advance()

        if self.__is_at_end():
            self.__mystic.error(self.__line, "Unterminated string.")
            return

        # The closing '.
        self.__advance()

        # Trim the surrounding quotes.
        value = self.__source[self.__start + 1 : self.__current - 1]
        self.__add_token(TokenType.STRING, value)

    def __peek(self) -> str:
        if self.__is_at_end():
            return "\0"
        return self.__source[self.__current]

    def __peek_next(self) -> str:
        if self.__current + 1 >= self.__source_len:
            return "\0"
        return self.__source[self.__current + 1]

    def __match(self, expected: str) -> bool:
        if self.__is_at_end():
            return False
        if self.__source[self.__current] != expected:
            return False

        self.__current += 1
        return True

    def __advance(self) -> str:
        self.__current += 1
        return self.__source[self.__current - 1]

    def __add_token(self, token_type: TokenType, literal: object = None):
        if literal != None:
            text = self.__source[self.__start : self.__current]
            self.__tokens.append(Token(token_type, text, literal, self.__line))
        else:
            self.__tokens.append(Token(token_type, "", None, self.__line))

    def __parse_double(self, lexeme: str) -> float:
        integer_part = 0
        fractional_part = 0
        fractional_multiplier = 1
        is_fractional = False

        lexeme = lexeme.strip()

        for char in lexeme:
            if char == ".":
                if is_fractional:
                    return ValueError("Invalid lexeme: " + lexeme)
                is_fractional = True
                continue

            if not is_fractional:
                integer_part = integer_part * 10 + (ord(char) - ord("0"))
            else:
                fractional_multiplier *= 0.1
                fractional_part = fractional_part * 10 + (ord(char) - ord("0"))

        value = integer_part + fractional_multiplier * fractional_part

        return value if is_fractional else value * 1.0
