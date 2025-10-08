# generate_ast_golden.py
import glob
import json
import pathlib
from lexer import lexer, lexer_errors
from parser import parser, ast_to_dict

def reset_lexer():
    lexer_errors.clear()
    lexer.lineno = 1

def write_json(path: pathlib.Path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8", newline="\n")

def process_file(source_file: str):
    p = pathlib.Path(source_file)
    code = p.read_text(encoding="utf-8", errors="replace")

    # reset lexer state
    reset_lexer()

    try:
        ast = parser.parse(code, lexer=lexer)
    except Exception as e:
        errors = list(lexer_errors)
        errors.append(f"Parser error: {str(e)}")
        err_path = p.with_suffix(".ast.errors.json")
        write_json(err_path, errors)
        print(f"[ERROR] {source_file}: {e}")
        return False

    if lexer_errors:
        err_path = p.with_suffix(".ast.errors.json")
        write_json(err_path, list(lexer_errors))
        print(f"[ERROR] {source_file}: lexer errors -> wrote {err_path.name}")
        for err in lexer_errors:
            print("   ", err)
        return False

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
