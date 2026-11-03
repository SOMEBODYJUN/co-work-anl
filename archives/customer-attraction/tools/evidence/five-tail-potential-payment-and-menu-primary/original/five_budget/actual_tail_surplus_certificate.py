"""Exact five-player certificate; no external solver is used.

Generate one complete ordered-history SPE with prescribed path XXCBC,
then verify every history and every one-action deviation from the JSON policy.
The minmax certificates are independently checked by finite exact inequalities.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOPICS = "ABCX"
MEMBERSHIP = ((1,1,0,1), (0,0,1,1), (1,0,1,1),
              (1,1,1,0), (0,0,0,1))
MULTIPLICITIES = (3,3,1,5,1)
M = 5
TARGET = "XXCBC"
TARGET_COUNTS = (0,1,2,2)

def counts(history):
    return tuple(history.count(a) for a in TOPICS)

def plus(q, a):
    return tuple(v + (i == a) for i, v in enumerate(q))

@lru_cache(None)
def payoff(q, a):
    return sum((F(r, sum(c*b for c,b in zip(q, mem)))
                for r,mem in zip(MULTIPLICITIES, MEMBERSHIP) if mem[a]), F())

@lru_cache(None)
def attainable(q):
    """All attainable terminal count vectors, with arbitrary ordered ties."""
    if sum(q) == M:
        return frozenset((q,))
    kids = tuple(attainable(plus(q,a)) for a in range(4))
    threshold = max(min(payoff(z,a) for z in kids[a]) for a in range(4))
    return frozenset(z for a in range(4) for z in kids[a]
                     if payoff(z,a) >= threshold)

def build(history, target, policy):
    if len(history) == M:
        assert counts(history) == target
        return
    q = counts(history)
    kids = tuple(attainable(plus(q,a)) for a in range(4))
    minima = tuple(min(payoff(z,a) for z in kids[a]) for a in range(4))
    threshold = max(minima)
    good = [a for a in range(4) if target in kids[a]
            and payoff(target,a) >= threshold]
    if TARGET.startswith(history):
        a = TOPICS.index(TARGET[len(history)])
        assert a in good
    else:
        a = good[0]
    policy[history] = TOPICS[a]
    for b in range(4):
        child_target = target if b == a else min(
            kids[b], key=lambda z: (payoff(z,b), z))
        build(history + TOPICS[b], child_target, policy)

def continue_policy(history, policy):
    while len(history) < M:
        history += policy[history]
    return history

def security(a, background):
    return sum((F(r, 1 + sum(c*b for c,b in zip(background,mem)))
                for r,mem in zip(MULTIPLICITIES,MEMBERSHIP) if mem[a]), F())

def potential_increment(background, a, d):
    return sum((r * sum((F(1, sum(c*b for c,b in zip(background,mem)) + t)
                        for t in range(1,mem[a]+mem[d]+1)),F())
                for r,mem in zip(MULTIPLICITIES,MEMBERSHIP)), F())

def main():
    assert TARGET_COUNTS in attainable((0,0,0,0))
    policy = {}
    build("", TARGET_COUNTS, policy)
    payload = {"topics": list(TOPICS), "multiplicities": MULTIPLICITIES,
               "membership": MEMBERSHIP, "players": M, "target": TARGET,
               "policy": policy}
    (HERE / "actual_tail_surplus_policy.json").write_text(
        json.dumps(payload,indent=2,sort_keys=True) + "\n")

    # Verify the complete JSON policy by direct replay, without attainable().
    loaded = json.loads((HERE / "actual_tail_surplus_policy.json").read_text())
    pol = loaded["policy"]
    histories = ["".join(h) for k in range(M)
                 for h in product(TOPICS,repeat=k)]
    assert set(pol) == set(histories)
    comparisons = 0
    for h in histories:
        actual = continue_policy(h,pol)
        source_action = TOPICS.index(actual[len(h)])
        source = payoff(counts(actual),source_action)
        for a in TOPICS:
            dev = continue_policy(h+a,pol)
            assert source >= payoff(counts(dev),TOPICS.index(a)), (h,a)
            comparisons += 1
    assert continue_policy("",pol) == TARGET
    actual_payoffs = [payoff(TARGET_COUNTS,TOPICS.index(a)) for a in TARGET]
    assert actual_payoffs == [F(5,2),F(5,2),F(8,3),F(8,3),F(8,3)]
    assert sum(actual_payoffs) == 13
    # The actual path covers every one of the thirteen unit customers.
    assert all(sum(c*b for c,b in zip(TARGET_COUNTS,mem)) > 0
               for mem in MEMBERSHIP)

    # Fixed actual prefix XXC: q=(0,0,1,2).
    prefix = (0,0,1,2)
    utility = [[payoff(plus(plus(prefix,a),d),a) for d in range(4)]
               for a in range(4)]
    local_w = F(157,60)
    # Pure A is a primal and pure A is a dual for the local two-player game.
    assert min(utility[0]) == local_w
    assert max(row[0] for row in utility) == local_w
    pmat = [[potential_increment(prefix,a,d) for d in range(4)]
            for a in range(4)]
    gap = max(v for row in pmat for v in row) - pmat[1][2]
    assert gap == F(1,5)
    tail_profit = actual_payoffs[3] + actual_payoffs[4]
    assert tail_profit - 2*local_w == F(1,10) < gap

    # The original global v_5 is different from local w(q).
    backgrounds = [q for q in product(range(5),repeat=4) if sum(q) == 4]
    primal = (F(5,17),F(),F(5,17),F(7,17))
    dual = (((1,0,1,2),F(3,17)), ((1,0,2,1),F(7,17)),
            ((2,0,1,1),F(7,17)))
    global_v = F(202,85)
    assert min(sum((primal[a]*security(a,q) for a in range(4)),F())
               for q in backgrounds) == global_v
    assert max(sum((weight*security(a,q) for q,weight in dual),F())
               for a in range(4)) == global_v
    assert sum(actual_payoffs[:3]) + gap > 3*global_v
    out = {"histories":len(histories), "comparisons":comparisons,
           "path":TARGET, "payoffs":list(map(str,actual_payoffs)),
           "W":13, "OPT5":13, "local_w":str(local_w),
           "local_utility_matrix":[list(map(str,row)) for row in utility],
           "local_potential_matrix":[list(map(str,row)) for row in pmat],
           "Gamma2":str(gap), "tail_surplus":str(tail_profit-2*local_w),
           "global_v5":str(global_v), "status":"exact checks passed"}
    (HERE / "actual_tail_surplus_audit.json").write_text(
        json.dumps(out,indent=2) + "\n")
    print(json.dumps(out,indent=2))

if __name__ == "__main__":
    main()
