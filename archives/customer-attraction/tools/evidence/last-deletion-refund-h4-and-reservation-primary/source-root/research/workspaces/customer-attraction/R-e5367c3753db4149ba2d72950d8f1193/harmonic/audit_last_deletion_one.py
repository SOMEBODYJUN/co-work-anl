"""Exact unit-customer audit of the coefficient-one last-deletion reset.

Independent of the repository model, solver, and certificate verifier.
This refutes an auxiliary all-input statement, not Q-CAG-HALF.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

NAMES=("A","B","T","C")
TOPICS=(frozenset(range(25)),frozenset(range(24))|{25},frozenset(range(24)),frozenset(range(26,35)))
LAST={(0,0):1,(0,1):3,(0,2):1,(0,3):1,
      (1,0):3,(1,1):0,(1,2):0,(1,3):0,
      (2,0):1,(2,1):0,(2,2):0,(2,3):0,
      (3,0):1,(3,1):0,(3,2):0,(3,3):0}
SECOND=(1,0,3,0)

def prescribed(h):
    if not h:return 0
    if len(h)==1:return SECOND[h[0]]
    return LAST[h]

def follow(h):
    while len(h)<3:h=h+(prescribed(h),)
    return h

def follow_deleted(h):
    """Causal retained strategy, using the original prescriptions verbatim."""
    while len(h)<2:h=h+(prescribed(h),)
    return h

def utility(path,i):
    return sum((F(1,sum(x in TOPICS[a] for a in path)) for x in TOPICS[path[i]]),F(0))

def name(path):return "".join(NAMES[a] for a in path)

def audit():
    comparisons=0;minimum=None;second_rows=[];last_rows=[]
    for depth in range(3):
        for h in product(range(4),repeat=depth):
            leaf=follow(h);base=utility(leaf,depth)
            row=[]
            for a in range(4):
                forced=follow(h+(a,));value=utility(forced,depth);gap=base-value
                assert gap>=0,(h,a,leaf,forced,gap)
                comparisons+=1;minimum=gap if minimum is None else min(minimum,gap);row.append(value)
            if depth==1:second_rows.append(list(map(str,row)))
            if depth==2:last_rows.append({"history":name(h),"reply":NAMES[prescribed(h)],"payoffs":list(map(str,row))})
    Z=follow(());ZT=follow((2,));reduced_actual=Z[:-1];reduced_forced=ZT[:-1]
    ui=utility(Z,0);last=utility(Z,2);deleted=utility(reduced_forced,0)
    reducedvalues=[utility(follow((a,))[:-1],0) for a in range(4)]
    rho=max(reducedvalues)-utility(reduced_actual,0)
    R=utility(reduced_actual,0)-ui
    W=len(set().union(*(TOPICS[a] for a in Z)))
    OPT=max(len(set().union(*(TOPICS[a] for a in path))) for path in product(range(4),repeat=3))
    assert Z==(0,1,3) and ZT==(2,3,0)
    assert (ui,last,deleted,rho,R)==(F(13),F(9),F(24),F(11),F(0))
    assert deleted-ui-last==2 and W==OPT==35
    deleted_histories=[]
    for depth in range(2):
        for h in product(range(4),repeat=depth):
            original=follow(h);retained=follow_deleted(h)
            forced=[follow_deleted(h+(a,)) for a in range(4)]
            vals=[utility(leaf,depth) for leaf in forced]
            old=utility(original,depth);refund=utility(retained,depth)-old
            regret=max(vals)-utility(retained,depth)
            assert retained==original[:-1]
            for a,leaf in enumerate(forced):assert leaf==follow(h+(a,))[:-1]
            deleted_histories.append({"history":name(h),"prescribed":NAMES[prescribed(h)],
                                      "original_leaf":name(original),"retained_leaf":name(retained),
                                      "deleted_deviation_payoffs":list(map(str,vals)),
                                      "original_current_payoff":str(old),"actual_refund":str(refund),
                                      "original_last_payoff":str(utility(original,2)),
                                      "reduced_regret":str(regret),"regret_plus_refund":str(regret+refund)})
    return {"status":"PASS","scope":"one exact complete SPE refutes general coefficient-one last-deletion reset; half not refuted",
            "unit_customers":35,"players":3,"topics":list(NAMES),"decision_nodes":21,"spe_comparisons":comparisons,
            "minimum_spe_gap":str(minimum),"second_player_deviation_rows":second_rows,"last_player_rows":last_rows,
            "actual_path":name(Z),"actual_payoffs":[str(utility(Z,i)) for i in range(3)],
            "root_true_deviation_payoffs":[str(utility(follow((a,)),0)) for a in range(4)],
            "forced_T_original_path":name(ZT),"forced_T_original_payoff":str(utility(ZT,0)),
            "forced_T_deleted_path":name(reduced_forced),"forced_T_deleted_payoff":str(deleted),
            "root_deleted_deviation_payoffs":list(map(str,reducedvalues)),"reset_candidate_rhs":str(ui+last),
            "reset_violation":str(deleted-ui-last),"reduced_root_regret":str(rho),"actual_deletion_refund":str(R),
            "all_retained_ordered_histories":deleted_histories,
            "W":W,"OPT":OPT,"half_margin":2*W-OPT}

if __name__=="__main__":
    report=audit();out=Path(__file__).with_name("last_deletion_one_audit.json")
    out.write_text(json.dumps(report,indent=2)+"\n")
    certificate={"claim":"auxiliary coefficient-one causal last-deletion reset fails; Q-CAG-HALF not refuted",
                 "instance":{"topics":list(NAMES),"players":3,
                             "customers":[{"topics":[0,1,2],"multiplicity":24},
                                          {"topics":[0],"multiplicity":1},
                                          {"topics":[1],"multiplicity":1},
                                          {"topics":[3],"multiplicity":9}]},
                 "strategy":{"actions":[{"history":list(h),"action":prescribed(h)}
                                         for depth in range(3) for h in product(range(4),repeat=depth)]}}
    Path(__file__).with_name("last_deletion_one_certificate.json").write_text(json.dumps(certificate,indent=2)+"\n")
    print(json.dumps(report,indent=2))
