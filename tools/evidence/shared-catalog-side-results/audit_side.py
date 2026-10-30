#!/usr/bin/env python3
"""New side-result domains; exact support closures, not the old menu audit."""
from fractions import Fraction as F
from itertools import product,combinations
from random import Random
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent

def serial(x):
 if isinstance(x,F):return str(x)
 if isinstance(x,dict):return {str(k):serial(v) for k,v in x.items()}
 if isinstance(x,(tuple,list)):return [serial(y) for y in x]
 return x

def cells(a,b,w):
 a,b=F(a),F(b);w=list(map(F,w));total=a+b+sum(w,F());out=[]
 for status in product((-1,0,1),repeat=len(w)):
  mixed=[i for i,z in enumerate(status) if z==0];r=len(mixed)
  base=a-b+sum((z*v for z,v in zip(status,w)),F())
  low,high=-total,total
  for z,v in zip(status,w):
   if z>=0:high=min(high,v)
   if z<=0:low=max(low,-v)
  if r==1:
   if base:continue
  else:
   gap=base/(1-r)
   low=max(low,gap);high=min(high,gap)
  if low>high:continue
  endpoints=[]
  for gap in sorted(set((low,high))):
   p=[F(z+1,2) if z else (1+gap/v)/2 for z,v in zip(status,w)]
   x=a+sum((v*z for v,z in zip(w,p)),F());y=b+sum((v*(1-z) for v,z in zip(w,p)),F())
   assert x-y==gap and all(0<=z<=1 for z in p)
   # Direct conditional costs, independent of the signed support equations.
   for i,z in enumerate(p):
    c1=a+w[i]+sum((w[j]*p[j] for j in range(len(w)) if j!=i),F())
    c2=b+w[i]+sum((w[j]*(1-p[j]) for j in range(len(w)) if j!=i),F())
    assert (z==0 or c1<=c2) and (z==1 or c2<=c1)
   endpoints.append((x,y,p))
  out.append({'low':(total+low)/2,'high':(total+high)/2,'total':total,'ends':endpoints})
 assert out
 return out

def data(instance):
 w=list(map(F,instance['weights']));s=list(map(set,instance['locations']));cat=instance.get('U1',list(range(len(s))));cat=list(dict.fromkeys(cat));return w,s,cat

def all_local(instance):
 w,s,cat=data(instance);out={}
 for a in cat:
  for b in cat:
   common=sorted(s[a]&s[b]);pa=sum((w[i] for i in s[a]-s[b]),F());pb=sum((w[i] for i in s[b]-s[a]),F())
   out[a,b]=cells(pa,pb,[w[i] for i in common])
 return out

def optimum(instance):
 w,s,cat=data(instance);loc=all_local(instance);threat={t:max(min(p['low'] for p in loc[r,t]) for r in cat) for t in cat};best=None
 for (a,b),pieces in loc.items():
  for p in pieces:
   total=p['total'];den=threat[a]+threat[b];x=max(p['low'],min(p['high'],total*threat[b]/den if den else p['low']));y=total-x
   if (not x and threat[b]) or (not y and threat[a]):continue
   factor=max(F(1),threat[b]/x if x else F(),threat[a]/y if y else F())
   if best is None or factor<best['alpha']:best={'alpha':factor,'layout':[a,b],'loads':[x,y]}
 assert best
 return best

def reach(instance):
 w,s,cat=data(instance);return {t:sum((w[i] for i in s[t]),F()) for t in cat}

def sparse_menu(instance):
 w,s,cat=data(instance);R=reach(instance);order=sorted(cat,key=lambda t:(-R[t],t));d={};u={}
 for j,t in enumerate(order):
  ht=max((w[i] for i in s[t]),default=F());delta=min(R[t]/2,R[t]-ht)
  for a in order[:j]:
   common=s[a]&s[t];assert len(common)<=1
   u[a,t]=R[a]-sum((w[i] for i in common),F())
  d[t]=max([delta]+[u[a,t] for a in order[:j]]+[R[a] for a in order[j+1:]])
 best=None
 def candidate(nums,dens):
  if any(n and not z for n,z in zip(nums,dens)):return None
  return max([F(1)]+[n/z if z else F() for n,z in zip(nums,dens)])
 for j,t in enumerate(order):
  z=candidate([d[t]],[R[t]/2]);best=z if best is None or z is not None and z<best else best
  for a in order[:j]:
   z=candidate([d[t],d[a]],[u[a,t],R[t]]);best=z if best is None or z is not None and z<best else best
 return best

results={}
base={'weights':[1236068,762932,381966,72949,18221,763932],'locations':[[0,5],[0,1],[0,2],[0,3],[1,2,3,4],[5]]}
full=optimum(base);assert full['alpha']==F(499750,309017) and full['layout']==[0,4]
five={**base,'U1':list(range(5)),'U2':list(range(5))};cut=optimum(five);assert cut['alpha']==full['alpha']
results['six_and_five_site_integer']={'full':full,'restricted_five':cut,'coverage_totals':list(reach(base).values())}
three={'weights':[7071,2929,5000],'locations':[[0,1],[0],[2]]};th=optimum(three);assert th['alpha']==F(7071,5000)
four=[]
for z in [F(151,100),F(19,12),F(1587,1000)]:
 B=F(99,100);H=F(31,50);C=B*z/2;D=B/z
 inst={'weights':[H,1-H,B-H,C-H,D-B-C+2*H],'locations':[[0,1],[0,2],[0,3],[2,3,4]]}
 assert min(inst['weights'])>0
 opt=optimum(inst);assert opt['alpha']==z
 four.append({'z':z,'instance':inst,'optimum':opt})
z=F(19,12);eps=F(1,1000);H=(1-1/z**2+1/z)/2;B=1-eps;C=z/2;D=1/z
inst={'weights':[H,1-H,B-H,C-H,D-B-C+2*H],'locations':[[0,1],[0,2],[0,3],[2,3,4]]};opt=optimum(inst);assert opt['alpha']==F(6327,4000)
results['sparse_exact_fixtures']={'three':th,'four_no_loss':four,'four_epsilon':{'instance':inst,'optimum':opt}}
# All NE load endpoints in a different rational domain than the previous P/E/T audit.
local_count=0;endpoint_count=0
for k in range(5):
 for ws in product((F(1,2),F(3,2)),repeat=k):
  for a,b in product((F(0),F(2,3),F(7,3)),repeat=2):
   W=sum(ws,F());V=a+b+W;ward=max(a,min(a+W,V/2));eta=max(ws,default=F())
   for p in cells(a,b,ws):
    for x,y,prob in p['ends']:
     assert abs(x-ward)<=eta/2 and abs(y-(V-ward))<=eta/2
     if abs(a-b)>=W:assert x==ward
     endpoint_count+=1
   local_count+=1
results['granularity_local_all_NE_closures']={'inputs':local_count,'checked_support_endpoints':endpoint_count,'weights':'ordered 1/2 or 3/2, k=0..4','private_baselines':['0','2/3','7/3'],'checks':'direct conditional NE; all load endpoints satisfy Wardrop eta/2 error; domination endpoints exact'}
rng=Random(2026103019);sparsecounts={3:0,4:0};maxmenu={3:F(1),4:F(1)};granularcases=0;granulardeviations=0;worst=F(1)
for N in (3,4):
 for case in range(90):
  n=rng.randrange(1,7);sites=[set() for _ in range(N)];used=set();weights=[]
  for i in range(n):
   weights.append(F(rng.randrange(1,12),rng.randrange(1,7)))
   choices=[c for k in range(N+1) for c in combinations(range(N),k) if all(pair not in used for pair in combinations(c,2))]
   c=choices[rng.randrange(len(choices))];used.update(combinations(c,2))
   for t in c:sites[t].add(i)
  ins={'weights':weights,'locations':[sorted(s) for s in sites]};m=sparse_menu(ins);assert m is not None
  assert m**2<=2 if N==3 else m**3<=4
  ref=optimum(ins);assert ref['alpha']<=m
  sparsecounts[N]+=1;maxmenu[N]=max(maxmenu[N],m)
  R=reach(ins);rmax=max(R.values());theta=max((weights[i] for s,t in combinations(range(N),2) for i in sites[s]&sites[t]),default=F())
  if not rmax or theta>=rmax:continue
  ward={}
  for s in range(N):
   for t in range(N):
    W=sum((weights[i] for i in sites[s]&sites[t]),F());a=R[s]-W;b=R[t]-W;V=a+b+W;x=max(a,min(a+W,V/2));ward[s,t]=(x,V-x)
  on=max(ward,key=lambda p:tuple(sorted(ward[p])));x0,y0=ward[on];assert min(x0,y0)>=rmax/2
  bound=(rmax+theta)/(rmax-theta);loc=all_local(ins);s,t=on
  ownlow=[R[s]/2,R[t]/2] if s==t else [min(p['low'] for p in loc[s,t]),min(p['total']-p['high'] for p in loc[s,t])]
  for who in (0,1):
   for dest in range(N):
    if dest==on[who]:continue
    pair=(dest,t) if who==0 else (s,dest)
    if pair[0]==pair[1]:high=R[dest]/2
    elif who==0:high=max(p['high'] for p in loc[pair])
    else:high=max(p['total']-p['low'] for p in loc[pair])
    assert high<=bound*ownlow[who]
    if ownlow[who]:worst=max(worst,high/ownlow[who])
    granulardeviations+=1
  granularcases+=1
results['sparse_random_finite']={'seed':2026103019,'cases_by_sites':sparsecounts,'largest_constructive_menu_factor':maxmenu,'compared_with_all_support_optimum':True}
results['granularity_complete_rule_worst_NE_choices']={'instances_with_theta_below_R':granularcases,'actual_deviation_families':granulardeviations,'largest_observed_worst_NE_gain':worst,'meaning':'all support endpoint loads for on-path and off-path choices, balanced on every diagonal; finite domain only'}
results['not_claimed']=['universal phi upper theorem passed','external literature read successfully','newness established','producer code proves arbitrary inputs','old menu/box/PDF modules repeated']
(HERE/'math-results.json').write_text(json.dumps(serial(results),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(serial({k:v for k,v in results.items() if k not in ['sparse_exact_fixtures']}),ensure_ascii=False,indent=2))
