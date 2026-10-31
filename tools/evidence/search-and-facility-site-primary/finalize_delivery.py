from pathlib import Path
import ast,hashlib,json,os,re
S=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-search-and-facility-site-primary')
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
E=S/'tools/evidence/search-and-facility-site-primary'
W=S/'cleanup/workspaces/Boss4/r3-search-and-facility-site-primary-next'
def read(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
checks=[]
def ck(name,ok,detail=None):
 checks.append(dict(check=name,passed=bool(ok),**({'detail':detail} if detail is not None else {})))
 if not ok:raise AssertionError(name)
primary=read(E/'source-manifest.json');deps=read(E/'dependency-manifest.json');byid={d['id']:d for d in primary+deps}
for d in primary+deps:
 b=(S/d['saved_path']).read_bytes()
 ck('exact inventory bytes '+d['id'],len(b)==d['size'] and sha(b)==d['sha256'])
 if d['path'].endswith('.py'):ast.parse(b.decode())
claim=read(E/'actual-claim-receipt.json');owner=read(E/'primary-ownership-snapshot.json')
ck('actual pushed Boss4 synced five',claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced' and set(claim['ids'])=={d['id'] for d in primary})
ck('owner snapshot complete five in-progress',len(owner)==5 and all(d['owner']=='Boss4' and d['disposition']=='in-progress' and d['source_sha256']==byid[d['id']]['sha256'] for d in owner))
ck('full primary scope 48972B and 1124 lines',sum(d['size'] for d in primary)==48972 and sum(len((S/d['saved_path']).read_text().splitlines()) for d in primary)==1124)
for d in read(E/'context-manifest.json'):
 b=(S/d['saved_path']).read_bytes()
 ck('exact fully read context '+d['path'],len(b)==d['bytes'] and sha(b)==d['sha256'] and d['read_status'].startswith('complete'))
ready=read(E/'input-structure-and-run-readiness.json')
ck('three same-SHA old successes, two new planned',len(ready['old_success_reused'])==3 and len(ready['new_run_plan'])==2 and ready['no_fake_stubs_or_Git_fixture'])
search=read(S/byid['912c92b9572c9c92ca11']['saved_path'])
ck('search exact old code binding',search['audit_script_sha256']==byid['4a0a68157e801a180ce5']['sha256'] and search['status']=='completed')
ck('search finite domain and absent residual counterexample',search['total_instance_count']==27136 and search['minimum_ratio']=='5/9' and search['residual_lemma_counterexamples']==[] and search['universal_claim_proved'] is False and len(search['stages'])==13 and len(search['canonical_independent_crosschecks'])==13)
four=read(S/byid['79d0b8c76eebaca202fa']['saved_path'])
ck('four32 exact old code and constructor binding',four['source_sha256']['tests/audits/four_site_fptas.py']==byid['a4954c4665e08897643a']['sha256'] and four['source_sha256']['facility_spe/shared/four_site_fptas_hardness.py']==byid['9f32aa2a4194de92d3b6']['sha256'])
ck('four32 true finite counts',four['source_instances']==32 and four['yes']==8 and four['no']==24 and four['enumerated']==886344 and four['accepted_support_cells']==59340 and four['conditional_cost_comparisons']==811138)
ind=read(S/byid['c26e8f18cc84a854a492']['saved_path'])
ck('four19 exact old code binding',ind['source_sha256']['tests/audits/four_site_fptas_independent.py']==byid['f859371ea34882324c83']['sha256'])
ck('four19 true counts',ind['counts']==dict(sources=19,support_cells_examined=92496,accepted_cells=17890,conditional_cost_comparisons=932718,yes=8,no=11,yes_certificate_deviations=96))
from fractions import Fraction as F
ck('four19 every core optimum below analytic other-layout guard',all(F(row['core_guard_lower_bound'])<F(131,100) for row in ind['cases']))
layers={n:dict(cases=sum(x['n']==n for x in ind['cases']),yes=sum(x['yes'] for x in ind['cases'] if x['n']==n),no=sum(not x['yes'] for x in ind['cases'] if x['n']==n)) for n in [4,6,8]}
ck('actual independent layers 3/7,2/3,3/1',layers=={4:dict(cases=10,yes=3,no=7),6:dict(cases=5,yes=2,no=3),8:dict(cases=4,yes=3,no=1)})
runs=read(E/'runs/new-run-summary.json')
ck('exactly two new original CLI invocations',len(runs)==2 and sum(d['source_original_CLI_invocations_this_batch'] for d in runs)==2)
for run in runs:
 name=run['name'];out=E/'runs'/f'{name}-report.json'
 ck('new exact original CLI successful '+name,run['exit_code']==0 and run['runtime']['optimize']==0 and run['runtime']['isolated']==1 and run['source_sha256']==byid[run['source_id']]['sha256'])
 ck('stdout equals complete report '+name,read(out)==read(E/'runs'/f'{name}.stdout.txt') and (E/'runs'/f'{name}.stderr.txt').read_bytes()==b'')
 ck('actual dependencies hash-bound '+name,all(x['sha256']==byid[x['id']]['sha256'] and x['size']==byid[x['id']]['size'] for x in run['dependency_bindings']))
full=read(E/'runs/five-site-full-report.json');edge=read(E/'runs/five-site-edges-report.json')
ck('full finite domain 1103/96/14, default nonquick',full['parameter_search_tests']==1103 and full['forced_macro_tests']==96 and len(full['cases'])==14 and full['strict_boundary_counterexample_verified'] and full['invalid_factor_inputs_rejected']==3 and full['all_assertions_passed'] and full['repository_checks_run'] is False)
ck('edge finite nine and six invalid sources',len(edge['cases'])==9 and sum(d['source_yes'] for d in edge['cases'])==6 and edge['invalid_source_inputs_rejected']==6 and edge['all_assertions_passed'] and edge['repository_checks_run'] is False)
ck('new/old full reports only timing differs',len(read(E/'new-old-report-comparison.json'))==2 and all(d['differing_keys']==['elapsed_seconds'] and d['all_other_fields_equal'] for d in read(E/'new-old-report-comparison.json')))
ck('all five complete report fields semantically read',len(read(E/'finite-domain-readback.json'))==5 and all(d['all_original_fields_semantically_read'] for d in read(E/'finite-domain-readback.json').values()))
formal=read(E/'formal-resource-manifest.json')
c0=[];trailing=[];links=[];unresolved=[]
for d in formal:
 p=S/d['path'];t=p.read_text();b=p.read_bytes()
 ck('formal final byte hash '+d['path'],len(b)==d['bytes'] and sha(b)==d['sha256'])
 ck('flat MATEK '+d['path'],all(re.search(r'^'+f+':',t,re.M) for f in ['id','kind','type_tag','title','status','summary','source_refs']) and t.startswith('---\n'))
 bad=[dict(position=i,code=ord(c)) for i,c in enumerate(t) if ord(c)<32 and c not in '\n\r\t'];c0.extend(bad)
 tr=[i for i,l in enumerate(t.splitlines(),1) if l.rstrip(' \t')!=l];trailing.extend(tr)
 ck('formal no C0 '+d['path'],not bad)
 ck('formal no trailing whitespace '+d['path'],not tr)
 ck('complete TeX display pairs '+d['path'],t.count(chr(92)+'[')==t.count(chr(92)+']') and '§' not in t and not re.search(r'@(E|P[0-9]|CTX|[0-9a-f]{20})',t))
 for target in re.findall(r'\[[^\]\n]*\]\(([^)\n]+)\)',t):
  if '://' in target or target.startswith('#'):continue
  dest=(p.parent/target.split('#')[0]).resolve()
  ok=dest.exists()
  if not ok:
   try:rr=dest.relative_to(S);ok=(R/rr).exists()
   except ValueError:ok=False
  links.append(dict(source=d['path'],target=target,exists=ok))
  if not ok:unresolved.append(links[-1])
ck('all formal links resolve in staged or existing repo',not unresolved,dict(links=len(links)))
receipts=read(W/'semantic-receipts.json')
ck('exactly five primary receipts',len(receipts)==5 and {d['id'] for d in receipts}=={d['id'] for d in primary})
for d in receipts:ck('complete semantic receipt '+d['id'],all(d[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and all(d[k] for k in ['read_note','comparison_note','decision_note']) and d['disposition']=='integrated' and all((S/t).exists() for t in d['targets']))
proposals=read(E/'suggested-existing-facility-page-corrections.json')['proposals']
ck('two new suggestions only',len(proposals)==2 and all(d['applied_to_shared_tree'] is False for d in proposals))
ctx={d['path']:d for d in read(E/'context-manifest.json')}
for d in proposals:
 b=(S/ctx[d['path']]['saved_path']).read_bytes()
 ck('suggestion exact before '+d['path'],sha(b)==d['before_sha256'] and len(b)==d['before_bytes'])
 t=b.decode()
 for replacement in d['replacements']:
  ck('suggestion unique exact replacement '+d['path'],t.count(replacement['old'])==replacement['expected_count'])
  t=t.replace(replacement['old'],replacement['new'])
 ck('suggestion exact external preview '+d['path'],sha(t.encode())==d['after_sha256_if_applied'] and (S/d['preview_path']).read_text()==t)
# Historical BD proposals and external previews are evidence only, not canonical writes.
prior=read(E/'existing-page-corrections-from-BD.json')['proposals']
ck('BD four frozen suggestions retained',len(prior)==4 and all(d['applied_to_shared_tree'] is False for d in prior))
for d in prior:
 ck('BD preview only contains exact proposed SHA '+d['path'],any(sha(p.read_bytes())==d['after_sha256_if_applied'] for p in (E/'existing-correction-previews').glob('*.md')))
# No shared targets enter the whitelist; previews only live under the new evidence folder.
candidates=read(W/'next-candidates.json')
ck('five actual inventory candidates, not claimed',len(candidates)==5 and all(d['eligibility'].startswith('no local progress') and not d['local_progress_exists'] for d in candidates))
dump(E/'read-scope-and-evidence-status.json',dict(primary_files=5,primary_bytes=48972,primary_lines=1124,all_primary_actual_full_read=True,related_inventory_files=len(deps),related_inventory_bytes=sum(d['size'] for d in deps),related_formal_context_files=len(ctx),related_only_no_extra_done=True,old_success_same_SHA_reused=3,new_original_CLI_invocations=2,new_original_CLI_report_supported_completions=2,new_source_math_domain='14 default + 9 edge reduction cases; default1103 factor probes +96 macro comparisons; edge6 serialized YES complete certificates',old_only_math_domain='27136 CAG exact searches; 32 four-site full-layout and19 independent four-site cases',new_repository_suites_run=0,new_shared_Git_operations=0,new_network_operations=0,format_recovery='Builder Python emitted harmless invalid-escape SyntaxWarnings for literal LaTex quad/comma; switched those literals to § placeholders before final delivery. Derived Markdown retained correct backslashes, no C0 or mathematical change. This is formatter work, no new original mathematical run.',semantic_versus_structural='Full source and result semantics actually read. Recursively traversing3081 JSON values is a separate schema check, not mathematical certification.',limits=['finite regressions do not prove universal hardness or CAG half','old search canonical dependency SHAs not listed;13 old worst-stage confirms not27136 new-stack tests','five-site false per-layout entries are relaxations; global exactness uses proved diagonal normalization','original report provenance left unchanged; current run bindings in separate run records','no phase3 graph import or mapper claim','no existing formal page replacement in this batch']))
selfcheck=dict(passed=True,checks=len(checks),details=checks,formal_forbidden_C0=len(c0),formal_trailing_whitespace=len(trailing),relative_links_checked=len(links),scope='byte/actual ownership/domain/old-success reuse/new runtime/semantic receipts/format/links; mathematical proof status separately stated')
dump(W/'self-check.json',selfcheck)
dump(E/'formal-link-check.json',links)
allfiles=[]
for root in [S/'archives',S/'tools',S/'cleanup']:
 allfiles.extend(p for p in root.rglob('*') if p.is_file())
# Everything written is inside this new batch; do not copy the existing canonical paths in proposals.
allowed=[p for p in sorted(allfiles) if '__pycache__' not in p.parts and p.suffix!='.pyc']
rows=[dict(path=p.relative_to(S).as_posix(),bytes=p.stat().st_size,sha256=sha(p.read_bytes())) for p in allowed]
newformal={d['path'] for d in formal}
ck('no existing canonical targets in transport',[d['path'] for d in rows if d['path'].startswith('archives/')]==sorted(newformal))
# Update selfcheck after last whitelist assertion, then rebuild its row.
selfcheck['checks']=len(checks);selfcheck['details']=checks;dump(W/'self-check.json',selfcheck)
rows=[dict(path=p.relative_to(S).as_posix(),bytes=p.stat().st_size,sha256=sha(p.read_bytes())) for p in allowed]
dump(S/'copy-files.json',rows)
(S/'copy-paths.txt').write_text(''.join(d['path']+'\n' for d in rows))
summary=dict(stage=str(S),evidence_root=str(E.relative_to(S)),workspace=str(W.relative_to(S)),files=len(rows),bytes=sum(d['bytes'] for d in rows),formal_files=len(formal),formal_bytes=sum(d['bytes'] for d in formal),primary_sources=5,primary_bytes=48972,primary_lines=1124,related_inventory_sources=len(deps),semantic_receipts=len(receipts),self_checks=len(checks),relative_links=len(links),forbidden_formal_C0=0,formal_trailing_whitespace=0,new_original_CLI_invocations=2,old_same_SHA_successes_reused=3,copy_files_sha256=sha((S/'copy-files.json').read_bytes()),next_candidate_ids=[d['id'] for d in candidates],existing_page_replacements_applied=0)
dump(S/'delivery-summary.json',summary)
print(json.dumps(summary,ensure_ascii=False,indent=2))
