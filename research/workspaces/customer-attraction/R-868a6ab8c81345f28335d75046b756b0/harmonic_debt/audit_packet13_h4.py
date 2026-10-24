"""Independent exact H4/local debt audit of the existing thirteen-player DAG.
No expected/desired data, project verifier, or optimization solver is used.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from collections import deque
import gzip,json
BASE=Path(__file__).resolve().parents[5]
P=BASE/'research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/security/refined_tax_k10_packet.json.gz'
x=json.load(gzip.open(P,'rt')); ins=x['instance']; nodes=x['nodes'];m=ins['players'];K=len(ins['topics']);labels=ins['topics']
unit=[frozenset(r['topics']) for r in ins['customers'] for _ in range(r['multiplicity'])]
assert len(unit)==36
seen={x['root']};queue=deque(seen)
while queue:
 v=queue.popleft(); n=nodes[v];c=n['counts']; depth=sum(c)
 assert len(c)==K and all(isinstance(z,int) and z>=0 for z in c)
 if depth==m:
  assert 'action' not in n and 'children' not in n
  continue
 assert depth<m and len(n['children'])==K and 0<=n['action']<K
 for a,w in enumerate(n['children']):
  d=list(c);d[a]+=1;assert nodes[w]['counts']==d
  if w not in seen:seen.add(w);queue.append(w)
assert len(seen)==len(nodes) and nodes[x['root']]['counts']==[0]*K
@lru_cache(None)
def terminal(v):
 n=nodes[v]
 return tuple(n['counts']) if sum(n['counts'])==m else terminal(n['children'][n['action']])
@lru_cache(None)
def utility(counts,a):
 return sum((F(1,sum(counts[b] for b in customer)) for customer in unit if a in customer),F())
comparisons=0;slacks=[]
for v in seen:
 n=nodes[v]
 if sum(n['counts'])==m:continue
 chosen=utility(terminal(v),n['action'])
 for a,w in enumerate(n['children']):
  slack=chosen-utility(terminal(w),a);assert slack>=0;slacks.append(slack);comparisons+=1
q=terminal(x['root']);loads=[sum(q[a] for a in customer) for customer in unit]
W=sum(c>0 for c in loads);G=sum((F(1,c+1) for c in loads if c),F())
e=[sum((F(1,c+1) for customer,c in zip(unit,loads) if a in customer),F()) for a in range(K)]
actual=[];v=x['root']
while sum(nodes[v]['counts'])<m:
 actual.append(v);n=nodes[v];v=n['children'][n['action']]
d=[[utility(terminal(nodes[v]['children'][a]),a) for a in range(K)] for v in actual]
g=[sum((F(1,c*(c+1)) for customer,c in zip(unit,loads) if nodes[v]['action'] in customer),F()) for v in actual]
assert sum(g)==G
rows=[]
for i,v in enumerate(actual):
 a=nodes[v]['action'];u=utility(q,a)
 for T in range(K):
  if e[T]-d[i][T]>g[i]:
   rows.append({'position':i+1,'actual':labels[a],'query':labels[T],'e':str(e[T]),'d':str(d[i][T]),'g':str(g[i]),'violation':str(e[T]-d[i][T]-g[i])})
# H4 existence: DP over union of topic labels used in comparator.
# Since A,B,T,P have unique customers, OPT=36 iff these four occur.
required=(1<<0)|(1<<1)|(1<<2)|(1<<5)
dp={0:(F(),())}
for i in range(m):
 nxt={}
 for mask,(cost,path) in dp.items():
  for a in range(K):
   k=mask|(1<<a);val=cost+e[a]-d[i][a]
   if k not in nxt or val<nxt[k][0]:nxt[k]=(val,path+(a,))
 dp=nxt
best=min(val for mask,val in dp.items() if mask&required==required)
# Fixed optimal tuple with 10 T plus one A,B,P: exact assignment DP over quotas.
quota=(1,1,10,0,0,1)
qd={(0,)*K:(F(),())}
for i in range(m):
 nq={}
 for used,(cost,path) in qd.items():
  for a in range(K):
   if used[a]>=quota[a]:continue
   c=list(used);c[a]+=1;c=tuple(c);val=cost+e[a]-d[i][a]
   if c not in nq or val<nq[c][0]:nq[c]=(val,path+(a,))
 qd=nq
fixed=qd[quota]
report={'source':str(P.relative_to(BASE)),'all_nodes':len(nodes),'all_comparisons_including_self':comparisons,'min_IC_slack':str(min(slacks)),'q':q,'W':W,'G':str(G),'e':{labels[a]:str(e[a]) for a in range(K)},'local_violations':rows,'same_T_debt':str(sum(e[2]-d[i][2] for i in range(m))),'same_T_debt_minus_G':str(sum(e[2]-d[i][2] for i in range(m))-G),'best_optimal_H4_debt':str(best[0]),'best_optimal_H4_debt_minus_G':str(best[0]-G),'best_optimal_assignment':[labels[a] for a in best[1]],'ten_T_optimal_best_debt':str(fixed[0]),'ten_T_optimal_best_debt_minus_G':str(fixed[0]-G),'ten_T_optimal_best_assignment':[labels[a] for a in fixed[1]],'d_matrix':[{labels[a]:str(d[i][a]) for a in range(K)} for i in range(m)]}
print(json.dumps(report,indent=2))
(Path(__file__).parent/'packet13_h4_exact.json').write_text(json.dumps(report,indent=2)+'\n')
