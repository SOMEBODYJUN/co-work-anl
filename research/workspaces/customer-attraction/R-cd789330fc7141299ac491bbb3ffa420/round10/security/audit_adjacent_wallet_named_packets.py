"""Definition-level exact diagnostic of root's adjacent-wallet candidate.
Only the named old52 and old1953 packets. No solver/model imports or search.
All original complete ordered histories are checked before computing frozen
queries. Source files are read-only; output is local to this round directory.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import hashlib,json
ROOT=Path(__file__).resolve().parents[6]
OUT=Path(__file__).resolve().parent

def load(name):
 if name=='old52':
  rel='research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/static_matching/static_matching_counterexample.json'
  paths=[ROOT/rel];d=json.loads(paths[0].read_text());I=d['instance'];policy={tuple(r['history']):r['action']for r in d['certificate']['actions']}
 else:
  base=ROOT/'research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/dynamic_exchange'
  paths=[base/'assignment_instance.json',base/'assignment_full_policy.json'];I=json.loads(paths[0].read_text());d=json.loads(paths[1].read_text());policy={tuple(map(int,key.split(',')))if key else():a for key,a in d['policy'].items()}
 return I,policy,[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in paths]

def audit(name):
 I,policy,sources=load(name);m=I['players'];k=len(I['topics']);topics=range(k)
 units=[frozenset(row['topics'])for row in I['customers']for _ in range(row['multiplicity'])]
 histories={h for depth in range(m)for h in product(topics,repeat=depth)}
 assert set(policy)==histories and all(a in topics for a in policy.values())
 leaves={}
 def finish(h):
  if h not in leaves:
   z=h
   while len(z)<m:z=z+(policy[z],)
   leaves[h]=z
  return leaves[h]
 payoff_cache={}
 def pay(z,i):
  if z not in payoff_cache:
   counts=[sum(a in C for a in z)for C in units]
   payoff_cache[z]=tuple(sum((F(1,c)for C,c in zip(units,counts)if a in C),F())for a in z)
  return payoff_cache[z][i]
 mingap=None;checks=0
 for h in histories:
  i=len(h);own=pay(finish(h),i)
  for a in topics:
   gap=own-pay(finish(h+(a,)),i)
   assert gap>=0,(name,h,a,gap)
   mingap=gap if mingap is None else min(mingap,gap);checks+=1
 Z=finish(());c=[sum(a in C for a in Z)for C in units];W=sum(q>0 for q in c)
 def frozen(i,T):return sum((F(1,q-int(Z[i]in C)+1)for C,q in zip(units,c)if T in C),F())
 matrix=[[frozen(i,T)for T in topics]for i in range(m)]
 wallets=[sum((F(1,q*(q+1))for C,q in zip(units,c)if Z[j]in C and Z[j+1]not in C),F())for j in range(m-1)]
 M=[max(row)for row in matrix];max_tuple=tuple(next(a for a in topics if matrix[i][a]==M[i])for i in range(m))
 opt=-1;optimal=[];cashoutmin=None
 for T in product(topics,repeat=m):
  O=sum(any(a in C for a in T)for C in units)
  Q=sum((matrix[i][a]for i,a in enumerate(T)),F())
  S=Q+F(m-1,m)*W-O
  cashout=S+F(W,m)-sum(wallets)
  assert cashout>=0,(name,T,cashout)
  cashoutmin=cashout if cashoutmin is None else min(cashoutmin,cashout)
  if O>opt:opt=O;optimal=[(T,Q)]
  elif O==opt:optimal.append((T,Q))
 minQ=min(q for T,q in optimal);min_assign=next(T for T,q in optimal if q==minQ)
 return {'name':name,'sources':sources,'unit_customers':len(units),'m':m,'topics':k,'ordered_decision_histories':len(histories),'comparisons_including_self':checks,'nonself_comparisons':checks-len(histories),'minimum_SPE_gap':str(mingap),'actual':Z,'actual_payoffs':[str(pay(Z,i))for i in range(m)],'W':W,'OPT':opt,'frozen_matrix':[[str(x)for x in row]for row in matrix],'row_maxima':[str(x)for x in M],'row_maximizing_tuple':max_tuple,'adjacent_wallets':[str(x)for x in wallets],'wallet_sum':str(sum(wallets)),'strong_left_sum_max_minus_W':str(sum(M)-W),'strong_gap_left_minus_wallets':str(sum(M)-W-sum(wallets)),'optimal_ordered_comparison_tuples':len(optimal),'minimum_optimal_Q':str(minQ),'minimum_optimal_assignment':min_assign,'weak_gap_min_Q_minus_W_minus_wallets':str(minQ-W-sum(wallets)),'minimum_static_cashout_margin_over_all_comparisons':str(cashoutmin)}

if __name__=='__main__':
 report={'scope':'Two named pre-existing complete SPE packets, exact diagnostics of one general adjacent-wallet candidate; no general inference from non-refutation.','packets':[audit(n)for n in ('old52','old1953')]}
 (OUT/'adjacent_wallet_named_packets.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps([{'name':r['name'],'W':r['W'],'wallet_sum':r['wallet_sum'],'strong_gap':r['strong_gap_left_minus_wallets'],'weak_gap':r['weak_gap_min_Q_minus_W_minus_wallets'],'complete_SPE_checks':r['comparisons_including_self']}for r in report['packets']],indent=2))
