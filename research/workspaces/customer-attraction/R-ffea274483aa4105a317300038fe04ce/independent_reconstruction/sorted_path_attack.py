"""Finite exact attack of terminal-payoff sorting, not a universal proof."""
from functools import lru_cache
from itertools import combinations
import json
from pathlib import Path
import random
import sys

from customer_attraction import CustomerType, Instance, ExactSPESolver


def has_sorted_path(solver, terminal):
    values = solver.instance.topic_payoffs(terminal)
    @lru_cache(None)
    def visit(prefix):
        if prefix == terminal:
            return True
        candidates = [a for a in range(len(prefix)) if prefix[a] < terminal[a]]
        maximum = max(values[a] for a in candidates)
        for action in candidates:
            if values[action] != maximum:
                continue
            child = tuple(x + (a == action) for a, x in enumerate(prefix))
            if (terminal in solver.outcomes(child)
                    and values[action] >= solver.threshold(prefix)
                    and visit(child)):
                return True
        return False
    return visit((0,) * len(terminal))


def has_minimum_last_path(solver, terminal):
    values = solver.instance.topic_payoffs(terminal)
    minimum = min(values[a] for a in range(len(terminal)) if terminal[a])
    @lru_cache(None)
    def visit(prefix):
        remaining = [a for a in range(len(prefix)) if prefix[a] < terminal[a]]
        if not remaining:
            return True
        for action in remaining:
            if sum(prefix) == solver.instance.players - 1 and values[action] != minimum:
                continue
            child = tuple(x + (a == action) for a, x in enumerate(prefix))
            if (terminal in solver.outcomes(child)
                    and values[action] >= solver.threshold(prefix)
                    and visit(child)):
                return True
        return False
    return visit((0,) * len(terminal))


def main():
    rng = random.Random(1809409)
    checked = 0
    failures = {}
    for k, m, samples in [(3, 3, 300), (4, 3, 300), (4, 4, 400), (5, 4, 300), (5, 5, 200)]:
        signatures = [frozenset(a for a in range(k) if mask >> a & 1)
                      for mask in range(1, 1 << k)]
        for sample in range(samples):
            customers = tuple(CustomerType(signature, rng.randint(1, 8))
                              for signature in signatures if rng.random() < 0.33)
            instance = Instance(tuple(map(str, range(k))), customers, m)
            solver = ExactSPESolver(instance)
            for terminal in sorted(solver.outcomes()):
                checked += 1
                sorted_ok = has_sorted_path(solver, terminal)
                minimum_last_ok = has_minimum_last_path(solver, terminal)
                for label, okay in [('sorted', sorted_ok), ('minimum_last', minimum_last_ok)]:
                    if not okay and label not in failures:
                        paths = list(solver.ordered_outcomes(terminal))
                        failures[label] = {
                            'instance': instance.to_dict(),
                            'terminal': terminal,
                            'utilities': list(map(str, instance.topic_payoffs(terminal))),
                            'paths': paths,
                            'thresholds': {str(q): str(solver.threshold(q))
                                           for q in solver._outcomes if sum(q) < m},
                            'opt': instance.optimal_welfare(),
                            'welfare': instance.welfare(terminal),
                        }
                        print(label, json.dumps(failures[label]), flush=True)
                if len(failures) == 2:
                    report = {'checked': checked, 'failures': failures}
                    Path(sys.argv[1]).write_text(json.dumps(report, indent=2) + '\n')
                    return
    Path(sys.argv[1]).write_text(json.dumps({'checked': checked, 'failures': failures}, indent=2) + '\n')


if __name__ == '__main__':
    main()
