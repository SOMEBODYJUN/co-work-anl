"""Main exact audit of the 332-to-616 strict inclusion witness and its credit.

Rebuilds the common visible measure from literal indices, verifies all hidden
mass equations and all 332 old inequalities, and checks the 12-weight new row.
No discovery code is imported and no floating optimizer is needed.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
import hashlib, json, time
from main_cross_query_features_v1 import pay, query_samples, all_332, projection, weighted_value

B = Path(__file__).resolve().parent
pp = B/'master_cuts/dynamic_5775_exact.json'
lp = B/'joint_requery/exact_332_lift_cross_strictness_5775_v1.json'
ip = B/'joint_requery/cross_query_disagreement_identity_5775_v1.json'
cp = B/'joint_requery/cross_pairs_selected_5775_v1.json'
point, submitted, identity, pack = (json.loads(p.read_text()) for p in (pp,lp,ip,cp))
point_sha = hashlib.sha256(pp.read_bytes()).hexdigest()
assert submitted['source_sha256'] == identity['source_sha256'] == pack['source_sha256'] == point_sha
assert (submitted['i'], submitted['k'], submitted['member'], submitted['orb']) == (3,3,0,[0,0])
start = time.time()
cols = point['columns']
blocks = []
for ci,c in enumerate(cols):
    if c['kind'] == 'hist': blocks.append([ci,c,{}])
    elif c['kind'] == 'joint-reply':
        family,diag,wi,wj = c['group']
        blocks[-1][2][family,diag,tuple(wi),tuple(wj),tuple(c['state'])] = F(c['weight'])

actual = [F(0)]*6
K = F(cols[0]['weight'])
coarse, refined = defaultdict(F), defaultdict(F)
for ci,h,groups in blocks:
    a = tuple(map(int,h['actual_bits']))
    hm = F(h['weight'])
    for i in range(6): actual[i] += hm*pay(a[i],sum(a))
    words = tuple(w for w,n in zip(product((0,1),repeat=3),h['hist']) for _ in range(n))
    for i in range(6):
        for j in range(6):
            if i == j: continue
            masses = {state:groups.get((0,0,words[i],words[j],state),F(0)) for state in ((0,1),(1,0),(1,1))}
            masses[0,0] = hm - sum(masses.values(),F(0))
            assert min(masses.values()) >= 0
            for state,m in masses.items():
                _,qs,moments = query_samples(a,words,i,j,state)
                key = (sum(a[:3]),sum(a[:5]),state[0],qs)
                coarse[key] += m/30
                refined[key+(moments,)] += m/30
coarse = {k:m for k,m in coarse.items() if m}
refined = {k:m for k,m in refined.items() if m}
assert actual == list(map(F,submitted['actual_utilities']))
assert K == F(submitted['K'])
r,u6 = actual[3],actual[5]
states,masses = [],{}
for rec in submitted['old_visible']:
    p,ell,t,qs = rec['state']
    key = (p,ell,t,tuple(map(F,qs)))
    assert key not in masses
    states.append(key)
    masses[key] = F(rec['mass'])
assert masses == coarse and len(states) == 56

lift = submitted['old_lift']
observed_mass = [F(0)]*len(states)
sums = defaultdict(F)
for atom in lift['support']:
    vi,h,w = atom['visible'],tuple(atom['hidden']),F(atom['mass'])
    assert 0 <= vi < len(states) and w > 0
    assert len(h) == 6 and all(v in (0,1) for v in h[:4]) and h[4:] == (0,0)
    observed_mass[vi] += w
    values,budget = all_332(*states[vi],h,3)
    for name,value in values.items(): sums[name] += w*value
assert observed_mass == [masses[v] for v in states]
assert len(lift['support']) == 79
assert set(sums) == set(lift['all_332_slacks_at_actual'])
rsmall = F(lift['r_recovered_feasible'])
assert 0 <= rsmall <= r
assert r-rsmall == F(lift['r_actual_minus_recovered'])
gaps = {}
for name,(sr,su,sk) in budget.items():
    gap = sr*r+su*u6+sk*K-sums[name]
    assert gap == F(lift['all_332_slacks_at_actual'][name]) >= 0
    assert sr*rsmall+su*u6+sk*K-sums[name] >= 0
    gaps[name] = gap

# Check the advertised common refinement is a genuine disintegration, with
# each old atom split by n_v/n_y. All old features are independent of moments.
refined_mass_check = defaultdict(F)
for atom in lift['support']:
    coarse_key = states[atom['visible']]
    for full_key,m in refined.items():
        if full_key[:4] == coarse_key:
            refined_mass_check[full_key] += F(atom['mass'])*m/coarse[coarse_key]
assert dict(refined_mass_check) == refined

theta = {n:F(w) for n,w in identity['integer_cross_weights'].items()}
old = {n:F(w) for n,w in identity['old_332_replacement_weights'].items()}
assert len(theta) == 12 and theta['sourceT']+theta['sourceC'] == 413
assert sum(w for n,w in theta.items() if n.startswith('price:')) == 164
assert sum(w for n,w in theta.items() if n.startswith('cap:')) == 14
assert theta['oldpair1:6,10:product'] == 48
replacement = dict(theta)
del replacement['oldpair1:6,10:product']
replacement.update({'pair1:q6,q6':F(24),'pair1:q10,q10':F(24)})
assert old == replacement
newphi,oldphi = projection(theta,3),projection(old,3)
table = {}
for rec in identity['min_table']:
    state = tuple(rec['state'])
    assert state not in table
    table[state] = rec
assert len(table) == 192
hidden = tuple(bits+(0,0) for bits in product((0,1),repeat=4))
for p in range(4):
    for ell in range(p,p+3):
        for t,ti,ci,bj in product((0,1),repeat=4):
            qs = [F(0)]*17
            qs[6],qs[8],qs[10] = F(ti),F(ci),F(bj)
            qs = tuple(qs)
            products = (('oldpair1:6,10:product',F(ti*bj)),)
            premium = F(24*(ti-bj)**2,(p+t+1)*(p+t+2))
            for h in hidden:
                assert weighted_value(p,ell,t,qs,h,tuple(theta.items()),products) - weighted_value(p,ell,t,qs,h,tuple(old.items())) == premium
            nm,om = newphi(p,ell,t,qs,products),oldphi(p,ell,t,qs)
            assert nm == om+premium
            rec = table[p,ell,t,ti,ci,bj]
            assert nm == F(rec['new_min_integer_scale'])
            assert om == F(rec['old_min_integer_scale'])
            assert premium == F(rec['disagreement_increment_integer_scale'])

newcost,oldcost,premium = F(0),F(0),F(0)
for (p,ell,t,qs),m in coarse.items():
    products = (('oldpair1:6,10:product',qs[6]*qs[10]),)
    newcost += m*newphi(p,ell,t,qs,products)
    oldcost += m*oldphi(p,ell,t,qs)
    premium += m*F(24,413)*(qs[6]-qs[10])**2/((p+t+1)*(p+t+2))
newgap = (413*r+164*u6+14*K-newcost)/413
oldgap = (413*r+164*u6+14*K-oldcost)/413
assert newgap == F(identity['new_normalized_slack']) == F(submitted['cross_cut']['exact_slack']) == F(pack['cuts'][0]['exact_slack']) < 0
assert oldgap == F(identity['old_replacement_normalized_slack']) >= 0
assert premium == oldgap-newgap == F(identity['normalized_disagreement_premium']) > 0
audited = json.loads((B/'main_verify_cross_pairs_5775.json').read_text())
assert audited['status'] == 'PASS' and audited['point_sha256'] == point_sha
assert audited['pack_sha256'] == hashlib.sha256(cp.read_bytes()).hexdigest()
assert audited['rows'][0]['row_sha256'] == submitted['cross_cut']['row_sha256']

report = {'status':'PASS','scope':'Strict P616 subset P332 on the same refined actual4/R/orb00/17-menu visible domain; exact old hidden lift plus an independently reconstructed new negative row; no complete SPE assertion',
          'point_sha256':point_sha,'lift_sha256':hashlib.sha256(lp.read_bytes()).hexdigest(),
          'identity_sha256':hashlib.sha256(ip.read_bytes()).hexdigest(),'cross_pack_sha256':hashlib.sha256(cp.read_bytes()).hexdigest(),
          'old_visible_states':len(states),'refined_visible_states':len(refined),'old_hidden_atoms':len(lift['support']),
          'mass_equalities_exact':True,'refinement_mass_equalities_exact':True,'old_rows_checked':len(gaps),'minimum_old_slack':str(min(gaps.values())),
          'old_source_margin':str(r-rsmall),'all_192_min_identities_exact':True,'hidden_identity_cases':192*16,
          'new_negative_slack':str(newgap),'old_replacement_slack':str(oldgap),'disagreement_premium':str(premium),
          'seconds':time.time()-start}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
