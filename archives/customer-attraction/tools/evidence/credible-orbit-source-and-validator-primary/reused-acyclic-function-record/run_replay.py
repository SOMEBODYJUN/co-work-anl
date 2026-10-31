"""Rebuild historical paths in a temporary tree; preserve frozen source bytes."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent


def main():
    resources = json.loads((HERE / "manifest.json").read_text())["resources"]
    by_id = {r["id"]: r for r in resources}
    output = HERE / "replay"
    output.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="runtime-", dir=output) as directory:
        root = Path(directory)
        for record in resources:
            payload = (HERE / record["payload"]).read_bytes()
            assert hashlib.sha256(payload).hexdigest() == record["sha256"]
            target = root / record["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(payload)
        marker = root / "customer_attraction/model.py"
        marker.parent.mkdir(exist_ok=True)
        marker.write_text("# Ancestor discovery marker only; never imported.\n")
        pairs = [
            ("23a337560864ccbec9f3", "e83973d1b06960a495a1", "author.json"),
            ("2106a990188529e14de3", "d87c0677cdc1affff33a", "independent.json"),
        ]
        for script_id, report_id, name in pairs:
            script = root / by_id[script_id]["path"]
            process = subprocess.run(
                [sys.executable, str(script)], capture_output=True, text=True
            )
            assert process.returncode == 0, process.stderr
            actual = root / by_id[report_id]["path"]
            expected = HERE / by_id[report_id]["payload"]
            assert actual.read_bytes() == expected.read_bytes(), name
            shutil.copyfile(actual, output / name)
    print(json.dumps({"author_byte_identical": True, "independent_byte_identical": True}))


if __name__ == "__main__":
    main()
