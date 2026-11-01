"""Observe a single unchanged entry, without additional source-function calls."""
from pathlib import Path
import runpy,sys,json,collections
entry=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve();calls=collections.Counter();files=[];final={}
def profile(frame,event,arg):
 if Path(frame.f_code.co_filename).resolve()!=entry:return
 if event=='call':calls[frame.f_code.co_name]+=1
 elif event=='return' and frame.f_code.co_name=='main':
  for k in ['comparisons','minimum','t','D','core_cases','last_certificates','report']:
   if k in frame.f_locals:final[k]=frame.f_locals[k]
def audit(event,args):
 if event=='open' and isinstance(args[0],str):
  p=Path(args[0]);
  if p.is_absolute() and entry.parents[2] in p.parents:files.append({'path':str(p),'mode':args[1],'flags':args[2]})
def clean(v):
 if isinstance(v,dict):return {str(k):clean(x) for k,x in v.items()}
 if isinstance(v,(list,tuple,set,frozenset)):return [clean(x) for x in v]
 if isinstance(v,(str,int,float,bool)) or v is None:return v
 return str(v)
sys.addaudithook(audit);sys.setprofile(profile)
try:runpy.run_path(str(entry),run_name='__main__')
finally:
 sys.setprofile(None);out.write_text(json.dumps({'function_calls':dict(calls),'final_original_values':clean(final),'observed_local_opens':files,'observer_extra_original_calls':0,'entry_calls':calls['main']},ensure_ascii=False,indent=2)+'\n')
