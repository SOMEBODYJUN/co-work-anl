"""Attack the general candidate 2*m*u_i >= OPT_m on fixed full SPE cones.

This is a finite candidate diagnostic, never a proof of the universal claim.
LP discovery is accepted only after exact rational feasibility checks. Existing
complete strategies are held fixed; customer multiplicities may vary.
Run from repository root. No credentials, network, or repository writes occur.
"""
from __future__ import annotations

from fractions import Fraction
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations
import json
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
spec = spec_from_file_location("cone_diagnostic", ROOT / "tests/audits/customer_attraction_strategy_lp.py")
cone_module = module_from_spec(spec)
sys.modules[spec.name] = cone_module
spec.loader.exec_module(cone_module)


def main():
    # Boundary checks: one mover, repeated sole topic, and the zero-client game.
    boundary = []
    for players in (1, 3):
        actions = {tuple(0 for _ in range(depth)): 0 for depth in range(players)}
        cone = cone_module.StrategyCone(1, players, actions)
        assert cone.verify((Fraction(0),))
        assert cone.verify((Fraction(1),))
        payoff = cone_module.payoff_row(1, cone.root, 0)[0]
        assert payoff == Fraction(1, players)
        assert 2 * players * payoff - 1 == 1
        boundary.append({"players": players, "zero_client_feasible": True,
                         "one_client_payoff": str(payoff), "direct_margin": "1"})
    reports = []
    failures = []
    for source in sorted((ROOT / "evidence/certificates/customer_attraction").glob("*.json")):
        obj = json.loads(source.read_text())
        if not isinstance(obj, dict):
            continue
        strategy = obj.get("strategy", obj)
        if not isinstance(strategy, dict) or not {"actions", "terminal_counts"} <= strategy.keys():
            continue
        topics = len(strategy["terminal_counts"])
        players = sum(strategy["terminal_counts"])
        if not (1 <= topics <= 6 and 1 <= players <= 5):
            continue
        actions = {tuple(row["history"]): row["action"] for row in strategy["actions"]}
        cone = cone_module.StrategyCone(topics, players, actions)
        supports = list(combinations(range(topics), min(players, topics)))
        best = None
        exact_count = 0
        for action in sorted(set(actions.values()) & {a for a, n in enumerate(cone.root) if n}):
            payoff = cone_module.payoff_row(topics, cone.root, action)
            for support in supports:
                coverage = cone_module.coverage_row(topics, support)
                objective = tuple(2 * players * p - v for p, v in zip(payoff, coverage))
                result = linprog(np.asarray(objective, dtype=float),
                                 A_ub=-cone.matrix, b_ub=np.zeros(len(cone.rows)),
                                 A_eq=np.ones((1, (1 << topics) - 1)), b_eq=[1],
                                 bounds=(0, None), method="highs")
                if not result.success:
                    raise RuntimeError(result.message)
                weights = tuple(Fraction(float(w)).limit_denominator(10**7) for w in result.x)
                if not cone.verify(weights) or sum(weights) != 1:
                    continue
                exact_count += 1
                margin = cone_module.dot(objective, weights)
                if best is None or margin < best:
                    best = margin
                if margin < 0:
                    clones = cone_module.integer_clones(weights)
                    cone_module.independently_verify(cone, clones)
                    instance = cone_module.instance_from_clones(topics, players, clones)
                    # Check actual distinct sets: duplicate labels are not a
                    # legitimate separate action in the exact common directory.
                    topic_sets = [frozenset(mask for mask, count in enumerate(clones, 1)
                                            if count and mask & (1 << a)) for a in range(topics)]
                    distinct = len(set(topic_sets)) == topics
                    failures.append({"source": str(source.relative_to(ROOT)),
                                     "action": action, "comparison_support": support,
                                     "margin_normalized": str(margin),
                                     "distinct_topics": distinct,
                                     "instance": instance.to_dict(),
                                     "strategy": strategy})
        reports.append({"source": str(source.relative_to(ROOT)), "topics": topics,
                        "players": players, "exact_feasible_vertices": exact_count,
                        "smallest_checked_margin": str(best) if best is not None else None})
    print(json.dumps({"claim": "DIRECT-INDIVIDUAL-COVERAGE-FLOOR-v0: 2*m*u_i >= OPT_m",
                      "scope": "selected fixed complete SPE cones only; no universal conclusion",
                      "boundary_checks": boundary,
                      "reports": reports, "exact_negative_witnesses": failures},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
