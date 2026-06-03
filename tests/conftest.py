"""Make the stdlib-only parsers importable from tests/ without packaging."""
import os
import sys

PARSER_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "parser"
)
if PARSER_DIR not in sys.path:
    sys.path.insert(0, PARSER_DIR)
