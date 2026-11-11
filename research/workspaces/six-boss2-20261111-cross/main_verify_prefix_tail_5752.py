"""Main's independent shared endpoint alpha+discounted-beta exact audit.
Uses independently written features and solves all four two-state policies.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
from collections import defaultdict
import hashlib,json,time
from main_pair_features import pay,terms
B=Path(__file__).resolve().parent
pp=B/'master_cuts/dynamic_5752_exact.json';cp=B/'coverage_bridge/selected_prefix_tail_5752.json'
point=json.loads(pp.read_text());pack=json.loads(cp.read_text());cols=point['columns']
assert pack['input_sha256']==hashlib.sha256(pp.read_bytes()).hexdigest()
Qnames=tuple([f'A{i+1}' for i in range(6)]+['Ti','Bi','Ci','Tj','Bj','Cj','R','Z','other_T','other_B','other_C'])
blocks=[]
for i,c in enumerate(cols):
 if c['kind']=='hist':blocks.append([i,c,[]])
 elif c['kind']=='joint-reply':blocks[-1][2].append((i,c))
@lru_cache(None)
def features(p,ell,t,q,h,s,ss,k):return terms(p,ell,t,q,*h,s,ss,k)

def policy_values(e,theta):
 vals=[[],[]]
 for c0,c1 in product((0,1),repeat=2):
  a=1-theta*(c0==0);b=-theta*(c0==1);c=-theta*(c1==0);d=1-theta*(c1==1);det=a*d-b*c
  vals[0].append((d*e[0,c0]-b*e[1,c1])/det)
  vals[1].append((a*e[1,c1]-c*e[0,c0])/det)
 v=[min(z) for z in vals]
 assert all(v[t]==min(e[t,c]+theta*v[c] for c in (0,1)) for t in (0,1))
 return [(1-theta)*z for z in v]

def audit(rec):
 source=rec['source']-1;k=rec['k'];orb=tuple(rec['orbit']);member=rec['member'];ct=6 if orb[1] else 30;theta=F(rec['delta'])
 assert k==6-source and 0<=theta<1
 alpha={n:F(v) for n,v in rec['alpha'].items()};beta={n:F(v) for n,v in rec['beta'].items()}
 assert all(v>=0 for v in list(alpha.values())+list(beta.values()))
 _,prices=terms(0,0,0,0,0,0,0,0,k=k)
 ab=[sum((w*prices[n][j] for n,w in alpha.items() if '@' not in n),F(0)) for j in range(3)]
 bb=[beta.get('source',F(0)),(k-2)*beta.get('alpha_mid',F(0))+beta.get('alpha_last',F(0)),(k-2)*beta.get('beta_mid',F(0))+beta.get('beta_last',F(0))]
 budget=[a+b for a,b in zip(ab,bb)];assert budget==list(map(F,rec['budget'])) and budget[0]==1
 mu={n[3:]:v for n,v in beta.items() if n.startswith('mu_')};M=sum(mu.values(),F(0))
 internal=[(n,w) for n,w in alpha.items() if '@' not in n]
 external=[(*n.split('@'),w) for n,w in alpha.items() if '@' in n]
 @lru_cache(None)
 def project(p,ell,t,qs_tuple):
  qs=dict(zip(Qnames,qs_tuple));edges={}
  for current,last in product((0,1),repeat=2):
   vv=[]
   q=sum((w*(F(current) if n=='current' else qs[n]) for n,w in mu.items()),F(0))
   for s in range(k-1):
    z=p+current+s+last
    vv.append(pay(beta.get('source',F(0))*current-M*last,z)
     +beta.get('alpha_mid',F(0))*F(s,ell+1)+beta.get('alpha_last',F(0))*F(last,ell+1)
     +beta.get('beta_mid',F(0))*s+beta.get('beta_last',F(0))*last+q/(p+current+s+1))
   edges[current,last]=min(vv)
  psi=policy_values(edges,theta)
  together=[];alone=[]
  for h in product((0,1),repeat=4):
   for s in range(k-2):
    for ss in range(k-2):
     e,_=features(p,ell,t,F(0),h,s,ss,k)
     v=sum((w*e[n] for n,w in internal),F(0))
     for name,label,w in external:v+=w*features(p,ell,t,qs[label],h,s,ss,k)[0][name]
     alone.append(v);together.append(v+psi[h[3]])
  return min(together),min(alone)+min(psi)
 row=[F(0)]*len(cols);row[0]=budget[2];sep_row=[F(0)]*len(cols);sep_row[0]=budget[2]
 for hi,h,js in blocks:
  aa=tuple(map(int,h['actual_bits']));words=tuple(w for w,n in zip(product((0,1),repeat=3),h['hist']) for _ in range(n));incs=[defaultdict(F),defaultdict(F)];base=[F(0),F(0)]
  for i in range(6):
   for j in range(6):
    if (i==j)!=bool(orb[1]):continue
    others=[l for l in range(6) if l not in {i,j}];means=tuple(F(sum(words[l][v] for l in others),len(others)) for v in range(3));vv={}
    for st in product((0,1),repeat=2):vv[st]=project(sum(aa[:source]),sum(aa[:5]),st[member],tuple(map(F,aa+words[i]+words[j]+st))+means)
    for part in (0,1):
     z=vv[0,0][part];base[part]+=z/ct
     for st in [(0,1),(1,0),(1,1)]:incs[part][words[i],words[j],st]+=(vv[st][part]-z)/ct
  for part,target in enumerate([row,sep_row]):
   target[hi]=pay(aa[source],sum(aa))+budget[1]*pay(aa[5],sum(aa))-base[part]
   for ci,c in js:
    fam,diag,wi,wj=c['group']
    if (fam,diag)==orb:target[ci]=-incs[part][tuple(wi),tuple(wj),tuple(c['state'])]
 saved=[F(0)]*len(cols)
 for j,v in rec.get('row_nonzero',rec.get('sparse_row')):saved[j]=F(v)
 assert row==saved,[(i,str(x),str(y)) for i,(x,y) in enumerate(zip(row,saved)) if x!=y][:4]
 dot=lambda z:sum((v*F(c['weight']) for v,c in zip(z,cols)),F(0))
 joint,separate=dot(row),dot(sep_row)
 assert joint==F(rec['exact_slack'])<0
 assert separate==F(rec['separate_projection_slack'])
 assert separate-joint==F(rec['joint_projection_gain'])>=0
 return {'source':source+1,'member':member,'orb':list(orb),'delta':str(theta),'beta_nonzero':bool(beta),'same_full_4849_coefficients':True,'exact_slack':str(joint),'separate_slack':str(separate),'separation_requires_shared_endpoint_for_these_weights':separate>=0>joint}
start=time.time();rows=[audit(r) for r in pack['cuts']]
a={'status':'PASS','scope':'Independent literal-index and shared endpoint min plus four-policy Bellman audit; general legality uses alpha and beta budgets once each; no SPE or half conclusion','point_sha256':pack['input_sha256'],'pack_sha256':hashlib.sha256(cp.read_bytes()).hexdigest(),'rows':rows,'seconds':time.time()-start}
Path(__file__).with_suffix('.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in a.items() if k!='rows'},ensure_ascii=False,indent=2));print('rows',len(rows),'nonzero_beta',sum(z['beta_nonzero'] for z in rows),'shared_endpoint_needed',sum(z['separation_requires_shared_endpoint_for_these_weights'] for z in rows))
