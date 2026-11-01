"""One default 24-LP source CLI replay. No all-query or dependency main run."""
from pathlib import Path
import argparse,hashlib,json,platform,shutil,subprocess,sys,tempfile,time
import numpy,scipy
HERE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--point',type=Path,default=HERE.parent/'nested-reply-projection-program/related/combined_branch_latest_exact.json')
a=ap.parse_args();point=a.point.resolve()
expected={'original/early_reply_requery_cuts.py':'b458f25360e3e35416f571b31af6dcc0418e6b1eb30894a8bde3965b03e0434a',
'related/old_query_reply_cuts.py':'1d2feaf16a20f6d64158b5a1887d63e5500d17489977ce604157af7c95f057d5',
'related/terminal_portfolio_cuts.py':'46815b59bb97fad17d2aab75ab9a698fe3a3884bc41caac4196bf8e0251d5389',
'related/priced_hidden_reply.py':'3579b2eae0ad29e3a5b0c081f2c3833e9e55dc0dd740fbcafe0eb7239443c5f3'}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for rel,value in expected.items():assert sha(HERE/rel)==value
assert sha(point)=='50d51fadd1bd5cc6f2eb2230f1c35ac7001e21a5a75d11e91f4e259c1bf69224'
out=HERE/'replay';out.mkdir(exist_ok=True)
with tempfile.TemporaryDirectory(prefix='source-layout-',dir=out) as temp:
    stage=Path(temp);(stage/'work.py').write_text('# Unexecuted source-path marker only.\n')
    mapping={HERE/'original/early_reply_requery_cuts.py':Path('research/early_reply_requery_cuts.py'),
             HERE/'related/old_query_reply_cuts.py':Path('research/old_query_reply_cuts.py'),
             HERE/'related/terminal_portfolio_cuts.py':Path('research/terminal_portfolio_cuts.py'),
             HERE/'related/priced_hidden_reply.py':Path('customer_attraction/priced_hidden_reply.py')}
    for src,rel in mapping.items():
        dest=stage/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest)
    before={str(rel):sha(stage/rel) for rel in mapping.values()};before['point']=sha(point)
    cmd=[sys.executable,'-B',str(stage/'research/early_reply_requery_cuts.py'),str(point),str(out/'report.json')]
    start=time.perf_counter();p=subprocess.run(cmd,cwd=stage,capture_output=True);elapsed=time.perf_counter()-start
    after={str(rel):sha(stage/rel) for rel in mapping.values()};after['point']=sha(point);assert before==after
    event={'command':cmd,'cwd':str(stage),'wall_seconds':elapsed,'exit_code':p.returncode,
           'python':platform.python_version(),'numpy':numpy.__version__,'scipy':scipy.__version__,
           'source_sha256':expected['original/early_reply_requery_cuts.py'],'input_sha256':sha(point),
           'before':before,'after':after,'original_main_calls':1,'all_queries':False,'dependency_main_calls':0,
           'layout':'temporary original code, unexecuted work.py marker and namespace customer_attraction with only original priced module; no original package initialization',
           'temporary_layout_removed':True,'stdout_bytes':len(p.stdout),'stderr_bytes':len(p.stderr)}
(out/'stdout.txt').write_bytes(p.stdout);(out/'stderr.txt').write_bytes(p.stderr)
(out/'execution.json').write_text(json.dumps(event,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(event,ensure_ascii=False,indent=2));print(p.stdout.decode())
if p.returncode:print(p.stderr.decode())
raise SystemExit(p.returncode)
