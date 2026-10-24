"""Definition-level exact audit of one parameter of the all-k controller.

The finite controller has permanent canonical backward-induction exits. Counts
plus controller mode are a deterministic finite acyclic automaton on ALL
ordered histories. No repository model, optimizer, or SPE solver is imported.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations
from math import lcm
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent


def audit(k):
    assert k >= 6
    m, K = k+3, 6
    blocks = [(frozenset([0]),3), (frozenset([1]),4),
              (frozenset([2,3]),6), (frozenset([2,4]),6),
              (frozenset([0,3,4]),2), (frozenset([1,3,4]),2),
              (frozenset([5]),5*k)]
    units = [S for S,n in blocks for _ in range(n)]
    denominator = lcm(*range(1,m+1))
    initial = (0,)*K
    statistics = {"bi_nodes":0, "controller_nodes":0, "bi_comparisons":0,
                  "controller_comparisons":0, "minimum_gap_scaled":None}
    actual_actions = {}

    def add(q,a):
        return tuple(v+int(t==a) for t,v in enumerate(q))

    @lru_cache(None)
    def payoff(q,a):
        ans = 0
        for S in units:
            if a in S:
                count = sum(q[t] for t in S)
                assert count > 0 and denominator % count == 0
                ans += denominator//count
        return ans

    def record(gap, kind):
        assert gap >= 0, (kind,gap)
        statistics[kind+"_comparisons"] += 1
        old = statistics["minimum_gap_scaled"]
        statistics["minimum_gap_scaled"] = gap if old is None else min(old,gap)

    @lru_cache(None)
    def bi(q):
        if sum(q)==m:
            return q
        statistics["bi_nodes"] += 1
        children = [bi(add(q,a)) for a in range(K)]
        values = [payoff(children[a],a) for a in range(K)]
        chosen = max(range(K),key=lambda a:values[a])
        for value in values:
            record(values[chosen]-value,"bi")
        return children[chosen]

    main_second = (3,2,3,4,2)
    main_third = (2,3,2,2,3)
    good_second = (1,2,3,4,2)
    good_third = ((2,2,2,2,2),(2,2,3,2,2),(2,3,3,2,3),
                  (2,2,2,2,2),(2,2,3,2,2))
    main_second_payoff = (6,9,6,5,6)

    def check_prefix(q,h):
        assert tuple(q[:5])==tuple(h.count(a) for a in range(5))

    def choose(q,mode):
        kind = mode[0]
        if kind=="N":
            assert all(q[a]==0 for a in range(5)) and q[5]<k
            return 5
        if kind=="G":
            h=mode[1]
            check_prefix(q,h)
            assert q[5]==k and len(h)<3
            return 0 if not h else good_second[h[0]] if len(h)==1 else good_third[h[0]][h[1]]
        if kind=="B":
            check_prefix(q,(mode[1],))
            assert m-sum(q)>=2
            return main_second[mode[1]]
        if kind=="C":
            check_prefix(q,mode[1])
            return mode[2]
        if kind=="F":
            check_prefix(q,(0,2))
            assert m-sum(q)>=2
            return 2
        if kind=="S":
            # Every nonterminal saturated mode has the advertised raw core cap.
            assert all(payoff(add(q,a),a)<=5*denominator for a in range(5))
            return 5
        raise AssertionError(mode)

    def transition(q,mode,a):
        kind=mode[0]
        remaining=m-sum(q)
        if kind=="N":
            return ("N",) if a==5 and q[5]+1<k else ("G",()) if a==5 else ("B",a)
        if kind=="G":
            return None if a==5 else ("G",mode[1]+(a,))
        if kind=="S":
            return mode if a==5 else None
        if kind in {"B","C","F"} and a==5:
            needed=2 if kind in {"B","F"} else 1
            return mode if remaining>needed else None
        if kind=="C":
            return ("S",) if a==mode[2] else None
        if kind=="F":
            return ("C",(0,2,2),1) if a==2 else None
        if kind=="B":
            T=mode[1]
            if a==main_second[T]:
                return ("C",(T,a),main_third[T])
            if payoff(add(q,a),a)<=main_second_payoff[T]*denominator:
                return None
            if (T,a)==(0,2):
                return ("F",) if remaining>=3 else ("C",(0,2),2)
            if (T,a) in {(0,4),(2,4),(3,2),(4,3)}:
                return ("C",(T,a),2)
            raise AssertionError((q,mode,a))
        raise AssertionError((q,mode,a))

    @lru_cache(None)
    def solve(q,mode):
        if sum(q)==m:
            return q
        if mode is None:
            return bi(q)
        statistics["controller_nodes"] += 1
        chosen=choose(q,mode)
        children=[]
        for a in range(K):
            child=transition(q,mode,a)
            children.append(solve(add(q,a),child))
        base=payoff(children[chosen],chosen)
        for a in range(K):
            record(base-payoff(children[a],a),"controller")
        actual_actions[(q,mode)]=chosen
        return children[chosen]

    terminal=solve(initial,("N",))
    expected=(1,1,1,0,0,k)
    assert terminal==expected
    q,mode=initial,("N",)
    path=[]
    while sum(q)<m:
        assert mode is not None
        a=actual_actions[(q,mode)]
        path.append(a)
        mode=transition(q,mode,a)
        q=add(q,a)
    assert path==[5]*k+[0,1,2]
    payoffs=[F(payoff(terminal,a),denominator) for a in path]
    assert payoffs==[F(5)]*k+[F(5),F(6),F(12)]
    W=sum(any(q[a] for a in S) for S in units)
    OPT=max(sum(any(a in S for a in chosen) for S in units)
            for n in range(min(m,K)+1) for chosen in combinations(range(K),n))
    assert W==OPT==5*k+23
    lastprefix=(1,1,0,0,0,k)
    matrix=[[sum((F(1,1+sum(lastprefix[t] for t in S)+int(A in S))
                  for S in units if T in S),F(0)) for A in range(K)] for T in range(K)]
    assert min(matrix[2])==6
    assert max(row[2] for row in matrix)==6
    value=F(6)
    gap=m*value-W-payoffs[-1]/2
    assert gap==k-11
    report={"status":"PASS", "scope":"One exact parameter audit of the all-k>=6 full-history controller; weak LAST budget only, not half.",
            "k":k,"players":m,"topics":K,"unit_clients":len(units),
            "bi_exit_rule":"Permanent deterministic complete backward-induction policy on topic counts; first maximizing action wins ties.",
            "finite_automaton_completeness":"Every controller/BI decision has all six transitions; every transition increments exactly its observed topic count; each ordered history has one deterministic mode run ending at depth m.",
            "statistics":{**statistics,"minimum_gap":str(F(statistics['minimum_gap_scaled'],denominator))},
            "root_terminal_counts":terminal,"actual_path":path,"actual_payoffs":list(map(str,payoffs)),
            "W":W,"OPT":OPT,"last_menu_matrix_rows_query_columns_extra_action":[list(map(str,row)) for row in matrix],
            "last_menu_value":str(value),"row_certificate":2,"column_certificate":2,
            "weak_last_gap_mL_minus_W_minus_um_over_2":str(gap),"half_margin":2*W-OPT,
            "canonical_bi_cache_states":bi.cache_info().currsize,"controller_cache_states":solve.cache_info().currsize}
    return report


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--k",type=int,default=12)
    args=parser.parse_args()
    result=audit(args.k)
    path=HERE/f"padded_core_k{args.k}_audit.json"
    path.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
