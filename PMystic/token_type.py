from enum import Enum, auto


TOKENS = [
    # Single-character tokens.
    "LEFT_PAREN",
    "RIGHT_PAREN",
    "LEFT_BRACE",
    "RIGHT_BRACE",
    "COMMA",
    "DOT",
    "MINUS",
    "PLUS",
    "SEMICOLON",
    "SLASH",
    "STAR",
    # One or two character tokens.
    "BANG",
    "BANG_EQUAL",
    "EQUAL",
    "EQUAL_EQUAL",
    "GREATER",
    "GREATER_EQUAL",
    "LESS",
    "LESS_EQUAL",
    # Literals.
    "IDENTIFIER",
    "STRING",
    "NUMBER",
    # Keywords.
    "AND",
    "CLASS",
    "ELSE",
    "FALSE",
    "FUN",
    "FOR",
    "IF",
    "NIL",
    "OR",
    "PRINT",
    "RETURN",
    "PARENT",
    "THIS",
    "TRUE",
    "STORE",
    "WHILE",
    # End of file token.
    "EOF",
]


class TokenType(Enum):
    @classmethod
    def _generate_next_value_(cls, name, start, count, last_values):
        return cls.next_value

    @classmethod
    def _missing_(cls, value):
        # Optional: Handle missing values
        pass

    @classmethod
    def _init_next_value(cls):
        cls.next_value = 0

    @classmethod
    def _create_next_member(cls, name, value):
        member = object.__new__(cls)
        member._name_ = name
        member._value_ = value
        cls.next_value += 1
        return member

    def __repr__(self):
        return self.name


TokenType._init_next_value()
for token in TOKENS:
    setattr(TokenType, token, TokenType._create_next_member(token, token))
