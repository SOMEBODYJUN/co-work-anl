"""Exploratory cone search for actual-node static-menu restrictions."""
from pathlib import Path
import argparse,json,sys
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'round3_security'))
from cone_optimize import cone
from menu_probe import Search,probe


def optimize(s,w,rounds=15):
    info,root,G,states=cone(s,w)
    menu=probe(s,w);counts=[tuple(q) for q in menu['menu_counts']]
    B=np.array([s.security_coeff[s.cts[s.n-1].index(q)]/s.scale for q in counts])
    p=np.array(menu['restricted_query']);c=s.coverage_coeff[root]
    trace=[];previous=None
    for i in range(rounds):
        fixed=np.einsum('a,hat->ht',p,B)
        lp=linprog(np.r_[np.zeros(len(w)),-1],
            A_ub=np.r_[np.c_[-G,np.zeros(len(G))],np.c_[-fixed,np.ones(len(fixed))]],
            b_ub=np.zeros(len(G)+len(fixed)),A_eq=[np.r_[c,0]],b_eq=[1],
            bounds=[(0,None)]*len(w)+[(None,None)],method='highs')
        if not lp.success:return dict(status=lp.message)
        w=lp.x[:-1];pay=B@w
        q=linprog(np.r_[np.zeros(s.k),-1],A_ub=np.c_[-pay,np.ones(len(pay))],
            b_ub=np.zeros(len(pay)),A_eq=[np.r_[np.ones(s.k),0]],b_eq=[1],
            bounds=[(0,None)]*s.k+[(None,None)],method='highs')
        if not q.success:raise RuntimeError(q.message)
        p=q.x[:-1];value=q.x[-1]
        trace.append(dict(iteration=i,value=float(value),gap=float(1-s.n*value),
                          weak_gap=float(1-(s.n-.5)*value),spe_margin=float(min(G@w))))
        if previous is not None and abs(value-previous)<1e-10:break
        previous=value
    return dict(status='UNCERTIFIED_NUMERIC',n=s.n,k=s.k,initial=info,
                root_counts=s.final[root],actual_path=menu['actual_path'],
                menu_counts=counts,weights=w.tolist(),query=p.tolist(),trace=trace,
                rows=G.tolist(),policy_subproblems=states)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('source',type=Path)
    ap.add_argument('--count',type=int,default=20);ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args();source=json.loads(a.source.read_text());results=[]
    for j,z in enumerate(source.get('bank',[source['best']])[:a.count]):
        s=Search(z['n'],z['k']);r=optimize(s,np.array(z['weights'],dtype=np.int64));results.append(r)
        print(json.dumps(dict(seed=j,trace=r.get('trace'))),flush=True)
        a.output.write_text(json.dumps(dict(status='EXPLORATORY',results=results),indent=2)+'\n')
        if r.get('trace') and r['trace'][-1]['weak_gap']< -1e-7:break

if __name__=='__main__':main()
