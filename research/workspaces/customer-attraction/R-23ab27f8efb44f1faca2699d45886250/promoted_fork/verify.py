"""Exact promoted-terminal fork; no optimizer and no welfare search.

The theorem is the nonnegative decomposition in proof.md. This file checks
its implementation, replays real complete strategies, and evaluates two
previously frozen necessary-system points. It never overwrites evidence.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import sys

ROOT = next(p for p in Path(__file__).resolve().parents
            if (p / 'customer_attraction/model.py').is_file())
sys.path.insert(0, str(ROOT))
from customer_attraction.model import Instance, CustomerType
from customer_attraction.exact import ExactSPESolver

W = (F(1), F(1, 50), F(49, 800), F(1, 50), F(3, 160))


def share(a, z):
    return F(a, z) if a else F()


def local(p, t, q, s, b, c, v, pi, rho):
    """Weighted costs; the five true IC slacks are bound minus cost."""
    e = p + t + s
    z1, z2 = e + b + c, e + c + v
    costs = (share(t, z1), share(c, z2) - share(b, z1),
             F(q, e + b + 1) - share(c, z1),
             F(q, e + c + 1) - share(v, z2),
             F(v, e + b + 1) - share(c, z1))
    fee = b * (F(24, 125) * rho + F(1, 500))
    fee += c * (F(3, 50) * pi + F(24, 125) * rho)
    fee += v * (F(1, 800) * pi + F(1, 250) * rho)
    fee += F(49, 1600) * s
    return sum((w * z for w, z in zip(W, costs)), F()) + fee


def minimum(k, p, t, q, pi, rho):
    assert k >= 3 and p >= 0
    return min(local(p, t, q, s, b, c, v, pi, rho)
               for s, b, c, v in product(range(k - 2), range(2), range(2), range(2)))


def primitive_cost(p, t, q, middle, b, c, v, pi, rho):
    """Independent literal-theme calculation, retaining every middle bit."""
    first = [t, *middle, b, c]
    second = [t, *middle, c, v]
    z1, z2 = p + sum(first), p + sum(second)
    costs = [share(first[0], z1),
             share(second[-2], z2) - share(first[-2], z1),
             F(q, p + sum(first[:-1]) + 1) - share(first[-1], z1),
             F(q, p + sum(second[:-1]) + 1) - share(second[-1], z2),
             F(second[-1], p + sum(first[:-1]) + 1) - share(first[-1], z1)]
    value = sum((w * cost for w, cost in zip(W, costs)), F())
    value += F(24, 125) * rho * b + F(1, 500) * b
    value += F(3, 50) * pi * c + F(24, 125) * rho * c
    value += F(1, 800) * pi * v + F(1, 250) * rho * v
    value += sum((F(49, 1600) * bit for bit in middle), F())
    return value


def audit_coefficients():
    cases = 0
    for k in range(3, 9):
        for p, pi, rho, t, q in product(range(3), (F(1, 2), F(2, 7)),
                                      (F(1, 3), F(3, 8)), range(2), range(2)):
            literal = []
            for hidden in product(range(2), repeat=k):
                middle, b, c, v = hidden[:-3], *hidden[-3:]
                h = primitive_cost(p, t, q, middle, b, c, v, pi, rho)
                assert h == local(p, t, q, sum(middle), b, c, v, pi, rho)
                literal.append(h)
                cases += 1
            assert min(literal) == minimum(k, p, t, q, pi, rho)
    return {'literal_coefficient_states': cases,
            'horizons_checked': list(range(3, 9)),
            'scope': 'implementation check; arbitrary k follows from the proof'}


def terminal(actions, history, m):
    path = tuple(history)
    while len(path) < m:
        path += (actions[path],)
    return path


def audit_strategies():
    records = []
    for m in (3, 4, 6):
        ins = Instance(('A', 'B', 'C'), (
            CustomerType(frozenset({0}), 3), CustomerType(frozenset({1}), 2),
            CustomerType(frozenset({2}), 4), CustomerType(frozenset({0, 1}), 5),
            CustomerType(frozenset({0, 2}), 2), CustomerType(frozenset({1, 2}), 1)), m)
        solver = ExactSPESolver(ins)
        cert = solver.certificate()
        actions = cert.actions
        actual = terminal(actions, (), m)
        us = ins.player_payoffs(actual)
        K = max(sum(ct.multiplicity for ct in ins.customers if j in ct.topics)
                for j in range(3))
        # Two actual-node safe prices; valid for the entire common catalog.
        def prices(ct):
            return F(1, m), F(1, int(actual[0] in ct.topics) + m - 1)
        U, V = us[:2]
        all_ic = rows = 0
        for h in sorted(actions):
            prescribed = terminal(actions, h, m)
            i, k = len(h), m - len(h)
            for target in range(3):
                forced = terminal(actions, h + (target,), m)
                assert ins.player_payoffs(prescribed)[i] >= ins.player_payoffs(forced)[i]
                all_ic += 1
            if k < 3:
                continue
            r = ins.player_payoffs(prescribed)[i]
            for target, query in product(range(3), repeat=2):
                first = terminal(actions, h + (target,), m)
                middle, B, C = first[i + 1:-2], first[-2], first[-1]
                second = terminal(actions, first[:-2] + (C,), m)
                Vtopic = second[-1]
                rhs = raw = F()
                for ct in ins.customers:
                    p = sum(a in ct.topics for a in h)
                    t, q = int(target in ct.topics), int(query in ct.topics)
                    b, c, v = (int(a in ct.topics) for a in (B, C, Vtopic))
                    s = sum(a in ct.topics for a in middle)
                    pi, rho = prices(ct)
                    rhs += ct.multiplicity * minimum(k, p, t, q, pi, rho)
                    raw += ct.multiplicity * local(p, t, q, s, b, c, v, pi, rho)
                lhs = r + F(49, 800) * U + F(97, 250) * V
                lhs += (F(1, 500) + F(49, 1600) * (k - 3)) * K
                assert lhs >= raw >= rhs
                rows += 1
        records.append({'m': m, 'ordered_decision_histories': len(actions),
                        'all_history_IC_checked_including_self': all_ic,
                        'real_fork_rows_checked': rows})
    return records


OLD = 'research/workspaces/customer-attraction/R-964def22ed03479582e83410444f2ea2/parent/combined_702.json'
LATEST = 'research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/six_astra/attractive_nested_exact.json'


def audit_point(relative):
    path = ROOT / relative
    data = json.loads(path.read_text())
    if 'support' in data:
        support = [(tuple(map(int, x['actual_bits'])), F(x['weight'])) for x in data['support']]
        K = F(data['K'])
    else:
        support = [(tuple(map(int, x['actual_bits'])), F(x['weight']))
                   for x in data['columns'] if x['kind'] == 'hist']
        K = next(F(x['weight']) for x in data['columns'] if x['kind'] == 'K')
    u = [sum((w * share(a[j], sum(a)) for a, w in support), F()) for j in range(6)]
    rhs = sum((w * minimum(5, a[0], a[4], a[5], F(1, a[0] + 5),
                          F(1, a[0] + a[1] + 4)) for a, w in support), F())
    lhs = F(849, 800) * u[1] + F(97, 250) * u[2] + F(253, 4000) * K
    return {'path': relative, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'slack': str(lhs - rhs), 'strictly_separated': lhs < rhs,
            'scope': 'evaluation of this one exact necessary row; no SPE claim'}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    report = {'claim': 'R23-PROMOTED-TERMINAL-FORK-v1',
              'coefficients': audit_coefficients(), 'strategies': audit_strategies(),
              'point_evaluations': [audit_point(OLD), audit_point(LATEST)],
              'main_half_status': 'OPEN; no new six-player welfare bound'}
    assert report['point_evaluations'][0]['strictly_separated']
    assert not report['point_evaluations'][1]['strictly_separated']
    text = json.dumps(report, indent=2) + '\n'
    if args.output:
        with args.output.open('x') as stream:
            stream.write(text)
    print(text, end='')


if __name__ == '__main__':
    main()
