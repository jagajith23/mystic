from mystic_lexer import Lexer
from mystic_parser import Parser
from mystic_interpreter import Interpreter, Context

def run(filename, text):
    # Generate tokens
    lex = Lexer(filename, text)
    tokens, err = lex.make_tokens()
    if err: return None, err

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None, ast.error

    # Run program
    interpreter = Interpreter()
    context = Context('<program>')
    result = interpreter.visit(ast.node, context)

    return result.value, result.error
