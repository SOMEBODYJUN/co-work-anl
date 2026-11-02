"""Extract sparse numerical dual in one arbitrary full strategy cone."""
import json,math,random
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from customer_attraction.certificate import StrategyCertificate
from leaf_support_probe import bg_support
OUT=Path(__file__).resolve().parent
rng=random.Random(9114)
n,k=4,4
M=np.array([[(mask>>a)&1 for mask in range(1,1<<k)] for a in range(k)])
actions={};rows=[];labels=[]
sc=math.lcm(*range(1,n+1))
def vec(a,q):return M[a]*(sc//np.maximum(np.array(q)@M,1))
def walk(h):
 if len(h)==n:return tuple(h.count(a) for a in range(k))
 a=rng.randrange(k);actions[h]=a
 children=[walk(h+(b,)) for b in range(k)]
 for b in range(k):
  if b!=a:rows.append((vec(a,children[a])-vec(b,children[b]))/sc);labels.append((h,b))
 return children[a]
q=walk(());G=np.array(rows);c=(np.array(q)@M>0).astype(float)
cert=StrategyCertificate(actions,q);bgs,leaves=bg_support(cert,n,k)
p=np.ones(k)/k
beta=(p@M)/(1+np.array(bgs)@M)
res=linprog(np.r_[np.ones(len(G)),np.zeros(len(bgs))],A_ub=np.column_stack([G.T,n*beta.T]),b_ub=c,A_eq=np.array([np.r_[np.zeros(len(G)),np.ones(len(bgs))]]),b_eq=[1.],bounds=(0,None),method='highs')
print(res.message)
if res.success:
 record=dict(n=n,k=k,p=p.tolist(),on_path=q,actions={','.join(map(str,h)):a for h,a in actions.items()},lambda_rows=[dict(h=h,b=b,l=float(l)) for (h,b),l in zip(labels,res.x[:len(G)]) if l>1e-8],Q=[dict(background=b,probability=float(v)) for b,v in zip(bgs,res.x[len(G):]) if v>1e-8],remainder=(c-np.column_stack([G.T,n*beta.T])@res.x).tolist())
 (OUT/'one_leaf_dual.json').write_text(json.dumps(record,indent=2)+'\n')
 print(json.dumps({x:record[x] for x in ['n','k','on_path','lambda_rows','Q']},indent=2))
