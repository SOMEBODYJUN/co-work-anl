"""Static artifact checks only: do not rerun original or synthetic arithmetic."""
import ast
from hashlib import sha256
import json
from pathlib import Path
import re

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
PEER=HERE.parent/'fresh-arbitrary-reply-probe-program'
BODY=ROOT/'archives/customer-attraction/state/计算/单背景主题两人回复图的随机探针报告--计算.md'
RECEIPT=ROOT/'cleanup/workspaces/Boss7/receipts-round14/369a02858830364f3155.json'

def fp(p):
    b=p.read_bytes();return {'path':str(p.relative_to(ROOT)),'bytes':len(b),'sha256':sha256(b).hexdigest()}

def read(p):return json.loads(p.read_bytes())

def main():
    assert __debug__
    manifest=read(HERE/'source-manifest.json')
    for record in manifest['bound_files']:assert fp(ROOT/record['path'])==record
    raw=read(HERE/'original/fresh_arbitrary_probe.json')
    contract=read(HERE/'data-contract.json')
    assert raw==contract['original_fields']=={'q':7,'cases':12000,'background_repetitions':1,'feasible':12000,'best':0.0,'seconds':32.25970125198364}
    meanings=contract['all_six_field_interpretations']
    assert [x['field'] for x in meanings]==list(raw)
    assert all(x['saved_value']==raw[x['field']] and x['meaning'] for x in meanings)
    domain=contract['decoded_report_domain']
    assert domain['customer_types']==127 and domain['total_IC_rows']==48
    assert domain['last_IC_rows']==42 and domain['first_IC_rows']==6
    assert domain['reply_maps_with_fixed_rA_B']==117649 and domain['draws_with_replacement']==12000
    assert domain['historical_seed'] is None and domain['distinct_sample_count'] is None
    assert contract['source_AST']['best_store_count']==1
    assert not contract['source_AST']['historical_seed_in_report'] and not contract['source_AST']['defaults_are_historical_seed_evidence']
    for key in ('current_original_function_calls','current_original_main_calls','current_original_AST_arithmetic_executions','current_LP_calls','current_random_draws'):assert contract[key]==0
    shared=read(PEER/'cone-contract-audit.json');event=read(PEER/'audit-execution.json')
    assert shared['status']=='PASS_SYNTHETIC_CONE_ARITHMETIC_AND_EXACT_CERTIFICATE_MAPPING'
    assert shared['synthetic_inputs']=={'q':7,'L':1,'seed':0,'reply':[6,2,6,3,0,2,4]}
    assert shared['columns']==127 and shared['IC_rows']==48
    assert shared['utility_entries_checked']==6223 and shared['row_coefficients_checked']==6096 and shared['objective_entries_checked']==127
    assert len(shared['row_labels'])==len(shared['exact_rows'])==48
    assert all(len(row)==127 for row in shared['exact_rows'])
    assert len(shared['exact_objective'])==127
    assert [row['mask'] for row in shared['exact_nonnegative_remainders']]==list(range(1,128))
    assert [row['row'] for row in shared['four_multipliers']]==[43,42,8,9]
    for row in shared['four_multipliers']:assert row['label']==shared['row_labels'][row['row']]
    assert shared['universal_feasible_type']=={'mask':127,'weight':'1','all_IC_slacks':'0','objective':'2/3'}
    assert shared['historical_sampling_reconstructed'] is False and shared['new_universal_certificate_discovery'] is False
    assert shared['original_AST_arithmetic_executions']==event['original_AST_arithmetic_executions']==1
    assert shared['original_function_calls']==shared['original_main_calls']==shared['LP_calls']==0
    assert event['exit_code']==0 and event['original_run_calls']==event['original_main_calls']==event['LP_calls']==0
    assert event['report_sha256']==fp(PEER/'cone-contract-audit.json')['sha256']
    assert event['auditor_sha256']==shared['auditor_sha256']==fp(PEER/'audit_cone_contract.py')['sha256']
    assert shared['source_sha256']==fp(PEER/'original/probe_fresh_arbitrary_reply.py')['sha256']
    receipt=read(RECEIPT)
    assert receipt['id']=='369a02858830364f3155' and receipt['disposition']=='integrated'
    assert all(receipt[k] is True for k in ('full_file_reviewed','related_material_checked','unique_content_accounted_for'))
    for target in receipt['targets']:assert (ROOT/target).is_file() or ROOT/target==HERE/'self-check.json'
    links=[]
    for doc in (BODY,HERE/'README.md'):
        for link in re.findall(r'\]\(([^)]+)\)',doc.read_text()):
            if link.startswith(('https:','http:','#','source:')):continue
            target=(doc.parent/link.split('#',1)[0]).resolve()
            assert target.is_file() or target==HERE/'self-check.json',(str(doc),link)
            links.append({'from':str(doc.relative_to(ROOT)),'link':link,'target':str(target.relative_to(ROOT))})
    scripts=[HERE/'inspect_report.py',HERE/'check_package.py',PEER/'original/probe_fresh_arbitrary_reply.py',PEER/'audit_cone_contract.py']
    for p in scripts:ast.parse(p.read_bytes())
    json_paths=list(HERE.rglob('*.json'))
    for p in json_paths:read(p)
    inventory=sorted(p for p in HERE.rglob('*') if p.is_file() and p.name!='self-check.json')+[BODY,RECEIPT]
    result={'status':'PASS_STATIC_REPORT_PACKAGE','scope':'preserved field/source bindings, shared report structure and provenance, links and receipt; no coefficient reconstruction, original calls, random draws or LPs',
      'bound_files_checked':len(manifest['bound_files']),'original_fields_checked':6,'shared_IC_matrix_shape':[48,127],'shared_remainder_records':127,
      'shared_synthetic_AST_events':1,'shared_original_run_events':0,'shared_original_main_events':0,'shared_LP_events':0,
      'current_original_calls':0,'current_AST_arithmetic_executions':0,'current_synthetic_audit_calls':0,'current_LP_calls':0,'current_random_draws':0,
      'python_AST_files':len(scripts),'own_json_files_parsed':len(json_paths),'receipt_targets':len(receipt['targets']),'local_links_checked':len(links),'links':links,'files':[fp(p) for p in inventory]}
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
