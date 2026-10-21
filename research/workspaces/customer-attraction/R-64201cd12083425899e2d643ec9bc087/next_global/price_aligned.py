"""Full atom-domain pricing of the first sparse enhanced 5-player dual.

Floating exploration only. Family separation is exact for the checked active
row names; coefficient checks use the sibling's direct Fraction definitions.
"""
from pathlib import Path
import sys, json, time
from itertools import product
from fractions import Fraction as F
import numpy as np

HERE=Path(__file__).resolve().parent
SIB=HERE.parent/'next_credible'
sys.path.insert(0,str(SIB))
from offdiagonal_probe import rows as off_rows
from crossmenu_probe import rows as cross_rows
from menutax_probe import rows as tax_rows
from alignedtax_probe import rows as align_rows
ROOT=HERE.parents[4]
ns={}
src=(ROOT/'tests/audits/customer_attraction_five_indexed.py').read_text()
exec(compile(src.split('from pathlib import Path')[0],'<canonical definitions>','exec'),ns)

def compositions(n,k):
 if k==1:
  yield(n,);return
 for x in range(n+1):
  for rest in compositions(n-x,k-1):yield(x,)+rest

types=np.array(list(product((0,1),repeat=3)),dtype=int)
quads=np.array(list(product((0,1),repeat=4)),dtype=int)
TH=np.array(list(compositions(5,8)),dtype=int)
SH=np.array(list(compositions(5,16)),dtype=int)
TD=TH@types[:,0];SD=SH@quads[:,0]
TC=TH@types[:,1:];SC=SH@quads[:,1:]
SDOT=SH@(quads[:,2]*quads[:,3])
TIDS=[np.flatnonzero(TD==d) for d in range(6)]
SIDS=[np.flatnonzero(SD==d) for d in range(6)]

def div(n,d):
 n,d=np.broadcast_arrays(np.asarray(n,float),np.asarray(d,float))
 return np.divide(n,d,out=np.zeros_like(n),where=(n!=0))

def third_metrics(p):
 t,x,y=types.T;load=p+t+x+y
 return {k:TH@v for k,v in {
  'zx':div(x,load),'zy':div(y,load),'dx':1/(p+t+2),
  'D1':1/(p+t+1),'D2':1/(p+t+2),
  'cxlast':div(x,p+t+x+1),
  'dy':1/(p+t+x+1),
  'H':div(x+y,load)+div(x,(p+t+1)*(p+t+2))}.items()}

def second_metrics(p):
 t,u,v,w=quads.T;load=p+t+u+v+w;bg=p+t+u
 return {k:SH@val for k,val in {
  'zu':div(u,load),'zv':div(v,load),'zw':div(w,load),
  'du':1/(p+t+3),'dw':1/(p+t+u+v+1),
  'cfw':div(w,p+t+3),'cvlast':div(v,p+t+u+v+1),
  'D1':1/(bg+1),'D2':1/(bg+2),
  'H':div(v+w,load)+div(v,(bg+1)*(bg+2))}.items()}

TM=[third_metrics(p) for p in range(3)]
SM=[second_metrics(p) for p in range(2)]
LABELS='ABCDEUVWXY'
PATHS={'actual':'ABCDE','second':'AEUVW','third':'ABEXY'}

class Price:
 def __init__(self,report):
  self.beta=report['dual_beta'];self.w={n:v for n,v in zip(report['names'],report['dual_lambda']) if v>1e-10}
  self.n=[n for n in self.w if n not in self.expected()]
  if self.n:raise ValueError('Unimplemented active rows: '+str(self.n))
 def expected(self):
  return set('''actual:1:K:W actual:1:K:X actual:1:K:Y actual:5:K:U actual:5:K:Y actual:reply:S actual:reply:V actual:reply:Z second:reply:V second:reply:topic-D third:5:sum-L-second third:reply:V third:reply:Z third:reply:cross-L-second F:second F:third AB:4:K:V AB:actual:5:sum-Y AE:actual:5:sum-X AE:second:5:sum-Y Sbranch:3:K:Y actual:5:sum-SU actual:5:sum-SW second:3:sum-SW second:5:sum-SW third:5:sum-SW AB:node-2:off-X Sbranch:node-1:off-W Sbranch:node-3:off-V AE:node-1:crossmenu-Sbranch:W AB:newtax:Y|L2 Sbranch:newtax:V|W Sbranch:newtax:W|L2 Sbranch:newtax:X|Y AB:align-tax:Sbranch:V|Sbranch:W Sbranch:align-tax:Sbranch:V|Sbranch:W'''.split())
 def old_score(self,b,d,lhs):
  e0,h0=lhs[0];e1,h1=lhs[1];e2,h2=lhs[2]
  def share(p,i):return b[p[i]]/sum(b[k] for k in p) if b[p[i]] else 0.
  ac,se,th=[PATHS[n] for n in ('actual','second','third')]
  p0=sum(b[k] for k in ac[:3]);p1=sum(b[k] for k in se[:3]);p2=sum(b[k] for k in th[:3]);D0=(p0+1)*(p0+2);D1=(p1+1)*(p1+2);D2=(p2+1)*(p2+2)
  a5=sum(b[k] for k in ac[:4])+1;s5=sum(b[k] for k in se[:4])+1;t5=sum(b[k] for k in th[:4])+1
  rows={f'actual:1:K:{k}':share(ac,0)-b[k]/5 for k in 'WXY'}
  rows.update({f'actual:5:K:{k}':share(ac,4)-b[k]/a5 for k in 'UY'})
  rows.update({'actual:reply:S':5*share(ac,3)-d/(p0+1)+h0/D0,
   'actual:reply:V':(d*e0-5*h0)/D0,
   'actual:reply:Z':5*share(ac,4)-e0/a5,
   'second:reply:V':(d*e1-5*h1)/D1,
   'second:reply:topic-D':(e1-5*b['D'])/(p1+1)+(d*b['D']-h1)/D1,
   'third:5:sum-L-second':5*share(th,4)-e1/t5,
   'third:reply:V':(d*e2-5*h2)/D2,
   'third:reply:Z':5*share(th,4)-e2/t5,
   'third:reply:cross-L-second':5*(e2-e1)/(p2+1)+(d*e1-5*h2)/D2,
   'F:second':share(ac,1)-share(se,1),'F:third':share(ac,2)-share(th,2)})
  return sum(self.w.get(k,0)*v for k,v in rows.items())
 def family_scores(self,b,ell):
  ac,se,th=[PATHS[n] for n in ('actual','second','third')]
  def sh(p,i):return b[p[i]]/sum(b[k] for k in p) if b[p[i]] else 0.
  a5=sum(b[k] for k in ac[:4])+1;s5=sum(b[k] for k in se[:4])+1;t5=sum(b[k] for k in th[:4])+1
  A=TM[b['A']+b['B']];E=TM[b['A']+b['E']];S=SM[b['A']]
  def w(k):return self.w.get(k,0.)
  x,y=TC.T;u,v,z=SC.T;dot=SDOT
  ab=w('AB:4:K:V')*(A['zx']-b['V']*A['dx'])+w('AB:actual:5:sum-Y')*(5*sh(ac,4)-y/a5)
  ab+=w('AB:node-2:off-X')*(4*A['zy']-x*A['dy']+A['cxlast'])
  ab+=w('AB:newtax:Y|L2')*(5*A['H']-(b['Y']*(5-ell)+(1-b['Y'])*ell)*A['D1']-2*b['Y']*ell*A['D2'])
  ab+=w('AB:align-tax:Sbranch:V|Sbranch:W')*5*A['H']
  ae=w('AE:actual:5:sum-X')*(5*sh(ac,4)-x/a5)+w('AE:second:5:sum-Y')*(5*sh(se,4)-y/s5)
  ae+=w('AE:node-1:crossmenu-Sbranch:W')*5*E['zx']
  sb=w('Sbranch:3:K:Y')*(S['zu']-b['Y']*S['du'])
  for n,c,p,i,den in [('actual:5:sum-SU',u,ac,4,a5),('actual:5:sum-SW',z,ac,4,a5),('second:3:sum-SW',z,se,2,b['A']+b['E']+3),('second:5:sum-SW',z,se,4,s5),('third:5:sum-SW',z,th,4,t5)]:sb+=w(n)*(5*sh(p,i)-c/den)
  sb+=w('Sbranch:node-1:off-W')*(4*S['zu']-z*S['du']+S['cfw'])
  sb+=w('Sbranch:node-3:off-V')*(4*S['zw']-v*S['dw']+S['cvlast'])
  for n,j,k in [('Sbranch:newtax:V|W','V','W'),('Sbranch:newtax:X|Y','X','Y')]:
   sb+=w(n)*(S['H']-(b[j]*(1-b[k])+(1-b[j])*b[k])*S['D1']-2*b[j]*b[k]*S['D2'])
  sb+=w('Sbranch:newtax:W|L2')*(5*S['H']-(b['W']*(5-ell)+(1-b['W'])*ell)*S['D1']-2*b['W']*ell*S['D2'])
  sb+=w('Sbranch:align-tax:Sbranch:V|Sbranch:W')*(5*S['H']-(v+z)*S['D1']+2*dot*(S['D1']-S['D2']))
  return ab,ae,sb
 def direct_score(self,a):
  v=ns['evaluate'](list(map(int,a['bits'])),[a['AB_hist'],a['AE_hist'],a['second_hist']],a['menus_lh'],True)
  for f in (off_rows,cross_rows,tax_rows,align_rows):v.update(f(a))
  return sum(self.w[n]*float(v[n]) for n in self.w)
 def check(self):
  rng=np.random.default_rng(91302)
  for _ in range(80):
   bits=tuple(map(int,rng.integers(0,2,10)));b=dict(zip(LABELS,bits));d=int(rng.integers(0,6));it=int(rng.choice(TIDS[d]));ie=int(rng.choice(TIDS[d]));iz=int(rng.choice(SIDS[d]));lhs=[]
   for j in range(3):
    h=int(rng.integers(0,d+1));r=int(rng.integers(0,6-d));lhs.append((h+r,h))
   ab,ae,sb=self.family_scores(b,lhs[2][0]);u,v,z=SC[iz];dot=SDOT[iz];A=TM[b['A']+b['B']];E=TM[b['A']+b['E']]
   score=self.old_score(b,d,lhs)+ab[it]+ae[ie]+sb[iz]
   score+=self.w.get('AB:align-tax:Sbranch:V|Sbranch:W',0)*(-(v+z)*A['D1'][it]+2*dot*(A['D1'][it]-A['D2'][it]))
   score-=self.w.get('AE:node-1:crossmenu-Sbranch:W',0)*z*E['dx'][ie]
   atom={'bits':''.join(map(str,bits)),'AB_hist':TH[it].tolist(),'AE_hist':TH[ie].tolist(),'second_hist':SH[iz].tolist(),'menus_lh':lhs}
   direct=self.direct_score(atom)
   assert abs(score-direct)<1e-9,(score,direct,atom)
  return 80
 def run(self):
  best=None;negative=[];priced=0;t0=time.time();wa=self.w.get('AB:align-tax:Sbranch:V|Sbranch:W',0);we=self.w.get('AE:node-1:crossmenu-Sbranch:W',0)
  for bi,bits in enumerate(product((0,1),repeat=10)):
   b=dict(zip(LABELS,bits));A=TM[b['A']+b['B']];E=TM[b['A']+b['E']];W=int(any(bits[:5]));maskbest=None
   for ell in range(6):
    ab,ae,sb=self.family_scores(b,ell)
    for d in range(6):
     ti=TIDS[d];si=SIDS[d]
     # The AB coupling needs only v+w and dot(v,w), and AE only w.
     abgrid=ab[ti][None,None,:]-wa*np.arange(11)[:,None,None]*A['D1'][ti]+2*wa*np.arange(6)[None,:,None]*(A['D1'][ti]-A['D2'][ti])
     abarg=np.argmax(abgrid,axis=2);abmax=np.max(abgrid,axis=2)
     aegrid=ae[ti][None,:]-we*np.arange(6)[:,None]*E['dx'][ti];aearg=np.argmax(aegrid,axis=1);aemax=np.max(aegrid,axis=1)
     base=self.old_score(b,d,[(0,0),(0,0),(ell,0)])
     corners=[(0,0),(d,d),(5-d,0),(5,d)]
     choices=[]
     for f in range(2):
      vals=[]
      for lh in corners:
       lhs=[(0,0),(0,0),(ell,0)];lhs[f]=lh;vals.append(self.old_score(b,d,lhs)-base)
      j=int(np.argmax(vals));choices.append(corners[j])
     lh0,lh1=choices
     hs=range(max(0,ell-(5-d)),min(d,ell)+1)
     oldvals=[self.old_score(b,d,[lh0,lh1,(ell,h)]) for h in hs]
     jh=int(np.argmax(oldvals));h=list(hs)[jh];oldmax=oldvals[jh]
     vs=SC[si,1];ws=SC[si,2];dots=SDOT[si]
     value=oldmax+sb[si]+abmax[vs+ws,dots]+aemax[ws]
     jj=int(np.argmax(value));iz=int(si[jj]);it=int(ti[abarg[vs[jj]+ws[jj],dots[jj]]]);ie=int(ti[aearg[ws[jj]]]);res=self.beta*W-int(d>0)-float(value[jj]);priced+=len(si)*len(ti)*len(ti)
     if maskbest is None or res<maskbest['residual']:
      atom={'bits':''.join(map(str,bits)),'AB_hist':TH[it].tolist(),'AE_hist':TH[ie].tolist(),'second_hist':SH[iz].tolist(),'menus_lh':[lh0,lh1,(ell,h)]}
      exactres=self.beta*W-int(d>0)-self.direct_score(atom)
      assert abs(res-exactres)<1e-9,(res,exactres,atom)
      maskbest={'residual':res,'atom':atom,'W':W,'O':int(d>0),'d':d}
   if maskbest['residual'] < -1e-8:negative.append(maskbest)
   if best is None or maskbest['residual']<best['residual']:best=maskbest
   if bi%64==0:print(json.dumps({'mask':bi,'minimum_residual':best['residual'],'elapsed':time.time()-t0}),flush=True)
  return {'scope':'floating full atom-domain pricing of the specified sparse 2196-row dual; not a universal certificate','beta':self.beta,'active_rows':len(self.w),'fixed_masks':1024,'AB_AE_histograms':len(TH),'S_histograms':len(SH),'best':best,'negative_columns':negative,'elapsed_seconds':time.time()-t0}

if __name__=='__main__':
 p=Price(json.loads((SIB/'reopt_aligned.json').read_text()));checks=p.check();r=p.run();r['direct_formula_checks']=checks
 print(json.dumps({k:v for k,v in r.items() if k!='negative_columns'},indent=2));HERE.joinpath('price_aligned.json').write_text(json.dumps(r,indent=2)+'\n')
