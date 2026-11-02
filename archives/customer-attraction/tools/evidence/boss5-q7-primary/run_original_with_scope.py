"""Execute the untouched original main once and preserve its computed locals.

The extra scope arithmetic is informed review, not a second original replay.
No LP, strategy construction, or SPE enumerator is invoked.
"""
import contextlib
from fractions import Fraction as F
import hashlib
import io
import json
from pathlib import Path
import runpy
import sys
import time

ROOT = Path(__file__).resolve().parent
ORIGINAL = ROOT / "original/ef96d599cbb1a11171b5/q7_joint_row_obstruction.py"
OUT = ROOT / "run"
OUT.mkdir(exist_ok=True)
captured = {}


def profile(frame, event, arg):
    if event == "return" and frame.f_code.co_name == "main" and Path(frame.f_code.co_filename) == ORIGINAL:
        captured.update(frame.f_locals)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


before = digest(ORIGINAL)
start = time.monotonic()
stdout, stderr = io.StringIO(), io.StringIO()
sys.setprofile(profile)
try:
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        namespace = runpy.run_path(str(ORIGINAL), run_name="__main__")
finally:
    sys.setprofile(None)
elapsed = time.monotonic() - start
assert digest(ORIGINAL) == before
support = namespace["SUPPORT"]
weights = namespace["WEIGHTS"]
assert all(w > 0 for w in weights)
assert len(set(captured["cols"])) == 1631
assert len(set(support)) == len(support) == len(weights) == 17
pairs = namespace["PAIRS"]
row_names = [f"M{t}" for t in range(6)] + [f"L{j}" for j in range(7)] + [f"T{j},{k}" for j, k in pairs]
original = {
    "column_count": len(captured["cols"]),
    "support_count": len(support),
    "weight_sum": str(sum(weights, F(0))),
    "all_weights_strictly_positive": True,
    "base_average": str(captured["base_average"]),
    "row_averages": {name: str(value) for name, value in zip(row_names, captured["averages"])},
    "support": [{"I": i, "J": j, "weight": str(w)} for (i, j), w in zip(support, weights)],
}
(OUT / "original-main-details.json").write_text(json.dumps(original, ensure_ascii=False, indent=2) + "\n")
(OUT / "original.stdout.txt").write_text(stdout.getvalue())
(OUT / "original.stderr.txt").write_text(stderr.getvalue())

# Scope corrections: fixed six-set targets, exact actual-load deviations,
# the stronger mixed M4, and the existing strong-pair overlap correction.
private = [sum((w for (i, _), w in zip(support, weights) if i == 1 << j), F(0)) for j in range(7)]
fixed_six = [captured["base_average"] + p / 2 for p in private]
deviations = {}
strong_pair = {}
for t in range(6):
    for label in range(7):
        value = F(0)
        for (i, j), w in zip(support, weights):
            count = j.bit_count()
            pay = F((j >> t) & 1, count) if count else F(0)
            prior = (j & ((1 << t) - 1)).bit_count()
            value += w * (pay - F((i >> label) & 1, prior + 6 - t))
        deviations[f"D{t},{label}"] = value
for index, (a, b) in enumerate(pairs):
    overlap = sum((w * F(1, ((j & 15).bit_count() + 1) * ((j & 15).bit_count() + 2))
                   for (i, j), w in zip(support, weights) if (i >> a) & 1 and (i >> b) & 1), F(0))
    strong_pair[f"PAIR{a},{b}"] = captured["averages"][13 + index] - overlap
shared_mass = sum((w for (i, _), w in zip(support, weights) if 2 <= i.bit_count() <= 6), F(0))
strong_m4 = captured["averages"][4] - shared_mass * (F(1, 11) - F(1, 12))
scope = {
    "kind": "informed-exact-scope-review-not-original-output",
    "private_masses": {f"X{j}": str(p) for j, p in enumerate(private)},
    "fixed_six_set_target_averages": {f"omit{j}": str(p) for j, p in enumerate(fixed_six)},
    "true_OPT6_target_average": str(min(fixed_six)),
    "minimum_private_labels": [j for j, p in enumerate(private) if p == min(private)],
    "source_shared_floor": ["1/21", "2/37", "1/16", "2/27", "1/12", "7/72"],
    "stronger_mixed_M4_average": str(strong_m4),
    "actual_load_deviation_averages": {name: str(value) for name, value in deviations.items()},
    "strong_pair_averages": {name: str(value) for name, value in strong_pair.items()},
}
(OUT / "scope-review.json").write_text(json.dumps(scope, ensure_ascii=False, indent=2) + "\n")
record = {
    "status": "passed",
    "original_main_invocations": 1,
    "direct_original_CLI_invocations": 0,
    "wrapper_path": str(Path(__file__).resolve()),
    "wrapper_sha256": digest(Path(__file__)),
    "original_path": str(ORIGINAL),
    "original_sha256_before": before,
    "original_sha256_after": digest(ORIGINAL),
    "argv": sys.argv,
    "python": sys.version,
    "cwd": str(Path.cwd()),
    "assertions_enabled": __debug__,
    "elapsed_seconds_original": elapsed,
    "stdout_bytes": len(stdout.getvalue().encode()),
    "stderr_bytes": len(stderr.getvalue().encode()),
    "scope_calculation": "one informed supplementary exact computation on the same literal support",
    "LP_strategy_search_complete_SPE_invocations": 0,
}
(OUT / "run.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": "passed", "original_main_invocations": 1, "base_average": original["base_average"], "true_OPT6_target_average": scope["true_OPT6_target_average"], "negative_D": {k: str(v) for k, v in deviations.items() if v < 0}, "stronger_M4": str(strong_m4)}, ensure_ascii=False))
