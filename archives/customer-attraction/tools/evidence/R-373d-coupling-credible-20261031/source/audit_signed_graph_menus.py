"""Definition-level Fraction audit; does not import the canonical solver."""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb
from random import Random
import json
from pathlib import Path


def cut_cost(bits, edges, weights):
    return sum((w for (r, s, sign), w in zip(edges, weights)
                if (bits[r] != bits[s]) == (sign == 'D')), F(0))


def audit_case(states, backgrounds, edges, multipliers):
    L, q = len(states), len(states[0])
    K = [sum(z for z, f in row) for row in states]
    a = [F(1, b + 1) for b in backgrounds]
    g = [F(1, (b + 1) * (b + 2)) for b in backgrounds]
    A = [sum((F(f, b + z + 1) for z, f in row), F(0))
         for row, b in zip(states, backgrounds)]
    weights = [lam * g[r] for (r, s, sign), lam in zip(edges, multipliers)]
    tau = min(cut_cost(bits, edges, weights) for bits in product((0, 1), repeat=L))
    raw = env = deficit = offset = F(0)
    for (r, s, sign), lam, w in zip(edges, multipliers, weights):
        C = sum(states[r][i][0] * states[s][i][0] for i in range(q))
        h = sum(states[r][i][0] != states[s][i][0] for i in range(q))
        if sign == 'D':
            direct = sum((F(states[r][i][1], backgrounds[r] + states[r][i][0] + 1)
                          - F(states[s][i][0], backgrounds[r] + states[r][i][0] + 1)
                          for i in range(q)), F(0))
            formula = A[r] - a[r] * K[s] + g[r] * C
            E = A[r] - a[r] * K[s] + g[r] * min(K[r], K[s])
            delta = F(h - abs(K[r] - K[s]), 2)
            off = abs(K[r] - K[s])
        else:
            direct = sum((F(states[r][i][1], backgrounds[r] + states[r][i][0] + 1)
                          - F(states[s][j][0], backgrounds[r] + states[r][i][0] + 1)
                          for i in range(q) for j in range(q) if i != j), F(0))
            formula = (q - 1) * A[r] - (q - 1) * a[r] * K[s] + g[r] * (K[r] * K[s] - C)
            E = ((q - 1) * A[r] - (q - 1) * a[r] * K[s]
                 + g[r] * (K[r] * K[s] - max(0, K[r] + K[s] - q)))
            delta = F(q - h - abs(q - K[r] - K[s]), 2)
            off = abs(q - K[r] - K[s])
        assert direct == formula
        assert delta >= 0 and lam * (E - direct) == w * delta
        raw += lam * direct
        env += lam * E
        deficit += w * delta
        offset += w * off
    columns = sum((cut_cost(tuple(states[r][i][0] for r in range(L)), edges, weights)
                   for i in range(q)), F(0))
    assert deficit == (columns - offset) / 2
    xi = max(F(0), (q * tau - offset) / 2)
    assert deficit >= xi and raw <= env - xi
    return raw, env, deficit, tau


def main():
    rng = Random(373803)
    random_cases = 0
    for _ in range(1200):
        L, q = rng.randint(2, 6), rng.randint(1, 6)
        states = [[(rng.randrange(2), rng.randrange(2)) for i in range(q)] for r in range(L)]
        b = [rng.randrange(6) for r in range(L)]
        edges = [(r, s, rng.choice('DO')) for r, s in combinations(range(L), 2)
                 if rng.randrange(3)]
        lam = [F(rng.randrange(6), rng.randint(1, 5)) for e in edges]
        audit_case(states, b, edges, lam)
        random_cases += 1
    sharp_half_cases = 0
    for L in range(2, 7):
        for q in (2, 4, 6):
            for _ in range(10):
                edges = [(r, s, rng.choice('DO')) for r, s in combinations(range(L), 2)]
                b = [rng.randrange(4) for r in range(L)]
                lam = [F(rng.randrange(1, 5), rng.randrange(1, 5)) for e in edges]
                weights = [v / ((b[r]+1)*(b[r]+2)) for (r,s,sgn),v in zip(edges,lam)]
                bits = min(product((0, 1), repeat=L), key=lambda v: cut_cost(v, edges, weights))
                states = [[(bits[r], rng.randrange(2)) for _ in range(q//2)]
                          + [(1-bits[r], rng.randrange(2)) for _ in range(q//2)] for r in range(L)]
                raw, env, deficit, tau = audit_case(states, b, edges, lam)
                assert deficit == q * tau / 2
                sharp_half_cases += 1
    clique_cases = 0
    for q in range(1, 7):
        for L in range(2, 7):
            for k in range(q+1):
                rows = [frozenset((r*k+j) % q for j in range(k)) for r in range(L)]
                states = [[(int(i in rows[r]), 0) for i in range(q)] for r in range(L)]
                edges = [(r,s,'O') for r,s in combinations(range(L),2)]
                raw, env, deficit, tau = audit_case(states,[0]*L,edges,[F(2)]*len(edges))
                t, rem = divmod(L*k,q)
                value = q*comb(t,2)+rem*t-comb(L,2)*max(0,2*k-q)
                assert deficit == value
                clique_cases += 1
    edges = [(r,s,'O') for r,s in combinations(range(5),2)]
    states = [[(1,1),(0,0)] for r in range(2)] + [[(0,0),(1,1)] for r in range(3)]
    raw, env, deficit, tau = audit_case(states,[0]*5,edges,[F(1)]*10)
    assert (raw,env,deficit,tau)==(F(-2),F(0),F(2),F(2))
    # A fractional triangle packing attains 5/3: ten triangles, each weight 1/3.
    # Every odd cycle uses at least 3 edges, giving the matching upper bound.
    cycle_bound=F(10,3)*F(1,2)
    assert cycle_bound==F(5,3)<deficit
    report={"status":"passed","random_definition_cases":random_cases,
            "half_density_sharp_cases":sharp_half_cases,"clique_sharp_cases":clique_cases,
            "K5":{"joint_deficit":str(deficit),"best_scalar_odd_cycle_packing":str(cycle_bound)},
            "scope":"Audits formulas, not a general half proof or a SPE realization."}
    print(json.dumps(report,ensure_ascii=False,indent=2))
    out=Path(__file__).with_name('signed_graph_menu_audit.json')
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':
    main()
