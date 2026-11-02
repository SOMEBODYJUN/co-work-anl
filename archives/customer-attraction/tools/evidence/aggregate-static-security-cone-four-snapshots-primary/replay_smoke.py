#!/usr/bin/env python3
"""Run the unmodified search CLI on one small, fresh discovery trial."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import numpy
import scipy

BASE = Path(__file__).resolve().parent
DEPENDENCY = BASE.parent / "security-cce-search-program-primary" / "original" / "search_cce.py"
assert hashlib.sha256(DEPENDENCY.read_bytes()).hexdigest() == "bf868944a4c4400b408db663626b3cb9223fb4acd9a5cbe99bc83590a888cc26"
assert hashlib.sha256((BASE / "original" / "search_aggregate_security.py").read_bytes()).hexdigest() == "d7cbed7712b79ff06c61f40b21831a5862ffb07bf35f29cba83df99bec96b013"
OUT = BASE / "rerun"
OUT.mkdir(exist_ok=True)
env = dict(os.environ, PYTHONPATH=str(DEPENDENCY.parent))
command = [sys.executable, str(BASE / "original" / "search_aggregate_security.py"),
           "--k", "2", "--m", "2", "--trials", "1", "--seed", "1", "--out", str(OUT / "smoke-best.json")]
result = subprocess.run(command, env=env, capture_output=True, text=True, timeout=30)
(OUT / "smoke.stdout.txt").write_text(result.stdout)
(OUT / "smoke.stderr.txt").write_text(result.stderr)
metadata = {"python": sys.version, "numpy": numpy.__version__, "scipy": scipy.__version__,
            "argv_relative": ["python", "original/search_aggregate_security.py", "--k", "2", "--m", "2", "--trials", "1", "--seed", "1", "--out", "rerun/smoke-best.json"],
            "PYTHONPATH_dependency": str(DEPENDENCY.relative_to(BASE.parent)),
            "dependency_sha256": hashlib.sha256(DEPENDENCY.read_bytes()).hexdigest(),
            "returncode": result.returncode,
            "scope": "one fresh k2 m2 trial; does not recreate any of the four frozen snapshots or its unknown search run"}
(OUT / "smoke-execution.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")
assert result.returncode == 0, result.stderr
assert (OUT / "smoke-best.json").is_file()
print(result.stdout, end="")
print(json.dumps({key: metadata[key] for key in ("numpy", "scipy", "returncode", "scope")}, ensure_ascii=False))
