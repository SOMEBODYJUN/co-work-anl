"""Independent exact finite audit; no repository imports. Not a general proof."""
from fractions import Fraction as F
from itertools import product
from math import comb
import json
import argparse
import hashlib
import platform
from pathlib import Path


def path_counts(n, edges):
    # Enumerate actual vertex tuples, independently of the weight recurrence.
    out = [[v for u, v in edges if u == a] for a in range(n)]
    counts = [0] * n
    def walk(a, length):
        counts[length - 1] += 1
        for b in out[a]:
            walk(b, length + 1)
    for a in range(n):
        walk(a, 1)
    return counts


def evaluate(p, x):
    return sum(F(a) * x ** j for j, a in enumerate(p))


def q_interval(counts, steps=64):
    n = counts[0]
    lo, hi = F(1), F(1 + sum(counts))
    def excess(r):
        return r - 1 - sum(F(pk) / r ** (k + 1) for k, pk in enumerate(counts))
    assert excess(lo) < 0 and excess(hi) >= 0
    for _ in range(steps):
        mid = (lo + hi) / 2
        if excess(mid) < 0:
            lo = mid
        else:
            hi = mid
    assert excess(lo) < 0 <= excess(hi)
    return lo, hi


def main():
    zs = [F(101,100), F(21,20), F(11,10), F(5,4), F(3,2), F(2)]
    ds = [1, 2, 5]
    graphs = cases = feasible = endpoint_cases = strict_q_cases = 0
    for n in range(1, 6):
        possible = [(u, v) for u in range(n) for v in range(u+1, n)]
        for bits in product((0,1), repeat=len(possible)):
            edges = [e for b,e in zip(bits,possible) if b]
            counts = path_counts(n, edges)
            assert counts[0] == n
            assert all(pk <= comb(n,k+1) for k,pk in enumerate(counts))
            graphs += 1
            qlo,qhi = q_interval(counts)
            # Every strict q bound below is certified by a rational upper enclosure.
            for z in zs:
                weights = [F(0)] * n
                for u in range(n-1,-1,-1):
                    weights[u] = z-1 + z * sum(weights[v] for a,v in edges if a == u)
                W = sum(weights)
                S = sum(F(pk)*z**k for k,pk in enumerate(counts))
                budget = z*(z-1)*S
                assert W == (z-1)*S
                for u in range(n):
                    outgoing = sum(weights[v] for a,v in edges if a == u)
                    assert weights[u] > outgoing
                    assert 1+weights[u] == z*(1+outgoing)
                for d in ds:
                    cases += 1
                    epsilon = 1/z**d
                    node_constraints = all((1+sum(weights[v] for a,v in edges if a == u))**d <= epsilon*(1+weights[u])**d for u in range(n))
                    root_constraint = W**d <= epsilon
                    assert node_constraints
                    assert root_constraint == (budget <= 1)
                if budget <= 1:
                    feasible += 1
                    assert W < 1
                    B = 1/(z*(z-1))
                    if edges:
                        assert qhi*(qhi-1) < B
                        strict_q_cases += 1
                    else:
                        assert n <= B
                if budget == 1:
                    endpoint_cases += 1
    # Algebraic endpoint: one isolated vertex, z=phi, w=phi-1,
    # epsilon=phi^(-d), with exact arithmetic in Q[phi]/(phi^2-phi-1).
    def phi_mul(x,y):
        a,b=x; c,e=y
        return (a*c+b*e,a*e+b*c+b*e)
    def phi_pow(x,k):
        ans=(F(1),F(0))
        for _ in range(k):
            ans=phi_mul(ans,x)
        return ans
    phi=(F(0),F(1)); phi_minus_one=(F(-1),F(1)); unit=(F(1),F(0))
    assert phi_mul(phi,phi_minus_one)==unit
    algebraic_endpoints=0
    for d in range(1,9):
        # Root equality W^d * z^d = 1. Vertex equality z^d = (1+w)^d.
        assert phi_mul(phi_pow(phi_minus_one,d),phi_pow(phi,d))==unit
        assert phi_pow((phi_minus_one[0]+1,phi_minus_one[1]),d)==phi_pow(phi,d)
        algebraic_endpoints+=1
    polys = 0
    for d in [1,2,3,4]:
        for coeff in product([0,1,3],repeat=d+1):
            if not any(coeff):
                continue
            for a,b in [(F(1,10),F(1)),(F(1),F(1)),(F(3,2),F(5,2)),(F(3),F(2))]:
                pa,pb = evaluate(coeff,a),evaluate(coeff,b)
                assert pa > 0 and pb > 0
                if a<=b:
                    assert pa/pb >= (a/b)**d
                else:
                    assert pa>=pb
                polys += 1
    result = dict(status='passed',forward_labelled_DAGs=graphs,max_vertices=5,monomial_degree_cases=cases,feasible_graph_z_pairs=feasible,rational_budget_endpoint_pairs=endpoint_cases,algebraic_endpoint_degree_checks=algebraic_endpoints,strict_q_upper_certificates=strict_q_cases,nonnegative_polynomial_checks=polys,q_bisection_steps=64,arithmetic='fractions.Fraction',scope='finite corroboration only')
    result.update(python=platform.python_version(), code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), seed=None, inputs={'rational_z':[str(z) for z in zs], 'degrees':ds, 'graphs':'all forward-labelled DAGs on 1..5 vertices', 'q_interval':'64 exact Fraction bisections', 'polynomials':'all nonzero coefficients in {0,1,3}, d=1..4; load pairs explicitly in code', 'endpoint':'one isolated vertex in Q(phi), phi^2=phi+1; d=1..8'})
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    report=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if args.output:
        with args.output.open('x',encoding='utf-8') as f: f.write(report)
    else:
        print(report,end='')

if __name__ == '__main__':
    main()
