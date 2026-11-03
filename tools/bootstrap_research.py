"""Prepare the standard-library-only research tools without changing Git identity."""
from pathlib import Path
import subprocess
import sys
import venv

root = Path(__file__).resolve().parents[1]
if sys.version_info < (3, 11):
    raise SystemExit('Python 3.11 or newer is required')
if not (root / '.venv/bin/python').exists():
    venv.EnvBuilder(with_pip=True).create(root / '.venv')
result = subprocess.run([str(root / '.venv/bin/python'), '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_research_runtime.py', '-q'], cwd=root)
if result.returncode:
    raise SystemExit(result.returncode)
print('Ready: .venv/bin/python work.py research --help')
print('No credentials installed, no research agents launched, no remote writes performed.')
