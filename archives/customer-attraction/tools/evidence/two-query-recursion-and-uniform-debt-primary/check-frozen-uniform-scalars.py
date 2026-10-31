#!/usr/bin/env python3
"""Checks only the given1617 report scalars. Never certifies absent791 input or SPE."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
E=Path(__file__).resolve().parent;S=E.parents[4];W=S/'cleanup/workspaces/Boss4/r3-two-query-recursion-and-uniform-debt-primary';gate=json.loads((W/'primary-authorization-check.json').read_text());assert gate['status']=='pass'
out=E/'frozen-uniform-scalar-check.json';assert not out.exists(),'single report-only scalar check; do not repeat'
p=E/'original/research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round2/mixed/uniform_debt_audit.json';r=json.loads(p.read_text());query=list(map(F,r['query']));assert len(query)==7 and all(v>=0 for v in query) and sum(query)==1
rows=[];sums={k:F() for k in ['psi','C','D','actual_utility','root_slack','free_column_gain','covariance','insertion_tax']}
for row in r['positions']:
 x={k:F(row[k]) for k in sums};assert x['root_slack']==x['actual_utility']-x['D']>=0 and x['free_column_gain']==x['C']-x['psi']>=0
 cov_res=x['D']-x['C']-x['covariance']-x['insertion_tax'];debt_res=x['psi']-x['actual_utility']-x['C']+x['D']+x['root_slack']+x['free_column_gain'];assert cov_res==debt_res==F(row['identity_residual'])==0
 if row['index']>=2:assert x['psi']<=x['actual_utility']
 for k in sums:sums[k]+=x[k]
 rows.append({'index':row['index'],'covariance_identity_residual':str(cov_res),'debt_identity_residual':str(debt_res),'psi_minus_reported_utility':str(x['psi']-x['actual_utility']),'reported_last_two_scalar_bound_checked':row['index']>=2})
Welfare=F(r['welfare']);assert sums['actual_utility']==Welfare==597
left=sums['psi']-Welfare;right=sums['C']-sums['D']-sums['root_slack']-sums['free_column_gain'];assert left==right==F(-26407,84)
res={'status':'pass-report-internal-scalars-only','entry_calls':1,'input_path':str(p.relative_to(S)),'input_size':p.stat().st_size,'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source_program3862_calls':0,'source_functions_or_solver_calls':0,'full_SPE_checks':0,'791_unit_model_reconstructed':False,'missing48798_input_replaced_or_rebuilt':False,'report_query_sum':str(sum(query)),'position_results':rows,'report_scalar_sums':{k:str(v) for k,v in sums.items()},'report_sum_psi_minus_report_W':str(left),'aggregate_scalar_residual':str(left-right),'not_certified':['true791 customer model or57-action map','399 completeSPE comparisons','underlyingK/minimizing columns or per-client covariance/tax source','generaluniformtimeU']}
out.write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':res['status'],'source_program3862_calls':0,'full_SPE_checks':0,'report_sum_psi_minus_report_W':str(left)}))
