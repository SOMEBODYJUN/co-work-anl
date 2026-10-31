"""Randomly realize the fixed/optimal theme marginals of an LP obstruction.
Only the actual game is solved; absent reply labels never treated as available.
Integer rounding creates a fresh finite unit-customer instance, not a relaxation certificate.
"""
import sys,json,time,random,argparse
from pathlib import Path
from itertools import combinations_with_replacement,combinations
from functools import lru_cache
import numpy as np
R=Path(__file__).resolve().parents[5];sys.path.insert(0,str(R))
from customer_attraction import Instance,CustomerType,ExactSPESolver
D=Path(__file__).parent

def run(seed,scale):
 rng=random.Random(seed);raw=json.loads((R/'evidence/certificates/customer_attraction/five_player_indexed_bound.json').read_text())['primal'];den=int(raw['denominator']);types={}
 for atom in raw['atoms']:
  mask=sum((int(v)<<a) for a,v in enumerate(atom['bits']));j=sum(atom['AB_hist'][4:]);subset=rng.sample(range(10,15),j)
  mask+=sum(1<<a for a in subset);weight=(int(atom['mass_numerator'])*scale+den//2)//den
  if mask and weight:types[mask]=types.get(mask,0)+weight
 p,m=15,5;B=np.array([[(mask>>a)&1 for a in range(p)] for mask in types],dtype=np.int64);weights=np.array(list(types.values()),dtype=np.int64)
 qs=tuple(tuple(h.count(a) for a in range(p)) for h in combinations_with_replacement(range(p),m));qidx={q:i for i,q in enumerate(qs)}
 Q=np.array(qs,dtype=np.int64);denoms=Q@B.T
 # Every positive denominator divides60 (m=5).
 fractions=np.zeros_like(denoms);nz=denoms>0;fractions[nz]=60//denoms[nz]
 pay=(fractions*weights)@B;welfare=(denoms>0)@weights
 bydepth=[tuple(tuple(h.count(a) for a in range(p)) for h in combinations_with_replacement(range(p),d)) for d in range(m)]
 outcomes={q:frozenset([i]) for i,q in enumerate(qs)};threshold={}
 def inc(k,a):return k[:a]+(k[a]+1,)+k[a+1:]
 t=time.time()
 for d in range(m-1,-1,-1):
  for k in bydepth[d]:
   children=[outcomes[inc(k,a)] for a in range(p)]
   floor=max(min(int(pay[q,a]) for q in child) for a,child in enumerate(children));threshold[k]=floor
   outcomes[k]=frozenset(q for a,child in enumerate(children) for q in child if pay[q,a]>=floor)
  print(json.dumps({'seed':seed,'depth':d,'seconds':time.time()-t,'max_outcomes':max(len(outcomes[k]) for k in bydepth[d])}),flush=True)
 root=(0,)*p;worst=min(outcomes[root],key=lambda q:welfare[q]);actual=(1,1,1,1,1)+(0,)*10;wid=int(welfare[worst]);actualw=int(welfare[qidx[actual]])
 opt=0
 masks=np.array(list(types),dtype=np.int64)
 for port in combinations(range(p),m):
  cover=sum(1<<a for a in port);val=sum(w for mask,w in types.items() if cover&mask);opt=max(opt,val)
 result={'seed':seed,'scale':scale,'types':[[mask,w] for mask,w in types.items()],'root_worst_counts':qs[worst],'welfare':wid,'optimum':opt,'ratio':opt/wid,'actual_ABCDE_welfare':actualw,'actual_ABCDE_is_SPE_outcome':qidx[actual] in outcomes[root],'root_outcomes':len(outcomes[root]),'root_threshold_scaled60':threshold[root],'seconds':time.time()-t}
 (D/f'materialized_seed{seed}_scale{scale}.json').write_text(json.dumps(result));print(json.dumps({k:v for k,v in result.items() if k!='types'}),flush=True)
 return result
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--seed',type=int,default=37381021);ap.add_argument('--scale',type=int,default=1000000);a=ap.parse_args();run(a.seed,a.scale)
