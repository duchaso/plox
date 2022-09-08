from .expr import *
from .token_type import TokenType
from .runtime_err import RuntimeErr

class Interpreter(Visitor):
    def interpret(self, expression: Expr) -> None:
        try:
            value = self.evaluate(expression)
            print(self.stringify(value))
        except RuntimeErr as error:
            pass

    def stringify(self, object: object) -> str:
        if object is None: return "nil"

        if isinstance(object, float):
            text = str(object)
            if text.endswith(".0"):
                text = text[:len(text) - 2]
            return text

        return str(object)
    
    def visit_binary_expr(self, expr: Binary) -> object:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.BANG_EQUAL:
                return not self.is_eq(left, right)
            case TokenType.EQUAL_EQUAL:
                return self.is_eq(left, right)

            case TokenType.GREATER:
                self.check_number_operands(expr.operator, left, right)
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return float(left) >= float(right)
            case TokenType.LESS:
                self.check_number_operands(expr.operator, left, right)
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return float(left) <= float(right)
            
            case TokenType.MINUS:
                self.check_number_operands(expr.operator, left, right)
                return float(left) - float(right)
            case TokenType.SLASH:
                self.check_number_operands(expr.operator, left, right)
                return float(left) / float(right)
            case TokenType.STAR:
                self.check_number_operands(expr.operator, left, right)
                return float(left) * float(right)
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) + float(right)
                if isinstance(left, str) and isinstance(right, str):
                    return str(left) + str(right)
                raise RuntimeErr(expr.operator, "Operands must be two numbers or two strings.")

    def visit_grouping_expr(self, expr: Grouping) -> object:
        return self.evaluate(expr.expression)

    def visit_literal_expr(self, expr: Literal) -> object:
        return expr.value

    def visit_unary_expr(self, expr: Unary) -> object:
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.MINUS: 
                self.check_number_operand(expr.operator, right)
                return -float(right)
            case TokenType.BANG: return not self.is_truthy(right)

        #Unreachable.
        return None
        

    def evaluate(self, expr: Expr) -> object:
        return expr.accept(self)

    def is_truthy(self, obj: object) -> bool:
        if obj == None: return False
        if isinstance(obj, bool): return bool(obj)
        return True

    def is_eq(self, a: object, b: object) -> bool:
        if a == None and b == None: return True
        if a == None: return False

        return a == b

    def check_number_operand(self, operator: Token, operand: object) -> None:
        if isinstance(operand, float): return
        raise RuntimeErr(operator, "Operand must be a number.")
    
    def check_number_operands(self, operator: Token, left: object, right: object) -> None:
        if (isinstance(left, float) and isinstance(right, float)): return
        raise RuntimeErr(operator, "Operands must be numbers.")