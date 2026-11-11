"""Independent full-row audit of 616-feature cross-query PAIR cuts.
Reads the submitted weights as inputs; never imports its generator.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
import hashlib, json, time
from main_cross_query_features_v1 import pay, query_samples, literal_product, projection

B = Path(__file__).resolve().parent
pp = B / 'master_cuts/dynamic_5775_exact.json'
cp = B / 'joint_requery/cross_pairs_selected_5775_v1.json'
point, pack = json.loads(pp.read_text()), json.loads(cp.read_text())
assert pack['source_sha256'] == hashlib.sha256(pp.read_bytes()).hexdigest()
cols = point['columns']
blocks = []
for ci, c in enumerate(cols):
    if c['kind'] == 'hist': blocks.append((ci, c, []))
    elif c['kind'] == 'joint-reply': blocks[-1][2].append((ci, c))


def audit(rec):
    source, k, member, orb = rec['i'], rec['k'], rec['member'], tuple(rec['orb'])
    assert k == 6 - source and 3 <= k <= 6
    count = 6 if orb[1] else 30
    weights = {n: F(w) for n, w in rec['weights'].items()}
    assert all(w >= 0 for w in weights.values())
    assert weights.get('sourceT', 0) + weights.get('sourceC', 0) == F(rec['source_weight_sum']) == 1
    price = sum((w * (k-3 if n.split(':')[1] in ('s','ss') else 1) for n,w in weights.items() if n.startswith('price:')), F(0))
    cap = sum((w * (k-3 if n.split(':')[1] in ('s','ss') else 1) for n,w in weights.items() if n.startswith('cap:')), F(0))
    assert price == F(rec['u6_coefficient']) and cap == F(rec['K_coefficient'])
    cross_names = tuple(n for n in weights if n.startswith('oldpair'))
    assert cross_names
    phi = projection(weights, k)
    row = [F(0)] * len(cols)
    row[0] = cap
    visible_masses, visible_values = defaultdict(F), {}
    for hi, h, joint in blocks:
        a = tuple(map(int, h['actual_bits']))
        words = tuple(w for w,n in zip(product((0,1),repeat=3), h['hist']) for _ in range(n))
        assert len(words) == 6
        hm = F(h['weight'])
        joint_masses = {(tuple(c['group'][:2]), tuple(c['group'][2]), tuple(c['group'][3]), tuple(c['state'])): F(c['weight']) for _,c in joint}
        base, increments = F(0), defaultdict(F)
        for i in range(6):
            for j in range(6):
                if (i == j) != bool(orb[1]): continue
                values = {}
                masses = {st: joint_masses.get((orb,words[i],words[j],st),F(0)) for st in ((0,1),(1,0),(1,1))}
                masses[0,0] = hm - sum(masses.values(),F(0))
                assert min(masses.values()) >= 0
                for state in product((0,1),repeat=2):
                    samples, qs, moments = query_samples(a,words,i,j,state)
                    products = tuple((n,literal_product(samples,n)) for n in cross_names)
                    signature = (sum(a[:source]),sum(a[:5]),state[member],qs,moments)
                    value = phi(*signature[:4],products)
                    values[state] = value
                    visible_values[signature] = value
                    visible_masses[signature] += masses[state]/count
                base += values[0,0]/count
                for state in ((0,1),(1,0),(1,1)):
                    increments[words[i],words[j],state] += (values[state]-values[0,0])/count
        row[hi] = pay(a[source],sum(a)) + price*pay(a[5],sum(a)) - base
        for ci,c in joint:
            family,diag,wi,wj = c['group']
            if (family,diag) == orb:
                row[ci] = -increments[tuple(wi),tuple(wj),tuple(c['state'])]
    saved = [F(0)] * len(cols)
    for ci,v in rec['sparse_row']: saved[ci] = F(v)
    assert row == saved
    assert hashlib.sha256(json.dumps(list(map(str,row)),separators=(',',':')).encode()).hexdigest() == rec['row_sha256']
    slack = sum((v*F(c['weight']) for v,c in zip(row,cols)),F(0))
    assert slack == F(rec['exact_slack']) < 0
    supplied_visible = {}
    for v in rec['visible']:
        p,ell,t,qs,moments = v['state']
        sig = (p,ell,t,tuple(map(F,qs)),tuple(map(F,moments)))
        assert sig not in supplied_visible
        supplied_visible[sig] = F(v['mass'])
        assert visible_values[sig] == F(v['minimum'])
    assert {v:m for v,m in visible_masses.items() if m} == supplied_visible
    return {'source':source+1,'k':k,'member':member,'orb':list(orb),'full_4849_coefficients_equal':True,
            'literal_query_couplings':True,'visible_states':len(supplied_visible),'exact_slack':str(slack),
            'row_sha256':rec['row_sha256']}


if __name__ == '__main__':
    start = time.time()
    assert len(pack['cuts']) == pack['cut_count'] == 8
    report = {'status':'PASS','scope':'Full 4849-column exact rederivation from legal query-pair index distributions, shared hidden states and true source budgets; no SPE is asserted',
              'point_sha256':pack['source_sha256'],'pack_sha256':hashlib.sha256(cp.read_bytes()).hexdigest(),
              'rows':[audit(rec) for rec in pack['cuts']],'seconds':time.time()-start}
    Path(__file__).with_suffix('.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
