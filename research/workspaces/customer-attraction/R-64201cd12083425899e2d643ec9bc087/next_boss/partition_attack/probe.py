"""Attack the separate optimal partitioned-frozen-query sufficient bridge.

Fixed complete two-player policies, positive customer cone. A positive floating
point needs exact recovery and all optimal portfolios before it is a result.
"""
from itertools import product, combinations
from pathlib import Path
import json, random
import numpy as np
from scipy.optimize import linprog

P=6
BITS=np.array(list(product((0,1),repeat=P))[1:],dtype=int)
PAIRS=list(combinations(range(P),2))

def utility(a,b,player):
    return np.divide(BITS[:,player],BITS[:,a]+BITS[:,b],
                     out=np.zeros(len(BITS)),where=(BITS[:,a]+BITS[:,b])!=0)

def cover(a,b):return np.maximum(BITS[:,a],BITS[:,b]).astype(float)

def partition(t,s,first,second):
    c=BITS[:,0]+BITS[:,1]
    x=np.divide(1.,c+1-BITS[:,first])
    y=np.divide(1.,c+1-BITS[:,second])
    return np.where(BITS[:,t] & BITS[:,s],np.minimum(x,y),
                    np.where(BITS[:,t],x,np.where(BITS[:,s],y,0.)))

def solve(reply):
    rows=[]
    for a in range(P):
        for b in range(P):rows.append(utility(a,reply[a],reply[a])-utility(a,b,b))
    for a in range(P):rows.append(utility(0,1,0)-utility(a,reply[a],a))
    actual=cover(0,1);opt=cover(2,3)
    # delta is at most every strict-optimality gap and both assignment gaps.
    extra=[opt-cover(a,b) for a,b in PAIRS if (a,b)!=(2,3)]
    extra += [partition(2,3,0,1)-actual,partition(2,3,1,0)-actual]
    A=[np.r_[-row,0.] for row in rows]+[np.r_[-row,1.] for row in extra]
    result=linprog(np.r_[np.zeros(len(BITS)),-1.],A_ub=A,b_ub=np.zeros(len(A)),
                   A_eq=[np.r_[actual,0.]],b_eq=[1.],
                   bounds=[(0,None)]*len(BITS)+[(None,None)],method='highs')
    return result

def main():
    rng=random.Random(64220261021)
    trials=[(1,4,4,5,5,4)]
    trials += [(1,)+tuple(rng.randrange(P) for _ in range(P-1)) for _ in range(500)]
    best=None
    for j,reply in enumerate(trials):
        r=solve(reply)
        if not r.success:continue
        gap=-r.fun
        if best is None or gap>best['margin']:
            best={'iteration':j,'reply':reply,'margin':gap,'weights':r.x[:-1].tolist()}
            print(json.dumps({k:v for k,v in best.items() if k!='weights'}),flush=True)
        if gap>1e-7:break
    report={'scope':'finite floating fixed-policy attack, not a proof','best':best,'checked':j+1}
    Path(__file__).with_name('probe.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
