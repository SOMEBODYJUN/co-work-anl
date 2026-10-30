"""Boss3 raw-share audit of the submitted binary four-tail certificate.

No author modules or audit programs are imported or executed. The certificate
is read from a pinned git object. All output stays beside this audit.
"""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
REPO = next(p for p in HERE.parents if (p / 'AGENTS.md').is_file())
REF = 'a1d7184466e5ae115a86efd8c0da6da2aabfaa09'
SRC = 'research/workspaces/customer-attraction/R-febfdd131cde4128882ca0edd4d712ba/parent/binary_tail_exact_1999.json'
raw = subprocess.check_output(['git', 'show', REF + ':' + SRC], cwd=REPO)
cert = json.loads(raw)
weights = {key: F(value) for key, value in cert['multipliers'].items()}
assert len(weights) == 13 and all(w >= 0 for w in weights.values())
beta = (F(cert['beta0']), F(cert['beta1']))
assert beta == (F(1999, 1000), F(5, 3))

def div(n, d):
    return F(n, d) if n else F(0)

def terms(p, seven, opt):
    a,b,c,d,q,r,s = seven
    paths = {'actual': (a,b,c,d), 'off': (d,q,r,s)}
    bits = dict(zip('abcdqrs', seven))
    def payoff(path, i):
        return div(path[i], p + sum(path))
    ans = {}
    for name, path in paths.items():
        first_legal = 0 if name == 'actual' else 1
        for i in range(first_legal, 4):
            for label, member in bits.items():
                ans[f'{name}:{i}:K:{label}'] = payoff(path, i) - div(member, p + sum(path[:i]) + 4-i)
        ans[f'{name}:3:sum-opt'] = sum((payoff(path,3) - div(bit, p + sum(path[:3])+1) for bit in opt), F(0))
        bg = p + sum(path[:2])
        h = payoff(path,2) + payoff(path,3) + div(path[2], (bg+1)*(bg+2))
        # Reconstruct the six distinct INDEX pairs separately, not via e-count.
        ans[f'{name}:pair-opt'] = sum((h-div(opt[i]+opt[j], bg+opt[i]+opt[j]) for i,j in combinations(range(4),2)), F(0))
    ans['root-copy-d'] = payoff(paths['actual'],0) - payoff(paths['off'],0)
    assert set(weights) <= ans.keys()
    k = a+b+c+d
    target = div(sum(opt), p + sum(opt))
    lhs = beta[p] * div(k, p+k) - target
    return lhs, {key: ans[key] for key in weights}

res = {}
row_digest = hashlib.sha256()
raw_checked = 0
for p, seven, opt in product((0,1), product((0,1), repeat=7), product((0,1), repeat=4)):
    lhs, rows = terms(p, seven, opt)
    remainder = lhs - sum((weights[key]*rows[key] for key in weights), F(0))
    assert remainder >= 0, (p, seven, opt, remainder)
    key = (p, seven, sum(opt))
    assert key not in res or res[key] == remainder
    res[key] = remainder
    row_digest.update(repr((p,seven,opt,str(lhs),tuple(str(rows[k]) for k in weights),str(remainder))).encode())
    raw_checked += 1
assert raw_checked == 4096 and len(res) == 1280
assert min(res.values()) == 0
assert sum(x == 0 for x in res.values()) == 19

# Eliminate only the three additional real-tail memberships by taking all eight
# possibilities. This produces a 160-state table usable with matched root types.
retained = []
for p, actual, e in product((0,1), product((0,1), repeat=4), range(5)):
    r, aux = min((res[(p, actual+aux, e)], aux) for aux in product((0,1), repeat=3))
    retained.append({'p': p, 'abcd': ''.join(map(str,actual)), 'comparison_count': e,
                     'minimum_residual': str(r), 'attaining_qrs': ''.join(map(str,aux))})
assert len(retained) == 160

# The matched-complement and inside-share identities use no equilibrium rows.
root_checks = []
for membership in product((0,1), repeat=5):
    e = sum(membership)
    matched = sum((div(e-t, e) for t in membership), F(0))
    assert matched == (4 if e else 0)
    root_checks.append(str(matched))
for t,k in product((0,1), range(5)):
    forced_share = div(t, t+k)
    inside = t * div(k, t+k)
    assert inside == t-forced_share

# A root theme Y need not be one of the optimal indices. A safe unindexed lift
# sums all five comparator quartets instead of using the matched identity.
for p,e in product((0,1), range(6)):
    all_quartets = div(e*(e-1), p+e-1) + div((5-e)*e, p+e)
    assert all_quartets >= 4*div(int(e>0), p+1)
assert 5*beta[0]*3000 == 29985
assert (2-5*(beta[0]-beta[1]))*3000 == 1015

out = {
    'status': 'PASS independent raw-share coefficient audit; not a new welfare proof',
    'pinned_ref': REF, 'certificate_path': SRC,
    'certificate_sha256': hashlib.sha256(raw).hexdigest(),
    'raw_rows_sha256': row_digest.hexdigest(),
    'author_modules_imported': False, 'author_audits_executed': False,
    'raw_states': raw_checked, 'compressed_states': len(res),
    'nonnegative_multipliers': len(weights), 'minimum_residual': '0',
    'zero_compressed_states': sum(v==0 for v in res.values()),
    'beta_out': str(beta[0]), 'beta_in': str(beta[1]),
    'matched_root_membership_states': len(root_checks),
    'matched_root_identity': 'sum_i R_{1_Ti}(T_-i)=4 OPT_5',
    'coarse_root_row': '5997 sum_i V_i+997 sum_i z_i-997 sum_i|Ti|-12000 OPT_5>=0',
    'old_retained_coarse_row': '2998 sum_i V_i+251 sum_i z_i-251 sum_i|Ti|-6000 OPT_5>=0',
    'new_minus_twice_old_row': 'sum_i Vout_i-494 sum_i Vin_i',
    'unindexed_root_E_lift_states': 12,
    'unindexed_root_E_lift': '12000 OPT_5<=29985 V+1015 |Y|+4985 z; Y is any root theme',
    'retained_residuals_160': retained,
    'scope': 'All algebraic client types, plus independent node-legality review in companion report; no sampling of games.',
}
dest = HERE / 'oct25_binary_tail_raw_audit.json'
dest.write_text(json.dumps(out, ensure_ascii=False, indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='retained_residuals_160'}, ensure_ascii=False, indent=2))
