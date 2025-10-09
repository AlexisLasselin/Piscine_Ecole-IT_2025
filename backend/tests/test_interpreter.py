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

def run_code(source: str):
    """Parse et exécute le code, capture sortie et erreurs."""
    from io import StringIO
    import contextlib

    output = StringIO()
    errors = []

    try:
        ast = parser.parse(source, lexer=lexer)
        interpreter = Interpreter()
        with contextlib.redirect_stdout(output):
            interpreter.run(ast)
    except RuntimeError as e:
        errors.append(str(e))

    return output.getvalue().splitlines(), errors


@pytest.mark.parametrize("source_file", glob.glob("backend/tests/samples/*.pisc"))
def test_interpreter_against_golden(source_file, request):
    update_golden = getattr(request.config, "update_golden", False)

    run_file = source_file.replace(".pisc", ".run.json")
    err_file = source_file.replace(".pisc", ".run.errors.json")

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
            assert errors == expected_errors, f"Runtime error mismatch for {source_file}"
    else:
        if update_golden:
            with open(run_file, "w", encoding="utf-8") as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
            pytest.skip(f"[UPDATED] Run golden for {source_file}")
        else:
            with open(run_file, "r", encoding="utf-8") as f:
                expected_output = json.load(f)
            assert output == expected_output, f"Output mismatch for {source_file}"
