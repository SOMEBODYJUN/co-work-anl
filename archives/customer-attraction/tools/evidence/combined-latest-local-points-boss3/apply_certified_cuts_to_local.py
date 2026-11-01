"""Apply already certified common-coordinate sparse cuts to the new local point.

No cut is reconstructed from a hidden model; no original row helper or LP is run.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import json,hashlib,sys
HERE=Path(__file__).resolve().parent
def meta(c):return {k:v for k,v in c.items() if k!='weight'}
def main():
    if len(sys.argv)!=2:raise SystemExit('usage: apply_certified_cuts_to_local.py /absolute/repository')
    repo=Path(sys.argv[1]);root=repo/'archives/customer-attraction/tools/evidence/requery-capacity-cut-packs-boss3'
    sparse_path=root/'runs/all-sparse-row-coefficients.json';audit_path=root/'runs/exact-cut-audit.json'
    sparse=json.loads(sparse_path.read_text());old_audit=json.loads(audit_path.read_text())
    lookup={(r['pack'],r['field'],c['number']):(r,c) for r in old_audit['reports'] for c in r['rows']}
    latest=json.loads((HERE/'original/combined_branch_latest_exact.json').read_text())
    local_raw=(HERE/'original/combined_branch_local_exact.json').read_bytes();local=json.loads(local_raw)
    parent_latest=root/'original/research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_5/combined_branch_latest_exact.json'
    assert parent_latest.read_bytes()==(HERE/'original/combined_branch_latest_exact.json').read_bytes()
    assert len(latest['columns'])==len(local['columns'])==1905
    assert [meta(c) for c in latest['columns']]==[meta(c) for c in local['columns']]
    ys=[F(c['weight']) for c in local['columns']]
    dep=repo/'archives/customer-attraction/tools/evidence/combined-branch-master-program/dependencies/research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_5/joint_local_cuts.json'
    included_requery=json.loads(dep.read_text())['requery']
    results=[]
    for rec in sparse:
        assert rec['length'] in (1905,2033)
        indices=[j for j,v in rec['nonzero']];assert len(indices)==len(set(indices)) and all(0<=j<1905 for j in indices)
        full=[F()]*rec['length']
        for j,v in rec['nonzero']:full[j]=F(v)
        assert all(full[j] for j in indices)
        fingerprint=hashlib.sha256(json.dumps(list(map(str,full)),separators=(',',':')).encode()).hexdigest()
        assert fingerprint==rec['row_sha256']
        parent,entry=lookup[rec['pack'],rec['field'],rec['number']]
        value=sum((F(v)*ys[j] for j,v in rec['nonzero']),F())
        results.append({'pack':rec['pack'],'field':rec['field'],'number':rec['number'],'row_sha256':fingerprint,'original_coordinate_length':rec['length'],'extra_tail_coefficients_verified_zero':rec['length']-1905,
          'original_bound_point':parent['source'],'original_bound_point_sha256':parent['point_sha256'],
          'original_reported_and_previously_checked_slack':entry['slack'],'local5189_slack':str(value),'cut':entry['cut'],
          'included_by_exact_local_requery_parameter_identity':parent['kind']=='requery' and entry['cut'] in included_requery})
    groups={}
    for pack in sorted({r['pack'] for r in results}):
        rr=[r for r in results if r['pack']==pack]
        neg=[r for r in rr if F(r['local5189_slack'])<0]
        groups[pack]={'records':len(rr),'negative_records':len(neg),'zero_records':sum(F(r['local5189_slack'])==0 for r in rr),
          'positive_records':sum(F(r['local5189_slack'])>0 for r in rr),'distinct_negative_vectors':len({r['row_sha256'] for r in neg}),
          'included_local_requery_records':[r['number'] for r in rr if r['included_by_exact_local_requery_parameter_identity']]}
    report={'status':'existing certified sparse rows applied to a new exact vector','new_point_filename':'combined_branch_local_exact.json',
      'new_point_sha256':hashlib.sha256(local_raw).hexdigest(),'all_1905_descriptors_equal_parent_bound_latest':True,
      'certified_sparse_file':str(sparse_path.relative_to(repo)),'certified_sparse_sha256':hashlib.sha256(sparse_path.read_bytes()).hexdigest(),
      'previous_audit_file':str(audit_path.relative_to(repo)),'previous_audit_sha256':hashlib.sha256(audit_path.read_bytes()).hexdigest(),
      'cut_derivations_repeated':False,'row_helper_calls':0,'optimizer_calls':0,'groups':groups,'results':results,
      'limits':'Finite new-point applications of previously certified vectors. Original slacks retain their original bound input; no full closure, SPE, optimum or whole-system infeasibility.'}
    (HERE/'replay/certified-cuts-at-local5189.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='results'},ensure_ascii=False))
if __name__=='__main__':main()
