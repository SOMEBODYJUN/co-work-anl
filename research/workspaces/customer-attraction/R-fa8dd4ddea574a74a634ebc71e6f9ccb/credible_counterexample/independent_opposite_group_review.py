"""Independent definition-level reconstruction of the six-query identities.

No author checker or discovery code is imported. Formula rows are reconstructed
from a full ordered-history policy and 1/(b+load), then compared to the proposed
binary four-term tax, rather than merely checked for a nonnegative residual.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import sys

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'customer_attraction/__init__.py').exists())
AUTHOR=HERE.parent/'aggregate_security'
sys.path.insert(0,str(ROOT))
from customer_attraction import Instance, CustomerType, StrategyCertificate, verify_certificate

LABELS=tuple(range(6));X=frozenset((0,1,2));Y=frozenset((3,4,5))
policy={():0}
for first in LABELS:
    policy[first,]=3 if first in X else 0
    for second in LABELS:
        policy[first,second]=min((X if second in X else Y)-{first,second})
assert len(policy)==43


def follow(history):
    current=tuple(history)
    while len(current)<3:current+=policy[current],
    return current


def add(*vectors):return tuple(sum(entries) for entries in zip(*vectors))
def neg(vector):return tuple(-x for x in vector)
ZERO=(0,0,0,0)


def payoff(action,terminal,mask):
    """Coefficients of 1/(b+j), j=0,1,2,3; j=0 never occurs."""
    if action not in mask:return ZERO
    denominator=sum(label in mask for label in terminal)
    assert 1<=denominator<=3
    return tuple(int(j==denominator) for j in range(4))


def gamma(history,deviation,mask):
    return add(payoff(policy[history],follow(history),mask),
               neg(payoff(deviation,follow(history+(deviation,)),mask)))


def polynomial(vector):
    """Multiply rational row by D(b)=(b+1)(b+2)(b+3)."""
    out=[0,0,0]
    assert vector[0]==0
    for denominator,coefficient in enumerate(vector[1:],1):
        remaining=[j for j in (1,2,3) if j!=denominator]
        a,b=remaining
        for i,x in enumerate((a*b,a+b,1)):out[i]+=coefficient*x
    return tuple(out)


TABLE={
 0:(((),3),((0,),1),((0,2),0),((1,5),0)),
 1:(((),3),((0,),1),((0,4),1)),
 2:(((),3),((0,),1),((0,5),2),((3,0),2)),
 3:(((),3),((0,),1),((0,2),3)),
 4:(((),4),((0,),1),((0,2),4)),
 5:(((),5),((0,),1),((0,2),5)),
}
TAX={0:(1,0,3,5),1:(0,1,3,4),2:(0,2,3,5)}
root=follow(())
assert root==(0,3,4)
source=json.loads((AUTHOR/'group3_background_exact_certificate.json').read_text())
expected_lambdas={(a,h,b) for a,rows in TABLE.items() for h,b in rows}
actual_lambdas={(row['a'],tuple(row['h']),row['b']) for row in source['lambda']}
assert expected_lambdas==actual_lambdas and all(F(row['value'])==1 for row in source['lambda'])
assert [(tuple(row['B']),F(row['p'])) for row in source['Q']]==[((0,1),F(1,2)),((0,2),F(1,2))]
saved={(row['a'],row['mask']):tuple(map(F,row['coefficients'])) for row in source['remainders']}

nonzero={a:0 for a in LABELS};identity_count=0
for membership in product((0,1),repeat=6):
    mask=frozenset(i for i,x in enumerate(membership) if x)
    mask_number=sum(1<<i for i in mask)
    budget=add(payoff(0,root,mask),payoff(3,root,mask))
    for query,rows in TABLE.items():
        e=add(budget,neg(payoff(query,(0,1,query),mask)),
              neg(payoff(query,(0,2,query),mask)))
        residual=add(e,*[neg(gamma(h,b,mask)) for h,b in rows])
        if query in TAX:
            background,A,B,D=TAX[query]
            # Reconstruct R from its four payoffs, including the background
            # theme as a separate occurrence even if labels coincide.
            four=add(payoff(B,(background,B,A),mask),
                     neg(payoff(B,(background,B,D),mask)),
                     payoff(A,(background,A,D),mask),
                     neg(payoff(A,(background,A,A),mask)))
            signed=(int(A in mask)-int(B in mask))*(int(A in mask)-int(D in mask))
            assert signed>=0
            # D(b)*delta_{b+1_background} is b+3 or b+1.
            factor=1 if background in mask else 3
            expected=(signed*factor,signed,0)
            assert polynomial(four)==expected
        else:
            expected=(0,0,0)
        assert polynomial(residual)==expected,(query,membership,residual,expected)
        if mask_number:assert saved[query,mask_number]==expected
        nonzero[query]+=any(expected)
        identity_count+=1

# The cyclic difference used for query 2 vanishes as a rational row, before
# clearing denominators, for every one of the 64 membership patterns.
for membership in product((0,1),repeat=6):
    mask=frozenset(i for i,x in enumerate(membership) if x)
    cyclic=add(payoff(3,(0,1,3),mask),neg(payoff(1,(0,1,3),mask)),
               payoff(1,(0,1,2),mask),neg(payoff(2,(0,1,2),mask)),
               payoff(2,(0,2,3),mask),neg(payoff(3,(0,2,3),mask)))
    assert cyclic==ZERO

# A nonzero legal unit-customer instance shows that the fixed-policy SPE cone
# is nonempty. This extra canonical check is not used in the identity proof.
inst=Instance(tuple(str(i) for i in LABELS),tuple(CustomerType(frozenset(i for i in LABELS if mask>>i&1))
              for mask in range(1,64)),3)
cert=StrategyCertificate(policy,inst.counts(root,terminal=True))
verified=verify_certificate(inst,cert);verified.assert_valid()
report={
 'review_status':'independent analytic and exact coefficient reconstruction passed; no fatal objection',
 'scope':'fixed complete six-label opposite-group three-player policy, arbitrary per-customer b>=0, nonnegative masses, satisfying all full-history SPE inequalities',
 'root':root,'ordered_policy_nodes':len(policy),'full_nontrivial_incentives':len(policy)*5,
 'query_indexed_nonnegative_incentive_occurrences':len(expected_lambdas),
 'distinct_used_nonnegative_incentives':len({(h,b) for a,h,b in expected_lambdas}),
 'query_membership_identities':identity_count,
 'checked_polynomial_coefficients':identity_count*3,
 'nonzero_remainders_by_query':nonzero,
 'Q':[{'B':[0,1],'p':'1/2'},{'B':[0,2],'p':'1/2'}],
 'four_term_tax':'R=delta*(1_A-1_B)*(1_A-1_D)>=0 pointwise',
 'canonical_nonempty_cone_check':{'unit_customers':63,'histories':verified.checked_histories,
                                'deviations':verified.checked_deviations,'valid':verified.valid},
 'source_hashes':{name:hashlib.sha256((AUTHOR/name).read_bytes()).hexdigest()
                  for name in ('opposite_group_pair_payment.md','group3_background_exact_certificate.json')},
 'review_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'not_proved':['general first-two inequality','arbitrary policy cones','more than six labels','general half coverage']}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
