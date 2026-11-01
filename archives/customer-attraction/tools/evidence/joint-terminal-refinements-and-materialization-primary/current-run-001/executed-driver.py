from pathlib import Path
import json,hashlib,shutil,subprocess,sys,time,datetime
c=Path(__file__).resolve().parent;repo=c.parent/'boss4-research';run=c/'root-joint-terminal-materialization-run-001';assert not run.exists(),'one original wrapped entry only'
inv={x['id']:x for x in map(json.loads,(repo/'cleanup/inventory.jsonl').read_text().splitlines())}
rows=json.loads((c/'resumed-next-root_joint_terminal_four-originals/actual-source-manifest.json').read_text())['rows'];src={x['id']:Path(x['local_path'])for x in rows}
src['daf43c377037eed6e5cc']=repo/'archives/customer-attraction/tools/evidence/five-player-indexed/evidence/certificates/customer_attraction/five_player_indexed_bound.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
before=[]
for sid in ['c7f3dce5073dbce44d3a','6a5e43928a2b09522a28','daf43c377037eed6e5cc']:
 p=src[sid];x=inv[sid];assert sha(p)==x['sha256']and p.stat().st_size==x['size'];q=run/'tree'/x['path'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q);before.append({'id':sid,'source':str(p),'isolated':str(q),'sha256':sha(p),'size':p.stat().st_size})
wrapper=run/'capture_already_computed_globals.py'
wrapper.write_text("""from pathlib import Path
import sys,runpy,json,contextlib
out=Path(__file__).resolve().parent
with (out/'native-stdout.txt').open('w') as stdout,(out/'native-stderr.txt').open('w') as stderr:
 with contextlib.redirect_stdout(stdout),contextlib.redirect_stderr(stderr):
  values=runpy.run_path(sys.argv[1],run_name='__main__')
# Serialize only values the original already computed; no utility or row call.
data={'labels':values['labels'],'scaling':values['scale'],'customer_types':[{'mask':str(mask),'multiplicity':count}for mask,count in values['customers'].items()]}
(out/'native-already-computed-unit-type-instance.json').write_text(json.dumps(data,indent=2)+'\\n')
""")
code=run/'tree'/inv['c7f3dce5073dbce44d3a']['path'];argv=[sys.executable,'-I','-B',str(wrapper),str(code)]
started=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic();p=subprocess.run(argv,cwd=run/'tree',stdin=subprocess.DEVNULL,capture_output=True);elapsed=time.monotonic()-t
(run/'wrapper-stdout.txt').write_bytes(p.stdout);(run/'wrapper-stderr.txt').write_bytes(p.stderr)
assert all(sha(Path(x['source']))==x['sha256']==sha(Path(x['isolated']))for x in before)
new=run/'tree'/inv['f5325553c3ee777a361a']['path'];old=src['f5325553c3ee777a361a'];same=new.is_file()and new.read_bytes()==old.read_bytes()
event={'started_utc':started,'argv':argv,'cwd':str(run/'tree'),'python':sys.version,'elapsed_seconds':elapsed,'exit_code':p.returncode,'wrapper_stdout_bytes':len(p.stdout),'wrapper_stderr_bytes':len(p.stderr),'before':before,'source_and_isolated_inputs_unchanged':True,'new_report_sha256':sha(new)if new.exists()else None,'frozen_report_sha256':sha(old),'report_byte_identical':same,'report_fields_equal':json.loads(new.read_text())==json.loads(old.read_text())if new.exists()else False,'original_wrapped_entries':1,'direct_original_CLI_entries':0,'new_mathematical_implementations':0,'globals_serialization':'original already-computed labels/scaling/customer masks and multiplicities only; no second utility or matrix call','scope':'integer instance of65 distinct topics and33 specified final-player nodes,2145incl-own comparisons; not a full SPE or all708-primal-row recheck'}
(run/'event.json').write_text(json.dumps(event,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:event[k]for k in ['elapsed_seconds','exit_code','report_byte_identical','report_fields_equal']}));assert p.returncode==0 and not p.stderr and same
