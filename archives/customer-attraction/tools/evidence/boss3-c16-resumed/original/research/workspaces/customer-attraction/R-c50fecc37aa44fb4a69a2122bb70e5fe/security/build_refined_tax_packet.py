"""Generate one finite compact full-history strategy, using the canonical exact BI oracle.
The separately implemented auditor does not import this constructor or its solver.
"""
import json,gzip
from pathlib import Path
from customer_attraction import Instance,ExactSPESolver
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
def build(k=10):
 old=json.loads((ROOT/'examples/customer_attraction/coverage_opportunity_failure.json').read_text())
 assert k%2==0
 data={'topics':old['topics']+['P'],'players':k+3,'customers':old['customers']+[{'topics':[5],'multiplicity':5*k//2}]}
 inst=Instance.from_dict(data);solver=ExactSPESolver(inst)
 desired=(2,1,0,0,0,k);assert desired in solver.outcomes()
 nodes=[];lookup={}
 def ensure(c,t):
  key=(c,t)
  if key in lookup:return lookup[key]
  idx=len(nodes);lookup[key]=idx;nodes.append(None)
  if sum(c)==inst.players:
   assert c==t;nodes[idx]={'counts':list(c),'terminal':True};return idx
  floor=solver.threshold(c)
  children=[];admissible=[]
  for a in range(inst.topic_count):
   ch=tuple(v+int(j==a)for j,v in enumerate(c));outs=solver.outcomes(ch)
   minimum=min(inst.topic_payoff(a,z)for z in outs)
   minimizer=min(z for z in outs if inst.topic_payoff(a,z)==minimum)
   children.append((ch,minimizer))
   if t in outs and inst.topic_payoff(a,t)>=floor:admissible.append(a)
  assert admissible
  # A compact automaton can remember the desired outcome. This does not force
  # two histories with equal counts to use the same continuation.
  priority=([5,0,1,2,3,4] if t==desired and c[:5]==(0,0,0,0,0) and c[5]<k else [0,1,2,3,4,5])
  chosen=next(a for a in priority if a in admissible)
  links=[]
  for a,(ch,child_target) in enumerate(children):
   if a==chosen:child_target=t
   links.append(ensure(ch,child_target))
  nodes[idx]={'counts':list(c),'action':chosen,'children':links,'desired':list(t)}
  return idx
 root=ensure((0,)*6,desired)
 path=[];node=root
 while not nodes[node].get('terminal'):
  a=nodes[node]['action'];path.append(a);node=nodes[node]['children'][a]
 assert path==[5]*k+[0,0,1],path
 packet={'scope':'One complete ordered-history pure SPE represented by a deterministic finite acyclic continuation automaton. Histories update the automaton via the observed action. Different equal-count histories may reach different nodes.','instance':data,'root':root,'nodes':nodes,'expected_path':path,'expected_terminal_counts':list(desired),'constructor_stats':vars(solver.stats)}
 out=HERE/'refined_tax_k10_packet.json.gz'
 with gzip.open(out,'wt') as f:json.dump(packet,f,separators=(',',':'))
 print(json.dumps({'path':str(out),'nodes':len(nodes),'decision_nodes':sum(not z.get('terminal',False)for z in nodes),'compressed_bytes':out.stat().st_size,'stats':vars(solver.stats)},indent=2))
if __name__=='__main__':build()
