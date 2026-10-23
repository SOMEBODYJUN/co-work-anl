#!/usr/bin/env python3
"""Exact audit of scalar one-step closure obstruction; this is NOT an SPE."""
from fractions import Fraction as F
from itertools import combinations_with_replacement
from pathlib import Path
import json
weights={2:9,3:1,4:7,5:3,8:7,9:3};k=4;r=3
responses={0:(2,2),1:(1,2),2:(2,3),3:(2,3)}
def load(z,t):return sum(t>>a&1 for a in z)
def payoff(a,z):return sum((F(w,load(z,t)) for t,w in weights.items() if t>>a&1),F())
def profit(z,b):return sum((F(w*load(z,t),load(b,t)+load(z,t)) for t,w in weights.items() if load(z,t)),F())
def cover(z):return sum(w for t,w in weights.items() if load(z,t))
def new(z,b):return sum(w for t,w in weights.items() if load(z,t) and not load(b,t))
def ss(v):
 if isinstance(v,F):return str(v)
 if isinstance(v,dict):return {str(k):ss(x) for k,x in v.items()}
 if isinstance(v,(list,tuple)):return [ss(x) for x in v]
 return v
rows=[];actual=(0,)+responses[0];root=payoff(0,actual)
for a,q in responses.items():
 z=(a,)+q;P=profit(q,(a,));G=new(q,(a,));cases=[]
 for t in combinations_with_replacement(range(k),r-1):
  cases.append({'comparison':t,'R':profit(t,(a,)),'new':new(t,(a,))})
 fp=max(c['R'] for c in cases);mn=max(c['new'] for c in cases)
 assert payoff(a,z)<=root
 assert fp<=2*P
 assert mn<=G+P
 rows.append({'first':a,'tail':q,'first_payoff':payoff(a,z),'P':P,'G':G,'F2':fp,'M2':mn,'profit_half_slack':2*P-fp,'coverage_half_slack':G+P-mn,'all_comparisons':cases})
opt=max(cover(q) for q in combinations_with_replacement(range(k),r));W=cover(actual)
assert W==14 and opt==30 and 2*W<opt
# A specific true local deviation proves the synthetic response menu is not SPE.
follow=payoff(2,actual);dev=payoff(1,(0,2,1))
assert follow==F(9,2) and dev==F(19,2) and dev>follow
report={'status':'not an SPE; exact counterexample only to scalar one-step closure','weights':weights,'responses':responses,'root_payoff':root,'actual':actual,'W':W,'OPT':opt,'twice_W_minus_OPT':2*W-opt,'children':rows,'fatal_terminal_deviation':{'history':(0,2),'specified':2,'payoff':follow,'deviation':1,'deviation_payoff':dev}}
print(json.dumps(ss(report),indent=2))
if __name__=='__main__':
 p=Path(__file__).with_name('one_step_closure_exact.json');p.write_text(json.dumps(ss(report),indent=2)+'\n')
