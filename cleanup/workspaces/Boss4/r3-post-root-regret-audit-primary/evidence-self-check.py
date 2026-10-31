"""Artifacts and exact old/new report arithmetic; no research-code imports or new IC scan."""
from pathlib import Path
from fractions import Fraction as F
import ast,hashlib,json,posixpath,re
HERE=Path(__file__).resolve().parent;STAGE=HERE.parents[3];CACHE=STAGE.parent;REPO=CACHE.parent/'boss4-research'
E=STAGE/'archives/customer-attraction/tools/evidence/post-root-regret-audit-primary'
checks=[]
def check(ok,label):
 assert ok,label
 checks.append(label)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
p=json.loads((E/'source-manifest.json').read_text());d=json.loads((E/'dependency-manifest.json').read_text());r=json.loads((E/'related-source-manifest.json').read_text())
check(len(p)==5 and sum(a['size']for a in p)==23467,'five primary sources 23467B')
check(len(d)==1 and d[0]['size']==6437,'one true embedded-data dependency 6437B')
check(len(r)==1 and r[0]['size']==4825,'one read-only related review 4825B')
for group,items in [('original',p),('dependencies',d),('related-original',r)]:
 for row in items:
  path=E/group/row['path'];check(path.stat().st_size==row['size'] and sha(path)==row['sha256'],'frozen bytes '+row['id'])
claim=json.loads((HERE/'claim-evidence.json').read_text());check(claim['status']=='pushed' and claim['actor']=='Boss4' and set(claim['ids'])=={a['id']for a in p} and claim['local_sync_status']=='synced','unique actual claim pushed actor and exact IDs')
search=json.loads((HERE/'pre-claim-local-program-search.json').read_text());check(len(search['programs'])==2 and all(not a['current_local_program_matches']for a in search['programs']),'pre-materialization local program search no prior copies')
by={Path(a['path']).name:a for a in p};summary=json.loads((E/'replay/execution-summary.json').read_text())
check(summary['original_program_calls']==2 and summary['original_program_calls_per_entry']==1 and summary['optimize']==0,'two original entries one each with asserts')
for run in summary['runs']:
 root=E/'replay'/run['case']/'source-root';program=root/run['program'];name=Path(run['program']).name
 check(run['original_program_execution_count']==1 and run['exit_code']==0 and run['stderr_bytes']==0,'one successful original call '+run['case'])
 check(sha(program)==by[name]['sha256'] and run['local_program_imports']==[],'unchanged source and no local code import '+run['case'])
 tree=ast.parse(program.read_text());imports=[n.module for n in ast.walk(tree)if isinstance(n,ast.ImportFrom)]+[a.name for n in ast.walk(tree)if isinstance(n,ast.Import)for a in n.names]
 check(all(x in ['fractions','itertools','math','pathlib','json']for x in imports),'original standard-library-only AST '+run['case'])
 check(any(isinstance(n,ast.If)and '__name__'in ast.unparse(n.test)for n in tree.body),'original guarded main '+run['case'])
 output='exchange_potential_credit_audit.json'if run['case']=='exchange'else'owner_insertion_identity_audit.json';report=program.with_name(output)
 check(report.read_bytes()==(E/'original'/by[output]['path']).read_bytes(),'report equals frozen bytes '+run['case'])
 directory=root.parent
 check((directory/'original.stdout.txt').read_bytes()==report.read_bytes() and (directory/'original.stderr.txt').stat().st_size==0,'full stdout equals report and empty stderr '+run['case'])
 for tag in ['stdout','stderr']:
  path=directory/('original.'+tag+'.txt');check(sha(path)==run[tag+'_sha256'] and path.stat().st_size==run[tag+'_bytes'],'captured '+tag+' bytes '+run['case'])
 if run['case']=='exchange':
  check(len(run['dependencies'])==1 and sha(root/d[0]['path'])==d[0]['sha256'] and program.parent.parent.parent/'round2/global/pi_fixed_cone_counterexample.json'==root/d[0]['path'],'true WORKSPACE relative dependency contract')
 else:check(run['dependencies']==[],'insertion has no external inputs')
data=json.loads((E/'dependencies'/d[0]['path']).read_text());idx=json.loads((E/'fixture-input-index.json').read_text())
check(idx['complete_data']==data and idx['hardcoded_program_m']==3 and idx['hardcoded_T']==[1,2,4],'complete input index and program constants')
check(len(data['instance']['customers'])==17 and sum(a['multiplicity']for a in data['instance']['customers'])==430 and data['instance']['players']==3,'17 types encode 430 unit customers')
actions=data['strategy']['actions'];check(len(actions)==len({tuple(a['history'])for a in actions})==43 and all(len(a['history'])<3 and all(0<=v<6 for v in a['history']) and 0<=a['action']<6 for a in actions),'complete valid 43-policy-key structure only, no IC added')
policy={tuple(a['history']):a['action']for a in actions};check([policy[()],policy[(0,)],policy[(0,3)]]==[0,3,4],'actual path read directly from policy rows')
check(len(d)==1 and not any('individual_security' in a['path']for a in d),'source_strategy old certificate not a dependency')
x=json.loads((E/'original'/by['exchange_potential_credit_audit.json']['path']).read_text());i=json.loads((E/'original'/by['owner_insertion_identity_audit.json']['path']).read_text())
check(x['status']==i['status']=='PASS','both original status fields')
check([x['pattern_checks'][z]for z in ['marginal_checks','same_leaf_checks','all_future_prefix_incidence_checks']]==[72818,21844,10795],'original three pattern counters')
check(sum(m*2**(2*m-1)for m in range(1,8))==72818 and sum(4**m for m in range(1,8))==21844 and sum(2**(m-1)*(2**m-1)for m in range(1,8))==10795,'counter closed-form arithmetic only, no mask enumeration')
check(72818-sum(m*2**(m-1)for m in range(1,8))==72049 and 21844-sum(2**m for m in range(1,8))==21590,'unreported owner-loop closed-form counts')
check(sum(2**m-1 for m in range(1,8))==247,'nonempty A mask-family arithmetic')
check(len(x['rollout_checks'])==6 and 6*3==18 and 3+6+6==15,'six prefix chains 18 specified and 15 distinct comparison slots')
vals=[]
for row in x['rollout_checks']:
 left=F(324)-F(row['initial_potential'])+F(row['query_credit'])+F(row['IC_slack']);right=F(row['cross_leaf_credit'])+F(row['deletion_potential_difference'])
 check(left==right and F(row['actual_leaf_credit'])<=row['actual_I']==214,'original ROLL arithmetic and same-leaf field '+str(row['pi']))
 vals.append(left)
check(vals.count(F(177,2))==2 and vals.count(F(271,2))==4,'two 177/2 and four 271/2 rows')
check({F(a['deletion_potential_difference'])for a in x['rollout_checks']}=={F(-16),F(37),F(31)},'formal deletion difference sign retained')
check([i[z]for z in ['profile_count_identity_checks','independent_query_count_checks']]==[18,144] and 9*2==18 and 8*2*9==144 and 8*(9+17)==208,'insertion profile/groups versus scalar evaluation arithmetic')
scope=json.loads((E/'scope-contract.json').read_text());check(not scope['exchange']['full_43_node_258_IC_scan'] and not scope['exchange']['optimality_search'] and not scope['insertion']['game_input'] and scope['original_research_program_calls']==2,'scope contract denies uncalled full validation and games')
receipts=json.loads((HERE/'semantic-receipts.json').read_text());check(len(receipts)==5 and {a['id']for a in receipts}=={a['id']for a in p},'five exact primary semantic receipt IDs')
for row in receipts:
 check(all(row[z]is True for z in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and row['disposition']=='integrated' and all(len(row[z])>80 for z in ['read_note','comparison_note','decision_note']) and all((STAGE/a).is_file()for a in row['targets']),'complete semantic receipt '+row['id'])
objects=list((STAGE/'archives/customer-attraction/state').rglob('*.md'));check(len(objects)==3,'three self-contained formal objects')
ids=[];links=0;pending=[]
for path in objects:
 t=path.read_text();check(not any(ord(c)<32 and c!='\n'for c in t),'no broken math control escapes '+path.name)
 for key in ['id','kind','type_tag','title','status','summary','source_refs']:assert re.search('^'+key+':',t,re.M),(path,key)
 ids.append(re.search(r'^id: (.+)$',t,re.M).group(1))
 refs=re.findall(r'source:([^:]+):([^\n]+)',t);check(bool(refs) and all(len(commit)==40 and commit in ['68fad804ec5946cb296f77dc5b336308a66abf12','aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c']for commit,_ in refs),'valid frozen refs '+path.name)
 for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
  if '://'in link or link.startswith('#'):continue
  rel=posixpath.normpath(str(path.relative_to(STAGE).parent/link.split('#')[0]));options=[STAGE/rel,REPO/rel]+[CACHE/b/rel for b in ['r3-post-incoming-primary-batch','r3-relay-priority-audit-contracts','r3-incoming-balance-audit-history']]
  check(any(a.exists()for a in options),'resolved local link '+link)
  if not options[0].exists()and not options[1].exists():pending.append(rel)
  links+=1
check(len(set(ids))==3,'three distinct stable object IDs')
check(len(re.findall(r'^\d+\. ',(HERE/'MATHEMATICAL-SELF-CHECK.md').read_text(),re.M))==24,'24 analytic math self-check items')
result={'status':'PASS','scope':'bytes/input structure/import AST/real original captures/old report and closed-form arithmetic/receipts/links; no source functions or new original program/IC/game/mask/permutation search invoked','checks_passed':len(checks),'links_checked':links,'analytic_math_self_check_items':24,'original_research_program_calls':2,'calls_per_entry':1,'prior_complete_stage_links':sorted(set(pending)),'checks':checks}
(HERE/'evidence-self-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k!='checks'},ensure_ascii=False))
