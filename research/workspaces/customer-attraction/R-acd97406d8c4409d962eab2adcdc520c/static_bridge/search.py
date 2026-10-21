"""Attack only the candidate min-SPE-welfare >= min-static-PNE-welfare.

Run from the repository root. Exact Fraction comparisons; the canonical SPE
oracle is finite and retains arbitrary history-dependent ties. This is not a
test of the general half-coverage theorem.
"""
import argparse
import json
import random
from fractions import Fraction
from itertools import product
from pathlib import Path

from customer_attraction import CustomerType, ExactSPESolver, Instance, verify_certificate


def compositions(n, k):
    if k == 1:
        yield (n,)
        return
    for first in range(n + 1):
        for tail in compositions(n - first, k - 1):
            yield (first,) + tail


def static_equilibria(instance):
    for counts in compositions(instance.players, instance.topic_count):
        current = instance.topic_payoffs(counts)
        ok = True
        for a, number in enumerate(counts):
            if not number:
                continue
            for b in range(instance.topic_count):
                changed = list(counts)
                changed[a] -= 1
                changed[b] += 1
                if instance.topic_payoff(b, changed) > current[a]:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            yield counts


def assess(instance):
    solver = ExactSPESolver(instance)
    eqs = list(static_equilibria(instance))
    assert eqs, "finite exact potential game must have a PNE"
    sw = solver.minimum_welfare()
    nw = min(instance.welfare(c) for c in eqs)
    if sw < nw:
        cert = solver.worst_certificate()
        report = verify_certificate(instance, cert)
        report.assert_valid()
        return {"instance": instance.to_dict(), "spe_welfare": sw,
                "minimum_pne_welfare": nw, "all_pne_counts": eqs,
                "optimum": instance.optimal_welfare(),
                "certificate": cert.to_dict()}
    return None


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, default=606)
    p.add_argument("--trials", type=int, default=600)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    rng = random.Random(args.seed)
    checked = 0
    boundaries = [Instance(("empty",), (), 1),
                  Instance(("empty",), (CustomerType(frozenset(), 2),), 3),
                  Instance.from_topic_sets([set(), {0}, {0}], 3)]
    for ins in boundaries:
        assert assess(ins) is None
        checked += 1
    found = None
    for _ in range(args.trials):
        k = rng.choice((3, 4, 5))
        n = rng.choice((2, 3, 4, 5))
        weights = {mask: rng.randrange(8) if rng.random() < .5 else 0
                   for mask in range(1, 1 << k)}
        ins = Instance(tuple(map(str, range(k))),
                       tuple(CustomerType(frozenset(a for a in range(k) if mask >> a & 1), w)
                             for mask, w in weights.items() if w), n)
        found = assess(ins)
        checked += 1
        if found:
            break
    result = {"candidate": "min SPE W >= min static PNE W", "seed": args.seed,
              "checked": checked, "trials_limit": args.trials,
              "status": "refuted" if found else "finite search only", "counterexample": found}
    with args.output.open("x") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(json.dumps({key: value for key, value in result.items() if key != "counterexample"}))


if __name__ == "__main__":
    main()
