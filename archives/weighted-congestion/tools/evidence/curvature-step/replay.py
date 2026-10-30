#!/usr/bin/env python3
"""Replay unchanged frozen curvature/step audits; save complete output and differences.
Run from any working directory. Originals are never overwritten.
"""
import concurrent.futures, hashlib, json, platform, subprocess, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
ORIGINAL=ROOT/'original'
RUN=ROOT/'rerun'
RUN.mkdir(exist_ok=True)
JOBS=[
 ('curvature', 'polynomial_curvature/verify.py', 'polynomial_curvature/results.json', 'run'),
 ('envelope', 'polynomial_curvature/extension_verify.py', None, 'run'),
 ('leakage-author', 'polynomial_curvature/verify_dag_low_leakage.py', 'polynomial_curvature/dag_low_leakage.json', None),
 ('leakage-independent', 'polynomial_curvature/independent_dag_low_leakage.py', 'polynomial_curvature/dag_low_leakage_independent.json', None),
 ('step-author', 'step_dag/verify.py', 'step_dag/verification.json', 'run'),
 ('step-independent', 'step_dag/independent_audit.py', None, None),
 ('all-in-author', 'step_dag/verify_polynomial_extremal_all_in.py', 'step_dag/polynomial_extremal_all_in.json', None),
 ('all-in-independent', 'step_dag/independent_polynomial_all_in.py', 'step_dag/polynomial_extremal_all_in_independent.json', None),
]
def differences(a,b,path='$'):
 if type(a)!=type(b): return [dict(path=path, frozen=a, rerun=b)]
 if isinstance(a,dict):
  result=[]
  for k in sorted(a.keys()|b.keys()):
   if k not in a or k not in b:result.append(dict(path=path+'.'+k,frozen=a.get(k),rerun=b.get(k)))
   else:result.extend(differences(a[k],b[k],path+'.'+k))
  return result
 if isinstance(a,list):
  if len(a)!=len(b):return [dict(path=path+'.length',frozen=len(a),rerun=len(b))]
  return [d for i,(x,y) in enumerate(zip(a,b)) for d in differences(x,y,path+f'[{i}]')]
 return [] if a==b else [dict(path=path,frozen=a,rerun=b)]
def run(job):
 label, script_rel, record_rel, function=job
 script=ORIGINAL/'tests/audits/weighted_congestion'/script_rel
 if function:
  command=[sys.executable,'-c',"import runpy,json,sys; print(json.dumps(runpy.run_path(sys.argv[1])['run'](),indent=2))",str(script)]
 else: command=[sys.executable,str(script)]
 start=time.monotonic()
 r=subprocess.run(command,text=True,capture_output=True)
 (RUN/(label+'.stdout.json')).write_text(r.stdout)
 (RUN/(label+'.stderr.txt')).write_text(r.stderr)
 item=dict(label=label,command=command,returncode=r.returncode,seconds=round(time.monotonic()-start,3),source_sha256=hashlib.sha256(script.read_bytes()).hexdigest())
 if r.returncode: item['error']=r.stderr
 elif record_rel:
  frozen=json.loads((ORIGINAL/'evidence/runs/weighted_congestion'/record_rel).read_text())
  fresh=json.loads(r.stdout)
  item['differences']=differences(frozen,fresh)
 else:item['differences']=None
 return item
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: results=list(pool.map(run,JOBS))
 report=dict(python=platform.python_version(),scope='Exact finite regressions only; metadata differences retained, not hidden.',jobs=results)
 (RUN/'replay-summary.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(report,ensure_ascii=False,indent=2))
 assert all(r['returncode']==0 for r in results)
 assert all(r['differences'] is None or all(d['path']=='$.python' for d in r['differences']) for r in results)
