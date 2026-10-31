import sys,json
from pathlib import Path
sys.path.insert(0,'tmp/weak_matching_replay')
from customer_attraction import CustomerType,Instance,StrategyCertificate,verify_certificate
src=Path('archives/customer-attraction/tools/evidence/R-3b6b-counterexample-20261031/source/certified_m5k7_maximal.json')
d=json.loads(src.read_text())
i=d['instance']
inst=Instance(tuple(i['topics']),tuple(CustomerType(frozenset(x['topics']),x['multiplicity']) for x in i['customers']),i['players'])
cert=StrategyCertificate.from_dict(d['certificate'])
r=verify_certificate(inst,cert); r.assert_valid()
assert r.checked_histories==d['decision_histories'],(r.checked_histories,d['decision_histories'])
w=inst.welfare(cert.terminal_counts); opt=inst.optimal_welfare()
assert (w,opt)==(d['welfare'],d['optimum']),(w,opt,d['welfare'],d['optimum'])
assert str(opt//1)+'/'+str(w) == d['ratio'] or str(__import__('fractions').Fraction(opt,w))==d['ratio']
print(json.dumps({'passed':True,'checked_histories':r.checked_histories,'checked_deviations':r.checked_deviations,'welfare':w,'optimum':opt,'ratio':d['ratio'],'terminal_counts':cert.terminal_counts}))
