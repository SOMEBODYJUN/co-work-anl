"""Evaluate diagonal/offdiagonal f=1 basic IC separately at saved points."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json,sys
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'work.py').exists())
OLD=ROOT/'research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/six_astra'
sys.path.insert(0,str(OLD))
import new_reply_budget as nr
import actual_fifth_nested as nest
point=json.loads((OLD/'attractive_nested_exact.json').read_text());out=json.loads((HERE/'zz_threshold_exact.json').read_text())
K=F(point['columns'][0]['weight']);ds={};hi=None
for j,c in enumerate(point['columns']):
 if c['kind']=='hist':hi=j;ds[hi]={'data':c,'groups':{}}
 if c['kind']=='joint-reply':
  f,d,wi,wj=c['group'];g=(f,d,tuple(wi),tuple(wj));ds[hi]['groups'].setdefault(g,{})[tuple(c['state'])]=F(c['weight'])
for d in ds.values():
 for g,s in d['groups'].items():s['r']=s[1,0]+s[1,1];s['z']=F();s['rz']=F()
for v in out['variables']:
 f,d,wi,wj=v['group'];g=(f,d,tuple(wi),tuple(wj));s=ds[v['hist_column']]['groups'][g];y=F(v['weight']);s['z']+=y;s['rz']+=v['r']*y
slacks={(stage,diag,n):F() for stage,names in (('R',nr.NAMES),('Z',nest.BASIC)) for diag in (0,1) for n in names}
for hi,dd in ds.items():
 c=dd['data'];h=F(c['weight']);a=tuple(map(int,c['actual_bits']));p=sum(a[:3]);pa=sum(a[:4]);ell=sum(a[:5]);whole=sum(a)
 if not h:continue
 words=[w for w,n in zip(nr.PAT,c['hist']) for _ in range(n)];nb=sum(w[1] for w in words);nc=sum(w[2] for w in words)
 for i,j in product(range(6),repeat=2):
  wi=words[i];wj=words[j];t,b,cc=wi;y=wj[2];diag=int(i==j);g=(1,diag,wi,wj);s=dd['groups'][g];r=s['r'];z=s['z'];rz=s['rz'];den=p+t+y+1
  # First newly exposed true final R after (h,T_i,C_j).
  vals=[h*(nr.share(b,p+t+b+cc)-nr.share(y,p+t+y))+r*nr.share(y,(p+t+y)*den)]
  vals += [(r-h*q)/den for q in (b,cc,t,F(c['d'],6),*a,F(nb,6),F(nc,6))]
  vals += [h*nr.share(cc,p+t+b+cc)-r/F(p+t+b+1),h*nr.share(a[5],whole)-r/F(ell+1),-r]
  assert len(vals)==len(nr.NAMES)
  for n,v in zip(nr.NAMES,vals):slacks['R',diag,n]+=v
  # New Z after actual fifth chooses R; expectation of shares keeps rz.
  vz=z/F(pa+1)-rz/F((pa+1)*(pa+2))
  vr=r/F(pa+1)-rz/F((pa+1)*(pa+2))
  ha=nr.share(a[4]+a[5],whole)+F(a[4],(pa+1)*(pa+2))
  vals=[h*nr.share(a[4],whole)-vr,h*ha-F(r+z,pa+1)+F(rz,(pa+1)*(pa+2)),h*nr.share(a[5],whole)-z/F(ell+1),-z]
  # q/(pa+r+1)=q/(pa+1)-q*r/D
  vals += [vz-h*F(q,pa+1)+F(q*r,(pa+1)*(pa+2)) for q in a]
  vals += [vz-r/F(pa+2),F(r-z,den)]
  for n,v in zip(nest.BASIC,vals):slacks['Z',diag,n]+=v
for st,names in (('R',nr.NAMES),('Z',nest.BASIC)):
 for dg,count in ((1,6),(0,30)):slacks[st,dg,'capacity']+=count*K
report={'scope':'fixed exact 3949-point, f1 basic true rows split diagonal/offdiagonal, not SPE','rows':len(slacks),'negative_rows':[{'row':str(k),'slack':str(v)} for k,v in slacks.items() if v<0],'minimum_slack':str(min(slacks.values()))}
(HERE/'diagonal_basic_status.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
