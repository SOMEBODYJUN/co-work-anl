"""New arithmetic audit/rational recovery of the frozen 2408-row float point.

Uses the archived original coefficient functions; no independent old-2396
coefficient derivation or full-domain pricing is claimed. Never overwrites inputs.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse,json,sys,runpy,time,hashlib,platform
import numpy as np
p=argparse.ArgumentParser();p.add_argument('--runtime',type=Path,required=True);p.add_argument('--frozen',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
assert not a.output.exists();a.output.mkdir(parents=True)
t0=time.perf_counter()
rpath=Path('research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087')
entry=a.runtime/rpath/'round3_indexed/reopt_common_pivot.py'
sys.path[:0]=[str(entry.parent),str(a.runtime/rpath/'next_credible')]
ns=runpy.run_path(str(entry),run_name='coefficient_definitions_only')
frozen=json.loads(a.frozen.read_text());atoms=frozen['atoms'];cols=[ns['allrows'](atom) for atom in atoms]
names=list(cols[0]);assert names==frozen['names'] and len(names)==2408
assert all(list(c)==names for c in cols)
G=[[c[n] for c in cols] for n in names]
w=[int(any(map(int,at['bits'][:5]))) for at in atoms];o=[int(any(at['AB_hist'][4:])) for at in atoms]
point=np.array(frozen['point']);mat=np.array(G,dtype=float);lamb=np.array(frozen['dual_lambda']);beta=frozen['dual_beta']
primal_slack=mat@point;dual_slack=beta*np.array(w)-np.array(o)-lamb@mat
numeric={'normalization_error':float(np.array(w)@point-1),'recomputed_objective':float(np.array(o)@point),'minimum_primal_slack':float(min(primal_slack)),'negative_primal_rows_lt_minus_1e-10':[n for n,s in zip(names,primal_slack) if s< -1e-10],'minimum_dual_slack':float(min(dual_slack)),'max_lambda_times_primal_slack':float(max(abs(lamb*primal_slack))),'max_point_times_dual_slack':float(max(abs(point*dual_slack))),'duality_gap':float(beta-np.array(o)@point),'positive_point_count_gt_1e-8':int(sum(point>1e-8)),'positive_lambda_count_gt_1e-10':int(sum(lamb>1e-10))}
S=[i for i,x in enumerate(point) if x>1e-8]
active=[(n,row) for n,row,sl in zip(names,G,primal_slack) if abs(sl)<1e-7]
basis={};selected=[]
for title,row,rhs in [('W=1',w,F(1))]+[(n,r,F(0)) for n,r in active]:
 v=[F(row[i]) for i in S]+[rhs]
 for pivot,b in sorted(basis.items()):
  q=v[pivot]
  if q:v=[x-q*y for x,y in zip(v,b)]
 pivot=next((i for i,q in enumerate(v[:-1]) if q),None)
 if pivot is None:
  assert v[-1]==0;continue
 q=v[pivot];basis[pivot]=[x/q for x in v];selected.append(title)
 if len(basis)==len(S):break
assert len(basis)==len(S)
z=[F(0)]*len(S)
for pivot,b in sorted(basis.items(),reverse=True):z[pivot]=b[-1]-sum(b[i]*z[i] for i in range(pivot+1,len(S)))
exact=[F(0)]*len(atoms)
for i,v in zip(S,z):exact[i]=v
assert min(exact)>=0 and sum(v*b for v,b in zip(exact,w))==1
slacks={n:sum(c[n]*v for c,v in zip(cols,exact)) for n in names}
assert min(slacks.values())>=0
objective=sum(v*b for v,b in zip(exact,o));assert objective>2
record={'event_kind':'new-2026-11-02-rational-recovery-not-a-frozen-source-report','method':'support and near-tight rows from frozen float; Fraction elimination; all 2408 original coefficient rows checked exactly','frozen_input_sha256':hashlib.sha256(a.frozen.read_bytes()).hexdigest(),'rows':len(names),'candidate_atoms':len(atoms),'positive_atoms':sum(v>0 for v in exact),'support_indices':S,'near_tight_row_count':len(active),'selected_equations':selected,'basis_rank':len(basis),'normalization':'1','point':[str(v) for v in exact],'objective':str(objective),'objective_float':float(objective),'gap_above_two':str(objective-2),'all_slacks':{n:str(v) for n,v in slacks.items()},'zero_slacks':sum(v==0 for v in slacks.values()),'minimum_slack':str(min(slacks.values())),'common_pivot_slacks':{n:str(v) for n,v in slacks.items() if n.startswith('common-pivot:')},'all_rows_verified_exactly':True,'exact_dual_recovered':False,'full_domain_pricing_performed':False,'complete_SPE_provided':False,'numeric_diagnostics_of_frozen_point':numeric}
(a.output/'new_exact_2408_point.json').write_text(json.dumps(record,indent=2)+'\n')
script=Path(__file__)
event={'event':'new arithmetic audit and exact primal recovery','argv':sys.argv,'python':platform.python_version(),'numpy':np.__version__,'elapsed_seconds':time.perf_counter()-t0,'entry_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256((a.output/'new_exact_2408_point.json').read_bytes()).hexdigest(),'original_optimizer_calls':0,'coefficient_function_evaluations':65,'independent_coefficient_rederivation':False,'input_sha256':hashlib.sha256(a.frozen.read_bytes()).hexdigest()}
(a.output/'event.json').write_text(json.dumps(event,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items() if k not in ('point','all_slacks','selected_equations','support_indices')},indent=2))
