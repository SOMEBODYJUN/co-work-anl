"""Definition-level verification of the carried-floor recursive-step failure.

No canonical model, SPE solver, strategy-cone LP, numpy, or scipy is imported.
All 69 unit customers and all ordered histories are explicitly evaluated.
"""
from fractions import Fraction
from itertools import product
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
P=6
M=4
TYPES=[((0,),30),((1,),7),((2,),5),((3,),7),((2,4),2),
       ((2,5),2),((1,4,5),6),((2,4,5),4),((3,4,5),6)]
COVERS=[set() for _ in range(P)]
CLIENTS=[]
for members,n in TYPES:
    for _ in range(n):
        x=len(CLIENTS);CLIENTS.append(set(members))
        for a in members:COVERS[a].add(x)


def action(h):
    if len(h)<3:return 0
    number_A=h.count(0)
    if number_A<=1:return 0
    if number_A==2 and 5 in h:return 4
    return 5


def payoff(path,index):
    return sum((Fraction(1,sum(x in COVERS[a] for a in path))
                for x in COVERS[path[index]]),Fraction(0))


def terminal(h):
    while len(h)<M:h=h+(action(h),)
    return h


def F(prefix,slots):
    best=Fraction(-1);argmax=[]
    for tail in product(range(P),repeat=slots):
        total=Fraction(0)
        for x in range(len(CLIENTS)):
            old=sum(x in COVERS[a] for a in prefix)
            new=sum(x in COVERS[a] for a in tail)
            if new:total+=Fraction(new,old+new)
        if total>best:best=total;argmax=[tail]
        elif total==best:argmax.append(tail)
    return best,argmax


def h(prefix,slots):
    return max(sum((Fraction(1,sum(x in COVERS[t] for t in prefix)+slots)
                    for x in COVERS[a]),Fraction(0)) for a in range(P))


def main():
    histories=deviations=ties=0
    minimum=None
    for depth in range(M):
        for history in product(range(P),repeat=depth):
            histories+=1
            actual=terminal(history)
            u=payoff(actual,depth)
            for a in range(P):
                if a==action(history):continue
                deviations+=1
                branch=terminal(history+(a,))
                slack=u-payoff(branch,depth)
                assert slack>=0,(history,a,actual,branch,u,payoff(branch,depth))
                ties+=slack==0
                minimum=slack if minimum is None else min(minimum,slack)
    path=terminal(())
    welfare=len(set().union(*(COVERS[a] for a in path)))
    optimum,optimal_paths=F((),4)
    child,child_paths=F((0,),3)
    floor=h((),4);child_floor=h((0,),3);u=payoff(path,0)
    lhs=optimum;root_reserve=8*floor
    child_reserve=2*u+max(child,6*child_floor)
    rhs=max(root_reserve,child_reserve)
    assert (lhs,root_reserve,child_reserve,rhs,lhs-rhs)==(69,60,65,65,4)
    assert (welfare,tuple(payoff(path,i) for i in range(M)))==(48,(10,10,10,18))
    # The new closed-form policy equals the fully saved policy at every node.
    original=json.loads((HERE/"recursive_step_attack.json").read_text())[0]
    saved={tuple(v["history"]):v["action"] for v in original["strategy"]["actions"]}
    expected={h:action(h) for d in range(M) for h in product(range(P),repeat=d)}
    assert saved==expected
    saved_types=sorted((tuple(x["topics"]),x["multiplicity"]) for x in original["instance"]["customers"])
    assert saved_types==sorted(TYPES)
    result={"valid_full_ordered_history_pure_SPE":True,
            "independent_of_canonical_solver_and_LP":True,
            "unit_customers":len(CLIENTS),"topics":P,"players":M,
            "checked_histories":histories,"checked_deviations":deviations,
            "deviation_ties":ties,"minimum_slack":minimum,
            "path":path,"payoffs":[payoff(path,i) for i in range(M)],
            "welfare":welfare,"OPT":optimum,"Fchild":child,
            "hroot":floor,"hchild":child_floor,
            "root_floor_reserve":root_reserve,"child_reserve":child_reserve,
            "right_hand_side":rhs,"strict_failure_gap":lhs-rhs,
            "half_coverage_slack":2*welfare-optimum,
            "root_OPT_example":optimal_paths[0],"child_F_example":child_paths[0],
            "stored_complete_strategy_and_types_match":True}
    serial=lambda x:str(x) if isinstance(x,Fraction) else x
    output=json.dumps(result,default=serial,indent=2)+"\n"
    (HERE/"recursive_step_counterexample_verification.json").write_text(output)
    print(output,end="")


if __name__=="__main__":main()
