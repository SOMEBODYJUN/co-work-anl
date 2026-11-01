from pathlib import Path
from fractions import Fraction as F
import json,hashlib,time,datetime,sys
c=Path(__file__).resolve().parent;run=c/'root-penultimate-three-witness-check-001';assert not run.exists(),'one new independent witness check only';run.mkdir();started=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
ip=c/'root-joint-terminal-materialization-run-001/native-already-computed-unit-type-instance.json';rp=c/'resumed-next-root_penultimate_completion_two-originals/3da1f09eb44311acc9de/check_penultimate_completion.json';z=json.loads(ip.read_text());old=json.loads(rp.read_text());labels=z['labels'];idx={a:i for i,a in enumerate(labels)};customers=[(int(x['mask']),x['multiplicity'])for x in z['customer_types']];W=z['scaling'];calls=0
assert len(labels)==65 and len(customers)==1180

def profit(hist,role):
 global calls
 calls+=1;out=F(0)
 for mask,n in customers:
  if(mask>>hist[role])&1:
   d=sum((mask>>a)&1 for a in hist);assert d>=1;out+=F(n,d)
 return out
rows=[]
for report,forced in zip(old['results'],['L_third0','AE_S0','L_third0']):
 prefix=list(map(idx.__getitem__,report['prefix']));actual=profit(prefix+[idx[report['actual_action']],idx[report['actual_reply']]],3)/W
 q=idx[forced];vals=[profit(prefix+[q,b],4)for b in range(65)];mx=max(vals);brs=[b for b,v in enumerate(vals)if v==mx];floor=min(profit(prefix+[q,b],3)for b in brs)/W;gain=floor-actual
 assert str(actual)==report['actual_leader_utility_normalized']and str(floor)==report['maximum_guaranteed_deviation_normalized']and str(floor)==report['all_floor_payoffs'][forced]and gain>0
 original=next(d for d in report['guaranteed_profitable_deviations']if d['action']==forced);assert str(gain)==original['gain_normalized']and[labels[b]for b in brs]==original['all_last_best_replies']
 rows.append({'prefix':report['prefix'],'prescribed':[report['actual_action'],report['actual_reply']],'actual_leader_normalized':str(actual),'forced_action':forced,'all_last_best_replies':[labels[b]for b in brs],'minimum_leader_normalized':str(floor),'strict_gain_normalized':str(gain),'all65_last_utilities_normalized':[str(v/W)for v in vals],'reference_fields_exactly_match':True})
assert calls==201 and all(len(x['all_last_best_replies'])==1 for x in rows)
output={'scope':'three sufficient penultimate obstruction witnesses only; all65 legal final actions per witness; not rechecking all195 source floors or708 rows or complete SPE','unit_instance_sha256':hashlib.sha256(ip.read_bytes()).hexdigest(),'frozen_report_sha256':hashlib.sha256(rp.read_bytes()).hexdigest(),'rows':rows,'exact_utility_evaluations':calls,'original_import_or_native_entries':0,'new_independent_definition_implementation_entries':1}
(run/'certificate.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n');event={'started_utc':started,'elapsed_seconds':time.monotonic()-t,'python':sys.version,'executed_program_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'input_paths':[str(ip),str(rp)],'scope':output['scope'],'reference_fields_exactly_match':True,'all_three_strict_gains_positive':True,'mathematical_entries':1};(run/'event.json').write_text(json.dumps(event,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'checks':3,'exact_utility_evaluations':calls,'elapsed_seconds':event['elapsed_seconds'],'all_three_strict_gains_positive':True}));print(json.dumps([{k:v for k,v in r.items()if k!='all65_last_utilities_normalized'}for r in rows],ensure_ascii=False,indent=2))
