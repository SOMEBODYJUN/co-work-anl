"""Independent definition-level audit of the iid-support averaging obstruction.

Constructs each unit customer, all two-player decision histories, and exact
three-player iid payoffs. Does not import the discoverer's code or solver.
General statements require the accompanying algebra; this is a finite audit.
"""
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path
import json


def audit(k, core_copies, private_count):
    assert k>=8 and k%2==0
    customers=[]
    for S in combinations(range(1,k+1),k//2):
        customers.extend([frozenset((0,*S))]*core_copies)
    M=len(customers)
    for a in range(1,k+1):customers.extend([frozenset((a,))]*private_count)
    def payoff(a,z):
        return sum((F(1,sum(t in customer for t in z)) for customer in customers if a in customer),F(0))
    def reply(a):return 1 if a==0 else 0
    sigma={():0,**{(a,):reply(a) for a in range(k+1)}}
    def follow(h):
        while len(h)<2:h=(*h,sigma[h])
        return h
    slacks=[]
    for h,a in sigma.items():
        for other in range(k+1):
            slacks.append(payoff(a,follow(h))-payoff(other,follow((*h,other))))
    assert min(slacks)>=0
    q=[F(0)]+[F(1,k)]*k
    def g(t):return 1-t+t*t/3
    alpha=[sum((g(sum((q[b] for b in customer),F(0))) for customer in customers if a in customer),F(0)) for a in range(k+1)]
    lam=alpha[1]
    assert all(x==lam for x in alpha[1:]) and alpha[0]<=lam
    avg=sum((q[a]*payoff(a,follow((a,))) for a in range(k+1)),F(0))
    assert avg<lam<payoff(0,follow(()))
    assert alpha[0]==F(7*M,12)
    assert avg==F(M,4)+private_count
    assert lam==F(7*M,24)+private_count*g(F(1,k))
    root_W=sum(any(t in c for t in follow(())) for c in customers)
    optimum=max(sum(a in c or b in c for c in customers) for a in range(k+1) for b in range(k+1))
    assert 2*root_W>=optimum
    return dict(k=k,core_copies=core_copies,core_customers=M,private_per_peripheral=private_count,unit_customers=len(customers),ordered_decision_nodes=len(sigma),all_action_comparisons=len(slacks),min_SPE_slack=str(min(slacks)),iid_lambda=str(lam),iid_hub_value=str(alpha[0]),forced_iid_average=str(avg),gap=str(lam-avg),actual_root_payoff=str(payoff(0,follow(()))),W=root_W,OPT=optimum)

# Polynomial identities, ascending coefficient order in k.
# 72 k²(lambda-D)/M = 21k² + 24k²g - 42k².
assert [8,-24,21+24-42] == [8,-24,3]
# Substitute k=8+x by the binomial theorem.
def translate(coefficients, offset):
    return [sum(coefficients[j]*comb(j,i)*offset**(j-i) for j in range(i,len(coefficients))) for i in range(len(coefficients))]
expanded={'iid_Nash_and_average_gap_numerator':translate([8,-24,3],8),'hub_vs_other_peripheral_numerator':translate([-4,1],8)}
assert expanded=={'iid_Nash_and_average_gap_numerator':[8,24,3],'hub_vs_other_peripheral_numerator':[4,1]}
assert all(c>0 for coeffs in expanded.values() for c in coeffs)
# 24(k-1)(hub minus other peripheral)/M = -2(k-1)+3(k-2).
assert [2-6,-2+3]==[-4,1]
results=[audit(8,1,24)]
for kk in (8,10,12):results.append(audit(kk,3,comb(kk,kk//2)))
report={'scope':'Independent finite unit-customer checks and exact algebraic polynomial identities; not a proof of extra-slot or half in general.','source':'iid_extra_slot branch exact statement, reconstructed without its code','general_polynomials_at_k_equals_8_plus_x':expanded,'results':results,'all_checks_passed':True}
out=Path(__file__).with_name('iid_support_hub_independent_audit.json');out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
