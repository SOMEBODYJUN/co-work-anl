from pathlib import Path
from fractions import Fraction as F
from itertools import product
from datetime import datetime,timezone
import importlib.util,json,sys,hashlib,time,platform
S=Path(__file__).resolve().parent;R=S.parent/'global_prices_runtime';G=R/'research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087/next_global';C=G.parent/'next_credible'
sys.path.insert(0,str(G));tick=time.monotonic();start=datetime.now(timezone.utc).isoformat()
import price_aligned as P
LABELS='ABCDEUVWXY';TYPES=list(product((0,1),repeat=3));QUADS=list(product((0,1),repeat=4))
def atomkey(a):return json.dumps(a,sort_keys=True,separators=(',',':'))
def domain(a):
 assert set(a)=={'bits','AB_hist','AE_hist','second_hist','menus_lh'}
 assert len(a['bits'])==10 and set(a['bits'])<={'0','1'}
 ds=[]
 for name,cells in [('AB_hist',TYPES),('AE_hist',TYPES),('second_hist',QUADS)]:
  h=a[name];assert len(h)==len(cells)and all(type(x)is int and x>=0 for x in h)and sum(h)==5;ds.append(sum(n*t[0]for n,t in zip(h,cells)))
 assert len(set(ds))==1;d=ds[0];assert len(a['menus_lh'])==3
 for lh in a['menus_lh']:
  assert len(lh)==2 and all(type(x)is int for x in lh);ell,h=lh;assert 0<=h<=d and 0<=ell-h<=5-d
 return int(any(map(int,a['bits'][:5]))),int(d>0),d
reports=[]
for reportname,dualname in [('price_aligned.json','reopt_aligned.json'),('block_price.json','reopt_added.json')]:
 report=json.loads((S/'original'/reportname).read_text());dual=json.loads((C/dualname).read_text());assert len(dual['names'])==len(dual['dual_lambda'])==2196 and len(set(dual['names']))==2196
 active={n:F(v)for n,v in zip(dual['names'],dual['dual_lambda'])if v>1e-10};assert report['beta']==dual['dual_beta']and len(active)==report['active_rows']
 if reportname=='price_aligned.json':P.Price(dual)
 cols=report['negative_columns'];keys=set();results=[];rowset=None;maxerr=0.;recomputed_min=None
 for i,col in enumerate(cols):
  a=col['atom'];key=atomkey(a);assert key not in keys;keys.add(key);W,O,d=domain(a)
  if reportname=='price_aligned.json':assert a['bits']==format(i,'010b')and (col['W'],col['O'],col['d'])==(W,O,d)
  values=P.ns['evaluate'](list(map(int,a['bits'])),[a['AB_hist'],a['AE_hist'],a['second_hist']],a['menus_lh'],True)
  for f in (P.off_rows,P.cross_rows,P.tax_rows,P.align_rows):values.update(f(a))
  assert set(values)==set(dual['names'])
  rho=F(dual['dual_beta'])*W-O-sum((v*values[n]for n,v in active.items()),F())
  assert rho<0 and col['residual']<-1e-8
  error=abs(float(rho)-col['residual']);assert error<1e-8,(reportname,i,error);maxerr=max(maxerr,error)
  payload='\n'.join(n+'='+str(values[n])for n in sorted(values)).encode();digest=hashlib.sha256(payload).hexdigest()
  results.append({'index':i,'atom_sha256':hashlib.sha256(key.encode()).hexdigest(),'W':W,'O':O,'d':d,'stored_float_residual':col['residual'],'exact_binary_float_dual_rational_residual':str(rho),'all_2196_coefficient_sha256':digest,'float_difference':error})
  if recomputed_min is None or rho<recomputed_min:recomputed_min=rho
  if i%100==0:print(json.dumps({'report':reportname,'checked':i+1,'elapsed_seconds':time.monotonic()-tick}),flush=True)
 assert atomkey(report['best']['atom'])in keys
 bestindex=next(i for i,c in enumerate(cols)if atomkey(c['atom'])==atomkey(report['best']['atom']))
 assert report['best']['residual']==min(c['residual']for c in cols)
 if reportname=='block_price.json':assert report['best']['violation']==-report['best']['residual']and 0<=report['best']['restart']<report['restarts']and report['best']['passes']>=1
 else:assert (report['best']['W'],report['best']['O'],report['best']['d'])==domain(report['best']['atom'])
 reports.append({'report':reportname,'dual_input':dualname,'dual_input_sha256':hashlib.sha256((C/dualname).read_bytes()).hexdigest(),'row_count':2196,'dual_source_columns':len(dual['point']),'active_rows':len(active),'beta_float':dual['dual_beta'],'all_dual_lambda_nonnegative':all(x>=0 for x in dual['dual_lambda']),'discarded_nonzero_lambda_count':sum(v!=0 and v<=1e-10 for v in dual['dual_lambda']),'negative_columns':len(cols),'all_unique_atom_keys':True,'minimum_exact_residual':str(recomputed_min),'maximum_float_replay_error':maxerr,'best_index_in_columns':bestindex,'W_O_d_counts':{str(k):sum((x['W'],x['O'],x['d'])==k for x in results)for k in sorted({(x['W'],x['O'],x['d'])for x in results})},'columns':results})
D=S/'replay';D.mkdir(exist_ok=True);(D/'all-reported-column-checks.json').write_text(json.dumps({'scope':'all fixed reported columns only; shared original direct Fraction coefficients, stored Python binary floats treated as exact rational dual components; no global pricing search or independent whole-row derivation','reports':reports},ensure_ascii=False,indent=2)+'\n')
event={'event':'one full finite reported-column replay; imports current price_aligned definitions but never check/run/main; no search','start_utc':start,'elapsed_seconds':time.monotonic()-tick,'exit_code':0,'Python':platform.python_version(),'assertions_enabled':__debug__,'price_aligned_definition_imports':1,'block_price_imports':0,'price_root_hist_imports':0,'original_CLI_calls':0,'search_run_calls':0,'random_formula_check_calls':0,'LP_calls':0,'columns_checked':sum(x['negative_columns']for x in reports),'source_exact_coefficient_evaluations':2196*sum(x['negative_columns']for x in reports),'root_completion_evaluations':0}
(D/'column-replay-execution.json').write_text(json.dumps(event,ensure_ascii=False,indent=2)+'\n');print(json.dumps(event,ensure_ascii=False,indent=2))
