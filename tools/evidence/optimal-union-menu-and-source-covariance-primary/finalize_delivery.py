from pathlib import Path
from fractions import Fraction as F
import json,hashlib,re
S=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-optimal-union-menu-and-source-covariance-primary')
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
E=S/'tools/evidence/optimal-union-menu-and-source-covariance-primary';W=S/'cleanup/workspaces/Boss4/r3-optimal-union-menu-and-source-covariance-primary-next'
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
checks=[]
def ck(n,v,detail=None):
 checks.append(dict(check=n,passed=bool(v),**({'detail':detail} if detail is not None else {})))
 if not v:raise AssertionError(n)
primary=load(E/'source-manifest.json');related=load(E/'related-source-manifest.json');byid={d['id']:d for d in primary+related}
for d in primary+related:
 b=(S/d['saved_path']).read_bytes()
 ck('exact inventory bytes '+d['id'],len(b)==d['size'] and sha(b)==d['sha256'])
 ck('exact local blobSHA1 '+d['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==d['blob'])
ck('full four primary19776B307lines',len(primary)==4 and sum(d['size'] for d in primary)==19776 and sum(len((S/d['saved_path']).read_text().splitlines()) for d in primary)==307)
ck('full three related22863B only comparison',len(related)==3 and sum(d['size'] for d in related)==22863 and all(d['scope'].startswith('entire actual related') for d in related))
authority=Path('/workspace/scratch/37f0f9248cfc/boss4-r3-refill13dbdcdd-claim.json')
capture=load(E/'actual-claim-receipt.json');wanted={d['id'] for d in primary}
ck('actual original13 capture full byte preserved',capture['status']=='pushed' and capture['actor']=='Boss4' and capture['local_sync']['status']=='synced' and len(capture['ids'])==13 and wanted<=set(capture['ids']) and (E/'actual-claim-receipt.json').read_bytes()==authority.read_bytes())
owner=load(E/'primary-ownership-snapshot.json')
ck('actual four ownerBoss4 in-progress and SHA',len(owner)==4 and {d['id'] for d in owner}==wanted and all(d['owner']=='Boss4' and d['disposition']=='in-progress' and d['source_sha256']==byid[d['id']]['sha256'] for d in owner))
supply=load(E/'actual-local-input-supply-manifest.json');rows=supply.get('rows',supply) if isinstance(supply,dict) else supply
ck('learning_dd actual supplied intersection4',{d['id'] for d in rows if d['group']=='learning_dd'}==wanted)
provenance=load(E/'local-provenance-status.json')
ck('authorized preread then actual primary stage',provenance['primary_pre_read_before_claim'].startswith('explicitly authorized') and provenance['primary_staged_after_actual_claim'] and provenance['all_original_bytes_preserved'])
ck('no helper/Git/clean show/network run',all(provenance[k]==0 for k in ['this_agent_helper_executions','this_agent_Git_reads_or_writes','clean_show_calls','network_or_lazy_fetch_calls']))
export=load(E/'root-related-local-export-manifest.json')
ck('root provided three complete local inputs no miss',len(export['rows'])==3 and export['missing']==[] and {d['id'] for d in export['rows']}=={d['id'] for d in related})
ctx=load(E/'context-manifest.json')
for d in ctx:
 b=(S/d['saved_path']).read_bytes()
 ck('full actual formal context '+d['path'],len(b)==d['bytes'] and sha(b)==d['sha256'] and d['read_scope'].startswith('full actual formal'))
ck('three contexts25736B',len(ctx)==3 and sum(d['bytes'] for d in ctx)==25736)
obligations=load(E/'analytic-obligations.json')
ck('sixteen semantic/analytic obligations present',len(obligations)==16 and all(d['reviewed'] and d['reason'] and d['method'].startswith('complete analytic') for d in obligations))
review=(S/byid['f8b0639179fa0be8698a']['saved_path']).read_text()
current=(S/byid['37817148989a4881cf37']['saved_path']).read_text()
ck('historical r definition issue versus corrected current main','需要补一句' in review and '对所有 x∈a，定义' in current and 'I 及其他客户必须保留其真实完整负载' in current)
ck('later mass and owner-lottery sections distinguished','## 6. 可覆盖停止质量的另一个 action law' in current and '## 7. Hybrid 替换槽与真实付款 role 可分离' in current and '§§1–4' in review)
# Exact arithmetic for the explanatory legal distribution, not a strategy or solver run.
C=(F(1,3)+F(1,4))/2;D=(F(1,2)+F(1,3))/2
h=C;nmean=F(5,2);V=nmean*h-(F(2,3)+F(3,4))/2
Tsrc=(F(1,6)+F(1,12))/2;diag=F(1,4)/6+F(1,4)/12
oldbound=V-Tsrc;newbound=F(3,8)*V-diag
ck('exact explanatory source-tax comparison',C==F(7,24) and D==F(5,12) and V==F(1,48) and Tsrc==F(1,8) and diag==F(1,16) and oldbound==F(-5,48) and newbound==F(-7,128) and oldbound<newbound and C-D<=oldbound)
dump(E/'source-tax-bound-comparison.json',dict(scope='Direct exact evaluation of a legal non-SPE algebraic distribution; not an original program or finite strategy search',m=3,columns=['A,A,B','A,A,A'],probabilities=['1/2','1/2'],source='A in both',A='one customer',B='empty',C=str(C),D=str(D),V=str(V),T_src=str(Tsrc),diagonal=str(diag),C_minus_D=str(C-D),old_INT_bound=str(oldbound),three_eighths_diagonal_bound=str(newbound),conclusion='Keep both full bounds; improved bare V coefficient does not pointwise dominate old negative source tax'))
formal=load(E/'formal-resource-manifest.json');links=[];bad=[];trail=[]
for d in formal:
 p=S/d['path'];b=p.read_bytes();text=b.decode()
 ck('formal exact bytes '+d['path'],len(b)==d['bytes'] and sha(b)==d['sha256'])
 ck('formal flat MATEK '+d['path'],text.startswith('---\n') and all(re.search('^'+k+':',text,re.M) for k in ['id','kind','type_tag','title','status','summary','source_refs']))
 c0=[(i,c) for i,c in enumerate(b) if c<32 and c!=10];bad+=c0
 whitespace=[i for i,l in enumerate(text.splitlines(),1) if l.rstrip(' \t')!=l];trail+=whitespace
 ck('formal all nonLF C0 zero '+d['path'],not c0)
 ck('formal trailing whitespace zero '+d['path'],not whitespace)
 ck('formal TeX/paths complete '+d['path'],'§' not in text and not re.search(r'@(E|P[0-9]|CTX|[0-9a-f]{20})',text) and text.count(chr(92)+'[')==text.count(chr(92)+']'))
 for target in re.findall(r'\[[^\]\n]*\]\(([^)\n]+)\)',text):
  if '://' in target or target.startswith('#'):continue
  dest=(p.parent/target.split('#')[0]).resolve();exists=dest.exists()
  if not exists:
   try:exists=(R/dest.relative_to(S)).exists()
   except ValueError:exists=False
  links.append(dict(source=d['path'],target=target,exists=exists))
texts=[(S/d['path']).read_text() for d in formal]
ck('META candidate retains payment open and complete Y notation','|Y_i(A)|=m-i' in texts[0] and 'PAY是尚未证明的充分条件' in texts[0] and 'q_{Q_p}一般不等于p' in texts[0])
ck('old source tax not dropped by three8 label','两条带不同负项的完整上界并不逐点有统一强弱' in texts[0] and '−5/48' in texts[0] and '−7/128' in texts[0])
ck('3/8 proof integer and nonSPE sharpness preserved','Δ≥2' in texts[1] and '不是一个非退化分布必取等' in texts[1] and 'sqrt(3)' in texts[1] and '对角严格余项' in texts[1])
ck('frontier exact half balance distinguished','恰等价half' in texts[2] and '不与half自动等价' in texts[0] and '不能将其“未发现异议”自动扩到后加章节' in texts[2])
ck('all actual relative links resolve',all(d['exists'] for d in links),dict(count=len(links)))
receipts=load(W/'semantic-receipts.json')
ck('exact four primary receipts only',len(receipts)==4 and {d['id'] for d in receipts}==wanted)
for d in receipts:
 ck('complete semantic receipt '+d['id'],all(d[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and all(d[k] for k in ['read_note','comparison_note','decision_note']) and d['disposition']=='integrated' and all((S/p).exists() for p in d['targets']))
cand=load(W/'next-candidates.json')
ck('five actual currently unowned metadata candidates',len(cand)==5 and all(not d['local_progress_exists'] for d in cand))
scope=dict(primary_sources=4,primary_bytes=19776,primary_lines=307,primary_full_actual_read=True,related_original_sources=3,related_bytes=22863,formal_contexts=3,formal_context_bytes=25736,new_original_CLI_calls=0,new_SPE_or_strategy_replays=0,new_finite_scans=0,new_shared_Git_writes=0,this_agent_Git_reads=0,this_agent_local_export_helper_calls=0,new_clean_show=0,new_network_or_lazy_fetch=0,new_other_source_claim_or_done=0,mathematical_validation='Complete analytic reconstruction of identities, pair bound and review interfaces; one exact report-free illustrative algebraic evaluation, no computational universal inference',external_import='Standard finite-dimensional Brouwer fixed-point theorem explicitly named with the concrete continuous map; no external paper retrieved or review/novelty claim',version_boundaries=['README three8 review-pending is historical; actual independent proof read','current first-saturation already defines r for all clients; no repeated patch','stored frontier review not inherited by later mass/owner-lottery','Y excludes current A for exact complete-column identity','bare3/8 coefficient bound does not erase old negative source tax'],general_status='META/TREE-PAY and frontier funds not closed;3/8 algebra theorem not SPE welfare payment',phase3='No graph/mapper/forced connection')
dump(E/'read-scope-and-evidence-status.json',scope);dump(E/'formal-link-check.json',links)
files=[]
for root in [S/'archives',S/'tools',S/'cleanup']:
 files.extend(p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc')
ck('only three new canonical outputs',[p.relative_to(S).as_posix() for p in sorted(files) if p.relative_to(S).parts[0]=='archives']==sorted(d['path'] for d in formal))
whitespace=[]
for p in files:
 try:t=p.read_text()
 except UnicodeDecodeError:continue
 lines=[i for i,l in enumerate(t.splitlines(),1) if l.rstrip(' \t')!=l]
 if lines:whitespace.append(dict(path=p.relative_to(S).as_posix(),lines=lines,scope='exact frozen source/context preserved; not normalized'))
dump(E/'transport-whitespace-observations.json',whitespace)
dump(W/'self-check.json',dict(passed=True,checks=len(checks),details=checks,formal_all_nonLF_C0=len(bad),formal_trailing_whitespace=len(trail),relative_links_checked=len(links),scope='Actual local source bytes/claim/owner, explicit analytic obligations, precise source-tax example, version distinctions, format/links/receipts; no counts substitute proof'))
files=[]
for root in [S/'archives',S/'tools',S/'cleanup']:files.extend(p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc')
rows=[dict(path=p.relative_to(S).as_posix(),bytes=p.stat().st_size,sha256=sha(p.read_bytes())) for p in sorted(files)]
dump(S/'copy-files.json',rows);(S/'copy-paths.txt').write_text(''.join(d['path']+'\n' for d in rows))
summary=dict(stage=str(S),evidence_root=E.relative_to(S).as_posix(),workspace=W.relative_to(S).as_posix(),files=len(rows),bytes=sum(d['bytes'] for d in rows),formal_files=3,formal_bytes=sum(d['bytes'] for d in formal),primary_sources=4,primary_bytes=19776,primary_lines=307,semantic_receipts=4,self_checks=len(checks),relative_links=len(links),formal_all_nonLF_C0=0,formal_trailing_whitespace=0,new_original_CLIs=0,new_finite_strategy_scans=0,transport_whitespace_files=len(whitespace),existing_canonical_replacements=0,copy_files_sha256=sha((S/'copy-files.json').read_bytes()),next_candidate_ids=[d['id'] for d in cand])
dump(S/'delivery-summary.json',summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
