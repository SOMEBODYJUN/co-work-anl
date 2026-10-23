"""Definition-level diagnosis of the all-y transport candidate, not HALF.

One fixed finite input only tests the precise universal strengthening in the
working note. Uses Fraction and every ordered history, no SPE solver.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

OUT = Path(__file__).resolve().parent


def run():
    groups = (tuple(range(3)), tuple(range(3, 6)))
    units = [frozenset((i, 3+j)) for i in range(3) for j in range(3) for _ in range(2)]
    units += [frozenset(g) for g in groups]

    def group(a):
        return groups[a >= 3]

    def action(h):
        if not h:
            return 0
        if len(h) == 1:
            return min(a for a in group(h[0]) if a != h[0])
        a, b = h
        # In both the same and the mixed group cases, completing the first
        # group's unused action is a genuine terminal best response.
        return min(c for c in group(a) if c not in h)

    def terminal(h):
        while len(h) < 3:
            h += (action(h),)
        return h

    def pay(a, h):
        return sum((F(1, sum(t in C for t in h)) for C in units if a in C), F())

    gaps = []
    for depth in range(3):
        for h in product(range(6), repeat=depth):
            prescribed = pay(action(h), terminal(h))
            for a in range(6):
                gap = prescribed - pay(a, terminal(h + (a,)))
                assert gap >= 0, (h, a, gap)
                gaps.append(gap)
    p = [F(1, 6)] * 6
    ell = []
    for C in units:
        rho = sum(p[a] for a in C)
        conditional = sum((p[a] * sum(t in C for t in terminal((a,))[1:]) for a in C), F())
        ell.append(conditional / rho)
    assert ell[-2:] == [F(2), F(2)]
    # y=1 on each decorative customer, zero on the 18 original customers.
    # Every legal topic covers exactly one y unit, so r max_A y(A)=3.
    toll = sum(ell[-2:])
    assert toll == 4 > 3
    path = terminal(())
    assert path == (0, 1, 2)
    assert [pay(a, path) for a in path] == [F(19, 3)] * 3
    return {
        'status': 'PASS',
        'diagnosed_claim': 'all-p, all-y conditional-tail support bound T <= r max_A y(A)',
        'customers': len(units),
        'players': 3,
        'topics': 6,
        'ordered_nodes': 43,
        'comparisons': len(gaps),
        'minimum_gap': str(min(gaps)),
        'actual_path': list(path),
        'root_payoff': str(pay(0, path)),
        'p': [str(x) for x in p],
        'decorative_conditional_tail_loads': [str(x) for x in ell[-2:]],
        'toll': str(toll),
        'r_max_topic_y': '3',
        'scope': 'Only diagnoses an all-y transport strengthening. EXTRA-ONE-LEADER and HALF remain open. No claim about an endogenous optimal dual pair.',
    }


if __name__ == '__main__':
    result = run()
    (OUT / 'conditional_transport_audit.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
