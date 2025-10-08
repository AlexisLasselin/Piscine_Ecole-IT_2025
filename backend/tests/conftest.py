# backend/tests/conftest.py

def pytest_addoption(parser):
    parser.addoption(
        "--update-golden",
        action="store_true",
        default=False,
        help="Regenerate golden .json and .errors.json files from current lexer/parser output",
    )

def pytest_configure(config):
    # Make option accessible via config in tests
    config.update_golden = config.getoption("--update-golden")
