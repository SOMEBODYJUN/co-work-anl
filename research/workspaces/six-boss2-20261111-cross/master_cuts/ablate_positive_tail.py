#!/usr/bin/env python3
"""Exact finite-system witness for the contribution of positive tail weights.

Remove only the twelve beta-positive rows introduced in round 5775. Keep the
whole 5752 master, all seven new portfolio rows, and all four beta-zero updates.
The resulting rational point is a feasibility witness, not an optimality claim.
The source matrix is reused in memory; no duplicate matrix archive is written.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse, datetime, gzip, hashlib, json, platform, sys, time
import extend_master as engine

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]
STEM='ablate_5775_positive_tail'
SOURCE=HERE/'dynamic_5775_matrix.json.gz'
PACK=HERE.parent/'coverage_bridge/selected_prefix_tail_5752.json'
EXPECTED_SOURCE='49470d85127a7f24b4059c3289c9995f469445170fecefed6644bca3d29c82ae'
EXPECTED_PACK='595e7386cfacc591f513fe477453e94d9e2271e4cb63ce3f5c57a8dc34fabd50'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,value):
    p=HERE/(STEM+'_'+name+'.json')
    p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    return p

def load_domain():
    assert sha(SOURCE)==EXPECTED_SOURCE and sha(PACK)==EXPECTED_PACK
    with gzip.open(SOURCE,'rt',encoding='utf-8') as f: full=json.load(f)
    pack=json.loads(PACK.read_text())
    removed_names={f'prefix_tail_5752-{i}' for i,c in enumerate(pack['cuts'],1)
                   if any(F(v) for v in c['beta'].values())}
    assert len(removed_names)==12
    removed=[i for i,r in enumerate(full['rows']) if r['name'] in removed_names]
    keep=[i for i in range(len(full['rows'])) if i not in removed]
    assert len(removed)==12 and len(keep)==5763
    assert keep[:5759]==list(range(5759))
    assert [full['rows'][i]['name'] for i in keep[5759:]]==[
        'prefix_tail_5752-3','prefix_tail_5752-6',
        'prefix_tail_5752-11','prefix_tail_5752-14']
    data=dict(full)
    data['scope']='Finite ablation of certified 5775 system: remove only twelve positive-tail rows; preserve all 5752 old rows, seven portfolio updates and four beta-zero updates. Exact feasible point only, no ablated optimum or SPE claim.'
    data['row_count']=5763
    data['rows']=[dict(full['rows'][i],index=k,source_row_index=i) for k,i in enumerate(keep)]
    rows=[{j:F(v) for j,v in r['nonzero']} for r in data['rows']]
    obj=[F(v) for v in data['objective']]
    norm=[F(v) for v in data['normalization']]
    return full,data,rows,obj,norm,keep,removed

def verify(domain):
    started=time.time()
    full,data,rows,obj,norm,keep,removed=domain
    point_path=HERE/(STEM+'_exact.json')
    point=json.loads(point_path.read_text())
    assert [engine.desc(c) for c in point['columns']]==data['columns']
    x=[F(c['weight']) for c in point['columns']]
    assert min(x)>=0 and sum(n*v for n,v in zip(norm,x))==1
    W=sum(c*v for c,v in zip(obj,x)); assert W==F(point['W'])
    slacks=[sum(v*x[j] for j,v in row.items() if x[j]) for row in rows]
    assert min(slacks)>=0
    dual_path=HERE/'dynamic_5775_dual.json'
    dual=json.loads(dual_path.read_text());bound=F(dual['dual_value'])
    assert dual['matrix_sha256']==EXPECTED_SOURCE and dual['normalization_multiplier']==str(bound)
    residual=[c-bound*n for c,n in zip(obj,norm)]
    used=set()
    for record in dual['row_multipliers']:
        i=record['row_index'];weight=F(record['weight'])
        assert i not in used and weight>0 and record['row_name']==full['rows'][i]['name'];used.add(i)
        for j,v in full['rows'][i]['nonzero']:residual[j]-=weight*F(v)
    assert min(residual)>=0 and list(map(str,residual))==dual['residuals']
    assert W<bound
    removed_slacks=[{
        'source_row_index':i,'name':full['rows'][i]['name'],
        'slack':str(sum(F(v)*x[j] for j,v in full['rows'][i]['nonzero'] if x[j]))
    } for i in removed]
    result={
        'status':'PASS','scope':data['scope'],
        'claim':'The twelve added positive-tail rows strictly improve the finite optimum beyond all seven contemporaneous portfolio and four beta-zero updates. No complete-cone comparison is claimed.',
        'matrix_rows_retained':5763,'columns':len(x),'retained_source_row_indices':keep,
        'removed_source_rows':removed_slacks,
        'minimum_primal_slack':str(min(slacks)),
        'minimum_column_mass':str(min(x)),
        'feasible_W_without_positive_tail':str(W),
        'certified_full_system_lower_bound':str(bound),
        'strict_finite_improvement_at_least':str(bound-W),
        'feasible_W_display':float(W),'strict_improvement_display':float(bound-W),
        'full_dual_minimum_residual':str(min(residual)),
        'source_matrix_sha256':sha(SOURCE),'prefix_tail_pack_sha256':sha(PACK),
        'point_sha256':sha(point_path),'full_dual_sha256':sha(dual_path),
        'exact_feasible_point_positive_columns':sum(v>0 for v in x),
        'seconds':time.time()-started,
        'math_float_operations':'None in assertions; two display conversions only.',
        'optimizer_calls_in_verification':0
    }
    write('verification',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('retained_source_row_indices','removed_source_rows')},ensure_ascii=False),flush=True)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('mode',choices=('all','verify'));args=ap.parse_args()
    started=time.time();stamp=datetime.datetime.now(datetime.timezone.utc).isoformat();success=False
    try:
        domain=load_domain()
        if args.mode=='all':
            assert not (HERE/(STEM+'_exact.json')).exists(),'Frozen witness exists; use verify.'
            engine.STEM=STEM
            engine.load=lambda: domain[1:5]
            engine.solve()
            engine.reconstruct()
        verify(domain);success=True
    finally:
        write('execution_'+args.mode,{
            'command':[sys.executable,'-B',str(Path(__file__).resolve()),args.mode],
            'cwd':str(Path.cwd()),'started_utc':stamp,'elapsed_seconds':time.time()-started,
            'success':success,'script_sha256':sha(Path(__file__)),
            'python':platform.python_version(),
            'dependencies':{name:sha(HERE/name) for name in ('extend_master.py','merge_master.py')}
        })

if __name__=='__main__':main()
