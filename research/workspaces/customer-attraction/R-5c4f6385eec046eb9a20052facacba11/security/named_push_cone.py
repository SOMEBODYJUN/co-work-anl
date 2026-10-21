"""Discovery: jointly vary p and customer masses in two existing full policies."""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog,minimize

OUT=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--name',default='five_individual_security')
    ap.add_argument('--starts',type=int,default=30);args=ap.parse_args()
    inst=json.loads(Path('examples/customer_attraction',args.name+'.json').read_text())
    raw=json.loads(Path('evidence/certificates/customer_attraction',args.name+'.json').read_text())
    print(inst.keys(),flush=True)
    actions={tuple(r['history']):r['action']for r in raw['strategy']['actions']}
    k=len(inst['topics']);r=inst['players']
    cs=inst['customers']
    masks=[sum(1<<int(a)for a in c['topics'])for c in cs]
    ws=np.array([c['multiplicity']for c in cs],dtype=float)
    member=np.array([[(mask>>a)&1 for mask in masks]for a in range(k)])
    def end(h):
        while len(h)<r:h=h+(actions[h],)
        return h
    def util(a,h):return member[a]/np.maximum(np.sum(member[list(h)],axis=0),1)
    rows=[]
    for h,a in actions.items():
        z=end(h);c=util(a,z)
        for b in range(k):
            if b!=a:rows.append(c-util(b,end(h+(b,))))
    G=np.unique(np.array(rows),axis=0)
    z=end(());root=util(z[0],z)
    C=np.array([np.sum(member[list(end((a,)))],axis=0)for a in range(k)])
    def val(p,w):return np.dot(w,(p@member)/(1+p@C))
    def grad(p,w):
        t=p@member;den=1+p@C
        return member@(w/den)-C@(w*t/den**2)
    def pstep(p,w):
        ans=minimize(lambda pp:-val(pp,w),p,jac=lambda pp:-grad(pp,w),
            bounds=[(0,1)]*k,constraints=[{'type':'eq','fun':lambda pp:pp.sum()-1,
            'jac':lambda pp:np.ones(k)}],method='SLSQP',options={'ftol':1e-12,'maxiter':300})
        return ans.x
    def wstep(p):
        f=(p@member)/(1+p@C)
        ans=linprog(root-f,A_ub=-G,b_ub=np.zeros(len(G)),A_eq=root[None,:],b_eq=[1.],bounds=(0,None),method='highs')
        if not ans.success:raise RuntimeError(ans.message)
        return ans.x,-ans.fun
    rng=np.random.default_rng(987717)
    best=-1e6
    for start in range(args.starts):
        p=np.ones(k)/k if start==0 else rng.dirichlet(np.ones(k)*rng.choice([.1,.5,2.]))
        w=ws.copy()/np.dot(ws,root)
        for iteration in range(10):
            p=pstep(p,w);w,gap=wstep(p)
            if gap>best+1e-9:
                best=gap;packet=dict(status='numerical_only',name=args.name,start=start,iteration=iteration,
                    masks=masks,weights=w.tolist(),p=p.tolist(),gap=gap,path=z)
                (OUT/(args.name+'_full_push_best.json')).write_text(json.dumps(packet,indent=2)+'\n')
                print(json.dumps({kk:packet[kk]for kk in ['name','start','iteration','gap']}),flush=True)
            if gap>1e-7:return
    print(json.dumps(dict(status='finite_no_separation',name=args.name,starts=args.starts,best=best)),flush=True)

if __name__=='__main__':main()
