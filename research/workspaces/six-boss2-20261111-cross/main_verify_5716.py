"""Main's independent Fraction replay of the stored new matrix and point.
Does not import the solver, basis recovery, or original matrix constructor.
"""
from pathlib import Path
from fractions import Fraction as F
import gzip,json,hashlib,time
b=Path(__file__).resolve().parent/'master_cuts'
start=time.time()
mp=b/'master_5716_exact.json.gz';pp=b/'merged_5716_exact.json'
m=json.loads(gzip.decompress(mp.read_bytes()));p=json.loads(pp.read_text())
x=[F(c['weight']) for c in p['columns']]
descriptors=[{k:v for k,v in c.items() if k!='weight'} for c in p['columns']]
assert descriptors==m['columns']
assert len(x)==m['column_count']==4849 and min(x)>=0
vals=[]
for i,row in enumerate(m['rows']):
 assert row['index']==i
 v=sum((F(a)*x[j] for j,a in row['nonzero']),F(0));vals.append(v)
 assert v>=0,(i,row['name'],v)
O=sum((F(a)*v for a,v in zip(m['normalization'],x)),F(0))
W=sum((F(a)*v for a,v in zip(m['objective'],x)),F(0))
assert O==1 and W==F(p['W']) and 2*W<1
out={'status':'PASS','scope':'Independent arithmetic replay of stored 5716x4849 matrix; no independent derivation of all inherited 5692 rows and no SPE claim','matrix_sha256':hashlib.sha256(mp.read_bytes()).hexdigest(),'point_sha256':hashlib.sha256(pp.read_bytes()).hexdigest(),'rows':len(vals),'columns':len(x),'positive_columns':sum(v>0 for v in x),'zero_slacks':sum(v==0 for v in vals),'minimum_slack':str(min(vals)),'O':str(O),'W':str(W),'gap':str(1-2*W),'seconds':time.time()-start}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
