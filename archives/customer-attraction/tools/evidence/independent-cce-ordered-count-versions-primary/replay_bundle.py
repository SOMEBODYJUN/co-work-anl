"""Replay the three original finite entry points, preserving sources unchanged."""
from pathlib import Path
import datetime
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parent

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    manifest = json.loads((ROOT / "source-manifest.json").read_text())
    for source in manifest["sources"]:
        data = (ROOT / source["preserved_path"]).read_bytes()
        assert len(data) == source["size"]
        assert sha(data) == source["sha256"]
    runs = []
    for label, program, args, report_name, frozen_name in [
        ("forty-two-ordered", "independent_cce_audit.py", [], "independent_cce_audit.json", "independent_cce_audit.json"),
        ("eight-ordered", "independent_cce_audit.py", ["--small"], "independent_cce_eight_client_audit.json", "independent_cce_eight_client_audit.json"),
        ("eight-count", "count_policy_cce_audit.py", [], "count_policy_cce_audit.json", "count_policy_cce_audit.json"),
    ]:
        target = ROOT / "runs" / label
        target.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="cce-finite-") as tmp:
            script = Path(tmp) / program
            shutil.copyfile(ROOT / "original" / program, script)
            command = [sys.executable, "-I", str(script)] + args
            start = datetime.datetime.now(datetime.timezone.utc).isoformat()
            tick = time.monotonic()
            result = subprocess.run(command, capture_output=True, cwd=tmp)
            duration = time.monotonic() - tick
            (target / "stdout.txt").write_bytes(result.stdout)
            (target / "stderr.txt").write_bytes(result.stderr)
            event = {"entry": "original/" + program, "arguments": args,
                     "isolation": "unmodified copy in fresh temporary directory; python -I; assertions enabled",
                     "started_utc": start, "duration_seconds": duration,
                     "exit_code": result.returncode,
                     "program_sha256": sha(script.read_bytes()),
                     "stdout_sha256": sha(result.stdout), "stderr_sha256": sha(result.stderr)}
            (target / "execution.json").write_text(json.dumps(event, indent=2) + "\n")
            if result.returncode:
                raise RuntimeError(label + ": original entry failed; see captured stderr")
            data = (Path(tmp) / report_name).read_bytes()
            (target / "report.json").write_bytes(data)
        current = json.loads(data)
        frozen_bytes = (ROOT / "original" / frozen_name).read_bytes()
        frozen = json.loads(frozen_bytes)
        same = current == frozen
        comparison = {"label": label, "frozen": "original/" + frozen_name,
                      "report_sha256": sha(data), "byte_exact": data == frozen_bytes,
                      "json_equal": same}
        if label == "forty-two-ordered":
            projected = {k: v for k, v in current.items()
                         if k not in ("simple_dual_coefficients", "minimum_simple_dual_value")}
            projected["dual_rows"] = [{k: v for k, v in row.items() if k != "simple_dual_value"}
                                      for row in current["dual_rows"]]
            comparison.update({"new_top_level_fields": sorted(set(current) - set(frozen)),
                               "old_structure_exact_after_dropping_only_new_fields": projected == frozen,
                               "new_simple_dual_value_rows": sum("simple_dual_value" in r for r in current["dual_rows"])})
            assert projected == frozen
            assert set(current) - set(frozen) == {"simple_dual_coefficients", "minimum_simple_dual_value"}
            assert comparison["new_simple_dual_value_rows"] == 64
            assert not same and data != frozen_bytes
        else:
            assert same and data == frozen_bytes
        runs.append({**event, **comparison})
    verification = {"source_sha256_checks": len(manifest["sources"]),
                    "finite_original_entries_run": 3, "new_input_searches": 0, "runs": runs}
    (ROOT / "verification.json").write_text(json.dumps(verification, indent=2) + "\n")
    print(json.dumps(verification, indent=2))

if __name__ == "__main__":
    main()
