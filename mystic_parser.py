from token import TOKEN_TYPE
from error import InvalidSyntaxError

class NumberNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = tok.pos_start
        self.pos_end = tok.pos_end
    
    def __repr__(self):
        return f"{self.tok}"

class VarAccessNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = tok.pos_start
        self.pos_end = tok.pos_end

    def __repr__(self):
        return f"{self.tok}"

class VarAssignNode:
    def __init__(self, tok, value_node):
        self.tok = tok
        self.value_node = value_node
        self.pos_start = tok.pos_start
        self.pos_end = value_node.pos_end

    def __repr__(self):
        return f"{self.tok} = {self.value_node}"

class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
        self.pos_start = left_node.pos_start
        self.pos_end = right_node.pos_end

    def __repr__(self):
        return f"({self.left_node}, {self.op_tok}, {self.right_node})"

class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node
        self.pos_start = op_tok.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f"({self.op_tok}, {self.node})"

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count = 0

    def register_advancement(self):
        self.advance_count += 1

    def register(self, res):
        self.advance_count += res.advance_count
        if res.error: self.error = res.error
        return res.node
        
    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.advance_count == 0:
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
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '+', '-', '*', '/', '(', ')' or 'store'"))
        return res
    
    # Factor -> (Plus | Minus) Factor | Integer | Float | LParen Expr RParen
    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TOKEN_TYPE['Plus'], TOKEN_TYPE['Minus']):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))
        
        elif tok.type in (TOKEN_TYPE['Integer'], TOKEN_TYPE['Float']):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))

        elif tok.type == TOKEN_TYPE['Identifier']:
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(tok))

        elif tok.type == TOKEN_TYPE['LParen']:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error: return res
            if self.current_tok.type == TOKEN_TYPE['RParen']:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ')'"))
        
        return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected Integer, Float, Identifier, '+', '-' or '('"))
    
    # Term -> Factor ((Times | Div) Factor)*
    def term(self):
        return self.bin_op(self.factor, (TOKEN_TYPE['Times'], TOKEN_TYPE['Div']))
    
    # Expr  -> Keyword:store Identifier Eq Expr
    #       -> Term ((Plus | Minus) Term)*
    def expr(self):
        res = ParseResult()

        if self.current_tok.matches(TOKEN_TYPE["Keyword"], "store"):
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TOKEN_TYPE["Identifier"]:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected Identifier"))
            
            var_name = self.current_tok
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TOKEN_TYPE["Assign"]:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '='"))
            
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error: return res
            return res.success(VarAssignNode(var_name, expr))
        

        node = res.register(self.bin_op(self.term, (TOKEN_TYPE['Plus'], TOKEN_TYPE['Minus'])))

        if res.error:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected 'store', Integer, Float, Identifier, '+', '-' or '('"))
        
        return res.success(node)

    # BinOp -> LeftNode Op RightNode
    def bin_op(self, func, ops):
        res = ParseResult()
        left = res.register(func())
        if res.error: return res

        while self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            right = res.register(func())
            if res.error: return res
            left = BinOpNode(left, op_tok, right)
        
        return res.success(left)
            