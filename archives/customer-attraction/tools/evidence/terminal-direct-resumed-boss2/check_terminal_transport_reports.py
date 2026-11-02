"""New exact reconstruction of four frozen floating LP reports; no LP/import of source."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse, hashlib, json, time


def column(m, state):
    bits, d, ell = state
    assert len(bits) == m and all(v in (0, 1) for v in bits)
    assert 0 <= d <= m and ell in (0, m)
    c = sum(bits)
    p = sum(bits[:-2])
    a, b = bits[-2:]
    D = (p+1)*(p+2)
    u = [F(v, c) if c else F(0) for v in bits]
    H = u[-2]+u[-1]+F(a, D)
    q = [sum(bits[:i])+m-i for i in range(m)]
    r = {f'copy:{i}:{j}': u[i]-F(bits[j], q[i]) for i in range(m) for j in range(m)}
    r.update({f'copy-opt:{i}': m*u[i]-F(d, q[i]) for i in range(m)})
    r['menu-G'] = m*u[-2]+u[-1]/2-F(d, p+1)-F(ell, 2*m*(p+a+1))+F(d*ell, m*D)
    r['pair-opt-all'] = m*m*H-F(2*m*d, p+1)+F(d*d, D)
    r['pair-opt-diag'] = m*H-F(2*d, p+1)+F(d, D)
    r['pair-opt-offdiag'] = m*(m-1)*H-F(2*(m-1)*d, p+1)+F(d*d-d, D)
    r.update({f'pair-opt-actual:{j}': m*H-F(d+m*v, p+1)+F(d*v, D) for j, v in enumerate(bits)})
    r.update({f'pair-actual:{j}:{k}': H-F(bits[j]+bits[k], p+1)+F(bits[j]*bits[k], D) for j in range(m) for k in range(j, m)})
    assert r['pair-opt-all'] == r['pair-opt-diag']+r['pair-opt-offdiag']
    return r, int(c > 0), int(d > 0)


def recover(A, b, guesses):
    """Exact RREF; free coordinates fixed to explicit rationalized saved guesses."""
    n = len(guesses)
    M = [[F(x) for x in row]+[F(y)] for row, y in zip(A, b)]
    pivots = []
    row = 0
    for col in range(n):
        found = next((i for i in range(row, len(M)) if M[i][col]), None)
        if found is None:
            continue
        M[row], M[found] = M[found], M[row]
        lead = M[row][col]
        M[row] = [v/lead for v in M[row]]
        for i in range(len(M)):
            if i != row and M[i][col]:
                factor = M[i][col]
                M[i] = [v-factor*w for v, w in zip(M[i], M[row])]
        pivots.append(col)
        row += 1
        if row == len(M):
            break
    assert all(any(line[:n]) or not line[-1] for line in M), 'inconsistent exact equations'
    free = [j for j in range(n) if j not in pivots]
    x = [F(0)]*n
    for j in free:
        x[j] = F(str(guesses[j])).limit_denominator(10**6)
    for i, j in enumerate(pivots):
        x[j] = M[i][-1]-sum((M[i][k]*x[k] for k in free), F(0))
    assert all(sum((F(v)*w for v, w in zip(line, x)), F(0)) == F(y) for line, y in zip(A, b))
    return x, {'rank': len(pivots), 'unknowns': n, 'free_coordinates': {str(j):str(x[j]) for j in free}}


def check_one(path):
    raw = path.read_bytes()
    d = json.loads(raw)
    m = d['m']
    support = d['support']
    states = [a['state'] for a in support]
    assert len({json.dumps(s) for s in states}) == len(states)
    cols = [column(m, s) for s in states]
    rownames = list(cols[0][0])
    active = [r['row'] for r in d['dual']]
    assert len(set(active)) == len(active) and all(r in rownames for r in active)
    masses, primal_recovery = recover([[w for _,w,_ in cols]]+[[r[name] for r,_,_ in cols] for name in active], [1]+[0]*len(active), [a['mass'] for a in support])
    assert min(masses) > 0
    slacks = {name:sum((r[name]*mu for (r,_,_),mu in zip(cols,masses)), F(0)) for name in rownames}
    assert min(slacks.values()) >= 0
    W = sum((w*mu for (_,w,_),mu in zip(cols,masses)), F(0))
    O = sum((o*mu for (_,_,o),mu in zip(cols,masses)), F(0))
    assert W == 1 and O > 2
    extra_states = [[[0,0,1,1,1,0,1,0],1,0]] if m == 8 else []
    dual_cols = cols+[column(m, state) for state in extra_states]
    dual, dual_recovery = recover([[-r[name] for name in active]+[w] for r,w,o in dual_cols], [o for _,_,o in dual_cols], [r['weight'] for r in d['dual']]+[d['equality_dual']])
    dual_recovery['additional_zero_remainder_states'] = extra_states
    weights, beta = dual[:-1], dual[-1]
    assert min(weights) >= 0 and beta == O
    prices = []
    groups = []
    for bits in product((0,1), repeat=m):
        group = []
        for degree in range(m+1):
            for ell in (0,m):
                r,w,o = column(m, (bits,degree,ell))
                eta = beta*w-o-sum((v*r[name] for name,v in zip(active,weights)),F(0))
                assert eta >= 0, (m,bits,degree,ell,str(eta))
                prices.append({'bits':''.join(map(str,bits)), 'd':degree,'ell':ell,'remainder':str(eta)})
                group.append(eta)
        groups.append({'bits':''.join(map(str,bits)), 'minimum_remainder':str(min(group)), 'zero_columns':sum(v==0 for v in group)})
    assert d['rows']==len(rownames)==(3*m*m+5*m+8)//2
    assert d['types']==len(prices)==2**m*(m+1)*2
    return {'m':m,'input_sha256':hashlib.sha256(raw).hexdigest(), 'saved_beta':d['beta'], 'saved_equality_dual':d['equality_dual'], 'rows':len(rownames),'types':len(prices), 'new_exact_beta':str(beta),'new_exact_beta_float':float(beta),'support_count':len(masses),'positive_dual_count':sum(v>0 for v in weights),'primal_recovery':primal_recovery,'dual_recovery':dual_recovery,'W':str(W),'O':str(O),'exact_support':[{'state':s,'mass':str(mu),'saved_mass':a['mass']} for s,mu,a in zip(states,masses,support)], 'exact_dual':[{'row':name,'weight':str(v),'saved_weight':old['weight']} for name,v,old in zip(active,weights,d['dual'])], 'all_row_slacks':{k:str(v) for k,v in slacks.items()},'zero_rows':sum(v==0 for v in slacks.values()),'all_type_remainders':prices,'minimum_by_actual_bits':groups,'zero_columns':sum(x['remainder']=='0' for x in prices), 'max_mass_difference_from_saved_float':max(abs(float(mu)-a['mass']) for mu,a in zip(masses,support)), 'scope':'New exact primal-dual certificate for finite necessary-row cone; no game or SPE realization.'}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('source_dir',type=Path);ap.add_argument('output',type=Path);ap.add_argument('--only',type=int,nargs='+',choices=(5,6,7,8));args=ap.parse_args()
    start=time.monotonic()
    reports=[]
    for m in (args.only or (5,6,7,8)):
        report=check_one(args.source_dir/f'probe_m{m}.json')
        args.output.with_name(args.output.stem+f'-m{m}.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
        reports.append(report)
    result={'status':'all exact finite-cone certificates passed','origin':'new RREF recovery from saved support and positive-dual row names; original floating reports unchanged','original_LP_runs':0,'original_audit_runs':0,'source_algorithm_imports':0,'certificate_checks':reports,'elapsed_seconds':time.monotonic()-start}
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'elapsed_seconds':result['elapsed_seconds'],'certificates':[{k:r[k] for k in ('m','new_exact_beta','rows','types','support_count','positive_dual_count','zero_rows','zero_columns','primal_recovery','dual_recovery')} for r in reports]},ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
