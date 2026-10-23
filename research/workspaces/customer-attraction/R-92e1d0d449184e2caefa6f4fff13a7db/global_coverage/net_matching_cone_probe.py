"""Attack the arbitrary-m net real-deviation matching bridge in full SPE cones.

For a specified complete strategy, all nonempty topic-interest types are LP
variables.  Require the strategy to be SPE, the comparison portfolio to be
optimal, W=1, and maximize min_pi[OPT-W-sum_i V_(i,pi(i))].  Only a positive
exactly rechecked solution would refute the bridge.  Nonpositive numerical
answers are diagnostics, never a proof.
"""
import json
from fractions import Fraction
from itertools import combinations, permutations
from pathlib import Path

import numpy as np
from scipy.optimize import linprog


def finish(actions, prefix, m):
    history = prefix
    while len(history) < m:
        history = history + (actions[history],)
    return history


def payoff_row(signatures, path, i):
    return tuple(Fraction(1, sum(a in s for a in path)) if path[i] in s else Fraction(0)
                 for s in signatures)


def subtract(left, right):
    return tuple(a-b for a,b in zip(left,right))


def solve_certificate(name):
    obj = json.loads(Path(name).read_text())
    obj = obj.get("strategy", obj)
    actions = {tuple(x["history"]): x["action"] for x in obj["actions"]}
    m = 1 + max(map(len, actions))
    k = max(actions.values()) + 1
    signatures = tuple(frozenset(s) for size in range(1,k+1)
                       for s in combinations(range(k),size))
    n = len(signatures)
    actual = finish(actions, (), m)
    cover = tuple(Fraction(bool(set(actual) & s)) for s in signatures)
    gamma = []
    for history, a in actions.items():
        selected = finish(actions, history, m)
        own = payoff_row(signatures, selected, len(history))
        for b in range(k):
            if b != a:
                branch = finish(actions, history + (b,), m)
                gamma.append(subtract(own, payoff_row(signatures, branch, len(history))))
    all_comparisons = tuple(combinations(range(k), min(k,m)))
    cover_rows = [tuple(Fraction(bool(set(t)&s)) for s in signatures) for t in all_comparisons]
    results = []
    for comparison, optrow in zip(all_comparisons, cover_rows):
        portfolio = comparison + (comparison[0],)*(m-len(comparison))
        value = [[payoff_row(signatures, finish(actions, actual[:i]+(t,), m),i)
                  for t in portfolio] for i in range(m)]
        constraints = [tuple(-x for x in row)+(Fraction(0),) for row in gamma]
        constraints += [subtract(row,optrow)+(Fraction(0),) for row in cover_rows]
        net = subtract(optrow, cover)
        matching = []
        for perm in set(permutations(range(m))):
            deficit = tuple(net[j] - sum(value[i][perm[i]][j] for i in range(m))
                            for j in range(n))
            matching.append(deficit)
            constraints.append(tuple(-x for x in deficit)+(Fraction(1),))
        result = linprog([0]*n+[-1], A_ub=np.array(constraints,dtype=float),
                         b_ub=np.zeros(len(constraints)),
                         A_eq=np.array([cover+(Fraction(0),)],dtype=float),b_eq=[1],
                         bounds=[(0,None)]*n+[(None,None)],method="highs")
        report = {"comparison":portfolio,"status":result.message}
        if result.success:
            w = tuple(Fraction(float(x)).limit_denominator(1000000) for x in result.x[:n])
            deficit = min(sum(a*b for a,b in zip(row,w)) for row in matching)
            report["deficit"] = str(deficit)
            report["feasible_rational"] = (
                sum(a*b for a,b in zip(cover,w)) == 1 and
                all(sum(a*b for a,b in zip(row,w)) >= 0 for row in gamma) and
                all(sum(a*b for a,b in zip(subtract(optrow,row),w)) >= 0
                    for row in cover_rows))
            if deficit > 0:
                report["support"] = [{"topics":sorted(s),"multiplicity":str(x)}
                                     for s,x in zip(signatures,w) if x]
        results.append(report)
    return {"certificate":name,"players":m,"topics":k,"actual":actual,"results":results}


def main():
    names = ["coverage_opportunity_failure", "collision_free_occupancy",
             "eight_cce_welfare_gap", "worst_cce_welfare_failure",
             "prefix_balance_failure", "root_tax_failure", "individual_security_failure"]
    for name in names:
        path = "evidence/certificates/customer_attraction/"+name+".json"
        try:
            print(json.dumps(solve_certificate(path)), flush=True)
        except (KeyError, ValueError) as exc:
            print(json.dumps({"certificate":path,"error":str(exc)}),flush=True)


if __name__ == "__main__":
    main()
