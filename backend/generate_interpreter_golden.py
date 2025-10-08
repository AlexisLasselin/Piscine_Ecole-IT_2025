import glob
import json
import pathlib
import sys
from io import StringIO

from lexer import lexer, lexer_errors
from parser import parser
from interpreter import Interpreter

def run_code(code: str):
    """Parse + interprète le code et capture la sortie"""
    lexer_errors.clear()
    lexer.lineno = 1

    ast = parser.parse(code, lexer=lexer)

    if lexer_errors:
        return None, lexer_errors

    old_stdout = sys.stdout
    sys.stdout = StringIO()
    errors = []
    try:
        interpreter = Interpreter()
        interpreter.run(ast)
        output = sys.stdout.getvalue().splitlines()
    except Exception as e:
        errors = [str(e)]
        output = None
    finally:
        sys.stdout = old_stdout

    return output, errors


def write_json(path: pathlib.Path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def process_file(source_file: str):
    p = pathlib.Path(source_file)
    code = p.read_text(encoding="utf-8")

    output, errors = run_code(code)

    if errors:
        err_path = p.with_suffix(".out.errors.json")
        write_json(err_path, errors)
        print(f"[ERROR] {source_file}: wrote {err_path.name}")
        for e in errors:
            print("   ", e)
        return False

    out_path = p.with_suffix(".out.json")
    write_json(out_path, output)
    print(f"[OK] Generated {out_path}")
    return True


def main():
    files = glob.glob("backend/tests/samples/*.pisc")
    if not files:
        print("No .pisc files found under backend/tests/samples/")
        return

    for f in sorted(files):
        process_file(f)


if __name__ == "__main__":
    main()
