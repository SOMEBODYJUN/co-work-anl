"""Observe one raw entry; no extra original function calls."""
from pathlib import Path
import runpy,sys,json,collections
entry=str(Path(sys.argv[1]).resolve());out=Path(sys.argv[2]).resolve();kind=sys.argv[3];calls=collections.Counter();opens=[];final={};prefix=str(Path(entry).parent.parent)+'/'
def clean(x):
 if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
 if isinstance(x,(list,tuple,set,frozenset)):return [clean(v) for v in x]
 if isinstance(x,(str,int,float,bool)) or x is None:return x
 return str(x)
def profile(frame,event,arg):
 if frame.f_code.co_filename!=entry:return
 if event=='call':calls[frame.f_code.co_name]+=1
 elif event=='return' and ((kind=='uniform' and frame.f_code.co_name=='main') or (kind=='relay' and frame.f_code.co_name=='<module>')):
  keys=['report','failed','root_slacks','replay_rows','cases'] if kind=='uniform' else ['out','rho_checks','uniform_slacks','slacks','core_repairs','full_flip_bins']
  for k in keys:
   if k in frame.f_locals:final[k]=clean(frame.f_locals[k])
def audit(event,args):
 if event=='open' and isinstance(args[0],str) and args[0].startswith(prefix):opens.append({'path':args[0],'mode':args[1],'flags':args[2]})
sys.addaudithook(audit);sys.setprofile(profile)
try:runpy.run_path(entry,run_name='__main__')
finally:
 sys.setprofile(None);out.write_text(json.dumps({'function_calls':dict(calls),'observed_local_opens':opens,'final_original_values':final,'observer_extra_original_calls':0,'original_module_calls':calls['<module>'],'original_main_calls':calls['main']},ensure_ascii=False,indent=2)+'\n')
