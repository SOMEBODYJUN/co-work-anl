#!/usr/bin/env python3
"""Replay the unchanged frozen audit with the final frozen article dependency."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ARCHIVE = HERE.parents[2]
CODE = "tests/audits/weighted_congestion/linear_threshold_article_cost_split.py"
TEX = "research/current/weighted_congestion/linear_threshold_article.tex"
OLD = "evidence/runs/weighted_congestion/linear_threshold_article_cost_split.json"


def differences(a, b, path=""):
    if type(a) is not type(b):
        return [{"path": path, "old": a, "new": b}]
    if isinstance(a, dict):
        result = []
        for key in sorted(a.keys() | b.keys()):
            if key not in a or key not in b:
                result.append({"path": path + "/" + key, "old": a.get(key), "new": b.get(key)})
            else:
                result.extend(differences(a[key], b[key], path + "/" + key))
        return result
    if isinstance(a, list):
        if len(a) != len(b):
            return [{"path": path, "old": a, "new": b}]
        return [x for i, (u, v) in enumerate(zip(a, b)) for x in differences(u, v, path + "/" + str(i))]
    return [] if a == b else [{"path": path, "old": a, "new": b}]


def main():
    if sys.flags.optimize:
        raise SystemExit("assertions must be enabled")
    output = HERE / "replay"
    output.mkdir(exist_ok=True)
    old = json.loads((HERE / "original" / OLD).read_text())
    with tempfile.TemporaryDirectory(prefix="linear-cost-split-", dir=HERE) as temporary:
        root = Path(temporary)
        code = root / CODE
        tex = root / TEX
        code.parent.mkdir(parents=True)
        tex.parent.mkdir(parents=True)
        shutil.copy2(HERE / "original" / CODE, code)
        shutil.copy2(ARCHIVE / "papers/linear-article-assets/linear_threshold_article.tex", tex)
        command = [sys.executable, str(code), "--output", str(root / "new-cost-split.json")]
        run = subprocess.run(command, cwd=root, capture_output=True, text=True)
        (output / "cost-split-stdout.txt").write_text(run.stdout)
        (output / "cost-split-stderr.txt").write_text(run.stderr)
        if run.returncode:
            raise SystemExit("source audit exited " + str(run.returncode))
        raw = (root / "new-cost-split.json").read_bytes()
        new = json.loads(raw)
        (output / "cost_split.json").write_bytes(raw)
        delta = differences(old, new)
        mathematical_delta = [x for x in delta if x["path"] not in ("/article_sha256", "/command")]
        result = {
            "status": "passed" if not mathematical_delta else "failed",
            "command": command,
            "exit_code": run.returncode,
            "source_sha256": hashlib.sha256(code.read_bytes()).hexdigest(),
            "unchanged_source": hashlib.sha256(code.read_bytes()).hexdigest() == old["code_sha256"],
            "differences": delta,
            "mathematical_differences": mathematical_delta,
            "expected_metadata_difference": "The frozen report binds an earlier work-in-progress article; this run reads the final frozen TeX. The command uses the actual isolated path.",
            "states": sum(x["states"] for x in new["results"]),
            "deviations_including_self": sum(x["deviations_including_self"] for x in new["results"]),
            "scope": "Three literal finite cost identities; no preprocessing of zero-only-strategy players and no proof of a general equilibrium existence theorem.",
        }
        (HERE / "replay-comparison.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if mathematical_delta or not result["unchanged_source"]:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
