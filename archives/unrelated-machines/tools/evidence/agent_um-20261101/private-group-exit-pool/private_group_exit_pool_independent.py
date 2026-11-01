"""私有组共同退出与完整接收池的独立原调度枚举。

The proof contract was reconstructed before reading the normative code.
The second constructor enumerates macro destinations and covering subsets;
it does not use the normative Hungarian or covering-FPTAS implementation.
Original OPT is computed by enumerating assignments in the full original
processing-time matrix.  A sequential threshold restoration is independent
of the normative minimum-current-load restoration.  Finite checks are not
a proof of either the kernel theorem or UM-TARGET-v1.
"""
from fractions import Fraction as F
from itertools import product
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
import hashlib,json,platform,random

ROOT=Path(__file__).resolve().parents[3]
NORM=Path(__file__).with_name('private_group_exit_pool.py')

def matrix(I):
 h=I['h']; a=I['a']; rows=[[]for _ in range(h+len(a))]
 for j,M in enumerate(I['macros']):
  for i in range(h):rows[i].append(M['home'][i])
  for z,az in enumerate(a):rows[h+z].append(None if M['c']is None else I['pool_times'][j][z])
 for j,Q in enumerate(I['private'],len(I['macros'])):
  for i in range(h):rows[i].append(Q['p']if Q['home']==i else None)
  for z,az in enumerate(a):rows[h+z].append(None if Q['c']is None else I['pool_times'][j][z])
 return rows

def full_original_opt(I):
 P=matrix(I);n=len(P[0]);m=len(P)
 opts=[[i for i in range(m)if P[i][j]is not None]for j in range(n)]
 assert all(opts)
 best=None;sig=None;leaves=0
 # Exhaustive original assignments, with no mode/matching reduction.
 for s in product(*opts):
  load=[F(0)]*m
  for j,i in enumerate(s):load[i]+=P[i][j]
  c=max(load,default=F(0));leaves+=1
  if best is None or c<best:best=c;sig=s
 return best,sig,leaves

def exact_modes(I):
 h=I['h'];T=I['T']; b=len(I['macros']); modes={}
 forced=[j for j,Q in enumerate(I['private'])if Q['p']is None]
 for i in range(h):
  homeonly=[j for j,Q in enumerate(I['private'])if Q['home']==i and Q['c']is None]
  flex=[j for j,Q in enumerate(I['private'])if Q['home']==i and Q['p']is not None and Q['c']is not None]
  fixed=sum((I['private'][j]['p']for j in homeonly),F(0))
  for t in range(-1,b):
   bp=F(0)if t==-1 else I['macros'][t]['home'][i]
   if bp is None or fixed+bp>T:continue
   best=None
   for bits in product([0,1],repeat=len(flex)):
    stay=sum((I['private'][j]['p']for j,k in zip(flex,bits)if not k),F(0))
    if fixed+bp+stay>T:continue
    out=[j for j,k in zip(flex,bits)if k]
    cost=sum((I['private'][j]['c']for j in out),F(0))
    if best is None or cost<best[0]:best=(cost,out)
   assert best is not None
   modes[i,t]=best
 return modes,forced

def work_axis_restore(a,works,A,reverse=False):
 order=list(range(len(a)))
 if reverse:order.reverse()
 if A==0:
  assert all(c==0 for c in works)
  return [order[0]]*len(works)
 caps=[A/a[z]for z in order]
 prefix=F(0);left=F(0);k=0;right=caps[0];out=[]
 assert sum(works,F(0))<=sum(caps,F(0))
 for c in works:
  if c==0 and prefix==sum(caps,F(0)):
   out.append(order[-1]);continue
  while prefix>=right and k+1<len(order):
   k+=1;left=right;right+=caps[k]
  assert prefix<right or c==0
  out.append(order[k]);prefix+=c
 return out

def sequential_restore(I,labels,reverse=False):
 # Keep filling one actual sink until its current load exceeds rho*A,
 # then move to the next sink.  All sinks cannot close with work left:
 # work already placed >= sum_z load_z/(rho*a_z) > A*sum_z 1/a_z.
 a=I['a'];order=list(range(len(a)))
 if reverse:order.reverse()
 rho=I['rho'];A=(1+I['eta'])*I['T'];target=rho*A
 loads=[F(0)]*len(a);k=0;sig=[]
 for j in labels:
  row=I['pool_times'][j]
  if all(p==0 for p in row):
   sig.append(order[0]);continue
  while loads[order[k]]>target:
   k+=1
   assert k<len(order)
  z=order[k];sig.append(z);loads[z]+=row[z]
  assert loads[z]<=(rho*(1+I['eta'])+I['beta'])*I['T']
 return sig

def second_construct(I,reverse=False):
 h=I['h'];a=I['a'];T=I['T'];eta=I['eta']; beta=I['beta'];B=I['macros'];Q=I['private'];b=len(B)
 modes,forced=exact_modes(I)
 opts=[]
 for t,M in enumerate(B):
  opts.append([i for i in range(h)if (i,t)in modes]+([-1]if M['c']is not None else []))
 best=None
 for sig in product(*opts):
  hom=[i for i in sig if i>=0]
  if len(hom)!=len(set(hom)):continue
  byhome={i:t for t,i in enumerate(sig)if i>=0}
  if any((i,byhome.get(i,-1))not in modes for i in range(h)):continue
  evac=forced+sum((modes[i,byhome.get(i,-1)][1]for i in range(h)),[])
  exits=[t for t,i in enumerate(sig)if i<0]
  cost=sum((Q[j]['c']for j in evac),F(0))+sum((B[t]['c']for t in exits),F(0))
  if best is None or cost<best[0]:best=(cost,sig,evac,exits)
 if best is None:return None
 cost,sig,evac,exits=best
 W=T*sum((1/az for az in a),F(0));A=(1+eta)*T
 if cost>(1+eta)*W:return None
 s=list(sig)+[q['home']for q in Q]
 outs=exits+[b+j for j in evac]
 works=[B[t]['c']for t in exits]+[Q[j]['c']for j in evac]
 zsig=sequential_restore(I,outs,reverse)
 for j,z in zip(outs,zsig):s[j]=h+z
 P=matrix(I);load=[F(0)]*len(P)
 assert len(s)==len(P[0])
 for j,i in enumerate(s):
  assert i is not None and i>=0 and P[i][j]is not None
  load[i]+=P[i][j]
 assert all(l<=T for l in load[:h])
 assert all(l<=(I['rho']*(1+eta)+beta)*T for l in load[h:])
 actual_measure=sum((load[h+z]/a[z]for z in range(len(a))),F(0))
 assert sum(works,F(0))<=actual_measure<=I['rho']*sum(works,F(0))
 return s,load,cost

def rnd_instance(rng,rho):
 h=rng.randrange(4); nz=rng.randrange(1,4);a=[rng.choice([F(1,2),F(1),F(2)])for _ in range(nz)]
 T=rng.choice([F(0),F(1),F(2)]);eta=F(1,8);beta=F(1,8)
 b=rng.randrange(4);q=rng.randrange(7-b)if h else 0
 vals=[F(0),beta*T/(rho*max(a))/2,beta*T/(rho*max(a))]
 B=[]
 for _ in range(b):
  home=[rng.choice([None,T*F(2,3),T,T*F(4,3)])if T else rng.choice([None,F(1)])for _ in range(h)]
  c=rng.choice(vals+[None])
  if c is None and not any(x is not None for x in home):c=F(0)
  B.append({'home':home,'c':c})
 Q=[]
 for _ in range(q):
  home=rng.randrange(h)if h else None
  p=rng.choice([F(0),T/4,T,T*F(5,4),None])if h else None
  if T==0 and h:p=rng.choice([F(0),F(1),None])
  c=rng.choice(vals+[None])
  if p is None and c is None:c=F(0)
  Q.append({'home':home,'p':p,'c':c})
 profiles=[]
 for V in B+Q:
  c=V['c']
  profiles.append(None if c is None else [az*c*(1+rng.choice([F(0),F(1,2),F(1)])*(rho-1))for az in a])
 return dict(h=h,a=a,T=T,eta=eta,beta=beta,rho=rho,macros=B,private=Q,pool_times=profiles)

def validate(I):
 assert I['a']and all(az>0 for az in I['a'])
 assert I['T']>=0 and I['eta']>0 and I['beta']>0 and I['eta']+I['beta']<1
 for M in I['macros']:
  assert all(p is None or p>I['T']/2 for p in M['home'])
 for V,row in zip(I['macros']+I['private'],I['pool_times']):
  if V['c']is not None:
   assert all(az*V['c']<=p<=I['rho']*az*V['c']and p<=I['beta']*I['T']for az,p in zip(I['a'],row))

def check_actual(I,result):
 assert result['status']=='SCHEDULE'
 P=matrix(I);s=result['assignment'];n=len(P[0]);h=I['h']
 assert len(s)==n
 load=[F(0)]*len(P)
 for j,i in enumerate(s):
  assert type(i)is int and 0<=i<len(P)and P[i][j]is not None
  load[i]+=P[i][j]
 assert load==result['loads']
 assert all(v<=I['T']for v in load[:h])
 bound=(I['rho']*(1+I['eta'])+I['beta'])*I['T']
 assert all(v<=bound for v in load[h:])
 return load

def normative_call(norm,I):
 return norm.solve_exit_pool(I['h'],[M['home']+[M['c']]for M in I['macros']],
  [(Q['home'],Q['p'],Q['c'])for Q in I['private']],I['a'],I['T'],I['eta'],I['beta'],
  rho=I['rho'],pool_times=I['pool_times'])

if __name__=='__main__':
 spec=spec_from_file_location('norm_exit_pool',NORM);norm=module_from_spec(spec);spec.loader.exec_module(norm)
 rng=random.Random(1739);reports=[]
 for rho in [F(1),F(9,8)]:
  cases=leaves=feasible=success=norm_success=false_reject=zero=emptyH=optzero=0
  for k in range(700):
   I=rnd_instance(rng,rho);validate(I);opt,orig,n=full_original_opt(I)
   x=second_construct(I);y=second_construct(I,True);z=normative_call(norm,I)
   assert (x is None)==(y is None)
   if opt<=I['T']:
    feasible+=1
    if x is None or z['status']!='SCHEDULE':false_reject+=1
    assert x is not None and z['status']=='SCHEDULE'
   if x is not None:success+=1
   if z['status']=='SCHEDULE':
    load=check_actual(I,z);norm_success+=1
    if opt==0:assert max(load)==0
   else:assert z['status']=='REJECT_TARGET'and opt>I['T']
   cases+=1;leaves+=n;zero+=I['T']==0;emptyH+=I['h']==0;optzero+=opt==0
  reports.append(dict(rho=str(rho),eta='1/8',beta='1/8',factor=str(rho*F(9,8)+F(1,8)),cases=cases,
   original_assignments=leaves,T_feasible=feasible,second_success=success,norm_success=norm_success,
   false_reject=false_reject,T_zero=zero,H_empty=emptyH,OPT_zero=optzero))
 print(json.dumps(dict(title='私有组共同退出与完整池的独立原调度审计',seed=1739,python=platform.python_version(),
  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),normative_sha256=hashlib.sha256(NORM.read_bytes()).hexdigest(),
  arithmetic='Fraction; full original assignments; exact covering subsets and macro destination enumeration',
  limitation='Finite cases only; does not prove the kernel theorem or any general unrelated-machine approximation',reports=reports),ensure_ascii=False,indent=2))
