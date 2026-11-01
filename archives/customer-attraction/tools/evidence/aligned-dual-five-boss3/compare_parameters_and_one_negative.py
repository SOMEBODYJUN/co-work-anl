from pathlib import Path
from fractions import Fraction as F
import json,sys,hashlib,time
S=Path(__file__).resolve().parent;B=S.parent;R=B/'aligned_dual_runtime';C=R/'research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087/next_credible';sys.path.insert(0,str(C));tick=time.monotonic()
from offdiagonal_probe import rows as off
from crossmenu_probe import rows as cross
from menutax_probe import rows as tax
from alignedtax_probe import rows as align
exact=json.loads((S/'original/aligned_support_exact_dual.json').read_text());floating=json.loads((S/'original/reopt_aligned.json').read_text());negative=json.loads((S/'original/aligned_dual_exact_negative.json').read_text())
previous=B/'global_prices_runtime/research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087/next_credible/reopt_aligned.json'
assert hashlib.sha256(previous.read_bytes()).hexdigest()==hashlib.sha256((S/'original/reopt_aligned.json').read_bytes()).hexdigest()
lam={k:F(v)for k,v in exact['multipliers'].items()};flam={n:F(v)for n,v in zip(floating['names'],floating['dual_lambda'])if v>1e-9}
assert set(lam)==set(flam)and len(lam)==36 and all(x>0 for x in lam.values());beta=F(exact['beta']);assert 2-beta==F(exact['gap_below_two'])>0
parameters=[]
for n,ex,fl in [('beta',beta,F(floating['dual_beta']))]+[(n,lam[n],flam[n])for n in lam]:
 parameters.append({'parameter':n,'recovered_exact':str(ex),'previous_binary_float_as_rational':str(fl),'identical_exact_parameter':ex==fl,'exact_difference':str(ex-fl),'difference_float':float(ex-fl),'recovered_rounds_to_same_float':float(ex)==float(fl)})
cert=json.loads((R/'evidence/certificates/customer_attraction/five_player_indexed_bound.json').read_text())['primal'];atoms=cert['atoms'];assert len(atoms)==len(floating['point'])==len(exact['support_column_residuals'])==64
support=[i for i,x in enumerate(floating['point'])if x>1e-9];res=list(map(F,exact['support_column_residuals']));assert min(res)>=0 and all(res[i]==0 for i in support)
a=negative['atom'];fields=['bits','AB_hist','AE_hist','second_hist','menus_lh'];key=lambda a:json.dumps({k:a[k]for k in fields},sort_keys=True,separators=(',',':'))
assert key(a)not in {key(x)for x in atoms}
from itertools import product
cells=[list(product((0,1),repeat=3)),list(product((0,1),repeat=3)),list(product((0,1),repeat=4))];ds=[]
assert len(a['bits'])==10 and set(a['bits'])<={'0','1'}
for h,t in zip([a['AB_hist'],a['AE_hist'],a['second_hist']],cells):
 assert len(h)==len(t)and sum(h)==5 and all(type(v)is int and v>=0 for v in h);ds.append(sum(n*v[0]for n,v in zip(h,t)))
assert len(set(ds))==1
for ell,h in a['menus_lh']:assert 0<=h<=ds[0]and 0<=ell-h<=5-ds[0]
ns={};src=(R/'tests/audits/customer_attraction_five_indexed.py').read_text();exec(compile(src.split('from pathlib import Path')[0],'<original Fraction row definitions>','exec'),ns)
v=ns['evaluate'](list(map(int,a['bits'])),[a['AB_hist'],a['AE_hist'],a['second_hist']],a['menus_lh'],True)
for f in (off,cross,tax,align):v.update(f(a))
assert len(v)==2196 and set(v)==set(floating['names']);W=int(any(map(int,a['bits'][:5])));O=int(ds[0]>0)
rho=beta*W-O-sum((lam[n]*v[n]for n in lam),F());assert rho==F(negative['residual'])<0 and float(rho)==negative['float']
binary=F(floating['dual_beta'])*W-O-sum((flam[n]*v[n]for n in flam),F())
prior=B/'global_prices_stage/replay/all-reported-column-checks.json';prior_col=json.loads(prior.read_text())['reports'][0]['columns'][0];assert binary==F(prior_col['exact_binary_float_dual_rational_residual'])
full={'scope':'exact37-parameter comparison and one newly recovered rational-dual outside column; original recovery already checked64 columns, no1047 rescan','reopt_input_same_SHA_as_previous_batch':True,'active_threshold_current_recovery':1e-9,'active_threshold_previous_pricer':1e-10,'same_active_set_despite_thresholds':True,'parameter_count':len(parameters),'parameters_identically_equal':sum(x['identical_exact_parameter']for x in parameters),'parameters_different':sum(not x['identical_exact_parameter']for x in parameters),'maximum_abs_exact_parameter_difference_float':max(abs(x['difference_float'])for x in parameters),'parameters':parameters,'support_contract':{'columns':64,'floating_positive_columns':len(support),'positive_float_indices':support,'unknowns_beta_plus_lambda':37,'certificate_residual_zeros':sum(x==0 for x in res),'certificate_residual_positive':sum(x>0 for x in res),'all64_nonnegative':True,'all_float_positive_columns_tight':True,'no_exact_primal_recovery_claimed':True},'outside_column':{'valid_domain':True,'outside_original64':True,'W':W,'O':O,'d':ds[0],'new_rational_residual':str(rho),'previous_binary_float_residual':str(binary),'same_residual_exactly':rho==binary,'residual_difference':str(rho-binary),'recovered_parameters_used':True,'all2196_coefficients_sha256':hashlib.sha256('\n'.join(n+'='+str(v[n])for n in sorted(v)).encode()).hexdigest(),'active_coefficients':{n:str(v[n])for n in lam}},'execution':{'elapsed_seconds':time.monotonic()-tick,'source_recovery_extra_runs':0,'original_reopt_import_or_runs':0,'new_LP_calls':0,'new_negative_columns_checked':1,'whole1047_rescan':False,'exact_negative_producer_script_available_in_five_sources':False}}
(S/'parameter-and-one-column-comparison.json').write_text(json.dumps(full,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in full.items()if k not in ['parameters','outside_column']},ensure_ascii=False,indent=2));print('negative',rho)
