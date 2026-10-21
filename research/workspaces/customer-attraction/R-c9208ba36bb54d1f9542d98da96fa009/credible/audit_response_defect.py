"""Exact response identities and explicit symbolic-family query paths."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json


def kernel(h, t, r, d):
    return (F(r-t, h+t+r) if r != t else F(0)) - F(d, h+t+1)


def identity_audit():
    cases = 0
    for location, t, r, hp in product(("A", "H", "D", "outside"), (0,1), (0,1), range(8)):
        a,p,d = (int(location == x) for x in ("A", "H", "D"))
        ut = F(t, hp+t+r) if t else F(0)
        ur = F(r, hp+t+r) if r else F(0)
        vd = F(d, hp+t+1)
        er = F(r, p+a+1)
        gaps = F(a)-ut+ur-vd+F(d)-er
        delta = kernel(hp,t,r,d)-kernel(p,t,r,d)
        target = F(t) if location in ("A","outside") else F(t,2)
        assert F(3*a,2)-target == gaps + F(a*(1-r),2)-delta
        cases += 1
    return cases


def family(k):
    X = [set((2*i,2*i+1)) for i in range(k)]
    A = [X[i] | {2*k+i} for i in range(k)]
    b,d = 3*k,3*k+1
    B = [X[i] | {b} for i in range(k)]
    D = {b,d}
    actual = X + [D]
    topics = A+[D]
    total = F(0)
    query_rows=[]
    for i in range(k):
        old_others = actual[:i] + actual[i+1:-1]
        for j,T in enumerate(topics):
            if j < k and j >= i:
                # Old actual groups 0,...,i-1 remain; choose all fresh C except j.
                middle = X[:i] + [X[g] for g in range(i,k) if g != j]
                R = B[j]
            else:
                # Old-A or D query: fresh A players achieve the absolute cap 3.
                fresh = list(range(i,k))
                l = k-1 if i < k-1 else i
                middle = X[:i] + [A[g] for g in fresh if g != l]
                R = A[l]
            assert len(middle) == k-1
            terminal = middle + [T,R]
            # Deviating player's terminal value is 2 in every selected query.
            ut = sum((F(1,sum(x in S for S in terminal)) for x in T),F(0))
            assert ut == 2, (k,i,j,ut)
            delta = F(0)
            for x in range(3*k+2):
                p = sum(x in S for S in old_others)
                hp = sum(x in S for S in middle)
                delta += kernel(hp,int(x in T),int(x in R),int(x in D))-kernel(p,int(x in T),int(x in R),int(x in D))
            expected = int(i < k-1 and (j < i or j == k))
            assert delta == expected, (k,i,j,delta,expected)
            query_rows.append({"i":i+1,"query":f"A{j+1}" if j<k else "D","delta":str(delta)})
            total += delta
    W=2*k+2
    opt=3*k+2
    beta=F(8*k*k+11*k+4,4*(k+1)**2)
    defect_coeff=F(2*k+1,2*(k+1)**2)
    budget=F(5*k+4,2*(2*k+1))*W
    assert total == F(k*(k-1),2)
    assert F(opt) <= beta*W+defect_coeff*total
    assert (total > budget) == (k >= 7)
    return {"k":k,"m":k+1,"W":W,"OPT":opt,"delta_total":str(total),"sufficient_budget":str(budget),"budget_violated":total>budget,"queries":query_rows}


if __name__ == "__main__":
    report={"identity_rows":identity_audit(),"family_cases":[family(k) for k in range(2,21)],"scope":"exact finite formula audit; arbitrary-k complete-SPE existence relies on written symbolic gluing"}
    path=Path(__file__).with_suffix(".json")
    if path.exists():
        raise FileExistsError(path)
    path.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"identity_rows":report["identity_rows"],"cases":len(report["family_cases"]),"first_budget_violation_k":7}))
