"""Make the parsers and the package importable from tests/ without installing."""
import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARSER_DIR = os.path.join(_ROOT, "parser")
SRC_DIR = os.path.join(_ROOT, "src")
for _path in (PARSER_DIR, SRC_DIR):
    if _path not in sys.path:
        sys.path.insert(0, _path)
