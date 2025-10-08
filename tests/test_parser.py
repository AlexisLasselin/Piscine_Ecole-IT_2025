# tests/test_parser.py
import glob
import json
import pytest
from lexer import lexer, lexer_errors
from parser import parser, ast_to_dict

def parse_code(source):
    """Helper to parse code into an AST object."""
    lexer_errors.clear()     # reset erreurs
    lexer.lineno = 1         # reset numéros de lignes
    return parser.parse(source, lexer=lexer)

@pytest.mark.parametrize("source_file", glob.glob("tests/samples/*.pisc"))
def test_ast_against_golden(source_file, request):
    update_golden = request.config.update_golden

    json_file = source_file.replace(".pisc", ".ast.json")
    error_file = source_file.replace(".pisc", ".ast.errors.json")

    with open(source_file, "r", encoding="utf-8") as f:
        code = f.read()

    # Reset lexer state before parsing
    lexer_errors.clear()
    lexer.lineno = 1

    try:
        # Parse code
        ast = parse_code(code)

        if lexer_errors:
            if update_golden:
                with open(error_file, "w", encoding="utf-8") as f:
                    json.dump(lexer_errors, f, indent=2, ensure_ascii=False)
                pytest.skip(f"[UPDATED] Errors golden for {source_file}")
            else:
                with open(error_file, "r", encoding="utf-8") as f:
                    expected_errors = json.load(f)
                assert lexer_errors == expected_errors, f"Lexer errors mismatch for {source_file}"
            return

        # Convert AST to dict for stable comparison
        actual = ast_to_dict(ast)

        if update_golden:
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(actual, f, indent=2, ensure_ascii=False)
            pytest.skip(f"[UPDATED] AST golden for {source_file}")
        else:
            with open(json_file, "r", encoding="utf-8") as f:
                expected_ast = json.load(f)
            assert actual == expected_ast, f"AST mismatch for {source_file}"

    except SyntaxError as e:
        err_msg = str(e)
        if update_golden:
            with open(error_file, "w", encoding="utf-8") as f:
                json.dump([err_msg], f, indent=2, ensure_ascii=False)
            pytest.skip(f"[UPDATED] Parser error golden for {source_file}")
        else:
            with open(error_file, "r", encoding="utf-8") as f:
                expected_errors = json.load(f)
            assert err_msg in expected_errors, f"Parser error mismatch for {source_file}"
