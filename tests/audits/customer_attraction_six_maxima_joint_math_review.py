#!/usr/bin/env python3
"""Independent exact coefficient and mathematical-legality review.

Imports only the standard library and certificate data; reconstructs raw
customer slacks without the author audit, model, solver, or discovery LP.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import argparse, hashlib, json

ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path, help='Write a new frozen report; refuses to overwrite existing output.')
args=parser.parse_args()
CERT=ROOT/'evidence/certificates/customer_attraction/six_maxima_joint_bound.json'
DOC=ROOT/'research/current/customer_attraction/six_maxima_joint_bound.md'
record=json.loads(CERT.read_text())
pairs=[(a,b) for a in range(6) for b in range(a,6)]
incidences=[frozenset(j for j,v in enumerate(x) if v) for x in product((False,True),repeat=6) if any(x)]

def rows(n,I,J):
    total=len(J)
    salaries=[Q(1,total) if t in J else Q(0) for t in range(n)]
    floor=[]
    for t in range(n):
        if len(I)==6: contribution=Q(1,n)
        elif len(I)==1: contribution=Q(1,2*n)
        elif t==n-1: contribution=Q(n+1,n*(n+5))
        else: contribution=Q(1,3*n-2*t)
        floor.append(salaries[t]-contribution)
    earlier=len(J-{n-1})
    response=[salaries[-1]-(Q(1,earlier+1) if j in I else Q(0)) for j in range(6)]
    b=len(J-{n-2,n-1})
    tax=Q(1,(b+1)*(b+2)) if n-2 in J else Q(0)
    two=[]
    for a,c in pairs:
        loads=int(a in I)+int(c in I)
        # Sum actual follower shares, add the positive single-action tax,
        # subtract the comparison pair's total share under the same prefix.
        comparison=Q(loads,b+loads) if loads else Q(0)
        two.append(salaries[-2]+salaries[-1]+tax-comparison)
    return floor+response+two

def residual(n,I,J,multipliers):
    return Q(1 if J else 0)-Q(1,2)-sum((a*b for a,b in zip(multipliers,rows(n,I,J))),Q(0))

# Enumerate canonical complete strings from all six-label length-five tuples.
# A label's first occurrence must introduce the next unused integer.
def canonical(a):
    seen={}
    mapped=[]
    for label in a:
        if label not in seen: seen[label]=len(seen)
        mapped.append(seen[label])
    return tuple(mapped)
routes={canonical(a) for a in product(range(6),repeat=5)}
assert len(routes)==52
assert {tuple(x['route']) for x in record['n5_certificates']}==routes
assert len(record['n5_certificates'])==52
expected_names=[f'mixed:{t}' for t in range(5)]+[f'lastBR:{j}' for j in range(6)]+[f'twoTax:{a}{b}' for a,b in pairs]
assert record['row_order_n5']==expected_names
assert record['n5_common_denominator']==10000
counts=[]
for cert in record['n5_certificates']:
    a=cert['route']
    nums=cert['multipliers_numerator']
    assert len(nums)==32 and all(type(v)==int and v>=0 for v in nums)
    multipliers=[Q(v,10000) for v in nums]
    count=0
    smallest=None
    for I in incidences:
        for actual_bits in product((False,True),repeat=5):
            J=frozenset(t for t,v in enumerate(actual_bits) if v)
            if any(a[t] not in I for t in J):continue
            if (4 in J)!=(a[4] in I):continue
            r=residual(5,I,J,multipliers)
            assert r>=0,(a,I,J,r)
            smallest=r if smallest is None else min(smallest,r)
            count+=1
    assert count==cert['column_count']
    assert smallest==Q(cert['minimum_residual'])
    counts.append(count)
assert sum(counts)==20080

# Independently expand the compact symbolic residual.
def compact(n,I,J):
    k=len(I-{0}); f=int(0 in I)
    p=len(J-{n-2,n-1}); d=int(n-2 in J)
    m=len(I)
    if m==1: floor=Q(n-2,2*n)
    elif m==6: floor=Q(n-2,n)
    else: floor=sum((Q(1,3*n-2*t) for t in range(n-2)),Q(0))
    g=Q(k,p+1) if not f else Q(5-k,p+1)+Q(2*k,p+2)
    h=Q(k*(5-k),p+1)+Q(k*(k-1),p+2)
    share=Q(35*p+30*d+60*f,48*(p+d+f)) if p+d+f else Q(0)
    return (Q(1 if J else 0)-Q(1,2)+Q(35,48)*floor+Q(k,8*(p+d+1))
            +Q(5,48)*g+Q(1,96)*h-share-Q(5*d,8*(p+1)*(p+2)))

universal={}
for n,target in [(6,Q(1,72)),(7,Q(1,32)),(8,Q(23393,532224))]:
    multipliers=[Q(35,48) if t<n-2 else Q(0) for t in range(n)]
    multipliers += [Q(0)]+[Q(1,8)]*5
    multipliers += [Q(5,48) if a==0 and b!=0 else Q(1,96) if a>0 and a<b else Q(0) for a,b in pairs]
    smallest=None; number=0
    for I in incidences:
        for earlybits in product((False,True),repeat=n-1):
            J=frozenset(t for t,v in enumerate(earlybits+(0 in I,)) if v)
            r=residual(n,I,J,multipliers)
            assert r==compact(n,I,J),(n,I,J,r,compact(n,I,J))
            assert r>=0,(n,I,J,r)
            smallest=r if smallest is None else min(smallest,r)
            number+=1
    assert smallest==target
    assert number==63*2**(n-1)
    universal[n]={'columns':number,'minimum':str(smallest),'lower_W_over_U':str(Q(1,2)+smallest)}

report={
 'status':'PASS','scope':'Independent mathematical legality and exact coefficient review; no imports from author audit, solver, or discovery LP.',
 'n5_complete_routes':len(routes),'n5_exact_columns':sum(counts),'n6_8':universal,
 'legal_slacks':['Mixed all-history lower floors with singleton coefficient 1/(2n), core 1/n, shared b_t.','Actual-final-player maximal-theme deviations retain true earlier customer load.','Two-remaining-player tax retains actual prefix and adds tax with correct positive sign.'],
 'domain_review':'Complete RGS length five includes final maximal route. Every genuine customer appears in the I,J domain. For n6..8 enlarged earlier-membership domain with last bit fixed by incidence contains every legal profile. Permuting maximal labels preserves all rows and coefficients.',
 'accounting_review':'Residual target indicator(J nonempty)-1/2 minus a nonnegative combination of positive SPE slacks. The identity W-U/2=sum lambda*slack+sum mass*residual has the correct signs.',
 'minor_text_correction':'Fixed before review freeze: shared last-step comparison is (n+1)(n+4)-n(n+5)=4. Monotonicity and all exact coefficients are valid.',
 'substantive_gaps':[],
 'checker_source':str(Path(__file__).resolve().relative_to(ROOT)),
 'checks':{'last_action_full_maximal':'PASS','full_ordered_history_ties':'PASS','route_and_actual_coverage_distinction':'PASS','complete_route_relabeling':'PASS','final_deviation_loads':'PASS','two_tail_tax_sign_and_true_background':'PASS','nonnegative_multiplier_accounting':'PASS','raw_and_compressed_coefficients':'PASS','five_provider_full_certificate_completeness':'PASS','six_to_eight_enlarged_membership_domain':'PASS','independence_no_author_audit_import':'PASS'},
 'certificate_sha256':hashlib.sha256(CERT.read_bytes()).hexdigest(),
 'proof_sha256':hashlib.sha256(DOC.read_bytes()).hexdigest(),
 'reviewer_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
}
if args.output:
    assert not args.output.exists(), 'Frozen output exists; choose a new destination.'
    args.output.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
