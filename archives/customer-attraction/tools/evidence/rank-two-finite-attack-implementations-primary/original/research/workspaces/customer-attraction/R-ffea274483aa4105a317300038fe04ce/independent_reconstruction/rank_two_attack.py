"""Exact finite attacks on candidate floors for incidence rank at most two."""
from itertools import combinations
import json
from pathlib import Path
import random
import sys
import time

from customer_attraction import CustomerType, Instance, ExactSPESolver


def main():
    rng = random.Random(1809409)
    checked = 0
    failures = {}
    started = time.time()
    for k, m, samples in [(3, 3, 500), (4, 3, 500), (4, 4, 500), (5, 4, 300),
                           (5, 5, 200), (6, 5, 150), (7, 5, 100)]:
        signatures = [frozenset(a) for r in (1, 2) for a in combinations(range(k), r)]
        for sample in range(samples):
            customers = tuple(CustomerType(signature, rng.randint(1, 15))
                              for signature in signatures if rng.random() < 0.45)
            instance = Instance(tuple(map(str, range(k))), customers, m)
            solver = ExactSPESolver(instance)
            outcomes = solver.outcomes()
            theta = min(solver.threshold(q) for q in solver._outcomes if sum(q) == m - 1)
            for terminal in sorted(outcomes):
                checked += 1
                values = instance.topic_payoffs(terminal)
                individual_ok = all(values[a] >= theta for a in range(k) if terminal[a])
                aggregate_ok = instance.welfare(terminal) >= m * theta
                for label, okay in [('individual', individual_ok), ('aggregate', aggregate_ok)]:
                    if not okay and label not in failures:
                        failures[label] = {
                            'instance': instance.to_dict(),
                            'terminal': terminal,
                            'utilities': list(map(str, values)),
                            'theta': str(theta),
                            'path': next(solver.ordered_outcomes(terminal)),
                            'opt': instance.optimal_welfare(),
                            'welfare': instance.welfare(terminal),
                        }
                        print(label, json.dumps(failures[label]), flush=True)
                if len(failures) == 2:
                    report = {'checked': checked, 'failures': failures}
                    Path(sys.argv[1]).write_text(json.dumps(report, indent=2) + '\n')
                    return
        print(k, m, samples, checked, round(time.time()-started, 3), flush=True)
    Path(sys.argv[1]).write_text(json.dumps({'checked': checked, 'failures': failures}, indent=2) + '\n')


if __name__ == '__main__':
    main()
