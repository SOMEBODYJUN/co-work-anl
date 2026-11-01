from pathlib import Path
import json,hashlib,shutil
src=Path('cleanup/workspaces/Boss7/security_n7p8_source.json')
ev=Path('archives/customer-attraction/tools/evidence/R275-security-n7p8-agent'); ev.mkdir(parents=True,exist_ok=True)
shutil.copyfile(src,ev/'policy_iteration_n7p8_individual.json')
manifest={'source_id':'92a9d1bbe6ff5e844e55','source_path':'research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/security_global/policy_iteration_n7p8_individual.json','source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'source_bytes':src.stat().st_size,'related_script':'archives/customer-attraction/tools/evidence/R275-security-policy-agent/random_refined_scan.py','related_policy_script':'cleanup/workspaces/Boss7/security_policy_source.py','scope':'finite policy-iteration individual security candidate; no universal theorem','stats':{'n':7,'p':8,'individual':True,'restart':1,'step':9,'gap':-0.05843768634465096,'query_index':8,'root':[0,6,0,0,0,0,1,0],'weight_support':6,'weight_sum':1.0,'policy_levels':[1,8,36,120,330,792,1716]}}
(ev/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
