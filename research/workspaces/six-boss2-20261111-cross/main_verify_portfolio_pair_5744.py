"""Main's literal-index, shared-hidden-state audit of the 17-query PAIR pack.
No discovering-agent module or row builder is imported. All math is Fraction.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
from collections import defaultdict
import hashlib, json, time

B = Path(__file__).resolve().parent
pp = B / 'master_cuts/dynamic_5744_exact.json'
cp = B / 'joint_requery/portfolio_selected_5744.json'
point, pack = json.loads(pp.read_text()), json.loads(cp.read_text())
assert pack['source_sha256'] == hashlib.sha256(pp.read_bytes()).hexdigest()
cols = point['columns']
words8 = list(product((0, 1), repeat=3))
blocks = []
for i, col in enumerate(cols):
    if col['kind'] == 'hist':
        blocks.append([i, col, []])
    elif col['kind'] == 'joint-reply':
        blocks[-1][2].append((i, col))

def pay(n, d):
    return F(n, d) if n else F(0)

def audit(rec):
    source, k, member = rec['i'], rec['k'], rec['member']
    assert k == 6 - source and k >= 3
    orb = tuple(rec['orb'])
    ct = 6 if orb[1] else 30
    weights = {name: F(value) for name, value in rec['weights'].items()}
    assert min(weights.values()) >= 0
    source_cost = weights.get('sourceT', F(0)) + weights.get('sourceC', F(0))
    price_cost = sum((w * (k - 3 if n.split(':')[1] in ('s', 'ss') else 1)
                      for n, w in weights.items() if n.startswith('price:')), F(0))
    cap_cost = sum((w * (k - 3 if n.split(':')[1] in ('s', 'ss') else 1)
                    for n, w in weights.items() if n.startswith('cap:')), F(0))
    assert source_cost == 1 == F(rec['source_weight_sum'])
    assert price_cost == F(rec['u6_coefficient']) and cap_cost == F(rec['K_coefficient'])

    @lru_cache(None)
    def phi(p, ell, t, qs):
        ans = None
        for b, c, j, v in product((0, 1), repeat=4):
            for s in range(k - 2):
                for ss in range(k - 2):
                    u = dict(t=F(t), b=F(b), c=F(c), j=F(j), v=F(v), s=F(s), ss=F(ss))
                    u.update({f'q{i}': q for i, q in enumerate(qs)})
                    beta1, beta2 = p + t + s, p + c + ss
                    z1, z2 = beta1 + b + c, beta2 + j + v
                    own1, own2 = pay(c, z1), pay(v, z2)
                    value = F(0)
                    for name, weight in weights.items():
                        if name == 'sourceT':
                            e = pay(t, z1)
                        elif name == 'sourceC':
                            e = pay(c, z2)
                        else:
                            kind, label = name.split(':', 1)
                            if kind == 'price': e = u[label] / (ell + 1)
                            elif kind == 'cap': e = u[label]
                            elif kind == 'last1': e = u[label] / (beta1 + b + 1) - own1
                            elif kind == 'last2': e = u[label] / (beta2 + j + 1) - own2
                            elif kind == 'safeB': e = u[label] / (beta1 + 2) - pay(b, z1)
                            elif kind == 'safeJ': e = u[label] / (beta2 + 2) - pay(j, z2)
                            elif kind in ('pair1', 'pair2'):
                                a, d = label.split(',')
                                # An averaged query compared with itself means average of q_l^2.
                                # Distinct averaged query pairs are not features of this pack.
                                assert a == d or not (a.startswith('q') and d.startswith('q'))
                                overlap = u[a] if a == d else u[a] * u[d]
                                beta, first, last, z = (beta1, b, c, z1) if kind == 'pair1' else (beta2, j, v, z2)
                                e = (u[a] + u[d]) / (beta + 1) - (overlap + first) / ((beta + 1) * (beta + 2)) - pay(first + last, z)
                            else: raise AssertionError(name)
                        value += weight * e
                    ans = value if ans is None else min(ans, value)
        return ans

    row = [F(0)] * len(cols)
    row[0] = cap_cost
    for hi, h, js in blocks:
        aa = tuple(map(int, h['actual_bits']))
        words = tuple(w for w, n in zip(words8, h['hist']) for _ in range(n))
        assert len(words) == 6
        pairs = [(i, j) for i in range(6) for j in range(6) if (i == j) == bool(orb[1])]
        assert len(pairs) == ct
        base, increments = F(0), defaultdict(F)
        for i, j in pairs:
            others = [l for l in range(6) if l not in {i, j}]
            means = tuple(F(sum(words[l][a] for l in others), len(others)) for a in range(3))
            vals = {}
            for st in product((0, 1), repeat=2):
                qs = tuple(map(F, aa + words[i] + words[j] + st)) + means
                assert len(qs) == 17
                vals[st] = phi(sum(aa[:source]), sum(aa[:5]), st[member], qs)
            z = vals[0, 0]
            base += z / ct
            for st in [(0, 1), (1, 0), (1, 1)]:
                increments[words[i], words[j], st] += (vals[st] - z) / ct
        row[hi] = pay(aa[source], sum(aa)) + price_cost * pay(aa[5], sum(aa)) - base
        for ci, col in js:
            family, diag, wi, wj = col['group']
            if (family, diag) == orb:
                row[ci] = -increments[tuple(wi), tuple(wj), tuple(col['state'])]
    saved = [F(0)] * len(cols)
    for j, v in rec['sparse_row']:
        saved[j] = F(v)
    assert row == saved, [(j, str(a), str(b)) for j, (a, b) in enumerate(zip(row, saved)) if a != b][:5]
    slack = sum((v * F(col['weight']) for v, col in zip(row, cols)), F(0))
    assert slack == F(rec['exact_slack']) < 0
    return {'source': source + 1, 'k': k, 'member': member, 'orb': list(orb),
            'full_4849_coefficients_equal': True, 'exact_slack': str(slack), 'visible_states': phi.cache_info().currsize}

start = time.time()
report = {'status': 'PASS', 'scope': 'Independent exact shared 17-query, two-branch PAIR reconstruction; not an SPE or proof of strict inclusion over all single-query cuts',
          'point_sha256': pack['source_sha256'], 'pack_sha256': hashlib.sha256(cp.read_bytes()).hexdigest(),
          'rows': [audit(r) for r in pack['cuts']], 'seconds': time.time() - start}
Path(__file__).with_suffix('.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(report, ensure_ascii=False, indent=2))
