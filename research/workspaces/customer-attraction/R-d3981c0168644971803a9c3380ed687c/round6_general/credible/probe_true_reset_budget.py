"""Discovery only: test an explicitly stated all-input credible-reset budget.

Claim under test: after removing the first actual player from any complete
SPE path, the sum of positive true smaller-game threshold deficits of the
remaining ordered path is at most that deleted player's original payoff.
No finite negative result certifies the claim.
"""
from fractions import Fraction
from itertools import islice
from pathlib import Path
import json
import random
import sys

ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT))
from customer_attraction.model import Instance, CustomerType
from customer_attraction.exact import ExactSPESolver


def evaluate(instance, path):
    n = instance.players-1
    smaller = Instance(instance.topics, instance.customers, n)
    solver = ExactSPESolver(smaller)
    target = path[1:]
    profits = smaller.player_payoffs(target)
    deficits = []
    floors = []
    for i in range(n):
        floor = solver.threshold(smaller.counts(target[:i]))
        floors.append(floor)
        deficits.append(max(Fraction(0), floor-profits[i]))
    deleted = instance.player_payoffs(path)[0]
    return deleted, deficits, floors, profits


def main():
    rng = random.Random(9318)
    best = Fraction(0)
    best_record = None
    tested = 0
    for sample in range(300):
        k, m = 4, 4
        types = tuple(CustomerType(frozenset(a for a in range(k) if mask >> a & 1), w)
                      for mask in range(1, 1 << k)
                      if (w := rng.randrange(7)))
        instance = Instance(tuple(map(str, range(k))), types, m)
        original = ExactSPESolver(instance)
        for path in islice(original.ordered_outcomes(), 40):
            deleted, deficits, floors, profits = evaluate(instance, path)
            tested += 1
            if deleted:
                ratio = sum(deficits)/deleted
                if ratio > best:
                    best = ratio
                    best_record = dict(sample=sample, instance=instance.to_dict(),
                        path=list(path), deleted=str(deleted), ratio=str(ratio),
                        deficits=list(map(str, deficits)), floors=list(map(str, floors)),
                        new_profits=list(map(str, profits)))
                if ratio > 1:
                    print(json.dumps(dict(status='COUNTEREXAMPLE', tested=tested,
                                          record=best_record), indent=2))
                    return
    print(json.dumps(dict(status='NO_COUNTEREXAMPLE_IN_SAMPLE', tested=tested,
                         best=best_record), indent=2))


if __name__ == '__main__':
    main()
