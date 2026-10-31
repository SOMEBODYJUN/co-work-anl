"""Artifact/input-structure checks only; does not execute research code or an IC/search."""
from pathlib import Path
import ast, hashlib, json, posixpath, re
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent; STAGE=HERE.parents[3]; CACHE=STAGE.parent;REPO=CACHE.parent/'boss4-research'
E=STAGE/'archives/customer-attraction/tools/evidence/incoming-balance-audit-history-primary'
checks=[]
def check(ok,label):
 assert ok,label
 checks.append(label)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
primary=json.loads((E/'source-manifest.json').read_text());deps=json.loads((E/'dependency-manifest.json').read_text());related=json.loads((E/'related-source-manifest.json').read_text())
check(len(primary)==5 and sum(r['size']for r in primary)==16871,'five primary sources 16871B')
check(len(deps)==4 and sum(r['size']for r in deps)==30256,'four true dependencies 30256B')
check(len(related)==1 and related[0]['size']==6098,'one comparison original 6098B not primary done')
for group,rows in [('original',primary),('dependencies',deps),('related-original',related)]:
 for r in rows:
  p=E/group/r['path'];check(p.stat().st_size==r['size'] and sha(p)==r['sha256'],'frozen source bytes '+r['id'])
byn={Path(r['path']).name:r for r in primary};src=byn['audit_incoming_slack_transport.py']; tree=ast.parse((E/'original'/src['path']).read_text())
imports=[n.module for n in ast.walk(tree)if isinstance(n,ast.ImportFrom)]+[a.name for n in ast.walk(tree)if isinstance(n,ast.Import)for a in n.names]
check(all(x in ['collections','fractions','itertools','pathlib','argparse','json']for x in imports),'only standard library original imports')
check(any(isinstance(n,ast.If) and '__name__'in ast.unparse(n.test)for n in tree.body),'original main guard present')
state=json.loads((E/'replay/execution-state.json').read_text());rt=E/'replay/source-root';program=rt/src['path']
check(state['execution_count']==state['original_program_calls']==1 and state['exit_code']==0 and state['optimize']==0,'one successful original entry with asserts')
check(program.parent.parents[5]==rt and sha(program)==src['sha256'],'unchanged relative source path gives true mirrored ROOT')
for r in deps:check(sha(rt/r['path'])==r['sha256'],'actual replay dependency '+r['id'])
check(state['local_imports']==[] and len(state['dependencies'])==4,'no extra local code or marker dependency')
new=program.with_name('incoming_slack_exact_v2.json');old2=E/'original'/byn['incoming_slack_exact_v2.json']['path'];old1=E/'original'/byn['incoming_slack_exact.json']['path']
check(new.read_bytes()==old2.read_bytes() and new.stat().st_size==1147,'new v2 equals frozen bytes')
check((E/'replay/original.stdout.txt').read_bytes()==new.read_bytes() and (E/'replay/original.stderr.txt').stat().st_size==0,'stdout equals report and empty stderr')
for tag in ['stdout','stderr']:
 p=E/'replay'/('original.'+tag+'.txt');check(sha(p)==state[tag+'_sha256'] and p.stat().st_size==state[tag+'_bytes'],'captured '+tag+' hashes')
a,b=json.loads(old1.read_text()),json.loads(old2.read_text())
check({k:v for k,v in b.items()if k!='nonzero_local_count_regression'}==a and set(b)-set(a)=={'nonzero_local_count_regression'},'v1 common core equals v2 only one new key')
check([r['source_full_history_IC_checks']for r in b['cases']]==[30,1554] and sum(r['source_full_history_IC_checks']for r in b['cases'])==1584,'1584 actual full history IC count fields')
check([r['parent_contexts']for r in b['cases']]==[5,36] and [r['fresh_signed_identity_checks']for r in b['cases']]==[62,9],'41 parent records and 71 fresh checks')
check(all(r[k] in [0,'0']for r in b['cases']for k in ['new_outside_terms_kept','tracked_positive_recipient_terms','whole_recipient_half_checks','max_tracked_whole_coefficient']),'actual positive recipient and outside loops zero')
local=b['nonzero_local_count_regression'];check([F(x)for x in local['new_recipient_charges']]==[F(1,6)]*2 and F(local['old_prefix_credit'])==-F(1,6) and F(local['net_fresh_reset'])==F(1,6),'local non-game count exact values')
check(2*F(1,6)-F(1,6)==F(1,2)-F(1,3) and F(1,6)/F(1,3)==F(1,2),'local algebra only signed reset and half ratio')
observed=json.loads((E/'replay/runtime-case-state.json').read_text())
check(len(observed)==2 and [r['original_return']for r in observed]==b['cases'],'passive observations correspond to original case returns')
check([(r['actual'],r['optimum'],r['loaded_policy_keys'])for r in observed]==[([4,0],[1,3],6),([0,0,0,5],[0,1,2,3],259)],'actual and optimal tuples from original return locals')
idx=json.loads((E/'fixture-input-index.json').read_text());di={r['path']:r for r in deps}
for r in idx:
 name=r['case'];inst=json.loads((E/'dependencies/examples/customer_attraction'/(name+'.json')).read_text());cert=json.loads((E/'dependencies/evidence/certificates/customer_attraction'/(name+'.json')).read_text());actions=cert.get('strategy',cert)['actions']
 check(r['complete_original_actions']==actions and r['customer_types']==inst['customers'] and r['topics']==inst['topics'],'complete input index not summary '+name)
 check(len(actions)==len({tuple(x['history'])for x in actions})==sum(len(inst['topics'])**i for i in range(inst['players'])) and all(len(x['history'])<inst['players'] and 0<=x['action']<len(inst['topics'])for x in actions),'actual policy structural keys '+name)
 check(sum(t['multiplicity']for t in inst['customers'])==r['unit_customers'],'unit customer multiplicities '+name)
port,root=idx
check([a['action']for a in port['complete_original_actions']]==[4,1,2,1,2,0],'complete six-node portfolio policy')
def last_rule(h):
 nonzero=[a for a in h if a!=0]
 return 5 if len(nonzero)==0 or len(nonzero)==1 and nonzero[0]!=5 else 4 if len(nonzero)==1 and nonzero[0]==5 else 0
check(all(a['action']==(0 if len(a['history'])<3 else last_rule(a['history']))for a in root['complete_original_actions']),'root certificate equals complete compressed policy, data only')
fresh=lambda types,a,actual:sum(t['multiplicity']for t in types if a in t['topics'] and not set(t['topics'])&set(actual))
check([fresh(port['customer_types'],a,[4,0])for a in [1,2,1,2,0]]==[20,11,20,11,0],'portfolio terminal fresh count read-off')
check(fresh(root['customer_types'],4,[0,0,0,5])==3 and fresh(root['customer_types'],0,[0,0,0,5])==fresh(root['customer_types'],5,[0,0,0,5])==0,'root only E has three terminal fresh customers')
check(all(set(t['topics'])&{0,4,1,3}for t in port['customer_types']) and all(set(t['topics'])&{0,1,2,3}for t in root['customer_types']),'outside structurally absent in both input pairs')
check(json.loads((E/'finite-scope-derived.json').read_text())['all_71_fresh_checks_occur_at_terminal_role'],'terminal-only scope recorded as input reading, not original report')
receipts=json.loads((HERE/'semantic-receipts.json').read_text())
check(len(receipts)==5 and {r['id']for r in receipts}=={r['id']for r in primary},'five exact primary receipt ids')
for r in receipts:
 check(all(r[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and all(len(r[k])>80 for k in ['read_note','comparison_note','decision_note']) and r['disposition']=='integrated' and all((STAGE/t).is_file()for t in r['targets']),'complete semantic receipt '+r['id'])
objects=list((STAGE/'archives/customer-attraction/state').rglob('*.md'));check(len(objects)==2,'two self-contained formal objects')
ids=[];links=0;pending=[]
for p in objects:
 text=p.read_text();check(not any(ord(c)<32 and c!='\n'for c in text),'no broken math escapes '+p.name)
 for field in ['id','kind','type_tag','title','status','summary','source_refs']:assert re.search('^'+field+':',text,re.M),(p,field)
 ids.append(re.search(r'^id: (.+)$',text,re.M).group(1))
 refs=re.findall(r'source:([^:]+):([^\n]+)',text);check(bool(refs)and all(c in ['68fad804ec5946cb296f77dc5b336308a66abf12','aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c']and len(c)==40 for c,_ in refs),'valid frozen refs '+p.name)
 for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)',text):
  if '://'in link or link.startswith('#'):continue
  rel=posixpath.normpath(str(p.relative_to(STAGE).parent/link.split('#')[0])); candidates=[STAGE/rel,REPO/rel,CACHE/'r3-relay-priority-audit-contracts'/rel,CACHE/'r3-adaptive-relay-source-payment'/rel]
  check(any(x.exists()for x in candidates),'resolved existing local object '+link)
  if not candidates[0].exists() and not candidates[1].exists():pending.append(rel)
  links+=1
check(len(set(ids))==2,'distinct stable formal ids')
check(len(re.findall(r'^\d+\. ',(HERE/'MATHEMATICAL-SELF-CHECK.md').read_text(),re.M))==22,'22 analytic math self-check items')
result={'status':'PASS','scope':'source/input structure/original capture/report version arithmetic/receipts/links only; no new research-program/IC/strategy/activation/rank search calls','checks_passed':len(checks),'links_checked':links,'analytic_math_self_check_items':22,'original_program_calls':1,'current_version_replayed':'v2 only','prior_complete_stage_links':sorted(set(pending)),'checks':checks}
(HERE/'evidence-self-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items()if k!='checks'},ensure_ascii=False))
