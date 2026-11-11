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
    report={'scope':'Exact verification of the complete single-query envelope lift; common realization and full SPE remain unproved.',
            'point_sha256':sha(POINT),'symbolic_lift_sha256':sha(HERE/'symbolic_lift.json.gz'),
            'literal_preflight_sha256':sha(HERE/'preflight_literal_audit.json'),
            'certificate_sha256':sha(HERE/'exact_certificate.json'),'verifier_sha256':sha(Path(__file__)),
            'old_columns':4849,'new_columns':n,'rows':len(rows),'kind':cert['kind'],
            'optimization_calls':0,'zero_histograms_preserved':audit['zero_mass_histograms']}
    if cert['kind']=='primal':
        x=list(map(Q,cert['new_values']));assert len(x)==n and min(x)>=0
        assert cert['E_values']==list(map(str,x[:776]))
        assert cert['canonical_min_values']==list(map(str,x[776:]))
        values=w+x
        for i,c in enumerate(lift['new_columns'][776:]):
            assert x[776+i]==min(evaluate(decode(c['a']),values),evaluate(decode(c['b']),values))
        slacks=[evaluate(r,values) for r in rows]
        assert min(slacks)>=0 and list(map(str,slacks))==cert['row_slacks']
        report.update(all_rational_new_values_checked=True,all_canonical_mins_checked=True,
                      all_rows_nonnegative=True,minimum_slack=str(min(slacks)),
                      positive_E_values=sum(v>0 for v in x[:776]),exact_phase_I='0')
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
