"""Definition-level exact audit; no discovery LP or game solver is imported."""
from fractions import Fraction
from functools import reduce
from itertools import product
from math import lcm
import json
from pathlib import Path


class Game:
    def __init__(self,m,k):
        self.m,self.k,self.n=m,k,m-k
        self.L=reduce(lcm,range(1,self.n+1),1)
        self.E=tuple(f"E{i}" for i in range(self.n))
        self.U=tuple(f"U{i}" for i in range(m+k))
        self.topics=self.E+self.U
        self.size={t:self.L//(self.n-i) for i,t in enumerate(self.E)}
        self.size.update({t:self.L for t in self.U})

    def action(self,h):
        i=len(h)
        if i<self.n:
            for j,t in enumerate(h):
                if t!=self.E[j]:
                    return t
            return self.E[i]
        return next(t for t in self.U if t not in h)

    def continuation(self,h):
        h=tuple(h)
        while len(h)<self.m:
            h+=(self.action(h),)
        return h

    def utility(self,profile,i):
        t=profile[i]
        return Fraction(self.size[t],profile.count(t))

    def row(self,h,t):
        actual=self.continuation(h)
        deviated=self.continuation(tuple(h)+(t,))
        return self.utility(actual,len(h))-self.utility(deviated,len(h))


def audit_actual(m,k):
    g=Game(m,k)
    actual=g.continuation(())
    rows=[g.row(actual[:i],t) for i in range(m) for t in g.topics]
    assert min(rows)>=0
    W=sum(g.size[t] for t in set(actual))
    H=sum((Fraction(1,j) for j in range(1,g.n+1)),Fraction())
    assert W==g.L*(H+k)
    OPT=m*g.L
    missing=g.row((g.U[k],),g.U[k+1])
    assert missing==Fraction(g.L,g.n)-g.L<0
    return {"m":m,"k":k,"L":g.L,"W":W,"OPT":OPT,
            "ratio":str(Fraction(OPT,W)),"actual_rows":len(rows),
            "minimum_actual_slack":str(min(rows)),
            "missing_offpath_slack":str(missing)}


def audit_all_terminal(m,k):
    g=Game(m,k)
    count=0
    minimum=None
    for depth in range(m-k,m):
        for h in product(g.topics,repeat=depth):
            for t in g.topics:
                slack=g.row(h,t)
                assert slack>=0,(h,t,slack)
                minimum=slack if minimum is None else min(minimum,slack)
                count+=1
    return {"m":m,"k":k,"all_terminal_rows":count,
            "minimum_terminal_slack":str(minimum)}


if __name__=="__main__":
    report={"status":"template obstruction; strategy is not SPE",
            "actual":audit_actual(10,2),
            "terminal":[audit_all_terminal(4,2),audit_all_terminal(5,2)]}
    destination=Path(__file__).with_name("hybrid_obstruction_audit.json")
    destination.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))
