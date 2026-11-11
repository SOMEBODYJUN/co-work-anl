"""Apply the exact nine-weight source-4 inequality to the common maximum M.
Only frozen M/hist conditionals are read; hidden post-query tails are projected.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
b=Path(__file__).resolve().parent.parent
p=b/'master_cuts/merged_5716_exact.json';d=json.loads(p.read_text());cols=d['columns'];xx=[F(c['weight']) for c in cols]
hs={i:c for i,c in enumerate(cols) if c['kind']=='hist'}
allrows=[]
for query in list(range(6))+['Tmean','Bmean','Cmean']:
 row={0:F(925)}
 for i,h in hs.items():
  aa=list(map(int,h['actual_bits']));load=sum(aa)
  if aa[3]:row[i]=F(71198,load)
 for i,c in enumerate(cols):
  if c['kind']!='maximum-root-family-state':continue
  h=hs[c['hist_column']];aa=list(map(int,h['actual_bits']));pfx=sum(aa[:3]);t=c['M']
  if isinstance(query,int):q=F(aa[query])
  else:
   shift={'Tmean':2,'Bmean':1,'Cmean':0}[query]
   q=sum((F(w*((typ>>shift)&1),6) for typ,w in enumerate(h['hist'])),F(0))
  phi=F(6052)*q/(pfx+1) if not t else F(925)+(65146+6052*q)/(pfx+3)
  if phi:row[i]=-phi
 val=sum((v*xx[i] for i,v in row.items()),F(0))
 allrows.append({'query':query,'normalized_slack':str(val/71198),'float':float(val/71198),'coefficients':[[i,str(v/71198)] for i,v in sorted(row.items())]})
print([{k:v for k,v in r.items() if k!='coefficients'} for r in allrows])
(b/'main_pair/maximum_query_at_5716.json').write_text(json.dumps({'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'scope':'exact nine-weight source-4 necessary rows with T=M','rows':allrows},ensure_ascii=False,indent=2)+'\n')
