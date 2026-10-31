"""Artifact/hash/rational checks only; does not execute research programs or enumerate worlds."""
from pathlib import Path
from fractions import Fraction as F
import ast, hashlib, json, posixpath, re
HERE=Path(__file__).resolve().parent
STAGE=HERE.parents[3]
REPO=STAGE.parent.parent/'boss4-research'
PREVIOUS=STAGE.parent/'r3-adaptive-relay-source-payment'
E=STAGE/'archives/customer-attraction/tools/evidence/relay-priority-audit-contracts-primary'
checks=[]
def check(value,label):
    assert value,label
    checks.append(label)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
primary=json.loads((E/'source-manifest.json').read_text())
related=json.loads((E/'related-source-manifest.json').read_text())
check(len(primary)==5 and sum(x['size']for x in primary)==15992,'five primary sources 15992B')
check(len(related)==2 and sum(x['size']for x in related)==8798,'two related originals 8798B')
for label,items in [('original',primary),('related-original',related)]:
 for row in items:
    p=E/label/row['path'];check(len(p.read_bytes())==row['size'] and sha(p)==row['sha256'],'source bytes '+row['id'])
byn={Path(x['path']).name:x for x in primary}
programs={}
for name in ['audit_predictable_activation.py','audit_priority_coupling.py']:
    p=E/'original'/byn[name]['path']; tree=ast.parse(p.read_text());programs[name]=tree
    imports=[n.module for n in ast.walk(tree)if isinstance(n,ast.ImportFrom)]+[a.name for n in ast.walk(tree)if isinstance(n,ast.Import)for a in n.names]
    check(all(n in ['collections','fractions','itertools','pathlib','json','math']for n in imports),'stdlib-only import AST '+name)
    check(not any(isinstance(n,ast.If)and '__name__'in ast.unparse(n.test)for n in tree.body),'top-level original entry '+name)
def dag(tree):
    return next(ast.literal_eval(n.value)for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='DAG'for t in n.targets))
d=dag(programs['audit_predictable_activation.py'])
check(d==dag(programs['audit_priority_coupling.py']) and len(d)==9 and sum(map(len,d.values()))==13,'two exact 9-state 13-edge DAG inputs')
check(all(j[0]>s[0]for s,js in d.items()for j in js) and all(tuple(sorted(js))==js and len({j[0]for j in js})==len(js) for js in d.values()),'strict future ordered distinct successor roles')
summary=json.loads((E/'replay/execution-summary.json').read_text())
check(summary['original_program_execution_count']==2 and len(summary['runs'])==2,'two actual original program calls')
for r in summary['runs']:
    root=E/'replay'/r['case'];check(r['execution_count']==1 and r['exit_code']==0 and r['stderr_bytes']==0,'one successful call '+r['case'])
    check(sha(root/r['program'])==byn[r['program']]['sha256'] and not r['local_program_imports'],'unchanged source and no local program imports '+r['case'])
    output='predictable_activation_audit.json'if r['case']=='predictable'else'priority_coupling_audit.json'
    check((root/output).read_bytes()==(E/'original'/byn[output]['path']).read_bytes(),'new output exact frozen bytes '+r['case'])
    for out in ['stdout.txt','stderr.txt']:
        key=out.split('.')[0];check(sha(root/out)==r[key+'_sha256'] and (root/out).stat().st_size==r[key+'_bytes'],'captured '+r['case']+' '+out)
check((E/'replay/priority/predictable_activation_audit.json').read_bytes()==(E/'original'/byn['predictable_activation_audit.json']['path']).read_bytes(),'priority true frozen report input')
p=json.loads((E/'replay/predictable/predictable_activation_audit.json').read_text())
q=json.loads((E/'replay/priority/priority_coupling_audit.json').read_text())
check([p[k]for k in ['activation_vectors_per_source','sources','state_polynomial_checks','role_entry_checks']]==[64,9,81,18],'actual activation report count fields')
check([q[k]for k in ['priority_worlds','sources','unit_routes','exact_marginal_comparisons']]==[720,9,6480,81] and q['each_source_unit_in_every_world'] and not q['proves_general_budget'],'actual priority report count and budget fields')
rows=[(tuple(r['source']),c)for r in p['reports']for c in r['states']]
check(len(rows)==33 and sum(tuple(c['state'])!=source for source,c in rows)==24 and 81-len(rows)==48,'33 positive cells with 24 nonowner and 48 zero cells')
check(all(sum((F(c['absorb'])for c in r['states']),F(0))==1 for r in p['reports']),'nine source absorption totals one')
role_sums=[sum((F(c['entry'])for c in r['states']if c['state'][0]==i),F(0))for r in p['reports']for i in range(r['source'][0]+1,6)]
check(len(role_sums)==18 and sum(x>0 for x in role_sums)==17 and sum(x==0 for x in role_sums)==1 and max(role_sums)==F(1,2),'18 role sums include one zero and cap one half')
cells={tuple(c['state']):c for c in p['reports'][0]['states']}
check(F(cells[(3,'a')]['entry'])+F(cells[(3,'b')]['entry'])==F(1,2) and F(cells[(3,'a')]['absorb'])+F(cells[(3,'b')]['absorb'])==F(1,12),'old branch-merge role3 rational sums')
check(F(cells[(1,'b')]['absorb'])==F(1,20)==F(1,4*5),'old c4 nonowner Beta2 equality')
receipts=json.loads((HERE/'semantic-receipts.json').read_text())
check({r['id']for r in receipts}=={r['id']for r in primary} and len(receipts)==5,'five exact primary receipt IDs')
for row in receipts:
 check(all(row[k]is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and row['disposition']=='integrated' and all(len(row[k])>60 for k in ['read_note','comparison_note','decision_note']) and all((STAGE/t).is_file()for t in row['targets']),'full semantic receipt '+row['id'])
objects=list((STAGE/'archives/customer-attraction/state').rglob('*.md'))
check(len(objects)==3,'three new self-contained formal objects')
ids=[]
for path in objects:
 text=path.read_text();check(not any(ord(c)<32 and c!='\n' for c in text),'no broken math escapes '+path.name)
 for field in ['id','kind','type_tag','title','status','summary','source_refs']:
    assert re.search('^'+field+':',text,re.M),(path,field)
 ids.append(re.search(r'^id: (.+)$',text,re.M).group(1))
 refs=re.findall(r'source:([^:]+):([^\n]+)',text)
 check(bool(refs) and all(len(commit)==40 and commit in ['68fad804ec5946cb296f77dc5b336308a66abf12','aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c']for commit,_ in refs),'valid frozen source refs '+path.name)
check(len(ids)==len(set(ids)),'distinct stable object IDs')
link_count=0;prior_stage_links=[]
for path in objects:
 for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',path.read_text()):
    if '://' in target or target.startswith('#'):continue
    rel=posixpath.normpath(str(path.relative_to(STAGE).parent/target.split('#')[0]))
    candidates=[STAGE/rel,REPO/rel,PREVIOUS/rel]
    check(any(p.exists()for p in candidates),'resolved local link '+target)
    if not candidates[0].exists() and not candidates[1].exists():prior_stage_links.append(rel)
    link_count+=1
check(len(re.findall(r'^\d+\. ',(HERE/'MATHEMATICAL-SELF-CHECK.md').read_text(),re.M))==20,'20 analytic mathematical self-check items')
result={'status':'PASS','scope':'source bytes/import AST/real-run captures/frozen-report rational arithmetic/receipts/links; no original program re-execution or new activation/rank/game/SPE enumeration','checks_passed':len(checks),'links_checked':link_count,'analytic_math_self_check_items':20,'original_program_calls':2,'original_program_calls_per_entry':1,'prior_complete_stage_links':sorted(set(prior_stage_links)),'checks':checks}
(HERE/'evidence-self-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items()if k!='checks'},ensure_ascii=False))
