import readline
from StringIO import StringIO
import plsp.compiler
import traceback


def repl():

    while True:
        try:
            cmd = raw_input('>>> ')
            finished = False

            while not finished:
                # try parsing command
                try:
                    buf = StringIO(cmd)
                    code = plsp.compiler.compile(buf, '<stdin>', False)
                    finished = True

                except Exception:
                    # if it fails, continue reading
                    try:
                        cmd += "\n" + raw_input('... ')
                    except KeyboardInterrupt:
                        print
                        break

                try:
                    print repr(eval(code))
                except Exception:
                    traceback.print_exc()

        except (KeyboardInterrupt, EOFError):
            print ''
            break
