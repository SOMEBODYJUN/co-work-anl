"""Independent definition-level review of the waterfill credibility obstruction.
Reads only frozen input/strategy/security data; imports no author or solver code.
"""
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
from functools import lru_cache
from pathlib import Path
from collections import defaultdict
import hashlib,json
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'tail'
paths={name:SOURCE/name for name in ['endogenous_53_instance.json','endogenous_53_strategy.json','endogenous_53_security.json']}
game=json.loads(paths['endogenous_53_instance.json'].read_text())
packet=json.loads(paths['endogenous_53_strategy.json'].read_text())
security=json.loads(paths['endogenous_53_security.json'].read_text())
k=len(game['topics']);m=game['players'];assert (k,m)==(7,4)
units=[]
for row in game['customers']:
    assert type(row['multiplicity']) is int and row['multiplicity']>0
    units.extend([frozenset(row['topics'])]*row['multiplicity'])
assert len(units)==53
policy={tuple(row['history']):row['action'] for row in packet['actions']}
histories=[h for depth in range(m) for h in product(range(k),repeat=depth)]
assert set(policy)==set(histories) and len(policy)==len(packet['actions'])==400
@lru_cache(None)
def finish(h):
    return h if len(h)==m else finish((*h,policy[h]))
def unit(label,z,weights=None,extra=F(0)):
    weights=[F(1)]*len(z) if weights is None else list(map(F,weights))
    return sum((F(1)/(F(extra)+sum((weights[i] for i,a in enumerate(z) if a in likes),F(0))) for likes in units if label in likes),F(0))
def profits(z,weights=None):
    weights=[F(1)]*len(z) if weights is None else list(map(F,weights))
    return [weights[i]*unit(a,z,weights) if weights[i]>0 else F(0) for i,a in enumerate(z)]
slacks=[]
for h in histories:
    actual=profits(finish(h))[len(h)]
    for a in range(k):
        value=profits(finish((*h,a)))[len(h)]
        assert actual>=value,(h,a,actual,value)
        slacks.append(actual-value)
assert len(slacks)==2800 and min(slacks)==0
actual=finish((6,));deviation=finish((6,2))
assert actual==(6,0,3,4) and deviation==(6,2,3,4)
assert profits(actual)==[F(19),F(29,3),F(67,6),F(67,6)]
assert profits(deviation)==[F(19),F(29,3),F(35,3),F(35,3)]
p=list(map(F,security['primary']));Q=[(tuple(row['rivals']),F(row['probability'])) for row in security['dual']]
t=F(security['value']);assert t==F(28481,2924)
assert min(p)>=0 and sum(p)==1 and all(w>0 for _,w in Q) and sum(w for _,w in Q)==1
rivals=list(combinations_with_replacement(range(k),3));assert len(rivals)==84
primary=[sum((p[a]*unit(a,q,extra=1) for a in range(k)),F(0)) for q in rivals]
dual=[sum((w*unit(a,q,extra=1) for q,w in Q),F(0)) for a in range(k)]
assert min(primary)==t and set(dual)=={t}
D=t-F(29,3);assert D==F(647,8772)
assert F(67,6)>t and F(35,3)>t and F(19)>t
buckets={}
for a in [0,2]:
    bins=defaultdict(int)
    for likes in units:
        if a in likes:bins[int(3 in likes)+int(4 in likes)]+=1
    buckets[a]=[bins[i] for i in range(3)]
assert buckets=={0:[0,12,11],2:[1,12,8]}
# A current last-player utility has the form C+A/(rho+1)+B/(rho+2).
def last_coeff(third,label):
    cf=[F(0),F(0),F(0)]
    for likes in units:
        if label not in likes:continue
        fixed=1+int(6 in likes)+int(third in likes)
        if 0 in likes:
            assert fixed in [1,2]
            cf[fixed]+=1
        else:cf[0]+=F(1,fixed)
    return tuple(cf)
def difference(x,y):return tuple(a-b for a,b in zip(x,y))
def numerator(cf):
    C,A,B=cf
    return (2*C+2*A+B,3*C+A+B,C)
def bernstein2(poly):
    c0,c1,c2=poly
    return (c0,c0+c1/2,c0+c1+c2)
last_tables={};poly_tables={}
for third,winner in [(3,4),(1,2)]:
    vals=[last_coeff(third,a) for a in range(k)]
    gaps=[difference(vals[winner],v) for v in vals]
    polys=[numerator(cf) for cf in gaps]
    for a,poly in enumerate(polys):
        if a==winner:assert poly==(0,0,0);continue
        if third==1 and a==0:
            assert poly==(F(-1),F(9,2),F(11,2)) # (rho+1)(11rho-2)/2
        else:
            bc=bernstein2(poly)
            assert min(bc)>=0 and max(bc)>0,(third,a,poly,bc)
    last_tables[third]=[list(map(str,cf)) for cf in vals]
    poly_tables[third]=[list(map(str,poly)) for poly in polys]
# Complete boundary check, including all weak ties.
for rho,br_actual,br_deviation in [(F(0),[4],[0]),(F(2,11),[4],[0,2]),(F(1),[1,2,4,5],[2])]:
    for third,expected in [(3,br_actual),(1,br_deviation)]:
        vals=[unit(a,(6,0,third,a),(1,rho,1,1)) for a in range(k)]
        assert [a for a,v in enumerate(vals) if v==max(vals)]==expected
# Root flip and third-player flip; common-core density cancels in each comparison.
rho_checks=[]
for rho in [F(1),F(9,10),F(3,4),F(1,2),F(2,11),F(1,10)]:
    ws=(1,rho,1,1)
    root_delta=unit(0,actual,ws)-unit(2,deviation,ws)
    expected=F(3)/(rho+2)-1/rho
    assert root_delta==expected==2*(rho-1)/(rho*(rho+2))
    assert rho*root_delta==2*(rho-1)/(rho+2)
    third_delta=unit(3,(6,0,3,4),ws)-unit(1,(6,0,1,2),ws)
    assert third_delta==3*(rho-1)/((rho+1)*(rho+2))
    if rho<1:assert root_delta<0 and third_delta<0
    else:assert root_delta==third_delta==0
    for core in [0,1,10,1000]:
        common=F(core)/(rho+3)
        assert (unit(0,actual,ws)+common)-(unit(2,deviation,ws)+common)==root_delta
        assert (unit(3,(6,0,3,4),ws)+common)-(unit(1,(6,0,1,2),ws)+common)==third_delta
    rho_checks.append(dict(rho=str(rho),root_unit_delta=str(root_delta),root_profit_delta=str(rho*root_delta),third_delta=str(third_delta)))
def qX0(rho,core=0):return F(12)/(rho+2)+F(11+core)/(rho+3)
assert qX0(F(1))==F(27,4) and qX0(F(0))==F(29,3)
assert qX0(F(0))-qX0(F(1))==F(35,12)>D
assert qX0(F(2,11))-qX0(F(1))==F(309,140)>D
for core in [0,1,10,1000]:
    assert qX0(F(0),core)-qX0(F(1),core)==F(35,12)+F(core,12)>D
    assert qX0(F(2,11),core)-qX0(F(1),core)==F(309,140)+F(9*core,140)>D
    U1=F(12,2)+F(11,3)+F(core,4)
    assert (t+F(core,4))-U1==D
# The query refund is strictly decreasing on [0,1], since both reciprocal terms are.
# Exact polynomial identities and positive Bernstein coefficients above certify all rho regions.
# Positive repair outside the old high-tail-preservation contract: scale all three tails.
lam=F(84796,85443)
assert lam==F(29,3)/t and 0<lam<1
uniform_weights=(1,lam,lam,lam)
uniform_slacks=[]
for h in histories:
    if h and h[0]==6:
        current=profits(finish(h),uniform_weights)[len(h)]
        for a in range(k):
            other=profits(finish((*h,a)),uniform_weights)[len(h)]
            assert current>=other
            uniform_slacks.append(current-other)
assert len(uniform_slacks)==399 and min(uniform_slacks)==0
unit_tail=[unit(actual[i],actual,uniform_weights) for i in range(1,4)]
assert min(unit_tail)==t
# Root P is removed and a unit query is inserted, as in waterfill Q_T.
old_tail=(0,3,4)
def tail_query(a,weight):
    return sum((F(1)/(1+weight*sum(j in likes for j in old_tail)) for likes in units if a in likes),F(0))
uniform_returns=[tail_query(a,lam)-tail_query(a,F(1)) for a in range(k)]
H=sum((F(1)/(1+lam*sum(j in likes for j in old_tail))-F(1,1+sum(j in likes for j in old_tail)) for likes in units),F(0))
assert max(uniform_returns)==F(187117307516351,4918136562477105)<D
assert H==F(206474219394865,3934509249981684)<D
# All-core analytic repair: g_c(lambda)=u/lambda+c/(1+3lambda).
load_counts=defaultdict(int)
for likes in units:
    load_counts[sum(a in likes for a in old_tail)]+=1
assert [load_counts[j] for j in [1,2,3]]==[6,15,11]
S=sum((F(load_counts[j]*j,(1+j)**2) for j in [1,2,3]),F(0))
assert S==F(331,48) and F(29,3)-S==F(133,48)
assert all(policy[h]!=6 for h in histories if h and h[0]==6)
# A deviation to P after first P has s>=1 tail P choices; scaling improves the gap.
for s_count in range(1,4):
    for weight in [F(1),lam,F(1,2),F(1,10)]:
        correction=F(19,1+s_count)-19*weight/(1+weight*s_count)
        assert correction==19*(1-weight)/((1+s_count)*(1+weight*s_count))>=0
core_repairs=[]
for core in [0,1,10,1000,10**6]:
    target=t+F(core,4)
    def density(weight):return F(29,3)/weight+F(core)/(1+3*weight)
    low,high=lam,F(1)
    assert density(low)>=target and density(high)<target
    if core==0:high=low
    else:
        for _ in range(120):
            middle=(low+high)/2
            if density(middle)>target:low=middle
            else:high=middle
    def pool(weight):
        return sum((F(load_counts[j])*(F(1)/(1+j*weight)-F(1,1+j)) for j in [1,2,3]),F(0))+F(core)/(1+3*weight)-F(core,4)
    H_upper=pool(low)
    assert H_upper<D
    for weight in [low,high]:
        old_pool=pool(weight)-(F(core)/(1+3*weight)-F(core,4))
        assert old_pool<=S*(1/weight-1)
        V=32+3*weight*F(core)/(1+3*weight)
        residual=density(weight)-target
        assert V-3*weight*target-3==3*weight*residual
    core_repairs.append(dict(c=core,lambda_lower=str(low),lambda_upper=str(high),H_upper=str(H_upper),credit=str(D),exact_tail_budget_slack='3 at the unique water root'))
repair=dict(scope='all nonnegative integer c analytically; c=0 also exact packet replay; drops original-high-tail-must-stay-1 condition',lambda_value=str(lam),child_comparisons=len(uniform_slacks),minimum_slack=str(min(uniform_slacks)),tail_unit_densities=list(map(str,unit_tail)),maximum_query_refund=str(max(uniform_returns)),global_customer_query_pool=str(H),credit=str(D),old_load_counts=[6,15,11],old_pool_bound_coefficient=str(S),credit_strict_margin_coefficient='133/48',core_repairs=core_repairs)
# Exact all-lambda obstruction outside the protected P child.
assert policy[(0,0,6)]==1
full_flip_bins=defaultdict(int)
for likes in units:
    for label,sign in [(1,1),(2,-1)]:
        if label in likes:
            root_load=int(0 in likes)
            tail_load=int(0 in likes)+int(6 in likes)+1
            full_flip_bins[root_load,tail_load]+=sign
full_flip_bins={key:value for key,value in full_flip_bins.items() if value}
assert full_flip_bins=={(1,2):3,(0,1):-1}
assert 3*lam/(1+2*lam)-1==(lam-1)/(1+2*lam)==F(-647,255035)
full_flip=dict(history=[0,0,6],prescribed=1,deviation=2,buckets=[dict(root_load=a,tail_load=b,coefficient=v) for (a,b),v in sorted(full_flip_bins.items())],profit_delta='(lambda-1)/(1+2lambda)',at_lambda0='-647/255035',scope='Other root X0 child violates the protected interface avoidance condition')
out=dict(status='PASS: same-tree IC flip and impossibility of retaining the original waterfill leaf; not failure of waterfill algebra or weighted-SPE existence',sources={name:hashlib.sha256(path.read_bytes()).hexdigest() for name,path in paths.items()},broader_uniform_repair=repair,whole_tree_flip=full_flip,customers=53,nodes=len(histories),comparisons=len(slacks),minimum_unit_SPE_slack=str(min(slacks)),actual=actual,actual_payoffs=list(map(str,profits(actual))),deviation=deviation,deviation_payoffs=list(map(str,profits(deviation))),static_backgrounds=len(rivals),security_value=str(t),deficit=str(D),buckets=buckets,last_utility_coefficients_C_A_B=last_tables,last_gap_numerators_const_rho_rho2=poly_tables,rho_checks=rho_checks,query_refund_at_zero=str(F(35,12)),query_refund_at_2_over_11=str(F(309,140)),query_credit=str(D),critical_interval='2/11 < rho < 1',boundary_BR={'rho=0':{'after_P_X0_Y0':[4],'after_P_X0_X1':[0]},'rho=2/11':{'after_P_X0_Y0':[4],'after_P_X0_X1':[0,2]},'rho=1':{'after_P_X0_Y0':[1,2,4,5],'after_P_X0_X1':[2]}})
(HERE/'waterfill_credibility_review_audit.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({key:out[key] for key in ['status','customers','nodes','comparisons','minimum_unit_SPE_slack','security_value','deficit','actual','actual_payoffs','deviation','deviation_payoffs','critical_interval','query_refund_at_zero','query_refund_at_2_over_11']},indent=2))
