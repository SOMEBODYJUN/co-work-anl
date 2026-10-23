"""Diagnose the explicit stronger candidate OPT_m(uncovered) <= actual W.

Run from the repository root.  This is a candidate attack, not a proof.
"""
import json
import random
from itertools import combinations

from customer_attraction import CustomerType, ExactSPESolver, Instance


def omitted_opt(instance, counts):
    omitted = tuple(c for c in instance.customers
                    if not any(counts[t] for t in c.topics))
    residual = Instance(instance.topics, omitted, instance.players)
    return residual.optimal_welfare()


def main():
    rng = random.Random(920231)
    checked = 0
    best = None
    for m, k, trials in ((3, 4, 1000), (4, 5, 1000), (5, 7, 300)):
        signatures = [frozenset(s) for size in range(1, k + 1)
                      for s in combinations(range(k), size)]
        for trial in range(trials):
            chosen = rng.sample(signatures, rng.randint(k, min(len(signatures), 3 * k)))
            customers = tuple(CustomerType(s, rng.randint(1, 12)) for s in chosen)
            instance = Instance(tuple(map(str, range(k))), customers, m)
            solver = ExactSPESolver(instance)
            for counts in solver.outcomes():
                checked += 1
                welfare = instance.welfare(counts)
                residual = omitted_opt(instance, counts)
                record = (residual / max(welfare, 1), residual, welfare, instance, counts)
                if best is None or record[:3] > best[:3]:
                    best = record
                if residual > welfare:
                    cert = solver.certificate(counts)
                    print(json.dumps({"status": "counterexample", "checked": checked,
                                      "instance": instance.to_dict(), "counts": counts,
                                      "welfare": welfare, "residual_opt": residual,
                                      "certificate": cert.to_dict()}, indent=2))
                    return
    print(json.dumps({"status": "no_counterexample", "checked": checked,
                      "best_residual": best[1], "best_welfare": best[2],
                      "best_instance": best[3].to_dict(), "best_counts": best[4]}, indent=2))


if __name__ == "__main__":
    main()
