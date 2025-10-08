import glob
import json
import pytest
import sys
import os

# Ensure the backend directory is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from lexer import lexer, lexer_errors
from parser import parser
from interpreter import Interpreter

def run_interpreter(code: str):
    """Helper to execute code and capture output."""
    lexer_errors.clear()
    lexer.lineno = 1
    ast = parser.parse(code, lexer=lexer)
    if lexer_errors:
        raise SyntaxError(f"Lexer errors: {lexer_errors}")

    interpreter = Interpreter()
    return interpreter.run(ast)

@pytest.mark.parametrize("source_file", glob.glob("backend/tests/samples/*.pisc"))
def test_interpreter_against_golden(source_file, request):
    update_golden = request.config.update_golden

    golden_file = source_file.replace(".pisc", ".run.json")

    with open(source_file, "r", encoding="utf-8") as f:
        code = f.read()

    try:
        output = run_interpreter(code)
    except SyntaxError as e:
        output = {"errors": [str(e)]}

    if update_golden:
        with open(golden_file, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        pytest.skip(f"[UPDATED] Interpreter golden for {source_file}")
    else:
        try:
            with open(golden_file, "r", encoding="utf-8") as f:
                expected_output = json.load(f)
        except FileNotFoundError:
            pytest.skip(f"No golden run file for {source_file}")

        assert output == expected_output, f"Interpreter output mismatch for {source_file}"
