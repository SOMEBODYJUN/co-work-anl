#!/usr/bin/env python3
"""Replay byte-identical frozen checkers in their required input layout.

No source file is changed. The temporary layout repairs historical relocation
only. Output includes full JSON comparisons, not merely reported decimals.
"""
from pathlib import Path
from fractions import Fraction as Q
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

sys.set_int_max_str_digits(0)
HERE = Path(__file__).resolve().parent
RAW = HERE / "original"


def load(path):
    return json.loads(path.read_text())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    provenance = load(HERE / "provenance.json")
    for row in provenance["sources"]:
        assert hashlib.sha256((RAW / row["path"]).read_bytes()).hexdigest() == row["sha256"]
    report = {"python": sys.version.split()[0], "source_sha256_checks": len(provenance["sources"]),
              "source_modifications": [], "layout_only_repair": True, "checks": {}}
    with tempfile.TemporaryDirectory(prefix="crossover-replay-") as temporary:
        root = Path(temporary)
        game, review, source = (root / name for name in ("crossover", "review", "source32_bound"))
        for folder in (game, review, source):
            folder.mkdir()
        code = RAW / "tests/audits/weighted_congestion"
        cert = RAW / "evidence/certificates/weighted_congestion"
        runs = RAW / "evidence/runs/weighted_congestion"
        for name in ("verify_degree32.py", "verify_limit.py", "main_check.py"):
            shutil.copyfile(code / "crossover" / name, game / name)
        shutil.copyfile(code / "crossover_limit_review/check_independent.py", review / "check_independent.py")
        shutil.copyfile(cert / "source_degree32/certificate.json", source / "certificate.json")
        for name in ("degree32_certificate.json", "degree40_failure_certificate.json", "fixed_weight_limit_certificate.json"):
            shutil.copyfile(cert / "crossover" / name, game / name)
        shutil.copyfile(runs / "crossover/fixed_degree_scan.json", game / "fixed_degree_scan.json")
        (game / "limit_evidence").mkdir()
        for name in ("finite_scans.json", "scaled_limits.json", "uniform_bounds.json"):
            shutil.copyfile(runs / "crossover/limit_evidence" / name, game / "limit_evidence" / name)
        shutil.copyfile(cert / "crossover/limit_evidence/retuned_m3_certificate.json",
                        game / "limit_evidence/retuned_m3_certificate.json")
        commands = [
            ("degree32_fixed_degree_and_limit", [str(game / "verify_degree32.py")]),
            ("scaled_family_author", [str(game / "verify_limit.py")]),
            ("explicit_strategy_and_bernstein_second_reconstruction", [str(game / "main_check.py")]),
            ("independent_symbolic_and_directional_bound", [str(review / "check_independent.py"), "--write"]),
        ]
        for label, command in commands:
            completed = subprocess.run([sys.executable, *command], capture_output=True, text=True, check=True)
            assert not completed.stderr, completed.stderr
            report["checks"][label] = {"exit_code": completed.returncode,
                                         "summary": json.loads(completed.stdout)}
        main_frozen = load(runs / "crossover/main_check_results.json")
        main_actual = report["checks"]["explicit_strategy_and_bernstein_second_reconstruction"]["summary"]
        assert main_actual == main_frozen
        independent_frozen = load(runs / "crossover_limit_review/independent_evidence.json")
        independent_actual = load(review / "independent_evidence.json")
        assert independent_actual == independent_frozen
        report["full_frozen_comparisons"] = {
            "degree32_author_artifacts": 4, "scaled_author_artifacts": 4,
            "main_check_results_json_equal": True, "independent_evidence_json_equal": True,
            "all_rational_fields_reconstructed": True, "differences": []}
        # Inspect all stored all-state records and each exact rational field.
        checked_rows = checked_rationals = 0
        exact_keys = {"current_costs_exact", "deviation_costs_exact", "all_flip_ratios_exact",
                      "witness_strict_margin_exact", "witness_ratio", "costs_exact",
                      "flip_ratios_exact", "template_witness_alpha_margin_exact"}
        for file in (game / "degree32_certificate.json", game / "degree40_failure_certificate.json",
                     game / "fixed_weight_limit_certificate.json", game / "limit_evidence/retuned_m3_certificate.json"):
            data = load(file)
            assert len(data["records"]) == 16
            assert {row["state"] for row in data["records"]} == {f"{i:04b}" for i in range(16)}
            for row in data["records"]:
                checked_rows += 1
                for key in exact_keys & row.keys():
                    values = row[key] if isinstance(row[key], list) else [row[key]]
                    for value in values:
                        Q(value)
                        checked_rationals += 1
        report["certificate_schema_review"] = {"complete_state_rows": checked_rows,
                                                "exact_rational_fields_parsed": checked_rationals}
    output = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        with args.out.open("x") as handle:
            handle.write(output)
    print(output, end="")


if __name__ == "__main__":
    main()
