from fractions import Fraction
from itertools import product
from math import sqrt
import json,sys
sys.path.insert(0,'archives/customer-attraction/tools/evidence/R18-dynamic-two-agent')
from customer_attraction import Instance, CustomerType, ExactSPESolver

def comps(n,k):
 if k==1: yield (n,); return
 for a in range(n+1):
  for tail in comps(n-a,k-1): yield (a,)+tail
I=Instance.from_dict({"topics":["0","1","2"],"customers":[{"topics":[0],"multiplicity":6},{"topics":[1],"multiplicity":4},{"topics":[0,1],"multiplicity":3},{"topics":[0,2],"multiplicity":5},{"topics":[1,2],"multiplicity":7},{"topics":[0,1,2],"multiplicity":1}],"players":5})
S=ExactSPESolver(I); S.outcomes()
def F(b):
 r=I.players-sum(b);best=Fraction(0);args=[]
 for d in comps(r,I.topic_count):
  val=Fraction(0)
  for C in I.customers:
   B=sum(b[a] for a in C.topics);D=sum(d[a] for a in C.topics)
   if D: val += C.multiplicity*Fraction(D,B+D)
  if val>best:best=val;args=[d]
  elif val==best:args.append(d)
 return best,args
b=(2,1,0); child=(2,2,0); a=1; z=(2,3,0)
fb,ab=F(b);fc,ac=F(child);gap=fb-fc
u=S._utility(z,a); floor=S.threshold(b)
charge_terms=[]
for C in I.customers:
 if a in C.topics:
  B=sum(b[j] for j in C.topics); Z=sum(z[j] for j in C.topics)
  term=2*C.multiplicity*(sqrt(B+1)-sqrt(B))/sqrt(Z)
  charge_terms.append({'topics':sorted(C.topics),'multiplicity':C.multiplicity,'B':B,'Z':Z,'term':term})
charge=sum(x['term'] for x in charge_terms)
out={"instance":I.to_dict(),"prefix":b,"action":a,"child":child,"candidate_terminal":z,"F_prefix":str(fb),"F_prefix_argmax":ab,"F_child":str(fc),"F_child_argmax":ac,"gap":str(gap),"threshold":str(floor),"utility":str(u),"candidate_in_child":z in S.outcomes(child),"candidate_utility_ge_threshold":u>=floor,"charge_terms":charge_terms,"charge":charge,"deficit":float(gap)-charge,"solver_stats":S.stats.__dict__}
print(json.dumps(out,ensure_ascii=False,indent=2,default=str))
