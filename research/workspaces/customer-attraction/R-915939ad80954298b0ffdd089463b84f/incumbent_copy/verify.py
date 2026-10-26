"""Exact counterexample to normalizing a worst credible continuation to copy stability.

Independent ordered-history outcome recursion expands distinct unit customers;
the repository count-set solver is used only for a cross-check/certificate.
No random search is needed to reproduce this fixed mathematical witness.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import json
from pathlib import Path

M, TOPICS = 6, 5
WEIGHTS = {1:6, 2:6, 4:4, 8:3, 9:6, 10:1, 17:4, 20:1, 21:1, 24:7, 28:6}
UNITS = tuple(frozenset(a for a in range(TOPICS) if mask >> a & 1)
              for mask, multiplicity in WEIGHTS.items() for _ in range(multiplicity))
Q = (1, 1, 1, 2, 1)
PATH = (0, 3, 3, 4, 1, 2)

@lru_cache(None)
def payoff(z, role):
    action = z[role]
    return sum((F(1, sum(a in likes for a in z))
                for likes in UNITS if action in likes), F(0))

def counts(z):
    return tuple(z.count(a) for a in range(TOPICS))

def finish(actions, history=()):
    while len(history) < M:
        history += (actions[history],)
    return history

nodes = 0
thresholds = {}
def ordered_spe_outcomes(history):
    """All SPE terminal ordered paths at this precise ordered history.

    Off-path histories choose their SPE continuations independently.  Therefore
    chosen endpoint z in child a is implementable iff its current utility is
    at least the largest, over alternative children, of their minimum current
    utility.  This is a set-valued recursion; it does not impose Markov ties.
    """
    global nodes
    nodes += 1
    if len(history) == M:
        return frozenset((history,))
    i = len(history)
    children = [ordered_spe_outcomes(history + (a,)) for a in range(TOPICS)]
    threshold = max(min(payoff(z, i) for z in child) for child in children)
    thresholds[history] = threshold
    return frozenset(z for child in children for z in child if payoff(z, i) >= threshold)

def main():
    global nodes
    parser = argparse.ArgumentParser()
    parser.add_argument('--output')
    args = parser.parse_args()
    all_root = ordered_spe_outcomes(())
    assert all_root == frozenset((PATH, (0, 3, 3, 4, 2, 1)))
    root_nodes = nodes
    nodes = 0
    all_tail = ordered_spe_outcomes((0,))
    assert {counts(z) for z in all_tail} == {Q}
    assert all(payoff(z, 0) == F(31, 3) for z in all_tail)
    tail_nodes = nodes
    static = PATH[:3] + (0,) + PATH[4:]
    assert payoff(PATH, 3) == F(20, 3)
    assert payoff(static, 3) == F(41, 6)
    assert payoff(static, 3) - payoff(PATH, 3) == F(1, 6)

    # This is only a cross-check and complete strategy generator.  The all-
    # ordered-history uniqueness result above did not import these packages.
    from customer_attraction.model import Instance, CustomerType
    from customer_attraction.exact import ExactSPESolver
    from customer_attraction.certificate import verify_certificate
    inst = Instance(tuple(map(str, range(TOPICS))),
                    tuple(CustomerType(frozenset(a for a in range(TOPICS) if mask >> a & 1), w)
                          for mask, w in WEIGHTS.items()), M)
    solver = ExactSPESolver(inst)
    assert solver.outcomes() == frozenset((Q,))
    assert solver.outcomes((1,0,0,0,0)) == frozenset((Q,))
    cert = solver.certificate(on_path=PATH)
    checked = verify_certificate(inst, cert)
    checked.assert_valid()
    assert finish(cert.actions) == PATH

    # Independently evaluate EVERY original ordered history and all alternative
    # continuations in the generated full strategy, on distinct unit customers.
    ic_count, history_count, min_slack = 0, 0, None
    for length in range(M):
        for h in product(range(TOPICS), repeat=length):
            prescribed = finish(cert.actions, h)
            history_count += 1
            for a in range(TOPICS):
                deviated = finish(cert.actions, h + (a,))
                slack = payoff(prescribed, length) - payoff(deviated, length)
                assert slack >= 0
                ic_count += 1
                min_slack = slack if min_slack is None else min(min_slack, slack)
    real = finish(cert.actions, PATH[:3] + (0,))
    assert payoff(real, 3) <= payoff(PATH, 3)
    welfare = sum(any(a in likes for a in PATH) for likes in UNITS)
    optimum = max(sum(any(a in likes for a in z) for likes in UNITS)
                  for z in product(range(TOPICS), repeat=M))
    assert welfare == optimum == 45
    result = {
        'status': 'exact_fixed_witness_passed',
        'scope': 'Auxiliary normalization obstruction; not a HALF counterexample',
        'players': M, 'topic_count': TOPICS, 'unit_customers': len(UNITS),
        'weights_by_mask': WEIGHTS, 'root_spe_ordered_paths': sorted(all_root),
        'root_and_fixed_T_spe_terminal_counts': [Q],
        'fixed_T_ordered_spe_paths': sorted(all_tail),
        'root_recursion_ordered_nodes_including_leaves': root_nodes,
        'fixed_T_recursion_ordered_nodes_including_leaves': tail_nodes,
        'min_incumbent_profit': str(payoff(PATH,0)),
        'on_path': PATH, 'on_path_payoffs': [str(payoff(PATH,i)) for i in range(M)],
        'static_deviation_path': static, 'static_payoff': str(payoff(static,3)),
        'static_gain': str(payoff(static,3)-payoff(PATH,3)),
        'true_deviation_path': real, 'true_payoff': str(payoff(real,3)),
        'true_gain': str(payoff(real,3)-payoff(PATH,3)),
        'canonical_certificate_histories': checked.checked_histories,
        'canonical_certificate_comparisons_excluding_self': checked.checked_deviations,
        'independent_unit_history_count': history_count,
        'independent_unit_IC_including_self': ic_count,
        'minimum_IC_slack': str(min_slack), 'W': welfare, 'OPT_6': optimum,
    }
    out = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        with Path(args.output).open('x') as f: f.write(out)
    print(out)

if __name__ == '__main__':
    main()
