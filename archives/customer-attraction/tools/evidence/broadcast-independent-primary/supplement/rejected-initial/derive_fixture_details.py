"""Post-reading direct-definition expansion, not another original audit run or blind verifier."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json
LABELS=('H','A','B','T','D','E')
H,A,B,T,D,E=range(6)
blocks=[('H',8,{H}),('B',3,{B}),('T',3,{T}),('AD',2,{A,D}),('AE',2,{A,E}),('BDE',2,{B,D,E}),('TDE',2,{T,D,E})]
likes={name+str(k):s for name,size,s in blocks for k in range(size)}
topics={a:{x for x,s in likes.items() if a in s} for a in range(6)}
last_table=((D,B,D,D,E,D),(B,H,H,H,H,H),(D,H,H,H,H,H),(D,H,H,H,H,H),(H,H,H,H,H,H),(H,H,H,H,H,H))
second=(A,H,H,H,T,H)
strategy={():H,**{(a,):second[a] for a in range(6)},**{(a,b):last_table[a][b] for a,b in product(range(6),repeat=2)}}
def finish(g):
 z=tuple(g)
 while len(z)<3:z+=(strategy[z],)
 return z

def count(z,x):return sum(a in likes[x] for a in z)
def pay(z,i,keep=None):return sum((F(1,count(z,x)) for x in topics[z[i]] if keep is None or x in keep),F())
def cov(z):return len(set().union(*(topics[a] for a in z)))
def named(z):return [LABELS[a] for a in z]
def show(v):
 if isinstance(v,F):return str(v)
 if isinstance(v,dict):return {str(k):show(x) for k,x in v.items()}
 if isinstance(v,(tuple,list)):return [show(x) for x in v]
 return v
Z=finish(());C=set().union(*(topics[a] for a in Z));actual=[pay(Z,i) for i in range(3)]
# The explicit 43-action table above is checked at every node by direct payoff.
ic=[]
for g in strategy:
 i=len(g);own=pay(finish(g),i)
 for a in range(6):
  alt=finish(g+(a,));gap=own-pay(alt,i);assert gap>=0
  ic.append({'history':named(g),'alternative':LABELS[a],'gap':str(gap)})

def row(g,fresh=False,cancel=False):
 i=len(g);a=strategy[g];B=finish(g);Areset=finish(Z[:i]+(a,));edges={};past={};negative=F();retained=F();qplus=F();removed=F()
 for x in sorted(topics[a]):
  if fresh and x in C:continue
  ja={j for j in range(3) if j!=i and Areset[j] in likes[x]};jb={j for j in range(3) if j!=i and B[j] in likes[x]};price=F(1,count(Areset,x)*count(B,x));pos=sorted(ja-jb,key=lambda j:(j>i,j));n=len(jb-ja);r=min(len(pos),n) if cancel else 0
  removed+=r*price;retained+=(1+len(ja&jb)+r)*price;negative+=(n-r)*price
  for j in pos[r:]:
   qplus+=price
   if j>i:edges[Areset[:j]]=edges.get(Areset[:j],F())+price
   else:past[j,x]=past.get((j,x),F())+price
 return {'v':pay(B,i),'d':pay(Areset,i),'e':actual[i]-pay(Areset,i),'X':pay(B,i,C),'Y':pay(Areset,i,C),'N':negative,'retained':retained,'removed_same_customer_positive_price':removed,'future':edges,'past':past,'A':Areset,'B':B}

injection={(D,):F(1)};flows={};selected=[]
for mode in ('all','fresh','cancel'):
 rows={g:row(g,fresh=mode=='fresh',cancel=mode=='cancel') for g in strategy};incoming=dict(injection);beta={}
 for g in sorted(strategy,key=lambda x:(len(x),x)):
  r=rows[g];beta[g]=incoming.get(g,F())/r['v']
  for child,q in r['future'].items():incoming[child]=incoming.get(child,F())+beta[g]*q
 active=[]
 for g in strategy:
  if not beta[g]:continue
  r=rows[g];active.append({'history':named(g),'beta':str(beta[g]),'incoming':str(incoming[g]),'A':named(r['A']),'B':named(r['B']),**{k:str(r[k]) for k in ('v','d','e','X','Y','N','retained','removed_same_customer_positive_price')},'future':[{'target':named(t),'raw_price':str(v),'transmitted':str(beta[g]*v)} for t,v in r['future'].items()],'past':[{'role_1based':jx[0]+1,'customer':jx[1],'raw_price':str(v),'transmitted':str(beta[g]*v)} for jx,v in sorted(r['past'].items())]})
 flows[mode]={'active_contexts':active,'mass':str(sum((beta[g]*(rows[g]['v']-sum(rows[g]['future'].values(),F())) for g in strategy),F()))}
 if mode=='all':
  coupons=[]
  for j in range(3):
   for x in sorted(topics[Z[j]]):
    current=sum((beta[g] for g in strategy if len(g)==j),F());pastload=count(Z,x)*sum((beta[g]*rows[g]['past'].get((j,x),F()) for g in strategy if len(g)>j),F());gamma=F(1,8) if j==0 else F()
    coupons.append({'role_1based':j+1,'customer':x,'actual_coupon_value':str(F(1,count(Z,x))),'natural_current_coefficient':str(current),'past_coefficient':str(pastload),'natural_gross_coefficient':str(current+pastload),'source_uniform_coefficient':str(gamma),'source_plus_natural_gross_coefficient':str(gamma+current+pastload)})
result={'scope':'Post-reading supplemental derivation from explicit inputs and 43-action table. Original audit_broadcast.py was not executed again. This is not a blind or historically independent implementation.','blocks':[{'name':name,'unit_customers':size,'labels':named(sorted(s))} for name,size,s in blocks],'second_actions':[LABELS[a] for a in second],'last_actions':[[LABELS[a] for a in row] for row in last_table],'root_alternative_leaves':[{'action':LABELS[a],'leaf':named(finish((a,))),'root_profit':str(pay(finish((a,)),0))} for a in range(6)],'all_43_actions':[{'history':named(g),'action':LABELS[a]} for g,a in strategy.items()],'IC_count':len(ic),'IC_strict_count':sum(F(r['gap'])>0 for r in ic),'IC_tie_count':sum(F(r['gap'])==0 for r in ic),'row_variants':3*len(strategy),'future_subset_checks_all_three_variants':3*sum(6**i*2**(2-i) for i in range(3)),'all_ordered_triple_coverage':[{'triple':named(z),'coverage':cov(z)} for z in product(range(6),repeat=3)],'max_coverage_with_D':max(cov(z) for z in product(range(6),repeat=3) if D in z),'max_coverage_with_E':max(cov(z) for z in product(range(6),repeat=3) if E in z),'flows':flows,'all_gross_coupons_including_separate_source_payment':coupons}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ('second_actions','last_actions','root_alternative_leaves','IC_count','IC_strict_count','IC_tie_count','row_variants','future_subset_checks_all_three_variants','flows')},indent=2))
