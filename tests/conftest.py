"""Shared pytest configuration — ensures src/utils is importable for all tests."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "utils"))
