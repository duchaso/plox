from .tok import Token
from .token_type import TokenType
from . import error_handler as err

class Scanner:
    def __init__(self, source: str) -> None:
        self.source = source
        self.tokens = list()

        self.start = 0
        self.current = 0
        self.line = 1

        self.keywords = {
            "and":    TokenType.AND,
            "class":  TokenType.CLASS,
            "else":   TokenType.ELSE,
            "false":  TokenType.FALSE,
            "for":    TokenType.FOR,
            "fun":    TokenType.FUN,
            "if":     TokenType.IF ,
            "nil":    TokenType.NIL,
            "or":     TokenType.OR ,
            "print":  TokenType.PRINT,
            "return": TokenType.RETURN,
            "super":  TokenType.SUPER,
            "this":   TokenType.THIS,
            "true":   TokenType.TRUE,
            "var":    TokenType.VAR,
            "while":  TokenType.WHILE,
        }
    
    def scan_tokens(self) -> list:
        while not self.end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line)) 
        return self.tokens

    def scan_token(self):
        c = self.advance()
        match c:
            case '(': self.add_token(TokenType.LEFT_PAREN) 
            case ')': self.add_token(TokenType.RIGHT_PAREN) 
            case '{': self.add_token(TokenType.LEFT_BRACE) 
            case '}': self.add_token(TokenType.RIGHT_BRACE) 
            case ',': self.add_token(TokenType.COMMA) 
            case '.': self.add_token(TokenType.DOT) 
            case '-': self.add_token(TokenType.MINUS) 
            case '+': self.add_token(TokenType.PLUS) 
            case ';': self.add_token(TokenType.SEMICOLON); 
            case '*': self.add_token(TokenType.STAR) 

            case '!': self.add_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
            case '=': self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
            case '<': self.add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
            case '>': self.add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)

            case '/':
                if self.match('/'):
                    while self.peek() != '\n' and not self.end(): self.advance()
                else:
                    self.add_token(TokenType.SLASH)

            case ' ' | '\r' | '\t': pass
            case '\n': self.line += 1

            case '"': self.string()

            case _  : 
                if self.is_digit(c): self.number()
                elif self.is_alpha(c): self.identifier()
                else: err.error(self.line, "Unexpected character.")

    def identifier(self):
        while self.is_alphanumeric(self.peek()): self.advance()

        text = self.source[self.start:self.current]

        type = TokenType.IDENTIFIER if text not in self.keywords else self.keywords[text]

        self.add_token(type)

    def number(self):
        while self.is_digit(self.peek()): self.advance()

        if self.peek() == '.' and self.is_digit(self.peek_next()): 
            self.advance()
            while self.is_digit(self.peek()): self.advance()

        self.add_token(TokenType.NUMBER, float(self.source[self.start : self.current]))


    def string(self):
        while self.peek() != '"' and not self.end():
            if self.peek() == '\n': self.line += 1
            self.advance()

        if self.end():
            err.error(self.line, "Unterminated string.")
            return

        self.advance()

        value = self.source[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, value)

    def is_alpha(self, c: str) -> bool:
        return c >= 'a' and c <= 'z' or c >= 'A' and c <= 'Z' or c == '_'

    def is_alphanumeric(self, c: str) -> bool:
        return self.is_alpha(c) or self.is_digit(c)

    def is_digit(self, c: str) -> bool:
        return c >= '0' and c <= '9'

    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]
    
    def match(self, expected: str) -> bool:
        if self.end(): return False
        if self.source[self.current] != expected: return False

        self.current += 1
        return True

    def peek(self) -> str:
        if self.end(): return '\0'
        return self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source): return '\0'
        return self.source[self.current + 1]
    
    def add_token(self, type: TokenType, literal: object = None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def end(self) -> bool:
        return self.current >= len(self.source)