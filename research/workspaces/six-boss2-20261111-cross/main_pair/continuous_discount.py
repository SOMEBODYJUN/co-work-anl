"""Exact continuous-discount optimization for the balanced two-tail fixed row.
For source coefficient = total last-query weight, e00+e11=e01+e10.
The two-cycle is between the self-loop and one-switch policy, so only the
latter two can minimize. Each aggregate slack is convex piecewise affine.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
from itertools import product
import json,hashlib
B=Path(__file__).resolve().parent.parent
p=B/'master_cuts/dynamic_5727_exact.json';a=json.loads(p.read_text());cols=a['columns'];blocks=[];cur=None
for i,c in enumerate(cols):
 if c['kind']=='hist':cur={'index':i,'col':c,'joint':[]};blocks.append(cur)
 elif c['kind']=='joint-reply':cur['joint'].append((i,c))

def pay(n,d):return F(n,d) if n else F(0)
u5=sum((F(b['col']['weight'])*pay(int(b['col']['actual_bits'][4]),sum(map(int,b['col']['actual_bits']))) for b in blocks),F(0))
u6=sum((F(b['col']['weight'])*pay(int(b['col']['actual_bits'][5]),sum(map(int,b['col']['actual_bits']))) for b in blocks),F(0))
budget=u5+F(3,8)*u6+F(cols[0]['weight'])/64

def data_for(b):
 bits=list(map(int,b['col']['actual_bits']));pfx=sum(bits[:4]);ell=sum(bits[:5]);q=F(2*bits[5]+sum(n*(i&1) for i,n in enumerate(b['col']['hist'])),8)
 price=F(3,8*(ell+1))+F(1,64);A=q/(pfx+1);C=price+q/(pfx+2);D=F(1,pfx+1)-price
 return A,C,D

def phi(A,C,D,theta,t):
 k=theta*(C-A+D)-D
 return A+min(F(0),k) if t==0 else C-max(F(0),k)

results=[]
for orb in [(0,0),(1,0),(1,1)]:
 for member in [0,1]:
  atoms=[];breaks={F(0),F(1)}
  for b in blocks:
   h=b['col']['hist'];hm=F(b['col']['weight']);one=F(0);ct=6 if orb[1] else 30
   for i,c in b['joint']:
    fam,diag,wi,wj=c['group']
    if (fam,diag)!=orb or not c['state'][member]:continue
    u=4*wi[0]+2*wi[1]+wi[2];v=4*wj[0]+2*wj[1]+wj[2]
    n=h[u] if diag else h[u]*(h[v]-(u==v));one+=F(n,ct)*F(c['weight'])
   assert 0<=one<=hm
   A,C,D=data_for(b);br=D/(C-A+D)
   if 0<br<1:breaks.add(br)
   atoms.extend([(hm-one,A,C,D,0),(one,A,C,D,1)])
  values=[]
  for theta in sorted(breaks):
   sl=budget-sum((w*phi(A,C,D,theta,t) for w,A,C,D,t in atoms),F(0));values.append((sl,theta))
  val,theta=min(values)
  results.append({'orb':orb,'member':member,'minimum_theta':str(theta),'minimum_slack':str(val),'float':float(val),'candidate_breakpoints':list(map(str,sorted(breaks))),'scope':'theta=1 denotes continuous limit only; theta<1 is a finite Bellman certificate','all_breakpoint_values':[[str(t),str(s)] for s,t in values]})
print([{k:v for k,v in r.items() if k not in ['candidate_breakpoints','all_breakpoint_values']} for r in results])
(B/'main_pair/continuous_discount_5727.json').write_text(json.dumps({'scope':'Exact entire [0,1] fixed-weight balanced k=2 discounted family on this point, not full arbitrary multiplier cone','input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'results':results},indent=2)+'\n')
