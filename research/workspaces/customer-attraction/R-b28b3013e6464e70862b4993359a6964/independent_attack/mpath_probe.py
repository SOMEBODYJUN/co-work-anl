from customer_attraction import Instance, ExactSPESolver
from fractions import Fraction
from itertools import product
from scipy.optimize import linprog
import random,time,json

def path_from_cert(cert,m):
 h=(); p=[]
 for i in range(m):
  a=cert.actions[h]; p.append(a); h=h+(a,)
 return tuple(p)
def terminal_from(cert,h,m):
 # Follow policy from arbitrary history h to terminal
 while len(h)<m:
  h=h+(cert.actions[h],)
 return h
def matrix(inst,cert,path,i):
 # rows topic T, cols forced A; K=sum clients on T 1/(1+c_x)
 p=inst.topic_count; m=inst.players
 cols=[]
 h=path[:i]
 for a in range(p):
  z=terminal_from(cert,h+(a,),m)
  counts=inst.counts(z,terminal=True)
  row=[]
  for T in range(p):
   val=Fraction(0)
   for cu in inst.customers:
    if T in cu.topics:
      # all customers x in T, denominator 1 + final covered count
      val += Fraction(cu.multiplicity,1+sum(counts[j] for j in cu.topics))
   row.append(val)
  cols.append(row)
 # rows x columns
 return [[cols[a][T] for a in range(p)] for T in range(p)]
def mval(mat):
 p=len(mat)
 # min t s.t. mat q <= t, sum q=1
 c=[0]*p+[1]
 Aub=[]; bub=[]
 for row in mat:
  Aub.append(row+[ -1]); bub.append(0)
 Aeq=[[1]*p+[0]]; beq=[1]
 res=linprog(c,A_ub=Aub,b_ub=bub,A_eq=Aeq,b_eq=beq,bounds=[(0,None)]*p+[(None,None)],method='highs')
 if not res.success: raise RuntimeError(res.message)
 return Fraction(float(res.fun)).limit_denominator(10**8),res.x

def run(inst):
 s=ExactSPESolver(inst); c=s.worst_certificate(); path=path_from_cert(c,inst.players); u=inst.player_payoffs(path)
 bad=[]
 for i in range(inst.players):
  mat=matrix(inst,c,path,i); mv,q=mval(mat)
  if mv>u[i]: bad.append((i,mv,u[i],mat,q))
 return {'bad':bad,'path':path,'u':u,'O':inst.optimal_welfare(),'W':inst.welfare(inst.counts(path))}
random.seed(20261024); start=time.time(); n=0
for it in range(1000):
 p=random.randint(2,4); m=random.randint(2,5); ncu=random.randint(p,min(12,p*4+3)); cov=[set() for _ in range(p)]
 for x in range(ncu):
  mask=random.randrange(1,1<<p)
  for j in range(p):
   if mask>>j&1: cov[j].add(x)
 inst=Instance.from_topic_sets(cov,m)
 try:r=run(inst)
 except Exception: continue
 n+=1
 if r['bad']:
  i,mv,ui,mat,q=r['bad'][0]
  print(json.dumps({'it':it,'i':i,'mv':str(mv),'u':str(ui),'O':r['O'],'W':r['W'],'path':r['path'],'inst':inst.to_dict(),'mat':[[str(x) for x in row] for row in mat],'q':q.tolist()},indent=2),flush=True);break
 if n%100==0: print('checked',n,'sec',time.time()-start,flush=True)
else: print('none',n)
