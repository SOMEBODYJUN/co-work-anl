"""Independent exact audit of the single new fixed-policy tax LP capture.

No original import/helper, NumPy, SciPy, LP or canonical solver. Reconstruct
ordered-history coefficients, then verify primal/dual rational certificates.
The known 61-client seed's SPE comparisons are not rerun.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations
from collections import Counter
import gzip,hashlib,json,time

HERE=Path(__file__).resolve().parent
CAPTURE=HERE/'replay/capture.json.gz'
OUTPUT=HERE/'exact-audit.json'
assert not OUTPUT.exists(),'Refuse duplicate independent entry'
tick=time.perf_counter()
raw=gzip.decompress(CAPTURE.read_bytes());record=json.loads(raw)
globals_=record['source_globals'];n=globals_['n'];k=globals_['k'];masks=globals_['masks']
assert (n,k,masks)==(4,6,list(range(1,64)))
history_domain=[h for depth in range(n) for h in product(range(k),repeat=depth)]
sigma={tuple(row['history']):row['action'] for row in globals_['sigma']}
assert len(sigma)==259 and list(sigma)==history_domain
assert all(type(a) is int and 0<=a<6 for a in sigma.values())
assert {int(m):v for m,v in globals_['seed'].items()}=={1:12,2:8,4:4,8:8,17:6,33:6,20:3,36:3,49:6,50:2,52:1,56:2}
# Identity with the old published closed rule, not another seed-game BR audit.
for h,a in sigma.items():
    expected=0 if len(h)<3 or h.count(0)<=1 else 4 if 5 in h else 5
    assert a==expected

def finish(history):
    tail=list(history)
    while len(tail)<n:tail.append(sigma[tuple(tail)])
    assert len(tail)==n
    return tuple(tail)

def unit_share(mask,action,terminal):
    if not mask&(1<<action):return F(0)
    covered=[a for a in terminal if mask&(1<<a)]
    assert covered
    return F(1,len(covered))

gamma=[];labels=[]
for h in history_domain:
    chosen=sigma[h];actual=finish(h)
    own=[unit_share(mask,chosen,actual) for mask in masks]
    for a in range(k):
        alternative=finish(h+(a,))
        gamma.append([v-unit_share(mask,a,alternative) for mask,v in zip(masks,own)])
        labels.append((h,a))
assert len(gamma)==1554
assert sum(not any(row) for row in gamma)==259
source_gamma=[[F(x) for x in row] for row in record['optimize_return']['gamma']]
assert gamma==source_gamma
root=finish(())
assert root==tuple(record['optimize_return']['root'])==(0,0,0,5)
shared=record['shared_LP_constraints']
assert shared['b_ub']==[0.]*1554 and shared['A_eq']==[[1.]*63] and shared['b_eq']==[1]
assert shared['bounds']==[0,None] and shared['method']=='highs'
max_error=0.
for exact_row,float_row in zip(gamma,shared['A_ub'],strict=True):
    for exact,floating in zip(exact_row,float_row,strict=True):
        max_error=max(max_error,abs(float(-exact)-floating))
        assert abs(float(-exact)-floating)<=1e-15
int_gamma=[]
for row in gamma:
    scaled=[12*x for x in row];assert all(v.denominator==1 for v in scaled)
    int_gamma.append([int(v) for v in scaled])
gamma_digest=hashlib.sha256(json.dumps(int_gamma,separators=(',',':')).encode()).hexdigest()

root_loads=[sum(bool(mask&(1<<a)) for a in root) for mask in masks]
portfolios=list(combinations(range(k),n));assert len(portfolios)==15
exact_records=[];objective_coefficients=0;primal_ic_evaluations=0;dual_coordinate_evaluations=0
def rational(x):return F(float(x)).limit_denominator(10**6)

for original,portfolio in zip(record['LP_records'],portfolios,strict=True):
    assert original['portfolio']==list(portfolio)
    costs=[F(int(c>0))+F(c,c+1)-int(any(mask&(1<<a) for a in portfolio)) for mask,c in zip(masks,root_loads)]
    for exact,floating in zip(costs,original['c'],strict=True):
        assert (60*exact).denominator==1
        delta=abs(float(exact)-floating);max_error=max(max_error,delta);assert delta<=1e-15
        objective_coefficients+=1
    result=original['result'];assert result['success'] and result['status']==0
    primal=[rational(x) for x in result['x']]
    assert len(primal)==63 and min(primal)>=0 and sum(primal)==1
    support=[(j,x) for j,x in enumerate(primal) if x]
    slacks=[sum(row[j]*x for j,x in support) for row in gamma]
    assert min(slacks)>=0;primal_ic_evaluations+=len(slacks)
    value=sum(c*x for c,x in zip(costs,primal))
    # SciPy marginals y <= 0 for -Gamma x <= 0; lambda = -y >= 0.
    dual=[-rational(x) for x in result['inequality_marginals']]
    assert len(dual)==1554 and min(dual)>=0
    nu=rational(result['equality_marginals'][0])
    active_dual=[(i,x) for i,x in enumerate(dual) if x]
    reduced=[costs[j]-nu-sum(lam*gamma[i][j] for i,lam in active_dual) for j in range(63)]
    assert min(reduced)>=0 and value==nu
    for r,floating in zip(reduced,result['lower_marginals'],strict=True):
        delta=abs(float(r)-floating);max_error=max(max_error,delta);assert delta<=1e-14
    assert sum(lam*slacks[i] for i,lam in active_dual)==0
    assert sum(r*x for r,x in zip(reduced,primal))==0
    delta=abs(float(value)-result['fun']);max_error=max(max_error,delta);assert delta<=1e-14
    dual_coordinate_evaluations+=len(reduced)
    exact_records.append({'portfolio':list(portfolio),'floating_fun':result['fun'],'exact_optimum':str(value),
      'primal_weights':{str(j+1):str(x) for j,x in support},'primal_gamma_minimum':str(min(slacks)),
      'primal_gamma_zero_count':sum(x==0 for x in slacks),'primal_gamma_positive_count':sum(x>0 for x in slacks),
      'dual_equality':str(nu),'dual_nonnegative_multipliers':[{'row':i,'history':list(labels[i][0]),'alternative':labels[i][1],'value':str(lam)} for i,lam in active_dual],
      'dual_coordinate_remainders':[str(x) for x in reduced],
      'dual_identity':'cost = nu * ones + Gamma^T * lambda + nonnegative_remainder',
      'matching_primal_dual':True})

main=record['main_reconstruction'];integer_weights={int(m):v for m,v in main['weights'].items()}
assert integer_weights=={2:1,4:1,8:1,49:4}
integer_vector=[integer_weights.get(mask,0) for mask in masks]
actual_gamma=[sum(row[j]*v for j,v in enumerate(integer_vector) if v) for row in gamma]
assert [str(x) for x in actual_gamma]==main['all_gamma_values'] and min(actual_gamma)==0
W=sum(int(c>0)*v for c,v in zip(root_loads,integer_vector))
tax=sum(F(c,c+1)*v for c,v in zip(root_loads,integer_vector))
coverages=[sum(v for mask,v in integer_weights.items() if any(mask&(1<<a) for a in cc)) for cc in portfolios]
OPT=max(coverages)
assert (sum(integer_vector),W,tax,OPT,W+tax-OPT)==(7,4,F(16,5),7,F(1,5))
assert min(F(x['exact_optimum']) for x in exact_records)==F(1,35)
assert Counter(x['exact_optimum'] for x in exact_records)==Counter({'1/35':3,'3/32':9,'91/1030':3})

out={'status':'PASS','scope':'Independent coefficients and exact primal/dual certificates for one new fixed policy; old 61-client SPE audit not repeated.',
 'original_imports':0,'original_helpers':0,'LP_calls':0,'canonical_solver_calls':0,'old_seed_SPE_payoff_evaluations':0,
 'captured_source_sha256':'8f72ad4dc8464ef17883bce8f273faefe55152dd31b35aeee136c8bcf3579e21',
 'capture_sha256':hashlib.sha256(raw).hexdigest(),'capture_gzip_sha256':hashlib.sha256(CAPTURE.read_bytes()).hexdigest(),
 'policy_identity_nodes':259,'decision_nodes':259,'own_action_zero_rows':259,'nonself_rows':1295,'gamma_rows':1554,'type_columns':63,
 'gamma_coefficients_reconstructed':1554*63,'integer_Gamma_times_12_SHA256':gamma_digest,
 'objective_coefficients_reconstructed':objective_coefficients,'all_comparison_supports':15,
 'exact_primal_ic_evaluations':primal_ic_evaluations,'exact_dual_coordinate_evaluations':dual_coordinate_evaluations,
 'all_15_primal_dual_certificates_verified':True,'exact_optimum_counts':dict(Counter(x['exact_optimum'] for x in exact_records)),
 'minimum_mass_normalized_slack':'1/35','fixed_policy_universal_statement':'For this same full policy and every nonnegative customer vector satisfying Gamma x >= 0, W + tau - OPT_4 >= sum(x)/35; no assertion about other policies.',
 'main_integer_output':{'weights':integer_weights,'total_unit_customers':7,'root':list(root),'minimum_gamma':'0','W':W,'terminal_tax':str(tax),'OPT_4':OPT,'W_plus_tax_minus_OPT':str(W+tax-OPT),'normalized_by_customer_mass':'1/35','normalized_by_W':'1/20','static_portfolio_coverages':coverages},
 'maximum_absolute_float_difference':max_error,'records':exact_records,'elapsed_seconds':time.perf_counter()-tick}
OUTPUT.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('records','main_integer_output')},ensure_ascii=False))
