"""One fixed-input scalar qualification, not an independent implementation or CLI replay."""
import argparse,hashlib,json,time
from pathlib import Path
from fractions import Fraction as F
from qualified_scalar_loader import load

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--shared-evidence',type=Path,default=Path(__file__).resolve().parent.parent/'Boss7-resume-rcd-ap-tuple');args=ap.parse_args()
 here=Path(__file__).resolve().parent; start=time.perf_counter()
 p=here/'original/exact_max_menu_joint_primal.json';op=here/'original/omitted_tail_menu_slacks.json';d=json.loads(p.read_text());old=json.loads(op.read_text())
 L=load(args.shared_evidence);U=L.evaluator('joint');row_names=list(d['slacks']);total={n:F(0) for n in row_names};tail=None;W=F(0);O=F(0);atom_metrics=[]
 for i,a in enumerate(d['atoms']):
  L.verify_atom(a);assert len(a['max_bits'])==5 and set(a['max_bits'])<=set('01')
  x=F(a['exact_mass']);assert x>0
  rr=U.atom_rows(a);assert list(rr)==row_names
  assert all(isinstance(v,(int,F)) for v in rr.values())
  mb=tuple(map(int,a['max_bits']));tt={n:v for n,v in L.lm['rows'](a,mb).items() if ':tailmenu:' in n};assert len(tt)==28
  if tail is None:tail={n:F(0) for n in tt}
  for n,v in rr.items():total[n]+=x*v
  for n,v in tt.items():tail[n]+=x*v
  w=int(any(map(int,a['bits'][:5])));count=sum(a['AB_hist'][4:]);o=int(count>0);W+=x*w;O+=x*o
  atom_metrics.append({'index':i,'mass':str(x),'w':w,'d':count,'o':o,'max_bits':a['max_bits'],'minimum_coefficient':str(min(rr.values()))})
 eq=[{'row':n,'computed':str(v),'stored':d['slacks'][n],'equal':v==F(d['slacks'][n])} for n,v in total.items()];assert all(z['equal'] for z in eq);assert min(total.values())>=0
 assert W==F(d['welfare'])==1 and O==F(d['comparison_cover']) and O-2==F(d['gap_above_two']) and O>2
 # Preserve all 28 exact omitted values and the report's negative subset.
 saved=old.get('slacks',old.get('omitted_tail_menu_slacks'));assert saved is not None,old.keys()
 assert list(tail)==list(saved)
 teq=[{'row':n,'computed':str(v),'stored':saved[n],'equal':v==F(saved[n])} for n,v in tail.items()];assert all(z['equal'] for z in teq)
 negative={n:str(v) for n,v in tail.items() if v<0};assert negative==old['negative']
 for name,obj in [('all-3132-row-equalities.json',eq),('all-28-omitted-row-equalities.json',teq),('all-66-atom-metrics.json',atom_metrics),('selected-original-scalar-AST.json',L.contract)]:
  (here/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
 out={'scope':'Same whitelisted source scalar definitions as AP/tuple qualification; one different fixed 66-atom input. No independent coefficient implementation, original CLI, Universe initialization, LP, BI, price, full-domain certificate, game or SPE.','input':{'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)},'omitted_report':{'path':str(op),'bytes':op.stat().st_size,'sha256':sha(op)},'loader_sha256':sha(here/'qualified_scalar_loader.py'),'driver_sha256':sha(Path(__file__)),'shared_evidence_root':str(args.shared_evidence),'atoms':len(d['atoms']),'rows':len(total),'scalar_row_coefficients':len(d['atoms'])*len(total),'tail_coefficients':len(d['atoms'])*len(tail),'all_saved_3132_values_match':True,'minimum_slack':str(min(total.values())),'zero_slacks':sum(v==0 for v in total.values()),'W':str(W),'O':str(O),'gap':str(O-2),'omitted_rows':len(tail),'all_saved_28_values_match':True,'negative_omitted':negative,'seconds':time.perf_counter()-start}
 (here/'fixed-66-qualification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['scope','input','omitted_report']},ensure_ascii=False))
if __name__=='__main__':main()
