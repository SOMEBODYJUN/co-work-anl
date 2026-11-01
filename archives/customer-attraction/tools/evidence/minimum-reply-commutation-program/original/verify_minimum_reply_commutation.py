"""Independent full tail-strategy enumeration using 15 individual unit clients."""
from fractions import Fraction as F
from itertools import product
import json

types=[((1,),1),((0,2),2),((1,2),2),((0,1,2),2),((3,),1),
       ((0,3),2),((1,3),2),((0,1,3),1),((0,2,3),2)]
clients=[frozenset(ts) for ts,n in types for _ in range(n)]
prefix=(0,1,1);A=3

def pay(profile):
    ans=[F(0) for _ in profile]
    for customer in clients:
        users=[i for i,a in enumerate(profile) if a in customer]
        if users:
            for i in users:ans[i]+=F(1,len(users))
    return ans

def main():
    # Precompute definition-level terminal payoffs, without a count solver.
    utility={(c,d):pay(prefix+(A,c,d)) for c,d in product(range(4),repeat=2)}
    BR={c:[d for d in range(4) if utility[c,d][5]==max(utility[c,e][5] for e in range(4))] for c in range(4)}
    feasible=[];checked_last=0;checked_source=0
    for c in range(4):
        for replies in product(range(4),repeat=4):
            if not all(replies[b] in BR[b] for b in range(4)):continue
            checked_last+=4*4
            own=utility[c,replies[c]][4]
            checked_source+=4
            if any(own<utility[b,replies[b]][4] for b in range(4)):continue
            feasible.append((utility[c,replies[c]][3],c,replies[c],replies))
    ell=min(t[0] for t in feasible)
    witness=min(t for t in feasible if t[0]==ell and t[1]==3)
    swapped=min(utility[3,d][3] for d in BR[3])
    assert ell==F(71,30) and swapped==F(13,6) and ell-swapped==F(1,5)
    assert witness[1:3]==(3,2) and BR[3]==[0,2]
    source_floor=max(min(utility[c,d][4] for d in BR[c]) for c in range(4))
    assert swapped<source_floor<=ell
    distinct=len({frozenset(i for i,c in enumerate(clients) if a in c) for a in range(4)})==4
    assert distinct
    tie=F(0);delta=F(0)
    for client in clients:
        p=int(0 in client)+2*int(1 in client)
        t=c=int(3 in client);s=int(2 in client);z=int(0 in client)
        tie+=F(s-z,p+t+c+1)
        delta+=F(t*(z-s),(p+c+1)*(p+c+2))
    assert tie==0 and delta==ell-swapped
    print(json.dumps({'unit_customers':len(clients),'distinct_topics':distinct,
                      'all_two_player_policies':4**5,'SPE_tail_policies':len(feasible),
                      'last_best_reply_sets':BR,'last_comparisons':checked_last,
                      'source_comparisons':checked_source,'minimum_old_A':str(ell),
                      'minimum_after_commutation':str(swapped),'strict_gap':str(ell-swapped),
                      'source_threshold':str(source_floor),'witness_tail':witness[1:3],
                      'same_background_BR_equality':str(tie),'minimum_row_coefficient_sum':str(delta),
                      'all_checks_passed':True},indent=2))

if __name__=='__main__':main()
