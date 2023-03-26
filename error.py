class Error:
    def __init__(self, err_name, message, pos_start, pos_end):
        self.err_name = err_name
        self.message = message
        self.pos_start = pos_start
        self.pos_end = pos_end

    def _string_with_arrows(self, text, pos_start, pos_end):
        result = ''

        # Calculate indices
        idx_start = max(text.rfind('\n', 0, pos_start.idx), 0)
        idx_end = text.find('\n', idx_start + 1)
        if idx_end < 0: idx_end = len(text)

        # Generate each line
        line_count = pos_end.line - pos_start.line + 1
        for i in range(line_count):
            # Calculate line columns
            line = text[idx_start:idx_end]
            col_start = pos_start.col if i == 0 else 0
            col_end = pos_end.col if i == line_count - 1 else len(line) - 1

            # Append to result
            result += line + '\n'
            result += ' ' * col_start + '^' * (col_end - col_start)

            # Re-calculate indices
            idx_start = idx_end
            idx_end = text.find('\n', idx_start + 1)
            if idx_end < 0: idx_end = len(text)

        return result.replace('\t', '')

    def as_string(self):
        result = f'{self.err_name}: {self.message}\nFile: {self.pos_start.filename}, line {self.pos_start.line+1}'
        result += '\n\n' + self._string_with_arrows(self.pos_start.file_text, self.pos_start, self.pos_end)
        return result

class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, message):
        super().__init__('IllegalCharError', message, pos_start, pos_end)

class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, message=''):
        super().__init__('InvalidSyntaxError', message, pos_start, pos_end)