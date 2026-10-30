#!/usr/bin/env python3
"""Exact finite checks for the R2 power bridge and affine two-type potential.

No float comparisons, randomness, or external packages. This is evidence only;
the quantifiers over arbitrary real weights are proved in the current account.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement, product
from pathlib import Path
import argparse
import hashlib
import json
import platform
import subprocess


def root(q):
    from math import isqrt
    a, b = isqrt(q.numerator), isqrt(q.denominator)
    assert a*a == q.numerator and b*b == q.denominator
    return F(a, b)


def cost(x, coefficients):
    return sum((a*x**k for k, a in enumerate(coefficients)), F(0))


def ordered(values, coefficients):
    load = F(0)
    out = F(0)
    for v in sorted(values, reverse=True):
        load += v
        out += v*cost(load, coefficients)
    return out


def square_power(values, coefficients):
    return sum(map(root, values), F(0))*cost(sum(values, F(0)), coefficients)


def affine_phi(m, n, a, b, ha, hb, slope=F(1), intercept=F(0)):
    qa, qb = ha/a, hb/b
    if qa > qb:
        return affine_phi(n, m, b, a, hb, ha, slope, intercept)
    d = qb/qa
    k = root(d)
    x, y = m*a, n*b
    if x >= k*y:
        f = (x*x+2*d*x*y+d*y*y)/2
    else:
        f = (k*x*x+2*k*x*y+k*d*y*y)/2
    return slope*(qa*f+(m*ha*a+n*hb*b)/2)+intercept*(m*ha+n*hb)


def path(m, n, a, b, ha, hb, heavy_first):
    weights = [(a, ha)]*m+[(b, hb)]*n
    if not heavy_first:
        weights.reverse()
    load = F(0)
    result = F(0)
    for w, h in weights:
        load += w
        result += h*load
    return result


def compressed(m, n, a, b, ha, hb):
    own = ha*a*m*(m+1)/2+hb*b*n*(n+1)/2
    return own+m*n*hb*a, own+m*n*ha*b


def run():
    counts = {"ordered_edges": 0, "power_edges": 0, "packing_vectors": 0,
              "affine_edges": 0, "literal_paths": 0, "rational_exponents": 0}
    coefficients = [tuple([F(1)]), tuple([F(0)]),
                    tuple([F(0), F(1)]), tuple([F(0), F(0), F(1)]),
                    tuple([F(1), F(2), F(0), F(3)]),
                    tuple([F(0)]*12+[F(1)])]
    choices = [F(1,16), F(1,4), F(1), F(4)]
    for length in range(1,6):
        for weights in combinations_with_replacement(choices, length):
            low, high = min(weights), max(weights)
            scale = root(high)/low
            for mask in range(1 << length):
                users = [w for j,w in enumerate(weights) if mask >> j & 1]
                for i,v in enumerate(weights):
                    if mask >> i & 1:
                        continue
                    after = users+[v]
                    for c in coefficients:
                        target = cost(sum(after, F(0)), c)
                        delta = ordered(after,c)-ordered(users,c)
                        assert low*target <= delta <= v*target
                        assert root(v)*target <= scale*delta <= high/low*root(v)*target
                        counts["ordered_edges"] += 1
                        dp = square_power(after,c)-square_power(users,c)
                        assert dp >= root(v)*target
                        degree = len(c)-1
                        s = sum(users,F(0))/v
                        kernel = 1-(s/(1+s))**degree if degree else F(0)
                        bound = (root(v)+sum(map(root,users),F(0))*kernel)*target
                        assert dp <= bound
                        counts["power_edges"] += 1
    # Packing p=1/2, R=4 has A_R= sqrt(3). Check its squared form.
    for length in range(1,8):
        for weights in combinations_with_replacement(choices,length):
            # Membership is [x,4x), so an exact endpoint has already left.
            density = max(sum(x <= w < 4*x for w in weights) for x in weights)
            left = sum(map(root,weights), F(0))
            assert left*left <= 3*density*sum(weights,F(0))
            counts["packing_vectors"] += 1
    cases = [(F(1),F(1,16),F(1),F(1,4)),
             (F(1),F(1,16),F(1),F(1,16)),
             (F(2),F(1,8),F(8),F(2)),
             (F(1,9),F(9),F(1,3),F(3)),
             (F(1),F(1,16),F(1),F(1))]
    for a,b,ha,hb in cases:
        k = root(max(ha/a,hb/b)/min(ha/a,hb/b))
        for slope,intercept in [(F(1),F(0)),(F(3),F(5)),(F(0),F(2)),(F(0),F(0))]:
            for m,n in product(range(25),repeat=2):
                for dm,dn,w,h in [(1,0,a,ha),(0,1,b,hb)]:
                    load = (m+dm)*a+(n+dn)*b
                    delta = affine_phi(m+dm,n+dn,a,b,ha,hb,slope,intercept)-affine_phi(m,n,a,b,ha,hb,slope,intercept)
                    goal = h*(slope*load+intercept)
                    assert goal <= delta <= k*goal
                    counts["affine_edges"] += 1
        for m,n in product(range(7),repeat=2):
            p1,p2 = compressed(m,n,a,b,ha,hb)
            assert p1 == path(m,n,a,b,ha,hb,True)
            assert p2 == path(m,n,a,b,ha,hb,False)
            if p1 and p2:
                assert p1 <= k*p2 and p2 <= k*p1
            counts["literal_paths"] += 2
    rows = []
    # p=A/B, t=k^(B-A) makes all powers exactly rational.
    for aa,bb in [(0,1),(1,4),(1,2),(2,3),(3,4),(4,5),(9,10)]:
        for base in [2,3,4]:
            t = base**(bb-aa)
            n = base**(bb+2*aa)
            eps = F(1,base**(3*bb))
            h = F(1,base**(3*aa))
            assert h**bb == eps**aa
            hl,lh = compressed(1,n,F(1),eps,F(1),h)
            q = (F(1,t)+F(1,base**(2*bb+aa)))/2
            assert hl == 1+t+q and lh == 1+F(1,t*t)+q
            if t >= 4:
                assert hl > F(t,2)*lh
            counts["rational_exponents"] += 1
            rows.append({"p":str(F(aa,bb)),"base":base,"N":n,
                         "epsilon":str(eps),"ratio":str(hl/lh)})
    # A half-open endpoint audit: [1,4) contains 1 and not 4.
    assert sum(F(1) <= w < F(4) for w in [F(1),F(4)]) == 1
    # Derivative agreement of the affine pieces at x=k*y (D=4).
    for y in [F(0),F(1,8),F(3)]:
        k=F(2);d=k*k;x=k*y
        f1=(x*x+2*d*x*y+d*y*y)/2
        f2=(k*x*x+2*k*x*y+k*d*y*y)/2
        assert f1 == f2
        assert x+d*y == k*(x+y)
        assert d*(x+y) == k*x+k*d*y
    return {"checks":counts,"power_path_rows":rows,
            "limitations":"Exact finite checks only; general proofs and arbitrary real parameters are in the current account. No equilibrium nonexistence inference."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    args = parser.parse_args()
    result = run()
    repo = Path(__file__).resolve().parents[2]
    result.update(schema_version=1,python_version=platform.python_version(),
                  base_commit=subprocess.check_output(["git","rev-parse","HEAD"],cwd=repo,text=True).strip(),
                  arithmetic="fractions.Fraction; no tolerance; deterministic, no seed",
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  replay_command="python3 tests/audits/weighted_power_bridge.py")
    rendered = json.dumps(result,ensure_ascii=False,indent=2)+"\n"
    if args.output:
        Path(args.output).write_text(rendered)
    print(json.dumps(result["checks"],ensure_ascii=False))
