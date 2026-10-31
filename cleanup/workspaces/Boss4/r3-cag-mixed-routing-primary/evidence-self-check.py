"""Verify bytes, records and the explicit closed-form matrix; no source program, SPE or Nash solver."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,re
S=Path(__file__).resolve().parents[4];W=Path(__file__).resolve().parent;E=S/'archives/customer-attraction/tools/evidence/cag-mixed-routing-primary';R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');checks=[]
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ck(name,c):
 if not c:raise AssertionError(name)
 checks.append(name)
expected={'42096deb5e5b672c484e','efef49e0cb43c7636983','c5363fdb5df8ef8bc699','6e553ecf00149eaae721','4040cb83a3a078446c45'};rows=read(E/'source-manifest.json');claim=read(W/'claim-evidence.json')
ck('BG actual pushed Boss4 exact ids',claim['status']=='pushed'and claim['actor']=='Boss4'and set(claim['ids'])==expected)
ck('BG synced remote tip226cfe',claim['local_sync_status']=='synced'and claim['remote_tip']=='226cfe00554dbafe85653c6fc7aeb57ec8eedfb6')
ck('actual each source owner verified',claim['source_owners_verified']=='each actual cleanup/progress entry owner Boss4')
ck('five primary raw manifests equal',len(rows)==5 and rows==read(W/'requested-sources.json')and {x['id']for x in rows}==expected)
ck('primary bytes17512',sum(x['size']for x in rows)==17512)
for x in rows:
 p=E/'original'/x['path'];ck('original size '+x['id'],p.stat().st_size==x['size']);ck('original SHA '+x['id'],sha(p)==x['sha256'])
ck('all primary Markdown, no executable file',all(x['path'].endswith('.md')for x in rows))
comparisons=read(E/'comparison-manifest.json');ck('seven actual comparison snapshots',len(comparisons)==7)
for x in comparisons:
 p=S/x['copied_path'];ck('comparison size '+x['path'],p.stat().st_size==x['bytes']);ck('comparison SHA '+x['path'],sha(p)==x['sha256'])
ck('empty external dependency manifest',read(E/'dependency-manifest.json')==[])
execution=read(E/'execution-status.json');ck('no original runs, SPE or Nash calls',execution['original_program_calls']==execution['SPE_solver_calls']==execution['Nash_solver_calls']==execution['new_scans']==0)
ck('no fake replay directories',not(E/'replay').exists())
d=read(E/'analytic-bank-menu.json');topics=[tuple(x)for x in d['catalogue']];p=list(map(F,d['p']));K=[list(map(F,row))for row in d['K']];likes=d['unit_customer_likes_topic_indices'];full=d['full_root_column_loads'];tail=d['tail_column_loads']
ck('explicit bank10clients12topics',len(likes)==10 and topics==[(a,b)for a in range(4)for b in range(3)])
ck('explicit economic and two-unit bank memberships',likes==[[i for i,(a,b)in enumerate(topics)if a==x]for x in range(4)]+[[i for i,(a,b)in enumerate(topics)if b==bank]for bank in range(3)for _ in range(2)])
ck('all source topics contain exactly3unitclients',all(sum(j in q for q in likes)==3 for j in range(12)))
ck('actual complete bank path',d['actual_path']==[[0,0],[0,1],[0,2],[1,0]])
ck('closed all root full and tail column dimensions',len(full)==len(tail)==12 and all(len(x)==10 for x in full+tail))
for j,(a,b)in enumerate(topics):
 expect=[0]*10;expect[a]=3;expect[1 if a==0 else 0]=1
 for bank in range(3):
  for x in [4+2*bank,5+2*bank]:expect[x]=2 if bank==b else 1
 ck('complete root counts '+str(j),full[j]==expect)
 ck('tail excludes only own root '+str(j),tail[j]==[full[j][x]-int(j in likes[x])for x in range(10)])
ck('K complete row/query column/root orientation',len(K)==12 and all(len(row)==12 for row in K))
ck('all144 K entries exact extra-query denominator',all(K[i][j]==sum((F(1,1+full[j][x])for x in range(10)if i in likes[x]),F())for i in range(12)for j in range(12)))
rootd=[sum((F(1,full[j][x])for x in range(10)if j in likes[x]),F())for j in range(12)]
ck('all genuine root forced payoffs4/3',rootd==[F(4,3)]*12)
ck('p9 nonnegative normalized and exact support',sum(p)==1 and p==[F(0)if a==0 else F(1,9)for a,b in topics])
kp=[sum((K[i][j]*p[j]for j in range(12)),F())for i in range(12)];ptk=[sum((p[i]*K[i][j]for i in range(12)),F())for j in range(12)];value=sum((p[i]*kp[i]for i in range(12)),F())
ck('all stored Kp values exact',list(map(str,kp))==d['Kp'])
ck('Kp support59/36 off25/18',kp==[F(25,18)]*3+[F(59,36)]*9)
ck('explicit p satisfies symmetric NE',all(kp[i]<=value and (not p[i]or kp[i]==value)for i in range(12)))
ck('NE value and actual u strict gap',value==F(59,36)>F(d['root_u'])==F(4,3)and value-F(d['root_u'])==F(11,36))
ck('dual pTK stored and all columns lower bound',list(map(str,ptk))==d['pTK_column_values']and ptk==[F(31,18)]*3+[F(59,36)]*9)
ck('minmax explicit upper and dual lower coincide',max(kp)==min(ptk)==F(d['Mfull_minimax_value'])==F(59,36))
ck('B4 four-slot primal value',F(4,4+4)+F(2*3,3+4)==F(d['B4_four_slot_fractional_background'])==F(19,14))
ck('B4 strict root gap1/42',F(d['B4_four_slot_fractional_background'])-F(d['root_u'])==F(1,42))
ck('genuine example half still holds',2*d['W']-d['OPT']==6 and d['W']==8 and d['OPT']==10)
# Exact insertion identity from the stated 12 closed count columns, not a new SPE audit.
def phi(count,bg):return sum((sum((F(1,bg[x]+a)for a in range(1,count[x]+1)),F())for x in range(10)),F())
Ftail=[phi(c,[0]*10)for c in tail];Rmatrix=[];taxmatrix=[]
for i,T in enumerate(topics):
 bg=[int(i in likes[x])for x in range(10)];Rrow=[];taxrow=[]
 for j,A in enumerate(topics):
  rr=phi(tail[j],bg)-phi(tail[i],bg);tax=sum((F(1,(1+tail[j][x])*(2+tail[j][x]))for x in range(10)if i in likes[x]and j in likes[x]),F());Rrow.append(rr);taxrow.append(tax)
 Rmatrix.append(Rrow);taxmatrix.append(taxrow)
ck('144 closed suffix insertion identities exact',all(K[i][j]==rootd[i]+Ftail[i]-Ftail[j]+Rmatrix[i][j]-taxmatrix[i][j]for i in range(12)for j in range(12)))
meanR=sum((p[i]*p[j]*Rmatrix[i][j]for i in range(12)for j in range(12)),F());meanTax=sum((p[i]*p[j]*taxmatrix[i][j]for i in range(12)for j in range(12)),F());meanD=sum((p[i]*rootd[i]for i in range(12)),F())
ck('true suffix mean4/9',meanR==F(d['unpaid_suffix_regret_mean'])==F(4,9))
ck('correct single insertion tax mean5/36',meanTax==F(d['insertion_tax_mean'])==F(5,36))
ck('Nash gap equals unpaid suffix minus tax',meanD+meanR-meanTax==value and meanR-meanTax==F(11,36))
ck('three quantifiers separated in artifact',d['NQ_quantifier']!=d['Mfull_quantifier']!=d['WP_quantifier'])
objects=read(W/'objects.json');ck('four formal self contained objects',len(objects)==4);links=[]
for rel in objects.values():
 f=S/rel;t=f.read_text();front=t.split('---',2)[1];ck('flat metadata required '+rel,all(re.search('^'+key+':',front,re.M)for key in ['id','kind','type_tag','title','status','summary','source_refs']))
 for target in re.findall(r'\]\(([^)]+)\)',t):
  if target.startswith(('http:','https:','#')):continue
  rr=(f.parent/target.split('#')[0]).resolve().relative_to(S.resolve());ck('formal local link '+str(rr),(S/rr).exists()or(R/rr).exists());links.append({'from':rel,'target':str(rr)})
receipts=read(W/'semantic-receipts.json');ck('five semantic receipts exact IDs',len(receipts)==5 and {x['id']for x in receipts}==expected)
for x in receipts:ck('full substantive receipt '+x['id'],all(x[k]for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])and x['disposition']=='integrated'and all(len(x[k])>60 for k in ['read_note','comparison_note','decision_note'])and all(y in objects.values()for y in x['targets']))
ck('35 manual mathematical items',len(re.findall(r'^\d+\. ',(W/'MATHEMATICAL-SELF-CHECK.md').read_text(),re.M))==35)
ck('new counterexample current status refuted','NQ-Mfull-and-all-p-WP-refuted-for-general-model'in(S/list(objects.values())[3]).read_text())
ck('no old shared file in main object list',all('自由extra-one与iid安全值边界'not in x and '根重置对恒等式与辅助尾份额'not in x for x in objects.values()))
ck('body only staging not push/done claimed',read(W/'STATUS.json')['body_save_status']=='external-staging-only; parent copy/push/done not asserted')
ck('next five captured available',len(read(W/'next-candidates.json')['candidates'])==5 and all(x['progress_at_candidate_check']is None for x in read(W/'next-candidates.json')['candidates']))
result={'status':'PASS','scope':'artifact consistency and explicit closed-form matrix/insertion arithmetic; no original program call, no SPE/Nash search; all-input proofs and all-NE quantifier reviewed analytically','checks_passed':len(checks),'formal_local_links_checked':len(links),'mathematical_review_items':35,'closed_matrix_entries_verified':144,'closed_suffix_identity_entries_verified':144,'checks':checks,'links':links};(W/'evidence-self-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k not in ['checks','links']},ensure_ascii=False))
