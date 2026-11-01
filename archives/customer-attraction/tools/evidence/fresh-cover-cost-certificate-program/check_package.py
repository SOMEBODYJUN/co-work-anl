"""Static delivery validation only: no source imports, LP or matrix audit."""
import ast
from hashlib import sha256
import json
from pathlib import Path
import re
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[4]
BODY=REPO/'archives/customer-attraction/state/程序/背景旧覆盖付款的系数证书搜索程序--程序.md'
RECEIPT=REPO/'cleanup/workspaces/Boss7/receipts-round14/b634158696869226b89c.json'
def digest(p):return sha256(p.read_bytes()).hexdigest()
def check_records(rows):
    for rec in rows:
        path=REPO/rec['path']
        assert path.stat().st_size==rec['bytes'] and digest(path)==rec['sha256'],str(path)
def main():
    artifact=json.loads((HERE/'artifact-manifest.json').read_text());check_records(artifact['files'])
    shared=json.loads((HERE/'shared-audit-binding.json').read_text());check_records(shared['files'])
    comparisons=json.loads((HERE/'comparison-manifest.json').read_text());check_records(comparisons['formal_objects'])
    source=json.loads((HERE/'source-manifest.json').read_text())
    for rec in source['sources']:
        path=HERE/rec['preserved_path'];assert path.stat().st_size==rec['source']['size'] and digest(path)==rec['source']['sha256']
    json_count=0;ast_count=0
    for path in list(HERE.rglob('*'))+[RECEIPT]:
        if not path.is_file():continue
        if path.suffix=='.json':json.loads(path.read_bytes());json_count+=1
        if path.suffix=='.py':ast.parse(path.read_bytes());ast_count+=1
    links=[]
    # Historical source README links describe its frozen workspace, not this package.
    for path in [BODY,HERE/'README.md']:
        for target in re.findall(r'\]\(([^)]+)\)',path.read_text()):
            if target.startswith(('https:','http:','#')):continue
            resolved=(path.parent/target.split('#',1)[0]).resolve()
            assert resolved.exists(),(str(path),target)
            links.append({'from':str(path.relative_to(REPO)),'target':str(resolved.relative_to(REPO))})
    event=json.loads((HERE/'replay/execution.json').read_text())
    assert event['returncode']==0 and event['original_script_invocations']==event['original_linprog_calls']==1
    assert event['source_before']==event['source_after'] and event['new_report_equals_frozen_bytes']
    assert event['original_success_branch_executed'] is False
    for name,rec in event['files'].items():
        p=HERE/'replay'/name
        assert p.stat().st_size==rec['bytes'] and digest(p)==rec['sha256']
    report=HERE/'replay/fresh_cover_cost_2.json'
    assert report.read_bytes()==(HERE/'replay/stdout.txt').read_bytes()
    data=HERE.parent/'fresh-cover-cost-certificate-data'
    assert report.read_bytes()==(data/'original/fresh_cover_cost_2.json').read_bytes()
    exact=json.loads((data/'exact-audit.json').read_text())
    assert exact['rows']==192 and exact['columns']==24 and exact['paired_target']=='-6'
    assert exact['exact_coefficient_comparisons']==4608 and len(exact['integer_farkas_support'])==8
    assert exact['tau1_certificate']['zero_residuals']==40 and exact['tau1_certificate']['positive_residuals']==152
    assert exact['LP_calls']==exact['original_module_or_helper_calls']==0
    receipt=json.loads(RECEIPT.read_text())
    assert receipt['id']=='b634158696869226b89c' and receipt['disposition']=='integrated'
    for key in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']:assert receipt[key] is True
    for p in receipt['targets']:assert (REPO/p).is_file(),p
    result={'status':'PASS_STATIC_PACKAGE','artifact_bound_files':len(artifact['files']),'shared_bound_files':len(shared['files']),'comparison_bound_files':len(comparisons['formal_objects']),'json_parsed':json_count,'python_ast_parsed':ast_count,'markdown_links':len(links),'receipt_targets':len(receipt['targets']),'source_bytes':2041,'default_new_report_bytes':148,'exact_audit_sha256':digest(data/'exact-audit.json'),'new_mathematical_execution':False,'historical_source_readme_links':'preserved relative references; not delivery-navigation links','links':links}
    (HERE/'self-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='links'},indent=2))
if __name__=='__main__':main()
