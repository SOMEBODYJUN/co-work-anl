from pathlib import Path
import json,hashlib,shutil,subprocess,sys,os,time,datetime
ROOT=Path('/workspace/scratch/37f0f9248cfc');C=ROOT/'boss4-next-cache';REPO=ROOT/'boss4-research';S=C/'r3-background-interval-and-br-credit-review-primary';E=S/'archives/customer-attraction/tools/evidence/background-interval-and-br-credit-review-primary';IDS=['fb676b21950e0b1f2fe2','70fef0c029b8348d922e','07f5a50cd6c739bfd75e','148a41a135772b7c242d','9d71b6f39c90b2b87029']
claim=json.loads((ROOT/'boss4-r3-next-ni-claim.json').read_text());assert claim['status']=='pushed' and claim['actor']=='Boss4' and set(IDS)<=set(claim['ids']) and claim['local_sync']['status']=='synced'
main=json.loads((E/'source-manifest.json').read_text());m=json.loads((E/'related-original-program-manifest.json').read_text());assert m['all_two_certificates_every_row_and_field_read']
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def js(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
for x in main['rows']:
 d=json.loads((REPO/'cleanup/progress'/(x['id']+'.json')).read_text());assert d['owner']=='Boss4' and d['disposition']=='in-progress' and d['source_sha256']==x['sha256']
byid={x['id']:x for x in m['rows']};results=[]
for name,codeid,inputids,args,frozenid,outname in [('kernel-m5','0e4814f8788c5cfbfce3',['c388d1ee1cf9aeeb96fc'],['--m5'],'0215ced382911cf356e6','kernel_debt_independent_audit.json'),('kernel-m8','0e4814f8788c5cfbfce3',['fe415b54d0e09b2d0c48'],['--m8'],'04d1e2ca2e207a865455','kernel_debt_m8_independent_audit.json'),('safe-values','5136407ae621912d6ae6',[],[],'2d40bf1a2bf9101d458d','safe_value_audit.json')]:
 R=E/'runs'/name;assert not R.exists(),'already attempted; preserve first event, do not repeat';T=R/'source-root';T.mkdir(parents=True);x=byid[codeid];inputs=[x]+[byid[t] for t in inputids]
 for row in inputs:
  a=S/row['preserved_at'];assert sha(a)==row['sha256'];b=T/row['path'];b.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a,b)
 argv=[sys.executable,x['path']]+args;env=dict(os.environ,PYTHONOPTIMIZE='0',PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0');started=datetime.datetime.now(datetime.timezone.utc).isoformat();tick=time.monotonic();js(R/'planned-entry.json',dict(argv=argv,code_sha256=x['sha256'],inputs=[dict(id=t['id'],sha256=t['sha256']) for t in inputs],claim_tip=claim['remote_tip']))
 try:
  p=subprocess.run(argv,cwd=T,env=env,capture_output=True,timeout=60);rc=p.returncode;stdout=p.stdout;stderr=p.stderr;timeout=False
 except subprocess.TimeoutExpired as exc:
  rc=124;stdout=exc.stdout or b'';stderr=(exc.stderr or b'')+b'\nOriginal entry timeout after 60 seconds.\n';timeout=True
 elapsed=time.monotonic()-tick;(R/'stdout.txt').write_bytes(stdout);(R/'stderr.txt').write_bytes(stderr)
 event=dict(source_id=codeid,source_sha256=x['sha256'],argv=argv,cwd=str(T),started_utc=started,ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),wall_seconds=elapsed,exit_code=rc,timeout=timeout,stdout_sha256=sha(R/'stdout.txt'),stderr_sha256=sha(R/'stderr.txt'),source_inputs_unchanged=all(sha(T/t['path'])==t['sha256'] for t in inputs),source_input_ids=inputids,new_empty_directory=True,stdlib_only=True,assertions_enabled_by_PYTHONOPTIMIZE_0=True,original_frozen_output_seeded=False,related_primary_done=False,original_generator_7917_executed=False,driver_sha256=sha(Path(__file__)),claim_remote_tip=claim['remote_tip']);js(R/'event.json',event);assert rc==0,stderr.decode()
 native=(T/x['path']).with_name(outname);assert native.exists();shutil.copyfile(native,R/'report.json');frozen=byid[frozenid];raw=(S/frozen['preserved_at']).read_bytes();nativeobj=json.loads(native.read_bytes());oldobj=json.loads(raw);outobj=json.loads(stdout);assert nativeobj==oldobj==outobj
 cmp=dict(frozen_source_id=frozenid,frozen_sha256=frozen['sha256'],generated_file_byte_identical=native.read_bytes()==raw,stdout_byte_identical=stdout==raw,all_fields_equal=True,generated_bytes=native.stat().st_size,stdout_bytes=len(stdout),original_script_writes_report=True,original_report_seeded=False);js(R/'frozen-comparison.json',cmp);assert cmp['generated_file_byte_identical'];results.append(dict(name=name,code_id=codeid,argv=argv,exit_code=rc,wall_seconds=elapsed,stdout_bytes=len(stdout),report_bytes=native.stat().st_size,frozen_file_byte_identical=True,stdout_byte_identical=cmp['stdout_byte_identical']))
js(E/'actual-entry-execution-summary.json',dict(current_original_entries=3,unique_original_code_sources_executed=2,kernel_code_modes=['--m5','--m8'],each_mode_once=True,results=results,original_generator_7917_entries=0,new_implementation_entries=0,extra_primary_done=0));print(json.dumps(results,ensure_ascii=False))
