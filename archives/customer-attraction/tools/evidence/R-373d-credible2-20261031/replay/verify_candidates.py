from pathlib import Path
import json,sys
sys.path.insert(0,'.');sys.path.insert(0,'tests/audits')
from customer_attraction import StrategyCertificate,verify_certificate
from customer_attraction_strategy_lp import instance_from_clones
out=[]
for p in sorted(Path('candidates').glob('*.json')):
 d=json.loads(p.read_text());ins=instance_from_clones(d['p'],d['m'],d['weights']);cert=StrategyCertificate.from_dict(d['strategy']);v=verify_certificate(ins,cert);v.assert_valid();out.append({'file':p.name,'verified_histories':v.checked_histories,'welfare':str(ins.welfare(cert.terminal_counts)),'optimum':str(ins.optimal_welfare()),'objective':d['objective'],'path':d['path']})
print(json.dumps({'passed':True,'candidates':out},indent=2))
