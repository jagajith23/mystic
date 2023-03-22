class Error:
    def __init__(self, err_name, message, pos_start, pos_end):
        self.err_name = err_name
        self.message = message
        self.pos_start = pos_start
        self.pos_end = pos_end

    def as_string(self):
        return f'{self.err_name}: {self.message}\nFile: {self.pos_start.filename}, line {self.pos_start.line+1}'

class IllegalCharError(Error):
    def __init__(self, message, pos_start, pos_end):
        super().__init__('IllegalCharError', message, pos_start, pos_end)