"""Main's independent finite ablation verification; no optimizer/generator imports."""
from pathlib import Path
from fractions import Fraction as F
import gzip,hashlib,json,time
B=Path(__file__).resolve().parent
mp=B/'master_cuts/dynamic_5775_matrix.json.gz'
pp=B/'master_cuts/ablate_5775_positive_tail_exact.json'
cp=B/'coverage_bridge/selected_prefix_tail_5752.json'
dp=B/'master_cuts/dynamic_5775_dual.json'
m=json.loads(gzip.decompress(mp.read_bytes()))
p,pack,d=(json.loads(z.read_text()) for z in (pp,cp,dp))
start=time.time()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert d['matrix_sha256']==sha(mp)
assert m['columns']==[{k:v for k,v in c.items() if k!='weight'} for c in p['columns']]
x=[F(c['weight']) for c in p['columns']]
c,n=list(map(F,m['objective'])),list(map(F,m['normalization']))
assert min(x)>=0 and len(x)==4849 and sum(a*b for a,b in zip(n,x))==1
W=sum(a*b for a,b in zip(c,x));assert W==F(p['W'])
remove={f'prefix_tail_5752-{i+1}' for i,cut in enumerate(pack['cuts']) if any(F(w)>0 for w in cut['beta'].values())}
assert len(remove)==12
keep=[];dropped=[];slacks=[]
for i,row in enumerate(m['rows']):
    assert row['index']==i
    slack=sum((F(v)*x[j] for j,v in row['nonzero']),F(0))
    if row['name'] in remove:dropped.append({'index':i,'name':row['name'],'slack':str(slack)})
    else:
        assert slack>=0
        keep.append(i);slacks.append(slack)
assert len(keep)==5763 and len(dropped)==12
assert keep[:5759]==list(range(5759))
assert {m['rows'][i]['name'] for i in keep[5759:]}=={'prefix_tail_5752-3','prefix_tail_5752-6','prefix_tail_5752-11','prefix_tail_5752-14'}
bound=F(d['dual_value']);assert bound==F(d['normalization_multiplier'])>W
residual=[cj-bound*nj for cj,nj in zip(c,n)]
used=set()
for z in d['row_multipliers']:
    i,lam=z['row_index'],F(z['weight'])
    assert i not in used and lam>0 and z['row_name']==m['rows'][i]['name'];used.add(i)
    for j,v in m['rows'][i]['nonzero']:residual[j]-=lam*F(v)
assert min(residual)>=0 and residual==list(map(F,d['residuals']))
assert any(F(z['slack'])<0 for z in dropped)
out={'status':'PASS','scope':'Exact feasible point for all 5763 retained rows, with only twelve positive-tail rows omitted; strict comparison against certified 5775 lower bound, not an optimum claim for the ablated system or an infinite-cone separation',
     'matrix_sha256':sha(mp),'point_sha256':sha(pp),'prefix_tail_pack_sha256':sha(cp),'full_dual_sha256':sha(dp),
     'rows_retained':len(keep),'rows_removed':dropped,'positive_columns':sum(a>0 for a in x),'minimum_retained_slack':str(min(slacks)),
     'W_feasible_without_twelve_positive_tail_rows':str(W),'certified_full_lower_bound':str(bound),
     'strict_finite_improvement_at_least':str(bound-W),'minimum_full_dual_residual':str(min(residual)),'seconds':time.time()-start}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='rows_removed'},ensure_ascii=False,indent=2))
