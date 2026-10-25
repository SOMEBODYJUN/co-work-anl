"""Exact full-SPE attack on the binary-tail residual-only joint payment.

Uses the standard five-big/four-private lower-bound game, independently checks
every ordered-history IC, and reconstructs all 13 binary-certificate row types.
No author/audit implementation or SPE solver imported.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
REPO = next(p for p in HERE.parents if (p / 'AGENTS.md').is_file())
CERT = REPO / 'research/workspaces/customer-attraction/R-febfdd131cde4128882ca0edd4d712ba/parent/binary_tail_exact_1999.json'
weights = {k: F(v) for k, v in json.loads(CERT.read_text())['multipliers'].items()}


def div(n, d):
    return F(n, d) if n else F(0)


def payoff(topic, path):
    return div(5 if topic == 0 else 1, path.count(topic))


def rows(p, seven, e):
    a, b, c, d, q, r, s = seven
    bits = dict(zip('abcdqrs', seven))
    paths = {'actual': (a, b, c, d), 'off': (d, q, r, s)}
    out = {}
    for name, path in paths.items():
        pay = lambda i: div(path[i], p + sum(path))
        for i in range(0 if name == 'actual' else 1, 4):
            for label, bit in bits.items():
                out[f'{name}:{i}:K:{label}'] = pay(i) - div(bit, p + sum(path[:i]) + 4 - i)
        out[f'{name}:3:sum-opt'] = 4 * pay(3) - div(e, p + sum(path[:3]) + 1)
        bg = p + sum(path[:2])
        H = pay(2) + pay(3) + div(path[2], (bg + 1) * (bg + 2))
        out[f'{name}:pair-opt'] = 6 * H - div(e * (4 - e), bg + 1) - div(e * (e - 1), bg + 2)
    out['root-copy-d'] = div(a, p + a + b + c + d) - div(d, p + d + q + r + s)
    return {key: out[key] for key in weights}


def rho(p, head, aux, e):
    g = sum(weights[key] * value for key, value in rows(p, head + aux, e).items())
    return (F(1999, 1000) if p == 0 else F(5, 3)) * div(sum(head), p + sum(head)) - div(e, p + e) - g


def main():
    # Complete strategy: choose B (topic 0) at every ordered history.
    ic = strict = tied = histories = 0
    for depth in range(5):
        for history in product(range(5), repeat=depth):
            histories += 1
            chosen_value = payoff(0, history + (0,) * (5 - depth))
            for alternative in range(1, 5):
                value = payoff(alternative, history + (alternative,) + (0,) * (4 - depth))
                assert chosen_value >= value
                ic += 1
                strict += chosen_value > value
                tied += chosen_value == value
    assert histories == 781 and ic == 3124
    # Unit customers 0..4 like B only; customer 4+j likes private topic j.
    likes = ((0,),) * 5 + tuple((j,) for j in range(1, 5))
    branches = []
    total_R = total_B = total_r = total_G = F(0)
    for i in range(5):
        path = (i,) + (0,) * 4
        z = payoff(i, path)
        welfare = sum(any(a in liked for a in path) for liked in likes)
        V = welfare - z
        Bi = Ri = ri = Gi = F(0)
        global_rows = {key: F(0) for key in weights}
        for liked in likes:
            p = int(i in liked)
            head = tuple(int(a in liked) for a in path[1:])
            # Copy-D is the same action B, so its true continuation is B^3.
            aux = head[1:]
            e = sum(j in liked for j in range(5) if j != i)
            raw_r = rho(p, head, aux, e)
            min_r = min(rho(p, head, tail, e) for tail in product((0, 1), repeat=3))
            assert raw_r == min_r  # No loss from auxiliary minimization in this game.
            assert raw_r >= 0
            ri += raw_r
            Ri += div(e, p + e)
            Bi += (F(1999, 1000) if p == 0 else F(5, 3)) * div(sum(head), p + sum(head))
            for key, value in rows(p, head + aux, e).items():
                global_rows[key] += value
        assert all(value >= 0 for value in global_rows.values())
        Gi = sum(weights[key] * value for key, value in global_rows.items())
        assert Bi - Ri == Gi + ri
        branches.append({'root': i, 'W': welfare, 'z': str(z), 'V': str(V),
                         'B': str(Bi), 'R_complement': str(Ri),
                         'rho_equals_min_rho': str(ri), 'G': str(Gi),
                         'weighted_global_rows': {key: str(weights[key] * value) for key, value in global_rows.items()}})
        total_B += Bi
        total_R += Ri
        total_r += ri
        total_G += Gi
    assert total_R == 4 * 9
    assert total_B == F(6997, 150)
    assert total_r == F(13237604659, 2107435500)
    defect = total_B - total_r - 8 * 5
    assert defect == F(769816631, 2107435500) > 0
    actual_G = F(branches[0]['G'])
    assert defect > actual_G
    out = {'status': 'PASS residual-only payment counterexample; not HALF counterexample',
           'source': 'standard big-theme lower-bound family, m=5; full strategy here independently reconstructed',
           'histories': histories, 'IC_comparisons': ic, 'strict': strict, 'tied': tied,
           'W': 5, 'OPT_5': 9, 'u1': '1', 'J': 9,
           'sum_B': str(total_B), 'sum_R': str(total_R), 'sum_r_min': str(total_r),
           'sum_G': str(total_G), 'residual_payment_defect': str(defect),
           'actual_matched_G': str(actual_G),
           'defect_after_also_subtracting_actual_matched_G': str(defect - actual_G),
           'branch_detail': branches}
    HERE.joinpath('residual_payment_audit.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({k: v for k, v in out.items() if k != 'branch_detail'}, indent=2))


if __name__ == '__main__':
    main()
