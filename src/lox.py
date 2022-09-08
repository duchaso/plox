import sys
from . import error_handler as err
from .scanner import Scanner
from .parser import Parser
from .ast_printer import AstPrinter
from .interpreter import Interpreter

class Lox:
    interpreter = Interpreter()

    def run_file(self, path: str):
        with open(path, 'r') as f:
            source = f.read()
            self.__run(source)
            if err.had_error: sys.exit(65)
            if err.had_runtime_error: sys.exit(70) 

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

        parser = Parser(tokens)
        expression = parser.parse()

        if err.had_error: return

        Lox.interpreter.interpret(expression)
        # print(Interpreter().evaluate(expression))
        # print(AstPrinter().print(expression))