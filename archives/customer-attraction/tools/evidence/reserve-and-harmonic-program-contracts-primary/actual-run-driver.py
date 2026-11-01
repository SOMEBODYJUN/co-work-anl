from pathlib import Path
import json,hashlib,shutil,subprocess,sys,os,time,datetime
ROOT=Path('/workspace/scratch/37f0f9248cfc');C=ROOT/'boss4-next-cache';REPO=ROOT/'boss4-research';S=C/'r3-reserve-and-harmonic-program-contracts-primary';E=S/'archives/customer-attraction/tools/evidence/reserve-and-harmonic-program-contracts-primary'
IDS=['f8347b1c5b29822e10f1','db566dc942e67451b332','d777439916095d914217','a2668489705adc1df311','d0bd5e3d11026c1f9730']
claim=json.loads(Path(sys.argv[1]).read_text());assert claim['status']=='pushed' and claim['actor']=='Boss4' and set(IDS)<=set(claim['ids']);sync=claim['local_sync']['status']
if sync=='needs-attention':
 proof=json.loads(Path(sys.argv[2]).read_text());assert proof['stash_kept'] and not proof['missing'] and not proof['different'] and not proof['unmerged'] and all(z['same'] for z in proof['tracked'])
else:assert sync=='synced'
m=json.loads((E/'source-manifest.json').read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def js(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
for x in m['rows']:
 p=REPO/'cleanup/progress'/(x['id']+'.json');d=json.loads(p.read_text());assert d['owner']=='Boss4' and d['disposition']=='in-progress' and d['source_sha256']==x['sha256'];assert sha(S/x['preserved_at'])==x['sha256']
results=[]
for name,ident in [('harmonic-independent','d777439916095d914217'),('harmonic-author','d0bd5e3d11026c1f9730')]:
 R=E/'runs'/name;assert not R.exists(),'already attempted, preserve first event and do not repeat';T=R/'source-root';T.mkdir(parents=True);x=next(x for x in m['rows'] if x['id']==ident);p=T/x['path'];p.parent.mkdir(parents=True);shutil.copyfile(S/x['preserved_at'],p);assert sha(p)==x['sha256'];args=[sys.executable,str(p.relative_to(T))];env=dict(os.environ,PYTHONOPTIMIZE='0',PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0');start=datetime.datetime.now(datetime.timezone.utc).isoformat();tick=time.monotonic();run=subprocess.run(args,cwd=T,env=env,capture_output=True,timeout=60);elapsed=time.monotonic()-tick;(R/'stdout.txt').write_bytes(run.stdout);(R/'stderr.txt').write_bytes(run.stderr);event=dict(source_id=ident,source_sha256=x['sha256'],argv=args,cwd=str(T),started_utc=start,ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),wall_seconds=elapsed,exit_code=run.returncode,stdout_sha256=sha(R/'stdout.txt'),stderr_sha256=sha(R/'stderr.txt'),source_inputs_unchanged=sha(p)==x['sha256'],new_empty_directory=True,stdlib_only=True,embedded_input_only=True,original_runs_at_top_level_without_main_guard=True,assertions_enabled_by_PYTHONOPTIMIZE_0=True,original_frozen_output_seeded=False,original_script_writes_report=False,seed_in_source=(3491 if name=='harmonic-independent' else None),random_samples=(60 if name=='harmonic-independent' else 0),claim_remote_tip=claim['remote_tip'],claim_original_local_sync=sync);js(R/'event.json',event);assert run.returncode==0,run.stderr.decode()
 if name=='harmonic-independent':
  out=json.loads(run.stdout);f=next(x for x in m['rows'] if x['id']=='a2668489705adc1df311');raw=(S/f['preserved_at']).read_bytes();assert out==json.loads(raw);same=run.stdout==raw;assert same;js(R/'frozen-comparison.json',dict(frozen_source_id=f['id'],frozen_sha256=f['sha256'],all_fields_equal=True,stdout_byte_identical=same,stdout_bytes=len(run.stdout),native_file_written=False));shutil.copyfile(R/'stdout.txt',R/'report.json')
 else:
  lines=run.stdout.decode().splitlines();assert len(lines)==13 and lines[-1]=='exact checks passed; 510 single-customer position patterns';js(R/'output-contract.json',dict(threshold_lines=12,position_patterns=510,original_frozen_report_not_available=True,native_file_written=False,universal_proof_not_inferred_from_run=True))
 results.append(dict(name=name,source_id=ident,exit_code=run.returncode,wall_seconds=elapsed,stdout_bytes=len(run.stdout)))
js(E/'new-entry-execution-summary.json',dict(new_original_entries=2,each_once=True,results=results,prior_MP_reserve_entry_repeated=False,prior_LW_69_entry_repeated=False,new_implementation_entries=0,extra_primary_done=0));print(json.dumps(results,ensure_ascii=False))
