from pathlib import Path
import sys,json,runpy,collections
entry=str(Path(sys.argv[1]).resolve());out=Path(sys.argv[2]);kind=sys.argv[3];base=Path(sys.argv[4]).resolve();names=['__init__.py','model.py','exact.py','certificate.py'];allowed={entry:'entry'}
if kind=='graph':allowed.update({str(base/'customer_attraction'/n):'customer_attraction/'+n for n in names})
calls=collections.Counter();opens=[];final={};observing=True

def clean(x):
 if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
 if isinstance(x,(list,tuple,set,frozenset)):return [clean(v) for v in x]
 if isinstance(x,(str,int,float,bool)) or x is None:return x
 return str(x)
def profile(frame,event,arg):
 tag=allowed.get(frame.f_code.co_filename)
 if tag is None:return
 if event=='call':calls[tag+':'+frame.f_code.co_name]+=1
 elif event=='return' and tag=='entry' and frame.f_code.co_name=='main':
  for k in (['report','reports'] if kind=='graph' else ['report','count','type_checks','root_values','paths']):
   if k in frame.f_locals:final[k]=clean(frame.f_locals[k])
def audit(event,args):
 if observing and event=='open' and isinstance(args[0],str) and args[0].startswith(str(base)+'/'):opens.append({'path':args[0],'mode':args[1],'flags':args[2]})
sys.addaudithook(audit);sys.setprofile(profile)
try:runpy.run_path(entry,run_name='__main__')
finally:
 sys.setprofile(None);observing=False;loaded={k:getattr(v,'__file__',None) for k,v in sys.modules.items() if k=='customer_attraction' or k.startswith('customer_attraction.')};out.write_text(json.dumps({'function_calls':dict(calls),'observed_local_opens':opens,'final_original_values':final,'loaded_package_module_paths':loaded,'observer_extra_original_calls':0,'source_main_calls':calls['entry:main'],'source_module_calls':calls['entry:<module>']},ensure_ascii=False,indent=2)+'\n')
