"""Read-only known-instance attack of the new myopic ceiling relaxation."""
from pathlib import Path
import sys,json,time
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[5]
sys.path[:0]=[str(ROOT),str(Path(__file__).parent.parent/'independent')]
from customer_attraction import Instance
from myopic_ceiling_dp import MyopicCeilingFloor

records=[]
for path in sorted((ROOT/'examples/customer_attraction').glob('*.json')):
 try:ins=Instance.from_dict(json.loads(path.read_text()))
 except Exception:continue
 if ins.topic_count>8 or ins.players>8:continue
 t=time.time();dp=MyopicCeilingFloor(ins);G=dp.root();OPT=ins.optimal_welfare()
 if not OPT:continue
 record={'file':str(path.relative_to(ROOT)),'m':ins.players,'p':ins.topic_count,'G':str(G),'OPT':OPT,'G_over_OPT':str(G/OPT),'seconds':round(time.time()-t,3)}
 records.append(record)
 print(json.dumps(record),flush=True)
 if G<F(OPT,2):print('FATAL',str(path),flush=True)
records.sort(key=lambda d:F(d['G_over_OPT']))
Path(__file__).with_name('probe_myopic_known.json').write_text(json.dumps(records,indent=2)+'\n')
