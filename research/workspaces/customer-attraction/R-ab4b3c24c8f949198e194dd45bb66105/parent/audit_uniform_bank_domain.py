#!/usr/bin/env python3
"""Definition-level bank audit and exact candidate-lambda identities."""
import sys
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations, product
import json
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction.model import Instance, CustomerType
from customer_attraction.exact import ExactSPESolver

def run():
    records=[]
    for m in range(2,6):
        for bits in range(1,1<<(m-1)):
            marked=[i for i in range(m-1) if bits>>i&1]
            k=len(marked); d=m-k
            sizes=[2]*k+[d]+[1]*(d-1)
            labels=tuple(f"b{i}" for i in range(m))
            inst=Instance(labels,tuple(CustomerType(frozenset([i]),s) for i,s in enumerate(sizes)),m)
            solver=ExactSPESolver(inst)
            path=[]; bi=0
            for i in range(m):
                if i in marked: path.append(bi); bi+=1
                else: path.append(k)
            utilities=inst.player_payoffs(path)
            g=[]
            for i in range(m-1):
                mu=solver.threshold(inst.counts(path[:i]))
                g.append(mu-utilities[i])
                assert mu<=1
                assert g[-1]<=(-1 if i in marked else 0)
            last_mu=solver.threshold(inst.counts(path[:-1]))
            assert utilities[-1]==last_mu
            W=inst.welfare(inst.counts(path)); O=inst.optimal_welfare()
            assert (W,O,2*W-O)==(m+k,2*m-1,2*k+1)
            assert tuple(path) in set(solver.ordered_outcomes(inst.counts(path)))
            records.append({"m":m,"marked":marked,"W":W,"OPT":O,
                            "B":2*W-O,"g":[str(x) for x in g]})
    # The positive-part description is independently checked on a finite rational grid.
    grid=[F(0),F(1,2),F(1),F(2),F(5,2),F(3),F(4)]
    nchecks=0
    for lam in product(grid,repeat=4):
        subset_ok=all(sum(lam[i] for i in range(4) if mask>>i&1)<=2*mask.bit_count()+1
                      for mask in range(1,16))
        positive_ok=sum(max(F(0),v-2) for v in lam)<=1
        assert subset_ok==positive_ok
        nchecks+=1
    # Pure account, including positive and negative credible gaps.
    for u in product([F(0),F(1,2),F(3)],repeat=3):
        for mu in product([F(0),F(1),F(5,2)],repeat=2):
            W=sum(u); O=F(7); g=[mu[i]-u[i] for i in range(2)]
            assert 2*W-O+sum(g)==W+sum(mu)+u[-1]-O
            assert 2*W-O+2*sum(g)==2*(sum(mu)+u[-1])-O
    return {"scope":"finite bank and algebra implementation audit, not a proof of Q-CAG-HALF",
            "all_checks_passed":True,"bank_records":records,
            "m5_coefficient_grid_checks":nchecks,
            "lambda_one":"last-BR path version of TB-ANY",
            "lambda_two":"OPT <= 2 sum of credible thresholds along every last-BR path"}
if __name__=="__main__":
    out=run()
    Path(__file__).with_suffix(".json").write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({k:v for k,v in out.items() if k!="bank_records"},ensure_ascii=False))
    print("bank_games",len(out["bank_records"]))
