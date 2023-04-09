TOKEN_TYPE = {
    # Identifier and literals 
    'Identifier': 'identifier',
    'Keyword': 'keyword',
    'Integer': 'integer',
    'Float': 'float',

    # Arithmetic Operators
    'Plus': 'plus',                                   # +
    'Minus': 'minus',                                 # -
    'Times': 'times',                                 # *
    'Div': 'div',                                     # /

    # Relational Operators
    'Equal': 'equal',                                 # ==
    'NotEqual': 'not_equal',                          # !=
    'LessThan': 'less_than',                          # <
    'LessThanOrEqual': 'less_than_or_equal',          # <=
    'GreaterThan': 'greater_than',                    # >
    'GreaterThanOrEqual': 'greater_than_or_equal',    # >=

    # Logical Operators
    'And': 'and',                                     # &&
    'Or': 'or',                                       # ||
    'Not': 'not',                                     # !

    # Assignment Operators
    'Assign': 'assign',                               # =

    # Paranthesis
    'LParen': 'lparen',                               # (
    'RParen': 'rparen',                               # )

    # Special Token
    'EOF': 'end_of_file'
}

KEYWORDS = ["store"]

class Token:
    def __init__(self, type, value=None, pos_start=None, pos_end=None):
        self.type = type
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()
        
        if pos_end:
            self.pos_end = pos_end.copy()

    def matches(self, type_, value):
        return self.type == type_ and self.value == value

    def __repr__(self):
        return f"{self.type}: {self.value}"