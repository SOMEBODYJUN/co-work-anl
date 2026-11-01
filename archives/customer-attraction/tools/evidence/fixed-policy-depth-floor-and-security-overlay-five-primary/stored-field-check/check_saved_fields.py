"""Only saved-field arithmetic/probability-domain checks, no payoff or LP."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,sys
fixed=Path(sys.argv[1]);overlay=Path(sys.argv[2]);index=Path(sys.argv[3]);output=Path(sys.argv[4])
before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [fixed,overlay]};fr=json.loads(fixed.read_text());ov=json.loads(overlay.read_text());rows=json.loads(index.read_text());files={x['path']:json.loads(Path(x['local_path']).read_text()) for x in rows}
fixed_checks=[]
for r in fr:
 n,k=r['positions'],r['catalog'];g=files['examples/customer_attraction/'+r['instance']+'.json'];cert=files['evidence/certificates/customer_attraction/'+r['instance']+'.json'];assert g['players']==n and len(g['topics'])==k
 vals=list(map(F,r['position_floors']));assert len(vals)==n and sum(vals)==F(r['floor_sum']);assert len(r['root'])==len(r['root_utilities'])==n and vals[0]==F(r['root_utilities'][0])
 assert len(r['floor_witness_histories'])==n and all(len(h)==i and all(type(a) is int and 0<=a<k for a in h) for i,h in enumerate(r['floor_witness_histories']))
 assert r['histories']==len(cert['strategy']['actions'])==sum(k**d for d in range(n)) and r['comparisons']==k*r['histories']
 item=dict(instance=r['instance'],stored_floor_sum_consistent=True,witnesses_legal=True,reported_domain_count_consistent=True)
 if 'security_value' in r:
  assert sum(vals)-n*F(r['security_value'])==F(r['floor_security_gap']);sc=cert['security'];p=list(map(F,sc.get('primary',sc.get('p'))));Q=sc.get('dual',sc.get('Q'));assert len(p)==k and min(p)>=0 and sum(p)==1
  probs=[]
  for qrow in Q:
   B=qrow.get('rivals',qrow.get('competitors',qrow.get('background')));q=F(qrow.get('probability',qrow.get('weight')));assert len(B)==n-1 and all(type(a) is int and 0<=a<k for a in B) and q>=0;probs.append(q)
  assert sum(probs)==1;item.update(stored_exact_gap_consistent=True,saved_primal_and_dual_probability_domains_legal=True,static_query_or_matrix_evaluation=False)
 else:
  assert float(sum(vals))-n*r['security_value_discovery']==r['floor_security_gap_discovery'];item['stored_float_gap_expression_consistent']=True
 fixed_checks.append(item)
direct=next(v for p,v in files.items() if p.endswith('/direct/depth_floor_checks.json'));direct_by={r['input']:r for r in direct['records']};overlay_checks=[]
for r in ov:
 g=files[r['input']];n,k=g['players'],len(g['topics']);assert direct_by[r['input']]['floor_sum']==r['floor_sum'];assert float(F(r['floor_sum']))-n*r['security_discovery']==r['floor_security_gap_discovery'];p=list(map(F,r['query_candidate']));assert len(p)==k and min(p)>=0
 overlay_checks.append(dict(input=r['input'],direct_floor_sum_same=True,stored_float_gap_expression_consistent=True,query_coordinates=len(p),query_sum=str(sum(p)),query_sum_minus_one=str(sum(p)-1),query_exactly_normalized=sum(p)==1,reported_float_gap_negative=r['floor_security_gap_discovery']<0))
after={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [fixed,overlay]};assert before==after
out=dict(status='pass',scope='only stored sums/gaps, history shapes, probability domains and approximate query normalization; no utility/IC/H/static-query/matrix/LP/SPE calls',report_sha256_before=before,report_sha256_after=after,fixed_records=len(fr),overlay_records=len(ov),fixed_reported_histories=sum(r['histories'] for r in fr),fixed_reported_comparisons=sum(r['comparisons'] for r in fr),overlay_query_coordinates=sum(x['query_coordinates'] for x in overlay_checks),fixed_checks=fixed_checks,overlay_checks=overlay_checks)
output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False))
