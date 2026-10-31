"""Read-only raw-byte, recorded-recursion, source-label, link and whitelist validation."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import ast,hashlib,json,re
S=Path(__file__).resolve().parents[4];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');E=S/'archives/customer-attraction/tools/evidence/uniform-tax-and-pi-review-primary';W=Path(__file__).resolve().parent
checks=[]
def ck(n,v):
 if not v:raise AssertionError(n)
 checks.append(n)
def J(p):return json.loads(p.read_text(),parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
M=J(E/'source-manifest.json');T=J(W/'target-paths.json');D=J(E/'dependency-manifest.json');c=J(W/'claim-evidence.json');auth=J(W/'primary-authorization-check.json')
ck('exact-five-source-IDs',set(x['id']for x in M)=={'f8a2d95ea6658e4e3315','ee5f6fb57921123d8228','90dc474ead88b2d29be2','f7001370bfa3b1824d3d','7902279cb42f3340025d'})
ck('raw-source-total24550',sum(x['size']for x in M)==24550)
for x in M:
 p=E/'original'/x['path'];b=p.read_bytes();ck('source-full-byte-'+x['id'],len(b)==x['size']and sha(p)==x['sha256']and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'])
ck('claim-full13-pushed-synced-Boss4',len(c['ids'])==13 and c['status']=='pushed'and c['actor']=='Boss4'and c['local_sync']['status']=='synced')
ck('actual-five-intersection-not-projection',set(auth['expected_ids'])==set(x['id']for x in M)==set(auth['expected_actual_intersection'])and set(auth['expected_ids'])<=set(c['ids'])and auth['actual_claim_ids_count']==13)
ck('claim-tip1c4860',auth['remote_tip']==c['remote_tip']==c['local_sync']['remote_tip']=='1c4860b9f57b416991e61406d1a83272a605470c')
ck('original-capture-byte-identical',Path(auth['original_capture']).read_bytes()==(W/'claim-evidence.json').read_bytes()and sha(W/'claim-evidence.json')==auth['original_capture_sha256'])
ck('start-owner-gate',len(auth['owners_at_primary_start'])==5 and all(x['owner']=='Boss4'and x['disposition']=='in-progress'and x['source_sha256']==next(y['sha256']for y in M if y['id']==x['id'])for x in auth['owners_at_primary_start']))
local=J(W/'local-source-cache-manifest.json');ck('true-local-five-inputs',len(local['rows'])==5 and all(x['group']=='submarkov_dc'for x in local['rows']))
for x in local['rows']:ck('local-cache-SHA-'+x['id'],sha(Path(x['local_path']))==x['sha256'])
ck('sameSHA-no-prior-success',J(W/'pre-execution-same-sha-search.json')['matching_execution_records']==[])
ck('two-true-dependencies6435',len(D)==2 and sum(x['size']for x in D)==6435)
for x in D:ck('dependency-byte-'+x['id'],sha(S/x['copied_path'])==x['sha256']and(S/x['copied_path']).stat().st_size==x['size'])
src=next(x for x in M if x['path'].endswith('.py'));code=(E/'original'/src['path']).read_text();tree=ast.parse(code)
ck('no-main-guard',not any(isinstance(n,ast.If)and '__main__'in ast.unparse(n.test)for n in ast.walk(tree)))
ck('only-standard-library-imports',{n.module for n in ast.walk(tree)if isinstance(n,ast.ImportFrom)}|{x.name for n in ast.walk(tree)if isinstance(n,ast.Import)for x in n.names}=={'fractions','functools','itertools','pathlib','json'})
state=J(E/'replay/execution.json');obs=J(E/'replay/passive-observation.json');interpret=J(E/'passive-event-interpretation.json');reportpath=E/state['output_path'];report=J(reportpath)
ck('one-original-run-success-assertions-on',state['source_invocations']==1 and state['returncode']==0 and state['optimize']==0 and state['extra_original_function_calls']==0)
ck('source-byte-identical-in-mirror',sha(E/'replay/source-root'/src['path'])==src['sha256']==state['source_sha256'])
ck('original-ROOT-path-contract',(E/'replay/source-root'/src['path']).parent.parents[5]==E/'replay/source-root'and state['cwd']==state['original_ROOT']==str(E/'replay/source-root'))
ck('no-local-program-or-thirdparty-imports',state['local_program_imports']==state['third_party_libraries']==[])
ck('real-two-mirrored-file-inputs',{x['id']for x in state['true_file_inputs']}==set(x['id']for x in D))
for x in state['true_file_inputs']:ck('mirror-input-'+x['id'],sha(E/'replay/source-root'/x['path'])==x['sha256'])
frozen=E/'original'/next(x['path']for x in M if x['id']=='90dc474ead88b2d29be2')
ck('1230B-output-SHA-and-frozen-match',reportpath.stat().st_size==1230 and sha(reportpath)==state['output_sha256']=='766b72286306349133cd31db079f75aa20ab727948b7326814c87ddd06304bc7'and reportpath.read_bytes()==frozen.read_bytes())
ck('1230B-stdout-byte-equals-report',state['stdout_equals_output_bytes']and(E/'replay/stdout.txt').read_bytes()==reportpath.read_bytes()and state['stdout_bytes']==1230)
ck('empty-stderr',(E/'replay/stderr.txt').stat().st_size==0)
ck('output-object-matches-original-passive-return',obs['original_output']==report)
ck('original34-units-and43-keys',len(obs['expanded_unit_likes'])==34 and {tuple(x['history'])for x in obs['original_actions']}=={h for d in range(3)for h in product(range(6),repeat=d)})
ck('258-original-IC-records',len(obs['original_IC_slacks'])==258 and min(map(F,obs['original_IC_slacks']))==0)
ck('raw-six-passive-line-events-actual-three-lambda',len(obs['per_lambda'])==state['passive_lambda_snapshots']==6 and interpret['raw_line_events']==6 and interpret['distinct_lambda_executions']==3)
actions={tuple(x['history']):x['action']for x in obs['original_actions']};expected={(a,)for a in range(6)}|{(a,b)for a in range(6)for b in range(6)}
for n,i in enumerate([0,2,4]):
 a,b=obs['per_lambda'][i:i+2];row=report['scaled_checks'][n]
 ck('identical-observed-pair-'+str(n),a==b and a['lambda']==row['lambda']==['1/2','2/3','1'][n])
 nodes={tuple(x['history']):x for x in a['nodes']};ck('exact42-node-domain-'+a['lambda'],set(nodes)==expected and a['scaled_comparisons']==252 and len(a['prescribed_suffix_regret_sums'])==42)
 for j,(h,x)in enumerate(nodes.items()):
  child=h+(actions[h],);nextC=F(nodes[child]['remaining_credit'])if len(child)<3 else F();tax=F(x['current_tax']);reg=F(x['regret']);credit=F(x['remaining_credit']);suffix=F();hh=h
  while len(hh)<3:suffix+=F(nodes[hh]['regret']);hh=hh+(actions[hh],)
  ck('recorded-prescribed-Rec-'+a['lambda']+'-'+str(j),reg>=0 and tax>=reg and credit==tax+nextC and reg+nextC<=credit and suffix==F(a['prescribed_suffix_regret_sums'][j])<=credit)
 ck('actual-regret-max-'+a['lambda'],max(F(x['regret'])for x in nodes.values())==F(row['max_one_step_profit_regret'])and max(map(F,a['prescribed_suffix_regret_sums']))==F(row['max_prescribed_suffix_regret_sum']))
ck('positive-scaled-profit-regrets',report['scaled_checks'][0]['max_one_step_profit_regret']=='3/4'and report['scaled_checks'][1]['max_one_step_profit_regret']=='31/70')
ck('exact-three-budget-maxima',[x['max_tax_budget']for x in report['scaled_checks']]==['23/6','481/210','0'])
ck('zero-core-honest-limited-run',obs['common_core_units']==interpret['common_core_units']==0 and interpret['common_core_positive_case_executed']is False)
for x in J(E/'related-CV-manifest.json'):ck('related-CV-byte-'+Path(x['copied_path']).name,sha(S/x['copied_path'])==x['sha256']and(S/x['copied_path']).stat().st_size==x['bytes'])
cor=J(E/'source-corrections-and-history.json');lab=cor['README_prefix_label']
ck('A-not-B-label-correction',lab['true_topics']==['L0','A','B','L1','L2','L3']and lab['correct_drop_prefix_label']=='A'and lab['correct_drop_prefix_index']==1 and F(lab['delta_before'])-F(lab['delta_after_A'])==F(lab['drop'])==F(5,12)and lab['delta_after_B']==lab['delta_before'])
p=cor['balanced_PI430'];ck('balanced430-ell0-k8',F(p['P3'])-F(p['root_standalone_potential'])==F(p['tail_phi_with_root_increment'])and F(p['P2'])-F(p['tail_phi_without_root'])==F(p['k'])==8 and F(p['Delta3'])-F(p['ell'])+F(p['k'])==F(p['root_profit'])==91 and F(p['Delta4'])-F(p['root_profit'])==F(p['failure_gap'])==F(33,2))
h=cor['old_high_player_numbers'];ck('old13-displayed-rational-differences-only',F(h['13player_P13'])-F(h['13player_P12'])==F(h['13player_P14'])-F(h['13player_P13'])==F(5,2)and h['old_packet_matrix_and_full_strategy_not_reread_or_executed']is True)
ck('old8-displayed-rational-difference-only',F(h['8player_P9'])-F(h['8player_P8'])==F(h['difference'])==F(16,5)and F(h['reported_root'])-F(h['difference'])==F(1,20))
for x in J(E/'comparison-manifest.json'):ck('comparison-raw-'+Path(x['path']).stem,sha(S/x['copied_path'])==x['sha256']and(S/x['copied_path']).stat().st_size==x['bytes'])
receipts=J(W/'semantic-receipts.json');ck('exact-five-semantic-receipts',len(receipts)==5 and set(x['id']for x in receipts)==set(x['id']for x in M))
for x in receipts:ck('complete-receipt-'+x['id'],all(x[k]is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])and x['disposition']=='integrated'and all(len(x[k])>40 for k in ['read_note','comparison_note','decision_note'])and all(t in T and(S/t).exists()for t in x['targets']))
ck('44-manual-math-items',len(re.findall(r'^\d+\. ',(W/'mathematical-self-review.md').read_text(),re.M))==44)
ck('10-human-semantic-relations',len(J(W/'relation-review.json')['relations'])==10)
nexts=J(W/'next-candidates.json')['candidates'];ck('five-local-next-no-false-history',len(nexts)==5 and all(not x['availability_readonly']['progress_file_exists']and x['availability_readonly']['history_checked']is False for x in nexts))
links=[];ids=[]
for rel in T:
 p=S/rel;s=p.read_text();front=s.split('---',2)[1];ck('MATEK-flat-'+p.name,all(re.search(r'^'+k+r':',front,re.M)for k in ['id','kind','type_tag','title','status','summary','source_refs']));ids.append(re.search(r'^id: (.+)$',front,re.M).group(1));ck('no-source-placeholders-'+p.name,'SOURCE_'not in s)
 for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)',s):
  if dest.startswith(('https:','http:','#','source:')):continue
  q=(p.parent/dest.split('#')[0]).resolve();rr=q.relative_to(S);ck('formal-link-'+str(len(links)),q.exists()or(R/rr).exists());links.append({'from':rel,'to':str(rr)})
ck('three-distinct-formal-IDs',len(T)==len(set(ids))==3)
ck('scope-no-false-general-proof',all(x in (S/T[0]).read_text()for x in ['PI已假','不是B','恒主题','没有重新取回'])and all(x in (S/T[1]).read_text()for x in ['本次该审查程序执行0','80<91','未在本批从精确定义重判']))
actual=sorted(str(p.relative_to(S))for p in S.rglob('*')if p.is_file());manifest=J(W/'copy-files.json');ck('exact-sorted-whitelist-self-inclusive',manifest==actual and len(manifest)==len(set(manifest))and str((W/'copy-files.json').relative_to(S))in manifest)
ck('safe-relative-white-list',all(not Path(x).is_absolute()and '..'not in Path(x).parts for x in manifest))
for p in S.rglob('*.json'):J(p)
ck('strict-finite-JSON-everywhere',True)
result={'status':'pass','scope':'read-only hashes, recorded prescribed Rec, corrections arithmetic, links and whitelist; no original source/solver/LP calls','checks_count':len(checks),'checks':checks,'formal_links_count':len(links),'formal_links':links,'formal_objects':3,'primary_receipts':5,'original_program_calls_in_batch':1,'original_program_calls_in_selfcheck':0,'mixed_PI_review_program_calls_in_batch':0,'tail_author_tax_program_calls_in_batch':0,'actual_lambda_values':3,'raw_duplicate_line_events':6,'original_IC_checks':258,'scaled_comparisons':756,'human_math_items':44,'human_relations':10}
(W/'selfcheck.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k not in ['checks','formal_links']},ensure_ascii=False))
