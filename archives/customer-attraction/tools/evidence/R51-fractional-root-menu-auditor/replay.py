"""Hash-pinned, unchanged CLI replay in a disposable directory.

The original script writes beside __file__, so it must not run beside the
frozen comparison report.  This wrapper preserves both originals unchanged.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent


def main():
    manifest = json.loads((HERE / "source-manifest.json").read_text())
    for row in manifest:
        data = (HERE / row["preserved_path"]).read_bytes()
        if len(data) != row["size"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
            raise ValueError(f"Frozen source differs: {row['id']}")
    original = HERE / "original/audit_fractional_root_menu.py"
    frozen = (HERE / "original/fractional_root_menu_audit.json").read_bytes()
    env = dict(os.environ)
    env.pop("PYTHONOPTIMIZE", None)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    with tempfile.TemporaryDirectory(prefix="r51-fractional-menu-") as temp:
        script = Path(temp) / original.name
        shutil.copyfile(original, script)
        result = subprocess.run([sys.executable, str(script)], cwd=temp, env=env,
                                capture_output=True, timeout=30, check=False)
        generated = (Path(temp) / "fractional_root_menu_audit.json").read_bytes() if result.returncode == 0 else b""
    out = HERE / "replay"
    out.mkdir(exist_ok=True)
    (out / "stdout.txt").write_bytes(result.stdout)
    (out / "stderr.txt").write_bytes(result.stderr)
    (out / "fractional_root_menu_audit.json").write_bytes(generated)
    report = {"status": "PASS" if result.returncode == 0 and generated == frozen and result.stdout == frozen else "FAIL",
              "python": sys.version, "source_unchanged": True,
              "command": [sys.executable, "<temporary-directory>/audit_fractional_root_menu.py"],
              "assertions": "enabled: wrapper removes PYTHONOPTIMIZE and passes no -O flag",
              "returncode": result.returncode, "stderr_empty": result.stderr == b"",
              "generated_bytes_equal_frozen": generated == frozen,
              "stdout_bytes_equal_frozen": result.stdout == frozen,
              "generated_sha256": hashlib.sha256(generated).hexdigest(),
              "frozen_sha256": hashlib.sha256(frozen).hexdigest(),
              "generated_size": len(generated),
              "scope": "Unchanged finite-audit replay; continuous minimization rests on the separate analytic proof; the original scope string is preserved as historical text."}
    (out / "replay-summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    if report["status"] != "PASS":
        raise RuntimeError(json.dumps(report))
    print(json.dumps({k: report[k] for k in ("status", "returncode", "generated_size", "generated_bytes_equal_frozen", "stdout_bytes_equal_frozen")}))


if __name__ == "__main__":
    main()
