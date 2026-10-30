"""Independent definition-level compact full-history SPE audit, standard library only.
It reads only the frozen packet, expands distinct unit customers, and verifies
all automaton nodes, actions, and transitions. No constructor/BI oracle is used.
"""
from pathlib import Path
from math import lcm
from fractions import Fraction as F
import gzip,json,itertools
HERE=Path(__file__).resolve().parent

def audit():
 with gzip.open(HERE/'refined_tax_k10_packet.json.gz','rt')as f:d=json.load(f)
 inst=d['instance'];n=inst['players'];p=len(inst['topics']);nodes=d['nodes'];root=d['root']
 units=[frozenset(c['topics'])for c in inst['customers']for _ in range(c['multiplicity'])]
 L=lcm(*range(1,n+1));states={};visited=set();queue=[root]
 while queue:
  idx=queue.pop()
  if idx in visited:continue
  visited.add(idx);q=nodes[idx];c=tuple(q['counts']);assert len(c)==p and min(c)>=0 and sum(c)<=n
  if q.get('terminal'):
   assert sum(c)==n and 'children'not in q
  else:
   assert sum(c)<n and len(q['children'])==p and 0<=q['action']<p
   for a,j in enumerate(q['children']):
    assert 0<=j<len(nodes)
    assert tuple(nodes[j]['counts'])==tuple(v+int(b==a)for b,v in enumerate(c))
    queue.append(j)
 assert visited==set(range(len(nodes)))
 terminal={};payoff_cache={}
 def payoff(a,t):
  key=(a,t)
  if key not in payoff_cache:
   total=0
   for u in units:
    if a in u:
     load=sum(t[b]for b in u);assert load>=1 and L%load==0
     total+=L//load
   payoff_cache[key]=total
  return payoff_cache[key]
 comparisons=0;minimum=None;ties=0
 for idx in sorted(visited,key=lambda j:sum(nodes[j]['counts']),reverse=True):
  q=nodes[idx];c=tuple(q['counts'])
  if q.get('terminal'):terminal[idx]=c;continue
  a=q['action'];t=terminal[q['children'][a]];terminal[idx]=t
  assert tuple(q['desired'])==t
  base=payoff(a,t)
  for b,j in enumerate(q['children']):
   gap=base-payoff(b,terminal[j]);assert gap>=0,(idx,b,gap)
   comparisons+=1;minimum=gap if minimum is None else min(minimum,gap);ties+=gap==0
 # Completeness proof: from root, every observed action has exactly one
 # transition, whose counts add that action and whose depth increases by 1.
 # Thus every ordered history of length <n induces exactly one audited node.
 path=[];idx=root
 while not nodes[idx].get('terminal'):
  a=nodes[idx]['action'];path.append(a);idx=nodes[idx]['children'][a]
 assert path==d['expected_path']==[5]*10+[0,0,1]
 t=terminal[root];assert t==tuple(d['expected_terminal_counts'])==(2,1,0,0,0,10)
 loads=[sum(t[b]for b in u)for u in units]
 W=sum(h>0 for h in loads);payoffs=[F(payoff(a,t),L)for a in path]
 alpha=F(n-1,n)
 g=[sum((1/(1+alpha*h)for u,h in zip(units,loads)if a in u),F(0))for a in range(p)]
 G=sum((1/(1+alpha*h)for h in loads if h>0),F(0));M=max(g)
 assert W==33 and payoffs==[F(5,2)]*12+[F(3)]
 assert g==[F(65,37),F(39,25),F(3),F(2381,925),F(2381,925),F(325,133)]
 assert G==F(708669,123025)and M==3
 assert n*M-W-G==F(29481,123025)>0
 assert M-G/n-min(payoffs)==F(13999,246050)>0
 opt=max(sum(any(a in u for a in A)for u in units)for size in range(min(n,p)+1)for A in itertools.combinations(range(p),size))
 assert opt==36 and 2*W>=opt
 # A genuine static safety cap: 9 P rivals plus A,B,T, independent of query.
 B=(0,1,2)+(5,)*9
 f=[sum((F(1,1+sum(b in u for b in B))for u in units if a in u),F(0))for a in range(p)]
 assert f==[F(5,2),F(3,2),F(3,2),F(5,2),F(5,2),F(5,2)]
 assert max(f)==F(5,2)and W-n*max(f)==F(1,2)
 return {'status':'PASS','scope':d['scope'],'players':n,'topics':p,'unit_customers':len(units),'automaton_nodes':len(nodes),'decision_nodes':sum(not q.get('terminal',False)for q in nodes),'distinct_count_states':len({tuple(q['counts'])for q in nodes}),'decision_comparisons':comparisons,'ties_including_self':ties,'minimum_spe_gap':str(F(minimum,L)),'actual_path':path,'actual_payoffs':list(map(str,payoffs)),'W':W,'OPT':opt,'alpha':str(alpha),'query_values':list(map(str,g)),'M':str(M),'G':str(G),'aggregate_refined_tax_violation':str(n*M-W-G),'individual_refined_tax_violation':str(M-G/n-min(payoffs)),'static_cap_background':list(B),'static_cap_query_values':list(map(str,f)),'security_upper_bound':str(max(f)),'strong_security_margin_lower_bound':str(W-n*max(f))}
if __name__=='__main__':
 r=audit();print(json.dumps(r,indent=2,ensure_ascii=False));(HERE/'refined_tax_k10_audit.json').write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
