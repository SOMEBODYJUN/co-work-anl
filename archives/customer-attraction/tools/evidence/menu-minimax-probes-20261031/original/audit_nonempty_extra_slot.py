"""Independent exact test of adding a private client to the formerly empty topic.

Hard-coded unit-customer input and full policy; no parent-audit imports.
"""
import itertools,json
from fractions import Fraction as F

TYPES={4:1,27:4,29:3,30:3,31:2,32:1,43:3,45:3,46:3,51:3,53:3,54:3,59:2}
LAST=[[1,2,1,4,3,3,1],[2,0,0,4,3,3,0],[1,0,0,4,3,3,0],
      [1,0,0,4,5,4,4],[1,0,0,5,3,3,3],[1,0,0,4,3,3,3],
      [1,0,0,4,3,3,0]]
SECOND=[3,3,3,0,0,0,0]
def action(h):return 0 if not h else SECOND[h[0]] if len(h)==1 else LAST[h[0]][h[1]]
def terminal(h):
    while len(h)<3:h+=(action(h),)
    return h
OLD=[frozenset(a for a in range(7) if mask>>a&1) for mask,w in TYPES.items() for _ in range(w)]
NEW=[frozenset([6])]
def utility(clients,a,z,extra=False):
    return sum((F(1,int(extra)+sum(b in t for b in z)) for t in clients if a in t),F())

def main():
    scale=67;clients=OLD*scale+NEW
    slacks=[];olde=[];chosen=[]
    for length in range(3):
        for h in itertools.product(range(7),repeat=length):
            a0=action(h);z0=terminal(h)
            assert a0!=6
            chosen.append(utility(OLD,a0,z0))
            for a in range(7):
                if a==a0:continue
                z=terminal(h+(a,))
                slack=utility(clients,a0,z0)-utility(clients,a,z)
                assert slack>=0,(h,a,slack)
                slacks.append(slack)
                if a==6:
                    # Every successor action is old, so this E player's payoff is
                    # exactly one divided by the previous number of E's plus one.
                    assert utility(NEW,6,z)==F(1,1+h.count(6))
                    olde.append(utility(OLD,a0,z0))
    assert min(chosen)==F(29,3)
    actual=terminal(());p={2:F(1,24),6:F(23,24)}
    def budget(part):
        D=G=F()
        for i in range(3):
            branches={a:terminal(actual[:i]+(a,)) for a in p}
            D+=sum(p[a]*utility(part,a,branches[a]) for a in p)
            G+=sum(p[a]*p[t]*utility(part,t,branches[a],True) for a in p for t in p)
        return D,G
    Do,Go=budget(OLD);Dn,Gn=budget(NEW);D,G=budget(clients)
    assert Do-Go==F(-1,48)
    assert Dn-Gn==F(529,384)
    assert D-G==F(-7,384)==scale*(Do-Go)+(Dn-Gn)
    assert all(any(a in t for t in clients) for a in range(7))
    print(json.dumps({'status':'EXACT_NONEMPTY_STRONG_AGGREGATE_EXTRA_SLOT_FAILURE','scale':scale,'unit_customers':len(clients),'all_topics_nonempty':True,'histories':57,'nonself_comparisons':len(slacks),'all_comparisons_nonnegative':True,'minimum_old_current_payoff':str(min(chosen)),'minimum_new_spe_slack':str(min(slacks)),'old_D':str(Do),'old_G':str(Go),'private_client_D':str(Dn),'private_client_G':str(Gn),'private_client_D_minus_G':str(Dn-Gn),'new_D':str(D),'new_G':str(G),'new_D_minus_G':str(D-G),'general_gap_for_integer_K':'(529-8*K)/384; strict failure iff integer K>=67','general_SPE_sufficiency':'K>=1 (old chosen utility at least 29/3; E deviation utility at most 1)','scope':'Strong all-p aggregate decorrelation only, not weak sum G<=W, Mfull, or half.'},indent=2))

if __name__=='__main__':main()
