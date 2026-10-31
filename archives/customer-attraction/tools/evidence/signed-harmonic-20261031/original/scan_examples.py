"""Exact finite diagnostics for signed harmonic and linear extension budgets."""
import json, sys
from pathlib import Path
from itertools import combinations_with_replacement
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction.model import Instance
from customer_attraction.exact import ExactSPESolver

def analyze(inst):
 p,m=inst.topic_count,inst.players
 tuples=[]
 for h in combinations_with_replacement(range(p),m):
  q=tuple(h.count(i) for i in range(p));tuples.append((q,inst.welfare(q)))
 opt=max(v for _,v in tuples); opts=[q for q,v in tuples if v==opt]
 H=[Fraction(0)]
 for i in range(1,2*m+1):H.append(H[-1]+Fraction(1,i))
 outcomes=ExactSPESolver(inst).outcomes()
 worst_h=None; worst_l=None; worst_exist_h=None; worst_exist_l=None
 for a in outcomes:
  vals=[]
  for d in opts:
   F=L=Fraction(0);E=0
   for x in inst.customers:
    c=sum(a[t] for t in x.topics);k=sum(d[t] for t in x.topics);r=x.multiplicity
    F+=r*(H[c+k]-H[c]);L+=Fraction(r*k,c+1)
    E+=r*int(c>0 and k==0)
   budget=inst.welfare(a)+E
   vals.append((budget-F,budget-L,d))
  vh=min(vals,key=lambda t:t[0]);vl=min(vals,key=lambda t:t[1])
  eh=max(vals,key=lambda t:t[0]);el=max(vals,key=lambda t:t[1])
  wh=(vh[0],a,vh[2]);wl=(vl[1],a,vl[2]);we_h=(eh[0],a,eh[2]);we_l=(el[1],a,el[2])
  if worst_h is None or wh[0]<worst_h[0]:worst_h=wh
  if worst_l is None or wl[0]<worst_l[0]:worst_l=wl
  if worst_exist_h is None or we_h[0]<worst_exist_h[0]:worst_exist_h=we_h
  if worst_exist_l is None or we_l[0]<worst_exist_l[0]:worst_exist_l=we_l
 return dict(players=m,topics=p,customers=inst.customer_count,opt=opt,outcomes=len(outcomes),optimal_tuples=len(opts),harmonic=worst_h,linear=worst_l,exist_harmonic=worst_exist_h,exist_linear=worst_exist_l)

def main():
 out={}
 for f in sorted((ROOT/'examples/customer_attraction').glob('*.json')):
  inst=Instance.from_dict(json.loads(f.read_text()))
  out[f.name]=analyze(inst);print(f.name,json.dumps(out[f.name],default=str),flush=True)
 (Path(__file__).parent/'example_scan.json').write_text(json.dumps(out,default=str,indent=2)+'\n')
if __name__=='__main__':main()
