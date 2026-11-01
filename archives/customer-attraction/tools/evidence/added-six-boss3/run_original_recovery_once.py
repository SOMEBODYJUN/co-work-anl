from pathlib import Path
import json,subprocess,sys,time,platform,hashlib
from datetime import datetime,timezone
S=Path(__file__).resolve().parent;R=S.parent/'added_six_runtime';C=R/'research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087/next_credible';script=C/'recover_added.py';D=S/'replay';D.mkdir(exist_ok=True)
bootstrap='''import sys,runpy,json
from pathlib import Path
sys.path.insert(0,sys.argv[1])
e=runpy.run_path(sys.argv[2],run_name="__main__")
triples={n:v for n,v in e['slack'].items() if 'three-profit' in n}
metadata={'scope':'capture already computed original recovery namespace; no second matrix/LP/review execution','input_atoms':len(e['atoms']),'rows':len(e['names']),'selected_positive_float_indices':e['S'],'near_active_float_rows':len(e['active']),'exact_basis_rank':len(e['basis']),'exact_nonnegative_point':list(map(str,e['r'])),'row_names':e['names'],'all_original_computed_slacks':{n:str(v) for n,v in e['slack'].items()},'added_triple_rows':len(triples),'added_triple_positive_rows':sum(v>0 for v in triples.values()),'added_triple_zero_rows':sum(v==0 for v in triples.values()),'minimum_added_triple_slack':str(min(triples.values()))}
Path(sys.argv[3]).write_text(json.dumps(metadata,indent=2)+'\\n')
'''
cmd=[sys.executable,'-I','-B','-c',bootstrap,str(C),str(script),str(D/'recovery-internals.json')];start=datetime.now(timezone.utc).isoformat();tick=time.monotonic();result=subprocess.run(cmd,cwd=R,text=True,capture_output=True)
(D/'stdout.txt').write_text(result.stdout);(D/'stderr.txt').write_text(result.stderr);output=C/'enhanced_2396_exact_obstruction.json';frozen=S/'original/enhanced_2396_exact_obstruction.json'
if output.exists():(D/'enhanced_2396_exact_obstruction.json').write_bytes(output.read_bytes())
event={'event':'one unmodified original recover_added top-level through isolated runpy; namespace capture only reuses source-computed values','command':cmd,'cwd':str(R),'start_utc':start,'elapsed_seconds':time.monotonic()-tick,'exit_code':result.returncode,'Python':platform.python_version(),'assertions_enabled':True,'source_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'original_recovery_top_level_runs':1,'original_reopt_import_or_runs':0,'original_review2396_runs':0,'LP_calls':0,'output_file_bytes_equal':output.exists()and output.read_bytes()==frozen.read_bytes(),'output_file_fields_equal':output.exists()and json.loads(output.read_text())==json.loads(frozen.read_text()),'stdout_bytes':len(result.stdout.encode()),'stderr_bytes':len(result.stderr.encode())}
(D/'execution-record.json').write_text(json.dumps(event,ensure_ascii=False,indent=2)+'\n');print(json.dumps(event,ensure_ascii=False,indent=2));assert result.returncode==0,result.stderr;assert event['output_file_bytes_equal']
