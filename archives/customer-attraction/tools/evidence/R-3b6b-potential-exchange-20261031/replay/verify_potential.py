from pathlib import Path
import json,sys
sys.path.insert(0,'.')
from customer_attraction import CustomerType,Instance,StrategyCertificate,verify_certificate
out=[]
for p in [Path('last_average_selection_certificate.json'),Path('last_average_selection_small_certificate.json')]:
 d=json.loads(p.read_text()); i=d['instance']; inst=Instance(tuple(i['topics']),tuple(CustomerType(frozenset(x['topics']),x['multiplicity']) for x in i['customers']),i['players']); cert=StrategyCertificate.from_dict(d['certificate']); r=verify_certificate(inst,cert); r.assert_valid(); w=inst.welfare(cert.terminal_counts); opt=inst.optimal_welfare(); out.append({'file':p.name,'checked_histories':r.checked_histories,'checked_deviations':r.checked_deviations,'welfare':w,'optimum':opt,'terminal_counts':cert.terminal_counts,'source_min_welfare':d['min_welfare'],'source_opt':d['opt']}); assert w==d['min_welfare'] and opt==d['opt']
print(json.dumps({'passed':True,'certificates':out},indent=2))
