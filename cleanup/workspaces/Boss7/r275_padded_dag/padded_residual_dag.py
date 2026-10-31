"""Discovery/certificate builder using the canonical exact solver; no proof by itself."""
from pathlib import Path
import sys,json,math
sys.path.insert(0,str(Path(__file__).resolve().parents[5]))
from customer_attraction.model import Instance
from customer_attraction.exact import ExactSPESolver
HERE=Path(__file__).parent

def instance(m):
 sets=[{'AD0','AD1','AE0','AE1'},{'B0','B1','B2','BD0','BD1'},{'T0','T1','T2','TD0','TD1'},{'AD0','AD1','BD0','BD1','TD0','TD1'},{'AE0','AE1','BD0','BD1','TD0','TD1'}]
 sets.extend([{f'P{i}x{j}' for j in range(4)} for i in range(m-2)])
 return Instance.from_topic_sets(sets,m,labels=['A','B','T','D','E']+[f'P{i}' for i in range(m-2)])

def build(m):
 inst=instance(m);s=ExactSPESolver(inst);p=inst.topic_count;h=list(range(5,p))+[0,1];root_target=inst.counts(h);assert root_target in s.outcomes()
 nodes=[];lookup={}
 def add(k,c):
  key=(k,c)
  if key in lookup:return lookup[key]
  i=len(nodes);lookup[key]=i;nodes.append(None)
  if sum(k)==m:
   assert k==c;nodes[i]=dict(counts=k,target=c);return i
  ks=[k[:a]+(k[a]+1,)+k[a+1:] for a in range(p)]
  valid=[a for a,child in enumerate(ks) if c in s.outcomes(child) and inst.topic_payoff(a,c)>=s.threshold(k)]
  # Keep the intended ordered root path when this is its prefix.
  t=sum(k);onpath=tuple(h[:t]);pathcounts=inst.counts(onpath)
  a=h[t] if k==pathcounts and c==root_target and h[t] in valid else valid[0]
  children=[]
  for b,child in enumerate(ks):
   d=c if b==a else min(s.outcomes(child),key=lambda z:(inst.topic_payoff(b,z),z))
   children.append(add(child,d))
  nodes[i]=dict(counts=k,target=c,action=a,children=children);return i
 root=add((0,)*p,root_target)
 result=dict(schema='complete-SPE-count-target-DAG-v1',scope='Counterexample only to common-query regret <= minimum provider payoff; NOT to Q-CAG-HALF',instance=inst.to_dict(),root=root,nodes=nodes,expected=dict(path=h,utilities=[4]*(m-1)+[5],W=4*m+1,OPT=inst.optimal_welfare(),query=2,query_uncovered=5,F=5*m,minimum_utility=4,bridge_slack=5-m))
 out=HERE/f'padded_residual_m{m}_dag.json';out.write_text(json.dumps(result,separators=(',',':')))
 print(dict(m=m,nodes=len(nodes),file=str(out),bytes=out.stat().st_size),flush=True)
if __name__=='__main__':
 for m in map(int,sys.argv[1:] or ['6']):build(m)
