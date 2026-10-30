import json,runpy,sys
from pathlib import Path
calls=[]
def capture(frame,event,arg):
    if event=='call' and frame.f_code.co_name=='threshold_extrema':
        calls.append({k:[str(x) for x in frame.f_locals[k]] for k in ('num','den','lower','upper')})
sys.setprofile(capture)
try:
    runpy.run_path(sys.argv[1],run_name='__main__')
finally:
    sys.setprofile(None)
    Path('actual-threshold-inputs.json').write_text(json.dumps(calls,indent=2)+'\n')
