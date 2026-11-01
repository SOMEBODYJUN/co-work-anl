#!/usr/bin/env python3
"""Bounded report arithmetic/count formulas and byte binding only.
No original producer imports/runs, no full-tree or sparse-subset re-enumeration.
"""
import pathlib,json,hashlib
from fractions import Fraction as F
E=pathlib.Path(__file__).resolve().parent
rows=json.loads((E/'primary-inventory.json').read_text());P={r['id']:json.loads((E/'original'/r['path']).read_text()) for r in rows if r['path'].endswith('.json')}
a=P['3564da928d1da0e50943'];b=P['b4e64f98e7453d4d228a'];c=P['1fcf4d32e4c24b455d9f'];d=P['a8f608020c5f7b69f334']
checks=[]
for i,role in [('3564da928d1da0e50943','parent-aggregate'),('b4e64f98e7453d4d228a','parent-padding')]:
 r=next(r for r in rows if r['id']==i);stdout=E/'historical-runs'/role/'stdout.txt';event=json.loads((stdout.parent/'execution.json').read_text());assert event['exit_code']==0 and event['stdout_sha256']==hashlib.sha256(stdout.read_bytes()).hexdigest()==r['sha256'];assert stdout.read_bytes()==(E/'original'/r['path']).read_bytes();checks.append(dict(id=i,old_execution_reused=True,stdout_byte_identical=True))
assert a['sha256']==b['source_sha256']=='14f8b29548715323a8ee6eac0fabc3efb7e8ea0537fb34cd866c66ed131c855d'
assert sum(F(r['D']) for r in a['rows'])==F(a['D'])==F(63,2)
assert sum(F(r['vacancy']) for r in a['rows'])==F(a['vacancy'])==F(65,2)
assert sum(F(r['pure_extra']) for r in a['rows'])==F(a['pure_extra'])==F(41,2)
e=F(a['epsilon']);D,G=map(F,a['direct_D_G']);assert e==F(1,24) and D-G==-F(1,48)==F(a['gap']) and D==e*F(a['D']) and G==e*(1-e)*F(a['vacancy'])+e*e*F(a['pure_extra'])
assert sum(map(F,a['payoffs']))==F(a['W'])==32 and a['OPT']==34 and a['histories']==57 and a['nonself_deviations']==342
K,J=b['K'],b['private_proxy_customers'];assert K==67 and J==1 and b['customers']==K*34+J==2279 and F(b['W'])==K*32 and b['OPT']==K*34==2278
coeff=list(map(F,b['quadratic_coefficients']));assert coeff==[F(3,2),F(-70),F(1611,2)] and coeff[1]**2-4*coeff[0]*coeff[2]==b['discriminant']==67
assert F(b['gap'])==F(b['D'])-F(b['G'])==K*(12*e*e-e)+F(3*J,2)*(1-e)**2==-F(7,384)
row_count=3*sum((2**m)*sum(2**(m-j) for j in range(1,m)) for m in range(1,9));family_count=9*sum(2**m for m in range(1,9));spe_count=4*2*sum(2**(2*q)-1 for q in range(1,7))
assert row_count==c['all_sparse_subsets_row_cases']==259080 and family_count==c['nonuniform_sparse_family_budget_cases']==4590 and c['complete_spe_family_cases']==99-2+1==98
assert d['spe_comparisons']==spe_count==43632 and d['fraction_budget_cases']==79*4==316 and d['history_dependent_policy_variants']==4
# Check q=2 endpoint, q=3 current six-player special case, and one larger identity.
identities=[]
for q in [2,3,10]:
 h=sum((F(1,j) for j in range(1,q)),F(0));clock=sum((F(1,j*(j+1)*(j+2)) for j in range(1,q)),F(0));reset=h/6;premium=sum((F(1,j)*(F(1,6)-F(1,(j+1)*(j+2))) for j in range(1,q)),F(0));assert clock==F(1,4)-F(1,2*q*(q+1)) and reset==clock+premium
 identities.append(dict(q=q,players=2*q,W=2,OPT=2,reset=str(reset),clock=str(clock),premium=str(premium)))
# Oversaturated history: q=3, h=AAAA. Obey B then B -> A^4 B^2, current payoff 1/2;
# deviate A then B -> A^5 B, current payoff 1/5; not 1/q.
assert F(1,6-4)==F(1,2)>F(1,5) and F(1,2)!=F(1,3)
out=dict(status='PASS',scope=__doc__,old_extra_slot_reuse=checks,old_sparse_reports='finite historical declarations; actual producer stdout/event not located, no execution claim',count_formulas=dict(sparse_rows=row_count,nonuniform_families=family_count,SPE_action_comparisons=spe_count,budget_cases=316),bounded_identity_rows=identities,offpath_oversaturated_witness=dict(q=3,history='AAAA',obey_payoff='1/2',deviate_payoff='1/5',wrong_constant='1/3'),original_producer_runs_here=0,helper_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest())
pathlib.Path('result.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print('PASS: old extra reports byte-identical; 4 finite count formulas; bounded rent identities; oversaturated offpath witness; original runs 0')
