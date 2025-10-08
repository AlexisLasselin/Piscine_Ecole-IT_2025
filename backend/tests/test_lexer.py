import json
import glob
import pytest
import sys, os

# Ajouter le dossier backend/ au PYTHONPATH pour importer lexer
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from lexer import lexer, lexer_errors

# Base directory = dossier où est ce fichier
BASE_DIR = os.path.dirname(__file__)
SAMPLES_DIR = os.path.join(BASE_DIR, "samples")

def tokenize(code):
    lexer_errors.clear()
    lexer.lineno = 1
    lexer.input(code)
    return [(tok.type, tok.value) for tok in lexer]

@pytest.mark.parametrize("source_file", glob.glob(os.path.join(SAMPLES_DIR, "*.pisc")))
def test_lexer_against_golden(source_file, request):
    json_file = source_file.replace(".pisc", ".json")
    error_file = source_file.replace(".pisc", ".errors.json")

    with open(source_file, "r", encoding="utf-8") as f:
        code = f.read()

    tokens = tokenize(code)

    if lexer_errors:
        if request.config.update_golden:
            with open(error_file, "w") as f:
                json.dump(lexer_errors, f, indent=2)
            pytest.skip(f"Golden errors updated for {source_file}")
        else:
            with open(error_file, "r") as f:
                expected_errors = json.load(f)
            assert lexer_errors == expected_errors, f"Mismatch in errors for {source_file}"
    else:
        if request.config.update_golden:
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(tokens, f, indent=2, ensure_ascii=False)
            pytest.skip(f"Golden tokens updated for {source_file}")
        else:
            with open(json_file, "r", encoding="utf-8") as f:
                expected = json.load(f)
            assert lexer_errors == []
            assert tokens == [tuple(e) for e in expected], f"Token mismatch in {source_file}"
