"""Artifact/matrix-copy consistency only; never imports/runs original programs, LP or audit."""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import ast,copy,hashlib,json,re
S=Path(__file__).resolve().parents[4];W=Path(__file__).resolve().parent;E=S/'archives/customer-attraction/tools/evidence/cag-slot-potential-programs-primary';R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');checks=[]
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ck(name,c):
 if not c:raise AssertionError(name)
 checks.append(name)
expected={'307f0ade5c8981d08810','b04c2c8c5d4ef69f780a','46dcb02c08984b22b528','bb1fbbd18db347eb766e','5ae26250db6eb381a604'};rows=read(E/'source-manifest.json');claim=read(W/'claim-evidence.json');receipt=read(W/'original-claim-receipt.json');resolution=read(W/'claim-sync-resolution.json');preservation=read(W/'claim-sync-preservation.json')
ck('actual claim pushed Boss4 exact5',claim['status']=='pushed'and claim['actor']=='Boss4'and set(claim['ids'])==expected)
ck('original needsattention not rewritten',receipt['local_sync']['status']=='needs-attention'and claim['original_local_sync_status']=='needs-attention'and claim['original_receipt_unchanged'])
ck('independently resolved before primary',claim['effective_local_sync_status']==resolution['status']=='independently-resolved-after-original-needs-attention'and resolution['all_stashed_bytes_exact']and not resolution['unmerged'])
ck('start tip91d308 historical—not current merge assumption',claim['remote_tip']==resolution['actual_head']==receipt['remote_tip']=='91d308cf7d882fdeb5f996c3c349d0aa6087d7d7')
ck('actual5 start owners preserved',len(claim['owners_at_primary_start'])==5 and {x['id']for x in claim['owners_at_primary_start']}==expected and all(x['owner']=='Boss4'and x['disposition']=='in-progress'for x in claim['owners_at_primary_start']))
ck('restored tracked2 untracked2 all bytes exact',len(preservation['tracked'])==2 and all(x['same']for x in preservation['tracked'])and preservation['untracked_count']==2 and not preservation['missing']and not preservation['different']and not preservation['unmerged'])
ck('preservation report SHA actual copied',sha(W/'claim-sync-preservation.json')==claim['preservation_report_sha256'])
ck('five primary manifests equal',len(rows)==5 and rows==read(W/'requested-sources.json')and {x['id']for x in rows}==expected)
ck('primary bytes12527',sum(x['size']for x in rows)==12527)
for x in rows:
 p=E/'original'/x['path'];ck('raw size '+x['id'],p.stat().st_size==x['size']);ck('raw SHA '+x['id'],sha(p)==x['sha256'])
cm=read(E/'comparison-manifest.json');ck('four current full-read comparison snapshots',len(cm)==4)
for x in cm:
 p=S/x['copied_path'];ck('comparison size '+x['path'],p.stat().st_size==x['bytes']);ck('comparison SHA '+x['path'],sha(p)==x['sha256'])
search=read(W/'pre-execution-same-sha-search.json');ck('both source programs no earlier same SHA record',len(search['programs'])==2 and all(not x['same_named_program_paths']and not x['same_sha_execution_records']for x in search['programs']))
floor_tree=ast.parse((E/'original'/rows[0]['path']).read_text());pot_tree=ast.parse((E/'original'/rows[2]['path']).read_text())
def guarded(tree):return any(isinstance(n,ast.If)and ast.unparse(n.test)=="__name__ == '__main__'"for n in tree.body)
ck('floor no main guard, potential main guard',not guarded(floor_tree)and guarded(pot_tree))
ck('floor adjacent overwrite write_text side effect',any(isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and n.func.attr=='write_text'for n in ast.walk(floor_tree)))
ck('potential original exclusive x mode',any(isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and n.func.attr=='open'and n.args and isinstance(n.args[0],ast.Constant)and n.args[0].value=='x'for n in ast.walk(pot_tree)))
ck('floor third party imports exact',any(isinstance(n,ast.Import)and any(x.name=='numpy'for x in n.names)for n in floor_tree.body)and any(isinstance(n,ast.ImportFrom)and n.module=='scipy.optimize'for n in floor_tree.body))
deps=read(E/'dependency-manifest.json');ck('real np2.3.5/scipy1.17 dependencies', {x['name']:x['version']for x in deps}=={'numpy':'2.3.5','scipy':'1.17.0'})
ck('zero external file inputs',read(E/'file-input-manifest.json')==[])
fr=read(E/'replay-floor/execution-state.json');pr=read(E/'replay-potential/execution-state.json');ck('two original calls one each exit0 assert enabled',all(x['execution_count']==x['original_program_calls']==1 and x['exit_code']==0 and x['optimize']==0 for x in [fr,pr]))
ck('source byte mirror floor',sha(E/'replay-floor/source-root'/rows[0]['path'])==rows[0]['sha256']==fr['program_sha256'])
ck('source byte mirror potential',sha(E/'replay-potential/source-root'/rows[2]['path'])==rows[2]['sha256']==pr['program_sha256'])
ck('no source local/file inputs either run',fr['external_file_inputs']==fr['local_program_imports']==pr['external_file_inputs']==pr['local_program_imports']==[])
ck('empty stderr both originals',not(E/'replay-floor/original.stderr.txt').read_bytes()and not(E/'replay-potential/original.stderr.txt').read_bytes())
fnew=E/'replay-floor/source-root'/rows[1]['path'];fold=E/'original'/rows[1]['path'];pnew=E/'replay-potential/current-owner-output.json';pold=E/'original'/rows[4]['path'];initial=E/'original'/rows[3]['path']
ck('713B floor new old stdout byte equal',fnew.read_bytes()==fold.read_bytes()==(E/'replay-floor/original.stdout.txt').read_bytes()and fnew.stat().st_size==713)
ck('floor SHAdefbab',sha(fnew)==rows[1]['sha256']==fr['report_sha256'])
ck('865B owner new old stdout byte equal',pnew.read_bytes()==pold.read_bytes()==(E/'replay-potential/original.stdout.txt').read_bytes()and pnew.stat().st_size==865)
ck('potential SHA589cd matches owner not initial',sha(pnew)==rows[4]['sha256']==pr['report_sha256']and pr['matches_frozen_report_ids']==[rows[4]['id']]and pnew.read_bytes()!=initial.read_bytes())
fd=read(fold);old=read(initial);owner=read(pold);ck('report fields floor17 Beta10 owner14',len(fd)==17 and len(old)==10 and len(owner)==14)
ck('true floor6unitclient fixture',fd['customers']==[[2,1],[4,1],[9,2],[16,1],[32,1]])
ck('floor actual034/three1/W3/OPT4',fd['path']==[0,3,4]and fd['payoffs']==['1']*3 and fd['welfare']==3 and fd['opt']==4)
ck('floor43/258/min0/gapsminus2',fd['complete_histories']==43 and fd['compared_actions']==258 and fd['smallest_exact_ic']=='0'and fd['direct_floor_gap']==fd['comparison_gap']=='-2')
ck('floor not universal separated claim',fd['status']=='not separated in this one fixed cone')
snap_path=E/'replay-floor/complete-original-built-input-and-proposal.json';snap=read(snap_path);ck('passive namespace exact scope',snap['scope']=='copy of returned original top-level namespace; no extra action/follow/utility/cov or LP calls')
ck('actual63masks and43hist keys',snap['MASKS']==list(range(1,64))and len(snap['HISTORIES'])==43 and len({tuple(x)for x in snap['HISTORIES']})==43)
ck('all258x63 exact original rows copied',len(snap['ROWS'])==258 and all(len(row)==63 for row in snap['ROWS'])and len(snap['OBJ'])==63)
counts=snap['counts'];gaps=[sum((F(v)*n for v,n in zip(row,counts)),F())for row in snap['ROWS']];ck('258 stored exact slacks all matrix consistent/nonnegative',list(map(str,gaps))==snap['exact_slacks']and min(gaps)==0)
ck('original objective dot counts matches report',sum((F(v)*n for v,n in zip(snap['OBJ'],counts)),F())==F(-2))
ck('observed rational normalization—source not asserted',snap['common_denominator']==sum(counts)==6 and sum(map(F,snap['rational_point']))==1)
ck('finite LP float coords exact hex copies',all(float(x).hex()==h for x,h in zip(snap['lp_proposal']['x_float'],snap['lp_proposal']['x_float_hex'])))
ck('actual HiGHS reported success—not exact dual',snap['lp_proposal']['success']and snap['lp_proposal']['status']==0 and snap['lp_proposal']['nit']==41)
ck('copied original output object identical',snap['original_output_object']==fd)
encoding=read(W/'snapshot-nonfinite-encoding.json');ck('63 upper residual IEEE infinities explicit string encoding',len(encoding['nonfinite_values'])==63 and all(x['encoded']=='Infinity'and x['path'][:3]==['lp_proposal','upper','residual']for x in encoding['nonfinite_values']))
ck('new snapshot SHA matches encoding note',sha(snap_path)==encoding['new_snapshot_sha256']and snap_path.stat().st_size==encoding['new_snapshot_bytes']==222572)
reverse=copy.deepcopy(snap);reverse.pop('nonfinite_float_encoding')
for x in encoding['nonfinite_values']:
 cursor=reverse
 for key in x['path'][:-1]:cursor=cursor[key]
 cursor[x['path'][-1]]=float.fromhex(x['float_hex'])
raw=(json.dumps(reverse,ensure_ascii=False,indent=2)+'\n').encode();ck('nonfinite presentation encoding byte reversible',len(raw)==encoding['original_snapshot_bytes']==222253 and hashlib.sha256(raw).hexdigest()==encoding['original_snapshot_sha256'])
project={k:v for k,v in owner.items()if k not in ['owner_minorant_checks','owner_error_identities','owner_prefix_states','owner_prefix_credit_budgets']};project['claims_checked']=project['claims_checked'][:-2]
ck('initial report semantic projection only',project==old and len(old['claims_checked'])==6 and len(owner['claims_checked'])==8)
ck('four additional owner fields only',set(owner)-set(old)=={'owner_minorant_checks','owner_error_identities','owner_prefix_states','owner_prefix_credit_budgets'})
domain=read(E/'potential-input-domain.json');formulas={'profile_client_types':sum(4**m for m in range(1,9)),'present_slot_marginals':sum(m*2**(2*m-1)for m in range(1,9)),'diminishing_return_checks':sum(comb(m,2)*2**(2*m-2)for m in range(1,9)),'prefix_query_states':sum(2**(m-1)*(2**m-1)for m in range(1,9)),'prefix_credit_budgets':sum(2**m-1 for m in range(1,9)),'owner_minorant_checks':sum(m*2**(2*m-1)for m in range(1,9)),'owner_error_identities':sum(m*2**(2*m-1)for m in range(1,9)),'owner_prefix_states':sum(2**(m-1)*(2**m-1)for m in range(1,9)),'owner_prefix_credit_budgets':sum(2**m-1 for m in range(1,9))}
for k,v in formulas.items():ck('exact reported loop-group formula '+k,owner[k]==domain['derived_counter_formulas'][k]==v)
ck('potential actualm8 and maxerror1',owner['max_m_regression_only']==8 and owner['maximum_total_client_error']=='1'and domain['actual_max_m']==8)
ck('prefix firstowner vs staticallowner recorded','min(A)'in domain['owner_prefix']and domain['owner_static']=='each owner in A separately, all static owner choices')
ck('zero SPE/globalcatalog checks recorded',domain['SPE_or_catalogue_optimality_checks']is False)
versions=read(E/'version-and-scope.json');ck('exact two runs only current owner—not initial',versions['total_original_calls']==2 and versions['initial_version_executed_this_batch']is False and versions['initial_semantic_projection_equal'])
ck('bankm5 directfloor gap1/20 exact',F(13,10)-F(5,4)==F(1,20))
objects=read(W/'objects.json');ck('two selfcontained computation objects',len(objects)==2);links=[]
for rel in objects.values():
 p=S/rel;t=p.read_text();front=t.split('---',2)[1];ck('flat metadata required '+rel,all(re.search('^'+key+':',front,re.M)for key in ['id','kind','type_tag','title','status','summary','source_refs']))
 for target in re.findall(r'\]\(([^)]+)\)',t):
  if target.startswith(('http:','https:','#')):continue
  rr=(p.parent/target.split('#')[0]).resolve().relative_to(S.resolve());ck('formal local link '+str(rr),(S/rr).exists()or(R/rr).exists());links.append({'from':rel,'target':str(rr)})
receipts=read(W/'semantic-receipts.json');ck('five exact semantic receipts',len(receipts)==5 and {x['id']for x in receipts}==expected)
for x in receipts:ck('full substantive receipt '+x['id'],all(x[k]for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])and x['disposition']=='integrated'and all(len(x[k])>60 for k in ['read_note','comparison_note','decision_note'])and all(y in objects.values()for y in x['targets']))
ck('30 math/run selfreview items',len(re.findall(r'^\d+\. ',(W/'MATHEMATICAL-SELF-CHECK.md').read_text(),re.M))==30)
ck('body only staging no false push/done',read(W/'STATUS.json')['body_save_status']=='external-staging-only; parent copy/push/done not asserted')
cs=read(W/'next-candidates.json')['candidates'];hist=read(W/'next-progress-history-check.json');ck('next5 no reachable-progress history at captured check',len(cs)==len(hist)==5 and all(x['current_progress']is None and x['reachable_history_commits_touching_progress']==[] for x in hist))
# All generated JSON is standards-compliant; solver infinity is intentionally text encoded.
def nonfinite(s):raise ValueError('nonstandard JSON literal '+s)
jsonfiles=list(S.rglob('*.json'))
ck('all JSON strictly parses without Infinity/NaN',all(json.loads(p.read_text(),parse_constant=nonfinite)is not None for p in jsonfiles))
result={'status':'PASS','scope':'artifact/source AST/existing exact matrix-copy arithmetic/version/metadata checks only; no original source imports, LP calls or Beta audit reruns','checks_passed':len(checks),'formal_local_links_checked':len(links),'mathematical_review_items':30,'json_files_strictly_parsed':len(jsonfiles),'original_program_calls_remain':2,'checks':checks,'links':links};(W/'evidence-self-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n');print(json.dumps({k:v for k,v in result.items()if k not in ['checks','links']},ensure_ascii=False))
