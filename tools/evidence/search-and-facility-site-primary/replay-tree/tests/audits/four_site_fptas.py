"""Independent definition-level, exact finite audit of the four-site gap.

No equilibrium solver is imported. Closed support cells include all endpoints;
each accepted cell is checked through the original conditional-cost definition.
Full enumeration on all ten unordered layouts gives exact coordinate threats
and independently optimizes all sixteen labeled layouts. Finite audits do not
prove the reduction or classify its general approximation complexity.
"""
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from pathlib import Path
import argparse
import hashlib
import json
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from facility_spe.shared.four_site_fptas_hardness import parameters, reduction


def cells(instance, s, t):
    weights = instance["weights"]
    left, right = map(set, (instance["locations"][s], instance["locations"][t]))
    shared = sorted(left & right)
    a = sum(weights[i] for i in left - right)
    b = sum(weights[i] for i in right - left)
    v = a + b + sum(weights[i] for i in shared)
    out, enumerated, accepted, comparisons = [], 0, 0, 0
    for state in product((-1, 0, 1), repeat=len(shared)):
        enumerated += 1
        mixed = state.count(0)
        numerator = a - b + sum(weights[i] * z for i, z in zip(shared, state))
        lo, hi = -v, v
        for i, z in zip(shared, state):
            if z <= 0:
                lo = max(lo, -weights[i])
            if z >= 0:
                hi = min(hi, weights[i])
        if lo > hi:
            continue
        if mixed == 1:
            if numerator:
                continue
            dl, dh = F(lo), F(hi)
        else:
            denominator = 1 - mixed
            if denominator < 0:
                numerator, denominator = -numerator, -denominator
            if not lo * denominator <= numerator <= hi * denominator:
                continue
            dl = dh = F(numerator, denominator)
        accepted += 1
        for delta in {dl, dh, (dl + dh) / 2}:
            probabilities = [F(0) if z == -1 else F(1) if z == 1
                             else (1 + delta / weights[i]) / 2
                             for i, z in zip(shared, state)]
            x = a + sum((weights[i] * p for i, p in zip(shared, probabilities)), F(0))
            y = b + sum((weights[i] * (1 - p) for i, p in zip(shared, probabilities)), F(0))
            assert x - y == delta and x + y == v
            for i, prob in zip(shared, probabilities):
                assert 0 <= prob <= 1
                cost1, cost2 = x + (1 - prob) * weights[i], y + prob * weights[i]
                if prob > 0:
                    comparisons += 1
                    assert cost1 <= cost2
                if prob < 1:
                    comparisons += 1
                    assert cost2 <= cost1
        out.append((F(v + dl, 2), F(v + dh, 2), state))
    assert out
    return dict(s=s, t=t, v=v, shared=shared, cells=out,
                enumerated=enumerated, accepted=accepted, comparisons=comparisons)


def ratio(a, b):
    return F(a, b) if b else (F(0) if not a else None)


def audit(values):
    instance = reduction(values)
    p = parameters(values)
    n, scale = p["n"], p["scale"]
    normalized = [p["M"], *p["variables"], p["q"], n-p["q"], F(n),
                  p["R"]-p["M"]-p["q"], F(n, 5)]
    assert [w / scale for w in map(F, instance["weights"])] == normalized
    assert all(type(w) is int and 0 < w <= 200*n**3*p["total"] for w in instance["weights"])
    source_yes = any(2 * sum(x for x, sign in zip(values, mask) if sign) == p["total"]
                     for mask in product((0, 1), repeat=len(values)))
    encoded_yes = any(sum((w * sign for w, sign in zip(p["variables"], signs)), F(0)) == 0
                      for signs in product((-1, 1), repeat=n))
    assert source_yes == encoded_yes
    records = {(s, t): cells(instance, s, t) for s in range(4) for t in range(s, 4)}
    def minimum_first(s, t):
        rec = records[min(s, t), max(s, t)]
        if s <= t:
            return min(lo for lo, _, _ in rec["cells"])
        return rec["v"] - max(hi for _, hi, _ in rec["cells"])
    threats = [max(minimum_first(s, t) for s in range(4)) for t in range(4)]
    factors = {}
    for (s, t), rec in records.items():
        den = threats[t] + threats[s]
        ideal = F(rec["v"]) * threats[t] / den
        candidates = []
        for lo, hi, _ in rec["cells"]:
            x = min(hi, max(lo, ideal))
            r1, r2 = ratio(threats[t], x), ratio(threats[s], rec["v"]-x)
            if r1 is not None and r2 is not None:
                candidates.append(max(F(1), r1, r2))
        factors[s, t] = min(candidates) if candidates else None
    optimum = min(a for a in factors.values() if a is not None)
    if source_yes:
        assert optimum == F(13, 10)
    else:
        assert optimum >= F(13, 10) + F(1, 100*n*n)
        for lo, hi, state in records[0, 1]["cells"]:
            assert lo == hi, ("unexpected one-mixer interval", state)
            delta = (2*lo-records[0, 1]["v"]) / scale
            assert abs(delta-p["tau"]) >= F(3, 8*n)
    for pair, factor in factors.items():
        if pair != (0, 1) and factor is not None:
            assert factor > F(131, 100), (pair, factor)
    unique = {(0,2): [2*n, p["R"]-p["q"]], (1,2): [2*n,p["R"]],
              (0,3): [2*n,p["d"]], (1,3): [2*n,p["d"]],
              (2,3): [p["R"]-p["M"],p["d"]]}
    for pair, expected in unique.items():
        for lo, hi, _ in records[pair]["cells"]:
            assert lo == hi and [lo/scale, (records[pair]["v"]-lo)/scale] == expected
    return dict(source=values, n=n, yes=source_yes, alpha=str(optimum),
                layout_factors={f"{s},{t}": str(a) for (s,t),a in factors.items()},
                enumerated=sum(r["enumerated"] for r in records.values()),
                accepted_support_cells=sum(r["accepted"] for r in records.values()),
                conditional_cost_comparisons=sum(r["comparisons"] for r in records.values()))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    sources = [[x] for x in range(1, 7)]
    sources += [list(x) for x in combinations_with_replacement(range(1, 5), 2)]
    sources += [list(x) for x in combinations_with_replacement(range(1, 4), 3)]
    sources += [[1,1,1,1], [1,1,1,4], [2**100,2**100],
                [2**100,2**100+1], [1,2**200], [1,1,2**180]]
    for invalid in ([], [0], [-1], [F(1, 2)], [True], "1"):
        try:
            reduction(invalid)
        except ValueError:
            pass
        else:
            raise AssertionError(("invalid input accepted", invalid))
    results = [audit(source) for source in sources]
    tracked = ["facility_spe/shared/four_site_fptas_hardness.py", "tests/audits/four_site_fptas.py"]
    report = dict(schema_version=1, base_commit=subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        python_version=platform.python_version(), arithmetic="integer / Fraction; no floating point",
        seed=None, parameters="deterministic explicit sources below; all closed supports, all ten unordered layouts",
        replay_commands=["python3 tests/audits/four_site_fptas.py"],
        source_sha256={f: hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in tracked},
        source_instances=len(results), yes=sum(r["yes"] for r in results),
        no=sum(not r["yes"] for r in results),
        enumerated=sum(r["enumerated"] for r in results),
        accepted_support_cells=sum(r["accepted_support_cells"] for r in results),
        conditional_cost_comparisons=sum(r["conditional_cost_comparisons"] for r in results),
        results=results, limitations="Finite enumeration is not the universal proof. Closed supports can overlap and include endpoints; counts are not distinct equilibria. All layouts are enumerated without invoking canonical NE solvers. Original linked audit package was not available; original reported counts are not adopted.")
    if args.output:
        if args.output.exists():
            raise FileExistsError("frozen evidence must not be overwritten")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({k: report[k] for k in ["source_instances","yes","no","enumerated", "accepted_support_cells", "conditional_cost_comparisons"]}))


if __name__ == "__main__":
    main()
