"""Independent exact certificate check, bound to the literal-rebuilt matrix.

Does not import the constructor, numerical solver, or rational recoverer.
The independently reconstructed symbolic coefficient certificate is SHA-bound
and covers all rows, including every zero histogram and min upper bound.
"""
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import gzip
import json

HERE=Path(__file__).resolve().parent
POINT=HERE.parent/'full624_augmented_lp/recovery/augmented_lp_exact.json'

def sha(p):return sha256(p.read_bytes()).hexdigest()
def decode(v):return {j:Q(c) for j,c in v}
def sparse(v):return [[j,str(c)] for j,c in sorted(v.items()) if c]
def evaluate(v,w):return sum((c*w[j] for j,c in v.items()),Q())

def main():
    audit=json.loads((HERE/'preflight_literal_audit.json').read_bytes())
    lift=json.loads(gzip.decompress((HERE/'symbolic_lift.json.gz').read_bytes()))
    cert=json.loads((HERE/'exact_certificate.json').read_bytes())
    point=json.loads(POINT.read_bytes())
    assert audit['passed'] and audit['all_rows_checked']==21572
    assert audit['audit_source_sha256']==sha(HERE/'literal_audit.py')
    assert audit['point_sha256']==sha(POINT)==cert['point_sha256']==lift['point_sha256']
    assert audit['symbolic_lift_sha256']==sha(HERE/'symbolic_lift.json.gz')==cert['symbolic_lift_sha256']
    assert lift['old_descriptors']==[{k:v for k,v in c.items() if k!='weight'} for c in point['columns'][:4849]]
    w=[Q(c['weight']) for c in point['columns'][:4849]]
    rows=[decode(r['row']) for r in lift['rows']];n=len(lift['new_columns'])
    frozen=json.loads((HERE/'actions_ready.json').read_bytes())
    repo=HERE.parent.parents[2]
    for item in frozen['dependencies']:
        assert sha(repo/item['path'])==item['sha256']
    cloud=json.loads((HERE/'actions_output/phase_I_discovery.json').read_bytes())
    order=json.loads(gzip.decompress((HERE/'actions_output/phase_I_input_order.json.gz').read_bytes()))
    assert cloud['linprog_calls']==1 and cloud['success'] and cloud['phase_I']==0
    assert cloud['point_sha256']==sha(POINT) and cloud['symbolic_lift_sha256']==sha(HERE/'symbolic_lift.json.gz')
    assert cloud['preflight_sha256']==sha(HERE/'preflight_literal_audit.json')
    assert cloud['source_sha256']==sha(HERE/'actions_phase1.py')==sha(HERE/'actions_output/executed_actions_phase1.py')
    assert order['row_order']==[r['name'] for r in lift['rows']]
    assert order['new_column_order']==lift['new_columns']+[{'kind':'phase-I-uniform-delta'}]
    assert order['original_old_column_order']==lift['old_descriptors']
    assert order['fixed_old_values']==list(map(str,w))
    fixed=[evaluate({j:v for j,v in r.items() if j<4849},w) for r in rows]
    assert order['fixed_old_row_values']==cloud['fixed_old_row_values']==list(map(str,fixed))
    remote_audit=json.loads((HERE.parent/'compute_dispatch/rze-closure-download-input-audit.json').read_bytes())
    for item in remote_audit['runtime_outputs']:
        assert sha(repo/item['path'])==item['sha256']
    # Verify the numerical input arrays against the exact symbolic coefficients.
    # This imports sparse readers only; no numerical optimizer is imported.
    import numpy as np
    from scipy.sparse import load_npz,coo_matrix
    cloudA=load_npz(HERE/'actions_output/phase_I_matrix.npz').tocsr()
    ai=[];aj=[];av=[]
    for i,r in enumerate(rows):
        for j,v in r.items():
            if j>=4849:ai.append(i);aj.append(j-4849);av.append(-float(v))
        ai.append(i);aj.append(n);av.append(-1.)
    expectedA=coo_matrix((av,(ai,aj)),shape=(len(rows),n+1)).tocsr()
    assert (cloudA-expectedA).nnz==0
    with np.load(HERE/'actions_output/phase_I_vectors.npz') as vectors:
        assert np.array_equal(vectors['b_ub'],np.asarray([float(v) for v in fixed]))
        assert np.array_equal(vectors['c'],np.asarray([0.]*n+[1.]))
        assert np.array_equal(vectors['lower_bounds'],np.zeros(n+1))
        assert np.isposinf(vectors['upper_bounds']).all()
    report={'scope':'Exact verification of the complete single-query envelope lift; common realization and full SPE remain unproved.',
            'point_sha256':sha(POINT),'symbolic_lift_sha256':sha(HERE/'symbolic_lift.json.gz'),
            'literal_preflight_sha256':sha(HERE/'preflight_literal_audit.json'),
            'certificate_sha256':sha(HERE/'exact_certificate.json'),'verifier_sha256':sha(Path(__file__)),
            'old_columns':4849,'new_columns':n,'rows':len(rows),'kind':cert['kind'],
            'optimization_calls':0,'zero_histograms_preserved':audit['zero_mass_histograms']}
    report.update(all_frozen_inputs_unchanged=True,all_8_raw_cloud_outputs_unchanged=True,
                  cloud_input_arrays_match_exact_matrix=True,all_input_orders_checked=True,
                  discovery_sha256=sha(HERE/'actions_output/phase_I_discovery.json'),
                  cloud_run_id=remote_audit['run_id'],cloud_artifact_id=remote_audit['artifact_id'])
    if cert['kind']=='primal':
        x=list(map(Q,cert['new_values']));assert len(x)==n and min(x)>=0
        assert cert['E_values']==list(map(str,x[:776]))
        assert cert['canonical_min_values']==list(map(str,x[776:]))
        values=w+x
        for i,c in enumerate(lift['new_columns'][776:]):
            assert x[776+i]==min(evaluate(decode(c['a']),values),evaluate(decode(c['b']),values))
        slacks=[evaluate(r,values) for r in rows]
        assert min(slacks)>=0 and list(map(str,slacks))==cert['row_slacks']
        requested=json.loads((HERE/'fixed_envelopes.json').read_bytes())
        assert sha(HERE/'fixed_envelopes.json')==audit['fixed_envelopes_sha256']
        assert requested['exact_deduplication']==lift['exact_deduplication']
        aliases={tuple(a['requested']):a for a in lift['exact_deduplication']}
        all_requested=[]
        for r in requested['rows']:
            s=evaluate(decode(r['linear']),values)+sum((Q(v)*values[5625+j] for j,v in r['min_terms']),Q())
            alias=aliases[tuple(r['name'])]
            if alias['reference_kind']=='zero':expected=Q()
            elif alias['reference_kind']=='base':expected=slacks[alias['reference_index']]
            else:expected=slacks[893+alias['reference_index']]
            assert s==expected and s>=0
            all_requested.append({'name':r['name'],'value':str(s),'value_float':float(s),
                                  'reference_kind':alias['reference_kind'],'reference_index':alias['reference_index']})
        assert len(all_requested)==177
        (HERE/'new_envelopes_exact.json').write_text(json.dumps({
            'scope':report['scope'],'point_sha256':sha(POINT),'certificate_sha256':sha(HERE/'exact_certificate.json'),
            'rows':all_requested,'all_177_nonnegative':True},ensure_ascii=False,indent=2)+'\n')
        report.update(all_rational_new_values_checked=True,all_canonical_mins_checked=True,
                      all_rows_nonnegative=True,minimum_slack=str(min(slacks)),
                      positive_E_values=sum(v>0 for v in x[:776]),exact_phase_I='0',
                      all_177_requested_rows_and_aliases_checked=True,
                      requested_zero_rows=sum(r['value']=='0' for r in all_requested),
                      requested_positive_rows=sum(Q(r['value'])>0 for r in all_requested))
    else:
        assert cert['kind']=='Farkas'
        lam=list(map(Q,cert['lambda']));mu=list(map(Q,cert['nonnegative_new_multipliers']))
        assert len(lam)==len(rows) and len(mu)==n and min(lam)>=0 and min(mu)>=0
        assert sum(lam,Q())==1
        combined=defaultdict(Q)
        for a,r in zip(lam,rows):
            if a:
                for j,v in r.items():combined[j]+=a*v
        for j,v in enumerate(mu,4849):combined[j]+=v
        assert all(combined[j]==0 for j in range(4849,4849+n))
        oldrow={j:v for j,v in combined.items() if j<4849 and v}
        assert sparse(oldrow)==cert['old_necessary_row']
        value=evaluate(oldrow,w);assert value<0 and str(value)==cert['old_point_value']
        neg=json.loads((HERE/'necessary_negative_row.json').read_bytes())
        assert neg['row']==sparse(oldrow) and neg['value']==str(value)
        report.update(all_multipliers_nonnegative=True,all_new_columns_eliminated=True,
                      old_necessary_row=sparse(oldrow),old_point_value=str(value),old_point_value_float=float(value),
                      positive_lambda_count=sum(v>0 for v in lam),positive_nonnegative_new_count=sum(v>0 for v in mu))
    report['passed']=True
    (HERE/'independent_certificate_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='old_necessary_row'},ensure_ascii=False))

if __name__=='__main__':main()
