"""Fixed complete policy cone on monotone DR potentials with self congestion.
A positive result requires independent exact rational verification; numerical
zero/feasibility outcomes are exploratory only.
"""
import argparse,json,math,random
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

ROOT=Path(__file__).resolve().parents[5]
OUT=Path(__file__).resolve().parent

def states(k,m):
 def layer(r,j=0):
  if j==k-1:yield (r,);return
  for z in range(r+1):
   for tail in layer(r-z,j+1):yield (z,)+tail
 return tuple(q for r in range(m+1) for q in layer(r))

def cone(actions,k,m,p=None,strong=False,moments=False):
 ss=states(k,m);idx={q:i for i,q in enumerate(ss)};d=len(ss);p=p or [F(1,k)]*k
 def add(q,a):v=list(q);v[a]+=1;return tuple(v)
 def unit(i):v=[0.]*d;v[i]=1.;return np.array(v)
 def phi(q):return unit(idx[q])
 def marginal(q,a):return phi(add(q,a))-phi(q)
 def payoff(s,a):q=list(s);q[a]-=1;return phi(s)-phi(tuple(q))
 def terminal(h):
  while len(h)<m:h=h+(actions[h],)
  return tuple(h.count(a) for a in range(k))
 ineq=[];rhs=[]
 def ge(v,b=0):ineq.append(np.r_[-v,0.]);rhs.append(-b)
 # Monotonicity and adjacent DR up to size m.
 for q in ss:
  if sum(q)<m:
   for a in range(k):ge(marginal(q,a))
  if sum(q)<=m-2:
   for a in range(k):
    for b in range(k):ge(marginal(q,a)-marginal(add(q,b),a))
 # Strong self-congestion order at every possible total population <=m.
 for q in ss:
  if sum(q)<=m-2:
   for a in range(k):
    for c in range(k):ge(marginal(add(q,c),a)-marginal(add(q,a),a))
 if strong:
  # CAG sharp dilution under transferring a non-a player to a.
  # This implies the full-population pure-state bound requested by parent.
  for q in ss:
   for a in range(k):
    if not q[a]:continue
    for c in range(k):
     if c!=a and q[c]:
      z=list(q);z[c]-=1;z[a]+=1;z=tuple(z)
      ge((q[a]+1)*payoff(z,a)-q[a]*payoff(q,a))
 # Complete ordered history SPE constraints.
 for h,a in actions.items():
  on=payoff(terminal(h),a)
  for b in range(k):
   if b!=a:ge(on-payoff(terminal(h+(b,)),b))
 # p's genuine static safety, against every count tuple b of m-1 others.
 for b in ss:
  if sum(b)==m-1:
   v=sum((float(p[a])*marginal(b,a) for a in range(k)),np.zeros(d))
   ineq.append(np.r_[-v,1.]);rhs.append(0.)
 zero=(0,)*k;eq=[np.r_[phi(zero),0.]];eqrhs=[0.]
 if strong:
  for a in range(k):
   for t in range(2,m+1):
    q=tuple(t if b==a else 0 for b in range(k));H=sum((F(1,z) for z in range(1,t+1)),F(0))
    eq.append(np.r_[phi(q)-float(H)*marginal(zero,a),0.]);eqrhs.append(0.)
 if moments:
  # Exact common-support efficiency at all populations <=m. Together with
  # the potential marginal identity, this imposes all signed common-customer
  # harmonic moment identities (the Shapley recursion).
  for q in ss:
   if not sum(q):continue
   support=tuple(int(z>0) for z in q)
   Wq=sum((q[a]*payoff(q,a) for a in range(k) if q[a]),np.zeros(d))
   Wsupport=sum((payoff(support,a) for a in range(k) if support[a]),np.zeros(d))
   eq.append(np.r_[Wq-Wsupport,0.]);eqrhs.append(0.)
 # Compact scaling: every singleton potential at most 1.
 for a in range(k):ineq.append(np.r_[marginal(zero,a),0.]);rhs.append(1.)
 actual=terminal(());welfare=sum((actual[a]*payoff(actual,a) for a in range(k) if actual[a]),np.zeros(d));obj=np.r_[welfare,-float(m)]
 res=linprog(obj,A_ub=ineq,b_ub=rhs,A_eq=eq,b_eq=eqrhs,bounds=[(None,None)]*d+[(None,None)],method='highs')
 if not res.success:raise RuntimeError(res.message)
 return res,ss,obj,np.array(ineq),np.array(rhs),actual

def exact_check(ans,ss,obj,A,b,k,m,actions,p,strong=False,moments=False):
 # All coefficients are integral except p, so reconstruct the original rows
 # to exact rational arithmetic instead of trusting floating slacks.
 vals=[F(float(x)).limit_denominator(10**7) for x in ans.x]
 den=math.lcm(*(x.denominator for x in vals));vv=[int(x*den) for x in vals];gg=math.gcd(*vv);vv=[x//gg for x in vv];scale=F(den,gg)
 ph={q:F(vv[i]) for i,q in enumerate(ss)};v=F(vv[-1]);slacks={}
 def add(q,a):w=list(q);w[a]+=1;return tuple(w)
 def mar(q,a):return ph[add(q,a)]-ph[q]
 def pay(s,a):q=list(s);q[a]-=1;return ph[s]-ph[tuple(q)]
 def term(h):
  while len(h)<m:h=h+(actions[h],)
  return tuple(h.count(a) for a in range(k))
 mono=[];dr=[];selfc=[];spe=[];safe=[];dilute=[];pure=[];efficiency=[]
 for q in ss:
  if sum(q)<m:
   for a in range(k):mono.append(mar(q,a))
  if sum(q)<=m-2:
   for a in range(k):
    for c in range(k):dr.append(mar(q,a)-mar(add(q,c),a));selfc.append(mar(add(q,c),a)-mar(add(q,a),a))
  if sum(q)==m-1:safe.append(sum(p[a]*mar(q,a) for a in range(k))-v)
  if strong:
   for a in range(k):
    if not q[a]:continue
    for c in range(k):
     if c!=a and q[c]:
      z=list(q);z[c]-=1;z[a]+=1;z=tuple(z)
      dilute.append((q[a]+1)*pay(z,a)-q[a]*pay(q,a))
 if strong:
  for a in range(k):
   for t in range(2,m+1):
    q=tuple(t if b==a else 0 for b in range(k));H=sum((F(1,z) for z in range(1,t+1)),F(0))
    pure.append(ph[q]-H*mar((0,)*k,a))
 if moments:
  for q in ss:
   if not sum(q):continue
   support=tuple(int(z>0) for z in q)
   efficiency.append(sum(q[a]*pay(q,a) for a in range(k) if q[a])-sum(pay(support,a) for a in range(k) if support[a]))
 for h,a in actions.items():
  for c in range(k):spe.append(pay(term(h),a)-pay(term(h+(c,)),c))
 actual=term(());W=sum(actual[a]*pay(actual,a) for a in range(k) if actual[a]);gap=W-m*v
 slacks={name:str(min(x)) for name,x in [('monotonicity',mono),('DR',dr),('self_congestion',selfc),('SPE',spe),('static_safety',safe)]}
 if strong:
  slacks['sharp_dilution']=str(min(dilute));slacks['harmonic_pure_error']=str(max(map(abs,pure)))
  if any(pure):return None
 if moments:
  slacks['common_support_efficiency_error']=str(max(map(abs,efficiency)))
  if any(efficiency):return None
 if any(F(x)<0 for x in slacks.values()) or gap>=0:return None
 return {'status':'LP candidate with exact Fraction back-substitution; independent review separate','domain':'nonnegative integer count vectors with total at most m','strong_CAG_constraints':strong,'common_support_efficiency':moments,'topics':k,'players':m,'actual_counts':actual,'welfare':str(W),'safety_lower_bound':str(v),'gap':str(gap),'query':[str(x) for x in p],'min_slacks':slacks,'potential':[{'counts':q,'value':str(ph[q])} for q in ss],'actions':[{'history':h,'action':a} for h,a in sorted(actions.items(),key=lambda z:(len(z[0]),z[0]))]}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('source');ap.add_argument('--out',default='potential_cone_probe.json');ap.add_argument('--queries',type=int,default=20);ap.add_argument('--seed',type=int,default=1);ap.add_argument('--strong',action='store_true');ap.add_argument('--moments',action='store_true');args=ap.parse_args();source=ROOT/args.source;data=json.loads(source.read_text());data=data.get('strategy',data);actions={tuple(v['history']):v['action'] for v in data['actions']};k=1+max([a for a in actions.values()]+[a for h in actions for a in h]);m=max(map(len,actions))+1;rng=random.Random(args.seed);results=[]
 for j in range(args.queries):
  pp=[1]*k if j==0 else [rng.randrange(6) for _ in range(k)]
  if not sum(pp):continue
  p=[F(x,sum(pp)) for x in pp];res,ss,obj,A,b,actual=cone(actions,k,m,p,args.strong,args.moments);row={'query':[str(x) for x in p],'numerical_gap':res.fun};results.append(row);print(json.dumps(row),flush=True)
  if res.fun<-1e-8:
   exact=exact_check(res,ss,obj,A,b,k,m,actions,p,args.strong,args.moments)
   if exact:
    path=OUT/('candidate_'+Path(args.out).stem+'.json');path.write_text(json.dumps(exact,indent=2)+'\n');row['exact_candidate']=str(path.relative_to(ROOT));break
 answer={'status':'finite fixed-policy cone exploration','source':args.source,'topics':k,'players':m,'queries':results};(OUT/args.out).write_text(json.dumps(answer,indent=2)+'\n')
if __name__=='__main__':main()
