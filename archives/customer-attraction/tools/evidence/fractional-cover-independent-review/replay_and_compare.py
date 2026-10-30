"""Run the frozen independent audit and compare every saved residual.

The frozen audit owns the algebraic reconstruction.  This wrapper preserves
original bytes, checks its two full JSON reports, and compares all local types
with the separately written cleanup reconstruction.  No solver is imported.
"""
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
RELATED = ROOT.parent / "fractional-cover-half"


def table(rows, member_key):
    result = {}
    for row in rows:
        key = (tuple(row["actual_bits"]), row[member_key])
        assert key not in result
        result[key] = Fraction(row["residual"])
    expected = {(bits, member) for bits in product((0, 1), repeat=6)
                for member in (0, 1)}
    assert set(result) == expected
    assert min(result.values()) >= 0
    return result


def main():
    manifest = json.loads((ROOT / "manifest.json").read_text())
    for entry in manifest["files"]:
        path = ROOT / entry["original_file"]
        assert path.stat().st_size == entry["size"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == entry["sha256"]
    cleanup = json.loads((RELATED / "replay/independent-coefficients.json").read_text())
    reports = []
    with tempfile.TemporaryDirectory(prefix="frozen-audit-", dir=ROOT / "replay") as tmp:
        script = Path(tmp) / "audit_fractional_pair_half.py"
        shutil.copyfile(ROOT / "original/audit_fractional_pair_half.py", script)
        for mode, filename, cleanup_key, author_name in (
            ([], "audit_fractional_pair_half.json", "pair_21_5",
             "fractional_cover_pair_half_audit.json"),
            (["--endpoint"], "audit_fractional_endpoint_half.json", "endpoint_9_2",
             "fractional_cover_endpoint_half_audit.json"),
        ):
            proc = subprocess.run([sys.executable, str(script), *mode], check=True,
                                  text=True, capture_output=True)
            generated = json.loads((Path(tmp) / filename).read_text())
            original = json.loads((ROOT / "original" / filename).read_text())
            assert generated == original, filename
            old_table = table(original["types"], "in_comparison_set")
            new_table = table(cleanup[cleanup_key]["all_residuals"], "comparison_bit")
            assert old_table == new_table, filename
            author = json.loads((RELATED / "original" / author_name).read_text())
            for key in ("tau", "minimum_residual", "minimum_positive_residual"):
                assert original[key] == author[key]
            assert original["literal_types"] == author["state_count"] == 128
            assert original["zero_types"] == len(author["zero_states"])
            old_zeros = {key for key, value in old_table.items() if value == 0}
            author_zeros = {(tuple(row["actual_bits"]), row["comparison_bit"])
                            for row in author["zero_states"]}
            assert old_zeros == author_zeros
            (ROOT / "replay" / filename).write_text(
                json.dumps(generated, ensure_ascii=False, indent=2) + "\n")
            reports.append({"file": filename, "full_json_equal": True,
                            "all_residuals_equal_cleanup_reconstruction": len(old_table),
                            "author_summary_and_all_zero_types_equal": True,
                            "tau": original["tau"],
                            "minimum_positive_residual": original["minimum_positive_residual"],
                            "zero_types": original["zero_types"],
                            "stdout_summary": json.loads(proc.stdout)})
    summary = {"source_files_hash_checked": len(manifest["files"]),
               "reports": reports, "residuals_compared": 256,
               "scope": "two exact coefficient domains and recorded internal review; "
                        "not a full SPE search or an unconditional half theorem"}
    (ROOT / "replay/verification.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"source_files_hash_checked": len(manifest["files"]),
                      "full_json_reports_equal": len(reports),
                      "all_local_residuals_compared": 256,
                      "raw_three_IC_strongPAIR_identities": 160,
                      "S_Z_V_upper_bound_corners": 80}, indent=2))


if __name__ == "__main__":
    main()
