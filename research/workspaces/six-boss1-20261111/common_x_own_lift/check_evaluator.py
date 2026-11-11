"""Synthetic evaluator interface checks, never a recovered or old primal point."""
from fractions import Fraction as F
from hashlib import sha256
import gzip
import json
from pathlib import Path
import evaluate_point as evaluator

HERE=Path(__file__).resolve().parent
BASE=HERE.parent


def main():
    with gzip.open(BASE/'maxb_augmented_lp/full_lift/exact_matrix.json.gz','rt',encoding='utf-8') as f:
        descriptors=json.load(f)['columns']
    layer=json.loads((HERE/'own_facets.json').read_text())
    cases=[]
    def fixture(masses,X,yq,yr):
        H=sum(masses,F()); by_state=dict(zip(('00','10','01','11'),masses)); out=[]
        for c in descriptors:
            value=F()
            if c['kind']=='hist': value=H
            elif c['kind']=='joint-reply': value=by_state[''.join(map(str,c['state']))]
            elif c['kind']=='actual-B-family-state' and c['source']==4:
                value=by_state[''.join(map(str,c['hidden']))]/2
            elif c['kind']=='common-X-mass': value=X
            elif c['kind']=='X-query-overlap-upper':
                token=c['query_token']; value=yq if token[0]=='R' or token==['H',0] else yr
            out.append({**c,'weight':str(value)})
        return dict(columns=out,scope='SYNTHETIC_LOCAL_INTERFACE_FIXTURE_NOT_A_FULL_LP_POINT')
    for name,masses,X,yq,yr in [
        ('zero_hist',(F(),)*4,F(),F(),F()),
        ('interior', (F(1),)*4,F(2),F(1),F(1)),
        ('X_empty',(F(1),)*4,F(),F(),F()),
        ('X_full',(F(1),)*4,F(4),F(2),F(2)),
        ('equal_coverage_QR',(F(1),F(),F(),F(3)),F(2),F(1),F(1)),
        ('disjoint_reselected_y',(F(),F(1,2),F(1,2),F()),F(1,2),F(1,4),F(1,4)),
    ]:
        result=evaluator.evaluate(layer,fixture(masses,X,yq,yr))
        assert result['status']=='FIXED_OWN_X_VALUES_COMPLETE'
        assert all('beta_witness' in b for b in result['blocks'])
        cases.append(dict(name=name,blocks=210,status=result['status']))
    bad=evaluator.evaluate(layer,fixture((F(),F(1,2),F(1,2),F()),F(1,2),F(1,2),F(1,2)))
    assert bad['summary']['negative_facet_counts']=={'O6':210}
    assert bad['summary']['empty_beta_intervals']==210 and bad['summary']['base_precondition_failures']==0
    cases.append(dict(name='disjoint_canonical_fixed_y_failure',blocks=210,status=bad['status']))
    badmass=fixture((F(1),)*4,F(2),F(1),F(1))
    badmass['columns'][2673]['weight']='3/2'
    result=evaluator.evaluate(layer,badmass)
    assert result['summary']['base_precondition_failures']==1
    assert result['failed_blocks']==[19] and result['blocks'][19]['mass_identity_residual']=='1'
    cases.append(dict(name='B4_old_mass_equality_is_required',blocks=210,status=result['status']))
    rejected=0
    for badval in (1.0,True,'0.25','nan','1/0',None):
        try: evaluator.exact(badval)
        except (ValueError,TypeError): rejected+=1
        else: raise AssertionError('Inexact value accepted')
    for badpoint in (dict(columns=badmass['columns'][:20585]),dict(columns=[{**c,'kind':'wrong'} if j==0 else c
                                                                          for j,c in enumerate(badmass['columns'])])):
        try: evaluator.evaluate(layer,badpoint)
        except ValueError: rejected+=1
        else: raise AssertionError('Wrong coordinates accepted')
    report=dict(status='SYNTHETIC_FUTURE_POINT_EVALUATOR_PASS',cases=cases,
                local_blocks_evaluated=210*len(cases),invalid_input_rejections=rejected,
                actual_primal_point_reads=0,LP_calls=0,
                evaluator_sha256=sha256((HERE/'evaluate_point.py').read_bytes()).hexdigest(),
                checker_sha256=sha256(Path(__file__).read_bytes()).hexdigest())
    (HERE/'evaluator_verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False))


if __name__=='__main__': main()
