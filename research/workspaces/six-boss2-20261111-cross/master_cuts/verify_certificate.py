#!/usr/bin/env python3
"""Standard-library replay of every rational primal row and dual column.

No original constructor, optimizer, NumPy, SciPy, SymPy, or floating arithmetic
is used for a mathematical assertion. Timings and displayed decimal W are not
part of the certificate. Scope is the fixed finite necessary system only.
"""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import gzip, hashlib, json, os, platform, sys, time
HERE=Path(__file__).resolve().parent

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def canonical_sha(value):return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def load(name):return json.loads((HERE/name).read_text())

def main():
    start=time.time()
    with gzip.open(HERE/'master_5716_exact.json.gz','rt',encoding='utf-8') as handle:matrix=json.load(handle)
    point=load('merged_5716_exact.json');dual=load('dual_exact.json');identity=load('matrix_identity.json')
    assert (matrix['row_count'],matrix['column_count'])==(5716,4849)
    assert len(matrix['rows'])==5716 and len(matrix['columns'])==4849
    assert sha(HERE/'master_5716_exact.json.gz')==identity['matrix_file_sha256']==dual['matrix_sha256']
    assert sha(HERE/'merged_5716_exact.json')==dual['point_sha256']
    descriptors=[{k:v for k,v in c.items() if k!='weight'} for c in point['columns']]
    assert descriptors==matrix['columns']
    assert canonical_sha(descriptors)==identity['descriptor_sha256']
    assert canonical_sha(matrix['objective'])==identity['objective_sha256']
    assert canonical_sha(matrix['normalization'])==identity['normalization_sha256']
    x=[F(c['weight']) for c in point['columns']];c=list(map(F,matrix['objective']));n=list(map(F,matrix['normalization']))
    assert min(x)>=0 and sum(a*b for a,b in zip(n,x))==1
    W=sum(a*b for a,b in zip(c,x));assert W==F(point['W'])==F(dual['dual_value'])==F(dual['normalization_multiplier'])
    rows=[];slacks=[];hashes=[]
    for i,row in enumerate(matrix['rows']):
        assert row['index']==i
        h=canonical_sha(row['nonzero']);assert h==row['sparse_sha256'];hashes.append(h)
        vals={j:F(v) for j,v in row['nonzero']};assert len(vals)==len(row['nonzero']);rows.append(vals)
        slacks.append(sum(v*x[j] for j,v in vals.items() if x[j]))
    assert canonical_sha(hashes)==identity['row_vector_list_sha256']
    assert min(slacks)>=0
    residual=[cj-W*nj for cj,nj in zip(c,n)]
    used=set();positive=[]
    for record in dual['row_multipliers']:
        i=record['row_index'];lam=F(record['weight']);assert i not in used and 0<=i<5716 and lam>=0
        used.add(i);assert record['row_name']==matrix['rows'][i]['name']
        for j,v in rows[i].items():residual[j]-=lam*v
        assert lam*slacks[i]==0
        if lam:positive.append(i)
    assert min(residual)>=0 and list(map(str,residual))==dual['residuals']
    assert sum(a*b for a,b in zip(residual,x))==0
    added=sorted(i for i in positive if i>=5692)
    assert added==[5696,5698]
    result={'status':'passed','scope':'Exact finite 5716-row necessary LP optimum; same optimum for inherited 5692 rows plus rows 5696 and 5698. No universal six-player theorem or SPE realization.','verified_primal_rows':len(rows),'verified_nonnegative_columns':len(x),'verified_dual_column_residuals':len(residual),'O':'1','W':str(W),'minimum_primal_slack':str(min(slacks)),'minimum_dual_residual':str(min(residual)),'positive_dual_multipliers':len(positive),'positive_added_row_indices':added,'base_plus_two_exact_optimum':str(W),'strict_half_gap_O_minus_2W':str(1-2*W),'matrix_sha256':sha(HERE/'master_5716_exact.json.gz'),'point_sha256':sha(HERE/'merged_5716_exact.json'),'dual_sha256':sha(HERE/'dual_exact.json'),'row_name_counts':dict(Counter(r['name'].split(':')[0] for r in matrix['rows'])),'execution':{'command':[sys.executable,'-B',str(Path(__file__).resolve())],'cwd':os.getcwd(),'python':platform.python_version(),'script_sha256':sha(__file__),'elapsed_seconds':time.time()-start,'optimizer_calls':0,'original_constructor_calls':0,'math_float_operations':0}}
    (HERE/'certificate_verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='row_name_counts'},ensure_ascii=False),flush=True)
if __name__=='__main__':main()
