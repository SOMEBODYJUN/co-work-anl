"""Definition-level audit of the two-topic deletion example; no solver import."""
import argparse
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    themes=({0,1},{2,3})
    policy={():0,(0,):0,(1,):1,(0,0):1,(0,1):1,(1,0):0,(1,1):0}
    def terminal(history):
        while len(history)<3:history=history+(policy[history],)
        return history
    def payoff(history,index):
        return sum((F(1,sum(x in themes[a] for a in history)) for x in themes[history[index]]),F(0))
    comparisons=[]
    for depth in range(3):
        for history in product(range(2),repeat=depth):
            actual=terminal(history)
            for action in range(2):
                other=terminal(history+(action,))
                slack=payoff(actual,depth)-payoff(other,depth)
                assert slack>=0
                comparisons.append(str(slack))
    # Matching static saddle certificates: uniform query and pure AB background.
    static=[]
    for background in ((0,0),(0,1),(1,1)):
        query=[]
        for a in range(2):
            query.append(sum((F(1,1+sum(x in themes[c] for c in background)) for x in themes[a]),F(0)))
        static.append(query)
    assert max(static[1])==1 and min(sum(q,F(0))/2 for q in static)==1
    records=[]
    for root in range(2):
        full=terminal((root,));utilities=tuple(payoff(full,j) for j in range(3))
        assert utilities==(F(1),F(1),F(2))
        low=(1,);high=(2,);c=F(0);remainder=F(0)
        for x in range(4):
            a=int(x in themes[root]);h=int(x in themes[full[2]])
            ell=int(x in themes[full[1]]);q=F(h)
            dhat=a+h;den=dhat+ell
            if a or q:
                c+=(a-q)*ell/F(dhat*den)
                remainder+=(a-q)/F(dhat)
        assert c==1 and remainder==0
        d=utilities[0];z=utilities[2];eta=z-1
        assert d==1+eta+remainder-c
        actual_tail=utilities[1]+utilities[2];epsilon=actual_tail-2
        kappa=F(0)
        assert sum(utilities,F(0))-3==epsilon+kappa+eta+remainder-c
        records.append({"root":root,"terminal":full,"utilities":list(map(str,utilities)),
                        "deletion_cost":str(c),"stationary_remainder":str(remainder),
                        "retained_surplus":str(eta),"actual_tail_surplus":str(epsilon)})
    result={"status":"exact_identity_and_complete_spe_boundary_example",
            "decision_histories":len(policy),"comparisons":len(comparisons),
            "minimum_spe_slack":str(min(map(F,comparisons))),"safe_value":"1","branches":records,
            "strict_bad_root_hypothesis":False,
            "individual_security_reference_gap":str(F(2411,246)-F(29,3)),
            "individual_security_reference_tail_surplus":str(F(67,3)-2*F(2411,246))}
    if args.output:
        if args.output.exists():raise FileExistsError(args.output)
        args.output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__=="__main__":main()
