"""Exact checks for two explicitly targeted PB-extra interfaces.

No search is run here. The one uniform-background LP did not separate its fixed
query and strategy; its returned feasible point is audited, not promoted into a
theorem. The old 13-player packet audits the proposed two-menu expression.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import combinations_with_replacement as C
from functools import lru_cache
from math import lcm
import argparse,gzip,json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[5]
source34=ROOT/'evidence/certificates/customer_attraction/individual_security_failure.json'
d=json.loads(source34.read_text())
pol={tuple(v['history']):v['action'] for v in d['strategy']['actions']}
def finish(h):
    while len(h)<3:h=h+(pol[h],)
    return h
q=6;H=2
w={1:F(40,83),2:F(280,83),4:F(280,83),8:F(40,83),
   9:F(320,83),16:F(280,83),32:F(280,83)}
def profit(z,a):
    return sum((n/F(H+sum(bool(mask&(1<<b)) for b in z))
                for mask,n in w.items() if mask&(1<<a)),F())
checks=0;least=None
for h,a in pol.items():
    z=finish(h);chosen=profit(z,a)
    for b in range(q):
        slack=chosen-profit(finish(h+(b,)),b)
        assert slack>=0
        checks+=1;least=slack if least is None else min(least,slack)
security=[]
for rivals in C(range(q),3):
    security.append(sum((n*F(mask.bit_count(),q*(H+1+sum(bool(mask&(1<<b)) for b in rivals)))
                         for mask,n in w.items()),F()))
assert min(security)==1
z=finish(());pair=profit(z,z[0])+profit(z,z[1])
assert pair==F(560,249)>2
integer_min_card=min(sum((n*83 for mask,n in w.items() if mask&(1<<a)),F()) for a in range(q))
assert integer_min_card==280
assert integer_min_card/F(H+3)>F(1,H+1)
bg_report={'scope':'one fixed H=2/XY-strategy/uniform-query diagnostic, not PB theorem',
           'strategy_source':str(source34.relative_to(ROOT)),
           'background_per_customer':H,'remaining_players':3,
           'old_history_IC_checks':checks,'minimum_old_IC_slack':str(least),
           'query_p':['1/6']*6,'static_triples':len(security),
           'minimum_query_value':str(min(security)),
           'feasible_candidate_pair':str(pair),'pair_minus_two_query_lower_bound':str(pair-2),
           'discovery_float_objective':2.248995983935743,
           'optimizer_lower_bound_not_certified_here':True,
           'outcome':'no floating separation in this one targeted cone; stopped',
           'singleton_extension_min_card_after_integer_clearing':str(integer_min_card),
           'singleton_deviation_universal_upper':'1/3'}

source13=ROOT/'research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/security/refined_tax_k10_packet.json.gz'
d=json.loads(gzip.decompress(source13.read_bytes()))
nodes=d['nodes'];root=d['root'];inst=d['instance'];r=inst['players'];q=len(inst['topics'])
rows=[(tuple(v['topics']),v['multiplicity']) for v in inst['customers']]
den=lcm(*range(1,r+2))
@lru_cache(None)
def scaled(counts,a,entry=False):
    return sum(n*den//(int(entry)+sum(counts[j] for j in likes))
               for likes,n in rows if a in likes)
seen=set();todo=[root]
while todo:
    i=todo.pop()
    if i in seen:continue
    seen.add(i);v=nodes[i];counts=tuple(v['counts']);depth=sum(counts)
    if depth==r:assert not v.get('children')
    else:
        assert len(v['children'])==q
        for a,j in enumerate(v['children']):
            assert tuple(nodes[j]['counts'])==tuple(n+int(a==b) for b,n in enumerate(counts))
            todo.append(j)
assert len(seen)==len(nodes)
final={};source_checks=0
for i in sorted(seen,key=lambda j:sum(nodes[j]['counts']),reverse=True):
    v=nodes[i]
    if sum(v['counts'])==r:final[i]=tuple(v['counts']);continue
    a=v['action'];final[i]=final[v['children'][a]]
    for b,j in enumerate(v['children']):
        assert scaled(final[i],a)>=scaled(final[j],b)
        source_checks+=1
p=tuple(F(n,2293) for n in (200,225,200,75,75,1518))
t=F(9925,4586)
assert sum(p)==1
primary=[]
for rivals in C(range(q),r):
    c=tuple(rivals.count(a) for a in range(q))
    primary.append(sum((p[a]*F(scaled(c,a,True),den) for a in range(q)),F()))
assert min(primary)==t
dual=[((1,1,1,0,0,10),F(4571,20637)),((1,1,0,0,1,10),F(1348,20637)),
      ((1,0,0,1,1,10),F(964,6879)),((1,0,0,1,0,11),F(5674,20637)),
      ((1,0,0,0,1,11),F(1442,6879)),((0,0,0,1,1,11),F(1826,20637))]
assert sum(weight for c,weight in dual)==1
for a in range(q):assert sum((weight*F(scaled(c,a,True),den) for c,weight in dual),F())==t
Astar=nodes[root]['action'];after=nodes[root]['children'][Astar]
u1=F(scaled(final[root],Astar),den);u2=F(scaled(final[after],nodes[after]['action']),den)
K1=[];K2=[];D1=[];D2=[]
for a in range(q):
    qa=final[nodes[root]['children'][a]]
    q1=list(qa);q1[a]-=1;q1[Astar]+=1;q1=tuple(q1)
    q2=final[nodes[after]['children'][a]]
    assert sum(q1)==sum(q2)==r
    K1.append([F(scaled(q1,T,True),den) for T in range(q)])
    K2.append([F(scaled(q2,T,True),den) for T in range(q)])
    D1.append(F(scaled(qa,a),den));D2.append(F(scaled(q2,a),den))
    assert K1[a][a]<=D1[-1]<=u1
    assert K2[a][a]<=D2[-1]<=u2
C1=sum((p[a]*p[T]*K1[a][T] for a in range(q) for T in range(q)),F())
C2=sum((p[a]*p[T]*K2[a][T] for a in range(q) for T in range(q)),F())
d1=sum((p[a]*D1[a] for a in range(q)),F());d2=sum((p[a]*D2[a] for a in range(q)),F())
assert C1+C2==F(23222825,5257849)<u1+u2
assert (u1+u2)-(C1+C2)==(u1-d1)+(u2-d2)+(d1-C1)+(d2-C2)
menu_report={'scope':'one unchanged old full SPE, one exact safe-optimal p, no general bound',
             'source':str(source13.relative_to(ROOT)),'nodes':len(nodes),
             'original_IC_checks':source_checks,'players':r,
             'static_rival_multisets':len(primary),'safe_value':str(t),
             'primary':list(map(str,p)),
             'dual':[{'counts':list(c),'weight':str(weight)} for c,weight in dual],
             'first_pair':[str(u1),str(u2)],'C1':str(C1),'C2':str(C2),
             'pair_minus_Csum':str(u1+u2-C1-C2),
             'outcome':'two-menu sufficient inequality not separated at this old packet; stopped'}
out={'background_probe':bg_report,'two_menu_probe':menu_report}
parser=argparse.ArgumentParser();parser.add_argument('--output');args=parser.parse_args()
if args.output:
    dest=(HERE/args.output).resolve();assert dest.parent==HERE
    with dest.open('x') as file:json.dump(out,file,indent=2);file.write('\n')
print(json.dumps({'background':bg_report,'two_menu':{k:v for k,v in menu_report.items() if k not in ('primary','dual')}},indent=2))
