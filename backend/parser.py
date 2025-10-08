# parser.py
import ply.yacc as yacc
import ast as _ast
from lexer import tokens  # tokens must be defined in lexer.py

# -------------------------
# AST node classes
# -------------------------
class Program:
    def __init__(self, statements):
        self.statements = statements
    def __repr__(self):
        return f"Program({self.statements})"

class Assign:
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr
    def __repr__(self):
        return f"Assign({self.name}, {self.expr})"

class Print:
    def __init__(self, expr):
        self.expr = expr
    def __repr__(self):
        return f"Print({self.expr})"

class If:
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch  # list of statements
        self.else_branch = else_branch  # list of statements or nested If
    def __repr__(self):
        return f"If({self.condition}, {self.then_branch}, {self.else_branch})"

class While:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    def __repr__(self):
        return f"While({self.condition}, {self.body})"

class For:
    def __init__(self, var, count, body):
        self.var = var      # variable name
        self.count = count  # upper bound (int)
        self.body = body    # list of statements
    def __repr__(self):
        return f"For({self.var}, range({self.count}), {self.body})"

class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def __repr__(self):
        return f"BinOp({self.left}, {self.op}, {self.right})"

class UnaryOp:
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand
    def __repr__(self):
        return f"UnaryOp({self.op}, {self.operand})"

class Var:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"Var({self.name})"

class Number:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Number({self.value})"

class Boolean:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Boolean({self.value})"

class String:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"String({self.value!r})"

class Null:
    def __repr__(self):
        return "Null()"

# -------------------------
# Precedence (to reduce conflicts)
# -------------------------
precedence = (
    ('left', 'EQ', 'NEQ', 'LT', 'LEQ', 'GT', 'GEQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),
)

# -------------------------
# Grammar rules
# -------------------------

def p_program(p):
    "program : statement_list_opt"
    # p[1] is a list
    p[0] = Program(p[1])

def p_statement_list_opt(p):
    """statement_list_opt : statement_list
                          | empty"""
    p[0] = p[1] if p[1] is not None else []

def p_statement_list(p):
    """statement_list : statement_list statement
                      | statement"""
    if len(p) == 3:
        lst = p[1]
        stmt = p[2]
        # skip None statements (comments)
        if stmt is not None:
            p[0] = lst + [stmt]
        else:
            p[0] = lst
    else:
        stmt = p[1]
        p[0] = [] if stmt is None else [stmt]

# statement can be one of several nodes; comments produce None
def p_statement(p):
    """statement : assignment
                 | print_stmt
                 | if_stmt
                 | while_stmt
                 | for_stmt
                 | COMMENT"""
    # if COMMENT, ignore it (returns None)
    if p.slice[1].type == 'COMMENT':
        p[0] = None
    else:
        p[0] = p[1]

# assignment: IDENTIFIER = expression
def p_assignment(p):
    "assignment : IDENTIFIER EQUALS expression"
    p[0] = Assign(p[1], p[3])

# print: print(expr)
def p_print_stmt(p):
    "print_stmt : PRINT LPAREN expression RPAREN"
    p[0] = Print(p[3])

# if / elseif / else with block braces { }
def p_if_stmt(p):
    """
    if_stmt : IF expression BLOCK_START statement_list_opt BLOCK_END elif_list else_part
    """
    cond = p[2]
    then_branch = p[4]
    elifs = p[6]      # list of (cond, body) tuples or []
    else_branch = p[7]  # either None or list

    # Fold elifs into nested Ifs so representation is simple:
    current_else = else_branch
    # build from last to first
    for econd, ebody in reversed(elifs):
        current_else = [If(econd, ebody, current_else)]
    p[0] = If(cond, then_branch, current_else)

def p_elif_list_empty(p):
    "elif_list : empty"
    p[0] = []

def p_elif_list_one(p):
    "elif_list : ELSEIF expression BLOCK_START statement_list_opt BLOCK_END"
    p[0] = [(p[2], p[4])]

def p_elif_list_many(p):
    "elif_list : elif_list ELSEIF expression BLOCK_START statement_list_opt BLOCK_END"
    p[0] = p[1] + [(p[3], p[5])]

def p_else_part_empty(p):
    "else_part : empty"
    p[0] = None

def p_else_part(p):
    "else_part : ELSE BLOCK_START statement_list_opt BLOCK_END"
    p[0] = p[3]

# while
def p_while_stmt(p):
    "while_stmt : WHILE expression BLOCK_START statement_list_opt BLOCK_END"
    p[0] = While(p[2], p[4])

# for (Python-like): for IDENTIFIER in range(NUMBER) { body }
def p_for_stmt(p):
    "for_stmt : FOR IDENTIFIER IN RANGE LPAREN NUMBER RPAREN BLOCK_START statement_list_opt BLOCK_END"
    # Equivalent to: for i in range(5) { body }
    var_name = p[2]
    count = int(p[6])  # NUMBER
    p[0] = For(var_name, count, p[9])

# -------------------------
# Expressions
# -------------------------
def p_expression_binop(p):
    """expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression EQ expression
                  | expression NEQ expression
                  | expression LT expression
                  | expression LEQ expression
                  | expression GT expression
                  | expression GEQ expression"""
    p[0] = BinOp(p[1], p[2], p[3])

def p_expression_uminus(p):
    "expression : MINUS expression %prec UMINUS"
    p[0] = UnaryOp('-', p[2])

def p_expression_group(p):
    "expression : LPAREN expression RPAREN"
    p[0] = p[2]

def p_expression_number(p):
    "expression : NUMBER"
    # NUMBER token value may be string; try to convert
    try:
        if isinstance(p[1], (int, float)):
            val = p[1]
        elif isinstance(p[1], str) and '.' in p[1]:
            val = float(p[1])
        else:
            val = int(p[1])
    except Exception:
        # fallback: keep raw
        val = p[1]
    p[0] = Number(val)

def p_expression_boolean(p):
    "expression : BOOLEAN"
    # token value expected 'true' or 'false' (string)
    val = True if str(p[1]).lower() == "true" else False
    p[0] = Boolean(val)

def p_expression_null(p):
    "expression : NULL"
    p[0] = Null()

def p_expression_string(p):
    "expression : STRING"
    # STRING token from lexer has quotes. Use ast.literal_eval to unescape safely
    try:
        s = _ast.literal_eval(p[1])
    except Exception:
        # fallback: strip quotes if present
        s = p[1][1:-1] if len(p[1]) >= 2 else p[1]
    p[0] = String(s)

def p_expression_var(p):
    "expression : IDENTIFIER"
    p[0] = Var(p[1])

# -------------------------
# Helpers & error
# -------------------------
def p_empty(p):
    "empty :"
    p[0] = None
    
def p_error(p):
    if p:
        lineno = getattr(p, "lineno", "?")
        lexpos = getattr(p, "lexpos", -1)
        raise SyntaxError(f"Syntax error at token {p.type!r}, value {p.value!r}, line {lineno}, pos {lexpos}")
    else:
        raise SyntaxError("Unexpected end of input")


def ast_to_dict(node):
    """Convert AST objects into simple dicts/lists for JSON serialization."""
    if node is None:
        return None
    if isinstance(node, list):
        return [ast_to_dict(n) for n in node]
    # primitive (string, number, bool)
    if isinstance(node, (str, int, float, bool)):
        return node
    # objects with attributes
    if hasattr(node, "__dict__"):
        data = {}
        for k, v in vars(node).items():
            data[k] = ast_to_dict(v)
        return {node.__class__.__name__: data}
    # fallback
    return str(node)


# Build the parser
parser = yacc.yacc()
