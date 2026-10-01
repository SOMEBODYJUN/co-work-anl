#!/usr/bin/env python3
"""Compatibility entry point; canonical check is tests.audits.shared_menu."""
from pathlib import Path
import sys
_REPO_ROOT = Path(__file__).resolve().parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
if __name__ == "__main__":
    import runpy
    runpy.run_module("tests.audits.shared_menu", run_name="__main__")
else:
    from tests.audits.shared_menu import *
