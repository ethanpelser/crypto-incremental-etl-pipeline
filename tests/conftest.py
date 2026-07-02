"""Shared pytest configuration for the crypto ETL project."""

import sys
from pathlib import Path

# Allow tests to import modules directly from src/, e.g. `import transform`.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
