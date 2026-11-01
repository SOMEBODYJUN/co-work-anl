"""Fraction audit of Markov harmonic-potential bridge counterexample.
No solver imports; directly expands each type into unit clients and all ordered histories.
"""
from pathlib import Path
from fractions import Fraction
from itertools import product,combinations_with_replacement
from collections import Counter
import json,sys
ROOT=Path(__file__).parent
source=sys.argv[1]if len(sys.argv)>1 else 'truncated_potential_candidate.json';obj=json.loads((ROOT/source).read_text());q=obj['q'];r=obj['r'];policy={tuple(c):a for c,a in obj['policy']};weights={int(mask):Fraction(v).limit_denominator(100000) for mask,v in obj['weights'].items()}
from math import lcm
scale=lcm(*(v.denominator for v in weights.values()));weights={mask:int(v*scale)for mask,v in weights.items()}
clients=[tuple(a for a in range(q)if mask>>a&1)for mask,w in weights.items()for _ in range(w)]
def state(h):
 c=Counter(h);return tuple(c[a]for a in range(q))
def finish(h):
 while len(h)<r:h=h+(policy[state(h)],)
 return h
def utility(h,i):
 return sum((Fraction(1,sum(a in B for a in h))for B in clients if h[i]in B),Fraction(0))
def cover(h):return sum(any(a in B for a in h)for B in clients)
slacks=[]
for d in range(r):
 for h in product(range(q),repeat=d):
  actual=finish(h);on=utility(actual,d)
  for a in range(q):
   alt=finish(h+(a,));slack=on-utility(alt,d);assert slack>=0,(h,a,slack);slacks.append(slack)
actual=finish(());load=[sum(a in B for a in actual)for B in clients];phi=sum((sum((Fraction(1,j)for j in range(1,c+1)),Fraction(0))for c in load),Fraction(0));trunc=sum((min(Fraction(2),sum((Fraction(1,j)for j in range(1,c+1)),Fraction(0)))for c in load),Fraction(0));optimal=max((cover(h),h)for h in combinations_with_replacement(range(q),r))
result={'weights':weights,'clients':len(clients),'actual':actual,'payoffs':[str(utility(actual,i))for i in range(r)],'W':cover(actual),'OPT':optimal[0],'optimizer':optimal[1],'Phi':str(phi),'truncated_Phi':str(trunc),'difference':str(phi-optimal[0]),'history_count':sum(q**d for d in range(r)),'comparisons':len(slacks),'strict_comparisons':sum(s>0 for s in slacks),'minimum_slack':str(min(slacks)),'load_histogram':dict(Counter(load)),'two_layer_occupancy':sum(min(c,2)for c in load)}
print(json.dumps(result,indent=2));(ROOT/('two_layer_occupancy_audit.json'if source.startswith('two_layer')else 'harmonic_minimized_audit.json'if 'minimized'in source else 'truncated_potential_audit.json')).write_text(json.dumps(result,indent=2)+'\n')
