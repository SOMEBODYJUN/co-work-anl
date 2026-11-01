"""Static bindings and saved-event checks; never import/run the original entry."""
import ast
from hashlib import sha256
import json
from pathlib import Path
import re

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
DEPS=HERE.parent/'deletion-security-probe-program/dependencies'
BODY=ROOT/'archives/customer-attraction/state/程序/固定反组策略的终局删除查询探针--程序.md'
RECEIPT=ROOT/'cleanup/workspaces/Boss7/receipts-round15/54ba59fc852a4f5ee5b9.json'

def fp(p):
    b=p.read_bytes();return {'path':str(p.relative_to(ROOT)),'bytes':len(b),'sha256':sha256(b).hexdigest()}

def read(p):return json.loads(p.read_bytes())

def main():
    assert __debug__
    manifest=read(HERE/'source-manifest.json')
    for x in manifest['bound_files']:assert fp(ROOT/x['path'])==x
    event=read(HERE/'original-event/execution.json');contract=read(HERE/'contract-audit.json')
    assert event['exit_code']==0 and event['original_top_level_executions']==1
    assert event['LP_invocations_if_normal_completion']==22 and not event['entry_was_overwritten_by_original_output']
    assert event['preserved_post_entry_file'] is None
    assert event['deletion_probe_executions']==event['tax_probe_main_executions']==event['ExactSPESolver_calls']==0
    assert contract['actual_model']=={'n':3,'k':6,'mask_interval':[1,63],'customer_variables':63,'auxiliary_t_variables':1,'normalized_customer_mass':'sum w=1','policy':'fixed opposite-group rule on all ordered histories','decision_histories':43,'IC_rows':258,'self_IC_rows':43,'nonself_IC_rows':215,'root':[0,3,4]}
    queries=contract['LP_contract']['query_distributions'];assert len(queries)==22 and [q['index'] for q in queries]==list(range(22))
    assert [sum(q['family']==family for q in queries) for family in ('pure','uniform_pair','uniform_all')]==[6,15,1]
    assert contract['LP_contract']['variables']==64 and contract['LP_contract']['inequality_rows_per_LP']==261
    assert contract['candidate_output']['self_overwrite_if_positive'] and not contract['candidate_output']['branch_taken_in_recorded_event']
    assert not contract['candidate_output']['candidate_saved'] and not contract['saved_event']['best_query_and_weights_saved']
    assert contract['saved_event']['stdout']==(HERE/'original-event/stdout.txt').read_text()
    assert (HERE/'original-event/stderr.txt').read_bytes()==b''
    assert contract['saved_event']['best_float_lexeme']=='-0.08333333333333315'
    for r in event['input_files']:
        assert r['before']==r['after']
        p=HERE/'original/deletion_36.py' if r['runtime_path']=='deletion_36.py' else DEPS/r['runtime_path']
        assert {k:fp(p)[k] for k in ('bytes','sha256')}==r['before']
    for key,name in [('stdout','stdout.txt'),('stderr','stderr.txt')]:
        assert {k:fp(HERE/'original-event'/name)[k] for k in ('bytes','sha256')}==event[key]
    assert all(contract[k]==0 for k in ('current_original_entries','current_helper_calls','current_LP_calls','current_coefficient_reconstruction'))
    receipt=read(RECEIPT);assert receipt['id']=='54ba59fc852a4f5ee5b9' and receipt['disposition']=='integrated'
    assert all(receipt[k] is True for k in ('full_file_reviewed','related_material_checked','unique_content_accounted_for'))
    for target in receipt['targets']:assert (ROOT/target).is_file() or ROOT/target==HERE/'self-check.json'
    links=[]
    for doc in (BODY,HERE/'README.md'):
        for link in re.findall(r'\]\(([^)]+)\)',doc.read_text()):
            if link.startswith(('https:','http:','#','source:')):continue
            target=(doc.parent/link.split('#',1)[0]).resolve()
            assert target.is_file() or target==HERE/'self-check.json',(str(doc),link)
            links.append({'from':str(doc.relative_to(ROOT)),'link':link,'target':str(target.relative_to(ROOT))})
    scripts=sorted(HERE.rglob('*.py'))+sorted(DEPS.rglob('*.py'))
    for p in scripts:ast.parse(p.read_bytes())
    json_paths=sorted(HERE.rglob('*.json'))
    for p in json_paths:read(p)
    inventory=sorted(p for p in HERE.rglob('*') if p.is_file() and p.name!='self-check.json')+[BODY,RECEIPT]
    result={'status':'PASS_STATIC_PROGRAM_PACKAGE','scope':'file/source hashes, completed original event, saved AST contract, shared dependencies, links and receipt; no original entry or mathematical optimization rerun',
      'bound_files_checked':len(manifest['bound_files']),'shared_dependencies_checked':len(manifest['shared_dependencies']),'original_event_count':1,'normal_completion_LP_calls_in_recorded_event':22,'LP_count_is_solver_trace':False,
      'current_original_entry_calls':0,'current_helper_calls':0,'current_LP_calls':0,'source_self_overwrite_branch_taken':False,
      'saved_queries_checked':22,'python_AST_files':len(scripts),'own_JSON_files_parsed':len(json_paths),'local_links_checked':len(links),'receipt_targets':len(receipt['targets']),'links':links,'files':[fp(p) for p in inventory]}
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
