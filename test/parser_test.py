from unittest import TestCase

from plsp.lexer import Lexer
from plsp.parser import Parser
from plsp.prelude import symbol


class ParserTest(TestCase):
    def parse(self, input):
        l = Lexer(input)
        l.run()
        p = Parser(l.tokens)

        return p.parse()


    def test_lists(self):
        cases = [('(1 2 3)', [1, 2, 3]),
                 ('("hello" true 93456)', ["hello", symbol('true'), 93456]),
                 ('(1 (2 (3 (4))))', [1,[2,[3,[4]]]]),
                 ('((((()))))', [[[[[]]]]])]

        for input, output in cases:
            self.assertEqual(self.parse(input), output)
