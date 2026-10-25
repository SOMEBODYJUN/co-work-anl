"""Root last-reply feedback chains, genuine histories at every return.

The old point is fixed; this only finds a necessary-condition payment.
"""
import argparse,itertools,json
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from audit_root_D_payment import SOURCE,features,share

def edge_rows(z,q,n,t,final=False):
    root,kae,cae,kh,ch,d,e=z
    out=[root-share(q,q+n+t),share(t,q+n+t)-share(e,q+n+1),
         3*kae-n*cae,kh-t*ch]
    if final:out.append(root-F(t,5))
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--depth',type=int,default=2);args=ap.parse_args();k=args.depth
    pr=json.loads(SOURCE.read_text())['primal'];atoms=pr['atoms']
    states=list(itertools.product(range(4),range(2),repeat=k));rnames=[f'{i}:{s}' for i in range(k) for s in ('rootIC','lastE','AE4intermediates','second3last')]+['final:rootfloor']
    columns=[];groups=[]
    for at in atoms:
        feat=features(at);group=[]
        for st in states:
            q=feat[-2];co=[]
            for i in range(k):
                n,t=st[2*i:2*i+2];co+=edge_rows(feat,q,n,t);q=t
            co.append(feat[0]-F(q,5));group.append(co);columns.append(co)
        groups.append(group)
    matrix=np.asarray(columns,float).T;eq=np.kron(np.eye(len(atoms)),np.ones((1,len(states))))
    masses=[F(int(z['mass_numerator']),int(pr['denominator'])) for z in atoms]
    obj=np.zeros(len(columns)+1);obj[-1]=1
    sol=linprog(obj,A_ub=np.column_stack((-matrix,-np.ones(len(rnames)))),b_ub=np.zeros(len(rnames)),
      A_eq=np.column_stack((eq,np.zeros(len(atoms)))),b_eq=list(map(float,masses)),bounds=[(0,None)]*len(columns)+[(None,None)],method='highs')
    assert sol.success
    weights=[F(round(float(-v)*10**8),10**8) for v in sol.ineqlin.marginals]
    maxima=[max(sum(w*c for w,c in zip(weights,col)) for col in group) for group in groups]
    gap=sum(m*v for m,v in zip(masses,maxima))
    out={'scope':'Genuine root-reply feedback necessary constraints; not half proof or SPE','depth':k,'numeric_violation':float(sol.fun),'exact_gap':str(gap),'gap_float':float(gap),
         'weights':{n:str(w) for n,w in zip(rnames,weights) if w}}
    Path(__file__).with_name(f'root_reply_chain{k}.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
