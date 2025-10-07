# generate_ast_golden.py
import glob
import json
import pathlib
import sys

from lexer import lexer, lexer_errors
from parser import parser, ast_to_dict 

def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text

def write_json(path: pathlib.Path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8", newline="\n")

def show_source_context(source_text: str, lineno: int, context=3):
    lines = source_text.splitlines()
    start = max(0, lineno - context - 1)
    end = min(len(lines), lineno + context)
    out = []
    for i in range(start, end):
        marker = ">>" if (i + 1) == lineno else "  "
        out.append(f"{marker} {i+1:4d}: {lines[i]}")
    return "\n".join(out)

def process_file(source_file: str):
    p = pathlib.Path(source_file)
    code = p.read_text(encoding="utf-8", errors="replace")
    code = normalize_text(code)

    # Reset lexer state and errors BEFORE parsing
    lexer_errors.clear()
    lexer.lineno = 1

    # Try parse
    try:
        ast = parser.parse(code, lexer=lexer)
    except Exception as e:
        # collect lexer errors too (if any)
        errors = list(lexer_errors)
        # also include the parser exception message
        parser_msg = str(e)
        errors.append(f"Parser error: {parser_msg}")

        # Try to extract lineno from exception message (best-effort)
        # We'll attempt to find digits like "lineno 17" in the message
        lineno = None
        import re
        m = re.search(r"lineno\s*([0-9]+)", parser_msg)
        if m:
            lineno = int(m.group(1))

        # Write an errors file
        err_path = p.with_suffix(".ast.errors.json")
        write_json(err_path, errors)
        print(f"[ERROR] {source_file}: {parser_msg}")
        if lineno:
            print("Source context around reported lineno:")
            print(show_source_context(code, lineno))
        else:
            print("Lexer errors (if any):")
            for err in lexer_errors:
                print("  ", err)
        return False

    # If lexer reported errors (t_error), refuse to write AST
    if lexer_errors:
        err_path = p.with_suffix(".ast.errors.json")
        write_json(err_path, list(lexer_errors))
        print(f"[ERROR] {source_file}: lexer errors -> wrote {err_path.name}")
        for err in lexer_errors:
            print("   ", err)
        return False

    # Successful: convert AST -> plain dict and write .ast.json
    d = ast_to_dict(ast)
    out_path = p.with_suffix(".ast.json")
    write_json(out_path, d)
    print(f"[OK] Generated {out_path}")
    return True

def main():
    files = glob.glob("tests/samples/*.pisc")
    if not files:
        print("No .pisc files found under tests/samples/")
        return

    for f in sorted(files):
        process_file(f)

if __name__ == "__main__":
    main()
