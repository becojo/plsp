from parser import *
from peak.util.assembler import Code, Label
from analyser import SemanticAnalyser
import imp
import dis
import struct
import time
import marshal

def compile_pyc(code, buf):
    buf.write(imp.get_magic())
    buf.write(struct.pack('I', int(time.time())))
    marshal.dump(code, buf)


def compile(buf, filename, add_return=False):
    lexer = Lexer(buf)
    parser = Parser(lexer)
    ast = parser.parse()

    ast.apply(SemanticAnalyser())

    atoms = ast.getPProgram().getAtom()
    code = Code()

    code.co_filename = filename

    code.LOAD_CONST(None)

    for atom in atoms:
        load_value(atom, code)

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

        if hasattr(atom, 'scope') and atom.scope == 'local':
            c.LOAD_FAST(var)
        else:
            c.LOAD_GLOBAL(var)

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

                    c.STORE_GLOBAL(var)
                    c.LOAD_CONST(var)
                    return True

            if fn == 'print':
                if load_value(xs[1], c):
                    c.PRINT_ITEM()
                    c.PRINT_NEWLINE()
                    c.LOAD_CONST(None)
                    return True

            if fn == 'if' or fn == 'ife':
                false_part = Label()
                finish = Label()

                load_value(xs[1], c) # eval condition

                c(false_part.JUMP_IF_FALSE)
                c.POP_TOP() # discard boolean result
                load_value(xs[2], c)
                c(finish.JUMP_ABSOLUTE)

                c(false_part)
                c.POP_TOP() # discard boolean result

                if len(xs) == 4:
                    load_value(xs[3], c)
                else:
                    c.LOAD_CONST(None)

                c(finish)

                return True

            if fn == 'let':
                pair = xs[1].getVector().getAtom()
                body = xs[2]
                n = len(pair) / 2

                for i in range(n):
                    load_value(pair[i * 2 + 1], c)
                    print pair[i * 2]
                    unpack_var(pair[i * 2], c)

                load_value(body, c)

                # todo: DELETE_FAST

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

                func_code.co_filename = c.co_filename
                func_code.co_name = name
                func_code.co_argcount = len(arguments)
                func_code.co_varnames = [arg.getIdentifier().getText() for arg in arguments]

                load_value(body, func_code)

                func_code.RETURN_VALUE()

                c.LOAD_CONST(func_code.code())
                c.MAKE_FUNCTION(0)
                c.STORE_GLOBAL(name)

                c.LOAD_CONST(name)

                return True

            if fn == 'fn':
                arguments = xs[1].getVector().getAtom()
                body = xs[2]
                func_code = Code()

                func_code.co_filename = c.co_filename
                func_code.co_argcount = len(arguments)
                func_code.co_varnames = [arg.getIdentifier().getText() for arg in arguments]
                # func_code.co_cellvars = []

                load_value(body, func_code)

                func_code.RETURN_VALUE()

                c.LOAD_CONST(func_code.code())
                c.MAKE_FUNCTION(0)

                return True

            if fn == 'import':
                pkg = xs[1].getIdentifier().getText()

                c.LOAD_CONST(-1)

                if len(xs) == 3:

                   names = [t.getIdentifier().getText() for t in xs[2].getVector().getAtom()]
                   imports = tuple(names)

                   c.LOAD_CONST(imports)
                   c.IMPORT_NAME(pkg)

                   for name in names:
                       c.IMPORT_FROM(name)
                       c.STORE_GLOBAL(name)

                else:
                    c.LOAD_CONST(None)
                    c.IMPORT_NAME(pkg)
                    c.STORE_GLOBAL(pkg)

                return True

            if fn == '.':
                if isinstance(xs[1], AIdentifierAtom):
                    load_value(xs[2], c)
                    c.LOAD_ATTR(xs[1].getIdentifier().getText())
                else:
                    c.LOAD_GLOBAL('getattr')
                    load_value(xs[2], c)
                    load_value(xs[1], c)
                    c.CALL_FUNCTION(2)

                return True

            if fn == 'exec':
                load_value(xs[1], c)
                c.MAKE_FUNCTION(0)
                c.CALL_FUNCTION(0)
                return True

            if load_var(head, c):
                for x in xs[1:]:
                    load_value(x, c)

                c.CALL_FUNCTION(len(xs) - 1)
                return True

    return False
