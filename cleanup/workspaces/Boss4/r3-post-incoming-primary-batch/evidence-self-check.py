"""Source/artifact/old-report arithmetic checks only. No research program is run."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,posixpath,re
HERE=Path(__file__).resolve().parent;STAGE=HERE.parents[3];CACHE=STAGE.parent;REPO=CACHE.parent/'boss4-research'
E=STAGE/'archives/customer-attraction/tools/evidence/post-incoming-primary-batch'
checks=[]
def check(ok,label):
 assert ok,label
 checks.append(label)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
primary=json.loads((E/'source-manifest.json').read_text());related=json.loads((E/'related-source-manifest.json').read_text())
check(len(primary)==5 and sum(r['size']for r in primary)==28604,'five primary sources 28604B')
check(all(r['path'].endswith('.md')for r in primary),'all five primary sources Markdown, no original program entry')
check(len(related)==10 and sum(r['size']for r in related)==54670,'ten comparison originals 54670B')
for group,items in [('original',primary),('related-original',related)]:
 for r in items:
  p=E/group/r['path'];check(p.stat().st_size==r['size'] and sha(p)==r['sha256'],'original bytes '+r['id'])
claim=json.loads((HERE/'claim-evidence.json').read_text())
check(claim['parent_confirmed_status']=='pushed' and claim['parent_confirmed_local_sync']=='synced' and set(claim['ids'])=={r['id']for r in primary},'actual parent claim receipt exact IDs and pushed/synced state')
status=json.loads((HERE/'STATUS.json').read_text());check(status['original_research_program_calls']==0 and not any(E.rglob('*.py')),'no original research program code or run materialized')
by={Path(r['path']).name:E/'related-original'/r['path'] for r in related}
c=json.loads(by['conditional_transport_audit.json'].read_text());k=json.loads(by['optimal_exchange_review_audit.json'].read_text());x=json.loads(by['exchange_potential_credit_audit.json'].read_text());i=json.loads(by['owner_insertion_identity_audit.json'].read_text())
check(all(a['status']=='PASS'for a in [c,k,x,i]),'four frozen report status fields read only')
check([c[z]for z in ['customers','players','topics','ordered_nodes','comparisons']]==[20,3,6,43,258] and c['actual_path']==[0,1,2] and F(c['root_payoff'])==F(19,3),'conditional old report input scope fields')
check([F(a)for a in c['decorative_conditional_tail_loads']]==[2,2] and F(c['toll'])==4>F(c['r_max_topic_y'])==3,'all-y old diagnostic toll only, not endogenous optimum')
check([k[z]for z in ['bernoulli_event_checks','random_position_matching_checks','positive_rational_alpha_checks']]==[5460,91,45],'old optimal-exchange event report counts')
check([x['pattern_checks'][z]for z in ['marginal_checks','same_leaf_checks','all_future_prefix_incidence_checks']]==[72818,21844,10795] and len(x['rollout_checks'])==6,'old credit pattern report and six rollout rows')
check(all(F(r['actual_leaf_credit'])<=r['actual_I']for r in x['rollout_checks']),'old same-leaf credit fields no cross-leaf budget inferred')
check([i[z]for z in ['profile_count_identity_checks','independent_query_count_checks']]==[18,144],'old insertion report count fields')
p,lam,n,cnt=F(1,2),F(1,2),1,1
b0=p;old=b0/(p+cnt);new=b0/(p+lam*cnt);coef=F(n)*(1-lam)/(1+n*lam)
check(old==F(1,3) and new-old==F(1,6)>coef*old==F(1,9),'primary nonunit p half OLD-REF scope arithmetic')
check(F(42)-41==F(45)-44==1 and 41<42 and 41>=1,'primary old matching 41 below omitted42 above net1')
check(F(1)*(1-F(1))/(1+1*F(1))==0,'lambda one refund endpoint zero')
receipts=json.loads((HERE/'semantic-receipts.json').read_text())
check(len(receipts)==5 and {r['id']for r in receipts}=={r['id']for r in primary},'five exact primary semantic receipt IDs')
for r in receipts:
 check(all(r[z]is True for z in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and r['disposition']=='integrated' and all(len(r[z])>80 for z in ['read_note','comparison_note','decision_note']) and all((STAGE/t).is_file()for t in r['targets']),'complete semantic receipt '+r['id'])
objects=list((STAGE/'archives/customer-attraction/state').rglob('*.md'));check(len(objects)==4,'four self-contained formal objects')
ids=[];links=0;prior=[]
for path in objects:
 t=path.read_text();check(not any(ord(c)<32 and c!='\n'for c in t),'no broken math escapes '+path.name)
 for key in ['id','kind','type_tag','title','status','summary','source_refs']:assert re.search('^'+key+':',t,re.M),(path,key)
 ids.append(re.search(r'^id: (.+)$',t,re.M).group(1))
 refs=re.findall(r'source:([^:]+):([^\n]+)',t);check(bool(refs)and all(len(commit)==40 and commit in ['68fad804ec5946cb296f77dc5b336308a66abf12','aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c']for commit,_ in refs),'valid frozen source refs '+path.name)
 for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
  if '://'in target or target.startswith('#'):continue
  rel=posixpath.normpath(str(path.relative_to(STAGE).parent/target.split('#')[0]));options=[STAGE/rel,REPO/rel]+[CACHE/b/rel for b in ['r3-relay-priority-audit-contracts','r3-adaptive-relay-source-payment','r3-incoming-balance-audit-history']]
  check(any(p.exists()for p in options),'resolved local link '+target)
  if not options[0].exists()and not options[1].exists():prior.append(rel)
  links+=1
check(len(set(ids))==4,'four distinct stable IDs')
check(len(re.findall(r'^\d+\. ',(HERE/'MATHEMATICAL-SELF-CHECK.md').read_text(),re.M))==24,'24 analytic mathematical self-check items')
result={'status':'PASS','scope':'bytes/claim/receipts/local links/frozen-report and primary-example Fraction arithmetic; no original-program/IC/game/strategy/activation/permutation calls','checks_passed':len(checks),'links_checked':links,'analytic_math_self_check_items':24,'original_research_program_calls':0,'prior_complete_stage_links':sorted(set(prior)),'checks':checks}
(HERE/'evidence-self-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items()if k!='checks'},ensure_ascii=False))
