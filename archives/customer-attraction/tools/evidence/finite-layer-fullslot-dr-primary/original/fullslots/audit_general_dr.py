"""Independent Fraction audit of a positive finite DR-SUMmin-full counterexample.
Uses the rounded integer potential and strategy only, never the MILP rows.
"""
import json
from fractions import Fraction as F
from itertools import product
from pathlib import Path
base=Path(__file__).resolve().parent
src=json.loads((base/'dr_counterexample_exact.json').read_text())
phi={tuple(map(int,key.split(','))):F(value) for key,value in src['potential'].items()}
sig={tuple(map(int,key.split(','))) if key else ():a for key,a in src['strategy'].items()}
k=4;m=3
def ct(h):return tuple(h.count(a) for a in range(k))
def plus(q,a):r=list(q);r[a]+=1;return tuple(r)
def val(h):return phi[ct(h)]
def play(h):
 h=tuple(h)
 while len(h)<m:h=h+(sig[h],)
 return h
def u(z,j):return val(z)-val(z[:j]+z[j+1:])
def G(z):return sum((phi[plus(ct(z),a)]-val(z) for a in range(k)),F())/k
mono=[];dr=[]
for q in phi:
 if sum(q)<m+1:
  for a in range(k):
   d=phi[plus(q,a)]-phi[q];mono.append(d);assert d>=0,(q,a,d)
 if sum(q)<m:
  for a in range(k):
   for b in range(a,k):
    d=phi[plus(q,a)]+phi[plus(q,b)]-phi[q]-phi[plus(plus(q,a),b)]
    dr.append(d);assert d>=0,(q,a,b,d)
ics=[]
for h in sig:
 z=play(h);chosen=u(z,len(h))
 for a in range(k):
  d=chosen-u(play(h+(a,)),len(h));ics.append(d);assert d>=0,(h,a,d)
z=play(());pay=[u(z,j) for j in range(m)];W=sum(pay,F())
menus=[];queries=[]
for i in range(m):
 h=z[:i];leaves=[play(h+(a,)) for a in range(k)];q=[G(t) for t in leaves]
 menus.append({'position':i+1,'forced_leaf':leaves,'query_values':list(map(str,q)),'minimum':str(min(q))})
 queries.append(min(q))
gap=sum(queries,F())-W;assert gap>0
# A CAG harmonic potential obeys phi(aa)-phi(empty)=3/2*(phi(a)-phi(empty)).
nonCAG=[]
for a in range(k):
 d=val((a,a))-F(3,2)*val((a,))+F(1,2)*val(())
 if d:nonCAG.append({'action':a,'harmonic_repeat_residual':str(d)})
# Local third difference must be nonnegative in a harmonic customer potential.
third=[]
for q in phi:
 if sum(q)<=1:
  for a in range(k):
   for b in range(a,k):
    for c in range(b,k):
     d=F()
     acts=(a,b,c)
     for mask in range(8):
      r=q
      for j,t in enumerate(acts):
       if mask>>j&1:r=plus(r,t)
      d+=(-1)**(3-mask.bit_count())*phi[r]
     if d<0:third.append({'background':q,'actions':acts,'third_difference':str(d)})
out={'identity':'finite-domain DR-SUMmin-full auxiliary counterexample, not CAG',
 'm':m,'k':k,'query_distribution':['1/4']*k,'potential_scale':'exact integer input, independently audited with Fraction',
 'actual':z,'actual_payoffs':list(map(str,pay)),'total_marginal_utility':str(W),
 'menus':menus,'sum_min_query':str(sum(queries,F())),'gap':str(gap),
 'checks':{'potential_states':len(phi),'monotonic_edges':len(mono),'DR_local_squares_including_repetition':len(dr),'ordered_decision_histories':len(sig),'SPE_comparisons':len(ics),'minimum_monotonic_margin':str(min(mono)),'minimum_DR_margin':str(min(dr)),'minimum_IC_margin':str(min(ics))},
 'non_CAG_repeat_witnesses':nonCAG,'non_CAG_negative_third_difference':third[:1]}
(base/'dr_counterexample_audit.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
