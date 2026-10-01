#!/usr/bin/env python3
"""Compatibility entry point; canonical implementation is facility_spe.heterogeneous_two."""
from pathlib import Path
import sys
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
if __name__ == "__main__":
    import runpy
    runpy.run_module("facility_spe.heterogeneous_two", run_name="__main__")
else:
    from facility_spe.heterogeneous_two import *
