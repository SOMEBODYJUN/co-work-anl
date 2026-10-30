"""Exact primal/dual security boundary certificates; no SPE or floating LP oracle."""
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def value(customers, action, background):
    return sum((F(weight, 1 + sum(topic in signature for topic in background))
                for signature, weight in customers if action in signature), F(0))

def certify(topics, players, customers, primal, dual):
    if sum(primal.values()) != 1 or any(p < 0 for p in primal.values()):
        raise AssertionError("invalid primal distribution")
    if sum(dual.values()) != 1 or any(p < 0 for p in dual.values()):
        raise AssertionError("invalid dual distribution")
    backgrounds = tuple(combinations_with_replacement(range(topics), players - 1))
    matrix = {h: tuple(value(customers, a, h) for a in range(topics)) for h in backgrounds}
    secured = min(sum(p * matrix[h][a] for a, p in primal.items()) for h in backgrounds)
    upper = max(sum(p * matrix[h][a] for h, p in dual.items()) for a in range(topics))
    if secured != upper:
        raise AssertionError((secured, upper))
    return {"topics": topics, "players": players,
            "competitor_count_vectors": len(backgrounds), "exact_value": str(secured)}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    family = []
    for n in range(1, 7):
        customers = ((frozenset({0}), n),) + tuple((frozenset({a}), 1) for a in range(1, n))
        report = certify(n, n, customers, {0: F(1)}, {(0,) * (n - 1): F(1)})
        if F(report["exact_value"]) != 1:
            raise AssertionError("sharp family lost value one")
        optimum = sum(w for _, w in customers)
        if optimum != 2 * n - 1:
            raise AssertionError("incorrect family optimum")
        report["optimum"] = optimum
        family.append(report)
    source = ROOT / "examples/customer_attraction/aggregate_theta_failure.json"
    data = json.loads(source.read_text())
    customers = tuple((frozenset(c["topics"]), c["multiplicity"]) for c in data["customers"])
    same_group = tuple(combinations(range(3), 2)) + tuple(combinations(range(3, 6), 2))
    primal = {a: F(1, 6) for a in range(6)}
    dual = {h: F(1, 6) for h in same_group}
    compact = certify(6, 3, customers, primal, dual)
    if F(compact["exact_value"]) != 10:
        raise AssertionError("compact boundary value is not ten")
    classes = {}
    for h in combinations_with_replacement(range(6), 2):
        kind = "repeat" if h[0] == h[1] else "same_group" if (h[0] < 3) == (h[1] < 3) else "cross_group"
        mean = sum(value(customers, a, h) for a in range(6)) / 6
        classes.setdefault(kind, set()).add(mean)
    expected = {"repeat": {F(37, 3)}, "same_group": {F(10)}, "cross_group": {F(97, 9)}}
    if classes != expected:
        raise AssertionError((classes, expected))
    compact["mean_payoff_by_background_class"] = {k: str(next(iter(v))) for k, v in classes.items()}
    result = {"claim": "CA-OBLIVIOUS-MIXED-SECURITY-2N1", "sharp_family": family,
              "compact_36_customer_certificate": compact,
              "scope": "Exact security values of the seven listed inputs; no general SPE bridge."}
    if args.output:
        if args.output.exists():
            raise FileExistsError("refusing to overwrite an existing evidence report")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
