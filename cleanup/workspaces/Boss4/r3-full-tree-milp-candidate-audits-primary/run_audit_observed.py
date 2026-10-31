"""Execute unmodified original audit main once, observe its completed duals.

The trace reads mathematical locals immediately before records.append. It
does not change values, call another optimizer, or alter the original code.
This makes previously omitted multipliers replayable by a standalone checker.
"""
from pathlib import Path
from fractions import Fraction
import contextlib,hashlib,io,json,os,platform,runpy,sys,time,traceback
import numpy,scipy

sys.dont_write_bytecode=True

S=Path(__file__).resolve().parents[4]
E=S/'archives/customer-attraction/tools/evidence/full-tree-milp-candidate-audits-primary'
tree=E/'replay-tree';sub=Path('research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/next_boss')
target=tree/sub/'audit_milp_candidates.py';out=E/'replay-audit';out.mkdir(parents=True,exist_ok=True)
if (out/'started.json').exists():raise SystemExit('Original audit already started; do not repeat')
deps=json.loads((E/'dependency-manifest.json').read_text())
inputs=[tree/x['path'] for x in deps['sources'] if x['role']=='runtime-input-not-primary']
output=out/'exact_candidate_audit.json'
argv=[str(target),*[str(x) for x in inputs],'--out',str(output)]
lines=target.read_text().splitlines();line=next(i+1 for i,s in enumerate(lines) if 'records.append(dict(portfolio=proposal[' in s)
def enc(v):
    if isinstance(v,Fraction):return str(v)
    if isinstance(v,dict):return {str(k):enc(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [enc(x) for x in v]
    return v
observed=[]
seen=set()
def trace(frame,event,arg):
    if frame.f_code.co_filename!=str(target):return None
    if event=='line' and frame.f_lineno==line:
        d=frame.f_locals;c=d['cone']
        identity=(str(d['path']),len(d['records']))
        if identity in seen:return trace
        seen.add(identity)
        rowbytes=json.dumps(enc(c.rows),separators=(',',':')).encode()
        observed.append(enc({'input':str(d['path'].relative_to(tree)),'portfolio':d['proposal']['portfolio'],
         'beta':d['beta'],'dual_support':[(i,v) for i,v in enumerate(d['dual']) if v],
         'rows_count':len(c.rows),'rows_fraction_lex_order_sha256':hashlib.sha256(rowbytes).hexdigest(),
         'norm':d['norm'],'objective':d['objective'],'normalized_primal':d['values'],
         'dual_coordinate_residuals':d['residual'],'exact_dual_check_in_original':bool(d['exact_dual']),
         'primal_value':d['dot'](d['objective'],d['values']) if 'dot' in d else frame.f_globals['dot'](d['objective'],d['values'])}))
    return trace
meta={'actual_invocation':'runpy.run_path of unmodified original entry, run_name=__main__; read-only local observer',
 'original_argv':argv,'original_source_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
 'original_main_runs_this_batch':1,'expected_fixed_cone_LP_calls':14,'new_MILP_calls':0,
 'python':platform.python_version(),'numpy':numpy.__version__,'scipy':scipy.__version__,
 'input_files':8,'runtime_code_files':6,'observer_changes_original_values':False,
 'observer_calls_optimizer':False,'trace_line':line,'started_unix':time.time()}
(out/'started.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
oldargv=sys.argv[:];oldcwd=Path.cwd();stdout=io.StringIO();stderr=io.StringIO();start=time.monotonic();rc=0
try:
    os.chdir(tree);sys.argv=argv
    with contextlib.redirect_stdout(stdout),contextlib.redirect_stderr(stderr):
        sys.settrace(trace)
        runpy.run_path(str(target),run_name='__main__')
except BaseException:
    rc=1;traceback.print_exc(file=stderr)
finally:
    sys.settrace(None);sys.argv=oldargv;os.chdir(oldcwd)
meta.update(returncode=rc,wall_seconds=time.monotonic()-start,stdout_bytes=len(stdout.getvalue().encode()),
            stderr_bytes=len(stderr.getvalue().encode()),observed_dual_records=len(observed),
            fixed_cone_LP_calls_completed=len(observed),observer_deduplicates_multiline_trace_events=True)
(out/'stdout.txt').write_text(stdout.getvalue());(out/'stderr.txt').write_text(stderr.getvalue())
(out/'observed-exact-duals.json').write_text(json.dumps({'scope':'new read-only observations of the original single audit run; not multipliers saved in frozen primary report',
 'original_main_runs':1,'additional_optimizer_calls':0,'records':observed},ensure_ascii=False,indent=2)+'\n')
old=next((E/'original'/sub).glob('exact_candidate_audit.json')).read_bytes()
if output.exists():
    new=output.read_bytes();meta.update(output_bytes=len(new),output_sha256=hashlib.sha256(new).hexdigest(),
      frozen_sha256=hashlib.sha256(old).hexdigest(),byte_identical=new==old,
      json_identical=json.loads(new)==json.loads(old))
(out/'execution.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(meta,ensure_ascii=False))
if rc:raise SystemExit(rc)
