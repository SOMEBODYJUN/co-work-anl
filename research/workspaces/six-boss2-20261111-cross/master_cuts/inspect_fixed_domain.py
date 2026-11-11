#!/usr/bin/env python3
"""Exact descriptor/normalization facts underlying the fixed-support caveat."""
from pathlib import Path
from fractions import Fraction as F
import gzip,json,hashlib,os,platform,sys,time
HERE=Path(__file__).resolve().parent
start=time.time();source=HERE/'dynamic_5727_matrix.json.gz'
with gzip.open(source,'rt') as f:m=json.load(f)
h=[dict(c,column_index=j) for j,c in enumerate(m['columns']) if c['kind']=='hist']
assert len(h)==16 and {c['d'] for c in h}=={1}
assert all(sum(c['hist'])==6 for c in h)
assert all(F(m['normalization'][j])==int(c['kind']=='hist') for j,c in enumerate(m['columns']))
assert all(F(m['objective'][j])==(int('1' in c['actual_bits']) if c['kind']=='hist' else 0) for j,c in enumerate(m['columns']))
report={'status':'passed','matrix_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'histogram_count':16,'all_histograms_d_equal_1':True,'normalization_is_total_hist_mass':True,'objective_is_actual_union_mass':True,'domain_consequence':'Every saved customer type belongs to exactly one comparison T. O=1 is total customer mass. Static union coverage cannot exceed O in any common realization. This does not give all-history SPE or cover the full client-type domain.','histograms':h,'execution':{'command':[sys.executable,'-B',str(Path(__file__).resolve())],'cwd':os.getcwd(),'python':platform.python_version(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'seconds':time.time()-start}}
(HERE/'fixed_domain_summary.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='histograms'},ensure_ascii=False))
