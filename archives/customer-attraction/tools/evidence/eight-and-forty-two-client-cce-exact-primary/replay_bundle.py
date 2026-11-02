"""Check preserved bytes and replay the three unmodified historical CCE audits.

This is a replay/integration check, not a new independent mathematical verifier.
Run without -O so the assertions in the original programs remain active.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def load(relative):
    return json.loads((ROOT / relative).read_text())


def require(condition, description):
    if not condition:
        raise RuntimeError(description)


def main():
    manifest = load("source-manifest.json")
    for source in manifest["sources"]:
        raw = (ROOT / source["preserved_path"]).read_bytes()
        require(len(raw) == source["size"], source["id"] + " size")
        require(hashlib.sha256(raw).hexdigest() == source["sha256"], source["id"] + " SHA-256")

    results = {}
    for record in manifest["replays"]:
        # -I ignores Python optimization/import settings from the caller's environment.
        completed = subprocess.run(
            [sys.executable, "-I", str(ROOT / record["script"])],
            cwd=ROOT, capture_output=True, check=True,
        )
        raw = completed.stdout
        expected = (ROOT / record["output"]).read_bytes()
        require(raw == expected, record["script"] + " complete stdout differs")
        require(hashlib.sha256(raw).hexdigest() == record["output_sha256"], record["output"] + " SHA-256")
        results[Path(record["script"]).name] = json.loads(raw)

    count = results["verify_eight_client_cce.py"]
    ordered = results["verify_eight_client_cce_ordered_source.py"]
    forty_two = results["verify_cce_counterexample.py"]
    require(count == load("original/eight_client_cce_exact.json"), "count frozen report")
    require(count == load("original/eight_client_cce_verification_stdout.json"), "stdout frozen report")
    require(ordered == load("original/eight_client_cce_ordered_source.json"), "ordered frozen report")
    exact_bytes = (ROOT / "original/eight_client_cce_exact.json").read_bytes()
    stdout_bytes = (ROOT / "original/eight_client_cce_verification_stdout.json").read_bytes()
    require(stdout_bytes == exact_bytes + b"\n", "historical stdout newline identity")
    require([key for key in count if count[key] != ordered[key]] == ["histories"], "unexpected strategy-version change")
    differences = [a["history"] for a, b in zip(count["histories"], ordered["histories"]) if a != b]
    require(differences == [[1], [1, 2]], "unexpected changed histories")
    require(forty_two["welfare"] == 32 and forty_two["optimum"] == 42, "42-client summary")
    require(forty_two["cce_min_dual_expression"] == "33", "42-client fixed dual lower bound")
    report = {
        "status": "original-byte-replays-and-version-comparisons-passed",
        "original_files_sha256_checked": len(manifest["sources"]),
        "unmodified_programs_replayed": len(manifest["replays"]),
        "eight_count": {"histories": count["history_count"], "comparisons": count["comparison_count"],
                        "welfare": count["welfare"], "minimum_cce_welfare": count["sharp_cce_welfare"],
                        "security_value": count["security_value"]},
        "eight_ordered_changed_histories": differences,
        "forty_two": {"comparisons": forty_two["spe_comparisons"], "welfare": forty_two["welfare"],
                      "optimum": forty_two["optimum"], "fixed_dual_lower_bound": forty_two["cce_lower_bound"],
                      "sharp_minimum_not_claimed": True},
        "proof_identity": "historical implementations replayed; no new independent audit or discovery LP",
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
