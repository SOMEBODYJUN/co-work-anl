from pathlib import Path
from fractions import Fraction as F
from math import comb
import hashlib,json,re,subprocess,os

S=Path(__file__).resolve().parents[4]
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
E=S/'archives/customer-attraction/tools/evidence/markov-welfare-policy-cones-primary'
W=S/'cleanup/workspaces/Boss4/r3-markov-welfare-and-policy-cones-primary'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source=json.loads((E/'source-manifest.json').read_text());primary=source['sources']
assert len(primary)==5 and source['primary_bytes']==1015212
for x in primary:
    p=S/x['saved_path'];assert p.stat().st_size==x['size'] and sha(p)==x['sha256']
    assert len(x['sources'])==2 and all(z['bytes_verified'] for z in x['sources'])
claim=json.loads((W/'claim-observation.json').read_text())
assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync_status']=='synced'
assert sha(W/'claim-receipt.json')==claim['capture_sha256']
assert set(claim['claimed_primary_ids'])=={x['id'] for x in primary}
for x in claim['local_HEAD_owners']:
    assert x['record']['owner']=='Boss4' and x['record']['disposition']=='in-progress'
    assert x['record']['source_sha256']==next(z['sha256'] for z in primary if z['id']==x['id'])
receipts=json.loads((W/'semantic-receipts.json').read_text())
assert len(receipts)==5 and {x['id'] for x in receipts}==set(claim['claimed_primary_ids'])
for x in receipts:
    assert x['disposition']=='integrated'
    assert all(x[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
    assert all(x[k] for k in ['read_note','comparison_note','decision_note'])
    assert all((S/p).is_file() for p in x['targets'])
for name,x in zip(['welfare','cone'],primary[:2]):
    d=json.loads((E/f'replay-{name}/execution.json').read_text())
    assert d['returncode']==0 and not d['timed_out'] and d['original_entry_runs_this_batch']==1
    assert d['stderr_bytes']==0 and not (E/f'replay-{name}/stderr.txt').read_bytes()
    assert sha(E/f'replay-{name}-tree'/x['path'])==x['sha256']==d['source_sha256']
welfare=json.loads((E/'replay-welfare/stdout.txt').read_text())
assert welfare['done'] and welfare['checked']==19856 and welfare['skipped']==144
assert not (E/'replay-welfare/new_markov_gap.json').exists()
trace=[json.loads(x) for x in (E/'replay-cone/stdout.txt').read_text().splitlines()]
assert len(trace)==3 and trace[-1]['done'] and trace[-1]['best']==1.8
assert trace[0]['step']==0 and trace[1]['step']==5 and not any('status' in x for x in trace)
diff=json.loads((E/'original-output-comparison.json').read_text())
assert not diff['byte_identical'] and len(diff['json_differences'])==1 and diff['json_differences'][0]['field']=='seconds'
assert sha(E/'replay-cone/new_policy_cone.json')==diff['new_sha256']

review=json.loads((E/'independent-policy-review.json').read_text())
assert review['new_independent_review_runs']==1 and review['solver_calls']==0 and not review['original_imports']
assert len(review['frozen_policies'])==3 and review['new_original_output']
expected=[(5,7,330,2801),(6,8,1287,37449),(8,8,6435,2396745)]
for data,want in zip(review['frozen_policies'],expected):
    assert (data['m'],data['k'],data['count_policy_entries'],data['complete_ordered_decision_histories_covered'])==want
    assert data['count_policy_entries']==comb(data['m']+data['k']-1,data['k'])
    assert not data['explicit_ordered_histories_enumerated'] and data['all_prescribed_actions_in_single_core']
    assert sum(z['count_states'] for z in data['lossless_policy_layers'])==want[2]
    assert all(len(z['all_actions_in_source_order'])==z['count_states'] for z in data['lossless_policy_layers'])
    assert [z['mode'] for z in data['interpretations']]==['literal_decimal','exact_binary_float','small_denominator_reconstruction']
    assert all(z['saved_support_is_optimal'] for z in data['interpretations'])
five,six,eight=review['frozen_policies']
for d in [five,review['new_original_output']]:
    a,b,c=d['interpretations'];assert a['exact_policy_SPE'] and c['exact_policy_SPE'] and not b['exact_policy_SPE']
    assert F(b['minimum_IC_margin'])==F(-1,90071992547409920)
    assert b['first_violation']['past_counts']==[0]*7 and b['first_violation']['chosen']==4 and b['first_violation']['alternative']==0
    assert a['primitive_unit_customers']==c['primitive_unit_customers']==9 and a['OPT_over_W']=='9/5'
assert all(z['exact_policy_SPE'] for z in six['interpretations']+eight['interpretations'])
assert [z['primitive_unit_customers'] for z in six['interpretations']]==[91666666666666665,66052794534767273,11]
assert six['interpretations'][2]['OPT_over_W']=='11/6'
assert F(11,6)-F(six['interpretations'][0]['OPT_over_W'])==F(1,30000000000000000)
assert all(z['primitive_unit_customers']==12 and z['OPT_over_W']=='3/2' for z in eight['interpretations'])

proof=json.loads((E/'published-predecessor-proof.json').read_text())
pub=subprocess.run(['git','show',proof['actual_original_publication_commit']+':'+proof['path']],cwd=R,
                   env={**os.environ,'GIT_NO_LAZY_FETCH':'1'},capture_output=True,check=True).stdout
assert hashlib.sha256(pub).hexdigest()==proof['published_sha256']
for x in json.loads((E/'related-material.json').read_text())['objects']:
    p=R/x['path']
    if p.exists():assert sha(p)==x['sha256']
    else:assert x['path']==proof['path'] and x['sha256']==proof['published_sha256']
links=[];pending=[]
for md in S.rglob('*.md'):
    for link in re.findall(r'\]\(([^)]+)\)',md.read_text()):
        if '://' in link or link.startswith('#'):continue
        q=(md.parent/link.split('#',1)[0]).resolve();rel=str(q.relative_to(S))
        present=q.is_file() or (R/rel).is_file()
        if not present:
            assert rel==proof['path']
            pending.append({'path':rel,'original_publication':proof['actual_original_publication_commit'],'original_done':proof['actual_original_done_commit'],
                            'bytes_match_known_mature_and_original_publication':True,'root_restoration_required_before_done':True})
        links.append({'from':str(md.relative_to(S)),'link':link,'target':rel,'present_in_current_stage_or_checkout':present})
targets=sorted({p for x in receipts for p in x['targets']})
for p in targets:assert (S/p).read_text().startswith('---\nid:')
nexts=json.loads((W/'next-candidates.json').read_text())
assert nexts['do_not_infer_available_from_local_absence'] and all(z['requires_root_restored_actual_ledger_check'] for z in nexts['candidates'])
validation={'status':'pass-with-explicit-published-link-restoration-dependency' if pending else 'pass',
 'mathematical_review':'complete; expected binary-rounding rejection verified, not erased',
 'five_primary_SHA_and_double_frozen_verified':True,'two_replay_codes_unchanged':True,
 'new_original_entry_runs':2,'independent_exact_review_runs':1,'frozen_policy_records_all_accounted_for':8052,
 'three_input_versions_separated':True,'binary5_negative_IC_exactly_verified':True,
 'historical_published_baseline_verified_by_original_commit':True,'markdown_links_checked':len(links),
 'links':links,'temporary_checkout_loss_pending_root_restoration':pending,
 'next_candidates_not_asserted_available':True,
 'formal_bodies':[{'path':p,'size':(S/p).stat().st_size,'sha256':sha(S/p)} for p in targets],
 'validation_not_a_substitute_for_math_review':True}
(W/'validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n')
files=[]
for p in sorted(S.rglob('*')):
    if p.is_file() and p!=S/'copy-files.json':
        assert '__pycache__' not in p.parts
        files.append({'path':str(p.relative_to(S)),'size':p.stat().st_size,'sha256':sha(p)})
manifest={'stage_root':str(S),'manifest_is_transport_only':True,'file_count':len(files),
          'bytes':sum(z['size'] for z in files),'files':files}
(S/'copy-files.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':validation['status'],'file_count':len(files),'bytes':manifest['bytes'],
                  'manifest_bytes':(S/'copy-files.json').stat().st_size,'manifest_sha256':sha(S/'copy-files.json'),
                  'formal_bodies':validation['formal_bodies'],'links':len(links),'pending_published_target_restore':len(pending)},ensure_ascii=False))
