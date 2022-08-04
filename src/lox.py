import sys
from . import error_handler as err
from .scanner import Scanner

class Lox:
    def run_file(self, path: str):
        with open(path, 'r') as f:
            source = f.read()
            self.__run(source)
            if err.had_error:
                sys.exit(65)

    def run_prompt(self):
        while True:
            try:
                line = input("> ")
                self.__run(line)
                err.had_error = False
            except EOFError:
                print("EOF")
                break

    def __run(self, source: str):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        for token in tokens:
            print(token)