from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

def counts(m,p):
    if p==1: return [(m,)]
    return [(j,)+z for j in range(m+1) for z in counts(m-j,p-1)]

def value(B,p):
    xa=B&1
    t=(B>>1).bit_count()
    polynomial=xa-xa*t+t*(t-1)//2
    closed=t*(t-1)//2 if not xa else (t-1)*(t-2)//2
    assert polynomial==closed
    return polynomial

def main():
    report={"polynomial":[],"separation":[],"payoff_dominance":[]}
    for p in range(4,11):
        vals=[value(B,p) for B in range(1<<p)]
        assert min(vals)==0
        assert vals[0]==0 and vals[1]==1
        assert all(vals[1|(1<<j)]==0 for j in range(1,p))
        assert vals[-1]==(p-2)*(p-3)//2>0
        assert vals[0]+sum(vals[1|(1<<j)] for j in range(1,p))-vals[1]==-1
        report["polynomial"].append({"p":p,"types":len(vals),"minimum":min(vals),"full_type":vals[-1],"separator":-1})
    for p in range(4,9):
        n=0
        minimum=None
        for T in range((1<<p)-1):
            A=T
            while True:
                atom=lambda B: int((B&T)==A)
                sep=atom(0)+sum(atom(1|(1<<j)) for j in range(1,p))-atom(1)
                assert sep>=0
                minimum=sep if minimum is None else min(minimum,sep)
                n+=1
                if A==0: break
                A=(A-1)&T
        report["separation"].append({"p":p,"proper_local_atoms":n,"minimum_separator":minimum})
    for p in range(1,5):
        for m in range(1,6):
            qs=counts(m,p)
            n=0
            for a in range(p):
                occupied=[q for q in qs if q[a]]
                for q,r in product(occupied,repeat=2):
                    dominates=all(F(1,sum(q[j] for j in range(p) if B>>j&1))
                                  >=F(1,sum(r[j] for j in range(p) if B>>j&1))
                                  for B in range(1,1<<p) if B>>a&1)
                    concentration=all(q[b]>=r[b] for b in range(p) if b!=a)
                    assert dominates==concentration
                    n+=1
            report["payoff_dominance"].append({"p":p,"m":m,"ordered_comparisons":n})
    target=Path(__file__).with_name("global_positivity_arity_audit.json")
    target.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"polynomial_cases":len(report["polynomial"]),"separation_atoms":sum(x["proper_local_atoms"] for x in report["separation"]),"dominance_comparisons":sum(x["ordered_comparisons"] for x in report["payoff_dominance"])}))

if __name__=="__main__": main()
