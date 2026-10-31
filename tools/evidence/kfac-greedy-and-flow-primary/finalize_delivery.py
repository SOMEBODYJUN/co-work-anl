from pathlib import Path
import ast,hashlib,json,re
S=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-kfac-greedy-and-flow-primary')
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
E=S/'tools/evidence/kfac-greedy-and-flow-primary';W=S/'cleanup/workspaces/Boss4/r3-kfac-greedy-and-flow-primary-next'
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
checks=[]
def ck(n,v,detail=None):
 checks.append(dict(check=n,passed=bool(v),**({'detail':detail} if detail is not None else {})))
 if not v:raise AssertionError(n)
primary=load(E/'source-manifest.json');deps=load(E/'dependency-manifest.json');byid={d['id']:d for d in primary+deps}
for d in primary+deps:
 b=(S/d['saved_path']).read_bytes()
 ck('exact inventory source '+d['id'],sha(b)==d['sha256'] and len(b)==d['size'])
 ck('replay-tree actual original '+d['id'],(E/'replay-tree'/d['path']).read_bytes()==b)
 if d['path'].endswith('.py'):ast.parse(b.decode())
capture=load(E/'actual-claim-receipt.json');want={d['id'] for d in primary};owners=load(E/'primary-ownership-snapshot.json')
authority=Path('/workspace/scratch/37f0f9248cfc/boss4-r3-refill25cfcgchcick-claim.json')
ck('unprojected exact original25 actual pushed/synced Boss4',capture['status']=='pushed' and capture['actor']=='Boss4' and capture['local_sync']['status']=='synced' and len(capture['ids'])==25 and want<=set(capture['ids']) and (E/'actual-claim-receipt.json').read_bytes()==authority.read_bytes())
ck('actual expected intersection owner five',len(primary)==5 and len(owners)==5 and {d['id'] for d in owners}==want and all(d['owner']=='Boss4' and d['disposition']=='in-progress' and d['source_sha256']==byid[d['id']]['sha256'] for d in owners))
ck('primary full scope44347B957lines',sum(d['size'] for d in primary)==44347 and sum(len((S/d['saved_path']).read_text().splitlines()) for d in primary)==957)
ck('related real thirteen70376B',len(deps)==13 and sum(d['size'] for d in deps)==70376)
contexts=load(E/'context-manifest.json')
for d in contexts:
 b=(S/d['saved_path']).read_bytes()
 ck('complete exact context '+d['path'],len(b)==d['bytes'] and sha(b)==d['sha256'] and d['read_scope'].startswith('complete'))
ck('nine actual formal contexts82134B',len(contexts)==9 and sum(d['bytes'] for d in contexts)==82134)
old=load(E/'complete-old-report-readback.json')
for sid in ['41b0ab6732ba2f681e68','d027eeb6603c80ef3c5a']:
 report=load(S/byid[sid]['saved_path'])
 ck('complete old report readback '+sid,old[sid]['report']==report and old[sid]['sha256']==byid[sid]['sha256'])
 for path,h in report['source_sha256'].items():
  ck('old success true code/input SHA '+path,any(d['path']==path and d['sha256']==h for d in primary+deps))
flow=old['41b0ab6732ba2f681e68']['report'];ep=old['d027eeb6603c80ef3c5a']['report']
ck('flow actual finite counts6691/89521/7902',flow['status']=='all_passed' and flow['counts']['instances']==6691 and flow['counts']['enumerated_assignments']==89521 and flow['counts']['all_global_minima_checked']==7902 and flow['counts']['canonical_global_oracle_instances']==6691 and flow['counts']['archived_global_oracle_instances']==6691)
ck('flow archived-only residual6791/4015 and1000identities',flow['counts']['archived_residual_graphs_checked']==6791 and flow['counts']['archived_residual_graphs_with_zero_cost_cycles']==4015 and flow['counts']['nonuniform_path_identities_checked']==1000 and flow['counts']['canonical_invalid_inputs_rejected']==8 and flow['counts']['archived_invalid_inputs_rejected']==8)
embedded=(E/'read-embedded-equal-flow.py.txt').read_bytes();instrumented=(E/'instrumentation-readback.py.txt').read_bytes()
ast.parse(embedded.decode());ast.parse(instrumented.decode())
ck('fully read embedded exact pin340ee',sha(embedded)==flow['archived_code_sha256'])
ck('fully read sole instrumentation pin8d6',sha(instrumented)==flow['instrumented_archived_code_sha256'] and embedded.decode().count('    a = []\n')==1 and instrumented.decode()==embedded.decode().replace('    a = []\n','        audit_residual(graph, source, sink, total_cost)\n\n    a = []\n'))
ck('EP186 actual shared-only counter summary',ep['counts']==dict(instances=186,layouts=2976,full_cells_examined=73304,far_patterns_examined=14590,near_patterns_examined=7295,conditional_cost_comparisons=166968,facility_deviations=1116) and len(ep['results'])==186)
ck('EP all186 actual=menu',all(x['menu_bound']==x['actual_alpha'] for x in ep['results']))
ck('EP exact nontrivial row identities',[i for i,x in enumerate(ep['results']) if any(x[k]!='1' for k in ['optimal_alpha','menu_bound','actual_alpha'])]==[22,63,69,104,159,180,181,182] and [ep['results'][i]['optimal_alpha'] for i in [180,181,182]]==['13/10','2124/1625','144508/110895'])
reuse=load(E/'same-SHA-success-reuse.json')
ck('two adequate old successes, zero new calls',len(reuse['old_successes_reused'])==2 and all(x['all_report_source_hashes_match_actual_files'] and x['new_original_CLI_calls']==0 for x in reuse['old_successes_reused']) and reuse['new_original_CLIs']==3)
runs=load(E/'runs/new-run-summary.json')
ck('exact three original CLI invocations',len(runs)==3 and sum(x['original_CLI_invocations_this_batch'] for x in runs)==3)
for x in runs:
 name=x['name'];sid=x['source_id'];inp=x['input_binding']
 ck('one successful original '+name,x['exit_code']==0 and x['source_sha256']==byid[sid]['sha256'] and x['original_CLI_invocations_this_batch']==1)
 ck('real input binding '+name,inp['sha256']==byid[inp['id']]['sha256'] and inp['size']==byid[inp['id']]['size'])
 ck('actual concise stdout and empty stderr '+name,(E/'runs'/f'{name}.stdout.txt').stat().st_size==x['stdout_bytes'] and x['stdout_bytes']>0 and (E/'runs'/f'{name}.stderr.txt').read_bytes()==b'' and x['stderr_bytes']==0)
 ck('direct isolated original CLI '+name,'-I' in x['command'] and '-B' in x['command'] and not any(a.startswith('-O') for a in x['command']) and x['command'][-1]==str(E/'replay-tree'/byid[sid]['path']))
probe=load(E/'runtime-flags-probe.json')
ck('separate flags probe zero original calls',probe['probe_only'] and probe['original_source_invocations']==0 and probe['performed_after_three_original_runs'] and probe['runtime']['optimize']==0 and probe['runtime']['isolated']==1)
formal=load(E/'formal-resource-manifest.json');links=[];c0=[];trailing=[]
for d in formal:
 p=S/d['path'];b=p.read_bytes();t=b.decode()
 ck('formal exact final bytes '+d['path'],len(b)==d['bytes'] and sha(b)==d['sha256'])
 ck('flat required MATEK '+d['path'],all(re.search('^'+k+':',t,re.M) for k in ['id','kind','type_tag','title','status','summary','source_refs']) and t.startswith('---\n'))
 bad=[(i,ord(c)) for i,c in enumerate(t) if ord(c)<32 and c not in '\r\n\t'];c0+=bad
 tr=[i for i,l in enumerate(t.splitlines(),1) if l.rstrip(' \t')!=l];trailing+=tr
 ck('formal C0 zero '+d['path'],not bad)
 ck('formal trailing zero '+d['path'],not tr)
 ck('all TeX and path placeholders recovered '+d['path'],'§' not in t and not re.search(r'@(E|P[0-9]|CTX|[0-9a-f]{20})',t) and t.count(chr(92)+'[')==t.count(chr(92)+']'))
 for target in re.findall(r'\[[^\]\n]*\]\(([^)\n]+)\)',t):
  if '://' in target or target.startswith('#'):continue
  dest=(p.parent/target.split('#')[0]).resolve();ok=dest.exists()
  if not ok:
   try:ok=(R/dest.relative_to(S)).exists()
   except ValueError:ok=False
  links.append(dict(source=d['path'],target=target,exists=ok))
ck('all actual relative links resolve',all(x['exists'] for x in links),dict(count=len(links)))
receipts=load(W/'semantic-receipts.json')
ck('exact five semantic receipts no related extras',len(receipts)==5 and {x['id'] for x in receipts}==want)
for d in receipts:ck('complete semantic receipt '+d['id'],all(d[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and all(d[k] for k in ['read_note','comparison_note','decision_note']) and d['disposition']=='integrated' and all((S/p).exists() for p in d['targets']))
proposal=load(E/'suggested-existing-eptas-page-corrections.json')['proposals']
ck('one guarded suggestion only',len(proposal)==1 and not proposal[0]['applied_to_shared_tree'])
for d in proposal:
 c=next(c for c in contexts if c['path']==d['path']);before=(S/c['saved_path']).read_bytes();t=before.decode()
 ck('exact before-SHA suggestion',sha(before)==d['before_sha256'] and len(before)==d['before_bytes'])
 for x in d['replacements']:
  ck('exact suggestion occurrence '+x['old'][:60],t.count(x['old'])==x['expected_count']);t=t.replace(x['old'],x['new'])
 ck('exact suggested external preview',sha(t.encode())==d['after_sha256_if_applied'] and (S/d['preview_path']).read_text()==t)
cand=load(W/'next-candidates.json')
ck('actual four candidate inventory IDs only',len(cand)==4 and all(not x['local_progress_exists'] for x in cand))
scope=dict(primary_files=5,primary_bytes=44347,primary_lines=957,primary_full_actual_read=True,related_inventory_files=13,related_inventory_bytes=70376,related_formal_context_files=9,related_formal_bytes=82134,original_capture_is_unprojected25=True,new_original_CLI_invocations=3,new_original_CLI_report_supported_completions=3,reused_same_SHA_successes=2,new_flow_and_EPTAS_original_invocations=0,new_related_source_done=0,new_repository_suites=0,new_shared_Git_operations=0,new_network_operations=0,derived_math='Explicit original-fixture proofs, finite support/menu/flow algorithms and source-control-flow semantics; no new broad numerical survey',read_boundary='Every original primary/code dependency and explicit JSON/report field read. Random input seeds/generators fully read; old reports do not contain4500/180 full input arrays, so no absent per-random-row reading claimed.',separate_runtime_probe='One tiny isolated flags probe after three original CLIs, zero mathematical source invocation; no trace invented inside originals.',external_sources='URLs and source claims retained as frozen history only; no new paper read, external review, priority claim or scheduler import',phase3='No graph/mapper write or implicit model migration')
dump(E/'read-scope-and-evidence-status.json',scope);dump(E/'formal-link-check.json',links)
selfcheck=dict(passed=True,checks=len(checks),details=checks,formal_forbidden_C0=len(c0),formal_trailing_whitespace=len(trailing),relative_links_checked=len(links),scope='Actual bytes/ownership/source domain/real-run count/old success bindings/semantic receipts/format/links; counts are not mathematical proofs')
dump(W/'self-check.json',selfcheck)
files=[]
for root in [S/'archives',S/'tools',S/'cleanup']:files.extend(p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc')
files=sorted(files)
ck('white list has only three new canonical files',[p.relative_to(S).as_posix() for p in files if p.relative_to(S).parts[0]=='archives']==sorted(d['path'] for d in formal))
selfcheck['checks']=len(checks);selfcheck['details']=checks;dump(W/'self-check.json',selfcheck)
rows=[dict(path=p.relative_to(S).as_posix(),bytes=p.stat().st_size,sha256=sha(p.read_bytes())) for p in files]
dump(S/'copy-files.json',rows);(S/'copy-paths.txt').write_text(''.join(x['path']+'\n' for x in rows))
summary=dict(stage=str(S),evidence_root=E.relative_to(S).as_posix(),workspace=W.relative_to(S).as_posix(),files=len(rows),bytes=sum(d['bytes'] for d in rows),formal_files=len(formal),formal_bytes=sum(d['bytes'] for d in formal),primary_sources=5,primary_bytes=44347,primary_lines=957,related_inventory_files=13,semantic_receipts=5,self_checks=len(checks),relative_links=len(links),forbidden_formal_C0=0,formal_trailing_whitespace=0,new_original_CLIs=3,reused_same_SHA_successes=2,copy_files_sha256=sha((S/'copy-files.json').read_bytes()),next_candidate_ids=[x['id'] for x in cand],existing_canonical_replacements_applied=0)
dump(S/'delivery-summary.json',summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
