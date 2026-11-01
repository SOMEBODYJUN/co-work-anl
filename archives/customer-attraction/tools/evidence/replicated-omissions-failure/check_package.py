"""Static identity and saved-result checks; no terminal payoff, DP or LP recomputation."""
import ast
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import re

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
DOC=ROOT/'archives/customer-attraction/state/障碍/复制遗漏客户池的末两人严格偏离障碍--障碍.md'
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def binding(p):return dict(path=str(p.relative_to(ROOT)),bytes=p.stat().st_size,sha256=sha(p))
manifest=load(HERE/'source-manifest.json')
for row in manifest['primary_sources']:
    p=HERE/row['preserved_as']
    assert p.stat().st_size==row['size'] and sha(p)==row['sha256']
related={'d6cb467c51e97a499f39':HERE.parent/'credible-padding-theory/original/all_k_padding.md',
         '6f957bfb27488f5b01db':HERE.parent/'credible-padding-program/original/all_k_padding.py'}
for row in manifest['related_sources_read']:
    p=related[row['id']]
    assert p.stat().st_size==row['size'] and sha(p)==row['sha256']
for row in manifest['formal_comparisons']:
    p=ROOT/row['path']
    assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256']
source=load(HERE/'original/replicated_k17_direct_audit.json')
report=load(HERE/'direct-audit.json')
execution=load(HERE/'execution.json')
assert len(source)==13 and set(source)==set(report['source_fields'])
assert report['source_sha256']==sha(HERE/'original/replicated_k17_direct_audit.json')
assert report['source_bytes']==1412
assert execution['exit_code']==0 and execution['script_sha256']==sha(HERE/'audit_direct.py')
assert (HERE/'stderr.txt').read_bytes()==b''
assert report['status']=='PASS_EXACT_DIRECT_TERMINAL_TABLE'
assert report['independent_audit_entries']==1
assert report['original_program_entries']==report['DP_calls']==report['LP_calls']==0
assert len(report['topics'])==len(set(report['topics']))==54
assert len(report['customers'])==report['unit_customers']==203
assert [x['id'] for x in report['customers']]==list(range(203))
assert all(set(x['likes'])<=set(report['topics']) and x['likes'] for x in report['customers'])
assert report['players']==source['players']==20
assert report['k']==report['pools']==source['k']==source['pools']==17
assert len(report['last_reply_rows'])==54
assert {x['last_action']:x['last_payoff'] for x in report['last_reply_rows']}==source['last_action_values']
assert report['all_last_best_replies']==source['all_last_best_replies']==['T'+str(j) for j in range(1,17)]
assert len(report['deviator_payoffs_for_every_best_reply'])==16
assert {x['last_action'] for x in report['deviator_payoffs_for_every_best_reply']}==set(source['all_last_best_replies'])
assert all(x['payoff']=='7' for x in report['deviator_payoffs_for_every_best_reply'])
assert report['best_reply_payoff']==source['last_best_reply_payoff']=='6'
assert report['proposed_current_payoff']=='5' and report['strict_deviation_gain']=='2'
assert report['proposed_player_payoffs']==['5']*19+['6']
assert len(report['OPT_certificate']['actions'])==20
assert report['formal_path_welfare']==source['formal_path_welfare']==101
assert report['formal_OPT']==source['formal_optimum']==report['OPT_certificate']['covered']==203
assert report['formal_half_deficit']==source['formal_half_violation']==1
for row in report['last_reply_rows']:
    F(row['last_payoff']);F(row['deviator_payoff'])
stdout=load(HERE/'stdout.txt')
assert all(report[k]==v for k,v in stdout.items())
receipts=[]
for uid in ['e828f5d0e87a440be274','90e1e51f8ab1cd80dd62']:
    p=ROOT/f'cleanup/workspaces/Boss7/receipts-round18/{uid}.json'
    receipt=load(p)
    assert receipt['id']==uid and receipt['disposition']=='integrated'
    assert all(receipt[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
    assert receipt['targets']==[str(DOC.relative_to(ROOT))]
    receipts.append(p)
links=[]
for p in [DOC,HERE/'README.md']:
    for href in re.findall(r'\[[^\]]*\]\(([^)]+)\)',p.read_text()):
        if href.startswith(('https:','http:','#','source:')):continue
        target=(p.parent/href.split('#')[0]).resolve()
        assert target.exists(),(str(p),href)
        links.append(dict(source=str(p.relative_to(ROOT)),target=str(target.relative_to(ROOT))))
files=sorted(p for p in HERE.rglob('*') if p.is_file() and p.name!='self-check.json')
ast_count=json_count=0
for p in files+receipts:
    if p.suffix=='.py':ast.parse(p.read_text());ast_count+=1
    if p.suffix=='.json':load(p);json_count+=1
result=dict(status='PASS_STATIC_ONLY',scope='Saved source/report bytes, record structure, exact string agreement, AST/JSON, links and both receipts; no new payoff evaluation, original entry, DP or LP.',
            primary_source_bindings=2,related_source_bindings=2,formal_comparison_bindings=4,
            source_JSON_top_fields=13,last_action_rows=54,best_reply_rows=16,unit_customer_records=203,
            python_ast_files=ast_count,json_files=json_count,local_links=len(links),links=links,
            artifacts=[binding(p) for p in files+[DOC]+receipts],self_hash_excluded=True,new_mathematical_runs=0)
(HERE/'self-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','python_ast_files','json_files','local_links','new_mathematical_runs']}))
