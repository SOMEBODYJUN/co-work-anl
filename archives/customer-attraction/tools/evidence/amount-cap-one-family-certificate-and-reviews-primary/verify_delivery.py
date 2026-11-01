"""Structural action-table/source check; does not calculate payoffs or execute original code."""
from pathlib import Path
from itertools import product
import hashlib,json,re
E=Path(__file__).resolve().parent;S=E.parents[4]
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
P=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-terminal-amount-cap-and-audit-primary')
W=S/'cleanup/workspaces/Boss4/r3-amount-cap-one-family-certificate-and-reviews-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=read(E/'actual-source-manifest.json');rows=m['rows'];ids={r['id'] for r in rows}
assert len(rows)==5 and sum(r['size'] for r in rows)==54013
claim=read(E/'authoritative-full-claim.json')
assert claim['status']=='pushed' and claim['operation']=='claim' and claim['actor']=='Boss4'
assert len(claim['ids'])==9 and ids<=set(claim['ids']) and claim['local_sync']['status']=='synced'
assert claim['remote_tip']=='f5fc0baba13d9649bd779f471dfa1fca2e2185c1'
for row in rows:
 p=S/row['stage_path'];b=p.read_bytes()
 assert len(b)==row['size'] and sha(p)==row['sha256']
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['blob']
 assert Path(row['local_path']).read_bytes()==b
 progress=read(E/'local-progress-at-read'/(row['id']+'.json'))
 assert progress['owner']=='Boss4' and progress['source_sha256']==row['sha256']
 assert (E/'normal-show-captures'/Path(row['actual_normal_show_capture']).name).is_file()
author=next(r for r in rows if r['id']=='44ac5a996de190a8da48')
assert author['exact_prior_normal_show_reused'] is True and author['no_new_normal_show_for_this_source'] is True
rr=read(W/'semantic-receipts.json');assert len(rr)==5 and {r['id'] for r in rr}==ids
assert sum(r['disposition']=='duplicate' for r in rr)==1 and sum(r['disposition']=='retained' for r in rr)==4
for r in rr:
 assert all(r[k] is True for k in ('full_file_reviewed','related_material_checked','unique_content_accounted_for'))
 assert all(r[k] for k in ('read_note','comparison_note','decision_note'))
 assert all((S/t).is_file() or (R/t).is_file() or (P/t).is_file() for t in r['targets'])
comp=read(E/'formal-comparison.json');assert len(comp)==3
for r in comp:
 p=S/r['snapshot'];assert p.stat().st_size==r['bytes'] and sha(p)==r['sha256'] and r['full_file_reviewed']
cert=read(S/next(r['stage_path'] for r in rows if r['id']=='110a1ed1af682948ed17'))
assert len(cert)==16 and cert['n']==3 and cert['players']==4 and cert['topics']==7
assert cert['unit_customers']==18 and cert['ordered_nodes']==400 and cert['IC_including_self']==2800
assert cert['recipient_payoff']=='3' and cert['combined_positive_price']=='15/4' and cert['column_coefficient']=='5/4'
assert cert['welfare']==cert['optimum']==18 and 'terminal_counts' not in cert and 'profits' not in cert
actions=cert['actions'];mapping={tuple(r['history']):r['action'] for r in actions}
assert len(actions)==len(mapping)==400
assert all(set(r)=={'history','action'} for r in actions)
assert set(mapping)=={h for d in range(4) for h in product(range(7),repeat=d)}
assert all(type(a) is int and 0<=a<7 for a in mapping.values())
assert actions==sorted(actions,key=lambda r:(len(r['history']),tuple(r['history'])))
h=()
for _ in range(4):h=h+(mapping[h],)
assert list(h)==cert['actual_path']==[0,1,2,3]
assert cert['requests']==[{'sender':j+1,'cut':4,'forced_topic':j+4,'parent_payoff':'5','child_payoff':'4','claim_coefficient':'5/4','positive_price':'1'} for j in range(3)]
structure=read(E/'certificate-structural-readout.json')
assert structure['depth_counts']==[1,7,49,343] and structure['actual_chain']==[0,1,2,3]
assert structure['summary']=={k:v for k,v in cert.items() if k!='actions'} and structure['IC_2800_recalculated'] is False
scope=read(E/'execution-and-review-scope.json')
assert scope['new_normal_show_files']==4 and scope['frozen_certificate_read_all_actions']==400
assert all(scope[k]==0 for k in ('current_original_entry_runs','current_imports','current_payoff_or_IC_replays','new_mathematical_implementation_runs','new_solver_or_SPE_search_runs'))
assert not (E/'runs').exists()
assert len(read(W/'relation-evidence.json'))==6 and read(W/'source-state-updates.json')==[]
math=list((S/'archives/customer-attraction/state').rglob('*.md'));assert len(math)==1
assert '<!--' not in math[0].read_text()
links=0
for p in math+[E/'README.md']:
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if '://' in target or target.startswith('#'):continue
  q=(p.parent/target.split('#',1)[0]).resolve()
  if not q.exists():assert (R/q.relative_to(S)).is_file() or (P/q.relative_to(S)).is_file(),(str(p),target)
  links+=1
for r in read(E/'content-manifest.json'):
 p=S/r['path'];assert p.stat().st_size==r['bytes'] and sha(p)==r['sha256']
copy=W/'copy-files.json'
if copy.exists():assert read(copy)==sorted(str(p.relative_to(S)) for p in S.rglob('*') if p.is_file())
result={'status':'PASS','scope':'structural source/action-table fields/key domain/range/sort/4-link actual chain only; no payoffs, IC, import or original code execution','primary_files':5,'primary_bytes':54013,'receipts':5,'duplicates':1,'retained':4,'formal_math_files':1,'comparison_snapshots':3,'relations':6,'source_state_updates':0,'frozen_actions_read_and_structurally_checked':400,'current_original_entries':0,'current_IC_or_payoff_replays':0,'new_mathematical_implementation_runs':0,'links_checked':links}
(W/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
