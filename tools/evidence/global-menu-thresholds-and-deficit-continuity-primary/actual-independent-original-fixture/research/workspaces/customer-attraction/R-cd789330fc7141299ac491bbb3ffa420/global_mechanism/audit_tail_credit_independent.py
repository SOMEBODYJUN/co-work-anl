"""Independent review: reads frozen DAG only, no discovery/audit/oracle imports.

The earlier source audits were read to understand the claimed contract. This
implementation rebuilds unit customers, reachability, path multiplicity, all
true continuation payoffs and the new deletion quantities directly.
"""
from fractions import Fraction as F
from functools import lru_cache
from math import lcm
from pathlib import Path
import gzip,hashlib,json
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[4]
SOURCE=REPO/'research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/security/refined_tax_k10_packet.json.gz'
blob=SOURCE.read_bytes();data=json.loads(gzip.decompress(blob));nodes=data['nodes'];root=data['root'];instance=data['instance']
n=instance['players'];labels=instance['topics'];a_count=len(labels)
units=[frozenset(t['topics']) for t in instance['customers'] for _ in range(t['multiplicity'])]
assert (n,a_count,len(units))==(13,6,36)
expected={(0,):2,(1,):2,(2,):1,(2,3):1,(2,4):1,(0,3,4):3,(1,3,4):1,(5,):25}
observed={}
for u in units:observed[tuple(sorted(u))]=observed.get(tuple(sorted(u)),0)+1
assert observed==expected and labels==['A','B','T','D','E','P']
assert nodes[root]['counts']==[0]*a_count
reachable={root};frontier=[root]
while frontier:
 i=frontier.pop();v=nodes[i];q=v['counts'];depth=sum(q)
 assert len(q)==a_count and all(type(c) is int and c>=0 for c in q)
 assert 0<=depth<=n
 if depth==n:
  assert v.get('terminal') is True and not v.get('children')
 else:
  assert not v.get('terminal',False) and type(v['action']) is int and 0<=v['action']<a_count
  assert len(v['children'])==a_count
  for a,j in enumerate(v['children']):
   assert type(j) is int and 0<=j<len(nodes)
   assert nodes[j]['counts']==[c+(a==b) for b,c in enumerate(q)]
   if j not in reachable:reachable.add(j);frontier.append(j)
assert len(reachable)==len(nodes)
order=sorted(reachable,key=lambda i:sum(nodes[i]['counts']))
ways=[0]*len(nodes);ways[root]=1
for i in order:
 if sum(nodes[i]['counts'])<n:
  for j in nodes[i]['children']:ways[j]+=ways[i]
for depth in range(n+1):assert sum(ways[i] for i in order if sum(nodes[i]['counts'])==depth)==a_count**depth
D=lcm(*range(1,n+1))
@lru_cache(None)
def payoff(q,a):
 total=0
 for unit in units:
  if a in unit:
   load=sum(q[b] for b in unit)
   assert 1<=load<=n and D%load==0
   total+=D//load
 return total
leaf={};path={};slacks=[];strict_witness=None
for i in reversed(order):
 v=nodes[i]
 if sum(v['counts'])==n:
  leaf[i]=tuple(v['counts']);path[i]=();continue
 a=v['action'];j=v['children'][a];leaf[i]=leaf[j];path[i]=(a,)+path[j]
 if 'desired' in v:assert tuple(v['desired'])==leaf[i]
 current=payoff(leaf[i],a)
 for alt,j in enumerate(v['children']):
  slack=current-payoff(leaf[j],alt)
  assert slack>=0,(i,alt,F(slack,D))
  slacks.append(slack)
  if slack>0 and strict_witness is None:strict_witness={'node':i,'chosen':a,'alternative':alt,'slack':str(F(slack,D))}
assert path[root]==(5,)*10+(0,0,1)
q=leaf[root];actual=tuple(F(payoff(q,a),D) for a in path[root]);assert actual==(F(5,2),)*12+(F(3),)
assert sum(actual)==33
branches=[]
for a,j in enumerate(nodes[root]['children']):
 full=(a,)+path[j];terminal=leaf[j];payments=[F(payoff(terminal,b),D) for b in full]
 assert payments[0]==F(5,2)
 branches.append({'theme':labels[a],'path':[labels[b] for b in full],'root':str(payments[0]),'tail':str(sum(payments[1:])),'tail_payoffs':list(map(str,payments[1:]))})
assert [F(b['tail']) for b in branches]==[F(61,2),F(63,2),F(63,2),F(61,2),F(61,2),F(61,2)]
checks=[]
for eps in (F(1,24),F(1,10**3),F(1,10**6)):
 threshold=F(5,2)+eps
 assert all(F(b['tail'])>=12*threshold for b in branches)
 low=[i for i in range(1,n) if actual[i]<threshold]
 assert low==list(range(1,12))
 kept=[a for i,a in enumerate(path[root]) if i not in low]
 after_counts=tuple(kept.count(a) for a in range(a_count))
 # payoff() scales by lcm to n and remains valid with fewer retained players.
 before=actual[0];after=F(payoff(after_counts,5),D);gain=after-before
 deficit=sum((threshold-actual[i] for i in low),F(0))
 absolute_overlap=F(0);formula=F(0)
 for unit in units:
  if 5 in unit:
   retained=sum(a in unit for a in kept)
   removed=sum(path[root][i] in unit for i in low)
   formula+=F(removed,retained*(retained+removed))
   absolute_overlap+=F(removed,retained+removed)
 assert after==25 and gain==F(45,2) and deficit==11*eps
 assert gain==formula==absolute_overlap
 checks.append({'epsilon':str(eps),'t':str(threshold),'low_indices':low,'root_before':str(before),'root_after':str(after),'gain':str(gain),'deficit':str(deficit),'ratio':str(gain/deficit),'deleted_overlap_profit':str(absolute_overlap),'deleted_total_profit':str(sum(actual[i] for i in low))})
report={'status':'PASS','source':str(SOURCE.relative_to(REPO)),'source_sha256':hashlib.sha256(blob).hexdigest(),'imports':'standard library only; no source audits, discovery scripts, canonical model or SPE oracle imported','source_audits_read_before_implementation':True,'unit_customers':len(units),'nodes':len(nodes),'decision_nodes':len(slacks)//a_count,'comparisons_including_self':len(slacks),'min_slack':str(F(min(slacks),D)),'distinct_count_states':len({tuple(v['counts']) for v in nodes}),'ordered_decision_histories':sum(a_count**d for d in range(n)),'terminal_histories':a_count**n,'actual_path':[labels[a] for a in path[root]],'actual_payoffs':list(map(str,actual)),'root_branches':branches,'deletion':checks,'strict_comparison_witness':strict_witness,'strongest_valid_scope':'fixed genuine SPE and fixed instance; arbitrary positive threshold margin epsilon; any coefficient K depending on instance/r but not on epsilon is impossible','not_refuted':'threshold tied to genuine safety value; fractional deletion; general GAP-r/EI/half'}
(HERE/'tail_credit_independent_audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ('status','unit_customers','nodes','comparisons_including_self','ordered_decision_histories','min_slack','deletion')}))
