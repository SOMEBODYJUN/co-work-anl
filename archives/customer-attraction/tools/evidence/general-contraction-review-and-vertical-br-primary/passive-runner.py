"""Observe a single top-level raw source entry; never call its functions again."""
from pathlib import Path
import sys,runpy,json,collections
entry=str(Path(sys.argv[1]).resolve());target=Path(sys.argv[2]);kind=sys.argv[3];calls=collections.Counter();opens=[];final={};prefix=str(Path(entry).parent.parent)+'/'
def clean(x):
 if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
 if isinstance(x,(list,tuple,set,frozenset)):return [clean(v) for v in x]
 if isinstance(x,(str,int,float,bool)) or x is None:return x
 return str(x)
def profile(frame,event,arg):
 if frame.f_code.co_filename!=entry:return
 if event=='call':calls[frame.f_code.co_name]+=1
 elif event=='return' and frame.f_code.co_name=='<module>':
  for k in (['out','cases','a0','identity_checks'] if kind=='uniform' else ['out']):
   if k in frame.f_locals:final[k]=clean(frame.f_locals[k])
def audit(event,args):
 if event=='open' and isinstance(args[0],str) and args[0].startswith(prefix):opens.append({'path':args[0],'mode':args[1],'flags':args[2]})
sys.addaudithook(audit);sys.setprofile(profile)
try:runpy.run_path(entry,run_name='__main__')
finally:
 sys.setprofile(None);target.write_text(json.dumps({'function_calls':dict(calls),'observed_local_opens':opens,'final_original_values':final,'original_module_calls':calls['<module>'],'original_main_calls':calls['main'],'observer_extra_original_calls':0},ensure_ascii=False,indent=2)+'\n')
