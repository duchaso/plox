import sys

from runtime_err import RuntimeErr

had_error = False
had_runtime_error = False

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def report(line: int, where: str, message: str):
    eprint("[line " + str(line) + "] Error" + where + ": " + message)    
    had_error = True

def error(line: int, message: str):
    report(line, "", message)

def runtime_error(error: RuntimeErr) -> None:
    eprint(str(error) + "\n[line " + error.token.line + "]")    
    had_runtime_error = True