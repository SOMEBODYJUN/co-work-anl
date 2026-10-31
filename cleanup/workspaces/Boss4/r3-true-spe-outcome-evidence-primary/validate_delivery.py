from pathlib import Path
from itertools import product
import hashlib,json,re

S=Path(__file__).resolve().parents[4]
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
E=S/'archives/customer-attraction/tools/evidence/true-spe-outcome-evidence-primary'
W=S/'cleanup/workspaces/Boss4/r3-true-spe-outcome-evidence-primary'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source=json.loads((E/'source-manifest.json').read_text())
assert source['primary_count']==5 and source['unique_raw_paths']==12
checked=[]
for x in source['sources']:
    f=S/x['saved_path']
    assert f.stat().st_size==x['size'] and sha(f)==x['sha256'],x['path']
    if 'runtime_path' in x:
        assert (S/x['runtime_path']).read_bytes()==f.read_bytes()
    assert len(x['sources'])==2 and all(z['bytes_verified'] for z in x['sources'])
    checked.append(x['id'])
assert len(set(checked))==12
claim=json.loads((W/'claim-observation.json').read_text())
assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync_status']=='synced'
assert sha(W/'claim-receipt.json')==claim['capture_sha256']
receipts=json.loads((W/'semantic-receipts.json').read_text())
assert len(receipts)==5 and {x['id'] for x in receipts}==set(claim['claimed_primary_ids'])
assert sum(x['disposition']=='duplicate' for x in receipts)==3
for x in receipts:
    assert all(x[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
    assert all(x[k] for k in ['read_note','comparison_note','decision_note'])
    for target in x['targets']:assert (S/target).is_file() or (R/target).is_file(),target
for rec in claim['local_HEAD_owners']:
    assert rec['record']['owner']=='Boss4' and rec['record']['disposition']=='in-progress'
    src=next(x for x in source['sources'] if x['id']==rec['id'])
    assert rec['record']['source_sha256']==src['sha256']
for x in json.loads((E/'reused-evidence.json').read_text())['evidence']:
    assert sha(R/x['path'])==x['sha256']
for x in json.loads((E/'related-material.json').read_text())['full_related_objects']:
    assert sha(R/x['path'])==x['sha256']
exe=json.loads((E/'replay-large-baseline/execution.json').read_text())
assert exe['returncode']==0 and exe['original_entry_runs_this_batch']==1
assert exe['original_milp_calls']==1 and exe['exact_fixed_cone_lp_calls']==0
assert exe['stderr_bytes']==0 and not (E/'replay-large-baseline/stderr.txt').read_bytes()
assert len(exe['json_differences'])==1 and exe['json_differences'][0]['pointer']=='/milp/seconds'
assert not exe['byte_identical']
assert sha(E/'replay-large-baseline/dag_baseline_fixed_m5p7.json')==exe['new_report_sha256']
baseline=json.loads((E/'replay-large-baseline/dag_baseline_fixed_m5p7.json').read_text())
assert baseline['exact_full_history_verified'] and baseline['ordered_history_nodes']==2801
assert baseline['exact_deviation_checks']==16806 and (baseline['welfare'],baseline['optimal_welfare'],baseline['ratio'])==(5,9,'9/5')
ind=json.loads((E/'independent-baseline-review.json').read_text())
assert ind['status']=='pass' and ind['solver_calls']==0 and ind['new_independent_script_runs']==1
assert ind['comparisons_including_self']==19607 and ind['comparisons_excluding_self']==16806
assert ind['complete_ordered_decision_histories']==2801 and ind['minimum_IC_margin']=='0'
assert not ind['seven_historical_candidate_feasibility_recertified']
pm=json.loads((E/'primary-manifest.json').read_text())['sources']
cert=json.loads((S/pm[0]['saved_path']).read_text())
actions={tuple(x['history']):x['action'] for x in cert['actions']}
assert len(actions)==85 and set(actions)=={h for d in range(4) for h in product(range(4),repeat=d)}
h=()
while len(h)<4:h+=(actions[h],)
assert [h.count(a) for a in range(4)]==cert['terminal_counts']==[1,3,0,0]
links=[]
for md in S.rglob('*.md'):
    for link in re.findall(r'\]\(([^)]+)\)',md.read_text()):
        if '://' in link or link.startswith('#'):continue
        path=(md.parent/link.split('#',1)[0]).resolve()
        rel=path.relative_to(S)
        assert path.is_file() or (R/rel).is_file(),(str(md.relative_to(S)),link)
        links.append({'from':str(md.relative_to(S)),'link':link,'target':str(rel)})
body=S/'archives/customer-attraction/state/计算/七主题固定输入基线与终局搜索版本--计算.md'
assert body.read_text().startswith('---\nid:')
report={'status':'pass','checked_primary':5,'checked_raw_sources':12,'checked_runtime_code_files_unchanged':7,
        'receipt_targets_exist':True,'published_reused_evidence_bytes_match':True,
        'published_related_objects_bytes_match':True,'markdown_links_checked':len(links),'links':links,
        'original_branch_success_and_only_seconds_change':True,'explicit_independent_policy_report_pass':True,
        'complete_85_node_original_m4_table_structure_and_root_checked':True,
        'validation_does_not_replace_mathematical_review':True,
        'new_formal_body_sha256':sha(body),'new_formal_body_bytes':body.stat().st_size}
(W/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
files=[]
for path in sorted(S.rglob('*')):
    if path.is_file() and path!=S/'copy-files.json':
        assert '__pycache__' not in path.parts
        files.append({'path':str(path.relative_to(S)),'size':path.stat().st_size,'sha256':sha(path)})
manifest={'stage_root':str(S),'manifest_is_transport_only':True,'file_count':len(files),
          'bytes':sum(x['size'] for x in files),'files':files}
(S/'copy-files.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'pass','file_count':manifest['file_count'],'bytes':manifest['bytes'],
                  'manifest_sha256':sha(S/'copy-files.json'),'manifest_bytes':(S/'copy-files.json').stat().st_size,
                  'formal_body_sha256':sha(body),'formal_body_bytes':body.stat().st_size,
                  'local_links':len(links)},ensure_ascii=False))
