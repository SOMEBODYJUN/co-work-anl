from pathlib import Path
import sys,runpy,json,collections
entry=str(Path(sys.argv[1]).resolve());out=Path(sys.argv[2]);calls=collections.Counter();opens=[];final={}
def profile(frame,event,arg):
 if frame.f_code.co_filename!=entry:return
 if event=='call':calls[frame.f_code.co_name]+=1
 elif event=='return' and frame.f_code.co_name=='main':
  for k in ['total','hub_hypotheses','unanimous','report']:
   if k in frame.f_locals:final[k]=frame.f_locals[k]
def audit(event,args):
 if event=='open' and isinstance(args[0],str) and args[0].startswith(str(Path(entry).parent)+'/'):opens.append({'path':args[0],'mode':args[1],'flags':args[2]})
sys.addaudithook(audit);sys.setprofile(profile)
try:runpy.run_path(entry,run_name='__main__')
finally:
 sys.setprofile(None);out.write_text(json.dumps({'function_calls':dict(calls),'observed_local_opens':opens,'final_original_values':final,'observer_extra_original_calls':0},ensure_ascii=False,indent=2)+'\n')
