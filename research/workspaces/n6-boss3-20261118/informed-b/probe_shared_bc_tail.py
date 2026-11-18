"""Shared-catalogue necessary LP for B/C tails with both successors extra.

Each of s forced new-anchor branches uses one specified ordered pair among
four fixed extra coverages F0..F3, all on one shared client membership space.
The fifth extra E is already present t times in the common prefix. This is a
necessary relaxation, not complete SPE synthesis. Branches in which A or Y
is another anchor are excluded and remain a separate proof obligation.
"""
from itertools import product,combinations_with_replacement
from fractions import Fraction as F
import argparse,json,random,time
import numpy as np
from scipy.optimize import linprog


def model(s,t):
    # Extra membership bits are E,F0,F1,F2,F3. All old-anchor background outside
    # the new anchors is discarded, weakening the constraints conservatively.
    types=[(b,bits) for b in range(s+1) for bits in product((0,1),repeat=5)
           if b<s or any(bits)]
    V=len(types)
    def row(fn):return np.array([float(fn(b,v)) for b,v in types]+[0.0])
    def has(label,b,v):
        return int(b==label) if isinstance(label,int) else v[label[1]+1] if label[0]=='F' else v[0]
    def utility(j,a,y):
        return row(lambda b,v:F(has(a,b,v),t*v[0]+int(b==j)+has(a,b,v)+has(y,b,v)) if has(a,b,v) else 0)
    def last_query(j,a,label):
        return row(lambda b,v:F(has(label,b,v),t*v[0]+int(b==j)+has(a,b,v)+1) if has(label,b,v) else 0)
    def penult_query(j,label):
        return row(lambda b,v:F(has(label,b,v),t*v[0]+int(b==j)+2) if has(label,b,v) else 0)
    eq=[row(lambda b,v:b==j) for j in range(s)]
    ub=[row(lambda b,v:v[k]) for k in range(5)]
    br={}
    E=[row(lambda b,v:v[0]*(b==j)) for j in range(s)]
    c=F(t,t+1)
    for j in range(s):
        for a,y in product(range(4),repeat=2):
            if a==y:continue
            A=('F',a);Y=('F',y)
            UA=utility(j,A,Y); UY=utility(j,Y,A)
            UT=row(lambda b,v:F(1,t*v[0]+1+has(A,b,v)+has(Y,b,v)) if b==j else 0)
            force=UT.copy();force[-1]=-1
            rows=[force];rhs=[0.0];names=['force-payoff-at-most-gamma']
            # Genuine last player can query every shared legal new anchor or extra.
            for label in list(range(s))+[('E',0)]+[('F',k) for k in range(4)]:
                rows.append(last_query(j,A,label)-UY);rhs.append(0.0);names.append('last-query-'+str(label))
            # Direct worst-last denominator guarantee at genuine penultimate node.
            for label in list(range(s))+[('E',0)]+[('F',k) for k in range(4)]:
                rows.append(penult_query(j,label)-UA);rhs.append(0.0);names.append('penultimate-H-'+str(label))
            # Strong per-anchor real last-deficit lower bounds for penultimate.
            for k in range(s):
                if k==j:continue
                r=-UA-c*E[k]-c/(s-2)*sum((E[l] for l in range(s) if l!=j and l!=k),np.zeros(V+1))
                rows.append(r);rhs.append(-1.0);names.append('penultimate-true-anchor-deficit-'+str(k))
            br[j,a,y]=(rows,rhs,names,UT,UA,UY)
    return types,eq,ub,br


def run(s,t,rounds,seed):
    types,eq,ub,br=model(s,t)
    pairs=[(a,y) for a,y in product(range(4),repeat=2) if a!=y]
    rng=random.Random(seed)
    # Branch permutation symmetry lets one use pair multisets.
    patterns=list(combinations_with_replacement(range(12),s))
    if rounds and rounds<len(patterns):patterns=rng.sample(patterns,rounds)
    best=None; started=time.perf_counter(); solved=0
    for pattern in patterns:
        rows=list(ub);rhs=[1.0]*5;names=['extra-size-'+str(k) for k in range(5)]
        for j,k in enumerate(pattern):
            a,y=pairs[k];rs,bs,ns,*_=br[j,a,y]
            rows.extend(rs);rhs.extend(bs);names.extend('branch'+str(j)+'-'+n for n in ns)
        objective=np.zeros(len(types)+1);objective[-1]=1
        z=linprog(objective,A_ub=np.array(rows),b_ub=np.array(rhs),A_eq=np.array(eq),b_eq=np.ones(s),bounds=[(0,None)]*(len(types)+1),method='highs')
        solved+=1
        if z.success and (best is None or z.fun<best['gamma']-1e-10):
            best={'gamma':z.fun,'pattern':[pairs[k] for k in pattern],
                'atoms':[{'block':b,'bits':list(v),'mass':float(x)} for (b,v),x in zip(types,z.x[:-1]) if x>1e-8],
                'active_rows':[n for n,x in zip(names,z.ineqlin.residual) if x<1e-8]}
    return {'s':s,'t':t,'patterns_solved':solved,'seed':seed,'best':best,'elapsed_seconds':time.perf_counter()-started,
        'scope':'Shared-catalogue necessary relaxation with A_j,Y_j both among four unused extras; excludes successor-anchor cases and does not certify full SPE.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--rounds',type=int,default=100);p.add_argument('--seed',type=int,default=11803);args=p.parse_args()
    print(json.dumps([run(5,2,args.rounds,args.seed),run(4,1,args.rounds,args.seed)],indent=2))
