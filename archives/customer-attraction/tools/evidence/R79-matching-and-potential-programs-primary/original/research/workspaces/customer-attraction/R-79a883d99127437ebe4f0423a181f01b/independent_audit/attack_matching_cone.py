"""Propose exact matching-bridge counterexamples in one fixed full-strategy cone.

Floating LP only proposes customer multiplicities; an accepted witness must be
reconstructed rationally and independently verified against every ordered IC.
"""
from itertools import product, combinations, permutations
from fractions import Fraction
from pathlib import Path
import json
import sys
import numpy as np
from scipy.optimize import linprog

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parents[4]))
from customer_attraction.model import Instance, CustomerType
from customer_attraction.certificate import StrategyCertificate, verify_certificate
from attack_optimal_static_matching import inspect

K, M = 6, 3
MASKS = list(range(1, 1 << K))
TOPICS = range(K)


def action(h):
    if len(h) == 0:
        return 0
    if len(h) == 1:
        return 3 if h[0] < 3 else 0
    group = range(3) if h[1] < 3 else range(3, 6)
    return min(a for a in group if a not in h)


def terminal(h):
    while len(h) < M:
        h += (action(h),)
    return h


def payoff(h, i, mask):
    return (Fraction(1, sum(bool(mask & (1 << a)) for a in h))
            if mask & (1 << h[i]) else Fraction())


def cover(h, mask):
    return int(any(mask & (1 << a) for a in h))


def main():
    z = terminal(())
    gamma = []
    for depth in range(M):
        for h in product(TOPICS, repeat=depth):
            true = terminal(h)
            for a in TOPICS:
                alt = terminal(h + (a,))
                gamma.append([payoff(true, depth, mask)
                              - payoff(alt, depth, mask) for mask in MASKS])
    all_comps = list(combinations(TOPICS, M))
    cov_z = [cover(z, mask) for mask in MASKS]
    scores = []
    for comp in all_comps:
        aub = [[-float(x) for x in row] + [0.] for row in gamma]
        # All other size-m supports must weakly lose. This tests whether one
        # optimal support can fail the bridge. The final inspect() requires
        # every optimal multiset to fail before treating the proposal as a
        # counterexample to the existential candidate.
        for alt in all_comps:
            if alt != comp:
                aub.append([float(cover(alt, mask) - cover(comp, mask))
                            for mask in MASKS] + [0.])
        for assignment in permutations(comp):
            gap = []
            for mask in MASKS:
                static = sum(payoff(z[:i] + (assignment[i],) + z[i+1:], i, mask)
                             for i in range(M))
                gap.append(static - cov_z[MASKS.index(mask)])
            aub.append([-float(x) for x in gap] + [1.])
        result = linprog([0.] * len(MASKS) + [-1.], A_ub=aub,
                         b_ub=np.zeros(len(aub)),
                         A_eq=[[1.] * len(MASKS) + [0.]], b_eq=[1.],
                         bounds=[(0, None)] * (len(MASKS) + 1), method="highs")
        scores.append((comp, float(result.x[-1]) if result.success else None))
        if result.success and result.x[-1] > 1e-8:
            rational = [Fraction(float(v)).limit_denominator(1000000)
                        for v in result.x[:-1]]
            from math import lcm, gcd
            denominator = lcm(*(v.denominator for v in rational))
            values = [int(v * denominator) for v in rational]
            common = gcd(*values)
            values = [v // common for v in values]
            instance = Instance(tuple(map(str, TOPICS)),
                tuple(CustomerType(frozenset(a for a in TOPICS if mask & (1 << a)), v)
                      for mask, v in zip(MASKS, values) if v), M)
            actions = {h: action(h) for depth in range(M)
                       for h in product(TOPICS, repeat=depth)}
            certificate = StrategyCertificate(actions, instance.counts(z, terminal=True))
            verified = verify_certificate(instance, certificate)
            witness = inspect(instance)
            payload = {"fixed_strategy_verification": verified,
                       "chosen_optimal_support": comp,
                       "LP_proposed_margin": float(result.x[-1]),
                       "witness": witness}
            (BASE / "matching_cone_proposal.json").write_text(
                json.dumps(payload, indent=2) + "\n")
            print(json.dumps(payload, indent=2))
            return
    print(json.dumps({"candidate": "existence of OPT static matching <= W",
                      "cone": "six-topic paired-group complete strategy",
                      "result": "finite LP proposals only; no theorem", "scores": scores}))


if __name__ == "__main__":
    main()
