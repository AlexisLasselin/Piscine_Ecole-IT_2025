# tests/conftest.py
def pytest_addoption(parser):
    parser.addoption(
        "--update-golden",
        action="store_true",
        default=False,
        help="Regenerate golden .json and .errors.json files from current lexer output",
    )

def pytest_configure(config):
    # Make it accessible globally
    config.update_golden = config.getoption("--update-golden")
