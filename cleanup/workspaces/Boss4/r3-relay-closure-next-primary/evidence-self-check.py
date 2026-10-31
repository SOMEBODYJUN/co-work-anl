"""Artifact and closed-form/report arithmetic checks, no original functions or new event/game scan."""
from pathlib import Path
from fractions import Fraction as F
import ast,hashlib,json,posixpath,re
HERE=Path(__file__).resolve().parent;STAGE=HERE.parents[3];CACHE=STAGE.parent;REPO=CACHE.parent/'boss4-research'
E=STAGE/'archives/customer-attraction/tools/evidence/relay-closure-next-primary'
checks=[]
def check(ok,label):
 assert ok,label
 checks.append(label)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
primary=json.loads((E/'source-manifest.json').read_text());related=json.loads((E/'related-source-manifest.json').read_text());deps=json.loads((E/'dependency-manifest.json').read_text())
check(len(primary)==5 and sum(a['size']for a in primary)==21153,'five primary originals 21153B')
check(len(related)==1 and related[0]['size']==17219,'one root-related complete original 17219B')
check(deps==[],'zero external original-program data dependencies')
for group,items in [('original',primary),('related-original',related)]:
 for row in items:
  path=E/group/row['path'];check(path.stat().st_size==row['size'] and sha(path)==row['sha256'],'frozen bytes '+row['id'])
claim=json.loads((HERE/'claim-evidence.json').read_text());check(claim['status']=='pushed' and claim['actor']=='Boss4' and set(claim['ids'])=={a['id']for a in primary} and claim['local_sync_status']=='synced','actual unique claim pushed actor IDs synced')
pre=json.loads((HERE/'pre-claim-local-program-search.json').read_text());prior=json.loads((HERE/'pre-execution-same-sha-search.json').read_text())
check(pre['same_named_program_files']==[] and prior['matching_execution_records']==[],'pre-entry same-name and exact-SHA local execution search empty')
by={Path(a['path']).name:a for a in primary};src=next(a for a in primary if a['path'].endswith('.py'));state=json.loads((E/'replay/execution-state.json').read_text());program=E/'replay/source-root'/src['path']
check(state['execution_count']==state['original_program_calls']==1 and state['exit_code']==0 and state['optimize']==0,'one successful original entry with asserts')
check(sha(program)==src['sha256'] and state['program_bytes']==4251,'unchanged original 4251B replay source')
check(state['local_program_imports']==state['external_dependencies']==[],'no root shared imports or external data')
tree=ast.parse(program.read_text());imports=[n.module for n in ast.walk(tree)if isinstance(n,ast.ImportFrom)]+[a.name for n in ast.walk(tree)if isinstance(n,ast.Import)for a in n.names]
check(all(a in ['fractions','itertools','math','pathlib','json']for a in imports),'original standard-library-only import AST')
check(any(isinstance(n,ast.If)and '__name__'in ast.unparse(n.test)for n in tree.body),'original guarded main')
check(not any(isinstance(n,ast.Attribute)and n.attr in ['read_text','read_bytes','load']for n in ast.walk(tree)),'no original input-reader method or json load')
report=program.with_name('optimal_exchange_review_audit.json');frozen=E/'original'/by[report.name]['path'];stdout=E/'replay/original.stdout.txt';stderr=E/'replay/original.stderr.txt'
check(report.read_bytes()==frozen.read_bytes() and report.stat().st_size==655,'new 655B report equals original bytes')
check(stdout.read_bytes()==report.read_bytes() and stderr.stat().st_size==0,'full stdout identical and empty stderr')
for tag,path in [('stdout',stdout),('stderr',stderr)]:check(sha(path)==state[tag+'_sha256'] and path.stat().st_size==state[tag+'_bytes'],'captured '+tag+' bytes and hash')
r=json.loads(report.read_text());scope=json.loads((E/'scope-contract.json').read_text())
check(r['status']=='PASS' and [r[k]for k in ['bernoulli_event_checks','random_position_matching_checks','positive_rational_alpha_checks']]==[5460,91,45],'actual reported three counters')
check(4*sum(4**m for m in range(6))==5460 and 4*sum(8**m for m in range(6))==149796,'event and word closed-form arithmetic, no words enumerated')
check(sum((m+1)**2 for m in range(6))==91 and 9*5==45,'position and parameter counter arithmetic')
check(scope['event_m_values']==list(range(6)) and scope['event_p_values']==['0','1/7','1/2','1'],'exact original event constant domains')
check(scope['kernel_c_values']==list(range(9)) and scope['positive_alpha_values']==['1/101','1/3','1/2','1','7/3'],'exact original parameter constant domains')
check(scope['alpha_zero_direct_extension_checks']==9 and len(scope['complete_anchor_m_values'])==7 and scope['random_matching_is_c_subsets_not_factorial_permutations'],'zero extension and complete-zero-anchor scope')
check(scope['global_optimality_BER_inequality_tested']is False and scope['game_or_policy_input']is False and scope['SPE_IC_validation_calls']==0 and scope['original_program_calls']==1,'scope denies uncalled global game SPE FLOW checks')
check(F(2,2)-1==0 and F(3,2)-F(2,3)-1==F(-1,6)==F(r['ic_beta_reweighting']),'source local terminal IC integral arithmetic only')
check('No SPE-to-FLOW or HALF' in r['limitation'] and 'Exact event and boundary' in r['scope'],'original limitation preserved')
receipts=json.loads((HERE/'semantic-receipts.json').read_text());check(len(receipts)==5 and {a['id']for a in receipts}=={a['id']for a in primary},'five exact primary receipt IDs')
for row in receipts:
 check(all(row[k]is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and row['disposition']=='integrated' and all(len(row[k])>=80 for k in ['read_note','comparison_note','decision_note']) and all((STAGE/a).is_file()for a in row['targets']),'full semantic receipt '+row['id'])
objects=list((STAGE/'archives/customer-attraction/state').rglob('*.md'));check(len(objects)==3,'three self-contained formal objects')
ids=[];links=0;pending=[]
for path in objects:
 t=path.read_text();check(not any(ord(c)<32 and c!='\n'for c in t),'no broken math control escapes '+path.name)
 for key in ['id','kind','type_tag','title','status','summary','source_refs']:assert re.search('^'+key+':',t,re.M),(path,key)
 ids.append(re.search(r'^id: (.+)$',t,re.M).group(1))
 refs=re.findall(r'source:([^:]+):([^\n]+)',t);check(bool(refs)and all(len(commit)==40 and commit in ['68fad804ec5946cb296f77dc5b336308a66abf12','aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c']for commit,_ in refs),'valid frozen refs '+path.name)
 for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
  if '://'in link or link.startswith('#'):continue
  rel=posixpath.normpath(str(path.relative_to(STAGE).parent/link.split('#')[0]));options=[STAGE/rel,REPO/rel]+[CACHE/b/rel for b in ['r3-post-root-regret-audit-primary','r3-post-incoming-primary-batch','r3-relay-priority-audit-contracts']]
  check(any(a.exists()for a in options),'resolved local link '+link)
  if not options[0].exists()and not options[1].exists():pending.append(rel)
  links+=1
check(len(set(ids))==3,'three distinct stable object IDs')
check(len(re.findall(r'^\d+\. ',(HERE/'MATHEMATICAL-SELF-CHECK.md').read_text(),re.M))==24,'24 analytic math self-check items')
result={'status':'PASS','scope':'bytes/import AST/real-run capture/counter closed forms/primary local Fraction arithmetic/receipts/links only; no original functions or new event/game/SPE/flow calls','checks_passed':len(checks),'links_checked':links,'analytic_math_self_check_items':24,'original_research_program_calls':1,'SPE_IC_validation_calls':0,'prior_complete_stage_links':sorted(set(pending)),'checks':checks}
(HERE/'evidence-self-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k!='checks'},ensure_ascii=False))
