"""Parse all saved actions and reconcile finite shape/metadata only.

No original import, model build, MILP/LP, payoff/BI or verifier execution.
The single all-topic unit customer gives SPE and welfare analytically in text.
"""
import hashlib
import itertools
import json
import math
from fractions import Fraction as F
from pathlib import Path

HERE=Path(__file__).resolve().parent
path=HERE/'original/symmetric_AAAAB.json'
b=path.read_bytes();x=json.loads(b)
assert set(x)=={'scope','universal_result','parameters','milp','proof'}
assert x['universal_result'] is False
assert x['scope']=='finite candidate generation in count-dependent complete-history policies'
par=x['parameters'];m=par['m'];p=par['p'];assert (m,p,par['symmetry'],par['seconds'])==(5,7,True,55.0)
requested=tuple(map(int,par['path'].split(',')));J=tuple(map(int,par['portfolio'].split(',')))
assert requested==(0,0,0,0,1)and J==(2,3,4,5,6)
proof=x['proof'];assert set(proof)=={'instance','strategy','ratio','W','OPT','payoffs','exact_cone_objective','exact_SPE_verified'}
I=proof['instance'];assert I==dict(topics=[str(i)for i in range(p)],customers=[dict(topics=list(range(p)),multiplicity=1)],players=m)
strategy=proof['strategy'];assert set(strategy)=={'terminal_counts','actions'}
rows=strategy['actions'];expected={h for d in range(m)for h in itertools.product(range(p),repeat=d)}
assert len(rows)==len(expected)==2801
assert all(set(r)=={'history','action'}and all(type(a)is int and 0<=a<p for a in r['history'])and type(r['action'])is int and 0<=r['action']<p for r in rows)
actions={tuple(r['history']):r['action']for r in rows}
assert len(actions)==len(rows)and set(actions)==expected
counts={};sizes={}
for h,a in actions.items():
    q=tuple(h.count(i)for i in range(p))
    assert q not in counts or counts[q]==a
    counts[q]=a;sizes[q]=sizes.get(q,0)+1
for q,size in sizes.items():
    den=math.prod(math.factorial(a)for a in q)
    assert size==math.factorial(sum(q))//den
h=()
while len(h)<m:h+=(actions[h],)
assert h==requested
actual=tuple(h.count(i)for i in range(p));assert list(actual)==strategy['terminal_counts']==[4,1,0,0,0,0,0]
assert F(proof['ratio'])==F(proof['exact_cone_objective'])==1
assert proof['W']==proof['OPT']==1 and proof['payoffs']==['1/5']*m and proof['exact_SPE_verified']is True

# Closed combinatorial counts, not construction or evaluation of an MILP matrix.
N=math.comb(m+p-1,p)
n=4*(p-1)-1
assert N==330 and n==23 and len(counts)==N
variables=n+2*p*N;binaries=p*N;matrix_rows=p+3+N*(1+2*p*p+p*(p-1))
internal=math.comb(m+p-2,p)
last=math.comb(m+p-2,p-1)
positive_last=math.comb(m+p-3,p-1)
contain=2*(2*(p-1))+(p-2)*4*(p-2)
global_nnz=3*(p-1)+n+(contain+p)+2
internal_nnz=internal*(p+3*(2*p*p+p*(p-1)))
last_nnz=last*p+2*(2*last*p*p+contain*(p*positive_last+(last-positive_last)))+last*(p-1)*(2*p+contain)
nnz=global_nnz+internal_nnz+last_nnz
meta=x['milp'];assert (meta['variables'],meta['binaries'],meta['rows'],meta['nnz'],meta['customer_orbits'])==(variables,binaries,matrix_rows,nnz,n)==(4643,2310,46540,444996,23)
assert meta['status']==1 and meta['exact_reconstruction']is True
assert 'Time limit reached'in meta['message']
out=dict(kind='complete saved JSON/table and closed combinatorial shape check, not a new SPE verifier or solver run',source=dict(path=str(path),size=len(b),sha256=hashlib.sha256(b).hexdigest()),all_top_and_nested_semantic_fields_read=True,all_2801_actions_read=True,exact_ordered_history_keyset=True,no_duplicates=True,all_labels_legal=True,depth_counts=[dict(depth=d,histories=p**d)for d in range(m)],count_policy_consistent=True,count_states=N,count_policy=[dict(counts=list(q),action=counts[q],ordered_history_multiplicity=sizes[q])for q in sorted(counts,key=lambda q:(sum(q),q))],actual_ordered_path=list(h),actual_counts=list(actual),requested_path_matches=True,all_seven_coverage_columns_identical_single_unit_customer=True,analytic_payoff_every_player_every_terminal='1/5',analytic_W_OPT_ratio=[1,1,1],nonself_comparisons_covered_by_analytic_tie_proof=(p-1)*len(expected),including_self_comparisons_covered_by_analytic_tie_proof=p*len(expected),original_numeric_incumbent_vector_saved=False,post_reconstruction_point_not_original_milp_vector=True,metadata_geometry=dict(customer_orbits=n,count_nodes=N,variables=variables,binaries=binaries,rows=matrix_rows,nnz=nnz,nnz_parts=dict(global_rows=global_nnz,nonlast_rows=internal_nnz,last_rows=last_nnz)),original_milp=meta,original_entry_or_import_runs=0,LP_MILP_BI_payoff_verifier_runs=0,extra_point_export_or_recovery=False)
(HERE/'point-review.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(status='passed',ordered_nodes=2801,count_states=330,actual_path=list(h),rows=matrix_rows,nnz=nnz,trivial_one_customer_point=True,original_or_solver_runs=0)))
