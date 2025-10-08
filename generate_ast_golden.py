# generate_ast_golden.py
import os
import glob
import json
from lexer import lexer, lexer_errors
from parser import parser, ast_to_dict


def parse_code(code):
    """Parse code into AST and return dict representation."""
    lexer_errors.clear()
    lexer.lineno = 1
    return parser.parse(code, lexer=lexer)


def main():
    sample_files = glob.glob("tests/samples/*.pisc")
    if not sample_files:
        print("No .pisc files found in tests/samples/")
        return

    for source_file in sample_files:
        json_file = source_file.replace(".pisc", ".ast.json")
        error_file = source_file.replace(".pisc", ".ast.errors.json")

        with open(source_file, "r", encoding="utf-8") as f:
            code = f.read()

        try:
            ast = parse_code(code)

            if lexer_errors:
                # → errors from lexer
                print(f"[ERRORS] in {source_file}:")
                for e in lexer_errors:
                    print("   ", e)
                with open(error_file, "w", encoding="utf-8") as f:
                    json.dump(lexer_errors, f, indent=2, ensure_ascii=False)
            else:
                # → valid AST
                print(f"[OK] Generated {json_file}")
                with open(json_file, "w", encoding="utf-8") as f:
                    json.dump(ast_to_dict(ast), f, indent=2, ensure_ascii=False)

        except Exception as e:
            # → parser error
            err_msg = str(e)
            print(f"[ERROR] in {source_file}: {err_msg}")
            with open(error_file, "w", encoding="utf-8") as f:
                json.dump([err_msg], f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
