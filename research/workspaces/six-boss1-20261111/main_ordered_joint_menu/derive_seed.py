"""Main independently derives same-menu ordered-average projection; no optimization."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import hashlib
import json

P=Path(__file__).resolve().parent
W=P.parent
source=W/'all_source_joint_reweighted_safe/parameter_polytopes.json'
source_sha=hashlib.sha256(source.read_bytes()).hexdigest()
sources=json.loads(source.read_text())['sources']
atoms=list(product((0,1),repeat=9))
checks=0;tables=[];rows=[];root_proofs=[]
broot=F(1767904008200582,16877573861922720)
croot=F(337340181272013,16877573861922720)

def hidden_cost(i,p,t,q,theta,a,r):
    load=p+t+sum(r)
    value=(a*t-r[-1]-sum(theta[k]*r[k] for k in range(5-i)))/load if load else F(0)
    value+=F(sum(r[:-1]),2)+r[-1]+q/F(p+t+sum(r[:-1])+1)
    value+=sum(theta[j-i-1]*q/F(p+t+sum(r[:j-i-1])+7-j) for j in range(i+1,6))
    return value

for source_row in sources:
    i=source_row['source'];n=6-i;ci=F(n+1,2)
    for v in source_row['vertices']:
        theta=tuple(map(F,v['theta']));s=F(v['s']);a=25+sum(theta)-s
        loss=max([F(0)]+[theta[j-i-1]+sum(theta[ell-i-1]*F(1,5*(7-ell)*(8-ell)) for ell in range(j+1,6))-F(2,5) for j in range(i+1,6)])
        gp=[]
        for p in range(i):
            minimum={}
            for d in range(7):
                for t in (0,1):
                    if (d==0 and t==1) or (d==6 and t==0):continue
                    q=F(d-t,5);assert 0<=q<=1
                    values=[hidden_cost(i,p,t,q,theta,a,r) for r in product((0,1),repeat=n)]
                    minimum[d,t]=min(values);checks+=len(values)
            assert minimum[0,0]==0
            f=[]
            for d in range(1,7):
                value=F(d,6)*minimum[d,1]
                if d<6:value+=F(6-d,6)*minimum[d,0]
                f.append(value)
            assert f[0]==min(f) and all(vv>f[0] for vv in f[1:])
            closed=(ci+F(24,p+n+1)+F(1,p+1)-s/F(min(p+n+1,5))+sum(theta[j-i-1]/F(p+7-j) for j in range(i+1,6)))/6
            if p==0:closed-=F(5,6)*loss
            assert closed==f[0]
            A=ci+F(24,p+n+1)-s/F(min(p+n+1,5))
            B=minimum[1,0]
            assert minimum[1,1]==A and A>=F(227,63) and B<=F(221,720)
            for d in range(2,7):assert f[d-1]-f[0]>=F(d-1,6)*(A-B)>=F(d-1)*F(16613,30240)
            gp.append(closed)
            tables.append({'source':i,'vertex':v['id'],'p':p,'loss':str(loss),
                           'G':str(closed),'f_d1_through_d6':list(map(str,f))})
        vector={}
        for h,bits in enumerate(atoms):
            actual=bits[:6];p=sum(actual[:i-1]);o=bits[7]
            u=F(actual[i-1],sum(actual)) if sum(actual) else F(0)
            vector[str(h)]=str(a*u-o*gp[p])
        vector['512']=str(ci)
        row={'name':f'MAIN_ORDERED_MENU_{v["id"]}','source':i,'vertex':v['id'],
             'theta':list(map(str,theta)),'s':str(s),'source_IC_weight':str(a),
             'G_by_prefix':list(map(str,gp)),'a':vector,'rhs':'0','numerical_divisor':'25'}
        rows.append(row)
        if i==1:
            kweight=ci+a*broot;oweight=a*croot+kweight/6-gp[0]
            assert kweight>0 and oweight>=0
            for h in range(513):
                if h==512:u=0;o=0;k=1
                else:
                    actual=atoms[h][:6];u=F(actual[0],sum(actual)) if sum(actual) else F(0)
                    o=atoms[h][7];k=0
                assert F(vector[str(h)])==a*(u-broot*k-croot*o)+kweight*(k-F(o,6))+oweight*o
            root_proofs.append({'vertex':v['id'],'root_line_weight':str(a),'K_ge_O6_weight':str(kweight),'O_nonnegative_weight':str(oweight)})
assert checks==24192 and len(rows)==67 and len(tables)==111 and len(root_proofs)==39
assert hashlib.sha256(source.read_bytes()).hexdigest()==source_sha
for name,data in [('exact_rows.json',rows),('exact_projection_tables.json',tables),('root39_redundancy.json',root_proofs)]:
    (P/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
result={'owner':'Boss1/Main','status':'PASS','optimizer_calls':0,'parameter_source_sha256':source_sha,
        'physical_hidden_state_checks':checks,'G_tables':len(tables),'necessary_rows':len(rows),
        'full_column_coefficients':len(rows)*513,'root_redundancy_identities':39*513,
        'continuous_domain_claim':'Analytic monotonicity and exact single-middle loss proof in proof_seed.md; finite table checks only sample67 parameters.',
        'complete_continuous_family_not_yet_generated':True}
(P/'check_result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
