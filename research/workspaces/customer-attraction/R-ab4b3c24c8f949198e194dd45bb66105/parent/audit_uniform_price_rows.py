#!/usr/bin/env python3
"""Exact definition audit for the universal-price test component; not a general proof."""
import sys,json
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction.model import Instance, CustomerType
from customer_attraction.exact import ExactSPESolver

def run():
    records=[]
    for m in range(2,7):
        # A=0, Q_1,...,Q_(m-1), E=m; only A has two distinct clients.
        inst=Instance(tuple(f"T{i}" for i in range(m+1)),
                      tuple(CustomerType(frozenset([i]),2 if i==0 else 1) for i in range(m)),m)
        solver=ExactSPESolver(inst)
        assert inst.optimal_welfare()==m+1
        for j in range(m-1):
            path=[m]*(m-1)+[1]
            path[j]=0
            u=inst.player_payoffs(path)
            W=inst.welfare(inst.counts(path))
            mus=[solver.threshold(inst.counts(path[:i])) for i in range(m)]
            assert mus==[F(1)]*m
            assert u[-1]==mus[-1]
            g=[mus[i]-u[i] for i in range(m-1)]
            assert g==[F(-1) if i==j else F(1) for i in range(m-1)]
            assert W==3 and 2*W-inst.optimal_welfare()==5-m
            assert sum(2*x for x in g)+(5-m)==m-1
            records.append({"m":m,"j_one_based":j+1,"path":path,
                            "u":[str(x) for x in u],"mu":[str(x) for x in mus],
                            "g":[str(x) for x in g],"B":5-m})
    # The new row excludes an actual point of the old bank domain.
    bad=(F(3),F(0),F(0),F(0))
    assert sum(max(F(0),x-2) for x in bad)<=1
    assert sum(bad)-2*bad[0]<0
    return {"scope":"finite exact implementation audit, not a proof of Q-CAG-HALF",
            "all_checks_passed":True,"records":records,
            "m5_old_domain_point_excluded":[str(x) for x in bad],
            "lambda_two_all_row_slack":"m-1"}
if __name__=="__main__":
    out=run()
    Path(__file__).with_suffix(".json").write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({k:v for k,v in out.items() if k!="records"},ensure_ascii=False))
    print("target_paths_checked",len(out["records"]))
