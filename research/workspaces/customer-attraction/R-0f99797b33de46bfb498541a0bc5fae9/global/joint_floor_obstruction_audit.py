"""Exact audit of the analytic copy-floor obstruction; no equilibrium claim."""
from fractions import Fraction
from itertools import product
import argparse
import json
from pathlib import Path


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    m,k=5,6
    rows=[]
    for r in range(2,m+1):
        checked=0;best=None
        for d in range(1,r):
            lhs=Fraction(1,r-d)-Fraction(1,r)
            rhs=Fraction(d,r*(r-1))
            assert lhs==Fraction(d,r*(r-d)) and lhs>=rhs
        for ds in product(range(r),repeat=k):
            if sum(ds)<r-1:continue
            value=sum((Fraction(1,r-d) for d in ds),Fraction(0))
            assert value>=Fraction(k+1,r)
            if best is None or value<best:best=value
            checked+=1
        assert best==Fraction(k+1,r)
        # q_l=T\{x_l}+{z}: every remaining player receives (k+1)/r.
        follower=Fraction(r-1,r-1)+Fraction(k-r+1,r)
        assert follower==best<k
        fresh_uncovered_lower=r*k-1
        assert fresh_uncovered_lower>=k
        rows.append({"remaining":r,"deficit_vectors":checked,"minimum":str(best),
                     "fresh_clients_lower":fresh_uncovered_lower,"last_deviation_value":k})
    harmonic=sum((Fraction(1,r) for r in range(1,m+1)),Fraction(0))
    budget=(k+1)*harmonic-1
    assert budget==Fraction(899,60) and budget<Fraction(m*k,2)
    asymptotic_samples=[]
    for players in (5,10,20,50,100):
        petal=players-1
        h=sum((Fraction(1,r) for r in range(1,players+1)),Fraction(0))
        b=(petal+1)*h-1
        asymptotic_samples.append({"players":players,"theme_size":petal,
                                   "optimum":players*petal,"budget":str(b),
                                   "optimum_over_budget":str(Fraction(players*petal,b))})
    result={"status":"mechanism_obstruction_only","players":m,"theme_size":k,
            "customers":(m+1)*k,"optimum":m*k,"harmonic":str(harmonic),
            "budget":str(budget),"half_shortfall":str(Fraction(m*k,2)-budget),
            "deficit_checks":rows,"growing_population_samples":asymptotic_samples}
    if args.output:
        if args.output.exists():raise FileExistsError(args.output)
        args.output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__=="__main__":main()
