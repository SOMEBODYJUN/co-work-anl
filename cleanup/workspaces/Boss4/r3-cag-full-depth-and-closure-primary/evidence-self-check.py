"""Artifact and analytic-data consistency only; no source research program execution."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,re
S=Path(__file__).resolve().parents[4];W=Path(__file__).resolve().parent;E=S/'archives/customer-attraction/tools/evidence/cag-full-depth-and-closure-primary';R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');checks=[]
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ck(name,c):
 if not c:raise AssertionError(name)
 checks.append(name)
expected={'ec4ec12df4dbddac21ca','9b35f62cef8a57e76955','309cae54953ec625ee7f','0c36b5acbbe295107178','d86dbd9fcaa174674ce1'};rows=read(E/'source-manifest.json');claim=read(W/'claim-evidence.json')
ck('actual BT pushed Boss4 exact ids',claim['status']=='pushed'and claim['actor']=='Boss4'and set(claim['ids'])==expected)
ck('actual BT synced tipa301d8',claim['local_sync_status']=='synced'and claim['remote_tip']=='a301d8254fb5127522dfbef4bf5447bfbab7c8bd')
ck('actual each progress owner read',claim['source_owners_verified']=='each actual progress entry owner Boss4')
ck('five primary source/requested manifest match',len(rows)==5 and rows==read(W/'requested-sources.json')and {x['id']for x in rows}==expected)
ck('source total19178B',sum(x['size']for x in rows)==19178)
for x in rows:
 p=E/'original'/x['path'];ck('raw size '+x['id'],p.stat().st_size==x['size']);ck('raw SHA '+x['id'],sha(p)==x['sha256'])
ck('all source Markdown/no executable',all(x['path'].endswith('.md')for x in rows))
cm=read(E/'comparison-manifest.json');ck('seven related full-read snapshots',len(cm)==7)
for x in cm:
 p=S/x['copied_path'];ck('comparison size '+x['path'],p.stat().st_size==x['bytes']);ck('comparison SHA '+x['path'],sha(p)==x['sha256'])
ck('BG result has accurate prior-stage provenance','preceding mature BG result'in cm[-1]['role']and 'read_from'in cm[-1])
rm=read(E/'related-result-manifest.json');ck('one prior analytic result input',len(rm)==1)
for x in rm:
 p=S/x['copied_path'];ck('prior analytic bank byte count',p.stat().st_size==x['bytes']);ck('prior analytic bank SHA',sha(p)==x['sha256'])
ck('zero external executable dependencies',read(E/'dependency-manifest.json')==[])
execution=read(E/'execution-status.json');ck('zero original program/SPE/new scan calls',execution['original_program_calls']==execution['SPE_solver_calls']==execution['new_scans']==0 and execution['executable_primary_sources']==0)
ck('no fake replay files',not(E/'replay').exists())
der=read(E/'derived-closure-and-full-depth-debt.json');bank=read(E/'related-analytic-bank-menu.json');cyc=der['singleton_cycle'];cl=der['bank_query_seed_closure'];wp=der['full_depth_WP'];floor=der['shared_direct_floor']
ck('cycle fixedm2 seedone generalp construction',cyc['m']==2 and cyc['source_seed']==['A0']and cyc['parameter']=='every integer p>=2')
ck('cycle size/p-minusone rounds parameteric not finite samples',cyc['closure_size']=='p'and cyc['strict_growth_rounds']=='p-1')
ck('cycle pureSPE given exact root/last1',cyc['root_payoff']==cyc['last_payoff']=='1'and cyc['W']==cyc['OPT2']=='2')
ck('bank closure three added econ0 topics',cl['first_round_additions']==[{'history':[],'action':[0,0]},{'history':[[1,1],[1,0],[1,2]],'action':[0,1]},{'history':[[1,2],[1,0],[1,1]],'action':[0,2]}])
seed={(a,b)for a in [1,2,3]for b in range(3)};additions={tuple(x['action'])for x in cl['first_round_additions']};ck('bank seed9 plus additions exactly full12',len(seed)==9 and seed|additions=={(a,b)for a in range(4)for b in range(3)})
for x in cl['first_round_additions'][1:]:
 h=[tuple(z)for z in x['history']];a,b=h[0];used={b};valid=True
 for action in h[1:]:
  expectedaction=(a,min(set(range(3))-used));valid=valid and action==expectedaction;used.add(action[1])
 ck('BASE witness genuine prescribed suffix '+str(x['action']),valid and len(used)==3 and a==1 and tuple(x['action'])==(0,b))
ck('WP bank root/full menu values reused',bank['root_u']=='4/3'and bank['pTKp']=='59/36'and wp['r']==4)
ck('WP known sum difference4/9',wp['E_sum_D_minus_sum_s']==bank['unpaid_suffix_regret_mean']=='4/9')
ck('WP exact tax5/36 and e0',wp['E_insertion_tax']==bank['insertion_tax_mean']=='5/36'and wp['root_slack_e']=='0')
ck('PAY-WP positive excess11/36',F(wp['E_sum_D_minus_sum_s'])-F(wp['E_insertion_tax'])-F(wp['root_slack_e'])==F(wp['PAY_WP_excess'])==F(11,36))
ck('same excess equals exact fullK gap',F(bank['pTKp'])-F(bank['root_u'])==F(wp['PAY_WP_excess']))
ck('separate sums not falsely computed','no claim to separately compute'in wp['meaning'])
ck('direct floor true m5 threshold gap1/20',floor['m']==5 and F(floor['OPT_over_2m'])-F(floor['bank_root_u'])==F(floor['threshold_minus_u'])==F(1,20))
ck('direct floor threshold13/10 really OPT/2m',F(floor['OPT5'])/(2*floor['m'])==F(floor['OPT_over_2m']))
pre=read(W/'pre-claim-bank-boundary.json');ck('preclaim note does not claim unread primary','no unclaimed BT primary read'in pre['scope'])
ck('preclaim Jensen decomposition exact',F(pre['exact_gaps']['economic_Jensen_gap'])+F(pre['exact_gaps']['bank_Jensen_gap'])==F(pre['exact_gaps']['fullmenu_minus_B4'])==F(71,252))
objects=read(W/'objects.json');ck('three new formal objects',len(objects)==3);links=[]
for rel in objects.values():
 p=S/rel;t=p.read_text();front=t.split('---',2)[1];ck('flat metadata complete '+rel,all(re.search('^'+key+':',front,re.M)for key in ['id','kind','type_tag','title','status','summary','source_refs']))
 for target in re.findall(r'\]\(([^)]+)\)',t):
  if target.startswith(('https:','http:','#')):continue
  rr=(p.parent/target.split('#')[0]).resolve().relative_to(S.resolve());ck('formal local link '+str(rr),(S/rr).exists()or(R/rr).exists());links.append({'from':rel,'target':str(rr)})
receipts=read(W/'semantic-receipts.json');ck('five exact receipts',len(receipts)==5 and {x['id']for x in receipts}==expected)
for x in receipts:ck('substantive completed receipt '+x['id'],all(x[k]for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])and x['disposition']=='integrated'and all(len(x[k])>60 for k in ['read_note','comparison_note','decision_note'])and all(y in objects.values()for y in x['targets']))
ck('33 mathematical check items',len(re.findall(r'^\d+\. ',(W/'MATHEMATICAL-SELF-CHECK.md').read_text(),re.M))==33)
ck('PAY-WP status current refuted explicit','universal-PAY-WP-refuted'in(S/list(objects.values())[1]).read_text())
ck('closure uniform size limitation explicit','size-unbounded-at-fixed-m-seed'in(S/list(objects.values())[0]).read_text())
ck('main formal objects do not overwrite comparison objects',set(objects.values()).isdisjoint({x['path']for x in cm}))
ck('worker body not falsely pushed/done',read(W/'STATUS.json')['body_save_status']=='external-staging-only; parent copy/push/done not asserted')
cs=read(W/'next-candidates.json')['candidates'];ck('next five truly captured available',len(cs)==5 and all(x['progress_at_candidate_check']is None for x in cs))
result={'status':'PASS','scope':'artifact hashes/metadata/links/closed analytic certificate consistency only; no source program call or SPE/Nash scan; general proofs reviewed separately','checks_passed':len(checks),'formal_local_links_checked':len(links),'mathematical_review_items':33,'checks':checks,'links':links};(W/'evidence-self-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k not in ['checks','links']},ensure_ascii=False))
