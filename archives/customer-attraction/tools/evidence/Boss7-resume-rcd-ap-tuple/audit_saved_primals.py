"""One fixed-input Fraction qualification; no LP/search/original CLI/BI.
Uses the original scalar functions extracted by qualified_scalar_loader.py.
"""
from fractions import Fraction as F
from pathlib import Path
from collections import Counter
import hashlib,json,time,sys
from qualified_scalar_loader import load
ROOT=Path(__file__).resolve().parent
CASES=[('menu','435e9d4bab69861905d1','exact_menu_ap_primal.json','64d42044677286960ce2','menu_ap_discovery.json',76,2621),
       ('tuple','5db6a037342bdee0f107','exact_max_menu_tuple_primal.json','cd89b461ba6f34668855','max_menu_tuple_discovery.json',61,4007)]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def no_old_mass(a):return {k:v for k,v in a.items() if k!='exact_mass'}
def run():
 start=time.monotonic(); L=load(ROOT); results=[]
 (ROOT/'selected-original-scalar-AST.json').write_text(json.dumps(L.contract,indent=2)+'\n')
 for mode,eid,ename,did,dname,natoms,nrows in CASES:
  src=ROOT/'original'/eid/ename; discovery=ROOT/'original'/did/dname
  exact=json.loads(src.read_text());floatpoint=json.loads(discovery.read_text());u=L.evaluator(mode)
  assert len(exact['atoms'])==exact['positive_atoms']==natoms
  assert len(exact['slacks'])==exact['row_count']==nrows
  assert len(floatpoint['row_names'])==len(set(floatpoint['row_names']))==nrows
  assert set(floatpoint['row_names'])==set(exact['slacks'])
  assert len(floatpoint['atoms'])==len(floatpoint['primal_float'])
  selected=[a for a,v in zip(floatpoint['atoms'],floatpoint['primal_float']) if v>1e-8]
  assert [no_old_mass(a) for a in selected]==[no_old_mass(a) for a in exact['atoms']]
  assert exact['source_sha256']==sha(discovery)
  slacks={name:F(0) for name in exact['slacks']};W=O=F(0); atomvalues=[]
  for i,a in enumerate(exact['atoms']):
   bits,hs,d=L.verify_atom(a)
   if mode=='tuple':assert len(a['max_bits'])==5 and set(a['max_bits'])<={'0','1'}
   mass=F(a['exact_mass']);assert mass>0
   rr=u.atom_rows(a);assert set(rr)==set(slacks)
   assert all(isinstance(v,(int,F)) for v in rr.values())
   for name,v in rr.items():slacks[name]+=mass*v
   ww=int(any(bits[:5]));oo=int(d>0);W+=mass*ww;O+=mass*oo
   atomvalues.append({'index':i,'exact_mass':str(mass),'W_bit':ww,'O_bit':oo,'optimal_multiplicity':d,
     'coefficients_sha256':hashlib.sha256(json.dumps({n:str(rr[n]) for n in floatpoint['row_names']},separators=(',',':')).encode()).hexdigest(),
     'coefficient_count':len(rr)})
  mismatches={n:{'saved':exact['slacks'][n],'computed':str(v)} for n,v in slacks.items() if v!=F(exact['slacks'][n])}
  assert not mismatches,mismatches
  assert W==F(exact['welfare'])==1
  assert O==F(exact['comparison_cover'])>2
  assert O-2==F(exact['gap_above_two'])
  minimum=min(slacks.values());zeros=sum(v==0 for v in slacks.values())
  assert minimum==F(exact['minimum_exact_slack']) and minimum>=0
  assert zeros==exact['zero_slacks']
  rows=[{'index':i,'name':n,'saved':exact['slacks'][n],'computed':str(slacks[n]),'equal':True,'nonnegative':slacks[n]>=0} for i,n in enumerate(floatpoint['row_names'])]
  (ROOT/(mode+'-all-row-equalities.json')).write_text(json.dumps(rows,indent=2)+'\n')
  (ROOT/(mode+'-all-atom-metrics.json')).write_text(json.dumps(atomvalues,indent=2)+'\n')
  results.append({'mode':mode,'input':str(src.relative_to(ROOT)),'input_sha256':sha(src),
   'discovery':str(discovery.relative_to(ROOT)),'discovery_sha256':sha(discovery),
   'positive_atoms':natoms,'rows':nrows,'evaluated_atom_coefficients':natoms*nrows,
   'all_saved_slacks_equal_recomputed':True,'all_slacks_nonnegative':True,
   'minimum_slack':str(minimum),'zero_slacks':zeros,'W':str(W),'O':str(O),'gap_above_two':str(O-2),
   'selected_float_support_structure_equal':True,
   'saved_menu_code_sha256':exact['code_sha256'],
   'current_menu_code_sha256':sha(ROOT/'original/95ae42780dac898a9c0d/menu_ap_pricing.py'),
   'historical_generator_same_version_certified':False,
   'scope':'Fixed saved masses, current frozen scalar formulas only; original source-function extraction, not independent implementation. No game/SPE/actual OPT/global dual claim.'})
 report={'cases':results,'row_equalities':sum(r['rows'] for r in results),
  'evaluated_atom_coefficients':sum(r['evaluated_atom_coefficients'] for r in results),
  'original_imports_executed':False,'original_main_init_qr_lp_bi_price_executed':False,
  'elapsed_seconds':time.monotonic()-start,'driver_sha256':sha(Path(__file__)),
  'loader_sha256':sha(ROOT/'qualified_scalar_loader.py')}
 (ROOT/'saved-primal-qualification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':run()
