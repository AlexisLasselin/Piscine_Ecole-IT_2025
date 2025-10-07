# ast_visualizer.py
from graphviz import Digraph

def generate_ast_graph(ast, filename="ast", view=True):
    """
    Generate a Graphviz visualization of the AST.
    :param ast: root AST node
    :param filename: output filename (without extension)
    :param view: open the file automatically if True
    """
    dot = Digraph(comment="Abstract Syntax Tree", format="png")
    _add_node(dot, ast)
    dot.render(filename, view=view)

def _add_node(dot, node, parent_id=None, counter=[0]):
    """
    Recursive helper to add nodes and edges to the Graphviz graph.
    """
    node_id = str(counter[0])
    counter[0] += 1

    if isinstance(node, list):
        label = "Block"
        dot.node(node_id, label)
        if parent_id is not None:
            dot.edge(parent_id, node_id)
        for child in node:
            if child is not None:
                _add_node(dot, child, node_id, counter)
        return

    if node is None:
        return

    # Label according to node type
    label = node.__class__.__name__
    if hasattr(node, "name"):
        label += f"\\n{node.name}"
    if hasattr(node, "op"):
        label += f"\\n{node.op}"
    if hasattr(node, "value") and node.value is not None:
        label += f"\\n{node.value}"

    dot.node(node_id, label)

    if parent_id is not None:
        dot.edge(parent_id, node_id)

    # Recurse on children
    if hasattr(node, "__dict__"):
        for attr, child in vars(node).items():
            if isinstance(child, (list, tuple)):
                for c in child:
                    if c is not None:
                        _add_node(dot, c, node_id, counter)
            elif child is not None and not isinstance(child, (str, int, float, bool)):
                 _add_node(dot, child, node_id, counter)

