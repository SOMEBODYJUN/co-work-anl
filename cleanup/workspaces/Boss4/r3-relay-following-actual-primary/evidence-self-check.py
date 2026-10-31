"""Artifact consistency and exact rational substitutions only. Never imports/runs original code."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import ast,hashlib,json,re
S=Path(__file__).resolve().parents[4];W=Path(__file__).resolve().parent;E=S/'archives/customer-attraction/tools/evidence/relay-following-actual-primary';R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');checks=[]
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ck(name,condition):
 if not condition:raise AssertionError(name)
 checks.append(name)
rows=read(E/'source-manifest.json');requested=read(W/'requested-sources.json');claim=read(W/'claim-evidence.json');expected={'c4229abca09f2ea9e6f2','b43495a5aa16087ddb2b','d1690270377419753ed0','4b5051f77ed2e0d0491b','4f27f196d80c7e752dd1'}
ck('actual pushed Boss4 claim exact IDs',claim['status']=='pushed'and claim['actor']=='Boss4'and set(claim['ids'])==expected)
ck('claim synced and remote tip',claim['local_sync_status']=='synced'and claim['remote_tip']=='a9dddd6b7061c24935a53c40aa3338cf68e5b551')
ck('five source manifests match requested IDs',len(rows)==5 and set(x['id']for x in rows)==expected and rows==requested)
ck('primary byte total 20616',sum(x['size']for x in rows)==20616)
for x in rows:
 p=E/'original'/x['path'];ck('raw source size '+x['id'],p.stat().st_size==x['size']);ck('raw source sha '+x['id'],sha(p)==x['sha256'])
comparisons=read(E/'comparison-manifest.json');ck('five current comparison snapshots',len(comparisons)==5)
for x in comparisons:
 p=S/x['copied_path'];ck('comparison size '+x['path'],p.stat().st_size==x['bytes']);ck('comparison sha '+x['path'],sha(p)==x['sha256'])
ck('empty external input/dependency manifest',read(E/'dependency-manifest.json')==[])
search=read(W/'pre-claim-program-search.json');ck('pre-run no same SHA successful record',not search['same_sha_execution_records']and not search['same_named_program_files'])
program=next(x for x in rows if x['path'].endswith('.py'));report=next(x for x in rows if x['path'].endswith('.json'));src=E/'original'/program['path'];tree=ast.parse(src.read_text());imports={n.module for n in ast.walk(tree)if isinstance(n,ast.ImportFrom)}|{a.name for n in ast.walk(tree)if isinstance(n,ast.Import)for a in n.names}
ck('AST only four stdlib imports',imports=={'fractions','itertools','pathlib','json'})
ck('AST original main guard',any(isinstance(n,ast.If)and ast.unparse(n.test)=="__name__ == '__main__'"for n in tree.body))
ck('original write_text output side effect retained',any(isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and n.func.attr=='write_text'for n in ast.walk(tree)))
run=read(E/'replay/execution-state.json');obs=read(E/'replay/program-built-input-and-runtime.json');new=E/'replay/source-root'/report['path'];old=E/'original'/report['path'];out=E/'replay/original.stdout.txt'
ck('one original entry exactly, exit0 assertions enabled',run['original_program_calls']==run['execution_count']==1 and run['exit_code']==0 and run['optimize']==0)
ck('zero source local imports/external dependencies',run['local_program_imports']==run['external_dependencies']==[])
ck('original program mirror exact bytes',sha(E/'replay/source-root'/program['path'])==program['sha256'])
ck('new report frozen report stdout byte exact',new.read_bytes()==old.read_bytes()==out.read_bytes())
ck('three reports exactly 626B',new.stat().st_size==old.stat().st_size==out.stat().st_size==626)
ck('reports exact SHA',sha(new)==sha(old)==sha(out)==report['sha256'])
ck('empty stderr',not(E/'replay/original.stderr.txt').read_bytes()and run['stderr_bytes']==0)
ck('passive observation no extra calls description',obs['scope']=='passive original return locals, no extra action/terminal/pay/IC invocation')
likes=obs['unit_customer_likes'];expectedlikes=[list((i,3+j))for i in range(3)for j in range(3)for _ in range(2)]+[[0,1,2],[3,4,5]]
ck('all 20 built-in unit client likes preserved',likes==expectedlikes)
ck('uniform six prices and exact ell',obs['p']==['1/6']*6 and obs['all_conditional_tail_loads']==['0']*18+['2','2'])
policy=obs['observed_original_action_returns'];keys={tuple(x['history'])for x in policy};expectedkeys={h for d in range(3)for h in product(range(6),repeat=d)}
ck('all 43 ordered history keys observed',len(policy)==43 and keys==expectedkeys)
ck('all observed actions legal',all(x['action']in range(6)for x in policy))
ck('all 258 original comparisons nonnegative with ties',len(obs['original_gap_values_in_original_order'])==258 and min(map(F,obs['original_gap_values_in_original_order']))==0)
ck('original actual path and returns preserved',obs['actual_path']==[0,1,2]and obs['original_return']==read(old))
ck('root19/3 and report diagnosis',read(old)['root_payoff']=='19/3'and read(old)['toll']=='4'and read(old)['r_max_topic_y']=='3')
ck('historical OPEN report untouched',read(old)['scope']=='Only diagnoses an all-y transport strengthening. EXTRA-ONE-LEADER and HALF remain open. No claim about an endogenous optimal dual pair.')
d=read(E/'derived-static-and-bank-correction.json');b=d['bank_m4'];t=d['twenty_customer'];
ck('20client static Jensen totals',18*F(1,3)/(1+F(1))==3 and 2*F(1,2)/(1+F(3,2))==F(2,5))
ck('20client uniform query upper and lower B',F(6,2)+F(1,1+F(3,2))==F(t['B3'])==F(17,5))
ck('20client true root bound holds',F(t['root_payoff'])>F(t['B3']))
ck('20client decorative price nonoptimal',F(t['decorative_only_L_squared'])/(F(t['decorative_only_Q'])+3*F(t['decorative_only_M']))==F(2,5)<F(t['B3']))
Q=4*F(1,16)+6*F(3,49);M=F(1,16)+2*F(3,49);L=4*F(1,8)+6*F(1,7);T=4*F(1,16)*2+6*F(3,49);D=F(4,3);den=Q+4*M;Rc=D*(Q+T)-L*L
for k,v in [('Q',Q),('M',M),('L',L),('T',T),('D',D),('Q_plus_rM',den),('R_c',Rc)]:ck('bank exact '+k,F(b[k])==v)
ck('bank static optimal ratio',L*L/den==F(b['B4'])==F(19,14))
ck('bank primal y derives from rho/z',F(1,4)/(1+F(1))**2==F(1,16)and F(1,3)/(1+F(4,3))**2==F(3,49))
ck('bank negative BAL equality',D*den-L*L==D*(4*M-T)+Rc==F(-19,588))
ck('bank strict missing dynamic payment',D*(T-4*M)==F(25,147)>Rc==F(27,196))
ck('bank root shortfall yet half',F(b['B4'])-D==F(1,42)and 2*F(b['W'])-F(b['OPT'])==6)
ck('HallB algebraic cut example identity universal coefficients',all(F(1+c-a,1+c)-F(1,1+a)==F(a*(c-a),(1+c)*(1+a))for c in range(9)for a in range(c+1)))
ck('missingowner conversion rational identity',all(F(1,c*(c+1))+F(1,c+1)==F(1,c)for c in range(1,10)))
objects=read(W/'objects.json');ck('four formal objects',len(objects)==4)
links=[]
for rel in objects.values():
 p=S/rel;txt=p.read_text();front=txt.split('---',2)[1];ck('flat metadata complete '+rel,all(re.search('^'+f+':',front,re.M)for f in ['id','kind','type_tag','title','status','summary','source_refs']))
 for target in re.findall(r'\]\(([^)]+)\)',txt):
  if target.startswith(('http:','https:','#')):continue
  target=target.split('#')[0];loc=(p.parent/target).resolve();rr=loc.relative_to(S.resolve());ck('local formal link '+str(rr),(S/rr).exists()or(R/rr).exists());links.append({'from':rel,'target':str(rr)})
receipts=read(W/'semantic-receipts.json');ck('five exact receipt IDs',len(receipts)==5 and {x['id']for x in receipts}==expected)
for x in receipts:
 ck('full substantive receipt '+x['id'],all(x[k]for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])and x['disposition']=='integrated'and all(len(x[k])>60 for k in ['read_note','comparison_note','decision_note'])and all(t in objects.values()for t in x['targets']))
math=(W/'MATHEMATICAL-SELF-CHECK.md').read_text();ck('26 mathematical review items',len(re.findall(r'^\d+\. ',math,re.M))==26)
ck('current bridge refutation explicit','universal-optimal-price-root-bridge-refuted'in (S/list(objects.values())[0]).read_text())
ck('next candidates five actual unowned at captured check',len(read(W/'next-candidates.json')['candidates'])==5 and all(x['progress_at_candidate_check']is None for x in read(W/'next-candidates.json')['candidates']))
ck('worker stage only no push/done assertion',read(W/'STATUS.json')['body_save_status']=='external-staging-only; parent copy/push/done not asserted')
result={'status':'PASS','scope':'artifact hashes/record consistency/exact rational substitutions only; zero source code imports or original source calls','checks_passed':len(checks),'formal_local_links_checked':len(links),'mathematical_review_items':26,'checks':checks,'links':links}
(W/'evidence-self-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k not in ['checks','links']},ensure_ascii=False))
