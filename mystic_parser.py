from token import TOKEN_TYPE
from error import InvalidSyntaxError

class NumberNode:
    def __init__(self, tok):
        self.tok = tok
    
    def __repr__(self):
        return f"{self.tok}"

class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

    def __repr__(self):
        return f"({self.left_node}, {self.op_tok}, {self.right_node})"

class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node

    def __repr__(self):
        return f"({self.op_tok}, {self.node})"

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error: self.error = res.error
            return res.node
        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()
    
    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def parse(self):
        res = self.expr()
        if not res.error and self.current_tok.type != TOKEN_TYPE['EOF']:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '+', '-', '*', '/', '(', or ')'"))
        return res
    
    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TOKEN_TYPE['Plus'], TOKEN_TYPE['Minus']):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))
        
        elif tok.type in (TOKEN_TYPE['Integer'], TOKEN_TYPE['Float']):
            res.register(self.advance())
            return res.success(NumberNode(tok))

        elif tok.type == TOKEN_TYPE['LParen']:
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error: return res
            if self.current_tok.type == TOKEN_TYPE['RParen']:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ')'"))
        
        return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected Integer or Float"))
    
    def term(self):
        return self.bin_op(self.factor, (TOKEN_TYPE['Times'], TOKEN_TYPE['Div']))
    
    def expr(self):
        return self.bin_op(self.term, (TOKEN_TYPE['Plus'], TOKEN_TYPE['Minus']))

    def bin_op(self, func, ops):
        res = ParseResult()
        left = res.register(func())
        if res.error: return res

        while self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register(self.advance())
            right = res.register(func())
            if res.error: return res
            left = BinOpNode(left, op_tok, right)
        
        return res.success(left)
            