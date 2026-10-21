"""Independent definition-level audit. No canonical solver/verifier imports.
Reads an explicit complete-history strategy represented by a count/target DAG.
All customers expanded to distinct unit clients, all arithmetic Fraction.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json,sys,hashlib

HERE=Path(__file__).resolve().parent
DEFAULT=HERE.parent/'direct_global/padded_residual_m6_dag.json'

def check(path):
 raw=Path(path).read_bytes();data=json.loads(raw)
 ins=data['instance'];names=ins['topics'];p=len(names);n=ins['players'];nodes=data['nodes'];root=data['root']
 assert isinstance(n,int) and n>=1 and p>=1 and len(set(names))==p
 clients=[]
 for row in ins['customers']:
  likes=frozenset(row['topics']);mult=row['multiplicity']
  assert likes and all(type(a)is int and 0<=a<p for a in likes)
  assert type(mult)is int and mult>0
  clients.extend([likes]*mult)
 def validcounts(c,total=None):
  assert len(c)==p and all(type(x)is int and x>=0 for x in c)
  assert sum(c)<=n
  if total is not None:assert sum(c)==total
 def payoff(a,c):
  assert c[a]>0
  out=F(0)
  for likes in clients:
   if a in likes:
    load=sum(c[j] for j in likes)
    assert load>0
    out+=F(1,load)
  return out
 assert type(root)is int and 0<=root<len(nodes)
 assert nodes[root]['counts']==[0]*p
 strict=ties=comparisons=0
 incoming=[0]*len(nodes);incoming[root]=1
 depthnodes={d:[] for d in range(n+1)}
 for idx,node in enumerate(nodes):
  c=node['counts'];t=node['target'];validcounts(c);validcounts(t,n)
  assert all(x<=y for x,y in zip(c,t))
  depthnodes[sum(c)].append(idx)
 for depth in range(n+1):
  for idx in depthnodes[depth]:
   node=nodes[idx];c=node['counts'];t=node['target']
   assert incoming[idx]>0,('unreachable',idx)
   if depth==n:
    assert c==t
    assert 'action' not in node and 'children' not in node
    continue
   a=node['action'];children=node['children']
   assert type(a)is int and 0<=a<p
   assert len(children)==p and all(type(j)is int and 0<=j<len(nodes) for j in children)
   assert nodes[children[a]]['target']==t
   own=payoff(a,t)
   for b,j in enumerate(children):
    child=nodes[j]
    expected=c.copy();expected[b]+=1
    assert child['counts']==expected,('wrong successor counts',idx,b,j)
    counter=payoff(b,child['target'])
    assert own>=counter,('profitable true deviation',idx,b,str(own),str(counter))
    comparisons+=1
    if own==counter:ties+=1
    else:strict+=1
    incoming[j]+=incoming[idx]
  assert sum(incoming[i] for i in depthnodes[depth])==p**depth
 # The action/child-target equalities plus terminal target=count prove by backward
 # induction that target is the strategy's actual continuation at every node.
 # The all-action comparisons therefore prove SPE at every unfolded history.
 idx=root;path=[]
 while sum(nodes[idx]['counts'])<n:
  a=nodes[idx]['action'];path.append(a);idx=nodes[idx]['children'][a]
 terminal=nodes[idx]['counts']
 assert terminal==nodes[root]['target']
 pay=[payoff(a,terminal) for a in path]
 covered=[any(terminal[a] for a in likes) for likes in clients]
 W=sum(covered);assert sum(pay)==W
 opt=0;optsupport=None
 for size in range(min(n,p)+1):
  for sup in combinations(range(p),size):
   coveredopt=sum(bool(set(sup)&likes) for likes in clients)
   if coveredopt>opt:opt=coveredopt;optsupport=sup
 query=names.index('T')
 Fquery=F(0)
 for i,a in enumerate(path):
  dev=terminal.copy();dev[a]-=1;dev[query]+=1
  Fquery+=payoff(query,dev)
 uncoveredquery=sum(query in likes and not cov for likes,cov in zip(clients,covered))
 # Refined fractional budget and a separate explicit oblivious dual.
 alpha=F(n-1,n);loads=[sum(terminal[a] for a in likes) for likes in clients]
 G=sum((1/(1+alpha*load) for load in loads if load),F(0))
 g=[sum((1/(1+alpha*load) for likes,load in zip(clients,loads) if a in likes),F(0)) for a in range(p)]
 # Four private P's + D are a valid 5-theme oblivious background; choose this
 # only as a feasible dual, without asserting minimax optimality.
 background=[names.index(x) for x in ['P0','P1','P2','P3','D']]
 bcounts=[background.count(a) for a in range(p)]
 staticquery=[]
 for a in range(p):
  c=bcounts.copy();c[a]+=1;staticquery.append(payoff(a,c))
 result={
  'scope':'Complete pure SPE via DAG induction, unit clients, all true deviations; auxiliary bridge failure only',
  'source_sha256':hashlib.sha256(raw).hexdigest(),'players':n,'topics':p,'unit_clients':len(clients),
  'dag_nodes':len(nodes),'decision_nodes':sum(len(depthnodes[d]) for d in range(n)),
  'dag_comparisons':comparisons,'strict':strict,'ties':ties,
  'unfolded_decision_histories':sum(p**d for d in range(n)),
  'unfolded_terminal_histories':p**n,
  'root_path':[names[a] for a in path],'root_counts':terminal,
  'payoffs':list(map(str,pay)),'W':W,'OPT':opt,'optimal_support':[names[a] for a in optsupport],
  'query':'T','wholly_uncovered_query_clients':uncoveredquery,'Fquery':str(Fquery),
  'minimum_payoff':str(min(pay)),'counterexample_gap':str(Fquery-W-min(pay)),
  'alpha':str(alpha),'G':str(G),'g_values':list(map(str,g)),
  'refined_fractional_budget_slack':str(W+G-n*max(g)),
  'oblivious_background':[names[a] for a in background],
  'oblivious_query_values':list(map(str,staticquery)),
  'oblivious_cap':str(max(staticquery)),
  'aggregate_security_lower_slack_from_this_dual':str(W-n*max(staticquery)),
  'status':'pass'
 }
 assert Fquery>W+min(pay)
 return result

if __name__=='__main__':
 result=check(sys.argv[1] if len(sys.argv)>1 and not sys.argv[1].startswith('--') else DEFAULT)
 print(json.dumps(result,indent=2))
 if '--output' in sys.argv:
  out=Path(sys.argv[sys.argv.index('--output')+1])
  with out.open('x') as fh:json.dump(result,fh,indent=2);fh.write('\n')
