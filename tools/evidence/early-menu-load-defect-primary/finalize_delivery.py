from pathlib import Path
from fractions import Fraction as F
import json,hashlib,re,difflib
S=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-early-menu-load-defect-primary')
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
E=S/'tools/evidence/early-menu-load-defect-primary';W=S/'cleanup/workspaces/Boss4/r3-early-menu-load-defect-primary-next'
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
checks=[]
def ck(name,ok,detail=None):
 checks.append(dict(check=name,passed=bool(ok),**({'detail':detail} if detail is not None else {})))
 if not ok:raise AssertionError(name)
primary=load(E/'source-manifest.json');related=load(E/'related-source-manifest.json');ctx=load(E/'context-manifest.json')
for d in primary+related:
 b=(S/d['saved_path']).read_bytes()
 ck('exact original inventory bytes '+d['id'],len(b)==d['size'] and sha(b)==d['sha256'])
ck('two full primary13548B299lines',len(primary)==2 and sum(d['size'] for d in primary)==13548 and sum(len((S/d['saved_path']).read_text().splitlines()) for d in primary)==299)
claim=load(E/'actual-claim-receipt.json');wanted={d['id'] for d in primary};owners=load(E/'primary-ownership-snapshot.json')
ck('unprojected24 actual pushed synced Boss4',claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced' and len(claim['ids'])==24 and wanted<=set(claim['ids']))
ck('actual own intersection2',len(owners)==2 and {d['id'] for d in owners}==wanted and all(d['owner']=='Boss4' and d['disposition']=='in-progress' for d in owners))
supply=load(E/'actual-local-input-supply-manifest.json')
ck('exact pure local supplied2 learning_ct',set(d['id'] for d in supply['rows'] if d['group']=='learning_ct')==wanted and all(next(x for x in supply['rows'] if x['id']==d['id'])['sha256']==d['sha256'] for d in primary))
for d in ctx:
 b=(S/d['saved_path']).read_bytes()
 ck('full actual context byte binding '+d['path'],len(b)==d['bytes'] and sha(b)==d['sha256'] and d['read_scope'].startswith('full'))
obligations=load(E/'analytic-review-obligations.json')
ck('thirteen independent analytic obligations retained',len(obligations)==13 and all(d['reviewed'] and d['reason'] and d['verification'].startswith('independent algebraic') for d in obligations))
cor=load(E/'s-z-overlap-correction/correction-metadata.json')
before=(S/cor['before_path']).read_bytes();proposed=(S/cor['proposed_path']).read_bytes();patch=(S/cor['patch_path']).read_bytes()
ck('complete correction old before SHA',sha(before)==cor['before_sha256'] and len(before)==cor['before_bytes'])
ck('complete correction minimal proposed SHA',sha(proposed)==cor['after_sha256_if_applied'])
text=before.decode()
for d in cor['replacements']:
 ck('one exact minimal phrase',text.count(d['old'])==d['expected_count']==1);text=text.replace(d['old'],d['new'])
ck('only exact one phrase changed',text.encode()==proposed)
expected=''.join(difflib.unified_diff(before.decode().splitlines(True),proposed.decode().splitlines(True),fromfile='a/'+cor['canonical_path'],tofile='b/'+cor['canonical_path'],n=0))
ck('zero-context exact patch unchanged',patch==expected.encode() and sha(patch)==cor['patch_sha256'] and cor['patch_context_lines']==0)
ck('suggestion only no old canonical copy',cor['applied_to_shared_tree'] is False)
reportrow=next(d for d in related if d['id']=='dc8933a15680748913d6')
report=load(S/reportrow['saved_path']);packet=report['packet13'];fields=packet['worst_optimal_query_true_G_credits']
ck('exact report fields preserved',cor['evidence']['exact_report_fields']==fields and cor['evidence']['report_sha256']==reportrow['sha256'])
m=tau=13;CG=F(fields['current_credit'])+F(fields['last_menu_credit'])+F(fields['last_player_credit'])
ck('S/Z exact total2399/429',CG==F(fields['total_credit'])==F(2399,429))
delta=F(packet['optimal_empirical_queries']['maximum_delta']);budget=F(packet['budget'])
ck('same exact query counts and budget',packet['optimal_empirical_queries']['maximum_counts']==[1,1,1,9,0,1] and budget==F(18,13) and delta==F(1373,507))
adjusted=delta-CG/tau;excess=adjusted-budget;overlap=F(fields['overlap_credit']);after=excess-overlap/tau
ck('after S/Z only12704/5577 with excess4982/5577',adjusted==F(fields['adjusted_total_delta'])==F(12704,5577) and excess==F(fields['adjusted_excess'])==F(4982,5577))
ck('overlap441/2 normalized by13',overlap==F(441,2) and overlap/tau==F(441,26))
ck('signed after-overlap minus179225/11154',after==F(fields['overlap_adjusted_excess'])==F(-179225,11154) and cor['evidence']['checks']['after_overlap_positive_budget_slack']==str(-after))
ck('no general all-query success invented',packet['optimal_empirical_queries']['number']==2002 and packet['optimal_empirical_queries']['above_budget']==368 and F(packet['optimal_empirical_queries']['minimum_delta'])<budget)
formal=load(E/'formal-resource-manifest.json');links=[]
for d in formal:
 p=S/d['path'];b=p.read_bytes();text=b.decode()
 ck('formal final bytes '+d['path'],sha(b)==d['sha256'] and len(b)==d['bytes'])
 ck('formal flat MATEK',text.startswith('---\n') and all(re.search('^'+k+':',text,re.M) for k in ['id','kind','type_tag','title','status','summary','source_refs']))
 ck('formal all non-LF C0 zero',not [(i,c) for i,c in enumerate(b) if c<32 and c!=10])
 ck('formal trailing whitespace zero',all(line.rstrip(' \t')==line for line in text.splitlines()))
 ck('formal complete TeX and no unresolved placeholders','§' not in text and not re.search(r'@(E|CTX|[a-f0-9]{20})',text) and text.count(chr(92)+'[')==text.count(chr(92)+']'))
 ck('explicit Fq and signed defect/max distinction','记F_q(z)=' in text and 'δ(μ)可以为负' in text and 'S_0、V_0没有非负保证' in text and 'δ(μ)=−Vbar(μ)可能为负' in text)
 for target in re.findall(r'\[[^\]\n]*\]\(([^)\n]+)\)',text):
  if '://' in target or target.startswith('#'):continue
  dest=(p.parent/target.split('#')[0]).resolve();ok=dest.exists()
  if not ok:
   try:ok=(R/dest.relative_to(S)).exists()
   except ValueError:ok=False
  links.append(dict(source=d['path'],target=target,exists=ok))
ck('all relative links resolve',all(d['exists'] for d in links),dict(count=len(links)))
recovery=load(E/'derived-format-recovery.json')
recovery.update(final_formal_sha256=formal[0]['sha256'],final_formal_bytes=formal[0]['bytes'],final_all_non_LF_C0=0,final_polish='explicit Fq definition added after raw-template fix; no frozen source or mathematical run changed')
dump(E/'derived-format-recovery.json',recovery)
ck('pre-delivery formatter recovery recorded',recovery['non_LF_C0_byte_positions'] and recovery['final_all_non_LF_C0']==0 and recovery['new_original_CLI_invocations']==0)
receipts=load(W/'semantic-receipts.json')
ck('exact two primary complete receipts',len(receipts)==2 and {d['id'] for d in receipts}==wanted)
for d in receipts:
 ck('semantic completeness '+d['id'],all(d[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and all(d[k] for k in ['read_note','comparison_note','decision_note']) and d['disposition']=='integrated' and all((S/p).exists() for p in d['targets']))
cand=load(W/'next-candidates.json')
ck('four actual unclaimed local candidates only',len(cand)==4 and all(not d['local_progress_exists'] for d in cand))
dump(E/'formal-link-check.json',links)
scope=dict(primary_sources=2,primary_bytes=13548,primary_lines=299,primary_full_actual_read=True,related_sources=2,related_bytes=sum(d['size'] for d in related),related_contexts=len(ctx),related_context_bytes=sum(d['bytes'] for d in ctx),source_capture_unprojected24=True,source_supply_manifest_unmodified=True,original_CLI_invocations=0,canonical_solver_invocations=0,independent_SPE_tree_replays=0,original_2002_query_searches_rerun=0,code_ownership_respected='c3e4387bcefcaf1c8183 Boss6 in-progress observed; no own claim, read, import, run or done for it; no claim/done of351B audit JSON',validation='Complete analytic proof reconstruction; exact Fraction arithmetic of already-read report fields; byte/format/link/receipt checks, not a new numeric or SPE suite.',new_shared_Git_operations=0,new_clean_show_calls=0,new_network_or_lazy_fetch=0,new_other_source_dispositions=0,phase3='No graph/mapper/import',status_limits=['epsilon/delta point values signed; maxima nonnegative via pointA','local parameter lemma and stated structural half conditions retained; no general payment or six-player conclusion','related finite boundaries read, not reexecuted; full packet not certified anew','one old-page phrase guarded correction only, not wholesale old-page/source-done rejection'])
dump(E/'read-scope-and-evidence-status.json',scope)
# Keep frozen originals/context exactly; report any transport whitespace without normalizing it.
files=[]
for root in [S/'archives',S/'tools',S/'cleanup']:
 files.extend(p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc')
files=sorted(files)
ck('only one new canonical in white list',[p.relative_to(S).as_posix() for p in files if p.relative_to(S).parts[0]=='archives']==[formal[0]['path']])
whitespace=[]
for p in files:
 try:t=p.read_text()
 except UnicodeDecodeError:continue
 lines=[i for i,l in enumerate(t.splitlines(),1) if l.rstrip(' \t')!=l]
 if lines:whitespace.append(dict(path=p.relative_to(S).as_posix(),lines=lines,scope='preserved exact source/context if any; not new canonical'))
dump(E/'transport-whitespace-observations.json',whitespace)
selfcheck=dict(passed=True,checks=len(checks),details=checks,formal_all_non_LF_C0=0,formal_trailing_whitespace=0,relative_links_checked=len(links),scope='Bytes/actual ownership/analytic obligations/report arithmetic/correction scope/format/links/receipts; no finite suite used as proof')
dump(W/'self-check.json',selfcheck)
# Recollect to include the two files just written.
files=[]
for root in [S/'archives',S/'tools',S/'cleanup']:files.extend(p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc')
rows=[dict(path=p.relative_to(S).as_posix(),bytes=p.stat().st_size,sha256=sha(p.read_bytes())) for p in sorted(files)]
dump(S/'copy-files.json',rows);(S/'copy-paths.txt').write_text(''.join(d['path']+'\n' for d in rows))
summary=dict(stage=str(S),evidence_root=E.relative_to(S).as_posix(),workspace=W.relative_to(S).as_posix(),files=len(rows),bytes=sum(d['bytes'] for d in rows),formal_files=len(formal),formal_bytes=sum(d['bytes'] for d in formal),primary_sources=2,primary_bytes=13548,primary_lines=299,semantic_receipts=2,self_checks=len(checks),relative_links=len(links),formal_all_non_LF_C0=0,formal_trailing_whitespace=0,new_original_CLI_invocations=0,new_SPE_or_query_replays=0,copy_files_sha256=sha((S/'copy-files.json').read_bytes()),old_canonical_replacements_applied=0,old_page_suggestion_before_sha256=cor['before_sha256'],next_candidate_ids=[d['id'] for d in cand],transport_whitespace_files=len(whitespace))
dump(S/'delivery-summary.json',summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
