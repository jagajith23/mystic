from error import IllegalCharError
from token import Token, TOKEN_TYPE

DIGITS = '0123456789'

class Position:
    def __init__(self, filename, file_text, idx, line, col):
        self.filename = filename
        self.file_text = file_text
        self.idx = idx
        self.line = line
        self.col = col
    
    def advance(self, current_char=None):
        self.idx+=1
        self.col+=1

        if current_char == '\n':
            self.line+=1
            self.col=0
        return self

    def copy(self):
        return Position(self.filename, self.file_text, self.idx, self.line, self.col)

class Lexer:
    def __init__(self, filename, text):
        self.filename = filename
        self.text = text
        self.pos = Position(self.filename, self.text, -1, 0, -1)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ['\t', ' ']:
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(TOKEN_TYPE['Plus'], '+', pos_start=self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TOKEN_TYPE['Minus'], '-', pos_start=self.pos))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TOKEN_TYPE['Times'], '*', pos_start=self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TOKEN_TYPE['Div'], '/', pos_start=self.pos))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TOKEN_TYPE['LParen'], '(', pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TOKEN_TYPE['RParen'], ')', pos_start=self.pos))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, f"'{char}'")

        tokens.append(Token(TOKEN_TYPE['EOF'], None, pos_start=self.pos))
        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()
        
        if dot_count == 0:
            return Token(TOKEN_TYPE['Integer'], int(num_str), pos_start=pos_start, pos_end=self.pos)
        else:
            return Token(TOKEN_TYPE['Float'], float(num_str), pos_start=pos_start, pos_end=self.pos)