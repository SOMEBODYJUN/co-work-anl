"""Run the unchanged original main once; serialize its existing return locals."""
from pathlib import Path
import json,runpy,sys
source=Path(sys.argv[1]).resolve()
captured={};main_returns=0
def profile(frame,event,arg):
    global main_returns
    if event=='return' and frame.f_code.co_name=='main' and Path(frame.f_code.co_filename).resolve()==source:
        main_returns+=1
        captured.update({'row_count':frame.f_locals['row_count'],
                         'averages':[str(x) for x in frame.f_locals['averages']],
                         'objective':str(frame.f_locals['obj']),
                         'support':[[i,j,str(w)] for i,j,w in frame.f_globals['SUPPORT']],
                         'pairs':[list(x) for x in frame.f_globals['PAIRS']]})
sys.setprofile(profile)
try:
    runpy.run_path(str(source),run_name='__main__')
finally:
    sys.setprofile(None)
assert main_returns==1 and len(captured['averages'])==83
captured['original_main_return_events']=main_returns
captured['capture_scope']='existing original-main locals only; no further row function calls or mathematical recomputation'
Path('captured-original-main-locals.json').write_text(json.dumps(captured,indent=2)+'\n')
