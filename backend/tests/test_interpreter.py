import glob
import json
import pytest
from io import StringIO
import sys, os

# Ensure the backend directory is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from lexer import lexer, lexer_errors
from parser import parser
from parser import ast_to_dict
from interpreter import Interpreter

def run_code(source):
    """Parse + interprète le code et capture la sortie"""
    lexer_errors.clear()
    lexer.lineno = 1

    ast = parser.parse(source, lexer=lexer)

    if lexer_errors:
        return None, lexer_errors

    # Capture stdout
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


@pytest.mark.parametrize("source_file", glob.glob("backend/tests/samples/*.pisc"))
def test_interpreter_against_golden(source_file, request):
    update_golden = request.config.update_golden

    out_file = source_file.replace(".pisc", ".out.json")
    err_file = source_file.replace(".pisc", ".out.errors.json")

    with open(source_file, "r", encoding="utf-8") as f:
        code = f.read()

    output, errors = run_code(code)

    if errors:
        if update_golden:
            with open(err_file, "w", encoding="utf-8") as f:
                json.dump(errors, f, indent=2, ensure_ascii=False)
            pytest.skip(f"[UPDATED] Errors golden for {source_file}")
        else:
            with open(err_file, "r", encoding="utf-8") as f:
                expected_errors = json.load(f)
            assert errors == expected_errors, f"Interpreter errors mismatch for {source_file}"
        return

    if update_golden:
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        pytest.skip(f"[UPDATED] Output golden for {source_file}")
    else:
        with open(out_file, "r", encoding="utf-8") as f:
            expected_output = json.load(f)
        assert output == expected_output, f"Interpreter output mismatch for {source_file}"
