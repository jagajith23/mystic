# from fsm import FSM
from error import IllegalCharError
from token import Token, TOKEN_TYPE

DIGITS = '0123456789'

# class Lexer:
#     def __init__(self, inp):
#         self.inp = inp
#         self.pos = 0
#          0
#         self.col = 0
#         self.inp_len = len(self.inp)

#     def next_token(self):
#         if self.pos >= self.inp_len-1:
#             return Token(TOKEN_TYPE['EndOfInput'], None, self.col)

#         self.skip_whitespace_and_newlines()

#         char = self.inp[self.pos]

#         if char.isalpha() or char == '_':
#             return self.lex_identifier()

#         if char.isdigit():
#             return self.lex_number()
        
#         if char in ('+', '-', '*', '/'):
#             return self.lex_arithmetic_operator()

#         if char in ('=', '!', '<', '>'):
#             return self.lex_relational_operator()
        
#         if char in ('(', ')'):
#             return self.lex_parenthesis()

#         raise Exception('Invalid character: ' + char + ' at line: ' + str( 1) + ' col: ' + str(self.col + 1))

#     def skip_whitespace_and_newlines(self):
#         while self.pos < self.inp_len and self.inp[self.pos] in (' ', '\t', '\n'):            
#             if self.inp[self.pos] == '\n':
#                 = 1
#                 self.col = 0
#             else:
#                 self.col += 1

#             self.pos += 1

#     def lex_identifier(self):
#         pos = self.pos
#         line =          col = self.col
#         identifier = ''

#         while pos < self.inp_len:
#             char = self.inp[pos]
#             if not (char.isalpha() or char.isdigit() or char == '_'):
#                 break
#             identifier += char
#             pos += 1

#         self.pos += len(identifier)
#         self.col += len(identifier)

#         return Token(TOKEN_TYPE['Identifier'], identifier, line, col)

#     def lex_number(self):
#         pos = self.pos
#         line =          col = self.col

#         fsm = self.build_number_recognizer()
#         fsm_input = self.inp[pos:]

#         is_number_recognized, number = fsm.run(fsm_input)

#         if is_number_recognized:
#             self.pos += len(number)
#             self.col += len(number)
#             return Token(TOKEN_TYPE['Number'], number, line, col)
#         else:
#             if number == 'not a number':
#                 raise Exception('Invalid literal at line: ' + str(line) + ' col: ' + str(col))

    
#     def lex_arithmetic_operator(self):
#         pos = self.pos
#         line =          col = self.col
#         char = self.inp[pos]

#         self.pos += 1
#         self.col += 1

#         if char == '+':
#             return Token(TOKEN_TYPE['Plus'], '+', line, col)
#         elif char == '-':
#             return Token(TOKEN_TYPE['Minus'], '-', line, col)
#         elif char == '*':
#             return Token(TOKEN_TYPE['Times'], '*', line, col)
#         elif char == '/':
#             return Token(TOKEN_TYPE['Div'], '/', line, col)

#     def lex_relational_operator(self):
#         pos = self.pos
#         line =          col = self.col
#         char = self.inp[pos]

#         self.pos += 1
#         self.col += 1

#         lookahead = self.inp[pos + 1] if pos + 1 < self.inp_len else None
#         is_lookahead_valid = lookahead and lookahead == '='

#         if is_lookahead_valid:
#             self.pos += 1
#             self.col += 1
        
#         if char == '<':
#             if is_lookahead_valid:
#                 return Token(TOKEN_TYPE['LessThanOrEqual'], '<=', line, col)
#             return Token(TOKEN_TYPE['LessThan'], '<', line, col)
#         elif char == '>':
#             if is_lookahead_valid:
#                 return Token(TOKEN_TYPE['GreaterThanOrEqual'], '>=', line, col)
#             return Token(TOKEN_TYPE['GreaterThan'], '>', line, col)
#         elif char == '=':
#             if is_lookahead_valid:
#                 return Token(TOKEN_TYPE['Equal'], '==', line, col)
#             return Token(TOKEN_TYPE['Assign'], '=', line, col)    
    
#     def lex_parenthesis(self):
#         pos = self.pos
#         line =          col = self.col
#         char = self.inp[pos]

#         self.pos += 1
#         self.col += 1

#         if char == '(':
#             return Token(TOKEN_TYPE['LParen'], '(', line, col)
        
#         return Token(TOKEN_TYPE['RParen'], ')', line, col)

#     def build_number_recognizer(self):
#         state = {
#             "Initial": 1,
#             "Integer": 2,
#             "BeginWithFractionalPart": 3,
#             "NumberWithFractionalPart": 4,
#             "BeginNumberWithExponent": 5,
#             "BeginNumberWithSignedExponent": 6,
#             "NumberWithExponent": 7,
#             "NO_NEXT_STATE": -1,
#         }

#         states = [
#             state["Initial"],
#             state["Integer"],
#             state["BeginWithFractionalPart"],
#             state["NumberWithFractionalPart"],
#             state["BeginNumberWithExponent"],
#             state["BeginNumberWithSignedExponent"],
#             state["NumberWithExponent"],
#             state["NO_NEXT_STATE"],
#         ]
#         initial_state = state["Initial"]
#         accepting_states = [state["Integer"], state["NumberWithFractionalPart"], state["NumberWithExponent"]]
        
#         def next_state(curr_state, char):
#             if curr_state == state["Initial"]:
#                 if char.isdigit():
#                     return state["Integer"]
            
#             if curr_state == state["Integer"]:
#                 if char.isdigit():
#                     return state["Integer"]
#                 if char == '.':
#                     return state["BeginWithFractionalPart"]
#                 if char in ('e', 'E'):
#                     return state["BeginNumberWithExponent"]

#             if curr_state == state["BeginWithFractionalPart"]:
#                 if char.isdigit():
#                     return state["NumberWithFractionalPart"]

#             if curr_state == state["NumberWithFractionalPart"]:
#                 if char.isdigit():
#                     return state["NumberWithFractionalPart"]
#                 if char in ('e', 'E'):
#                     return state["BeginNumberWithExponent"]

#             if curr_state == state["BeginNumberWithExponent"]:
#                 if char.isdigit():
#                     return state["NumberWithExponent"]
#                 if char in ('+', '-'):
#                     return state["BeginNumberWithSignedExponent"]

#             if curr_state == state["BeginNumberWithSignedExponent"]:
#                 if char.isdigit():
#                     return state["NumberWithExponent"]

#             if curr_state == state["NumberWithExponent"]:
#                 if char.isdigit():
#                     return state["NumberWithExponent"]
            
#             return state["NO_NEXT_STATE"]

#         fsm = FSM(states, initial_state, accepting_states, next_state)
#         return fsm

#     def all_tokens(self):
#         token = self.next_token()
#         tokens = []
#         while token.type != TOKEN_TYPE['EndOfInput']:
#             tokens.append(token)
#             token = self.next_token()

#         return tokens

# lexer = Lexer('''int main()
#     int a = 5
#     int b = 6

#     return a + b
# ''')
# tokens = lexer.all_tokens()

# for token in tokens:
#     print(token.value, token.type)

class Position:
    def __init__(self, filename, file_text, idx, line, col):
        self.filename = filename
        self.file_text = file_text
        self.idx = idx
        self.line = line
        self.col = col
    
    def advance(self, current_char):
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
                tokens.append(Token(TOKEN_TYPE['Plus'], '+'))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TOKEN_TYPE['Minus'], '-'))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TOKEN_TYPE['Times'], '*'))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TOKEN_TYPE['Div'], '/'))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TOKEN_TYPE['LParen'], '('))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TOKEN_TYPE['RParen'], ')'))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(f"'{char}'", pos_start, self.pos)

        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()
        
        if dot_count == 0:
            return Token(TOKEN_TYPE['Integer'], int(num_str))
        else:
            return Token(TOKEN_TYPE['Float'], float(num_str))