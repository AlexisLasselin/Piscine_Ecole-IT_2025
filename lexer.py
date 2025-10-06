from ply import lex

# --- Reserved keywords ---
reserved = {
    'if': 'IF',
    'elseif': 'ELSEIF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'true': 'BOOLEAN',
    'false': 'BOOLEAN',
    'null': 'NULL',
    'print': 'PRINT',
}

# --- Deduplicate reserved token names while preserving order ---
reserved_tokens = list(dict.fromkeys(reserved.values()))

# --- Base token list (without reserved tokens) ---
base_tokens = [
    # Operators
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS',

    # Comparisons
    'EQ', 'NEQ', 'LT', 'GT', 'LEQ', 'GEQ',

    # Brackets and punctuation
    'LPAREN', 'RPAREN',
    'LBRACE', 'RBRACE',
    'BLOCK_START', 'BLOCK_END',
    'DOT', 'DOUBLE_QUOTE',
    'SEMICOLON', 'COMMA', 'COLON',

    'COMMENT',

    # Literals
    'NUMBER', 'STRING',
    'IDENTIFIER',
]

# --- Final tokens list: base + deduplicated reserved tokens ---
tokens = base_tokens + reserved_tokens

# Safety check: no duplicates
assert len(tokens) == len(set(tokens)), f"Duplicate tokens detected: {set([t for t in tokens if tokens.count(t) > 1])}"

# --- Literals (single-character shortcuts, optional) ---
literals = ['+', '-', '*', '/', '=', '(', ')', '{', '}', '.', ';', ',', ':', '#', '?', '!']

# --- Regex rules for simple tokens ---
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
t_LPAREN        = r'\('
t_RPAREN        = r'\)'
t_LBRACE        = r'\['
t_RBRACE        = r'\]'
t_BLOCK_START   = r'\{'
t_BLOCK_END     = r'\}'
t_DOT           = r'\.'
t_DOUBLE_QUOTE  = r'"'
t_SEMICOLON     = r';'
t_COMMA         = r','
t_COLON         = r':'
t_COMMENT       = r'\#.*'
t_NUMBER        = r'\d+(\.\d+)?'
t_STRING        = r'"([^"\\]*(\\.[^"\\]*)*)"'   # string with escaped quotes

# --- Identifiers and reserved words ---
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')  # Check reserved words
    return t

# --- Ignore spaces and tabs ---
t_ignore = ' \t'

# --- Track newlines ---
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# --- Error collection ---
lexer_errors = []

def t_error(t):
    last_newline = t.lexer.lexdata.rfind('\n', 0, t.lexpos)
    if last_newline < 0:
        last_newline = -1
    col = t.lexpos - last_newline
    msg = f"Illegal character '{t.value[0]}' at line {t.lineno}, col {col}"
    lexer_errors.append(msg)
    t.lexer.skip(1)

# --- Build the lexer ---
lexer = lex.lex()

# --- Helper to compute column ---
def find_column(input_text, token):
    last_newline = input_text.rfind('\n', 0, token.lexpos)
    if last_newline < 0:
        last_newline = -1
    return token.lexpos - last_newline

# --- Manual run for debug ---
if __name__ == "__main__":
    current_line = 0
    with open('./tests/samples/while.pisc', 'r') as file:
        data = file.read()
        lexer.input(data)
        for tok in lexer:
            col = find_column(data, tok)
            if tok.lineno != current_line:
                if current_line != 0:
                    print()
                current_line = tok.lineno
            print(f"(line {tok.lineno}, col {col}) {tok.type}: {tok.value}")

    if lexer_errors:
        print("\nErrors:")
        for e in lexer_errors:
            print("  ", e)
