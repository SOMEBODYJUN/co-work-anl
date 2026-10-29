"""Finite unit-customer 18-label seed subcatalogs from threshold realizations.

Deleting other actions does not preserve an SPE; these are candidate instances
for complete original-model backward induction, not counterexample certificates.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,permutations
from collections import defaultdict
from math import lcm,gcd
import json,hashlib
HERE=Path(__file__).resolve().parent
PAT=tuple(product(range(2),repeat=3))

def main():
 source=HERE/'combined_branch_master_exact.json';point=json.loads(source.read_text());byhist={};hi=None
 for j,c in enumerate(point['columns']):
  if c['kind']=='hist':hi=j;byhist[hi]={'data':c,'groups':{}}
  elif c['kind']=='joint-reply':
   f,d,wi,wj=c['group'];g=(f,d,tuple(wi),tuple(wj));byhist[hi]['groups'].setdefault(g,{})[tuple(c['state'])]=F(c['weight'])
 zr=json.loads((HERE/'pair_master_exact.json').read_text());zslabs={}
 for v in zr['variables']:
  key=(v['hist_column'],v['left'],v['right']);f,d,wi,wj=v['group'];g=(f,d,tuple(wi),tuple(wj));zslabs.setdefault(key,{})[g]=F(v['weight'])
 allmasks={q:defaultdict(F) for q in ('Rdiag','Zdiag')}
 for hi,dd in byhist.items():
  c=dd['data'];hm=F(c['weight']);a=tuple(map(int,c['actual_bits']));h=c['hist']
  if not hm:continue
  words=[w for w,n in zip(PAT,h) for _ in range(n)];assignments=sorted(set(permutations(words)));nperm=len(assignments)
  radii={g:s[1,0]+s[1,1] for g,s in dd['groups'].items() if g[0:2]==(1,1)}
  rcuts=sorted({F(),hm,*radii.values()})
  actualmask=sum(x<<i for i,x in enumerate(a))
  for ws in assignments:
   basemask=actualmask+sum(w[0]<<(6+i) for i,w in enumerate(ws))
   for lo,up in zip(rcuts,rcuts[1:]):
    mask=basemask+sum(int(up<=radii[1,1,w,w])<<(12+i) for i,w in enumerate(ws))
    allmasks['Rdiag'][mask]+=F(up-lo,nperm)
   for (hii,left,right),zs in zslabs.items():
    if hii!=hi:continue
    width=F(right)-F(left);wanted={g:v for g,v in zs.items() if g[0:2]==(1,1)}
    cuts=sorted({F(),width,*wanted.values()})
    for lo,up in zip(cuts,cuts[1:]):
     mask=basemask+sum(int(up<=wanted[1,1,w,w])<<(12+i) for i,w in enumerate(ws))
     allmasks['Zdiag'][mask]+=F(up-lo,nperm)
 for kind,masses in allmasks.items():
  assert sum(v for mask,v in masses.items() if mask&63)==F(point['W'])
  assert sum(v for mask,v in masses.items() if mask&(63<<6))==1
  masses={mask:v for mask,v in masses.items() if mask and v}
  # Deduplicate identical coverage columns so the catalogue is literally a set.
  masks=sorted(masses);columns=[tuple(int(mask>>i&1) for mask in masks) for i in range(18)]
  unique=[];mapping=[]
  for col in columns:
   if col not in unique:unique.append(col)
   mapping.append(unique.index(col))
  # OR repeated bits rather than summing duplicate coverage aliases.
  merged=defaultdict(F)
  for mask,v in masses.items():
   new=0
   for i in range(18):
    if mask>>i&1:new|=1<<mapping[i]
   merged[new]+=v
  den=lcm(*(v.denominator for v in merged.values()));ints={mask:int(v*den) for mask,v in merged.items()};gg=gcd(*ints.values());ints={mask:v//gg for mask,v in ints.items()};scale=F(den,gg)
  labels=['A'+str(i+1) for i in range(6)]+['T'+str(i+1) for i in range(6)]+[kind+'_'+str(i+1) for i in range(6)]
  topics=[labels[mapping.index(i)] for i in range(len(unique))]
  inst={'topics':topics,'customers':[{'topics':[i for i in range(len(unique)) if mask>>i&1],'multiplicity':v} for mask,v in sorted(ints.items())],'players':6}
  target=HERE/('seed18_'+kind+'.json');target.write_text(json.dumps(inst,indent=2)+'\n')
  meta={'scope':'exact original-model seed subcatalog, no inherited SPE','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'pair_master_sha256':hashlib.sha256((HERE/'pair_master_exact.json').read_bytes()).hexdigest(),'selection':kind,'source_label_aliases':dict(zip(labels,mapping)),'themes':len(unique),'customer_types':len(ints),'customer_scale':str(scale),'total_customers':str(sum(ints.values())),'multiplicity_max_digits':max(map(lambda x:len(str(x)),ints.values())),'actual_path':[mapping[i] for i in range(6)],'comparison_T_path':[mapping[i] for i in range(6,12)],'actual_W':str(scale*F(point['W'])),'comparison_union':str(scale),'actual_path_is_SPE':'not asserted; full BI required'}
  target.with_name(target.stem+'_meta.json').write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps({k:v for k,v in meta.items() if k not in ('source_label_aliases',)},indent=2))
if __name__=='__main__':main()
