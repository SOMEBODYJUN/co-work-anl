from pathlib import Path
import runpy,json
x=runpy.run_path('research/workspaces/customer-attraction/R-7eb35cf5aa0f402c892d23bc658a0639/reserve/audit_uniform_reserve.py',run_name='__main__')
Path('native-data.json').write_text(json.dumps(x['data'],ensure_ascii=False,indent=2)+'\n')
