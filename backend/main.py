# main.py

from lexer import lexer
from parser import parser
from ast_visualizer import generate_ast_graph
from interpreter import Interpreter

def run_file(filename: str):
    # Lire le code source
    with open(filename, "r", encoding="utf-8") as f:
        code = f.read()

    # Parser en AST
    ast = parser.parse(code, lexer=lexer)

    # Afficher l'AST en texte
    print("=== AST ===")
    print(ast)

    # Générer une image de l'AST
    generate_ast_graph(ast, filename="ast_output", view=True)

    # Exécuter le code
    print("\n=== Execution ===")
    interpreter = Interpreter()
    interpreter.run(ast)


if __name__ == "__main__":
    run_file("backend/tests/samples/if.pisc")
