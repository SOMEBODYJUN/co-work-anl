"""Exact Farkas certificates for every fractional query in one complete SPE cone.

`build` uses scipy only to propose dual coefficients. `verify` needs no optimizer
and independently reconstructs every full-history SPE comparison over Fraction.
A successful result proves only the stated fixed-policy cone assertion.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import argparse,json,sys
BASE=Path(__file__).resolve().parent
ROOT=next(p for p in BASE.parents if (p/'customer_attraction/__init__.py').is_file())
sys.path[:0]=[str(BASE),str(ROOT),str(ROOT/'tests/audits')]
from fractional_query_vertices import enumerate_vertices
from customer_attraction import Instance,ExactSPESolver,StrategyCertificate,verify_certificate


def row_payoff(p,q,a):
    return tuple(F(1,sum(q[b] for b in range(p) if mask>>b&1)) if mask>>a&1 else F(0) for mask in range(1,1<<p))


def reconstruct_rows(p,m,cert):
    required={h for d in range(m) for h in product(range(p),repeat=d)}
    if set(cert.actions)!=required:raise ValueError('incomplete ordered strategy')
    terms={h:tuple(h.count(a) for a in range(p)) for h in product(range(p),repeat=m)}
    for d in range(m-1,-1,-1):
        for h in product(range(p),repeat=d):terms[h]=terms[h+(cert.actions[h],)]
    if terms[()]!=cert.terminal_counts:raise ValueError('root count mismatch')
    rows=set()
    for h,a in cert.actions.items():
        actual=row_payoff(p,terms[h],a)
        for b in range(p):
            if b!=a:
                alternative=row_payoff(p,terms[h+(b,)],b)
                row=tuple(x-y for x,y in zip(actual,alternative))
                if any(row):rows.add(row)
    q=terms[()];w=tuple(F(any(q[a] and mask>>a&1 for a in range(p))) for mask in range(1,1<<p))
    return tuple(sorted(rows)),w


def objective(p,m,q,a,z,kind):
    u=row_payoff(p,q,a);tau=sum(z)
    c=tuple(min(F(1),sum(z[b] for b in range(p) if mask>>b&1)) for mask in range(1,1<<p))
    w=tuple(F(any(q[b] and mask>>b&1 for b in range(p))) for mask in range(1,1<<p))
    if kind=='tstar':return tuple(x-(m-1+tau)*y for x,y in zip(c,u))
    if kind=='price_plus_u':return tuple(x-(tau-1)*y-v for x,y,v in zip(c,u,w))
    if kind=='price':return tuple(x-tau*y-v for x,y,v in zip(c,u,w))
    raise ValueError('unknown price objective')


def build(kind,output):
    import numpy as np
    from scipy.optimize import linprog
    source=ROOT/'examples/customer_attraction/worst_pne_welfare_failure.json'
    game=Instance.from_dict(json.loads(source.read_text()));solver=ExactSPESolver(game)
    target=min(solver.worst_outcomes());cert=solver.certificate(target);verify_certificate(game,cert).assert_valid()
    rows,w=reconstruct_rows(game.topic_count,game.players,cert);V=enumerate_vertices(game.topic_count)[0];proofs=[]
    for a,count in enumerate(target):
        if not count:continue
        for j,z in enumerate(V):
            c=objective(game.topic_count,game.players,target,a,z,kind)
            out=linprog(-np.array(c,float),A_ub=-np.array(rows,float),b_ub=np.zeros(len(rows)),A_eq=[w],b_eq=[1],bounds=(0,None),method='highs')
            if not out.success:raise AssertionError(out.message)
            beta=F(float(-out.eqlin.marginals[0])).limit_denominator(10**9)
            mus=tuple(F(float(-x)).limit_denominator(10**9) for x in out.ineqlin.marginals)
            remainder=tuple(beta*w[k]-sum(mu*row[k] for mu,row in zip(mus,rows))-c[k] for k in range(len(w)))
            if any(x<0 for x in mus) or any(x<0 for x in remainder):raise AssertionError('failed exact dual recovery')
            proofs.append({'topic':a,'query_index':j,'beta':str(beta),'multipliers':[[i,str(mu)] for i,mu in enumerate(mus) if mu]})
    result={'scope':'one fixed complete ordered-history policy cone; all nonnegative customer multiplicities; all fractional queries','kind':kind,'source_instance':game.to_dict(),'source_file':str(source.relative_to(ROOT)),'strategy':cert.to_dict(),'vertices':[[str(x) for x in z] for z in V],'proofs':proofs,'row_count':len(rows),'all_bounds_nonpositive':all(F(proof['beta'])<=0 for proof in proofs),'universal_policy_claim':False}
    output.write_text(json.dumps(result,indent=2)+'\n');return verify(output)


def verify(file):
    data=json.loads(file.read_text());game=Instance.from_dict(data['source_instance']);cert=StrategyCertificate.from_dict(data['strategy']);check=verify_certificate(game,cert);check.assert_valid()
    p=game.topic_count;m=game.players;rows,w=reconstruct_rows(p,m,cert);V=tuple(tuple(F(x) for x in z) for z in data['vertices'])
    if V!=enumerate_vertices(p)[0]:raise ValueError('query list is not complete exact arrangement')
    used={a for a,count in enumerate(cert.terminal_counts) if count};required={(a,j) for a in used for j in range(len(V))}
    seen=set();bounds=[]
    for proof in data['proofs']:
        a=proof['topic'];j=proof['query_index'];key=(a,j)
        if key not in required or key in seen:raise ValueError('missing or duplicate indexed proof')
        seen.add(key);beta=F(proof['beta']);mu={}
        for i,value in proof['multipliers']:
            if i in mu or not 0<=i<len(rows):raise ValueError('invalid multiplier index')
            mu[i]=F(value)
            if mu[i]<0:raise ValueError('negative Farkas multiplier')
        c=objective(p,m,cert.terminal_counts,a,V[j],data['kind'])
        if any(beta*w[k]-sum(v*rows[i][k] for i,v in mu.items())-c[k]<0 for k in range(len(w))):raise ValueError('negative exact dual residual')
        bounds.append(beta)
    if seen!=required:raise ValueError('proof does not cover all topics and all fractional queries')
    result={'verified':True,'scope':'fixed supplied full-policy cone only','kind':data['kind'],'queries':len(V),'occupied_topics':len(used),'dual_proofs':len(bounds),'row_count':len(rows),'all_bounds_nonpositive':max(bounds)<=0,'maximum_beta':str(max(bounds)),'source_histories_verified':check.checked_histories,'source_deviations_verified':check.checked_deviations}
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('operation',choices=['build','verify']);ap.add_argument('--kind',choices=['tstar','price','price_plus_u'],default='tstar');ap.add_argument('--file',type=Path,required=True);args=ap.parse_args()
    print(json.dumps(build(args.kind,args.file) if args.operation=='build' else verify(args.file),indent=2))
