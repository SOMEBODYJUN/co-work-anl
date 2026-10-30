#!/usr/bin/env python3
"""有序尾部冻结的独立精确审计；不导入作者实现或第三方库。

默认打印 JSON；--output NEW_PATH 使用 x 模式创建，不覆盖现有证据。
有限有理计算只检查所记录输入，不代替任意正实权的一般证明。
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
from math import comb
from pathlib import Path
import platform
from random import Random
import sys
import json

VERSION = "1.0"
SEED = 95471


def enc(value):
    if isinstance(value, Q):
        return str(value)
    if isinstance(value, dict):
        return {str(k): enc(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [enc(x) for x in value]
    return value


def require(ok, context):
    if not ok:
        raise AssertionError(context)


def powerset(ids):
    for mask in range(1 << len(ids)):
        yield tuple(ids[k] for k in range(len(ids)) if mask >> k & 1)


def latency(coeff, load):
    return sum((a * load ** k for k, a in enumerate(coeff)), Q(0))


def phi_direct(ids, i, weights, coeff, base=Q(0)):
    """Uniform-subset definition; no call to the potential routine."""
    from math import factorial
    others = tuple(j for j in ids if j != i)
    n = len(ids)
    ans = Q(0)
    for T in powerset(others):
        z = sum((weights[j] for j in T), Q(0))
        wi = weights[i]
        f_after = (z + wi) * latency(coeff, base + z + wi)
        f_before = z * latency(coeff, base + z)
        ans += Q(factorial(len(T)) * factorial(n - len(T) - 1), factorial(n)) * (f_after - f_before)
    return ans


def potential(ids, weights, coeff, base):
    n = len(ids)
    ans = Q(0)
    for T in powerset(ids):
        if T:
            z = sum((weights[i] for i in T), Q(0))
            ans += z * latency(coeff, base + z) / (len(T) * comb(n, len(T)))
    return ans


def check_shares():
    grid = (Q(1, 2), Q(1), Q(3))
    cases = marginal_checks = 0
    for n in range(1, 6):
        ids = tuple(range(n))
        for weights in product(grid, repeat=n):
            for degree in range(8):
                coeff = (Q(0),) * degree + (Q(1),)
                phis = [phi_direct(ids, i, weights, coeff) for i in ids]
                W = sum(weights, Q(0)); c = latency(coeff, W)
                require(sum(phis, Q(0)) == W * c, ("efficiency", weights, degree))
                for i in ids:
                    require(min(weights) * c <= phis[i] <= max(weights) * c, ("envelope", weights, degree, i))
                    without = tuple(j for j in ids if j != i)
                    require(potential(ids, weights, coeff, Q(0)) - potential(without, weights, coeff, Q(0)) == phis[i], ("marginal", weights, degree, i))
                    marginal_checks += 1
                    for j in ids:
                        if weights[i] <= weights[j]:
                            require(phis[i] <= phis[j], ("share_order", weights, degree, i, j))
                            require(phis[i] / weights[i] >= phis[j] / weights[j], ("normalized_order", weights, degree, i, j))
                cases += 1
    return {"cases": cases, "marginal_checks": marginal_checks,
            "inputs": {"weight_grid": grid, "lengths": list(range(1, 6)),
                       "latency_degrees": list(range(8)), "enumeration": "all ordered Cartesian products"}}


def game_cost(i, s, weights, coeffs):
    return sum((latency(coeffs[e], sum((weights[k] for k in range(len(s)) if e in s[k]), Q(0))) for e in s[i]), Q(0))


def stage_data(game, j, partial):
    weights, families, coeffs, groups, d = game
    E = range(len(coeffs)); group = groups[j]
    before = tuple(i for g in groups[:j] for i in g)
    after = tuple(i for g in groups[j+1:] for i in g)
    bases = {e: sum((weights[i] for i in before if e in partial[i]), Q(0)) for e in E}
    constants = {}
    for e in E:
        U = tuple(i for i in group if any(e in z for z in families[i]))
        if U:
            a = min(weights[i] for i in U); b = max(weights[i] for i in U)
            L = sum((weights[i] for i in after if any(e in z for z in families[i])), Q(0))
            constants[e] = a, b, (1 + L/a)**d
    return bases, constants


def audit_game(game):
    weights, families, coeffs, groups, d = game
    n = len(weights); E = range(len(coeffs))
    all_indices = [i for g in groups for i in g]
    require(sorted(all_indices) == list(range(n)) and len(all_indices) == n, "partition")
    require(all(groups) and all(families), "nonempty groups and strategy families")
    require(all(w > 0 for w in weights), "positive weights")
    require(all(len(c) <= d+1 and all(a >= 0 for a in c) for c in coeffs), "nonnegative degree bound")
    A = Q(1)
    for j in range(len(groups)):
        # All earlier strategies empty suffices for constants, which depend only on potential users.
        _, constants = stage_data(game, j, [()] * n)
        for a, b, beta in constants.values():
            A = max(A, b/a*beta)
    counts = {"stage_nodes": 0, "stage_minimizers": 0, "terminal_paths": 0,
              "final_states": 0, "deviations": 0, "interface_chains": 0}
    final_states = set()

    def visit(j, partial, history):
        if j == len(groups):
            counts["terminal_paths"] += 1
            state = tuple(partial)
            if state in final_states:
                return
            final_states.add(state)
            for i in range(n):
                owner = next(k for k, g in enumerate(groups) if i in g)
                bases, constants, snapshot = history[owner]
                for t in families[i]:
                    dev = list(state); dev[i] = t
                    require(game_cost(i, state, weights, coeffs) <= A * game_cost(i, dev, weights, coeffs),
                            ("final_equilibrium", enc(game), state, i, t, str(A)))
                    def D(local):
                        total = Q(0)
                        for e in local[i]:
                            ids = tuple(k for k in groups[owner] if e in local[k])
                            a, b, beta = constants[e]
                            total += beta/a * phi_direct(ids, i, weights, coeffs[e], bases[e])
                        return total
                    stage_dev = list(snapshot); stage_dev[i] = t
                    stage_cost = sum((latency(coeffs[e], bases[e] + sum((weights[k] for k in groups[owner] if e in stage_dev[k]), Q(0))) for e in t), Q(0))
                    chain = [game_cost(i,state,weights,coeffs), D(snapshot), D(stage_dev), A*stage_cost, A*game_cost(i,dev,weights,coeffs)]
                    require(all(x <= y for x,y in zip(chain,chain[1:])), ("interface_chain",enc(game),state,i,t,enc(chain)))
                    counts["deviations"] += 1; counts["interface_chains"] += 1
            return
        counts["stage_nodes"] += 1
        group = groups[j]; bases, constants = stage_data(game,j,partial)
        def P(choice):
            return sum((constants[e][2]/constants[e][0] * potential(tuple(i for i,z in zip(group,choice) if e in z),weights,coeffs[e],bases[e]) for e in E if e in constants), Q(0))
        choices = list(product(*(families[i] for i in group)))
        values = [P(c) for c in choices]; best = min(values)
        minima = [c for c,v in zip(choices,values) if v == best]
        counts["stage_minimizers"] += len(minima)
        for choice in minima:
            new = list(partial)
            for i,z in zip(group,choice): new[i] = z
            visit(j+1,new,history+[(bases,constants,tuple(new))])
    visit(0,[()] * n,[])
    counts["final_states"] = len(final_states)
    return {"A": A, **counts}


def stage_inputs():
    full = ((),(0,),(1,),(0,1))
    games = [
        ([Q(1),Q(3)], [full,full], [(Q(0),),(Q(0),)], [[0],[1]], 0),
        ([Q(1,3),Q(2),Q(5)], [full,full,full], [(Q(0),Q(1)),(Q(1),Q(0),Q(1))], [[0,2],[1]], 2),
        ([Q(1),Q(1),Q(8)], [((),)]*3, [(Q(1),Q(2)),(Q(0),)], [[2],[0,1]], 1),
        ([Q(2),Q(1)], [((0,),(0,1)),((0,),())], [(Q(1),Q(1)),(Q(0),Q(0),Q(1))], [[1],[0]], 2),
        ([Q(1),Q(4),Q(1,2)], [full,full,full], [(Q(0),)*4,(Q(0),)*4], [[1,2],[0]], 3),
        ([Q(5),Q(2),Q(1)], [((0,),(1,)),full,((0,1),())], [(Q(2),),(Q(1),)], [[2],[0,1]], 0),
    ]
    rng = Random(SEED)
    for run in range(96):
        n = rng.randrange(1,5); d = rng.randrange(5)
        weights = [rng.choice([Q(1,3),Q(1),Q(3),Q(7,2)]) for _ in range(n)]
        families = [tuple(z for z in full if rng.randrange(2)) or ((),) for _ in range(n)]
        coeffs = [tuple(Q(rng.randrange(3),rng.randrange(1,4)) for _ in range(d+1)) for _ in range(2)]
        if run % 11 == 0: coeffs = [(Q(0),)*(d+1)]*2
        if run % 13 == 0: families = [((),)]*n
        indices = list(range(n)); rng.shuffle(indices)
        cuts = sorted(set([0,n]+[rng.randrange(n+1) for _ in range(n)]))
        groups = [indices[a:b] for a,b in zip(cuts,cuts[1:]) if a < b]
        games.append((weights,families,coeffs,groups,d))
    return games


def ordered_partitions(n):
    # Labelled players; no quotient by light-player permutations.
    for m in range(1,n+1):
        for labels in product(range(m),repeat=n):
            if len(set(labels)) == m:
                yield tuple(tuple(i for i in range(n) if labels[i] == j) for j in range(m))


def parameter_value(weights,groups,d):
    ans = Q(1)
    for j,B in enumerate(groups):
        a=min(weights[i] for i in B); b=max(weights[i] for i in B)
        L=sum((weights[i] for g in groups[j+1:] for i in g),Q(0))
        ans=max(ans,b/a*(1+L/a)**d)
    return ans


def check_parameter():
    cases=[]; total=0
    cache={K:list(ordered_partitions(K+1)) for K in range(1,5)}
    for H,K,d in product((Q(1),Q(3,2),Q(2),Q(5,2)),range(1,5),(0,1,2,4)):
        weights=[H]+[Q(1)]*K
        best=min(parameter_value(weights,g,d) for g in cache[K])
        target=min(H,(1+Q(K)/H)**d) if d else Q(1)
        require(best==target,("sharp_parameter",str(H),K,d,str(best),str(target)))
        cases.append({"H":H,"K":K,"d":d,"partitions":len(cache[K]),"minimum":best})
        total+=len(cache[K])
    return {"cases":cases,"partition_evaluations":total,"includes_degree_zero_separate_endpoint":True}


def check_dense():
    cases=[]
    for d in range(2,9):
        for n in (d,d+1,2*d):
            M=d*n; q=Q(1,n*(d*n+1)); beta=(1+Q(1,d))**d
            high_factor=1/(1-(1-q)**d)
            require(beta<Q(3),("dense_beta_lt_3",d,n))
            require(high_factor>=1/(d*q),("high_share_comparison",d,n))
            cases.append({"d":d,"n":n,"M":M,"beta":beta,"q":q,"high_share_factor":high_factor,"high_share_lower_bound":1/(d*q)})
    # Rational square roots at p=1/2, R=25/9: A_R(p)=2 exactly.
    density=[]
    for root_d in (2,3,4):
        for root_n in (root_d,root_d+1,2*root_d):
            d=root_d**2;n=root_n**2
            B=Q(2*root_d*root_n)
            require(B>=d,("density_lower_comparison",d,n))
            density.append({"d":d,"n":n,"R":"25/9","p":"1/2","A_R_p":"2","K_R":n,"B":B})
    return {"pure_nonzero_degree_d_shared_resource_cases":cases,"exact_density_cases":density,
            "scope":"comparisons assume a shared resource of nonzero latency x^d; zero-fee resources are not charged by the high-degree-share bound"}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    games=stage_inputs()
    stage=[{"input":g,"result":audit_game(g)} for g in games]
    totals={k:sum(row["result"][k] for row in stage) for k in ("stage_nodes","stage_minimizers","terminal_paths","final_states","deviations","interface_chains")}
    report={"title":"有序尾部冻结：独立份额、全最小点、参数锐式与密集群审计",
            "audit_version":VERSION,"python_version":platform.python_version(),
            "source_sha256":sha256(Path(__file__).read_bytes()).hexdigest(),"seed":SEED,
            "arithmetic":"fractions.Fraction; exact comparisons; no tolerance",
            "imports_author_code":False,"share_audit":check_shares(),
            "staged_game_count":len(games),"staged_totals":totals,"staged_games":stage,
            "parameter_audit":check_parameter(),"dense_audit":check_dense(),
            "result":"pass","limitation":"Finite rational input audit, not a proof over arbitrary real parameters."}
    payload=json.dumps(enc(report),ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    if args.output:
        with args.output.open("x",encoding="utf-8") as f:f.write(payload)
        print(json.dumps({"status":"created","output":str(args.output),"source_sha256":report["source_sha256"],"staged_games":len(games),"staged_totals":totals},ensure_ascii=False,sort_keys=True))
    else:
        sys.stdout.write(payload)


if __name__=="__main__":
    main()
