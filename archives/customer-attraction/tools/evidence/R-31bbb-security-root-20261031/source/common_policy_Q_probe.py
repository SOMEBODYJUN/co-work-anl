"""Test a stronger linear common-Q template on full fixed-policy cones.

For every pure query a, require c - n E_Q beta(a) in the SPE-cone dual.
One Q must work for all queries and every mass vector in this policy cone.
Feasibility is numerical; failure is not a true aggregate-security counterexample.
"""
import argparse
import itertools
import json
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

sys.path.insert(0,str(Path(__file__).resolve().parent))
from background_pair_probe import policy_cone,representation


def test(actions,n,k):
    M,sunk,R,scale=representation(n,k,[0]*k)
    def term(h):
        while len(h)<n:h+=(actions[h],)
        return h
    def util(a,z):return M[a]/np.maximum(sum(M[b] for b in z),1)
    G=np.unique(np.array([util(a,term(h))-util(b,term(h+(b,)))
                         for h,a in actions.items() for b in range(k)]),axis=0)
    z=term(());c=(sum(M[a] for a in z)>0).astype(float)
    bs=len(R);gs=len(G);types=len(c)
    # m E_Q beta + G^T lambda_a <= coverage, with nonnegative variables.
    rr=[];cc=[];vv=[]
    for a in range(k):
        qblock=n*R*M[a]
        i,j=np.nonzero(qblock)
        rr.extend((a*types+j).tolist());cc.extend(i.tolist());vv.extend(qblock[i,j].tolist())
        i,j=np.nonzero(G)
        rr.extend((a*types+j).tolist());cc.extend((bs+a*gs+i).tolist());vv.extend(G[i,j].tolist())
    A=coo_matrix((vv,(rr,cc)),shape=(k*types,bs+k*gs)).tocsr()
    eq=coo_matrix((np.ones(bs),(np.zeros(bs,int),np.arange(bs))),shape=(1,bs+k*gs)).tocsr()
    out=linprog(np.zeros(bs+k*gs),A_ub=A,b_ub=np.tile(c,k),
                A_eq=eq,b_eq=[1.],bounds=(0,None),method='highs')
    rec={'n':n,'k':k,'status':out.status,'message':out.message,'rows':gs,'backgrounds':bs}
    if out.success:rec['Q']=out.x[:bs].tolist()
    return rec


def main():
    par=argparse.ArgumentParser();par.add_argument('--trials',type=int,default=30)
    par.add_argument('--output',type=Path,required=True);args=par.parse_args()
    cases=[]
    root=Path('evidence/certificates/customer_attraction')
    for name in ['aggregate_theta_failure','individual_security_failure','local_security_increment','worst_pne_welfare_failure','worst_cce_welfare_failure']:
        d=json.loads((root/(name+'.json')).read_text());rows=d.get('strategy',d)['actions']
        actions={tuple(x['history']):x['action'] for x in rows}
        n=1+max(map(len,actions));k=1+max(max(h+(a,)) for h,a in actions.items())
        rec=test(actions,n,k)|{'name':name};cases.append(rec)
        print(json.dumps({x:rec[x] for x in ['name','status','rows','backgrounds']}),flush=True)
        args.output.write_text(json.dumps({'scope':'numerical template screen only','cases':cases},indent=2)+'\n')
    import random
    rng=random.Random(31010229)
    for trial in range(args.trials):
        n,k=rng.choice([(3,5),(3,6),(4,5)])
        M,sunk,R,scale=representation(n,k,[0]*k)
        w=np.array([rng.randrange(1,16) if rng.random()<.4 else 0 for _ in range((1<<k)-1)],int)
        actions,*_=policy_cone(n,k,M,sunk,scale,w,rng)
        rec=test(actions,n,k)|{'name':'random_'+str(trial)};cases.append(rec)
        print(json.dumps({x:rec[x] for x in ['name','status','rows','backgrounds']}),flush=True)
        args.output.write_text(json.dumps({'scope':'numerical template screen only','cases':cases},indent=2)+'\n')
        if rec['status']==2:
            break


if __name__=='__main__':main()
