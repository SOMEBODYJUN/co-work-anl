"""Replay the unchanged source and reconcile its saved finite result."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ORIGINAL = HERE / "original"
OUT = HERE / "replay"


def main():
    manifest = json.loads((HERE / "source-manifest.json").read_text())
    for row in manifest:
        data = (HERE / row["preserved_path"]).read_bytes()
        if hashlib.sha256(data).hexdigest() != row["sha256"]:
            raise ValueError(f"Pinned source hash differs: {row['id']}")
    OUT.mkdir(exist_ok=True)
    env = {**os.environ, "PYTHONPATH": str(ORIGINAL), "PYTHONDONTWRITEBYTECODE": "1"}
    calls = []
    commands = [
        ("cli", [sys.executable, str(ORIGINAL / "probe_background.py")]),
        ("minimize", [sys.executable, "-c", "import json,probe_background;print(json.dumps(probe_background.minimize(),indent=2))"]),
        ("saved-check", [sys.executable, "-c", "import json,probe_background as p;from customer_attraction import Instance;z=json.load(open(" + repr(str(ORIGINAL / "background_nonmonotone.json")) + "));I=Instance.from_dict(z['instance']);rows=[(sum(1<<a for a in t.topics),t.multiplicity) for t in I.customers];ok,I,v,J,w=p.check(rows,tuple(z['base']),z['add'],z['r']);print(json.dumps({'ok':ok,'original':[str(v[0]),v[1]],'added':[str(w[0]),w[1]],'I_players':I.players,'J_players':J.players},indent=2))"]),
    ]
    for label, argv in commands:
        with tempfile.TemporaryDirectory(prefix="r51-background-") as temp:
            result = subprocess.run(argv, cwd=temp, env=env, capture_output=True, text=True,
                                    timeout=120, check=False)
        (OUT / f"{label}.stdout.txt").write_text(result.stdout)
        (OUT / f"{label}.stderr.txt").write_text(result.stderr)
        calls.append({"label": label, "argv": argv, "returncode": result.returncode,
                      "stdout_sha256": hashlib.sha256(result.stdout.encode()).hexdigest(),
                      "stderr_sha256": hashlib.sha256(result.stderr.encode()).hexdigest()})
        if result.returncode:
            raise RuntimeError(f"Unchanged replay failed: {label}")
    frozen = (ORIGINAL / "background_nonmonotone.json").read_bytes()
    minimized = (OUT / "minimize.stdout.txt").read_bytes()
    cli = json.loads((OUT / "cli.stdout.txt").read_text())
    comparison = {"python": sys.version, "commands": calls,
                  "minimize_JSON_fields_equal_frozen": json.loads(minimized) == json.loads(frozen),
                  "minimize_stdout_equal_frozen_bytes": minimized == frozen,
                  "minimize_stdout_without_one_final_LF_equal_frozen_bytes": minimized.removesuffix(b"\n") == frozen,
                  "default_run_seed": cli.get("seed"), "default_run_trial": cli.get("trial"),
                  "default_run_fields": sorted(cli),
                  "historical_invocation": "not recorded; current reproduction does not prove historical invocation"}
    (OUT / "replay-summary.json").write_text(json.dumps(comparison, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: comparison[k] for k in ("minimize_JSON_fields_equal_frozen", "minimize_stdout_equal_frozen_bytes", "default_run_seed", "default_run_trial")}))


if __name__ == "__main__":
    main()
