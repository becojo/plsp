import ast
from plsp.prelude import symbol, quote

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        self.program = []

    def run(self):
        pass

    def is_eof(self):
        return self.index >= len(self.tokens)

    def parse(self):
        if self.is_eof():
            return None

        tok = self.tokens[self.index]

        if tok['type'] == 'OPEN_PAREN':
            return self.read_list('CLOSE_PAREN')

        if tok['type'] == 'OPEN_LIST':
            return quote(self.read_list('CLOSE_LIST'))

        elif tok['type'] == 'SYMBOL':
            self.index += 1
            return symbol(tok['value'])

        elif tok['type'] == 'STRING':
            self.index += 1
            return tok['value']

        self.index += 1
        return ast.literal_eval(tok['value'])


    def read_list(self, ending):
        values = []

        self.index += 1

        while not self.is_eof() and self.tokens[self.index]['type'] != ending:
            values.append(self.parse())

        return values
