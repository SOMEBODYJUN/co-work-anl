"""Independent ordered-bit reconstruction of source3 middle-SAFE cut.

Only frozen data is read. No discovery code or old coefficient generator is
imported. Integer primitive formulas are rebuilt from the stated IC weights.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p/'work.py').exists())
POINT = ROOT/'research/workspaces/customer-attraction/R-a241704002304c95bca9ef95d516b61f/solo_six/source_requery_exact.json'
CUT = HERE.parent/'attack/source_middle/cut_source3_B-off.json'


def share(n, d):
    return F(n, d) if n else F()


def value(a, t, ti, ci, bj, tail):
    p, q, z = tail
    b, ell = sum(a[:2]), sum(a[:5])
    d = b+t+p+q+z
    # 285 source IC; capacities 5P+Q; actual terminal price 15P;
    # actual third-player SAFE prices 96Q+120Z; middle Q SAFE query Ci
    # weight 15; terminal Z queries Ti,Ci,Bj each of weight 10.
    source = 285*share(t, d)
    capacity = 5*p+q
    prices = 15*F(p, ell+1)+F(96*q+120*z, b+4)
    middle = -15*share(q, d)+15*F(ci, b+t+p+2)
    terminal = -30*share(z, d)+10*F(ti+ci+bj, b+t+p+q+1)
    primitive = source+capacity+prices+middle+terminal
    compressed = (share(285*t-15*q-30*z, d)+5*p+q
                  +15*F(p, ell+1)+F(96*q+120*z, b+4)
                  +15*F(ci, b+t+p+2)
                  +10*F(ti+ci+bj, b+t+p+q+1))
    assert primitive == compressed
    return primitive


def phi(a, t, ti, ci, bj):
    return min(value(a, t, ti, ci, bj, tail)
               for tail in product((0, 1), repeat=3))


def main():
    local_checks = 0
    for a in product((0, 1), repeat=6):
        for t, ti, ci, bj in product((0, 1), repeat=4):
            for tail in product((0, 1), repeat=3):
                value(a, t, ti, ci, bj, tail)
                local_checks += 1
    data = json.loads(POINT.read_text())
    u = [F() for _ in range(6)]
    rhs = F()
    terms = 0
    for atom in data['atoms']:
        hi = atom['hist_index']
        hist = data['histograms'][hi]
        a = tuple(map(int, hist['actual_bits']))
        mass = F(atom['weight'])
        for i in range(6):
            u[i] += mass*share(a[i], sum(a))
        words = [w for w, n in zip(product((0, 1), repeat=3), hist['hist'])
                 for _ in range(n)]
        assert len(words) == 6
        group = {(g[0], g[1], tuple(g[2]), tuple(g[3])): index
                 for index, g in enumerate(data['groups'][hi])}
        for i, j in product(range(6), repeat=2):
            if i == j:
                continue
            r = atom['R'][group[0, 0, words[i], words[j]]]
            rhs += mass*phi(a, r, words[i][0], words[i][2], words[j][1])
            terms += 1
    lhs = 30*(501*u[2]+15*u[5]+6*F(data['K']))
    slack = lhs-rhs
    claimed = json.loads(CUT.read_text())['with_middle']
    assert lhs/285 == F(claimed['lhs'])
    assert rhs/285 == F(claimed['rhs'])
    assert slack/285 == F(claimed['slack']) < 0
    assert F(501) == 285+96+120 and F(6) == 5+1
    report = {
        'status': 'PASS',
        'scope': 'general row formula and exact separation of one necessary point; not six-player half or a SPE counterexample',
        'point_sha256': hashlib.sha256(POINT.read_bytes()).hexdigest(),
        'cut_sha256': hashlib.sha256(CUT.read_bytes()).hexdigest(),
        'all_local_primitive_expansions': local_checks,
        'literal_index_terms': terms,
        'ordered_hidden_states_per_term': 8,
        'integer_cost_per_pair': {'u3': 501, 'u6': 15, 'K': 6},
        'normalized_slack': str(slack/285),
        'normalized_slack_float': float(slack/285),
    }
    HERE.joinpath('source3_cut_audit.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
