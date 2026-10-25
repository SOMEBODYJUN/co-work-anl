"""Definition-exact finite BI for a designed >2 security-relaxation point.
All utilities are 60 times original utilities, evaluated with integers. The
point has 137 covered banking clients and 150 opt-private omitted clients;
outside-opt pair insurers are K5 edges. A relaxation point is not called SPE.
"""
from itertools import combinations
from pathlib import Path
from fractions import Fraction as F
import json,time,numpy as np,argparse
P=20;M=5;PATH=(0,1,2,3,4)
def counts(p,total):
 if p==1:yield(total,);return
 for j in range(total+1):
  for t in counts(p-1,total-j):yield(j,)+t
def inc(q,a):return q[:a]+(q[a]+1,)+q[a+1:]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--partial',action='store_true');args=ap.parse_args()
 start=time.time();source=(json.loads(Path(__file__).with_name('partial_insured_bank_lp.json').read_text()) if args.partial else json.loads(Path(__file__).with_name('insurance_security_lp.json').read_text())[1])
 scale=1 if args.partial else 137
 types=[tuple(t) for t,v in source['point']];weights=np.array([int(F(v)*scale) for t,v in source['point']],dtype=np.int64)
 I=np.array([[a in typ for a in range(P)] for typ in types],dtype=np.int64)
 Q=tuple(counts(P,M));Qi={q:i for i,q in enumerate(Q)};den=np.array(Q,dtype=np.int64)@I.T
 price=np.zeros(6,dtype=np.int64);price[1:]=[60//d for d in range(1,6)]
 U=(price[den]*weights)@I;U*=np.array(Q)>0;W=(den>0)@weights
 states=tuple(q for d in range(M,-1,-1) for q in counts(P,d));R={};floor={}
 for q in states:
  if sum(q)==M:R[q]=np.array([Qi[q]],int);continue
  ch=[R[inc(q,a)] for a in range(P)];f=max(U[c,a].min() for a,c in enumerate(ch));floor[q]=int(f)
  R[q]=np.unique(np.concatenate([c[U[c,a]>=f] for a,c in enumerate(ch)]))
 tq=tuple(PATH.count(a) for a in range(P));t=Qi[tq];root=(0,)*P;prefix=[]
 for i,a in enumerate(PATH):
  q=tuple(PATH[:i].count(b) for b in range(P));child=inc(q,a)
  entries=[]
  for b in range(P):
   menu=R[inc(q,b)];v=U[menu,b];mn=int(v.min());z=int(menu[np.argmin(v)])
   entries.append({'action':b,'min_forced_payoff':str(F(mn,60)),'one_min_leaf':Q[z]})
  best=max(entries,key=lambda x:F(x['min_forced_payoff']))
  prefix.append({'position':i+1,'actual_action':a,'actual_payoff':str(F(int(U[t,a]),60)),'threshold':str(F(floor[q],60)),'target_in_child':bool(t in R[child]),'target_current_passes':bool(U[t,a]>=floor[q]),'maximizing_forced':best})
 report={'scope':'complete pure SPE outcome sets, exact integer-scaled utilities, specified finite opt-private / outside-opt K5 insurance candidate','unit_clients':int(weights.sum()),'target_W':int(W[t]),'target_OPT':int(W.max()),'target_ratio':str(F(int(W.max()),int(W[t]))),'target_is_SPE_outcome':bool(t in R[root]),'minimum_SPE_welfare':int(W[R[root]].min()),'root_outcome_count':len(R[root]),'count_states':len(states),'terminal_counts':len(Q),'prefix_diagnosis':prefix,'elapsed':time.time()-start}
 (Path(__file__).with_name('diagnose_partial_insurance.json') if args.partial else Path(__file__).with_suffix('.json')).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
