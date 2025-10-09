import glob
import json
import pathlib
import sys

from lexer import lexer, lexer_errors
from parser import parser
from interpreter import Interpreter


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text


def write_json(path: pathlib.Path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8", newline="\n")


def process_file(source_file: str):
    p = pathlib.Path(source_file)
    code = p.read_text(encoding="utf-8", errors="replace")
    code = normalize_text(code)

    # Reset lexer state and errors BEFORE parsing
    lexer_errors.clear()
    lexer.lineno = 1

    try:
        ast = parser.parse(code, lexer=lexer)
    except Exception as e:
        # Parser error
        err_path = p.with_suffix(".run.errors.json")
        write_json(err_path, [f"Parser error: {str(e)}"])
        print(f"[ERROR] {source_file}: {e}")
        return False

    if lexer_errors:
        # Lexer errors
        err_path = p.with_suffix(".run.errors.json")
        write_json(err_path, list(lexer_errors))
        print(f"[ERROR] {source_file}: lexer errors")
        return False

    # Interpreter run
    interp = Interpreter()
    out = interp.run(ast)

    out_path = p.with_suffix(".run.json")
    write_json(out_path, out)
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
