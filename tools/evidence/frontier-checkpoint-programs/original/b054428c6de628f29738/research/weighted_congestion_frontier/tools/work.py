#!/usr/bin/env python3
"""Compatibility entry; the sole standalone implementation is /work.py."""
from pathlib import Path
import runpy

_PROGRAM = Path(__file__).resolve().parents[3] / "work.py"
if not _PROGRAM.is_file():
    raise SystemExit("Use the complete repository-root work.py attachment to restore a clone.")
if __name__ == "__main__":
    runpy.run_path(str(_PROGRAM), run_name="__main__")
else:
    globals().update({k: v for k, v in runpy.run_path(str(_PROGRAM)).items()
                      if not k.startswith("__")})
