from pathlib import Path
from fractions import Fraction as F
import json,hashlib
root=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-um-star-transfer-majority-and-rank-programs-primary/tools/evidence/um-star-transfer-majority-and-rank-programs-primary')
p=root/'replay/adc59aa8e0852e9e9cfd/exports'
a=json.loads((p/'contracted_sparse_configuration_input.json').read_text());w=json.loads((p/'contracted_sparse_configuration_witness.json').read_text());m=len(a['machines']);n=len(a['jobs']);T=F(a['threshold']);cost=[{i:F(t) for i,t in j['eligible']} for j in a['jobs']]
assert m==405 and n==727 and sum(map(len,cost))==1778
seen=set();cover=[F(0)]*n;support=0;forced=F(0);maxload=F(0);sinkidx=a['machines'].index(['z']);sinkmax=F(0)
for row in w['configuration_point']:
 i=row['machine'];assert i not in seen and 0<=i<m;seen.add(i);assert sum(F(c['weight']) for c in row['configurations'])==1
 for c in row['configurations']:
  weight=F(c['weight']);js=c['jobs'];assert weight>0 and len(js)==len(set(js));load=sum((cost[j][i] for j in js),F(0));assert load<=T;maxload=max(maxload,load);support+=1
  if i==sinkidx:sinkmax=max(sinkmax,load)
  for j in js:
   cover[j]+=weight
   if (j,i)==(w['forced_job'],w['forced_machine']):forced+=weight
assert seen==set(range(m)) and all(x==1 for x in cover) and forced==1
assignment=w['integer_upper_assignment'];assert len(assignment)==n;loads=[F(0)]*m
for j,i in enumerate(assignment):loads[i]+=cost[j][i]
assert max(loads)==F(w['integer_upper_makespan'])==F(5,3);assert sinkmax==F(w['maximum_sink_configuration'])==F(3,4)
result={'status':'passed','method':'one independent parsing/index-reconstruction check of newly exported data; no original import or rerun','machines':m,'jobs':n,'finite_edges':sum(map(len,cost)),'point_support':support,'forced_job':w['forced_job'],'forced_machine':w['forced_machine'],'forced_mass':str(forced),'maximum_configuration_load':str(maxload),'maximum_sink_configuration':str(sinkmax),'integer_upper_makespan':str(max(loads)),'all_serialized_jobs_and_rows_checked':True,'original_primary_entry_executions_added':0}
print(json.dumps(result,indent=2))
