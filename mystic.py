from mystic_lexer import Lexer
from mystic_parser import Parser
from mystic_interpreter import Interpreter, Context, SymbolTable, Number

global_symbol_table = SymbolTable()
global_symbol_table.set_val("null", Number(0))

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
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error
