import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

had_error = False

def report(line: int, where: str, message: str):
    eprint("[line " + str(line) + "] Error" + where + ": " + message)    
    had_error = True
def error(line: int, message: str):
    report(line, "", message)