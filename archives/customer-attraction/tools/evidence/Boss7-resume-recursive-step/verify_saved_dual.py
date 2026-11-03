"""Verify the previously unverified recursive-step dual, without an LP.

This checks one saved 504-row cone program. The independent unit-customer
SPE proof/replay already exists elsewhere and is reused rather than rerun.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product, combinations_with_replacement
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent


def main():
    data = json.loads((HERE / 'original/recursive_step_attack.json').read_text())
    assert len(data) == 1
    saved = data[0]
    p, m = saved['topics'], saved['players']
    assert (p, m) == (6, 4)
    actions = {tuple(v['history']): v['action'] for v in saved['strategy']['actions']}
    required = {h for d in range(m) for h in product(range(p), repeat=d)}
    assert len(actions) == len(saved['strategy']['actions']) == 259
    assert set(actions) == required

    def closed(h):
        if len(h) < 3 or h.count(0) <= 1:
            return 0
        return 4 if h.count(0) == 2 and 5 in h else 5

    assert all(actions[h] == closed(h) for h in required)
    terminals = {}
    for d in range(m, -1, -1):
        for h in product(range(p), repeat=d):
            terminals[h] = (tuple(h.count(a) for a in range(p)) if d == m
                            else terminals[h + (actions[h],)])
    root = terminals[()]
    assert root == tuple(saved['strategy']['terminal_counts']) == (3, 0, 0, 0, 0, 1)

    @lru_cache(None)
    def payoff(counts, action):
        return tuple(F(1, sum(counts[a] for a in range(p) if mask & (1 << a)))
                     if mask & (1 << action) else F(0)
                     for mask in range(1, 1 << p))

    gamma = set()
    for h, action in actions.items():
        actual = payoff(terminals[h], action)
        for a in range(p):
            if a == action:
                continue
            row = tuple(x-y for x, y in zip(actual, payoff(terminals[h+(a,)], a)))
            if any(row):
                gamma.add(row)
    gamma = sorted(gamma)
    assert len(gamma) == saved['spe_rows'] == 310
    n = (1 << p) - 1

    def counts(h):
        return tuple(h.count(a) for a in range(p))

    def profit(b, c):
        out = []
        for mask in range(1, 1 << p):
            bc = sum(b[a] for a in range(p) if mask & (1 << a))
            cc = sum(c[a] for a in range(p) if mask & (1 << a))
            out.append(F(cc, bc+cc) if cc else F(0))
        return tuple(out)

    def floor(b, r, a):
        return tuple(F(1, sum(b[t] for t in range(p) if mask & (1 << t))+r)
                     if mask & (1 << a) else F(0) for mask in range(1, 1 << p))

    b = (0,) * p
    child = (1, 0, 0, 0, 0, 0)
    roots = [counts(h) for h in combinations_with_replacement(range(p), m)]
    children = [counts(h) for h in combinations_with_replacement(range(p), m-1)]
    assert (len(roots), len(children)) == (saved['root_portfolios'], saved['child_portfolios']) == (126, 56)
    O = profit(b, counts(tuple(saved['root_comparison_portfolio'])))
    u = payoff(root, actions[()])
    rows = [tuple(row)+(F(0),) for row in gamma]
    rows += [tuple(x-y for x, y in zip(O, profit(b, c)))+(F(0),) for c in roots]
    rows += [tuple(x-2*m*y for x, y in zip(O, floor(b, m, a)))+(F(-1),) for a in range(p)]
    rows += [tuple(x-2*v-y for x, v, y in zip(O, u, profit(child, c)))+(F(-1),) for c in children]
    rows += [tuple(x-2*v-2*(m-1)*y for x, v, y in zip(O, u, floor(child, m-1, a)))+(F(-1),) for a in range(p)]
    assert len(rows) == saved['row_count'] == 504
    w = tuple(F(bool(mask & ((1 << 0) | (1 << 5)))) for mask in range(1, 1 << p))
    eq = w+(F(0),)
    x = [F(0)] * n
    for customer in saved['instance']['customers']:
        mask = sum(1 << a for a in customer['topics'])
        x[mask-1] += customer['multiplicity']
    W = sum(a*v for a, v in zip(w, x))
    assert W == 48 and sum(x) == 69
    beta = F(saved['exact_dual_bound'])
    q = tuple(v/W for v in x)+(beta,)
    assert beta == F(saved['normalized_gap']) == F(1, 12)
    assert all(v >= 0 for v in q[:n])
    assert sum(a*v for a, v in zip(eq, q)) == 1
    slacks = [sum(a*v for a, v in zip(row, q)) for row in rows]
    assert all(v >= 0 for v in slacks)
    target = (F(0),)*n+(F(1),)
    residual = [beta*a-c for a, c in zip(eq, target)]
    seen = set()
    for index, text in saved['dual_nonzero_multipliers']:
        mu = F(text)
        assert 0 <= index < len(rows) and index not in seen and mu > 0
        seen.add(index)
        residual = [v-mu*a for v, a in zip(residual, rows[index])]
    assert all(v >= 0 for v in residual[:n]) and residual[-1] == 0
    output = {
        'status': 'passed', 'scope': 'one fixed full policy, root background zero, specified optimal tuple ABCD',
        'source_sha256': hashlib.sha256((HERE/'original/recursive_step_attack.json').read_bytes()).hexdigest(),
        'complete_action_entries_bound_to_closed_policy': len(actions),
        'unique_nonzero_Gamma_rows': len(gamma), 'all_constraints': len(rows),
        'root_portfolios': len(roots), 'child_portfolios': len(children),
        'saved_positive_multipliers_verified': len(seen),
        'nonnegative_customer_residuals': n, 'free_gap_coordinate_residual': str(residual[-1]),
        'normalized_primal_gap': str(beta), 'exact_dual_upper_bound': str(beta),
        'unit_customer_scale': int(W), 'unit_gap': str(beta*W),
        'minimum_normalized_constraint_slack': str(min(slacks)),
        'original_LP_runs': 0, 'original_verifier_runs': 0,
        'new_unit_customer_full_history_replay_runs': 0,
        'existing_unit_customer_proof_and_replay_reused': True,
        'other_policy_or_other_optimal_tuple_certified': False,
    }
    (HERE/'verification.json').write_text(json.dumps(output, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(output, ensure_ascii=False))


if __name__ == '__main__':
    main()
