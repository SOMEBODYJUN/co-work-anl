"""Reproduce the eight-example report and check the saved background point.

Run this file beside source-root/, manifest.json, dependency-manifest.json.
The original 3000-trial module is intentionally never imported.
"""
from pathlib import Path
from fractions import Fraction
from functools import lru_cache
import hashlib
import importlib.util
import json
import random
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE / "source-root"
RUNS = HERE / "runs"
RUNS.mkdir(exist_ok=True)
R4 = ROOT / "research/workspaces/customer-attraction/R-4ffa8b85fa8847e09e45dcafc8e1326f/induction"
R7 = ROOT / "research/workspaces/customer-attraction/R-7e9f44beea424d469713364afe7dd180/background_induction"

for manifest in ("manifest.json", "dependency-manifest.json"):
    for row in json.loads((HERE / manifest).read_text()):
        p = ROOT / row["path"]
        assert p.stat().st_size == row["size"]
        assert hashlib.sha256(p.read_bytes()).hexdigest() == row["sha256"]

process = subprocess.run([sys.executable, str(R4 / "check_background_old_examples.py")],
                         cwd=ROOT, text=True, capture_output=True, check=True)
(RUNS / "old-examples.stdout.json").write_text(process.stdout)
(RUNS / "old-examples.stderr.txt").write_text(process.stderr)
observed = json.loads(process.stdout)
expected = json.loads((R4 / "background_old_examples.json").read_text())
assert observed == expected

sys.path.insert(0, str(ROOT))
from customer_attraction.model import Instance, CustomerType
from customer_attraction.exact import ExactSPESolver

spec = importlib.util.spec_from_file_location("background_original", R7 / "search_background.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
saved = json.loads((R7 / "background_best.json").read_text())
q, r, prefix = saved["q"], saved["r"], tuple(saved["prefix"])
weights = {int(k): v for k, v in saved["weights"].items()}
solver = module.BackgroundSolver(q, r, prefix, weights)
instance = Instance(tuple(map(str, range(q))), tuple(
    CustomerType(frozenset(a for a in range(q) if mask >> a & 1), weight)
    for mask, weight in weights.items()), sum(prefix) + r)
norm = ExactSPESolver(instance)
canonical = norm.outcomes(prefix)
bitset = {tuple(prefix[a] + c[a] for a in range(q))
          for i, c in enumerate(solver.terminals) if solver.out >> i & 1}
assert bitset == canonical
thresholds = 0
for c, threshold in solver.thresholds.items():
    total = tuple(prefix[a] + c[a] for a in range(q))
    assert norm.threshold(total) * solver.scale == threshold
    thresholds += 1
minimum, actual = solver.minimum()
optimum, optimal = solver.optimum()
assert minimum == Fraction(saved["minimum"])
assert optimum == Fraction(saved["optimum"])
assert optimum / minimum == Fraction(saved["ratio"])
assert tuple(saved["actual"]) == actual
assert tuple(saved["opt"]) == optimal

# Reproduce the generator up to the saved trial, without any oracle calls or writes.
rng = random.Random(saved["seed"])
for trial in range(saved["trial"] + 1):
    generated_prefix = [0] * q
    for _ in range(rng.randrange(0, 6)):
        generated_prefix[rng.randrange(q)] += 1
    generated_weights = {mask: rng.randrange(1, 31) for mask in rng.sample(
        range(1, 1 << q), rng.randrange(q, min(3*q, 1 << q)))}
assert tuple(generated_prefix) == prefix and generated_weights == weights

bgmask = sum(1 << a for a in range(q) if prefix[a])
def new_coverage(c):
    return sum(w for mask, w in weights.items() if not mask & bgmask
               and any(c[a] and mask >> a & 1 for a in range(q)))
maxnew = max(map(new_coverage, solver.terminals))
actualnew = new_coverage(actual)

# Reconstruct one full ordered tail strategy, using the bitset outcome sets.
# Its finite incentive audit below uses literal per-unit-customer fractions.
actions = {}
def unpack(bits):
    while bits:
        bit = bits & -bits
        yield solver.terminals[bit.bit_length() - 1]
        bits -= bit
def inc(c, a):
    return c[:a] + (c[a]+1,) + c[a+1:]
def expand(history, c, desired):
    if len(history) == r:
        assert c == desired
        return
    floor = solver.thresholds[c]
    admissible = [a for a in range(q)
                  if solver.solve(inc(c, a)) >> solver.tidx[desired] & 1
                  and solver.pays[solver.tidx[desired]][a] >= floor]
    chosen = min(admissible)
    actions[history] = chosen
    for a in range(q):
        child = inc(c, a)
        target = desired if a == chosen else min(unpack(solver.solve(child)),
            key=lambda t: (solver.pays[solver.tidx[t]][a], t))
        expand(history+(a,), child, target)
expand((), (0,)*q, actual)
unit_masks = [mask for mask, weight in weights.items() for _ in range(weight)]
@lru_cache(None)
def literal_pay(c, a):
    total = tuple(prefix[j]+c[j] for j in range(q))
    return sum((Fraction(1, sum(total[j] for j in range(q) if mask >> j & 1))
                for mask in unit_masks if mask >> a & 1), Fraction(0))
histories = comparisons = 0
def audit(history, c):
    global histories, comparisons
    if len(history) == r:
        return c
    leaves = [audit(history+(a,), inc(c, a)) for a in range(q)]
    chosen = actions[history]
    chosenpay = literal_pay(leaves[chosen], chosen)
    histories += 1
    for a in range(q):
        assert chosenpay >= literal_pay(leaves[a], a)
        comparisons += 1
    return leaves[chosen]
assert audit((), (0,)*q) == actual
certificate = {"prefix_counts": prefix, "remaining_players": r,
    "terminal_remaining_counts": actual,
    "actions": [{"history": h, "action": a}
                for h, a in sorted(actions.items(), key=lambda item:(len(item[0]), item[0]))]}
(RUNS / "saved-point-complete-tail-strategy.json").write_text(
    json.dumps(certificate, separators=(",", ":"))+"\n")

report = {
    "nine_primary_hashes_and_twelve_dependency_hashes": "matched",
    "old_report_all_fields_match": observed == expected,
    "old_report_checks": observed["checks"],
    "saved_point": {
        "generator_through_trial": saved["trial"], "generator_input_match": True,
        "q": q, "r": r, "prefix_players": sum(prefix), "unit_customers": len(unit_masks),
        "lcm_scale": solver.scale, "terminal_vectors": len(solver.terminals),
        "count_states": len(norm._outcomes), "decision_thresholds_compared": thresholds,
        "all_root_outcomes_equal": bitset == canonical,
        "root_outcomes": len(bitset), "active_profit_minimum": str(minimum),
        "active_profit_optimum": str(optimum), "profit_ratio": str(optimum/minimum),
        "actual_remaining_counts": actual, "optimal_remaining_counts": optimal,
        "actual_new_coverage": actualnew, "maximum_new_coverage": maxnew,
        "background_candidate_slack": str(minimum+actualnew-maxnew),
        "ordered_tail_histories_checked": histories,
        "ordered_tail_comparisons_including_self": comparisons,
        "full_saved_strategy_valid": True,
    },
    "not_executed": ["original random main", "search_invariants.py import or 3000-trial loop"],
}
(RUNS / "reconciliation.json").write_text(json.dumps(report, indent=2)+"\n")
print(json.dumps(report, indent=2))
