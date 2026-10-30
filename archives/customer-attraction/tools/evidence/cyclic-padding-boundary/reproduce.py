"""Replay both frozen programs without changing their bytes or frozen outputs."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent


def main():
    if not __debug__:
        raise RuntimeError("Assertions must be enabled")
    manifest = json.loads((HERE / "source-manifest.json").read_text())
    for item in manifest["files"]:
        relative = Path(item["local_path"]).relative_to(
            "archives/customer-attraction/tools/evidence/cyclic-padding-boundary")
        assert hashlib.sha256((HERE / relative).read_bytes()).hexdigest() == item["sha256"]
    replay = HERE / "replay"
    replay.mkdir(exist_ok=True)
    runs = []
    with tempfile.TemporaryDirectory(prefix="runtime-", dir=replay) as tmp:
        root = Path(tmp)
        shutil.copytree(HERE / "dependencies", root, dirs_exist_ok=True)
        old_here = root / "research/workspaces/customer-attraction/R-frozen/weak_matching/round2"
        old_here.mkdir(parents=True)
        for name in ("audit_cyclic_budget", "padding_kernel_boundary"):
            script = old_here / (name + ".py")
            shutil.copyfile(HERE / "original" / script.name, script)
            run = subprocess.run([sys.executable, str(script)], cwd=root,
                                 text=True, capture_output=True)
            (replay / (name + "-stdout.txt")).write_text(run.stdout)
            (replay / (name + "-stderr.txt")).write_text(run.stderr)
            assert run.returncode == 0, (name, run.stderr)
            generated = (old_here / (name + ".json")).read_bytes()
            original = (HERE / "original" / (name + ".json")).read_bytes()
            (replay / (name + ".json")).write_bytes(generated)
            assert generated == original, name
            runs.append({"program": name + ".py", "command": [sys.executable, str(script)],
                         "returncode": run.returncode, "stderr_empty": not run.stderr,
                         "output_bytes": len(generated), "byte_equal_to_frozen": True,
                         "sha256": hashlib.sha256(generated).hexdigest()})
    result = {"python": sys.version, "assertions_enabled": __debug__,
              "source_hashes_verified": len(manifest["files"]),
              "runtime_layout_only": "Temporary old-depth tree; program bytes unchanged",
              "runs": runs}
    (replay / "original-runs-manifest.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
