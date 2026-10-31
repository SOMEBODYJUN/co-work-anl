from pathlib import Path
from fractions import Fraction as F
import hashlib,json,re

S=Path(__file__).resolve().parents[4];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
E=S/'archives/customer-attraction/tools/evidence/full-tree-milp-candidate-audits-primary'
W=S/'cleanup/workspaces/Boss4/r3-full-tree-milp-candidate-audits-primary'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source=json.loads((E/'source-manifest.json').read_text());raw=source['sources']
assert len(raw)==24 and len({x['path'] for x in raw})==24 and sum(x['size'] for x in raw)==357249
for x in raw:
    p=S/x['saved_path'];assert p.stat().st_size==x['size'] and sha(p)==x['sha256']
    assert len(x['sources'])==2 and all(z['bytes_verified'] for z in x['sources'])
tree=json.loads((E/'runtime-tree-manifest.json').read_text())
assert len(tree['sources'])==15 and tree['code_files']==7 and tree['input_files']==8
for x in tree['sources']:assert sha(E/'replay-tree'/x['path'])==x['sha256']
cap=json.loads((W/'claim-receipt.json').read_text());obs=json.loads((W/'claim-observation.json').read_text())
assert cap['status']=='pushed' and cap['actor']=='Boss4' and cap['local_sync']['status']=='synced'
assert len(cap['ids'])==25 and obs['actual_merged_claim_ids']==cap['ids']
assert sha(W/'claim-receipt.json')==obs['capture_sha256']
expected=obs['expected_worker_subset'];intersection=[i for i in expected if i in set(cap['ids'])]
assert intersection==obs['claimed_primary_ids'] and len(intersection)==5 and not obs['missing_expected_ids']
assert all(z['record']['owner']=='Boss4' and z['record']['disposition']=='in-progress' for z in obs['local_HEAD_owners'])
receipts=json.loads((W/'semantic-receipts.json').read_text())
assert len(receipts)==5 and {x['id'] for x in receipts}==set(intersection)
for x in receipts:
    assert x['disposition']=='integrated'
    assert all(x[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
    assert all(x[k] for k in ['read_note','comparison_note','decision_note'])
    assert all((S/p).is_file() for p in x['targets'])
audit=json.loads((E/'replay-audit/execution.json').read_text());mip=json.loads((E/'replay-milp/execution.json').read_text())
assert audit['returncode']==mip['returncode']==0
assert audit['original_main_runs_this_batch']==mip['original_main_runs_this_batch']==1
assert not mip['timed_out'] and audit['fixed_cone_LP_calls_completed']==14 and audit['raw_observed_line_events']==28
assert audit['byte_identical'] and audit['json_identical'] and audit['output_bytes']==134039
assert sha(E/'replay-audit/exact_candidate_audit.json')==audit['output_sha256']==audit['frozen_sha256']
for name in ['audit','milp']:assert not (E/f'replay-{name}/stderr.txt').read_bytes()
duals=json.loads((E/'replay-audit/replayed-exact-duals.json').read_text())['records']
events=json.loads((E/'replay-audit/observed-exact-duals.json').read_text())['records']
assert len(duals)==14 and len(events)==28 and all(events[i]==events[i+1] for i in range(0,28,2))
for i,d in enumerate(duals):
    assert {k:v for k,v in d.items() if k!='raw_observer_event_indices'}==events[2*i]
    assert d['raw_observer_event_indices']==[2*i,2*i+1]
result=json.loads((E/'independent-exact-review.json').read_text())
assert result['status']=='pass' and result['new_independent_script_runs']==1 and result['optimizer_calls']==0
assert not result['imports_original_or_canonical'] and result['gap_distinct_dual_certificates_replayed']==14
assert (result['gap_points_nodes'],result['gap_points_including_self_comparisons'],result['gap_points_nonself_comparisons'])==(796,3919,3123)
assert (result['terminal_points_nodes'],result['terminal_points_including_self_comparisons'],result['terminal_points_nonself_comparisons'])==(42,168,126)
terminal=result['terminal_comparison_points'][0]
assert terminal['distinct_coverages']==4 and terminal['C1_slack']=='-1/2' and terminal['C2_slack']=='0'
assert terminal['root_path_count']==26 and terminal['W']==terminal['OPT']==7
assert all(x['independent_exact_dual_replay'] for x in result['gap_exact_points'])
assert all(x['independent_exact_dual_replay'] is None for x in result['terminal_comparison_points'])

comput=S/'archives/customer-attraction/state/计算/自由终局逐人归一模型的候选与对偶复核--计算.md'
table=[]
for line in comput.read_text().splitlines():
    match=re.fullmatch(r'\| (\d+) \| (\d+) \| (.*?) \|',line)
    if not match:continue
    i,n,items=match.groups();support=[]
    if items!='空':
        for entry in items.split('，'):
            row,value=entry.split(':');support.append([int(row),str(F(value))])
    table.append((int(i),int(n),support))
assert len(table)==14
for i,n,support in table:
    assert n==duals[i]['rows_count'] and support==duals[i]['dual_support']
counter=S/'archives/customer-attraction/state/反例/逐人末位二倍保底的七客户反例--反例.md'
last={tuple(x['history']):[F(z['payoff']) for z in x['alternatives']] for x in terminal['all_node_comparisons'] if len(x['history'])==2}
seen=set()
for line in counter.read_text().splitlines():
    match=re.fullmatch(r'\| ([0-3]{2}(?:、[0-3]{2})*) \| \(([^)]+)\) \|',line)
    if not match:continue
    hs,values=match.groups();values=[F(v) for v in values.split(',')]
    for h in hs.split('、'):
        key=tuple(map(int,h));assert last[key]==values;seen.add(key)
assert len(seen)==16
related=json.loads((E/'related-material.json').read_text())
for x in related['objects']:assert sha(R/x['path'])==x['sha256']
links=[]
for md in S.rglob('*.md'):
    for link in re.findall(r'\]\(([^)]+)\)',md.read_text()):
        if '://' in link or link.startswith('#'):continue
        p=(md.parent/link.split('#',1)[0]).resolve();rel=p.relative_to(S)
        assert p.is_file() or (R/rel).is_file(),(str(md.relative_to(S)),link)
        links.append({'from':str(md.relative_to(S)),'link':link,'target':str(rel)})
targets=sorted({p for x in receipts for p in x['targets']})
assert len(targets)==3 and all((S/p).read_text().startswith('---\nid:') for p in targets)
report={'status':'pass','primary_count':5,'raw_sources_SHA_checked':24,'runtime_files_unchanged':15,
 'entire_merged25_receipt_retained_and_worker_intersection_checked':True,
 'original_audit_byte_identical_134039B':True,'true_LP_calls14_not_raw_events28':True,
 'independent16_full_policy_unit_checks_and14_exact_duals_pass':True,
 'all14_dual_supports_in_formal_body_checked_against_actual_observation':True,
 'all16_terminal_payoff_rows_in_counterexample_checked':True,
 'explicit_read_order_and_observer_correction_preserved':True,
 'local_markdown_links_checked':len(links),'links':links,
 'formal_bodies':[{'path':p,'size':(S/p).stat().st_size,'sha256':sha(S/p)} for p in targets],
 'field_checks_do_not_replace_math_review':True}
(W/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
files=[]
for p in sorted(S.rglob('*')):
    if p.is_file() and p!=S/'copy-files.json':
        assert '__pycache__' not in p.parts
        files.append({'path':str(p.relative_to(S)),'size':p.stat().st_size,'sha256':sha(p)})
manifest={'stage_root':str(S),'manifest_is_transport_only':True,'file_count':len(files),'bytes':sum(x['size'] for x in files),'files':files}
(S/'copy-files.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'pass','file_count':len(files),'bytes':manifest['bytes'],
 'manifest_bytes':(S/'copy-files.json').stat().st_size,'manifest_sha256':sha(S/'copy-files.json'),
 'formal_bodies':report['formal_bodies'],'links':len(links)},ensure_ascii=False))
