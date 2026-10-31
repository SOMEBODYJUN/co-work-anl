"""Independent exact rows for the separable indexed true-continuation relaxation."""
from fractions import Fraction as F
from itertools import product
labels=tuple('ABCDEUVWXY');paths={'actual':tuple('ABCDE'),'second':tuple('AEUVW'),'third':tuple('ABEXY')};start={'actual':0,'second':2,'third':3};families=list(paths)
types=list(product((0,1),repeat=3));quads=list(product((0,1),repeat=4))
def q(n,v):return F(n,v) if n else F(0)
def old_rows(bits,d,lhs):
 b=dict(zip(labels,bits));opt=int(d>0);ell=[x[0] for x in lhs];hh=[x[1] for x in lhs];rows={}
 def share(path,i):return q(b[path[i]],sum(b[t] for t in path))
 for pn,path in paths.items():
  ss=[share(path,i) for i in range(5)]
  for i in range(start[pn],5):
   p=sum(b[t] for t in path[:i]);k=5-i
   for t in labels:rows[f'{pn}:{i+1}:K:{t}']=ss[i]-q(b[t],p+k)
   rows[f'{pn}:{i+1}:O']=5*k*ss[i]+q(p,p+k)-opt
   rows[f'{pn}:{i+1}:sum-opt']=5*ss[i]-q(d,p+k)
  p=sum(b[t] for t in path[:3]);D=(p+1)*(p+2);H=ss[3]+ss[4]+q(b[path[3]],D)
  rows[f'{pn}:r2:O']=F(5,2)*H+q(p,p+1)-opt
  rows[f'{pn}:r2:exact-opt']=10*H-q(d*(5-d),p+1)-q(d*(d-1),p+2)
  f=families.index(pn);e=ell[f];h=hh[f]
  rows[f'{pn}:reply:S']=5*ss[3]-q(d,p+1)+q(h,D)
  rows[f'{pn}:reply:V']=q(d*e-5*h,D)
  rows[f'{pn}:reply:Z']=5*ss[4]-q(e,p+b[path[3]]+1)
  rows[f'{pn}:reply:P']=5*ss[4]-q(d,p+b[path[3]]+1)
  rows[f'{pn}:reply:clone-opt']=q(e,p+1)-q(h,D)-q(d,p+2)
  rows[f'{pn}:reply:all-opt']=q(5*e-5*d,p+1)+q(d*d-5*h,D)
  for g,tf in enumerate(families):
   if tf!=pn:rows[f'{pn}:reply:cross-L-{tf}']=q(5*(e-ell[g]),p+1)+q(d*ell[g]-5*h,D)
  for t in labels:rows[f'{pn}:reply:topic-{t}']=q(e-5*b[t],p+1)+q(d*b[t]-h,D)
  for nn,pp in paths.items():
   for i in range(start[nn],5):
    pref=sum(b[t] for t in pp[:i]);rows[f'{nn}:{i+1}:sum-L-{pn}']=5*share(pp,i)-q(e,pref+5-i)
 for pn,i in [('second',1),('third',2)]:rows[f'F:{pn}']=share(paths['actual'],i)-share(paths[pn],i)
 return rows

def third_rows(bits,hist,lhs,tag):
 b=dict(zip(labels,bits));prefix={'AB':'AB','AE':'AE'}[tag];path0=paths['actual' if tag=='AB' else 'second'];p=sum(b[t] for t in prefix);d=sum(n*t for n,(t,x,y) in zip(hist,types));opt=int(d>0);rx=sum(n*x for n,(t,x,y) in zip(hist,types));ry=sum(n*y for n,(t,x,y) in zip(hist,types));rows={}
 def share(path,i):return q(b[path[i]],sum(b[t] for t in path))
 def sm(fn):return sum((n*fn(t,x,y) for n,(t,x,y) in zip(hist,types)),F(0))
 zt=sm(lambda t,x,y:q(t,p+t+x+y));zx=sm(lambda t,x,y:q(x,p+t+x+y));zy=sm(lambda t,x,y:q(y,p+t+x+y))
 dx=sm(lambda t,x,y:q(1,p+t+2));dy=sm(lambda t,x,y:q(1,p+t+x+1));D1=sm(lambda t,x,y:q(1,p+t+1));D2=sm(lambda t,x,y:q(1,p+t+2));H=zx+zy+sm(lambda t,x,y:q(x,(p+t+1)*(p+t+2)))
 def add(n,v):rows[tag+':'+n]=v
 add('F3',5*share(path0,2)-zt)
 for t in labels:add('4:K:'+t,zx-b[t]*dx);add('5:K:'+t,zy-b[t]*dy)
 add('4:sum-opt',5*zx-d*dx);add('5:sum-opt',5*zy-d*dy)
 add('4:own-T',zx-q(d,p+3));add('5:own-T',zy-sm(lambda t,x,y:q(t,p+t+x+1)))
 add('5:own-X',zy-sm(lambda t,x,y:q(x,p+t+x+1)));add('4:own-Y',zx-sm(lambda t,x,y:q(y,p+t+2)))
 add('r2:O',F(5,2)*H+sm(lambda t,x,y:q(p+t,p+t+1))-5*opt)
 add('r2:exact-opt',10*H-d*(5-d)*D1-d*(d-1)*D2)
 for menu,v in [('X',rx),('Y',ry)]:add('4:sum-'+menu,5*zx-v*dx);add('5:sum-'+menu,5*zy-v*dy)
 for f,pn in enumerate(families):
  path=paths[pn];pp=sum(b[t] for t in path[:3]);Dp=(pp+1)*(pp+2);ss=[share(path,i) for i in range(5)];hold=ss[3]+ss[4]+q(b[path[3]],Dp)
  for menu,val in [('X',rx),('Y',ry)]:
   for i in range(start[pn],5):
    pref=sum(b[t] for t in path[:i]);add(f'{pn}:{i+1}:sum-{menu}',5*ss[i]-q(val,pref+5-i))
   ell,h=lhs[f];add(f'{pn}:reply:all-{menu}',q(5*ell-5*val,pp+1)+q(d*val-5*h,Dp))
  for mn,qx,qy in [('XX',rx,rx),('XY',rx,ry),('YY',ry,ry)]:
   one=qx*(5-qy)+(5-qx)*qy;both=qx*qy;add(f'{pn}:r2:menu-{mn}',25*hold-q(one,pp+1)-q(2*both,pp+2))
 for mn,qx,qy in [('XX',rx,rx),('XY',rx,ry),('YY',ry,ry)]:
  one=qx*(5-qy)+(5-qx)*qy;both=qx*qy;add('r2:menu-'+mn,25*H-one*D1-2*both*D2)
 return rows

def second_rows(bits,hist):
 b=dict(zip(labels,bits));p=b['A'];d=sum(n*t for n,(t,u,v,w) in zip(hist,quads));opt=int(d>0);rows={}
 def share(path,i):return q(b[path[i]],sum(b[t] for t in path))
 def sm(fn):return sum((n*fn(t,u,v,w) for n,(t,u,v,w) in zip(hist,quads)),F(0))
 zt=sm(lambda t,u,v,w:q(t,p+t+u+v+w));zu=sm(lambda t,u,v,w:q(u,p+t+u+v+w));zv=sm(lambda t,u,v,w:q(v,p+t+u+v+w));zw=sm(lambda t,u,v,w:q(w,p+t+u+v+w))
 du=sm(lambda t,u,v,w:q(1,p+t+3));dv=sm(lambda t,u,v,w:q(1,p+t+u+2));dw=sm(lambda t,u,v,w:q(1,p+t+u+v+1))
 rows['Sbranch:F2']=5*share(paths['actual'],1)-zt
 for i,sh,den in [(3,zu,du),(4,zv,dv),(5,zw,dw)]:
  for t in labels:rows[f'Sbranch:{i}:K:{t}']=sh-b[t]*den
  rows[f'Sbranch:{i}:sum-opt']=5*sh-d*den
 rows['Sbranch:3:own-T']=zu-q(d,p+4)
 rows['Sbranch:5:own-T']=zw-sm(lambda t,u,v,w:q(t,p+t+u+v+1))
 rows['Sbranch:5:own-U']=zw-sm(lambda t,u,v,w:q(u,p+t+u+v+1))
 rows['Sbranch:5:own-V']=zw-sm(lambda t,u,v,w:q(v,p+t+u+v+1))
 rows['Sbranch:4:own-U']=zv-sm(lambda t,u,v,w:q(u,p+t+u+2))
 rows['Sbranch:4:own-W']=zv-sm(lambda t,u,v,w:q(w,p+t+u+2))
 H=zv+zw+sm(lambda t,u,v,w:q(v,(p+t+u+1)*(p+t+u+2)));D1=sm(lambda t,u,v,w:q(1,p+t+u+1));D2=sm(lambda t,u,v,w:q(1,p+t+u+2))
 rows['Sbranch:r2:O']=F(5,2)*H+sm(lambda t,u,v,w:q(p+t+u,p+t+u+1))-5*opt
 rows['Sbranch:r2:exact-opt']=10*H-d*(5-d)*D1-d*(d-1)*D2
 for pn,path in paths.items():
  for i in range(start[pn],5):
   pref=sum(b[t] for t in path[:i])
   for menu,pos in [('U',1),('V',2),('W',3)]:
    val=sum(n*ty[pos] for n,ty in zip(hist,quads));rows[f'{pn}:{i+1}:sum-S{menu}']=5*share(path,i)-q(val,pref+5-i)
 # Every true node compares all three indexed reply menus.
 for menu,pos in [('U',1),('V',2),('W',3)]:
  val=sum(n*ty[pos] for n,ty in zip(hist,quads))
  for i,sh,den in [(3,zu,du),(4,zv,dv),(5,zw,dw)]:rows[f'Sbranch:{i}:sum-'+menu]=5*sh-val*den
 rows['Sbranch:3:own-V']=zu-sm(lambda t,u,v,w:q(v,p+t+3))
 rows['Sbranch:3:own-W']=zu-sm(lambda t,u,v,w:q(w,p+t+3))
 return rows

def evaluate(bits,his,lhs,include_second_correlations=False):
 d=sum(n*t for n,(t,x,y) in zip(his[0],types));assert all(sum(h)==5 for h in his)
 assert sum(n*t for n,(t,x,y) in zip(his[1],types))==d
 assert sum(n*t for n,(t,u,v,w) in zip(his[2],quads))==d
 rows=old_rows(bits,d,lhs);rows.update(third_rows(bits,his[0],lhs,'AB'));rows.update(third_rows(bits,his[1],lhs,'AE'));sr=second_rows(bits,his[2])
 if not include_second_correlations:
  for m in 'UVW':
   for i in (3,4,5):del sr[f'Sbranch:{i}:sum-'+m]
  del sr['Sbranch:3:own-V'];del sr['Sbranch:3:own-W']
 rows.update(sr);return rows

from pathlib import Path
from collections import defaultdict
import json,sys,time
L=120
REPO=Path(__file__).resolve().parents[2]
CERTIFICATE_PATH=REPO/'evidence/certificates/customer_attraction/five_player_indexed_bound.json'
certificate=json.loads(CERTIFICATE_PATH.read_text())
mode='full';dual=certificate['dual'];primal=certificate['primal'];weights=dual['integer_multipliers'];C=dual['common_denominator'];BN=dual['beta_numerator']
assert dual['row_count']==primal['row_count']==437
assert len(weights)==57 and all(v>=0 for v in weights.values())
assert all(F(v)==F(weights[n],C) for n,v in dual['multipliers'].items())
assert F(dual['beta'])==F(BN,C)<F(2063,1000)
def compositions(n,k):
 if k==1:yield(n,);return
 for i in range(n+1):
  for c in compositions(n-i,k-1):yield(i,)+c
thirdhist=list(compositions(5,8))
if mode=='full':secondhist=list(compositions(5,16))
else:
 secondhist=[]
 for d in range(6):
  for a,b in product(range(8),repeat=2):
   hh=[0]*16;hh[a]=5-d;hh[8+b]=d;secondhist.append(tuple(hh))
def scaled(v):
 v=F(v)*L;assert v.denominator==1;return v.numerator

def metrics(hists,celltypes,kind):
 names={'third':['zt','zx','zy','dx','dy','D1','D2','H','taxp','ctlast','cxlast','cyfourth'],
        'second':['zt','zu','zv','zw','du','dv','dw','H','D1','D2','taxp','ctlast','culast','cvlast','cufourth','cwforth','cfv','cfw']}[kind]
 result={};d=[sum(n*ty[0] for n,ty in zip(h,celltypes)) for h in hists];counts={m:[sum(n*ty[i] for n,ty in zip(h,celltypes)) for h in hists] for i,m in enumerate('XY' if kind=='third' else 'UVW',1)}
 for p in range(3 if kind=='third' else 2):
  out={}
  for nm in names:
   units=[]
   for ty in celltypes:
    if kind=='third':
     t,x,y=ty;load=p+t+x+y
     val={'zt':q(t,load),'zx':q(x,load),'zy':q(y,load),'dx':q(1,p+t+2),'dy':q(1,p+t+x+1),'D1':q(1,p+t+1),'D2':q(1,p+t+2),'H':q(x,load)+q(y,load)+q(x,(p+t+1)*(p+t+2)),'taxp':q(p+t,p+t+1),'ctlast':q(t,p+t+x+1),'cxlast':q(x,p+t+x+1),'cyfourth':q(y,p+t+2)}[nm]
    else:
     t,u,v,w=ty;load=p+t+u+v+w
     val={'zt':q(t,load),'zu':q(u,load),'zv':q(v,load),'zw':q(w,load),'du':q(1,p+t+3),'dv':q(1,p+t+u+2),'dw':q(1,p+t+u+v+1),'H':q(v,load)+q(w,load)+q(v,(p+t+u+1)*(p+t+u+2)),'D1':q(1,p+t+u+1),'D2':q(1,p+t+u+2),'taxp':q(p+t+u,p+t+u+1),'ctlast':q(t,p+t+u+v+1),'culast':q(u,p+t+u+v+1),'cvlast':q(v,p+t+u+v+1),'cufourth':q(u,p+t+u+2),'cwforth':q(w,p+t+u+2),'cfv':q(v,p+t+3),'cfw':q(w,p+t+3)}[nm]
    units.append(scaled(val))
   out[nm]=[sum(n*v for n,v in zip(h,units)) for h in hists]
  if kind=='third':
   for i,sh,den in [(4,'zx','dx'),(5,'zy','dy')]:
    out[f'{i}:sum-opt']=[5*z-dv*ds for z,dv,ds in zip(out[sh],d,out[den])]
    for m,vv in counts.items():out[f'{i}:sum-{m}']=[5*z-c*ds for z,c,ds in zip(out[sh],vv,out[den])]
   out['4:own-T']=[z-scaled(q(dv,p+3)) for z,dv in zip(out['zx'],d)]
   out['5:own-T']=[z-v for z,v in zip(out['zy'],out['ctlast'])];out['5:own-X']=[z-v for z,v in zip(out['zy'],out['cxlast'])];out['4:own-Y']=[z-v for z,v in zip(out['zx'],out['cyfourth'])]
  else:
   for i,sh,den in [(3,'zu','du'),(4,'zv','dv'),(5,'zw','dw')]:
    out[f'{i}:sum-opt']=[5*z-dv*ds for z,dv,ds in zip(out[sh],d,out[den])]
    for m,vv in counts.items():out[f'{i}:sum-{m}']=[5*z-c*ds for z,c,ds in zip(out[sh],vv,out[den])]
   out['3:own-T']=[z-scaled(q(dv,p+4)) for z,dv in zip(out['zu'],d)]
   for row,sh,met in [('5:own-T','zw','ctlast'),('5:own-U','zw','culast'),('5:own-V','zw','cvlast'),('4:own-U','zv','cufourth'),('4:own-W','zv','cwforth'),('3:own-V','zu','cfv'),('3:own-W','zu','cfw')]:out[row]=[z-v for z,v in zip(out[sh],out[met])]
  out['r2:O']=[scaled(F(z, L)*F(5,2))+tax-5*L*int(dv>0) for z,tax,dv in zip(out['H'],out['taxp'],d)]
  out['r2:exact-opt']=[10*z-dv*(5-dv)*d1-dv*(dv-1)*d2 for z,dv,d1,d2 in zip(out['H'],d,out['D1'],out['D2'])]
  if kind=='third':
   xx,yy=counts['X'],counts['Y']
   for mn,qx,qy in [('XX',xx,xx),('XY',xx,yy),('YY',yy,yy)]:
    out['r2:menu-'+mn]=[25*z-(cx*(5-cy)+(5-cx)*cy)*d1-2*cx*cy*d2 for z,cx,cy,d1,d2 in zip(out['H'],qx,qy,out['D1'],out['D2'])]
  result[p]=out
 return result,d,counts

TM,td,tc=metrics(thirdhist,types,'third');SM,sd,sc=metrics(secondhist,quads,'second');idsT=[[i for i,d in enumerate(td) if d==dv] for dv in range(6)];idsS=[[i for i,d in enumerate(sd) if d==dv] for dv in range(6)]

def is_second(n):return n.startswith('Sbranch:') or ':sum-S' in n
oldweights={n:v for n,v in weights.items() if not n.startswith(('AB:','AE:')) and not is_second(n)}
familyweights={tag:{n[len(tag)+1:]:v for n,v in weights.items() if n.startswith(tag+':')} for tag in ('AB','AE')}
familyweights['S']={n:v for n,v in weights.items() if is_second(n)}

# Each family's active coefficients are grouped into hist features. The new menus share
# T_i membership but no active row couples two families, so conditional-d maxima separate.
def family_score(bits,tag):
 b=dict(zip(labels,bits));kind='second' if tag=='S' else 'third';p=b['A'] if tag=='S' else sum(b[t] for t in tag);M=SM[p] if tag=='S' else TM[p];counts=sc if tag=='S' else tc;hs=secondhist if tag=='S' else thirdhist;ds=sd if tag=='S' else td;co=defaultdict(int);const=0;menuE=[[0]*6 for _ in range(3)];menuH=[[0]*6 for _ in range(3)]
 def share(path,i):return q(b[path[i]],sum(b[t] for t in path))
 for n,v in familyweights[tag].items():
  sp=n.split(':')
  if tag=='S' and n.startswith('Sbranch:'):sp=sp[1:]
  if sp[0] in ('F2','F3'):
   path=paths['actual' if tag in ('AB','S') else 'second'];i=1 if tag=='S' else 2;const+=v*scaled(5*share(path,i));co['zt']-=v
  elif sp[0] in ('3','4','5'):
   i=int(sp[0]);sh={3:'zu',4:'zv',5:'zw'}[i] if tag=='S' else {4:'zx',5:'zy'}[i];den={3:'du',4:'dv',5:'dw'}[i] if tag=='S' else {4:'dx',5:'dy'}[i]
   if sp[1]=='K':co[sh]+=v;co[den]-=v*b[sp[2]]
   else:co[':'.join(sp)]+=v
  elif sp[0]=='r2':co[':'.join(sp)]+=v
  else:
   pn=sp[0];path=paths[pn]
   if sp[1]=='reply':
    menu=sp[2].removeprefix('all-');pp=sum(b[t] for t in path[:3]);Dp=(pp+1)*(pp+2);f=list(paths).index(pn)
    for dv in range(6):
     menuE[f][dv]+=v*scaled(q(5,pp+1));menuH[f][dv]-=v*scaled(q(5,Dp))
    # The d-dependent menu count coefficient is handled as a separate full-hist feature.
    co['allreply-'+menu+'-'+str(pp)]+=v
   elif sp[1]=='r2':
    pp=sum(b[t] for t in path[:3]);Dp=(pp+1)*(pp+2);hold=share(path,3)+share(path,4)+q(b[path[3]],Dp);const+=v*scaled(25*hold);co['oldtax-'+sp[2].removeprefix('menu-')+'-'+str(pp)]+=v
   else:
    i=int(sp[1])-1;prefix=sum(b[t] for t in path[:i]);menu=sp[2].removeprefix('sum-').removeprefix('S');const+=v*scaled(5*share(path,i));co['count-'+menu]-=v*scaled(q(1,prefix+5-i))
 vectors=[]
 for feature,v in co.items():
  if not v:continue
  if feature.startswith('count-'):a=counts[feature[6:]]
  elif feature.startswith('allreply-'):
   _,menu,pn=feature.split('-');pp=int(pn);Dp=(pp+1)*(pp+2);a=[scaled(q(-5*c,pp+1)+q(dv*c,Dp)) for c,dv in zip(counts[menu],ds)]
  elif feature.startswith('oldtax-'):
   _,mn,pn=feature.split('-');pp=int(pn);qx=counts[mn[0]];qy=counts[mn[1]];a=[-scaled(q(x*(5-y)+(5-x)*y,pp+1)+q(2*x*y,pp+2)) for x,y in zip(qx,qy)]
  else:a=M[feature]
  vectors.append((v,a))
 score=[const+sum(v*a[i] for v,a in vectors) for i in range(len(hs))]
 return score,menuE,menuH

# Exact primal check uses the direct Fraction equations independently of pricing features.
assert primal['row_count']==len(primal['rows'])==len(set(primal['rows']))==437
assert primal['denominator']>0
slack={n:F(0) for n in primal['rows']};W=O=F(0)
for st in primal['atoms']:
 mass=F(st['mass_numerator'],primal['denominator']);assert mass>0;bits=tuple(map(int,st['bits']));his=[st['AB_hist'],st['AE_hist'],st['second_hist']];lhs=st['menus_lh'];d=sum(n*t for n,(t,x,y) in zip(his[0],types))
 assert len(bits)==10 and all(v in (0,1) for v in bits)
 assert [len(h) for h in his]==[8,8,16] and all(isinstance(v,int) and v>=0 for h in his for v in h)
 assert len(lhs)==3 and all(len(lh)==2 and all(isinstance(v,int) for v in lh) for lh in lhs)
 for el,h in lhs:assert 0<=h<=d and 0<=el-h<=5-d
 rows=evaluate(bits,his,lhs,include_second_correlations=mode=='full');assert set(rows)==set(slack)
 for n in slack:slack[n]+=mass*rows[n]
 W+=mass*int(any(bits[:5]));O+=mass*int(d>0)
assert W==1 and O==F(primal['comparison_cover'])==F(dual['beta'])>2;assert all(v>=0 for v in slack.values());assert sorted(n for n,v in slack.items() if v==0)==sorted(primal['zero_slacks'])

minimum=None;zeros=0;checks=0;groupmin={};t0=time.time()
for bi,bits in enumerate(product((0,1),repeat=10)):
 fs=[];extraE=[[0]*6 for _ in range(3)];extraH=[[0]*6 for _ in range(3)]
 for tag in ('AB','AE','S'):
  score,e,h=family_score(bits,tag);ids=idsS if tag=='S' else idsT;fs.append([max(score[i] for i in ix) for ix in ids])
  for f in range(3):
   for d in range(6):extraE[f][d]+=e[f][d];extraH[f][d]+=h[f][d]
 for d in range(6):
  zero=[(0,0)]*3;rr=old_rows(bits,d,zero);base=sum(v*scaled(rr[n]) for n,v in oldweights.items());EC=[];HC=[]
  for f in range(3):
   e=[(0,0)]*3;e[f]=(1,0);re=old_rows(bits,d,e);h=[(0,0)]*3;h[f]=(0,1);rh=old_rows(bits,d,h)
   EC.append(extraE[f][d]+sum(v*scaled(re[n]-rr[n]) for n,v in oldweights.items()));HC.append(extraH[f][d]+sum(v*scaled(rh[n]-rr[n]) for n,v in oldweights.items()))
  corners=[(0,0),(d,d),(5-d,0),(5,d)]
  menu=maxsum=sum(max(e*EC[f]+h*HC[f] for e,h in corners) for f in range(3))
  residual=L*BN*int(any(bits[:5]))-L*C*int(d>0)-base-menu-sum(vals[d] for vals in fs)
  assert residual>=0,(bits,d,residual)
  minimum=residual if minimum is None else min(minimum,residual);zeros+=residual==0;checks+=1;key=''.join(map(str,bits[:5]));groupmin[key]=min(groupmin.get(key,residual),residual)


report={'row_count':len(slack),'primal_atoms':len(primal['atoms']),'primal_welfare':str(W),'primal_comparison_cover':str(O),'primal_gap_above_two':str(O-2),'zero_primal_slacks':sum(v==0 for v in slack.values()),'dual_beta':dual['beta'],'positive_multipliers':len(weights),'fixed_masks':1024,'optimal_multiplicities':6,'conditional_cases':checks,'third_histograms_per_family':len(thirdhist),'second_histograms':len(secondhist),'menus_corners_per_family':4,'integer_residual_scale':str(L*C),'minimum_scaled_residual':str(minimum),'zero_conditional_residuals':zeros,'minimum_by_actual_mask':{k:str(v) for k,v in groupmin.items()},'scope':'Universal dual certificate and exact obstruction only for the fully stated necessary-condition row system; no SPE counterexample.'}

import hashlib
report['certificate_sha256']=hashlib.sha256(CERTIFICATE_PATH.read_bytes()).hexdigest()
report['audit_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
report['claim_ids']=certificate['claim_ids']
if '--include-slacks' in sys.argv:report['slacks']={n:str(v) for n,v in slack.items()}
print(json.dumps(report,indent=2))
