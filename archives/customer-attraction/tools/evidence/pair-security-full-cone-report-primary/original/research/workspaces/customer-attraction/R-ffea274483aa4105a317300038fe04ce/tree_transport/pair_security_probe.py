"""Discovery-only exact-integer SPE menus and floating static minimax."""
from itertools import product
from math import lcm
from pathlib import Path
import argparse, json, random, time
import numpy as np
from scipy.optimize import linprog

def compositions(n,p):
    if p == 1:
        return [(n,)]
    return [(a,)+b for a in range(n+1) for b in compositions(n-a,p-1)]

class Probe:
    def __init__(self,p,r,k):
        self.p,self.r,self.k=p,r,tuple(k)
        self.m=r+sum(k)
        self.L=lcm(*range(1,self.m+1))
        self.types=[tuple(j for j in range(p) if mask>>j&1)
                    for mask in range(1,1<<p)]
        self.deltas={d:compositions(d,p) for d in range(r+1)}
        self.terminal=[tuple(a+b for a,b in zip(k,z)) for z in self.deltas[r]]
        self.index={q:i for i,q in enumerate(self.terminal)}
        self.forms=np.zeros((len(self.terminal),p,len(self.types)),dtype=np.int64)
        for qi,q in enumerate(self.terminal):
            for j,B in enumerate(self.types):
                den=sum(q[a] for a in B)
                if den:
                    for a in B:
                        if q[a]: self.forms[qi,a,j]=self.L//den
        self.security_indices=[]
        for z in self.deltas[r-1]:
            inds=[]
            for a in range(p):
                q=tuple(k[j]+z[j]+(j==a) for j in range(p))
                inds.append(self.index[q])
            self.security_indices.append(inds)

    def solve(self,w):
        pay=self.forms@np.asarray(w,dtype=np.int64)
        R={z:{i} for i,z in enumerate(self.deltas[self.r])}
        threshold={}
        for d in range(self.r-1,-1,-1):
            for z in self.deltas[d]:
                children=[R[tuple(z[j]+(j==a) for j in range(self.p))]
                          for a in range(self.p)]
                floor=max(min(int(pay[i,a]) for i in children[a])
                          for a in range(self.p))
                threshold[z]=floor
                R[z]=set(i for a in range(self.p) for i in children[a]
                         if pay[i,a]>=floor)
        root=(0,)*self.p
        best=None
        for a,b in product(range(self.p),repeat=2):
            e=tuple(int(j==a) for j in range(self.p))
            ee=tuple(int(j==a)+int(j==b) for j in range(self.p))
            for i in R[root]&R[e]&R[ee]:
                if pay[i,a]>=threshold[root] and pay[i,b]>=threshold[e]:
                    candidate=(int(pay[i,a]+pay[i,b]),a,b,i)
                    if best is None or candidate<best: best=candidate
        assert best is not None
        A=np.asarray([[pay[inds[a],a] for inds in self.security_indices]
                      for a in range(self.p)],dtype=float)/self.L
        result=linprog([0.]*self.p+[-1.],A_ub=np.column_stack([-A.T,np.ones(A.shape[1])]),
                       b_ub=np.zeros(A.shape[1]), A_eq=[[1.]*self.p+[0.]], b_eq=[1.],
                       bounds=[(0,None)]*self.p+[(0,None)],method="highs")
        assert result.success, result.message
        v=result.x[-1]
        score=best[0]/self.L/(2*v) if v>0 else float("inf")
        return score,{"ratio":score,"first_two_sum_numerator":best[0],
                      "denominator":self.L,"first_two_actions":best[1:3],
                      "terminal":self.terminal[best[3]],"v_float":v,
                      "p_float":result.x[:-1].tolist(),"weights":list(map(int,w)),
                      "p":self.p,"r":self.r,"prefix_counts":self.k}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--iterations",type=int,default=4000)
    ap.add_argument("--seed",type=int,default=831014)
    ap.add_argument("--output",default="pair_security_probe_report.json")
    args=ap.parse_args()
    rng=random.Random(args.seed)
    configurations=[(4,5,(0,0,0,0)),(5,5,(0,0,0,0,0)),
                    (5,4,(1,0,0,0,0)),(4,4,(1,0,1,0)),
                    (5,3,(1,1,0,0,0)),(6,3,(0,0,0,0,0,0))]
    report=[]
    start=time.monotonic()
    for p,r,k in configurations:
        probe=Probe(p,r,k)
        best=(float("inf"),None)
        for it in range(args.iterations):
            if it%5 and best[1] is not None:
                w=best[1]["weights"][:]
                for _ in range(rng.randint(1,4)):
                    j=rng.randrange(len(w))
                    w[j]=max(0,min(100,w[j]+rng.choice([-8,-3,-1,1,3,8])))
            else:
                w=[rng.choice([0,0,0,1,1,2,3,5,8,13,21]) for _ in probe.types]
            score,obj=probe.solve(w)
            if score<best[0]-1e-11:
                best=(score,obj)
                print(json.dumps({"config":[p,r,k],"iteration":it,"best":score}),flush=True)
            if score<1-1e-8:
                print("CANDIDATE "+json.dumps(obj),flush=True)
                break
        report.append({"iterations":it+1,"best":best[1]})
        out={"seed":args.seed,"method":"exact integer all-history SPE menus; floating minimax discovery only",
             "elapsed_seconds":time.monotonic()-start,"configurations":report}
        (Path(__file__).parent/args.output).write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"elapsed_seconds":time.monotonic()-start,"best_ratios":[r["best"]["ratio"] for r in report]}),flush=True)

if __name__=="__main__": main()
