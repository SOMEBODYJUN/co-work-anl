"""Consistency/AST/input-domain/record checks only; no original module imports or calls."""
from pathlib import Path
from itertools import combinations
from collections import Counter
from fractions import Fraction as F
import ast,hashlib,json,re
S=Path(__file__).resolve().parents[4];W=Path(__file__).resolve().parent;E=S/'archives/customer-attraction/tools/evidence/general-proof-and-optimal-exchange-primary';R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');checks=[]
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ck(name,c):
 if not c:raise AssertionError(name)
 checks.append(name)
expected={'2cbfcd673b188e626a02','8280d79b5376e1286d68','47676cb3c54c020992fc','3909b9c94221d05ab505','b01a6cf50b5ed8462ed3'};rows=read(E/'source-manifest.json');claim=read(W/'claim-evidence.json')
ck('actual pushed Boss4 claim exact worker subset',claim['status']=='pushed'and claim['actor']=='Boss4'and set(claim['ids'])==expected and expected<=set(claim['actual_batch_ids']))
ck('synced receipt actual remote tip',claim['local_sync_status']=='synced'and claim['remote_tip']=='372a7d401e044cd87f4457e55b6ae7e79704565a')
ck('five source IDs only and requested equal',len(rows)==5 and {x['id']for x in rows}==expected and rows==read(W/'requested-sources.json'))
ck('primary byte total26831',sum(x['size']for x in rows)==26831)
for x in rows:
 p=E/'original'/x['path'];ck('original raw size '+x['id'],p.stat().st_size==x['size']);ck('original raw SHA '+x['id'],sha(p)==x['sha256'])
cm=read(E/'comparison-manifest.json');ck('nine fully read current snapshots',len(cm)==9)
for x in cm:
 p=S/x['copied_path'];ck('comparison size '+x['path'],p.stat().st_size==x['bytes']);ck('comparison SHA '+x['path'],sha(p)==x['sha256'])
ck('comparison bytes69225',sum(x['bytes']for x in cm)==69225)
ck('zero external dependencies',read(E/'dependency-manifest.json')==[])
search=read(W/'pre-execution-same-sha-search.json');ck('no previous same named code or same SHA run',search['same_named_program_files']==search['same_sha_execution_records']==[])
program=rows[2];src=E/'original'/program['path'];text=src.read_text();tree=ast.parse(text);imports={n.module for n in ast.walk(tree)if isinstance(n,ast.ImportFrom)}|{a.name for n in ast.walk(tree)if isinstance(n,ast.Import)for a in n.names}
ck('AST only six standard library modules',imports=={'fractions','itertools','math','pathlib','argparse','json'})
ck('AST exact main guard',any(isinstance(n,ast.If)and ast.unparse(n.test)=="__name__ == '__main__'"for n in tree.body))
ck('AST four original functions no strategy/payoff function', {n.name for n in tree.body if isinstance(n,ast.FunctionDef)}=={'beta','union','check_case','main'})
ck('AST exclusive output x mode',any(isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and n.func.attr=='open'and n.args and isinstance(n.args[0],ast.Constant)and n.args[0].value=='x'for n in ast.walk(tree)))
ck('original source explicit finite n/m/T/B loops','for n in range(5)'in text and 'for m in [1, 2, 3]'in text and 'combinations_with_replacement(catalogue, m)'in text and 'product(catalogue, repeat=m)'in text)
ck('realizations only m<=2 and p1/2','check_case(n, T, B, m <= 2)'in text and 'if check_realizations and p == F(1, 2)'in text)
ck('integer alpha points and sameposition anchor control','for alpha in [1, 2, 3]'in text and 'if optimum[j] != profile[j]'in text)
ck('bool counter meaning exact return','return int(left > 0), int(any(c[x] for x in J)), anchored'in text)
run=read(E/'replay/execution-state.json');ck('one original CLI call success assert enabled',run['execution_count']==run['original_program_calls']==1 and run['exit_code']==0 and run['optimize']==0)
ck('zero instrumented/extra source function calls',run['no_source_function_instrumentation']is True)
ck('actual source mirror SHA exact',sha(E/'replay/source-root'/program['path'])==program['sha256']==run['program_sha256'])
ck('zero local imports/external inputs',run['local_program_imports']==run['external_dependencies']==[])
ck('real CLI explicit unique output argument',len(run['argv'])==4 and run['argv'][2]=='--output'and Path(run['argv'][3]).name=='current-original-output.json')
new=E/'replay/current-original-output.json';old=E/'original'/rows[3]['path'];late=E/'original'/rows[4]['path'];stdout=E/'replay/original.stdout.txt';stderr=E/'replay/original.stderr.txt'
ck('current output byte equal anchor frozen only',new.read_bytes()==late.read_bytes()and new.read_bytes()!=old.read_bytes()and run['matches_frozen_reports']==[rows[4]['id']])
ck('414/378/392 three distinct byte lengths',new.stat().st_size==late.stat().st_size==414 and old.stat().st_size==378 and stdout.stat().st_size==392)
ck('new SHA exact c72f18',sha(new)==rows[4]['sha256']==run['new_report_sha256'])
ck('stdout JSON equal but bytes different',read(stdout)==read(new)and stdout.read_bytes()!=new.read_bytes()and run['json_stdout_equals_report'])
ck('stdout SHA9ffc76',sha(stdout)==run['stdout_sha256']=='9ffc767adaa3e5de99fb7839abea893478c9e455bb45385268fb0e0af021af86')
ck('empty stderr no failure',not stderr.read_bytes()and run['stderr_bytes']==0)
initial=read(old);anchor=read(late);ck('initial9 fields anchor10',len(initial)==9 and len(anchor)==10)
ck('one field anchor semantic increment only',{k:v for k,v in anchor.items()if k!='anchored_profile_checks'}==initial and set(anchor)-set(initial)=={'anchored_profile_checks'})
counts={'catalogues':806,'optimal_portfolios':6035,'paired_profiles':98125,'nonzero_outside_harmonic':1311,'covered_loss_terms':29979,'anchored_profile_checks':93908}
for k,v in counts.items():ck('actual report count '+k,anchor[k]==read(new)[k]==v)
ck('scope retains finite and no SPE claim',anchor['scope']=='explicit finite boundary replay only'and anchor['limitations']=='No SPE property or general half coverage is inferred.')
inputrows=read(E/'replay/complete-built-input-catalogues.json');expectedinput=[{'n':n,'catalogue_masks':list(c)}for n in range(5)for size in range(1,min(3,1<<n)+1)for c in combinations(range(1<<n),size)]
ck('complete806 explicit input catalogues equal specified grid',inputrows==expectedinput and len(inputrows)==806)
ck('catalogue counts per n1/3/14/92/696',dict(Counter(x['n']for x in inputrows))=={0:1,1:3,2:14,3:92,4:696})
ck('zero customer true empty theme fixture',inputrows[0]=={'n':0,'catalogue_masks':[0]})
ck('catalogue masks distinct but repeated topic profiles allowed',all(len(x['catalogue_masks'])==len(set(x['catalogue_masks']))for x in inputrows)and 'combinations_with_replacement'in text)
domain=read(E/'replay/input-domain.json');ck('full finite literal p/alpha domain',domain['bernoulli_p']==['0','1/3','1/2','2/3','1']and domain['alpha']==[1,2,3]and domain['m']==[1,2,3])
ck('no SPE external source data calls',domain['spe_calls']==0 and domain['external_file_inputs']==[])
notes=read(E/'report-version-and-domain-notes.json');ck('no false historical version run claim',notes['no_claim_initial_code_was_rerun']and notes['initial_report_semantic_projection_from_late'])
ck('finite arithmetic evaluation totals',notes['bernoulli_inequality_evaluations']==490625 and notes['alpha_inequality_evaluations']==294375 and notes['harmonic_comparisons']==notes['matching_formula_comparisons']==98125)
ck('owner absent exact unit conversion',F(1,3*4)+F(1,4)==F(1,3))
ck('nonreweighting exact minusone sixth',F(3,2)-F(2,3)-1==F(-1,6))
objects=read(W/'objects.json');ck('three formal objects',len(objects)==3);links=[]
for rel in objects.values():
 p=S/rel;t=p.read_text();front=t.split('---',2)[1];ck('flat metadata all required '+rel,all(re.search('^'+key+':',front,re.M)for key in ['id','kind','type_tag','title','status','summary','source_refs']))
 for target in re.findall(r'\]\(([^)]+)\)',t):
  if target.startswith(('https:','http:','#')):continue
  rr=(p.parent/target.split('#')[0]).resolve().relative_to(S.resolve());ck('local formal link '+str(rr),(S/rr).exists()or(R/rr).exists());links.append({'from':rel,'target':str(rr)})
receipts=read(W/'semantic-receipts.json');ck('five receipts only exact worker IDs',len(receipts)==5 and {x['id']for x in receipts}==expected)
for x in receipts:
 ck('substantive complete receipt '+x['id'],all(x[k]for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])and x['disposition']=='integrated'and all(len(x[k])>60 for k in ['read_note','comparison_note','decision_note'])and all(y in objects.values()for y in x['targets']))
ck('32 mathematical selfreview items',len(re.findall(r'^\d+\. ',(W/'MATHEMATICAL-SELF-CHECK.md').read_text(),re.M))==32)
ck('candidate status not proof', 'FLOW-and-incoming-payment-unproved'in(S/list(objects.values())[0]).read_text())
ck('body stage not saved/done assertion',read(W/'STATUS.json')['body_save_status']=='external-staging-only; parent copy/push/done not asserted')
ck('next actual5 captured available',len(read(W/'next-candidates.json')['candidates'])==5 and all(x['progress_at_candidate_check']is None for x in read(W/'next-candidates.json')['candidates']))
result={'status':'PASS','scope':'artifact consistency/AST/domain/exact arithmetic only; no import or execution of original code, no additional SPE or research scan','checks_passed':len(checks),'formal_local_links_checked':len(links),'mathematical_review_items':32,'checks':checks,'links':links};(W/'evidence-self-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k not in ['checks','links']},ensure_ascii=False))
