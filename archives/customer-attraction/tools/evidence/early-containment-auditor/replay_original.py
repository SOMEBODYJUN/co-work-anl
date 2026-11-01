"""Execute the preserved assertion-based audit unchanged in a private cwd."""
from pathlib import Path
import hashlib
import json
import platform
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "original/audit_containment.py"
OUT = HERE / "rerun"
EXPECTED = "f195139aab2c9b95b9d21fccd8ee74a2d95debf8265385fd281366dbecb7c702"
REPORT_SHA = "9f23473ad97b4d4127c19f9643c3621ca1add12df42b61c662b5c9c0ea985a36"

def main():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED
    OUT.mkdir(parents=True, exist_ok=True)
    start = time.perf_counter()
    # Isolated mode ignores PYTHONOPTIMIZE; no -O is supplied, so assertions execute.
    result = subprocess.run([sys.executable, "-I", str(SOURCE)], cwd=OUT, capture_output=True, check=False)
    (OUT / "original_stdout.json").write_bytes(result.stdout)
    (OUT / "original_stderr.txt").write_bytes(result.stderr)
    assert result.returncode == 0, result.stderr.decode()
    parsed = json.loads(result.stdout)
    assert parsed["status"] == "passed"
    out_sha = hashlib.sha256(result.stdout).hexdigest()
    assert out_sha == REPORT_SHA
    source_after = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    assert source_after == EXPECTED
    metadata = {"status": "local-prepared", "python": platform.python_version(),
                "source_sha256": EXPECTED, "source_unchanged": source_after == EXPECTED,
                "command": ["python3", "-I", "original/audit_containment.py"],
                "cwd": "archives/customer-attraction/tools/evidence/early-containment-auditor/rerun",
                "returncode": result.returncode, "assertions_enabled": True,
                "stdout_sha256": out_sha, "stdout_bytes": len(result.stdout),
                "frozen_report_sha256": REPORT_SHA, "byte_equal_to_frozen_report": True,
                "elapsed_seconds": time.perf_counter() - start,
                "scope": "One unchanged original entry point: 1960 reduced types, 3360 feasible-overlap types and six-player multiplicity constants; no game/SPE enumeration, LP or other audit scripts executed"}
    (OUT / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")
    print(result.stdout.decode(), end="")
    print(json.dumps(metadata, ensure_ascii=False))

if __name__ == "__main__":
    main()
