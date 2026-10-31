"""Independent exact finite audit of the self-contained background compiler."""
from fractions import Fraction as Q
from itertools import product
from math import factorial
from pathlib import Path
import json


def mask_distribution(b, r):
    if b == 0:
        return {((1 << r) - 1): Q(1)}
    return {mask: Q(b * factorial(mask.bit_count())
                    * factorial(b + r - mask.bit_count() - 1),
                    factorial(b + r)) for mask in range(1 << r)}


def run():
    report = {"model": "unit customers, equal shares; full ordered histories",
              "single_customer_cases": 0, "endpoint_cases": 0,
              "signed_interior_cases": 0, "finite_witness_histories": 0,
              "compiled_profiles": 0, "compiled_complete_strategies": 0,
              "optimal_relative_error_cases": 0}
    for b in range(7):
        for r in range(1, 8):
            dist = mask_distribution(b, r)
            assert sum(dist.values()) == 1
            scale = factorial(b + r)
            assert all((scale * weight).denominator == 1 for weight in dist.values())
            for coverers in range(1 << r):
                c = coverers.bit_count()
                welfare = Q(0)
                utilities = [Q(0) for _ in range(r)]
                for mask, weight in dist.items():
                    retained = mask & coverers
                    k = retained.bit_count()
                    if k:
                        welfare += weight
                        for i in range(r):
                            if retained >> i & 1:
                                utilities[i] += weight / k
                assert welfare == (Q(c, b+c) if c else 0)
                assert utilities == [Q(1,b+c) if coverers >> i & 1 else Q(0)
                                     for i in range(r)]
                assert sum(utilities) == welfare
                report["single_customer_cases"] += 1

    for b in range(1, 8):
        for r in range(2, 10):
            alpha = Q(r*(b+r+1), (r+1)*(b+1)*(b+r))
            beta = Q(-r*b, (r+1)*(b+1)*(b+r))
            assert alpha > 0 and beta < 0
            assert alpha-beta/r == Q(1,b+1)
            assert alpha/r-beta == Q(1,b+r)
            report["endpoint_cases"] += 1
            for j in range(2,r):
                residual = alpha/j-beta/(r+1-j)-Q(1,b+j)
                formula = Q(b*(b+r+1)*(j-1)*(j-r),
                            (b+1)*(b+r)*j*(r+1-j)*(b+j))
                assert residual == formula < 0
                report["signed_interior_cases"] += 1
            epsilon=Q(b*(r-1),b*(r+1)+2*r)
            approx_alpha=Q(2*r,b*(r+1)+2*r)
            errors=[abs((b+j)*approx_alpha/j-1) for j in range(1,r+1)]
            assert max(errors)==epsilon
            assert errors[0]==errors[-1]==epsilon
            report["optimal_relative_error_cases"]+=1

    # Independent definition-level verification of Section 5's full strategy.
    # Topic 0=A contains client 0; topic 1=B contains client 1.
    strategy = {():1, (0,):1, (1,):0}
    def terminal(history):
        while len(history)<2:
            history += (strategy[history],)
        return history
    def background_payoff(path, i):
        client = path[i]
        return Q(1, int(client==0)+path.count(client))
    slacks=[]
    for history in [(),(0,),(1,)]:
        i=len(history)
        selected=strategy[history]
        actual=terminal(history+(selected,))
        row=[]
        for alternative in (0,1):
            branch=terminal(history+(alternative,))
            slack=background_payoff(actual,i)-background_payoff(branch,i)
            assert slack>=0
            row.append(str(slack))
        slacks.append({"history":list(history),"chosen":selected,"slacks":row})
        report["finite_witness_histories"]+=1
    bad_probability = sum(w for mask,w in mask_distribution(1,2).items()
                          if not (mask >> 1 & 1))
    assert bad_probability == Q(1,2)
    report["finite_witness"]={"slacks":slacks,
                              "bad_realization_probability":str(bad_probability)}
    # The deterministic unit compilation of b=1,r=2 has four useful customers.
    compiled = {mask:int(6*w) for mask,w in mask_distribution(1,2).items() if mask}
    assert compiled == {1:1, 2:1, 3:2}
    report["single_A_compilation"]={str(k):v for k,v in compiled.items()}

    # Explicitly expand ordinary unit customers in a mixed-background example,
    # rather than comparing only compressed kernels. Include an uninterested
    # customer, an empty theme (second example), and a zero-customer instance.
    examples = [[({0},1),({1},0),({0,1},2),(set(),1)],
                [({0},2),(set(),0)], []]
    for clients in examples:
        for r in range(1,4):
            scale=factorial(max((b for _,b in clients),default=0)+r)
            coverage=[[set() for _ in range(2)] for _ in range(r)]
            count=0
            for themes,b in clients:
                for mask,weight in mask_distribution(b,r).items():
                    copies=int(scale*weight)
                    if not mask: continue
                    for _ in range(copies):
                        for i in range(r):
                            for a in themes:
                                if mask>>i&1: coverage[i][a].add(count)
                        count+=1
            orig_payoffs={}; compiled_payoffs={}
            for path in product(range(2),repeat=r):
                orig=[Q(0) for _ in range(r)]
                for themes,b in clients:
                    attracted=[i for i,a in enumerate(path) if a in themes]
                    for i in attracted: orig[i]+=Q(1,b+len(attracted))
                actual=[Q(0) for _ in range(r)]
                welfare=0
                for x in range(count):
                    attracted=[i for i,a in enumerate(path) if x in coverage[i][a]]
                    if attracted: welfare+=1
                    for i in attracted: actual[i]+=Q(1,len(attracted))
                assert actual==[scale*u for u in orig]
                assert welfare==scale*sum(orig)
                orig_payoffs[path]=orig; compiled_payoffs[path]=actual
                report["compiled_profiles"]+=1
            assert max(sum(u) for u in compiled_payoffs.values()) == scale*max(
                sum(u) for u in orig_payoffs.values())
            histories=[h for depth in range(r) for h in product(range(2),repeat=depth)]
            def valid_strategy(actions,payoffs):
                def follow(history):
                    while len(history)<r: history+=(actions[history],)
                    return history
                for h in histories:
                    own=len(h)
                    own_u=payoffs[follow(h+(actions[h],))][own]
                    if any(payoffs[follow(h+(a,))][own]>own_u for a in (0,1)):
                        return False
                return True
            for choices in product(range(2),repeat=len(histories)):
                actions=dict(zip(histories,choices))
                assert valid_strategy(actions,orig_payoffs)==valid_strategy(actions,compiled_payoffs)
                report["compiled_complete_strategies"]+=1
    report["status"]="all finite exact checks passed; no general half-bound claimed"
    return report


if __name__ == "__main__":
    output=run()
    Path(__file__).with_suffix(".json").write_text(json.dumps(output,indent=2)+"\n")
    print(json.dumps(output,indent=2))
