"""Current rational check of one 516-row primal, reusing original row functions.

No original module import, LP, all-type maximization, old audit or SPE search.
The row formulas remain shared with original production code, not independent.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import ast,json,hashlib,time,datetime,sys
c=Path(__file__).resolve().parent;out=c/'recheck-output'
assert not out.exists(),'choose a fresh recheck-output directory'
out.mkdir();started=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
inv=json.loads((c/'source-records.json').read_text())
ids={'point':'2e7e484699da73a455ee','atoms':'daf43c377037eed6e5cc','base':'bea9206b2c5bb96bf322','closure':'2df2e83d19d9899feb44','envelope':'8d0d330332180d977d68'}
paths={role:c/'source-root'/inv[sid]['path']for role,sid in ids.items()}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
before=[]
for name,p in paths.items():
 x=inv[ids[name]];assert sha(p)==x['sha256']and p.stat().st_size==x['size'];before.append({'role':name,'id':ids[name],'path':str(p),'size':p.stat().st_size,'sha256':sha(p)})
ns={};prefix=paths['base'].read_text().split('\nfrom pathlib import Path\nfrom collections')[0]
assert len(prefix.encode())==6476;exec(compile(prefix,str(paths['base'])+'#6476B-prefix','exec'),ns)
def functions(p,names,glob):
 tree=ast.parse(p.read_text());nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name in names];assert {n.name for n in nodes}==set(names)
 exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p)+'#function-definitions-only','exec'),glob)
 return glob
cl=functions(paths['closure'],['rows'],{'F':F,'product':product})
en=functions(paths['envelope'],['target_counts','source_terms','rows'],{'F':F,'triples':list(product((0,1),repeat=3)),'quads':list(product((0,1),repeat=4))})
atoms=json.loads(paths['atoms'].read_text())['primal']['atoms'];point=json.loads(paths['point'].read_text());weights=list(map(F,point['exact_reweighting']));assert len(atoms)==len(weights)==64 and min(weights)>=0
columns=[];welfare=[];objective=[]
for a in atoms:
 bits=tuple(map(int,a['bits']));hist=[a[k]for k in ('AB_hist','AE_hist','second_hist')]
 assert len(bits)==10 and all(z in(0,1)for z in bits)
 assert [len(h)for h in hist]==[8,8,16]and all(all(type(z)is int and z>=0 for z in h)and sum(h)==5 for h in hist)
 d=sum(n*b[0]for n,b in zip(hist[0],ns['types']))
 for ell,h in a['menus_lh']:assert 0<=h<=d and 0<=ell-h<=5-d
 rows=ns['evaluate'](bits,hist,a['menus_lh'],include_second_correlations=True);assert len(rows)==437
 rows.update(cl['rows'](a));assert len(rows)==447
 rows.update({'cross_envelope:'+k:v for k,v in en['rows'](a).items()});assert len(rows)==493
 for g in ('AB','AE','second'):
  own,iv=en['source_terms'](a,g);total=sum(iv[0]+iv[1],F())
  for target,counts in en['target_counts'](a).items():
   if not target.startswith(g+'_'):rows['cross_full:'+g+':'+target]=5*own-sum(counts)*total
 assert len(rows)==516
 if columns:assert tuple(rows)==tuple(columns[0])
 columns.append(rows);welfare.append(int(any(bits[:5])));objective.append(int(d>0))
names=tuple(columns[0]);slacks={name:sum((mass*col[name]for mass,col in zip(weights,columns)),F())for name in names}
norm=sum((mass*v for mass,v in zip(weights,welfare)),F());value=sum((mass*v for mass,v in zip(weights,objective)),F())
assert norm==1 and min(slacks.values())>=0 and value>2
assert value==F(point['exact_primal_value'])and value-2==F(point['gap_above_two'])
new={k:str(v)for k,v in slacks.items()if k.startswith('cross_')};assert len(new)==69 and new==point['new_row_slacks']
assert sum(x>0 for x in weights)==point['nonzero_masses']==42
assert str(min(slacks.values()))==point['minimum_slack']=='0'
assert all(sha(Path(x['path']))==x['sha256']for x in before)
result={'status':'PASS_FIXED_64_SUPPORT_EXACT_516_ROW_PRIMAL_ONLY','rows':516,'columns':64,'positive_masses':42,'welfare_normalization':str(norm),'comparison_cover':str(value),'gap_above_two':str(value-2),'minimum_slack':str(min(slacks.values())),'zero_slack_count':sum(v==0 for v in slacks.values()),'all_slacks':{k:str(v)for k,v in slacks.items()},'all69_reported_cross_slacks_match':True,'row_function_sources':before,'shared_original_row_formulas_not_independent_implementation':True,'original_module_imports':0,'original_LP_entries':0,'all_type_pricing_entries':0,'SPE_search_entries':0,'exact_dual_or_optimality_certified':False,'actual_full_SPE_or_realizable_catalog_certified':False}
(out/'certificate.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
event={'entry_count':1,'started_utc':started,'argv':sys.argv,'cwd':str(Path.cwd()),'python':sys.version,'elapsed_seconds':time.monotonic()-t,'checker_sha256':sha(Path(__file__)),'inputs_before_after_same':True,'scope':'one exact stored primal with original shared row functions; no original LP/import/main or independent formula claim','certificate_sha256':sha(out/'certificate.json')}
(out/'event.json').write_text(json.dumps(event,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:result[k]for k in ['status','rows','columns','positive_masses','minimum_slack','zero_slack_count']},ensure_ascii=False))
