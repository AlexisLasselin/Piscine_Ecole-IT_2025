# main.py 

from flask import Flask, request, jsonify
from lexer import lexer
from parser import parser
from ast_visualizer import generate_ast_graph
from interpreter import Interpreter
import os

def run_file(filename: str):
    # Lire le code source
    with open(filename, "r", encoding="utf-8") as f:
        code = f.read()

    # Parser en AST
    ast = parser.parse(code, lexer=lexer)

    # Afficher l'AST en texte
    print("=== AST ===")
    print(ast)

    # Désactiver view=True en Docker (pas de xdg-open)
    in_docker = os.path.exists("/.dockerenv")
    view = not in_docker

    # Générer une image de l'AST
    generate_ast_graph(ast, filename="ast_output", view=view)

    # Exécuter le code
    print("\n=== Execution ===")
    interpreter = Interpreter()
    interpreter.run(ast)


# --- Flask API ---
app = Flask(__name__)

@app.route("/")
def home():
    return "🚀 Langage interpréteur en marche !"

@app.route("/run", methods=["POST"])
def run_code():
    code = request.data.decode("utf-8")  # Récupère le code envoyé
    try:
        ast = parser.parse(code, lexer=lexer)
        print(ast)  # Affiche l’AST dans les logs du conteneur

        # Génère un graphe AST (fichier PNG dans le volume backend)
        generate_ast_graph(ast, filename="ast_output", view=False)

        interpreter = Interpreter()
        output = interpreter.run(ast)

        return jsonify({"status": "ok", "ast": str(ast), "output": str(output)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


if __name__ == "__main__":
    # Lancer un test au démarrage (optionnel)
    run_file("tests/samples/if.pisc")

    # Démarrer le serveur Flask (ne s'arrêtera pas)
    app.run(host="0.0.0.0", port=5000, debug=False)
