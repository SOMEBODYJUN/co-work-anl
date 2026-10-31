from pathlib import Path
from itertools import product
import hashlib,json,re

S=Path(__file__).resolve().parents[4]
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
E=S/'archives/customer-attraction/tools/evidence/count-markov-probes-primary'
W=S/'cleanup/workspaces/Boss4/r3-count-markov-probes-primary'
NEW='archives/customer-attraction/state/计算/计数统一续局的有限枚举与辅助终局分离--计算.md'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source=json.loads((E/'source-manifest.json').read_text());primary=source['sources']
assert len(primary)==5 and source['primary_bytes']==211750
for x in primary:
    p=S/x['saved_path'];assert p.stat().st_size==x['size'] and sha(p)==x['sha256']
    assert len(x['sources'])==2 and all(s['bytes_verified'] for s in x['sources'])
claim=json.loads((W/'claim-observation.json').read_text())
assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync_status']=='synced'
assert sha(W/'claim-receipt.json')==claim['capture_sha256']
assert set(claim['claimed_primary_ids'])=={x['id'] for x in primary}
for x in claim['local_HEAD_owners']:
    rec=x['record'];assert rec['owner']=='Boss4' and rec['disposition']=='in-progress'
    assert rec['source_sha256']==next(z['sha256'] for z in primary if z['id']==x['id'])
receipts=json.loads((W/'semantic-receipts.json').read_text())
assert len(receipts)==5 and {x['id'] for x in receipts}==set(claim['claimed_primary_ids'])
assert sum(x['disposition']=='duplicate' for x in receipts)==2
for x in receipts:
    assert all(x[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
    assert all(x[k] for k in ['read_note','comparison_note','decision_note'])
    for p in x['targets']:assert (S/p).is_file() or (R/p).is_file()
for x in json.loads((E/'reused-evidence.json').read_text())['references']:assert sha(R/x['path'])==x['sha256']
for x in json.loads((E/'related-material.json').read_text())['related_objects']:assert sha(R/x['path'])==x['sha256']
old=json.loads((S/primary[4]['saved_path']).read_text())
assert len(old['Markov_last_map_results'])==648 and old['Markov_second_maps_exhausted']==130776
assert len(old['full_policy'])==31 and old['complete_SPE_comparisons']==155
assert old['full_min_welfare']==22428 and old['Markov_min_welfare']==22429 and old['OPT']==22431
for name,x in zip(['count','fresh','generic'],primary[:3]):
    d=json.loads((E/f'replay-{name}/execution.json').read_text())
    assert d['returncode']==0 and not d['timed_out'] and d['original_entry_runs_this_batch']==1
    assert d['solver_calls']==0 and d['stderr_bytes']==0 and not (E/f'replay-{name}/stderr.txt').read_bytes()
    code=E/f'replay-{name}-tree'/x['path'];assert sha(code)==x['sha256']==d['source_sha256']
assert (E/'replay-count/stdout.txt').read_text()=='all 128 binary equal 2244\nall 10000 random equal 15342\n'
g=json.loads((E/'replay-generic/stdout.txt').read_text());assert (g['equal'],g['skipped'],g['peak'])==(500,0,12)
raw=json.loads((E/'replay-fresh/stdout.txt').read_text());assert raw['trial']==205 and raw['onlyfull']==[[0,2,5]]
f=json.loads((E/'independent-fresh-review.json').read_text())
assert f['status']=='pass' and f['solver_calls']==0 and f['new_independent_script_runs']==1
assert f['full_root_sets']==['025','035','125','345'] and f['count_uniform_root_sets']==['035','125','345']
assert f['all_last_maps']==32 and f['second_maps_exhausted']==144
assert (f['complete_legal_fresh_decision_nodes'],f['comparisons_including_self'],f['comparisons_excluding_self'],f['ties_including_self'])==(37,156,119,53)
policy={tuple(x['history']):x['action'] for x in f['explicit_full_fresh_policy']}
required={h for d in range(3) for h in product(range(6),repeat=d) if len(set(h))==d}
assert set(policy)==required and all(a not in h for h,a in policy.items())
assert len(f['phi'])==35 and f['phi']==raw['phi']
classified={}
for row in f['last_map_results']:
    last=row['last'];roots=row['root_sets']
    expected=['125'] if last['25']==1 else (['125','345'] if last['05']==2 else ['035','125'])
    assert roots==expected
    k=tuple(expected);classified[k]=classified.get(k,0)+1
assert classified=={('125',):16,('125','345'):8,('035','125'):8}
phi={frozenset(map(int,k.split(','))):v for k,v in raw['phi'].items()}
totals={s:3*phi[frozenset(map(int,s))]-sum(phi[frozenset(map(int,s))-{int(a)}] for a in s) for s in f['full_root_sets']}
assert totals=={'025':7,'035':10,'125':17,'345':6}
assert min(totals[s] for s in f['full_root_sets'])==min(totals[s] for s in f['count_uniform_root_sets'])==6
links=[]
for md in S.rglob('*.md'):
    for dest in re.findall(r'\]\(([^)]+)\)',md.read_text()):
        if '://' in dest or dest.startswith('#'):continue
        p=(md.parent/dest.split('#',1)[0]).resolve();rel=p.relative_to(S)
        assert p.is_file() or (R/rel).is_file(),(str(md),dest)
        links.append({'from':str(md.relative_to(S)),'link':dest,'target':str(rel)})
assert (S/NEW).read_text().startswith('---\nid:')
validation={'status':'pass','primary_files_SHA_verified':5,'replay_code_unchanged':3,
 'receipt_scope_and_targets_checked':True,'existing_same_SHA_audit_report_and_related_objects_match':True,
 'all_three_new_original_main_success':True,'old_audit_not_rerun':True,
 'independent37node_auxiliary_policy_and32map_classification_checked':True,
 'auxiliary_minimum_sum_equality6_checked':True,'old_original_model_strict_min_welfare_difference_preserved':True,
 'local_markdown_links_checked':len(links),'links':links,
 'formal_body_bytes':(S/NEW).stat().st_size,'formal_body_sha256':sha(S/NEW),
 'machine_checks_do_not_replace_math_review':True}
(W/'validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n')
files=[]
for p in sorted(S.rglob('*')):
    if p.is_file() and p!=S/'copy-files.json':
        assert '__pycache__' not in p.parts
        files.append({'path':str(p.relative_to(S)),'size':p.stat().st_size,'sha256':sha(p)})
manifest={'stage_root':str(S),'manifest_is_transport_only':True,'file_count':len(files),'bytes':sum(x['size'] for x in files),'files':files}
(S/'copy-files.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'pass','file_count':manifest['file_count'],'bytes':manifest['bytes'],
                  'manifest_bytes':(S/'copy-files.json').stat().st_size,'manifest_sha256':sha(S/'copy-files.json'),
                  'formal_body_bytes':(S/NEW).stat().st_size,'formal_body_sha256':sha(S/NEW),
                  'local_links':len(links)},ensure_ascii=False))
