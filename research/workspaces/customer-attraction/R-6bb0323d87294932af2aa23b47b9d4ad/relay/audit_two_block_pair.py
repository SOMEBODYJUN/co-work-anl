"""Independent exact audit of named pair/quadratic candidates on one old SPE.

The full DAG is checked directly. No canonical solver, menu audit, or numerical
optimizer is imported. The general welfare question remains OPEN.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[5]
SOURCE = ROOT / "research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/counterexample/pure_menu_two_block_dag.json"


def solve(A, b):
    L = [list(row) + [rhs] for row, rhs in zip(A, b)]
    n = len(L)
    for c in range(n):
        pivot = next((i for i in range(c, n) if L[i][c]), None)
        if pivot is None:
            return None
        L[c], L[pivot] = L[pivot], L[c]
        q = L[c][c]
        L[c] = [v / q for v in L[c]]
        for i in range(n):
            if i != c:
                q = L[i][c]
                L[i] = [x - q * y for x, y in zip(L[i], L[c])]
    return [row[-1] for row in L]


def simplex_quadratic_max(K):
    """Exact exhaustive support computation; completeness proof in working.md."""
    k = len(K)
    Q = [[(K[a][t] + K[t][a]) / 2 for t in range(k)] for a in range(k)]
    best = F(-1), None, None
    checked = 0
    for size in range(1, k + 1):
        for S in combinations(range(k), size):
            L = [[Q[t][a] for a in S] + [F(-1)] for t in S]
            L += [[F(1)] * size + [F()]]
            sol = solve(L, [F()] * size + [F(1)])
            if sol is None:
                continue
            checked += 1
            if min(sol[:-1]) >= 0 and sol[-1] > best[0]:
                best = sol[-1], S, sol[:-1]
    value, support, probs = best
    p = [F()] * k
    for a, prob in zip(support, probs):
        p[a] = prob
    assert sum(p) == 1
    assert sum((p[t] * p[a] * K[t][a] for t in range(k) for a in range(k)), F()) == value
    return dict(value=str(value), support=support, p=list(map(str, p)), nonsingular_supports=checked)


def main():
    d = json.loads(SOURCE.read_text())
    data, nodes = d["instance"], d["nodes"]
    k, m = len(data["topics"]), data["players"]
    # Explicitly expand positive integer multiplicities into unit customers.
    customers = [frozenset(r["topics"]) for r in data["customers"] for _ in range(r["multiplicity"])]

    def load(q, B):
        return sum(q[a] for a in B)

    def payoff(a, q):
        return sum((F(1, load(q, B)) for B in customers if a in B), F())

    def insertion(t, q):
        return sum((F(1, 1 + load(q, B)) for B in customers if t in B), F())

    seen, stack, comparisons = set(), [d["root"]], 0
    while stack:
        ix = stack.pop()
        if ix in seen:
            continue
        seen.add(ix)
        n = nodes[ix]
        counts, target = n["counts"], n["target"]
        assert len(counts) == len(target) == k
        assert all(type(v) is int and v >= 0 for v in counts + target)
        assert sum(target) == m
        if sum(counts) == m:
            assert counts == target and n["action"] is None and not n["children"]
            continue
        assert sum(counts) < m and len(n["children"]) == k
        assert nodes[n["children"][n["action"]]]["target"] == target
        own = payoff(n["action"], target)
        for a, child_ix in enumerate(n["children"]):
            child = nodes[child_ix]
            expected = list(counts)
            expected[a] += 1
            assert child["counts"] == expected
            assert own >= payoff(a, child["target"])
            comparisons += 1
            stack.append(child_ix)
    assert len(seen) == len(nodes)

    H = [[F() for a in range(k)] for t in range(k)]
    ix, W, path, positions, selected_decompositions = d["root"], F(), [], [], []
    for i in range(m):
        n = nodes[ix]
        b = n["counts"]
        u = payoff(n["action"], n["target"])
        W += u
        path.append(n["action"])
        cols = [nodes[ch]["target"] for ch in n["children"]]
        D = [payoff(a, cols[a]) for a in range(k)]
        K = [[insertion(t, cols[a]) for a in range(k)] for t in range(k)]
        worst = min((2*u-K[t][a]-K[a][t], a, t) for a in range(k) for t in range(a, k))
        positions.append(dict(position=i+1, actual_profit=str(u), min_pair_margin=str(worst[0]), pair=worst[1:]))
        for t in range(k):
            for a in range(k):
                H[t][a] += K[t][a]
                reset, tax = F(), F()
                for B in customers:
                    ax, tx = a in B, t in B
                    ca, ct = load(cols[a], B), load(cols[t], B)
                    if ax and tx:
                        tax += F(1, ca*(ca+1)) + F(1, ct*(ct+1))
                    elif ax != tx:
                        past = load(b, B)
                        na = ca-past-int(ax)
                        nt = ct-past-int(tx)
                        reset += F((int(ax)-int(tx))*(na-nt), (past+1+na)*(past+1+nt))
                slack = 2*u-D[a]-D[t]
                assert 2*u-K[t][a]-K[a][t] == slack+tax-reset
                if (a, t) in [(3, 7), (4, 7)]:
                    selected_decompositions.append(dict(position=i+1,pair=[a,t],slack=str(slack),common_tax=str(tax),signed_reset=str(reset),margin=str(slack+tax-reset)))
        if i == 0:
            rootK = K
            rootcols = cols
            rootb = b
        ix = n["children"][n["action"]]
    global_worst = min((2*W-H[t][a]-H[a][t], a, t) for a in range(k) for t in range(a, k))
    qmax = simplex_quadratic_max(rootK)
    assert W == 32
    assert positions[0]["min_pair_margin"] == "-9/10"
    assert global_worst == (F(299,30),4,7)
    assert F(qmax["value"]) == F(1717,560)
    assert F(13,4)-F(qmax["value"]) == F(103,560)
    root_pair = [[rootK[t][a] for a in [3,7]] for t in [3,7]]
    assert root_pair == [[F(137,60),F(37,10)],[F(37,10),F(137,60)]]
    P = [[F(rootcols[a][t] - (a == t), m-1) for a in range(k)] for t in range(k)]
    testp = [F(a in [2,3,6,7],4) for a in range(k)]
    successorq = [sum((P[t][a]*testp[a] for a in range(k)),F()) for t in range(k)]
    G = sum((testp[t]*rootK[t][a]*testp[a] for t in range(k) for a in range(k)),F())
    derivative = sum(((successorq[t]-testp[t])*(rootK[t][a]+rootK[a][t])*testp[a] for t in range(k) for a in range(k)),F())
    quantitative_rhs = F(2,m-1)*(G-F(13,4))
    assert (G,derivative,derivative-quantitative_rhs) == (F(733,240),F(-1,4),F(-163,840))
    occupation_query = sum((successorq[t]*rootK[t][a]*testp[a] for t in range(k) for a in range(k)),F())
    tail_extra, occupation_reserve = F(), F()
    occupation_IC_reserve = F()
    for B in customers:
        ns = [load(rootcols[a],B)-load(rootb,B)-int(a in B) for a in range(k)]
        fs = [F(1,1+load(rootcols[a],B)) for a in range(k)]
        tail_extra += sum((testp[a]*ns[a]*fs[a] for a in range(k)),F())
        for a in range(k):
            for t in range(k):
                delta_n,delta_a = ns[a]-ns[t],int(a in B)-int(t in B)
                term = F(1,2)*testp[a]*testp[t]*delta_n*(delta_n+delta_a)*fs[a]*fs[t]
                assert term >= 0
                occupation_reserve += term
                if delta_n:
                    term2 = F(1,2)*testp[a]*testp[t]*(delta_n**2-delta_a**2)*fs[a]*fs[t]
                    assert term2 >= 0
                    occupation_IC_reserve += term2
        for a in range(k):
            if a in B:
                same_n_zero_mass = sum((testp[t] for t in range(k) if t not in B and ns[t]==ns[a]),F())
                c = load(rootcols[a],B)
                term3 = testp[a]*(1-same_n_zero_mass)*F(1,c*(c+1))
                assert term3 >= 0
                occupation_IC_reserve += term3
    assert (m-1)*occupation_query-tail_extra == occupation_reserve
    Dmean = sum((testp[a]*payoff(a,rootcols[a]) for a in range(k)),F())
    assert occupation_reserve-(G-Dmean) == occupation_IC_reserve
    assert Dmean+(m-1)*occupation_query-G-tail_extra == occupation_IC_reserve
    out = dict(
        status="LOCAL_PAIR_REJECTED; ROOT_SAME_P_AND_AGGREGATE_PAIR_PASS_THIS_INSTANCE_ONLY",
        source=str(SOURCE.relative_to(ROOT)),dag_nodes=len(nodes),full_SPE_comparisons=comparisons,
        customers=len(customers),players=m,actual_path=path,welfare=str(W),positions=positions,
        root_pair_3_7=[list(map(str,row)) for row in root_pair],
        root_two_point_same_p_max="359/120",root_global_same_p_max=qmax,
        aggregate_min_pair_margin=str(global_worst[0]),aggregate_argmin=global_worst[1:],
        selected_reset_decompositions=selected_decompositions,
        derivative_candidate_test=dict(p=list(map(str,testp)),G=str(G),derivative=str(derivative),quantitative_rhs=str(quantitative_rhs),quantitative_slack=str(derivative-quantitative_rhs),status="QUANTITATIVE_BOUND_FALSE; WEAKER_IMPLICATION_NOT_TESTED_BECAUSE_G_BELOW_U"),
        occupation_query_identity=dict(qKp=str(occupation_query),tail_extra_profit=str(tail_extra),nonnegative_reserve=str(occupation_reserve),Dmean=str(Dmean),extra_IC_reserve=str(occupation_IC_reserve)),
        H=[list(map(str,row)) for row in H],
    )
    Path(__file__).with_suffix(".json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({key:val for key,val in out.items() if key not in ["H","selected_reset_decompositions"]},indent=2))


if __name__ == "__main__":
    main()
