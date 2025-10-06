from ply import lex
from ply import yacc

tokens = [
    # Operators
    'PLUS',                 # +
    'MINUS',                # -
    'TIMES',                # *
    'DIVIDE',               # /
    'EQUALS',               # =

    # Comparisons
    'EQ',                   # ==
    'NEQ',                  # !=
    'LT',                   # <
    'GT',                   # >
    'LEQ',                  # <=
    'GEQ',                  # >=

    # Conditionals
    'IF',                   # if
    'ELSEIF',               # elseif
    'ELSE',                 # else
    'WHILE',                # while
    'FOR',                  # for

    # Brackets and punctuation
    'LPAREN',               # (
    'RPAREN',               # )
    'LBRACE',               # [
    'RBRACE',               # ]
    'BLOCK_START',          # {
    'BLOCK_END',            # }
    'DOT',                  # .
    'DOUBLE_QUOTE',         # "
    'SEMICOLON',            # ;
    'COMMA',                # ,
    'COLON',                # :

    'COMMENT',              # #

    # Literals
    'NUMBER',               # 123, 45.67
    'STRING',               # "hello"
    'BOOLEAN',              # true, false
    'NULL',                 # null
    'IDENTIFIER',           # variable names
    'WHITESPACE',           # spaces, tabs, newlines
]

# Define literals for single-character tokens
literals = ['+', '-', '*', '/', '=', '(', ')', '{', '}', '.', ';', ',', ':', '#', '?', '!']
# Note: Single-character tokens are defined in literals and do not need separate token definitions.

# Regular expression rules for simple tokens
t_PLUS          = r'\+'
t_MINUS         = r'-'
t_TIMES         = r'\*'
t_DIVIDE        = r'/'
t_EQUALS        = r'='
t_EQ            = r'=='
t_NEQ           = r'!='
t_LT            = r'<'
t_GT            = r'>'
t_LEQ           = r'<='
t_GEQ           = r'>='
t_LPAREN       = r'\('
t_RPAREN       = r'\)'
t_LBRACE       = r'\['
t_RBRACE       = r'\]'
t_BLOCK_START  = r'\{'
t_BLOCK_END    = r'\}'
t_DOT          = r'\.'
t_DOUBLE_QUOTE = r'"'
t_SEMICOLON    = r';'
t_COMMA        = r','
t_COLON        = r':'
t_COMMENT      = r'\#.*'
t_WHITESPACE   = r'\s+'
t_BOOLEAN      = r'\b(true|false)\b'
t_NULL         = r'\bnull\b'
t_IF           = r'\bif\b'
t_ELSEIF       = r'\belseif\b'
t_ELSE         = r'\belse\b'
t_WHILE        = r'\bwhile\b'
t_FOR          = r'\bfor\b'
t_IDENTIFIER   = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_NUMBER       = r'\d+(\.\d+)?'
t_STRING       = r'"([^"\\]*(\\.[^"\\]*)*)"'
# Note: The STRING regex captures escaped quotes within the string.
# The WHITESPACE token can be ignored in the parser if not needed.
# To ignore whitespace tokens, you can add the following function:

# Ignore whitespace (spaces, tabs)
t_ignore = ' \t'

# Track newlines
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

    
# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()

def find_column(input_text, token):
    last_newline = input_text.rfind('\n', 0, token.lexpos)
    if last_newline < 0:
        last_newline = -1
    return token.lexpos - last_newline

# Open a file and read its contents
current_line = 0

with open('./Test_Files/test.pisc', 'r') as file:
    data = file.read()
    lexer.input(data)
    for tok in lexer:
        col = find_column(data, tok)

        # Check if we changed lines
        if tok.lineno != current_line:
            if current_line != 0:   # Avoid extra newline at start
                print()  
            current_line = tok.lineno

        print(f"(line {tok.lineno}, col {col}) {tok.type}: {tok.value}")