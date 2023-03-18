NO_NEXT_STATE = -1

class FSM:
    def __init__(self, states, initial_state, accepting_states, next_state):
        self.states = states
        self.initial_state = initial_state
        self.accepting_states = accepting_states
        self.next_state = next_state
        self.curr_pos = 0

    def run(self, inp):
        curr_state = self.initial_state

        for idx in range(len(inp)):
            char = inp[idx]
            next_state = self.next_state(curr_state, char)
            self.curr_pos += 1
            if next_state == NO_NEXT_STATE:
                if char.isalpha() and inp[idx-1].isdigit():
                    return (False, 'not a number')
                elif char =='\n':
                    self.curr_pos -= 1
                break
            curr_state = next_state
        
        number = inp[:self.curr_pos]
        return (curr_state in self.accepting_states, number)


