#!/usr/bin/env python3
"""One standard-library definition audit of the fixed92/96 domain; no LP/recovery."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
from collections import Counter
import ast,hashlib,json,platform,time
P=Path(__file__).resolve().parent;start=time.perf_counter()
old=json.loads((P/'related/enhanced_2396_exact_obstruction.json').read_text())['atom_masses']
cells=json.loads((P/'related/root_menu_completion_exact.json').read_text())['positive_refinements']
run=json.loads((P/'original/couple_root_refinement.json').read_text());cert=json.loads((P/'original/root_coupling_obstruction_exact.json').read_text())
types=list(product((0,1),repeat=3));d=[sum(n*t for n,(t,x,y) in zip(a['AB_hist'],types)) for a in old]
assert len(old)==38 and len(cells)==92 and set(d)=={1}
assert len({(r['atom'],r['t'],tuple(r['replies'])) for r in cells})==92
# Independently enumerate multisets of the full five indexed root paths.
columns=[];inventory=[]
for a in range(38):
 pats={t:sorted(tuple(r['replies']) for r in cells if r['atom']==a and r['t']==t) for t in (0,1)}
 assert all(len(v)==4 and all(x in (0,1) for x in v) for vs in pats.values() for v in vs)
 local=[]
 for zero in combinations_with_replacement(pats[0],5-d[a]):
  for one in combinations_with_replacement(pats[1],d[a]):
   hist=[(t,v,n) for (t,v),n in sorted(Counter([(0,v) for v in zero]+[(1,v) for v in one]).items())]
   local.append((a,hist))
 columns+=local;inventory.append({'atom':a,'d':d[a],'t0_patterns':[list(v) for v in pats[0]],'t1_patterns':[list(v) for v in pats[1]],'histograms':len(local)})
key=lambda a,h:(a,tuple((t,tuple(v),n) for t,v,n in h))
newkeys={key(a,h) for a,h in columns};savedkeys={key(a,h) for a,h in run['column_specs']}
assert len(newkeys)==len(columns)==len(savedkeys)==len(run['column_specs'])==96 and newkeys==savedkeys
# Read only the original pure coefficient function, not its top level or solver.
source=ast.parse((P/'original/couple_root_refinement.py').read_text())
fn=next(x for x in source.body if isinstance(x,ast.FunctionDef) and x.name=='offrow')
space={'F':F};exec(compile(ast.Module(body=[fn],type_ignores=[]),'original-offrow-only','exec'),space)
lam=list(map(F,cert['lambda']));nu=list(map(F,cert['nu']))
assert len(lam)==16 and len(nu)==92 and sum(lam)==1 and min(lam)>=0
assert lam==[F(0)]*15+[F(1)]
assert lam==[F(x).limit_denominator(100) for x in run['dual_rows']]
assert nu==[F(x).limit_denominator(100) for x in run['dual_equalities']]
coeff=[];records=[]
for ix,(a,h) in enumerate(run['column_specs']):
 indexed=[(t,tuple(v)) for t,v,n in h for _ in range(n)]
 assert len(indexed)==5 and sum(t for t,v in indexed)==d[a]
 rows=[]
 for j in range(4):
  for k in range(4):
   # Literal customer contribution from five fixed true histories, with self index omitted.
   z=F(0)
   for i,(t,v) in enumerate(indexed):
    total=t+sum(v);pay=F(v[j],total) if v[j] else F(0)
    past=t+sum(v[:j]);remaining=4-j
    other=sum(vv[k] for ell,(tt,vv) in enumerate(indexed) if ell!=i)
    z+=(4*pay-F(other,past+remaining))/5
   assert z==space['offrow'](h,j,k)
   rows.append(z)
 coeff.append({'column':ix,'atom':a,'row_order':'4*j+k, j,k=0..3','coefficients':list(map(str,rows))})
 erow=[sum(n for t,v,n in h if t==r['t'] and tuple(v)==tuple(r['replies']))/F(5) if a==r['atom'] else F(0) for r in cells]
 residual=sum(x*y for x,y in zip(lam,rows))+sum(x*y for x,y in zip(nu,erow))
 assert residual<=0
 records.append({'column':ix,'dual_column_residual':str(residual),'dual_column_slack':str(-residual)})
budget=sum(x*F(r['mass']) for x,r in zip(nu,cells));assert budget>0 and str(budget)==cert['positive_impossibility_budget']
slacks=[F(x['dual_column_slack']) for x in records];assert str(min(slacks))==cert['minimum_column_dual_slack']
nonzero=[{'cell_index_zero_based':i,'atom':r['atom'],'t':r['t'],'replies':r['replies'],'nu':str(x),'mass':r['mass']} for i,(x,r) in enumerate(zip(nu,cells)) if x]
(P/'definition-row-coefficients.json').write_text(json.dumps(coeff,ensure_ascii=False,indent=2)+'\n')
report={'kind':'new exact standard-library definition audit; 0 original top levels, LP, BI, or recovery',
 'old_atoms':38,'all_d':1,'fixed_positive_cells':92,'complete_supported_histograms':96,
 'inventory_by_atom':inventory,'all_96_saved_columns_exhaustive_and_unique':True,
 'literal_fixed_index_vs_original_offrow_coefficients':1536,'all_coefficients_equal':True,
 'lambda_nonzero':[{'row':15,'j':3,'k':3,'weight':'1'}],
 'nu_nonzero_count':len(nonzero),'nu_nonzero':nonzero,'column_certificate':records,
 'all_column_residuals_nonpositive':True,'zero_column_slacks':sum(x==0 for x in slacks),
 'strict_column_slacks':sum(x>0 for x in slacks),'minimum_column_slack':str(min(slacks)),'maximum_column_slack':str(max(slacks)),
 'impossibility_budget':str(budget),'impossibility_budget_float':float(budget),
 'float_margin_in_original_only':run['margin'],'float_primal_recovered':False,
 'original_top_level_runs':0,'LP_calls':0,'BI_calls':0,'random_samples':0,'root92_recovery_runs':0,'full53_recovery_runs':0,'full1326_audits':0}
(P/'fixed92-definition-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
event={'kind':'one new definition/finite domain audit; no solver or source top-level',
 'command':'python audit_fixed92_from_definition.py > definition-audit.stdout 2> definition-audit.stderr','cwd':str(P),
 'python':platform.python_version(),'assertions_enabled':__debug__,'wall_seconds':time.perf_counter()-start,
 'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'new_definition_audit_runs':1,
 'original_top_level_runs':0,'LP_calls':0,'BI_calls':0,'random_samples':0,
 'source_function_extracted_without_top_level':'couple_root_refinement.py:offrow; 1536 exact coefficient comparisons',
 'inputs':[{'file':str(f.relative_to(P)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in [P/'related/enhanced_2396_exact_obstruction.json',P/'related/root_menu_completion_exact.json',P/'original/couple_root_refinement.py',P/'original/couple_root_refinement.json',P/'original/root_coupling_obstruction_exact.json']]}
(P/'definition-audit-event.json').write_text(json.dumps(event,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ('complete_supported_histograms','literal_fixed_index_vs_original_offrow_coefficients','nu_nonzero_count','zero_column_slacks','strict_column_slacks','maximum_column_slack','impossibility_budget_float')},ensure_ascii=False))
