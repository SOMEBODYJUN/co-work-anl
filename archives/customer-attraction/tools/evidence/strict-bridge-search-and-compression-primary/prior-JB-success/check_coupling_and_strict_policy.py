"""One new exact definition entry. Original coupling CLI unavailable and unexecuted.
Analytic universal claims are proved separately; finite scopes are explicit here.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from math import factorial
import json
E=Path(__file__).resolve().parent;OUT=E/'new-coupling-and-strict-policy.json'
assert not OUT.exists(),'do not rerun a successful entry'

def uq(w,t,q):return sum((F(mass,sum(q[j] for j in range(len(q)) if mask>>j&1)) for mask,mass in w.items() if mask>>t&1),F())
def cov(w,z):return sum((mass for mask,mass in w.items() if any(mask>>a&1 for a in z)),F())
def cnt(z,p):return tuple(z.count(a) for a in range(p))
def compositions(n,p):
 if p==1:return [(n,)]
 return [(k,)+q for k in range(n+1) for q in compositions(n-k,p-1)]
def sharp(w,p,m):
 qs=compositions(m,p);items=[]
 for t in range(p):
  for q in qs:
   if not q[t]:continue
   for r in qs:
    if not r[t]:continue
    k=max(F(sum(r[j] for j in range(p) if mask>>j&1),sum(q[j] for j in range(p) if mask>>j&1)) for mask in range(1,1<<p) if mask>>t&1)
    gap=k*uq(w,t,r)-uq(w,t,q);assert gap>=0
    items.append({'t':t,'q':q,'r':r,'kappa':str(k),'slack':str(gap)})
 return items

def policy_audit(w,p,m,policy,strict=False,static=False):
 def leaf(h):
  while len(h)<m:h=h+(policy(h),)
  return h
 rows=[]
 for d in range(m):
  for h in product(range(p),repeat=d):
   z=leaf(h);base=uq(w,z[d],cnt(z,p))
   for a in range(p):
    zz=leaf(h+(a,));alt=uq(w,a,cnt(zz,p));gap=base-alt
    assert gap>=0
    if strict and a!=policy(h):assert gap>0
    rows.append({'history':h,'chosen':policy(h),'alternative':a,'chosen_leaf':z,'alternative_leaf':zz,'slack':str(gap)})
 z=leaf(());data={'units_or_signed_mass_total':str(sum(w.values())),'types':{str(k):str(v) for k,v in w.items()},'history_nodes':sum(p**d for d in range(m)),'comparisons_including_self':len(rows),'comparisons_excluding_self':sum(p**d for d in range(m))*(p-1),'policy_rows':rows,'root_leaf':z,'root_utilities':[str(uq(w,a,cnt(z,p))) for a in z],'root_coverage':str(cov(w,z)),'actual_catalog_OPT':str(max(cov(w,q) for q in product(range(p),repeat=m)))}
 if strict:data['minimum_nonself_slack']=str(min(F(r['slack']) for r in rows if r['alternative']!=r['chosen']))
 if static:
  stat=[];pne=[]
  for q in product(range(p),repeat=m):
   gains=[]
   for i in range(m):
    old=uq(w,q[i],cnt(q,p))
    for a in range(p):
     zz=q[:i]+(a,)+q[i+1:];gains.append(uq(w,a,cnt(zz,p))-old)
   isp=max(gains)==0
   if isp:pne.append(q)
   stat.append({'profile':q,'coverage':str(cov(w,q)),'all_action_gains_including_self':[str(g) for g in gains],'is_PNE':isp})
  data['static_profiles']=stat;data['static_pne_profiles']=pne;data['static_pne_min_welfare']=str(min(cov(w,q) for q in pne));data['static_action_comparisons_including_self']=len(stat)*m*p
 return data

# Arbitrary background identity checked per single actual customer, including zero-load terms.
identity_cases=0
for r in range(1,7):
 for s in range(1,r+1):
  for hc,hd in product(range(5),repeat=2):
   for mask in range(1,16):
    ia,ib=mask&1,(mask>>1)&1;z=hc*((mask>>2)&1)+hd*((mask>>3)&1)
    den=r*ia+s*ib+z;denp=s*ia+r*ib+z
    ua=F(ia,den) if ia else F();ubp=F(ib,denp) if ib else F();uap=F(ia,denp) if ia else F()
    V=F(z,den) if z else F();Vp=F(z,denp) if z else F();T=F(z*(z+(r+s)*ia),den*denp) if ib and z else F()
    L=r*s*ua+r*(r-s)*ubp;R=s*s*uap+(r-s)*ib+s*Vp
    assert L+s*V+(r-s)*T==R and 0<=T<=V and L+s*V<=R<=L+r*V
    identity_cases+=1
matrix=[]
for i,j,z in [(0,0,1),(0,1,0),(0,1,1),(0,1,2),(1,0,0),(1,0,1),(1,0,2)]:
 mask=i+2*j+(4 if z else 0)+(8 if z==2 else 0);w={mask:1};q=(2,1,1,1);qp=(1,2,1,1);q0=(0,3,1,1)
 def V(v):d=sum(v[t] for t in range(4) if mask>>t&1);return F(z,d) if z else F()
 matrix.append([uq(w,0,q) if i else F(),uq(w,1,qp) if j else F(),uq(w,0,qp) if i else F(),uq(w,1,q0) if j else F(),V(q),V(qp),V(q0)])
a=[row[:] for row in matrix];det=F(1)
for col in range(7):
 k=next(i for i in range(col,7) if a[i][col]);
 if k!=col:a[k],a[col]=a[col],a[k];det=-det
 pivot=a[col][col];det*=pivot
 for i in range(col+1,7):
  factor=a[i][col]/pivot
  for j in range(col+1,7):a[i][j]-=factor*a[col][j]
  a[i][col]=0
assert det==-F(1,155520)

family=[]
for m in range(2,7):
 M=2*m**4;w={1:1,6:-2,2:M,4:M,3:M,5:M,7:M};qs=compositions(m,3)
 util=[uq(w,t,q) for q in qs for t in range(3) if q[t]];assert min(util)>=0
 C=lambda mask:sum(v for typ,v in w.items() if typ&mask)
 covers={str(mask):C(mask) for mask in range(1,8)}
 assert all(C(a)<=C(b) for a in range(1,8) for b in range(1,8) if a&b==a)
 local=[]
 for a,b in [(0,1),(0,2),(1,2)]:
  ca,cb,cab=C(1<<a),C(1<<b),C((1<<a)|(1<<b));cells=[cab-cb,cab-ca,ca+cb-cab];assert min(cells)>=0;local.append(cells)
 triangle=C(3)+C(5)-C(6)-C(1);assert triangle==-1
 family.append({'m':m,'M':M,'covers':covers,'pair_nonempty_masses':local,'minimum_terminal_utility':str(min(util)),'sharp_rows':sharp(w,3,m),'triangle_middle_a':triangle})
small={1:-F(1,15),2:F(1,3),3:F(1,5),4:F(1,3),5:F(1,5),6:-F(1,5),7:F(1,5)}
last=(1,2,1,2,2,1,1,1,1)
def smallpol(h):return 2 if not h else (1,2,1)[h[0]] if len(h)==1 else last[3*h[0]+h[1]]
signed=policy_audit(small,3,3,smallpol);legal=policy_audit({2:1,4:1},3,3,smallpol)
assert signed['root_coverage']==signed['actual_catalog_OPT']=='16/15';assert legal['root_coverage']==legal['actual_catalog_OPT']=='2'
C=lambda mask:sum(v for typ,v in small.items() if typ&mask)
assert C(3)+C(5)-C(6)-C(1)==-F(4,15)
smallsharp=sharp(small,3,3)
base={1:3,3:3,4:1,5:1,10:1,12:1,14:2};last4=((2,2,1,0),(2,0,0,0),(1,0,0,0),(0,0,0,0))
def strictpol(h):return 3 if not h else (3,0,0,0)[h[0]] if len(h)==1 else last4[h[0]][h[1]]
strict12=policy_audit(base,4,3,strictpol,True,True)
full={mask:100*base.get(mask,0)+1 for mask in range(1,16)};strict1215=policy_audit(full,4,3,strictpol,True,True)
assert strict12['minimum_nonself_slack']=='1/6' and strict1215['minimum_nonself_slack']=='18'
assert strict12['root_coverage']=='11' and strict12['static_pne_min_welfare']==strict12['actual_catalog_OPT']=='12'
assert strict1215['root_coverage']=='1112' and strict1215['static_pne_min_welfare']==strict1215['actual_catalog_OPT']=='1214'
assert len(strict12['static_pne_profiles'])==len(strict1215['static_pne_profiles'])==6
res={'status':'passed','new_math_entries':{'attempts':1,'successes':1,'failures':0},'original_CLI_entries':0,'solver_calls':0,'float_operations':0,'arbitrary_background_identity_single_customer_cases':identity_cases,'seven_slot_matrix':[[str(v) for v in row] for row in matrix],'seven_slot_determinant':str(det),'signed_general_family_finite_scope_m':[2,3,4,5,6],'signed_family_finite_data':family,'signed_family_new_sharp_comparisons':sum(len(v['sharp_rows']) for v in family),'small_signed_complete_policy':signed,'small_legal_complete_policy_same_actions':legal,'small_signed_sharp_rows':smallsharp,'small_signed_triangle':'-4/15','strict_twelve_clients':strict12,'strict_full_support_1215_clients':strict1215,'scope':'One stdlib definition entry; signed data and true unit customers separated. Only displayed policies verified, not all strategies. Universal m/background/DP/module claims analytic. No source discovery, optimization, original CLI, oldIID or other oldsuccess reruns.'}
OUT.write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'passed','new_entries':1,'background_single_customer_cases':identity_cases,'seven_slot_determinant':str(det),'signed_family_sharp_comparisons':res['signed_family_new_sharp_comparisons'],'small_policies_compares':len(signed['policy_rows'])+len(legal['policy_rows']),'strict_policies_compares':len(strict12['policy_rows'])+len(strict1215['policy_rows']),'old_reruns':0}))
