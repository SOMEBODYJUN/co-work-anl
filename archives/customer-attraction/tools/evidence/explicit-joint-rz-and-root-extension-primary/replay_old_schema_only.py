"""Call only the inherited old verifier once on frozen aggregated masses.
No joint_atoms/verify_joint_atoms entry, no ZZ recomputation and no optimizer.
"""
from pathlib import Path
from fractions import Fraction
from collections import Counter
import argparse,json,hashlib,sys,time,platform

def main():
 p=argparse.ArgumentParser();p.add_argument('--runtime',type=Path,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args();rt=args.runtime.resolve()
 sys.path[:0]=[str(rt),str(rt/'research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/six_astra'),str(rt/'research/workspaces/customer-attraction/R-07e871289a6b4c1fb07244c97eb4aac8/general_from_half5')]
 reads=set()
 def audit(event,values):
  if event=='open' and values and isinstance(values[0],str):
   q=Path(values[0])
   if q.is_file() and q.is_relative_to(rt):reads.add(q)
 sys.addaudithook(audit)
 import attractive_nested as at
 data=rt/'research/workspaces/customer-attraction/R-a8ee6fdb155c47da95540775b4a6a2db/closure/joint_atoms_old_schema.json';report=json.loads(data.read_text())
 saved={}
 def profile(frame,event,arg):
  if event=='return' and frame.f_code is at.verify.__code__:
   loc=frame.f_locals;saved['names']=list(loc['names']);saved['slacks']=list(map(str,loc['slacks']));saved['values']=list(map(str,loc['vals']))
 sys.setprofile(profile);start=time.perf_counter();result=at.verify(report);elapsed=time.perf_counter()-start;sys.setprofile(None)
 assert result['verified_rows']==3889 and result['minimum_slack']=='0'
 assert len(saved['slacks'])==3889 and len(saved['values'])==1905
 bound=sum(n.startswith(('joint-state-upper:','overlap-upper:')) for n in saved['names'])
 assert bound==2806
 raw=3889-bound;assert raw==1083
 zero=sum(Fraction(s)==0 for s in saved['slacks'])
 inputs=[{'path':str(q.relative_to(rt)),'size':q.stat().st_size,'sha256':hashlib.sha256(q.read_bytes()).hexdigest()} for q in sorted(reads)]
 output={'scope':'one inherited attractive_nested.verify on frozen1905 aggregated masses; no joint/ZZ entry or LP','result':result,'raw_rows':raw,'bound_rows':bound,'zero_slacks':zero,'positive_slacks':3889-zero,'row_names':saved['names'],'all_slacks':saved['slacks'],'all1905_values':saved['values'],'runtime_inputs_read':inputs,'input_sha256':hashlib.sha256(data.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'python':platform.python_version(),'assertions_enabled':__debug__,'elapsed_seconds':elapsed,'original_old_verify_calls':1,'original_full_joint_entry_calls':0,'literal_ZZ_rechecks':0,'LP_calls':0}
 args.output.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items() if k not in ('row_names','all_slacks','all1905_values','runtime_inputs_read')},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
