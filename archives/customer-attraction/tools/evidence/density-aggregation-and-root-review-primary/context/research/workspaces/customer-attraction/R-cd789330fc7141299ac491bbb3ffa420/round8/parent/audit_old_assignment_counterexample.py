"""Independent unit-customer replay of a previously existing FOMA refutation.
No solver/author code imported. This is status correction, not a new game.
"""
from pathlib import Path
from itertools import product,permutations
from fractions import Fraction as F
from collections import Counter
import json,hashlib
P=Path(__file__).resolve().parent
S=P.parents[2]/'R-a0bb57fa24044a8794bc7991918a19c6/static_matching/static_matching_counterexample.json'
p=json.loads(S.read_text());I=p['instance'];m=I['players'];k=len(I['topics']);scale=12
clients=[set(x['topics']) for x in I['customers'] for _ in range(x['multiplicity'])]
sigma={tuple(x['history']):x['action'] for x in p['certificate']['actions']}
def end(h):
 while len(h)<m:h+=(sigma[h],)
 return h
def pays(z,i):return sum(scale//sum(a in X for a in z) for X in clients if z[i] in X)
def cover(z):return sum(any(a in X for a in z) for X in clients)
n=c=0
for i in range(m):
 for h in product(range(k),repeat=i):
  n+=1;z=end(h)
  for a in range(k):assert pays(z,i)>=pays(end(h+(a,)),i);c+=1
Z=end(());W=cover(Z);OPT=max(map(cover,product(range(k),repeat=m)))
optimal=[z for z in product(range(k),repeat=m) if cover(z)==OPT]
supports={tuple(sorted(set(z))) for z in optimal};assert supports=={(0,1,4,5)}
values=[]
for T in permutations((0,1,4,5)):
 total=sum(pays(Z[:i]+(T[i],)+Z[i+1:],i) for i in range(m));values.append(F(total,scale))
assert (len(clients),m,Z,W,OPT,min(values))==(52,4,(3,3,2,2),47,52,F(48))
out={'scope':'Existing FOMA-EXISTS counterexample independently replayed; not a new result or HALF counterexample.',
 'source_sha256':hashlib.sha256(S.read_bytes()).hexdigest(),'clients':len(clients),'ordered_nodes':n,
 'IC_including_self':c,'ordered_terminal_profiles':k**m,'actual':Z,'payoffs':[str(F(pays(Z,i),scale)) for i in range(m)],
 'W':W,'OPT':OPT,'optimal_supports':list(supports),'static_cost_histogram':{str(v):n for v,n in Counter(values).items()},'status':'passed'}
with (P/'old_assignment_counterexample_replay.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
print(json.dumps(out))
