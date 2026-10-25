#!/usr/bin/env python3
"""Exact finite implementation check of all-m price lower-cut construction."""
import sys,json
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from customer_attraction.model import Instance,CustomerType
from customer_attraction.exact import ExactSPESolver

def run():
    rec=[]
    for m in range(2,7):
        cached={}
        for mask in range(1,1<<(m-1)):
            marked=[i for i in range(m-1) if mask>>i&1]
            k=len(marked);r=m-k
            if r not in cached:
                inst=Instance(tuple(f"T{i}" for i in range(m+1)),
                              tuple(CustomerType(frozenset([i]),r if i==0 else 1) for i in range(m)),m)
                cached[r]=(inst,ExactSPESolver(inst))
            inst,solver=cached[r]
            path=tuple(m if i in marked else 0 for i in range(m))
            u=inst.player_payoffs(path)
            mus=tuple(solver.threshold(inst.counts(path[:i])) for i in range(m))
            assert mus==(F(1),)*m
            g=tuple(mus[i]-u[i] for i in range(m-1))
            assert g==tuple(F(i in marked) for i in range(m-1))
            W=inst.welfare(inst.counts(path));O=inst.optimal_welfare()
            assert (W,O,2*W-O)==(r,r+m-1,1-k)
            rec.append({"m":m,"I_one_based":[i+1 for i in marked],"r":r,
                        "W":W,"OPT":O,"B":1-k,"g":[str(x) for x in g]})
    first=None
    for m in range(2,51):
        lam=[F(2*i,m) for i in range(1,m)]
        deficit=sum(max(F(0),1-x) for x in lam)
        if deficit>1 and first is None:
            I=[i for i,x in enumerate(lam) if x<1]
            first={"m":m,"I_one_based":[i+1 for i in I],
                   "lambda_sum":str(sum(lam[i] for i in I)),
                   "required_sum":len(I)-1,
                   "price_slack":str(1-len(I)+sum(lam[i] for i in I))}
    assert first=={"m":7,"I_one_based":[1,2,3],"lambda_sum":"12/7","required_sum":2,"price_slack":"-2/7"}
    # Independently enumerate the subset/positive-part description for the m=5 price domain.
    grid=[F(0),F(1,2),F(1),F(3,2),F(2),F(3)]
    from itertools import product
    checked=0
    for lam in product(grid,repeat=4):
        cuts=all(sum(lam[i] for i in range(4) if mask>>i&1)>=mask.bit_count()-1 for mask in range(1,16))
        pos=sum(max(F(0),1-x) for x in lam)<=1
        assert cuts==pos;checked+=1
    return {"all_checks_passed":True,"scope":"finite exact implementation, general proof is separate",
            "records":rec,"first_ramp_failure_in_checked_range":first,"m5_domain_grid_checks":checked}
if __name__=="__main__":
    out=run();Path(__file__).with_suffix('.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='records'},ensure_ascii=False));print('component_paths',len(out['records']))
