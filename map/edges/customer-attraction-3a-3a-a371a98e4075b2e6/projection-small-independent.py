"""Exact 56-cell small-weight projection audit from the five labeled IC rows.

The universal row semantics and the max direction are proved in the two cited
mathematical bodies. This script covers only their complete finite coefficient
domain; it imports neither the author nor the previous independent generator.
It never imports or builds the old 701/702-row system and does not solve an LP.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from hashlib import sha256
import json

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
WORDS=tuple(product((0,1),repeat=3))
WEIGHTS=(72,8,1,2,3)

def comp(n,k):
    if k==1:
        yield (n,)
    else:
        for i in range(n+1):
            for rest in comp(n-i,k-1):
                yield (i,)+rest

def menus(d):
    for h0 in comp(6-d,4):
        for h1 in comp(d,4):
            yield tuple(w for count,w in zip(h0+h1,WORDS) for _ in range(count))

def share(n,d):
    if n==0:return 0
    assert d>0 and 60%d==0
    return n*(60//d)

def rows(p,P,menu):
    # Actual representative has a5=a6=0, hence H*=0; a4=P-p.
    u4=F(P-p,P) if P>p else F()
    r=[int(360*u4),0,0,0,0]
    for i,(t,b,c) in enumerate(menu):
        den=p+t+b+c
        own_t=share(t,den)
        own_c=share(c,den)
        own_H=share(b+c,den)+share(b,(p+t+1)*(p+t+2))
        r[0]-=own_t
        r[1]-=share(b+c,P+1)-share(b*c,(P+1)*(P+2))
        for j,(_,bj,cj) in enumerate(menu):
            r[3]+=own_c-share(cj,p+t+b+1)
            if i!=j:
                r[2]+=own_c-share(bj,p+t+b+1)
                r[4]+=own_H-share(bj+cj,p+t+1)+share(bj*cj,(p+t+1)*(p+t+2))
    return tuple(r)

body=ROOT/'archives/customer-attraction/state/资源/第四源索引投影的作者实现小权预算与七百零二行组合--资源.md'
expected={}
for line in body.read_text().splitlines():
    z=line.strip().strip('|').split('|')
    if len(z)==9 and z[0] in {'0','1','2','3'} and z[1] in {'0','1','2','3','4'}:
        p,P=map(int,z[:2])
        for d,v in enumerate(z[2:]):expected[p,P,d]=F(v.replace("−","-"))
assert len(expected)==56
families=[tuple(menus(d)) for d in range(7)]
assert list(map(len,families))==[84,224,350,400,350,224,84]
result=[];cases=0;lookup={}
for p in range(4):
    for P in (p,p+1):
        u4=F(P-p,P) if P>p else F()
        for d,family in enumerate(families):
            best=None;arg=None
            for menu in family:
                v=sum(w*r for w,r in zip(WEIGHTS,rows(p,P,menu)))
                cases+=1
                if best is None or v>best:best,arg=v,menu
            psi=72*u4-F(best,360)
            assert psi==expected[p,P,d],(p,P,d,psi,expected[p,P,d])
            lookup[p,P,d]=psi
            hist=[arg.count(w) for w in WORDS]
            result.append({'p':p,'P':P,'d':d,'psi':str(psi),'maximum_scaled_weighted_row':best,'maximizer_histogram':hist})
assert cases==8*1716
point_path=ROOT/'archives/customer-attraction/tools/evidence/R964-parent-fourth-projection-and-combined-702-five-primary/original/62b9a6c6d47995ee269d/research/workspaces/customer-attraction/R-964def22ed03479582e83410444f2ea2/parent/combined_702.json'
point=json.loads(point_path.read_text())
coeff_path=ROOT/'archives/customer-attraction/tools/evidence/R964-parent-fourth-projection-and-combined-702-five-primary/original/b62dfdc807c4b60b5083/research/workspaces/customer-attraction/R-964def22ed03479582e83410444f2ea2/parent/fourth_indexed_projection.json'
v1=json.loads(coeff_path.read_text());coeff={(z['actual_bits'],z['d']):int(z['coefficient']) for z in v1['coefficients']}
O=W=budget=rhs=v1raw=F()
for z in point['support']:
    a=tuple(map(int,z['actual_bits']));mass=F(z['weight']);c=sum(a);p=sum(a[:3]);P=sum(a[:4]);d=z['d']
    O+=mass*(d>0);W+=mass*(c>0)
    u4=F(a[3],c) if a[3] else F()
    H=(F(a[4]+a[5],c) if a[4]+a[5] else F())+F(a[4],(P+1)*(P+2))
    budget+=mass*(72*u4+8*H)
    rhs+=mass*lookup[p,P,d]
    v1raw+=mass*coeff[z['actual_bits'],d]
assert O==1 and W==F(point['W']) and W<F(1,2)
assert budget-rhs>=0 and v1raw>=0
report={'status':'exact independent 56-cell reconstruction; point-substitution-only-not-702-reverification',
 'weights':WEIGHTS,'scale':60,'cells_checked':56,'joint_histograms_per_d':list(map(len,families)),
 'labeled_row_cases':cases,'comparison_body_sha256':sha256(body.read_bytes()).hexdigest(),
 'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),'all_cells':result,
 'combined_702_substitution':{'point_sha256':sha256(point_path.read_bytes()).hexdigest(),'projection_report_sha256':sha256(coeff_path.read_bytes()).hexdigest(),'O':str(O),'W':str(W),'twice_W_minus_O':str(2*W-O),'v1_raw_row':str(v1raw),'small_budget':str(budget),'small_rhs':str(rhs),'small_slack':str(budget-rhs)},
 'limits':'No old 701 rows built or checked, no exact optimum, no full SPE realization; universal necessary inequality follows from five true IC rows and the complete max projection, not from this point.'}
(BASE/'projection-small-independent.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='all_cells'},ensure_ascii=False,indent=2))
