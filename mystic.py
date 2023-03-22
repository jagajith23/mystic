from lexer import Lexer

def run(filename, text):
    lex = Lexer(filename, text)
    tokens, err = lex.make_tokens()

    return tokens, err