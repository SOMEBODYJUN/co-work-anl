import random,itertools,json,time
from fractions import Fraction
from customer_attraction import CustomerType,Instance,ExactSPESolver

def opt_tuples(ins):
 k,m=ins.topic_count,ins.players;best=ins.optimal_welfare(); arr=[]
 for t in itertools.product(range(k),repeat=m):
  if ins.welfare(ins.counts(t,terminal=True))==best:arr.append(t)
 return best,arr

def branch_hist(cert, actual, i, action):
 hist=actual[:i]+(action,)
 while len(hist)<len(actual): hist+=(cert.actions[hist],)
 return hist

def tax(ins,cert,actual,ot):
 m=ins.players;k=ins.topic_count
 actual_counts=ins.counts(actual,terminal=True)
 covered=set()
 for c in ins.customers:
  if any(actual_counts[t] for t in c.topics):
   covered.add(c)
 # expand customer ids via types impossible hash multiplicity; use topics and replicate conceptual units
 # use each type repeated; only U if no actual topic in topics
 U=[]
 for c in ins.customers:
  if (not any(actual_counts[t] for t in c.topics)) and any(t in c.topics for t in ot): U.extend([c.topics]*c.multiplicity)
 vals=[]
 for I in U:
  owners=[i for i,t in enumerate(ot) if t in I]
  if not owners:
   print('BAD',k,m,ot,I,cs,actual,actual_counts);raise ValueError('owner none')
  kv=[]
  for i in owners:
   hist=branch_hist(cert,actual,i,ot[i])
   kx=sum(1 for j in range(i+1,m) if hist[j] in I)
   kv.append(Fraction(kx,1+kx))
  vals.append(min(kv))
 R=sum(vals,Fraction(0))
 # I,G sets cardinalities (unit customers): actual customers in O? compute conceptual ids by type
 O=[]; C=[]
 for c in ins.customers:
  O.extend([c.topics]*c.multiplicity) # wrong topics not customer identity; determine if any opt t in type
  # actual covered if any actual theme in c.topics
 # each customer represented just type but overlap counts
 Icnt=Gcnt=0
 for c in ins.customers:
  o=any(t in c.topics for t in ot); a=any(actual_counts[t] for t in c.topics)
  if o and a:Icnt+=c.multiplicity
  if (not o) and a:Gcnt+=c.multiplicity
 return R,Icnt,Gcnt,vals

rng=random.Random(7);best=None;start=time.time();count=0
for k in range(2,8):
 for m in range(2,9):
  if k**m>500000:continue
  for it in range(5000):
   cs=[]
   for mask in range(1,1<<k):
    if rng.random()<.08:cs.append(CustomerType(frozenset(i for i in range(k) if mask>>i&1),rng.randint(1,5)))
   if not cs:continue
   ins=Instance(tuple(map(str,range(k))),tuple(cs),m);so=ExactSPESolver(ins);opt,ots=opt_tuples(ins);w=so.minimum_welfare()
   # only inspect worst outcomes and up to 20 optimal tuples
   for target in so.worst_outcomes():
    cert=so.certificate(target); actual=next(iter(so.ordered_outcomes(target)))
    for ot in ots[:min(20,len(ots))]:
      R,I,G,vals=tax(ins,cert,actual,ot); gap=R-(I+2*G)
      if best is None or gap>best[0]:
       best=(gap,R,I,G,k,m,it,opt,w,actual,target,ot,vals,[(sorted(c.topics),c.multiplicity) for c in cs]);print('best',best[:13],flush=True)
      if gap>0:
       print('VIOLATION',best);json.dump({'gap':str(gap),'R':str(R),'I':I,'G':G,'k':k,'m':m,'opt':opt,'w':w,'actual':actual,'target':target,'optimal_tuple':ot,'vals':[str(v) for v in vals],'customers':best[-1]},open('owner_tax_violation.json','w'));raise SystemExit
   count+=1
print('done',count,'best',best)
