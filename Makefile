# Python interpreter
PYTHON=python

# Default target (if you just run "make")
all: test

# Run all tests (normal mode, like CI/CD)
test:
	$(PYTHON) -m pytest -v

# Update golden files (tokens and errors)
golden:
	$(PYTHON) -m pytest -v --update-golden

# Clean cache files
clean:
	rm -rf __pycache__/ .pytest_cache/ tests/__pycache__/

# Optional: re-run golden update after cleaning
regolden: clean golden
