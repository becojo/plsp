from unittest import TestCase

from plsp.lexer import Lexer

class LexerTest(TestCase):
    def test_simple_string(self):
        l = Lexer('"a simple string"')
        l.run()

        self.assertEqual(l.tokens[0]['type'], 'STRING')
        self.assertEqual(l.tokens[0]['value'], 'a simple string')

    def test_escape_quote(self):
        l = Lexer('"a simple \\\"string"')
        l.run()

        self.assertEqual(l.tokens[0]['value'], 'a simple "string')

    def test_integers(self):
        cases = ['1209381209', '-23948302984023', '1203982L', '-132901823L']

        for case in cases:
            l = Lexer(case)
            l.run()

            self.assertEqual(l.tokens[0]['type'], 'INTEGER')
            self.assertEqual(l.tokens[0]['value'], case)


    def test_floats(self):
        cases = ['1234.12341324', '-324134.12431342']

        for case in cases:
            l = Lexer(case)
            l.run()
            
            self.assertEqual(l.tokens[0]['type'], 'FLOAT')
            self.assertEqual(l.tokens[0]['value'], case)
