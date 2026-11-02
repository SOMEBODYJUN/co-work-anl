from itertools import product
from fractions import Fraction
from customer_attraction import Instance, ExactSPESolver
import random,time,json
random.seed(20261024)
def cov(inst, support):
 c=inst.welfare(tuple(int(j in support) for j in range(inst.topic_count)))
 return c
def Ls(inst,s, hist):
 vals=[]
 for i in range(inst.players):
  cnt=inst.counts(hist[:i])
  row=[]
  for a in range(inst.topic_count):
   child=tuple(cnt[j]+(j==a) for j in range(inst.topic_count))
   row.append(min(inst.topic_payoff(a,t) for t in s._solve(child)))
  vals.append(row)
 return vals
def all_opt_tuples(inst):
 O=inst.optimal_welfare(); out=[]
 # only support set <=m, enumerate sets and one canonical tuple (but order may matter under L)
 for supmask in range(1<<inst.topic_count):
   sup=[j for j in range(inst.topic_count) if supmask>>j&1]
   if len(sup)<=inst.players and cov(inst,sup)==O:
      # all tuples whose support exactly subset sup? include repetitions. all permutations of sup padded by first
      # exhaustive product and dedupe supports only
      for tup in product(range(inst.topic_count), repeat=inst.players):
         if set(tup)==set(sup): out.append(tup)
      
 return list(dict.fromkeys(out))
def run(inst):
 s=ExactSPESolver(inst); O=inst.optimal_welfare(); bad=[]; npaths=0
 for z in s.outcomes():
  W=inst.welfare(z)
  for h in s.ordered_outcomes(z):
   npaths+=1
   ls=Ls(inst,s,h)
   for T in all_opt_tuples(inst):
      sm=sum(ls[i][T[i]] for i in range(inst.players))
      if sm < O-W:
        return {'bad':True,'O':O,'W':W,'gap':O-W,'sumL':sm,'z':z,'h':h,'T':T,'ls':ls,'inst':inst.to_dict()}
 return {'bad':False,'O':O,'paths':npaths,'outcomes':len(s.outcomes())}
start=time.time(); checks=0
for it in range(1000):
 p=random.randint(2,4); m=random.randint(2,5); n=random.randint(p,min(12, p*4))
 cover=[set() for _ in range(p)]
 for x in range(n):
  mask=random.randrange(1,1<<p)
  for j in range(p):
   if mask>>j&1: cover[j].add(x)
 inst=Instance.from_topic_sets(cover,m)
 try:r=run(inst)
 except Exception as e: continue
 checks+=1
 if r['bad']:
  print(json.dumps(r,default=str,indent=2));break
 if checks%100==0: print('checked',checks,'sec',time.time()-start,flush=True)
else: print('none',checks)
