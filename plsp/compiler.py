from parser import Parser
from lexer import Lexer
from peak.util.assembler import Code, Label
import prelude


class Compiler:
    def __init__(self, ast, filename='<eval>'):
        self.ast = ast
        self.code = Code()
        self.code.co_filename = filename

        self.code.LOAD_CONST(None)

        for atom in self.ast:
            self.compile(atom)

        self.code.RETURN_VALUE()

    def compile(self, atom):
        if isinstance(atom, list):
            head = atom[0]
            args = atom[1:]

            if isinstance(head, prelude.symbol):
                if head.name == 'print':
                    self.compile(args[0])
                    self.code.PRINT_ITEM()
                    self.code.PRINT_NEWLINE()

                    return True


        if isinstance(atom, int) or isinstance(atom, float) or isinstance(atom, str):
            self.code.LOAD_CONST(atom)
            return True
