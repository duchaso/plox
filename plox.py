import sys
# from src.lox import Lox
import src.lox as lox

if __name__ == "__main__":
    argc = len(sys.argv)
    lox = lox.Lox()
    if argc > 2:
        print("Usage: plox [script]")
        sys.exit(64)
    elif argc == 2:
        lox.run_file(path=sys.argv[1])
    else:
        lox.run_prompt()