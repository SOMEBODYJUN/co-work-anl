"""Numerical discovery: pool expected real deviation backgrounds before reciprocal.

Every Gamma row uses the full ordered policy. Fixed-p customer optimization is
an LP, p optimization is local SLSQP; neither negative output proves a bridge.
"""
import sys,json,math,itertools,argparse,random
from pathlib import Path
import numpy as np
from scipy.optimize import linprog,minimize

ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction import Instance,ExactSPESolver,CustomerType
OUT=Path(__file__).resolve().parent

def build(actions,n,k):
    mem=np.array([[(s>>a)&1 for s in range(1,1<<k)] for a in range(k)],dtype=np.int16)
    scale=math.lcm(*range(1,n+1)); rows=[]; ends={}
    def utility(a,z):
        return mem[a]*(scale//np.maximum(np.bincount(z,minlength=k)@mem,1))
    def walk(h):
        if len(h)==n:return h
        children=[walk(h+(a,)) for a in range(k)]
        a=actions[h];z=children[a];ends[h]=z
        for t in range(k):
            if t!=a:rows.append(utility(a,z)-utility(t,children[t]))
        return z
    z=walk(()); G=np.unique(np.array(rows),axis=0).astype(float)/scale
    cover=(np.bincount(z,minlength=k)@mem>0).astype(float)
    # H[a] averages over actual positions i the true terminal load if i switches
    # to a, deleting the deviator. Consequently each H[a] is a legal fractional
    # catalog background of total mass n-1.
    H=np.zeros((k,len(cover)));full=np.zeros_like(H)
    for i in range(n):
        for a in range(k):
            h=z[:i]+(a,)
            leaf=h if len(h)==n else ends[h]
            load=np.bincount(leaf,minlength=k)@mem
            full[a]+=load/n; H[a]+=(load-mem[a])/n
    return G,cover,mem,H,full,z

def probe(G,c,mem,H,n,seed,starts=12):
    rng=np.random.default_rng(seed);best=None
    for st in range(starts):
        p=np.ones(len(mem))/len(mem) if st==0 else rng.dirichlet(np.ones(len(mem)))
        for it in range(15):
            den=1+p@H;coef=n*(p@mem)/den
            lp=linprog(-coef,A_ub=-G,b_ub=np.zeros(len(G)),A_eq=[c],b_eq=[1],bounds=(0,None),method='highs')
            if not lp.success:raise RuntimeError(lp.message)
            w=lp.x
            def obj(p):return -n*np.dot(w,(p@mem)/(1+p@H))
            def jac(p):
                t=p@mem;d=1+p@H
                return -n*((mem/d-H*(t/d**2))@w)
            res=minimize(obj,p,jac=jac,method='SLSQP',bounds=[(0,1)]*len(p),constraints={'type':'eq','fun':lambda p:sum(p)-1,'jac':lambda p:np.ones(len(p))},options={'ftol':1e-12,'maxiter':150})
            p=np.maximum(res.x,0);p/=sum(p);ratio=-obj(p)
            if best is None or ratio>best['ratio']+1e-10:
                best=dict(ratio=float(ratio),p=p.tolist(),weights=w.tolist(),start=st,iteration=it)
            if ratio>1+1e-7:return best
    return best

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--random',type=int,default=0);ap.add_argument('--extra',action='store_true');args=ap.parse_args()
    report=[];prng=random.Random(181932014)
    for name in ['aggregate_theta_failure','individual_security_failure','local_security_increment','root_tax_failure','worst_pne_welfare_failure']:
        ins=Instance.from_dict(json.loads((ROOT/'examples/customer_attraction'/f'{name}.json').read_text()))
        n,k=ins.players,ins.topic_count
        solver=ExactSPESolver(ins);cert=solver.certificate(min(solver.outcomes(),key=ins.welfare))
        G,c,mem,H,full,z=build(cert.actions,n,k)
        best=probe(G,c,mem,full if args.extra else H,n,sum(map(ord,name)))
        rec=dict(name=name,n=n,k=k,extra=args.extra,rows=len(G),on_path=list(z),**best)
        report.append(rec);print(json.dumps({x:rec[x] for x in ['name','n','k','extra','ratio']}),flush=True)
        if best['ratio']>1+1e-7:
            rec['actions']=[{'history':list(h),'action':a} for h,a in cert.actions.items()]
            (OUT/('pool_full_candidate.json' if args.extra else 'pool_delete_candidate.json')).write_text(json.dumps(rec,indent=2)+'\n');break
    for trial in range(args.random):
        n,k=[(3,6),(4,6),(5,7),(6,7)][trial%4]
        density=prng.choice([.1,.3,.7,1.])
        customers=[CustomerType(frozenset(a for a in range(k) if mask>>a&1),prng.randrange(1,12)) for mask in range(1,1<<k) if prng.random()<density]
        ins=Instance(tuple(map(str,range(k))),tuple(customers),n)
        solver=ExactSPESolver(ins);cert=solver.certificate(min(solver.outcomes(),key=ins.welfare),action_selector=lambda h,c:prng.choice(c),continuation_selector=lambda h,c:prng.choice(c))
        G,c,mem,H,full,z=build(cert.actions,n,k)
        best=probe(G,c,mem,full if args.extra else H,n,trial+1923,starts=5)
        rec=dict(name=f'random_{trial}',n=n,k=k,extra=args.extra,rows=len(G),on_path=list(z),**best)
        report.append(rec);print(json.dumps({x:rec[x] for x in ['name','n','k','extra','ratio']}),flush=True)
        if best['ratio']>1+1e-7:
            rec['actions']=[{'history':list(h),'action':a} for h,a in cert.actions.items()]
            (OUT/('pool_full_candidate.json' if args.extra else 'pool_delete_candidate.json')).write_text(json.dumps(rec,indent=2)+'\n');break
    (OUT/('pool_full_report.json' if args.extra else 'pool_delete_report.json')).write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
