"""Prepare the standard-library-only research tools without changing Git identity."""
from pathlib import Path
import sys
import venv

root = Path(__file__).resolve().parents[1]
if sys.version_info < (3, 11):
    raise SystemExit('Python 3.11 or newer is required')
if not (root / '.venv/bin/python').exists():
    venv.EnvBuilder(with_pip=True).create(root / '.venv')
print('Ready: .venv/bin/python work.py research --help')
print('Environment prepared. Computations and engineering checks run only when explicitly requested.')
