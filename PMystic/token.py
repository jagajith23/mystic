from token_type import TokenType


class Token:
    def __init__(self, token_type: TokenType, lexeme: str, literal: object, line: int):
        self._token_type = token_type
        self._lexeme = lexeme
        self._literal = literal
        self._line = line

    def __str__(self):
        return str(self._token_type) + " " + self._lexeme + " " + str(self._literal)
