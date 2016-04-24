import re

class Lexer:
    def __init__(self, buffer):
        self.buffer = buffer
        self.index = 0
        self.tokens = []
        self.line = 0

    def is_eof(self):
        return self.index >= len(self.buffer)

    def run(self):
        while not self.is_eof():
            c = self.buffer[self.index]

            if c == '(':
                self.tokens.append({ 'type': 'OPEN_PAREN' })
                self.index += 1
            elif c == ')':
                self.tokens.append({ 'type': 'CLOSE_PAREN' })
                self.index += 1

            elif c == '"':
                self.read_string()

            elif self.read_float() or self.read_integer() or self.read_symbol():
                pass

            elif c.isspace():
                while self.buffer[self.index].isspace():
                    self.index += 1

            else:
                break

    def read_integer(self):
        match = re.match('^(-?[0-9]+L?)\s*', self.buffer[self.index:])
        match = match and match.group(1)

        if match:
            self.index += len(match)
            self.tokens.append({ 'type': 'INTEGER', 'value': match })
            return True

        return False

    def read_float(self):
        match = re.match('^(-?[0-9]+\.[0-9]+)\s*', self.buffer[self.index:])
        match = match and match.group(1)

        if match:
            self.index += len(match)
            self.tokens.append({ 'type': 'FLOAT', 'value': match })
            return True

        return False

    def read_string(self):
        escape = False
        value = ''

        self.index += 1

        while not self.is_eof():
            c = self.buffer[self.index]

            if c == '"':
                if escape:
                    value += '"'
                    escape = False
                else:
                    self.index += 1 # skip ending quote
                    self.tokens.append({ 'type': 'STRING', 'value': value })
                    return True

            elif c == '\\':
                escape = True
            else:
                value += c
                escape = False

            self.index += 1

    def read_symbol(self):
        match = re.match('^([a-zA-Z0-9\+\-\?\*/]+)\s*', self.buffer[self.index:])
        match = match and match.group(1)

        if match:
            self.index += len(match)
            self.tokens.append({ 'type': 'SYMBOL', 'value': match })
            return True

        return False
