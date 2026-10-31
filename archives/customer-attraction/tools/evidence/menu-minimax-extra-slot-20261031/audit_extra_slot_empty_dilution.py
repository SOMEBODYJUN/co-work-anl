"""Definition-level Fraction audit; no CAG solver or discovery-code imports."""
import itertools,json
from fractions import Fraction as F
from pathlib import Path

TYPES={4:1,27:4,29:3,30:3,31:2,32:1,43:3,45:3,46:3,51:3,53:3,54:3,59:2}
LAST=[[1,2,1,4,3,3,1],[2,0,0,4,3,3,0],[1,0,0,4,3,3,0],
      [1,0,0,4,5,4,4],[1,0,0,5,3,3,3],[1,0,0,4,3,3,3],
      [1,0,0,4,3,3,0]]
SECOND=[3,3,3,0,0,0,0]

def action(h):
    return 0 if not h else SECOND[h[0]] if len(h)==1 else LAST[h[0]][h[1]]

def terminal(h):
    while len(h)<3:h+=(action(h),)
    return h

# Expand actual unit customers, rather than treating their multiplicities as values.
CLIENTS=[frozenset(a for a in range(7) if mask>>a&1) for mask,w in TYPES.items() for _ in range(w)]
def utility(a,z,extra=False):
    return sum((F(1,int(extra)+sum(b in client for b in z)) for client in CLIENTS if a in client),F())

def main():
    comparisons=[]
    for length in range(3):
        for h in itertools.product(range(7),repeat=length):
            played=action(h);z=terminal(h);v=utility(played,z)
            for a in range(7):
                if a==played:continue
                slack=v-utility(a,terminal(h+(a,)))
                assert slack>=0,(h,a,slack)
                comparisons.append(slack)
    actual=terminal(())
    assert actual==(0,3,4)
    W=sum(utility(a,actual) for a in actual)
    assert W==32
    sums=[F(),F(),F()]; rows=[]
    expected=[(F(29,3),F(32,3),F(13,2)),(F(32,3),F(32,3),F(7)),(F(67,6),F(67,6),F(7))]
    for i in range(3):
        zq=terminal(actual[:i]+(2,));ze=terminal(actual[:i]+(6,))
        vals=(utility(2,zq),utility(2,ze,True),utility(2,zq,True))
        assert vals==expected[i]
        sums=[x+y for x,y in zip(sums,vals)]
        rows.append({'i':i+1,'Z_i_q':zq,'Z_i_empty':ze,'D_q':str(vals[0]),'H_empty_q':str(vals[1]),'G_q':str(vals[2])})
    assert sums==[F(63,2),F(65,2),F(41,2)]
    e=F(1,24);p={2:e,6:1-e};D=G=F()
    for i in range(3):
        branches={a:terminal(actual[:i]+(a,)) for a in p}
        D+=sum(p[a]*utility(a,branches[a]) for a in p)
        G+=sum(p[a]*p[t]*utility(t,branches[a],True) for a in p for t in p)
    assert (D,G,D-G)==(F(21,16),F(4,3),F(-1,48))
    result={'status':'EXACT_STRONG_AGGREGATE_EXTRA_SLOT_FAILURE','players':3,'topics':7,'unit_customers':len(CLIENTS),'histories':57,'nonself_comparisons':len(comparisons),'all_spe_comparisons_nonnegative':True,'actual':actual,'W':str(W),'rows':rows,'sum_D_q':str(sums[0]),'sum_H_empty_q':str(sums[1]),'sum_G_q':str(sums[2]),'gap_polynomial_coefficients':['0','-1','12'],'epsilon':str(e),'D_epsilon':str(D),'G_epsilon':str(G),'D_minus_G':str(D-G),'W_minus_G':str(W-G),'scope':'Auxiliary strong aggregate decorrelation only; weak aggregate W bound, Mfull and Q-CAG-HALF not refuted.'}
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
