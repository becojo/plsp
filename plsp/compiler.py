from parser import *
from peak.util.assembler import Code, Label
from analyser import LexicalAnalyser
import imp
import dis
import struct
import time
import marshal

def compile_pyc(code, buf):
    buf.write(imp.get_magic())
    buf.write(struct.pack('I', int(time.time())))
    marshal.dump(code, buf)


def compile(buf):
    lexer = Lexer(buf)
    parser = Parser(lexer)
    ast = parser.parse()

    atoms = ast.getPProgram().getAtom()
    code = Code()

    for atom in atoms:
        compile_atom(atom, code)

    code.LOAD_CONST(None)
    code.RETURN_VALUE()

    return code.code()

def load_const(atom, c):
    if isinstance(atom, ANumberAtom):
        n = atom.getNumber()

        if isinstance(n, AIntegerNumber):
            c.LOAD_CONST(int(n.getInteger().getText()))
            return True

        if isinstance(n, AFloatNumber):
            c.LOAD_CONST(float(n.getFloat().getText()))
            return True

        if isinstance(n, AHexNumber):
            c.LOAD_CONST(int(n.getHexNumber().getText()[2:], 16))
            return True

    if isinstance(atom, AStringAtom):
        c.LOAD_CONST(atom.getString().getText().strip('"'))
        return True

    return False


def load_var(atom, c):
    if isinstance(atom, AIdentifierAtom):
        var = atom.getIdentifier().getText()

        c.set_lineno(atom.getIdentifier().getLine())

        if var in ['True', 'False', 'None', 'raw_input', 'int', 'float', 'str', 'map', '__name__', 'getattr']:
            c.LOAD_GLOBAL(var)
        else:
            c.LOAD_FAST(var)

        return True

    return False


def load_value(atom, c):
    return load_const(atom, c) or load_var(atom, c) or compile_atom(atom, c)

def unpack_var(atom, code):
    if isinstance(atom, AIdentifierAtom):
        code.STORE_FAST(atom.getIdentifier().getText())

    elif isinstance(atom, AVectorAtom):
        codes = atom.getVector().getAtom()

        code.UNPACK_SEQUENCE(len(codes))

        for x in codes:
            unpack_var(x, code)


def compile_atom(atom, c):
    if isinstance(atom, AVectorAtom):
        values = atom.getVector().getAtom()

        for value in values:
            load_value(value, c)

        c.BUILD_LIST(len(values))
        return True


    if isinstance(atom, ADictAtom):
        values = atom.getDict().getAtom()
        n = len(values) / 2

        c.LOAD_GLOBAL('dict')
        for i in range(n):
            load_value(values[i * 2], c)
            load_value(values[i * 2 + 1], c)

        c.CALL_FUNCTION(0, n)
        return True


    if isinstance(atom, AListAtom):
        xs = atom.getList().getAtom()
        head = xs[0]

        if isinstance(head, AListAtom):
            for x in xs:
                load_value(x, c)

            c.CALL_FUNCTION(len(xs) - 1)

            return True

        if isinstance(head, AIdentifierAtom):
            fn = head.getIdentifier().getText()

            c.set_lineno(head.getIdentifier().getLine())

            if fn == 'def':
                var = xs[1].getIdentifier().getText()
                if load_value(xs[2], c):

                    c.STORE_FAST(var)
                    c.LOAD_CONST(var)
                    return True

            if fn == 'print':
                if load_value(xs[1], c):
                    c.PRINT_ITEM()
                    c.PRINT_NEWLINE()
                    c.LOAD_CONST(None)
                    return True

            if fn == 'ife':
                false_part = Label()
                finish = Label()

                load_value(xs[1], c) # eval condition

                c(false_part.JUMP_IF_FALSE)
                c.POP_TOP() # discard boolean result
                load_value(xs[2], c)
                c(finish.JUMP_ABSOLUTE)

                c(false_part)
                c.POP_TOP() # discard boolean result
                load_value(xs[3], c)

                c(finish)

                return True

            if fn == 'list':
                for x in xs[1:]:
                    load_value(x, c)

                c.BUILD_LIST(len(xs) - 1)

                return True


            if fn == 'for':
                pair = xs[1].getVector().getAtom()
                var = pair[0]
                ls = pair[1]
                body = xs[2]

                for_loop = Label()
                for_end = Label()

                load_value(ls, c)

                c.GET_ITER()
                c(for_loop)
                c(for_end.FOR_ITER)

                unpack_var(pair[0], c)

                load_value(body, c)

                c.POP_TOP()

                c(for_loop.JUMP_ABSOLUTE)
                c(for_end)

                return True


            if fn == 'defn':
                name = xs[1].getIdentifier().getText()
                arguments = xs[2].getVector().getAtom()
                body = xs[3]
                func_code = Code()

                func_code.co_argcount = len(arguments)
                func_code.co_varnames = [arg.getIdentifier().getText() for arg in arguments]

                load_value(body, func_code)

                func_code.RETURN_VALUE()

                c.LOAD_CONST(func_code.code())
                c.MAKE_FUNCTION(0)
                c.STORE_FAST(name)

                return True

            if fn == 'fn':
                arguments = xs[1].getVector().getAtom()
                body = xs[2]
                func_code = Code()

                func_code.co_argcount = len(arguments)
                func_code.co_varnames = [arg.getIdentifier().getText() for arg in arguments]
                # func_code.co_cellvars = []

                load_value(body, func_code)

                func_code.RETURN_VALUE()

                c.LOAD_CONST(func_code.code())
                c.MAKE_FUNCTION(0)

                return True

            if fn == 'import':
                name = xs[1].getIdentifier().getText()

                c.LOAD_CONST(-1)
                c.LOAD_CONST(None)
                c.IMPORT_NAME(name)
                c.STORE_FAST(name)

                return True

            if load_var(head, c):
                for x in xs[1:]:
                    load_value(x, c)

                c.CALL_FUNCTION(len(xs) - 1)
                return True

    return False
