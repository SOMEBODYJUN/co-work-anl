from pathlib import Path
import json,sys,subprocess,hashlib,traceback
root=Path(__file__).resolve().parents[3]; out=Path(__file__).resolve().parent
def reject(*a,**k): raise RuntimeError('Subprocess disabled for this pure-file validation')
subprocess.run=reject; subprocess.Popen=reject; subprocess.check_output=reject; subprocess.check_call=reject
sys.path.insert(0,str(root/'tools')); import registration
candidate=json.loads((out/'schema2-review-candidate.json').read_text()); pre=json.loads((out/'preimages-and-highest-mothers.json').read_text()); own={o['object_id'] for o in candidate['objects']}
peers={v['record']['object_id']:v['record'] for v in pre['highest_unique_mothers'].values() if v and v.get('record') and v['record']['object_id'] not in own}
report={'method':'direct registration.validate_batch only; subprocess API disabled; no compose/map_tasks/work.py/Git','candidate':{'path':str((out/'schema2-review-candidate.json').relative_to(root)),'sha256':hashlib.sha256((out/'schema2-review-candidate.json').read_bytes()).hexdigest()},'actual_DONE_peer_records':sorted(peers)}
try:
 report['result']=registration.validate_batch(root,candidate,expected_materials=[{k:r[k] for k in ['path','sha256']} for r in candidate['materials']],baseline_ref=candidate['baseline'],peer_objects=peers); report['status']='passed'
except Exception as e:
 report['status']='failed'; report['error']=str(e); report['traceback']=traceback.format_exc()
(out/'pure-file-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n'); print(json.dumps(report,ensure_ascii=False,indent=2))
