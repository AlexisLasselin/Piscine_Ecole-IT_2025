from lexer import lexer
from parser import parser
from ast_visualizer import generate_ast_graph

# Import sample code
with open("tests/samples/if.pisc", "r", encoding="utf-8") as f:
    code = f.read()
# Lexing and Parsing

ast = parser.parse(code, lexer=lexer)
print(ast)  # text representation
generate_ast_graph(ast, filename="ast_output", view=True)
