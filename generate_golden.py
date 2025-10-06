import os
import glob
import json
from lexer import lexer, lexer_errors

def tokenize(code):
    lexer_errors.clear()
    lexer.input(code)
    return [(tok.type, tok.value) for tok in lexer]

def main():
    sample_files = glob.glob("tests/samples/*.pisc")
    if not sample_files:
        print("No .pisc files found in tests/samples/")
        return

    for source_file in sample_files:
        json_file = source_file.replace(".pisc", ".json")
        error_file = source_file.replace(".pisc", ".errors.json")

        with open(source_file, "r") as f:
            code = f.read()

        tokens = tokenize(code)

        if lexer_errors:
            # Program contains errors → write .errors.json
            print(f"[ERRORS] in {source_file}:")
            for e in lexer_errors:
                print("   ", e)
            with open(error_file, "w") as f:
                json.dump(lexer_errors, f, indent=2)
        else:
            # Valid program → write .json with tokens
            print(f"[OK] Generated golden file for {source_file}")
            with open(json_file, "w") as f:
                json.dump(tokens, f, indent=2)

if __name__ == "__main__":
    main()
