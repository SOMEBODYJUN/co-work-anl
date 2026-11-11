"""Independent literal-index reconstruction of 17 old-cone hidden lift certificates."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
from functools import lru_cache
import hashlib,json,time
from main_pair_features import pay,terms
B=Path(__file__).resolve().parent
pp=B/'master_cuts/dynamic_5744_exact.json'
lp=B/'joint_requery/portfolio_comparison/exact_single_lifts_5744_i3_m0_orb00.json'
a=json.loads(lp.read_text());p=json.loads(pp.read_text());cols=p['columns']
assert hashlib.sha256(pp.read_bytes()).hexdigest()==a['source_sha256']
assert (a['i'],a['k'],a['member'],a['orb'])==(3,3,0,[0,0])
start=time.time();blocks=[]
for ci,col in enumerate(cols):
 if col['kind']=='hist':blocks.append([ci,col,{}])
 elif col['kind']=='joint-reply':
  fam,diag,wi,wj=col['group']
  blocks[-1][2][fam,diag,tuple(wi),tuple(wj),tuple(col['state'])]=F(col['weight'])
expected=[defaultdict(F) for _ in range(17)];r=F(0);u6=F(0);K=F(cols[0]['weight'])
for ci,h,groups in blocks:
 aa=tuple(map(int,h['actual_bits']));pfx=sum(aa[:3]);ell=sum(aa[:5]);hm=F(h['weight'])
 r+=hm*pay(aa[3],sum(aa));u6+=hm*pay(aa[5],sum(aa))
 words=tuple(w for w,n in zip(product((0,1),repeat=3),h['hist']) for _ in range(n))
 for i in range(6):
  for j in range(6):
   if i==j:continue
   others=[l for l in range(6) if l not in (i,j)]
   means=tuple(F(sum(words[l][v] for l in others),4) for v in range(3))
   mass={st:groups.get((0,0,words[i],words[j],st),F(0)) for st in [(0,1),(1,0),(1,1)]}
   mass[0,0]=hm-sum(mass.values(),F(0));assert min(mass.values())>=0
   for st,m in mass.items():
    qvec=tuple(map(F,aa+words[i]+words[j]+st))+means
    assert len(qvec)==17
    for qi,q in enumerate(qvec):expected[qi][pfx,ell,st[0],q]+=m/30
assert r==F(a['r_actual']) and u6==F(a['u6']) and K==F(a['K'])
expected=[{v:m for v,m in d.items() if m} for d in expected]
@lru_cache(None)
def e_at(p,ell,t,q,h):return terms(p,ell,t,q,*h)
checks=[]
assert sorted(z['query'] for z in a['queries'])==list(range(17))
for z in a['queries']:
 qi=z['query'];saved={};states=[]
 for v in z['visible']:
  pfx,ell,t,q=v['state'];key=(pfx,ell,t,F(q));states.append(key);assert key not in saved;saved[key]=F(v['mass'])
 assert saved==expected[qi],qi
 mass=[F(0)]*len(states);sums=defaultdict(F)
 _,cost=terms(0,0,0,0,0,0,0,0)
 assert len(cost)==76
 for atom in z['support']:
  i=atom['visible'];h=tuple(atom['hidden']);w=F(atom['mass'])
  assert w>=0 and len(h)==4 and all(v in (0,1) for v in h)
  mass[i]+=w;es,_=e_at(*states[i],h)
  for name,value in es.items():sums[name]+=w*value
 assert mass==[saved[v] for v in states]
 rsmall=F(z['r_recovered_feasible']);assert 0<=rsmall<=r
 gaps=[]
 for name,(sr,su,sk) in cost.items():
  gap=sr*r+su*u6+sk*K-sums[name]
  assert gap==F(z['all_76_slacks_at_actual'][name])>=0,(qi,name)
  assert sr*rsmall+su*u6+sk*K-sums[name]>=0
  gaps.append(gap)
 checks.append({'query':qi,'visible_states':len(states),'positive_hidden_atoms':sum(F(v['mass'])>0 for v in z['support']),'rows_checked':len(gaps),'minimum_slack':str(min(gaps)),'source_margin':str(r-rsmall)})
packpath=B/'joint_requery/portfolio_selected_5744.json';pack=json.loads(packpath.read_text());new=pack['cuts'][0]
assert new['exact_slack']==a['joint_negative_slack'] and new['row_sha256']==a['joint_row_sha256']
gap=sum((F(v)*F(cols[j]['weight']) for j,v in new['sparse_row']),F(0));assert gap==F(a['joint_negative_slack'])<0
independent=json.loads((B/'main_verify_portfolio_pair_5744.json').read_text())
assert independent['status']=='PASS' and independent['point_sha256']==a['source_sha256'] and independent['pack_sha256']==hashlib.sha256(packpath.read_bytes()).hexdigest()
report={'status':'PASS','scope':'Literal six-index visible marginals, 17 independent nonnegative hidden lifts, 1292 exact old rows; together with previously independently reconstructed joint row this proves strict projection separation for this source/orbit/17-query menu only','input_sha256':a['source_sha256'],'lift_sha256':hashlib.sha256(lp.read_bytes()).hexdigest(),'joint_pack_sha256':hashlib.sha256(packpath.read_bytes()).hexdigest(),'queries':checks,'old_rows_checked':sum(c['rows_checked'] for c in checks),'joint_negative_slack':str(gap),'seconds':time.time()-start}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='queries'},ensure_ascii=False,indent=2))
