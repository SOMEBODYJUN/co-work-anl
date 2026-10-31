import json, sys
from pathlib import Path
sys.path.insert(0, str(Path('archives/customer-attraction/tools/evidence/R18-global-walk-agent')))
from customer_attraction.model import Instance
from customer_attraction.certificate import StrategyCertificate, verify_certificate
src=json.load(open('archives/customer-attraction/tools/evidence/R275-direct-m5-agent/multigadget_m5.json'))
inst=Instance.from_dict(src['instance'])
cert=StrategyCertificate.from_dict(src['certificate'])
res=verify_certificate(inst,cert)
out={'valid':res.valid,'checked_histories':res.checked_histories,'checked_deviations':res.checked_deviations,'errors':list(res.errors),'violations':len(res.violations),'terminal_counts':list(res.terminal_counts or ()), 'welfare':inst.welfare(res.terminal_counts), 'optimal_welfare':inst.optimal_welfare(), 'action_count':len(cert.actions)}
print(json.dumps(out,ensure_ascii=False,indent=2))
json.dump(out,open('archives/customer-attraction/tools/evidence/R275-direct-m5-agent/verification.json','w'),ensure_ascii=False,indent=2); open('archives/customer-attraction/tools/evidence/R275-direct-m5-agent/verification.json','a').write('\n')
