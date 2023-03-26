from mystic_lexer import Lexer
from mystic_parser import Parser

def run(filename, text):
    lex = Lexer(filename, text)
    tokens, err = lex.make_tokens()

    if err: return None, err

    parser = Parser(tokens)
    ast = parser.parse()

    return ast.node, ast.error
