from unittest import TestCase

from plsp.lexer import Lexer

class LexerTest(TestCase):
    def test_simple_string(self):
        l = Lexer('"a simple string"')
        l.run()

        self.assertEqual(l.tokens[0]['type'], 'STRING')
        self.assertEqual(l.tokens[0]['value'], 'a simple string')
        self.assertEqual(len(l.tokens), 1)

    def test_escape_quote(self):
        l = Lexer('"a simple \\\"string"')
        l.run()

        self.assertEqual(l.tokens[0]['type'], 'STRING')
        self.assertEqual(l.tokens[0]['value'], 'a simple "string')
        self.assertEqual(len(l.tokens), 1)

    def test_integers(self):
        cases = ['1209381209', '-23948302984023', '1203982L', '-132901823L']

        for case in cases:
            l = Lexer(case)
            l.run()

            self.assertEqual(l.tokens[0]['type'], 'INTEGER')
            self.assertEqual(l.tokens[0]['value'], case)
            self.assertEqual(len(l.tokens), 1)


    def test_floats(self):
        cases = ['1234.12341324', '-324134.12431342']

        for case in cases:
            l = Lexer(case)
            l.run()

            self.assertEqual(l.tokens[0]['type'], 'FLOAT')
            self.assertEqual(l.tokens[0]['value'], case)
            self.assertEqual(len(l.tokens), 1)

    def test_lists(self):
        cases = [('(1 2)', [{'type': 'OPEN_PAREN'}, {'type': 'INTEGER', 'value': '1'}, {'type': 'INTEGER', 'value': '2'}, {'type': 'CLOSE_PAREN'}]),
                 ('(())', [{'type': 'OPEN_PAREN'}, {'type': 'OPEN_PAREN'}, {'type': 'CLOSE_PAREN'}, {'type': 'CLOSE_PAREN'}]),
                 ('(print "hello world")', [{'type': 'OPEN_PAREN'}, {'type': 'SYMBOL', 'value': 'print'}, {'type': 'STRING', 'value': 'hello world'}, {'type': 'CLOSE_PAREN'}])]

        for input, output in cases:
            l = Lexer(input)
            l.run()

            self.assertEqual(l.tokens, output)

    def test_symbols(self):
        cases = [('predicate?', [{'type': 'SYMBOL', 'value': 'predicate?'}]),
                 ('+', [{'type': 'SYMBOL', 'value': '+'}]),
                 ('asdfASDF203948*4?+/', [{'type': 'SYMBOL', 'value': 'asdfASDF203948*4?+/'}]),
                 ('symbol1 symbol2', [{'type': 'SYMBOL', 'value': 'symbol1'}, {'type': 'SYMBOL', 'value': 'symbol2'}])]

        for input, output in cases:
            l = Lexer(input)
            l.run()

            self.assertEqual(l.tokens, output)
