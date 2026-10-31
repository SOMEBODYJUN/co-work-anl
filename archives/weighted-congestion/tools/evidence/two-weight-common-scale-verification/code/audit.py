"""Isolated replay plus independent exact closed-form reconstruction.

Run from any working directory.  This script never writes to the exported
source directory, invokes git/work.py, or reads credentials.
"""
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time


HERE = Path(__file__).resolve().parent
SOURCES = HERE.parent / "sources"
SOURCE = SOURCES / "7439aa6018b0b8ea7499--verify_universal.py"
FROZEN = SOURCES / "ddcab84081659b17abfa--verify_universal.json"
REPLAY = HERE / "replay"
REPLAY.mkdir(exist_ok=True)


def identity(path):
    raw = path.read_bytes()
    return {"path": str(path.relative_to(HERE.parent)), "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest()}


assert identity(SOURCE)["sha256"] == "9a71ae1d252d7d5261664d3784cbaea0588d28acbcecb37319b1f780cfff917f"
assert identity(FROZEN)["sha256"] == "9b515bd165db52bbf10bf1389725e566141dec539181978fd0a715b8d81f2eb3"
original_copy = REPLAY / "verify_universal.py"
shutil.copyfile(SOURCE, original_copy)
started = time.monotonic()
run = subprocess.run([sys.executable, str(original_copy)], cwd=REPLAY,
                     text=True, capture_output=True, check=False)
duration = time.monotonic() - started
(REPLAY / "stdout.txt").write_text(run.stdout)
(REPLAY / "stderr.txt").write_text(run.stderr)
assert run.returncode == 0, run.stderr
actual = json.loads((REPLAY / "verify_universal.json").read_text())
frozen = json.loads(FROZEN.read_text())
assert actual == frozen
assert (REPLAY / "verify_universal.json").read_bytes() == FROZEN.read_bytes()
assert run.stdout == FROZEN.read_text() + "\n"

# This independent reconstruction uses the derived marginal polynomial,
# rather than importing source F/S2/H1 or evaluating their finite differences.
alpha, h = Q(64, 59), Q(59, 32)
classes = []
total = 0
for name, degree in [("quadratic", 2), ("affine", 1), ("constant", 0)]:
    for weight, scale in [(1, Q(1)), (2, h)]:
        lower = upper = None
        lo_at, hi_at = [], []
        for k in range(101):
            for l in range(101):
                load = k + 2 * l
                if degree == 2:
                    ratio = (Q(1) + Q(3 * l, 4 * (load + 1) ** 2)
                             if weight == 1
                             else Q(2) - Q(5 * k, 4 * (load + 2) ** 2))
                else:
                    ratio = Q(weight)
                assert scale <= ratio <= alpha * scale
                if lower is None or ratio < lower:
                    lower, lo_at = ratio, [[k, l]]
                elif ratio == lower:
                    lo_at.append([k, l])
                if upper is None or ratio > upper:
                    upper, hi_at = ratio, [[k, l]]
                elif ratio == upper:
                    hi_at.append([k, l])
                total += 1
        key = f"{name}_w{weight}"
        assert actual["extrema"][key] == [str(lower), str(upper)]
        classes.append({"key": key, "degree": degree, "weight": weight,
                        "scale": str(scale), "count": 101**2,
                        "min": str(lower), "max": str(upper),
                        "normalized_min": str(lower / scale),
                        "normalized_max": str(upper / scale),
                        "argmin_count": len(lo_at), "argmax_count": len(hi_at),
                        "first_argmin": lo_at[0], "first_argmax": hi_at[0]})
assert total == actual["finite_checks"] == 61206

# A finite algebra check of independently derived difference expressions.
# The full integer-domain justification is separately supplied in the draft.
def q2(t):
    return Q(t * (t + 1) * (2 * t + 1), 6)


def reconstructed_potential(k, l):
    return 8*q2(l) + q2(k) + 2*l*k*(k+1) + 4*l*l*k + Q(3, 4)*k*l


formula_checks = 0
for k in range(101):
    for l in range(101):
        load = k + 2*l
        assert reconstructed_potential(k+1, l)-reconstructed_potential(k, l) == (load+1)**2+Q(3,4)*l
        assert reconstructed_potential(k, l+1)-reconstructed_potential(k, l) == 2*(load+2)**2-Q(5,4)*k
        formula_checks += 2

manifest = {
    "source": identity(SOURCE), "frozen_report": identity(FROZEN),
    "replayed_copy": identity(original_copy),
    "replayed_report": identity(REPLAY / "verify_universal.json"),
    "python": platform.python_version(), "python_executable": sys.executable,
    "python_optimization_flag": sys.flags.optimize,
    "command": [sys.executable, str(original_copy)],
    "cwd": str(REPLAY), "exit_code": run.returncode,
    "runtime_seconds": duration,
    "original_program_runs": 1,
    "source_copy_byte_equal": original_copy.read_bytes() == SOURCE.read_bytes(),
    "generated_json_byte_equal": True, "generated_json_field_equal": True,
    "stdout_equals_frozen_json_plus_newline": True,
    "stderr_empty": run.stderr == "",
    "independent_formula_ratio_checks": total,
    "independent_difference_identity_checks": formula_checks,
    "classes": classes,
    "not_established_by_finite_checks": [
        "all nonnegative integer populations", "global optimality",
        "arbitrary weights or degree above two", "strategy-profile or improvement-path enumeration",
        "polynomial improvement-path length", "literature novelty"],
    "proof_filename_note": "UNIVERSAL_SCALING_ATTACK.md is a literal metadata string; the program does not open or verify that document. No such path was found in the local materialized files or the inspected cleanup inventory/increment. The existing finite_weight_scaled_potential.md and formal theorem supply the all-integer-domain proof.",
}
(HERE / "run-analysis.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"original_program_runs": 1, "exit_code": run.returncode,
                  "generated_json_byte_equal": True, "finite_checks": total,
                  "independent_difference_identity_checks": formula_checks,
                  "report_sha256": manifest["replayed_report"]["sha256"]}, indent=2))
