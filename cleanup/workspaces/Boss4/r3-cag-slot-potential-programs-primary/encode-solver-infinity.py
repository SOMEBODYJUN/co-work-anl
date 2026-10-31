"""Lossless presentation encoding of nonfinite solver residuals; never executes original code."""
from pathlib import Path
import hashlib,json,math
W=Path(__file__).resolve().parent;E=W.parents[3]/'archives/customer-attraction/tools/evidence/cag-slot-potential-programs-primary';P=E/'replay-floor/complete-original-built-input-and-proposal.json';raw=P.read_bytes();data=json.loads(raw);changes=[]
def visit(value,path):
 if isinstance(value,float)and not math.isfinite(value):
  encoded='NaN'if math.isnan(value)else('Infinity'if value>0 else'-Infinity');changes.append({'path':path,'encoded':encoded,'float_hex':value.hex()});return encoded
 if isinstance(value,list):return[visit(v,path+[i])for i,v in enumerate(value)]
 if isinstance(value,dict):return{k:visit(v,path+[k])for k,v in value.items()}
 return value
assert changes==[];clean=visit(data,[]);assert changes,'Do not repeat snapshot normalization'
clean['nonfinite_float_encoding']='IEEE nonfinite OptimizeResult residuals are string encoded; finite proposal x floats and hexadecimal copies preserved; original source stdout/report unchanged.'
P.write_text(json.dumps(clean,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
log={'scope':'post-run representation normalization only, not a source program call or solver retry','original_snapshot_bytes':len(raw),'original_snapshot_sha256':hashlib.sha256(raw).hexdigest(),'new_snapshot_bytes':P.stat().st_size,'new_snapshot_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'nonfinite_values':changes,'original_reports_and_stdout_untouched':True}
(W/'snapshot-nonfinite-encoding.json').write_text(json.dumps(log,ensure_ascii=False,indent=2,allow_nan=False)+'\n');print('encoded',len(changes),'solver residual infinities; bytes',P.stat().st_size)
