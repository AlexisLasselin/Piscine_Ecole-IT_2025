# ast_visualizer.py
from graphviz import Digraph
from my_ast import Number, Variable, BinaryOp, Assignment, Print

def add_nodes_edges(dot, node, parent=None):
    if node is None:
        return

    # 🔹 Label et couleur selon le type de nœud
    if isinstance(node, Number):
        label = f"Literal = {node.value}"
        color = "#ffb3b3"  # rose clair
        shape = "ellipse"
    elif isinstance(node, Variable):
        label = f"Identifier ({node.name})"
        color = "#a3e4d7"  # vert menthe
        shape = "ellipse"
    elif isinstance(node, BinaryOp):
        label = f"BinaryExpression ({op_symbol(node.op)})"
        color = "#a9dfbf"  # vert clair
        shape = "box"
    elif isinstance(node, Assignment):
        label = f"Assignment ({node.name})"
        color = "#f9e79f"  # jaune pâle
        shape = "parallelogram"
    elif isinstance(node, Print):
        label = "FunctionCall (print)"
        color = "#c39bd3"  # violet clair
        shape = "diamond"
    else:
        label = type(node).__name__
        color = "white"
        shape = "ellipse"

    node_id = str(id(node))
    dot.node(node_id, label, style="filled", fillcolor=color, shape=shape, color="black")

    # 🔹 Relier au parent s’il existe
    if parent:
        dot.edge(parent, node_id, color="gray50")

    # 🔹 Explorer les sous-nœuds
    for attr in ['left', 'right', 'expr']:
        child = getattr(node, attr, None)
        if child:
            add_nodes_edges(dot, child, node_id)

def op_symbol(op):
    """Convertit le type de token en symbole lisible"""
    return {
        "PLUS": "+",
        "MINUS": "-",
        "MULT": "*",
        "DIV": "/"
    }.get(op, op)

def generate_ast_graph(ast):
    dot = Digraph(comment="AST complet", format="png")
    dot.attr(bgcolor="white")
    dot.attr(rankdir="TB")  # top -> bottom
    dot.attr('node', fontname="Helvetica")

    # 🔹 Nœud racine “Program”
    program_id = "ProgramRoot"
    dot.node(program_id, "Program", shape="oval", style="filled", fillcolor="white")

    # 🔹 Chaque instruction devient un enfant direct du nœud “Program”
    for node in ast:
        add_nodes_edges(dot, node, parent=program_id)

    # 🔹 Génération du fichier
    output_path = dot.render("ast_graph_full", view=True)
    print(f"✅ Graphe généré : {output_path}")
