TOKEN_TYPE = {
    # Identifier and literals 
    'Identifier': 'identifier',
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
    'EndOfInput': 'end_of_input'
}

class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"{self.type}: {self.value}"