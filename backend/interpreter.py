# interpreter.py

from parser import (
    Program, Assign, Print, If, While, For,
    BinOp, UnaryOp, Var, Number, Boolean, String, Null
)

# -------------------------
# Environment (variable storage)
# -------------------------
class Environment:
    def __init__(self):
        self.vars = {}

    def get(self, name):
        if name not in self.vars:
            raise NameError(f"Variable '{name}' not defined")
        return self.vars[name]

    def set(self, name, value):
        self.vars[name] = value


# -------------------------
# Interpreter
# -------------------------
class Interpreter:
    def __init__(self):
        self.env = Environment()
        self.output = []  # on stocke les résultats des print()

    def run(self, program: Program):
        """Exécute un programme et retourne une liste des sorties (print)."""
        self.output = []
        for stmt in program.statements:
            self.exec_stmt(stmt)
        return self.output

    def exec_stmt(self, stmt):
        if isinstance(stmt, Assign):
            value = self.eval_expr(stmt.expr)
            self.env.set(stmt.name, value)

        elif isinstance(stmt, Print):
            value = self.eval_expr(stmt.expr)
            self.output.append(value)  # stocker la sortie
            print(value)               # conserver l’affichage console

        elif isinstance(stmt, If):
            cond = self.eval_expr(stmt.condition)
            if cond:
                for s in stmt.then_branch:
                    self.exec_stmt(s)
            elif stmt.else_branch:
                for s in stmt.else_branch:
                    self.exec_stmt(s)

        elif isinstance(stmt, While):
            while self.eval_expr(stmt.condition):
                for s in stmt.body:
                    self.exec_stmt(s)

        elif isinstance(stmt, For):
            for i in range(stmt.count):
                self.env.set(stmt.var, i)
                for s in stmt.body:
                    self.exec_stmt(s)

        else:
            raise RuntimeError(f"Unknown statement: {stmt}")

    # -------------------------
    # Expression evaluation
    # -------------------------
    def eval_expr(self, expr):
        if isinstance(expr, Number):
            return expr.value
        elif isinstance(expr, Boolean):
            return expr.value
        elif isinstance(expr, String):
            return expr.value
        elif isinstance(expr, Null):
            return None
        elif isinstance(expr, Var):
            return self.env.get(expr.name)

        elif isinstance(expr, BinOp):
            left = self.eval_expr(expr.left)
            right = self.eval_expr(expr.right)
            if expr.op == '+': return left + right
            if expr.op == '-': return left - right
            if expr.op == '*': return left * right
            if expr.op == '/':
                if right == 0:
                    raise RuntimeError("Division by zero")
                return left / right
            if expr.op == '==': return left == right
            if expr.op == '!=': return left != right
            if expr.op == '<': return left < right
            if expr.op == '<=': return left <= right
            if expr.op == '>': return left > right
            if expr.op == '>=': return left >= right
            raise RuntimeError(f"Unknown binary operator {expr.op}")

        elif isinstance(expr, UnaryOp):
            val = self.eval_expr(expr.operand)
            if expr.op == '-': return -val
            raise RuntimeError(f"Unknown unary operator {expr.op}")

        else:
            raise RuntimeError(f"Unknown expression: {expr}")


# -------------------------
# Manual test (only if run directly)
# -------------------------
if __name__ == "__main__":
    from lexer import lexer
    from parser import parser

    code = """
    a = 5
    b = 3
    a = a + b
    print(a)
    """

    ast = parser.parse(code, lexer=lexer)
    interpreter = Interpreter()
    result = interpreter.run(ast)

    print("\n=== Résultats collectés ===")
    print(result)
