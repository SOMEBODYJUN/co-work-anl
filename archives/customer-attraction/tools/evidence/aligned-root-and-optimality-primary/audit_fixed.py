"""A9 fixed saved-data audit. No original module/main, LP, pricing or RNG runs.
The three explicitly isolated original aligned_rows calls are recorded separately.
"""
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from functools import lru_cache
from pathlib import Path
from types import SimpleNamespace
import ast, json, hashlib, sys, time, traceback
E=Path(__file__).resolve().parent
O=E/'original';D=E/'dependencies'
def read(p):return json.loads(p.read_text())
def q(n,d):return F(n,d) if n else F(0)
def sh(bits,i):return q(bits[i],sum(bits))
def dump(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def hashed(p):return {'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
TYPES=list(product((0,1),repeat=5)); RPOS='TXYZK'
TAB=[{k:list(map(F,v)) for k,v in read(O/'root_tail'/n)['table'].items()} for n in ['binary_pareto_residual_table.json','binary_pareto_1999_residual_table.json']]
def first_table_binding():
 c=read(D/'binary_tail_exact.json');lam={k:F(v) for k,v in c['multipliers'].items()};count=0
 def rho(p,abcd,aux,e):
  a,b,c,d=abcd; eta=abcd+aux;off=(d,)+aux;v=dict(zip('abcdqrs',eta));rs={}
  for name,path,ii in [('actual',abcd,range(4)),('off',off,range(1,4))]:
   for i in ii:
    own=q(path[i],p+sum(path));den=p+sum(path[:i])+4-i
    for key,bit in v.items():rs[f'{name}:{i}:K:{key}']=own-q(bit,den)
    rs[f'{name}:{i}:sum-opt']=4*own-q(e,den)
   pref=p+sum(path[:2]);H=q(path[2]+path[3],p+sum(path))+q(path[2],(pref+1)*(pref+2))
   rs[name+':pair-opt']=6*H-q(e*(4-e),pref+1)-q(e*(e-1),pref+2)
  rs['root-copy-d']=q(a,p+sum(abcd))-q(d,p+sum(off))
  return (F(5,3) if p else F(2))*q(sum(abcd),p+sum(abcd))-q(e,p+e)-sum(w*rs[n] for n,w in lam.items())
 for p,abcd,e in product(range(2),product(range(2),repeat=4),range(5)):
  values=[rho(p,abcd,aux,e) for aux in product(range(2),repeat=3)];count+=len(values)
  assert min(values)==TAB[0][str(p)+''.join(map(str,abcd))][e]
 mature=read(D/'oct25_binary_tail_raw_audit.json')['retained_residuals_160']
 assert len(mature)==160
 for z in mature:assert TAB[1][str(z['p'])+z['abcd']][z['comparison_count']]==F(z['minimum_residual'])
 return {'initial_table_new_min8_binding':{'entries':160,'auxiliary_values':count,'all_equal':True,'purpose':'bind previously unbound primary table; not rerun original certificate CLI'},'strengthened_table_existing_exact_rows_reused':160,'strengthened_1280_or_4096_new_rechecks':0}
def aligned(a):
 b=tuple(map(int,a['bits'])); h=a['root_hist'];d=sum(n*t[0] for n,t in zip(h,TYPES));cov=int(d>0)
 def sm(f):return sum((n*f(*t) for n,t in zip(h,TYPES) if n),F())
 u=[sm(lambda *t:q(t[i],sum(t))) for i in range(5)];cc=[sm(lambda *t:t[i]) for i in range(5)];tail=sum(u[1:]);rr={}
 rr['Root:aligned:r4']=1499*tail-3000*cov
 rr['Root:aligned:r4-binary']=6*tail+u[0]-d-12*cov
 rr['Root:aligned:r4-binary1999']=5997*tail+997*u[0]-997*d-12000*cov
 for v in range(2):
  rr[f'Root:aligned:r4-pareto{v}']=sm(lambda t,x,y,z,k:(F(5,3) if t else F(2) if v==0 else F(1999,1000))*q(x+y+z+k,t+x+y+z+k)-TAB[v][''.join(map(str,(t,x,y,z,k)))][d-t])-4*cov
 def g4(p,c):return q(c*(c-1),p+c-1)+q((5-c)*c,p+c)
 for m,c in zip(RPOS,cc):rr[f'Root:aligned:r4-binary-menu:{m}']=29985*tail+4985*u[0]-4985*d-3000*sm(lambda t,x,y,z,k:g4(t,c))
 rr['Root:aligned:actual4-binary']=29985*q(sum(b[1:5]),sum(b[:5]))-4985*(b[0]-q(b[0],sum(b[:5])))-3000*g4(b[0],d)
 r0=list(map(F,['0','0','1/750','1/1500','1/1500','39/500','1/1000','623/3000','2747/12000','691/6000','47/1500','1919/12000','0','77/750','1/4000','1169/6000']))
 r1=list(map(F,['0','133/750','2003/12000','61853/180000','251/3000','6331/22500','7363/36000','26047/60000','239/1200','14579/45000','22183/90000','5177/12000','15767/90000','63893/180000','43349/180000','41143/90000']))
 rr['Root:aligned:r4-credit']=2998*tail-6000*cov-sm(lambda t,x,y,z,k:1500*(r1 if t else r0)[8*x+4*y+2*z+k])
 def g3(p,c):return q(c*(4-c)*(3-c)//2,p+1)+q(c*(c-1)*(4-c),p+2)+q(c*(c-1)*(c-2)//2,p+3)
 rr['Root:aligned:r3']=20*sum(u[2:])-3*sm(lambda t,x,y,z,k:g3(t+x,d-t))
 H=u[3]+u[4]+sm(lambda t,x,y,z,k:q(z,(t+x+y+1)*(t+x+y+2)))
 rr['Root:aligned:r2']=6*H-sm(lambda t,x,y,z,k:q((d-t)*(4-d+t),t+x+y+1)+q((d-t)*(d-t-1),t+x+y+2))
 for i in range(1,5):
  rr[f'Root:aligned:opt:{i}']=4*u[i]-sm(lambda *t:q(d-t[0],sum(t[:i])+5-i))
  for j,m in enumerate(RPOS[1:],1):rr[f'Root:aligned:menu:{i}:{m}']=4*u[i]-cc[j]*sm(lambda *t:q(1,sum(t[:i])+5-i))+sm(lambda *t:q(t[j],sum(t[:i])+5-i))
 return rr

def cg_audit():
 data=read(O/'template/aligned_root_cg.json');atoms=data['atoms'];pp=list(map(lambda v:F(str(v)),data['primal_float']));assert len(atoms)==len(pp)==934
 for a in atoms:
  ds=[]
  for key,n in [('AB_hist',3),('AE_hist',3),('second_hist',4),('root_hist',5)]:
   h=a[key];assert len(h)==2**n and all(isinstance(v,int) and v>=0 for v in h) and sum(h)==5
   ds.append(sum(h[2**(n-1):]))
  assert len(set(ds))==1
  d=ds[0]
  for l,h in a['menus_lh']:assert 0<=h<=d and 0<=l-h<=5-d
 rows=[aligned(a) for a in atoms];names=list(rows[0]);assert len(names)==34
 saved=[n for n in data['row_names'] if n.startswith('Root:aligned:')];new=[n for n in names if n not in saved]
 assert len(data['row_names'])==756 and len(saved)==25 and len(new)==9
 totals={n:sum(p*rs[n] for p,rs in zip(pp,rows)) for n in names}
 norm=sum(p*int(any(map(int,a['bits'][:5]))) for p,a in zip(pp,atoms));obj=sum(p*int(any(a['AB_hist'][4:])) for p,a in zip(pp,atoms))
 # Execute only this unchanged original pure function AST, not any original imports/module/Universe.
 src=O/'template/aligned_root_pricing.py';tree=ast.parse(src.read_text());node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='aligned_rows')
 ns={'F':F,'base':SimpleNamespace(EX={'q':q},VE={}), 'TYPES':TYPES,'RPOS':RPOS,'TABLES':TAB}
 exec(compile(ast.Module(body=[node],type_ignores=[]),str(src), 'exec'),ns)
 dump(E/'replay/isolated-function-inputs.json',{'extraction':'ast.parse original bytes; compile only unchanged aligned_rows FunctionDef; no original imports/module; supply q and table/type/RPOS mathematical inputs; numpy only for vector call','original_source':hashed(src),'extracted_function':ast.get_source_segment(src.read_text(),node)})
 normal=next(a for a in atoms if sum(a['root_hist'][16:])==1)
 assert ns['aligned_rows'](normal['root_hist'],True,normal['bits'])==aligned(normal)
 d5=next(a for a in atoms if sum(a['root_hist'][16:])==5)
 z=read(E/'replay/isolated-function-inputs.json');z.update(normal_atom=normal,d5_atom=d5,vector_histograms=[normal['root_hist'],d5['root_hist']]);dump(E/'replay/isolated-function-inputs.json',z)
 errors=[]
 try:ns['aligned_rows'](d5['root_hist'],True,d5['bits'])
 except Exception as ex:errors.append({'call':'isolated original exact d=5','type':type(ex).__name__,'message':str(ex),'traceback':traceback.format_exc()})
 else:raise AssertionError('expected original out-of-range not observed')
 import numpy as np
 ns.update(np=np,base=SimpleNamespace(EX={'q':q},VE={'q':lambda n,d:np.divide(n,d,out=np.zeros(np.broadcast(n,d).shape),where=np.asarray(n)!=0)}))
 try:ns['aligned_rows'](np.asarray([normal['root_hist'],d5['root_hist']]).T,False)
 except Exception as ex:errors.append({'call':'isolated original vector two histograms including d=5','type':type(ex).__name__,'message':str(ex),'traceback':traceback.format_exc()})
 else:raise AssertionError('expected vector out-of-range not observed')
 assert len(errors)==2 and all(z['type']=='IndexError' for z in errors)
 return {'atoms':len(atoms),'row_names':len(data['row_names']),'base_and_root_rows':731,'saved_aligned_rows':saved,'current_function_aligned_rows':names,'nine_new_names':new,'same_saved_output_for_current_code':False,'primal_positive_entries':sum(v>0 for v in pp),'last80_all_zero':all(v==0 for v in pp[-80:]),'optional_legacy_mass_numerator_indices':[i for i,a in enumerate(atoms) if 'mass_numerator' in a],'normalization_exact_decimal':str(norm),'objective_exact_decimal':str(obj),'objective_float':float(obj),'original_dual_beta_float':data['dual_beta_float'],'history':data['history'],'aligned_totals_from_saved_decimal_primal':{n:{'exact_decimal_interpretation':str(v),'float':float(v),'in_saved_rows':n in saved} for n,v in totals.items()},'negative_rows_beyond_1e-8':[n for n,v in totals.items() if v<F(-1,10**8)],'isolated_original_function_calls':3,'normal_exact_function_equality':True,'original_function_exceptions':errors,'new_independent_aligned_atom_rows':934*34,'full_731_inherited_rows_replayed':0,'original_module_and_main':0,'Universe_initializations':0,'pricing_calls':0,'LP_calls':0}

def game(weights,p):
 finals=[tuple(t.count(i) for i in range(p)) for t in combinations_with_replacement(range(p),5)];idx={c:i for i,c in enumerate(finals)}
 def util(c,a):return sum((F(w,sum(c[i] for i in range(p) if mask>>i&1)) for mask,w in weights.items() if mask>>a&1),F())
 pay=[[util(c,a) if c[a] else F(0) for a in range(p)] for c in finals]
 def inc(c,a):return c[:a]+(c[a]+1,)+c[a+1:]
 @lru_cache(None)
 def R(c):
  if sum(c)==5:return frozenset([idx[c]])
  ch=[R(inc(c,a)) for a in range(p)];floor=max(min(pay[f][a] for f in fs) for a,fs in enumerate(ch))
  return frozenset(f for a,fs in enumerate(ch) for f in fs if pay[f][a]>=floor)
 return finals,idx,pay,inc,R

def policy_audit(weights,p,policy):
 def finish(h):
  while len(h)<5:h=h+(policy[h],)
  return h
 def payoff(path,i):
  a=path[i];return sum((F(w,sum(bool(mask>>b&1) for b in path)) for mask,w in weights.items() if mask>>a&1),F())
 strict=ties=0;minimum=None
 for h,a in policy.items():
  good=payoff(finish(h),len(h))
  for b in range(p):
   if b==a:continue
   delta=good-payoff(finish(h+(b,)),len(h));assert delta>=0
   strict+=delta>0;ties+=delta==0;minimum=delta if minimum is None else min(minimum,delta)
 return {'ordered_nonterminal_histories':len(policy),'nonprescribed_IC':(p-1)*len(policy),'strict':strict,'ties':ties,'minimum_nonprescribed_slack':str(minimum),'actual_path':finish(()),'actual_payoffs':[str(payoff(finish(()),i)) for i in range(5)]},finish

def fixed_games():
 saved=read(O/'direct/tail_budget_probe.json');weights={int(k):v for k,v in saved['weights'].items()};finals,idx,pay,inc,R=game(weights,5);root=(0,)*5;assert R(root)
 targets=[idx[tuple(c)] for c in saved['branch_counts']];act=saved['actual_root'];policy={():act}
 def build(h,c,f):
  if len(h)==5:assert finals[f]==c;return
  ch=[R(inc(c,a)) for a in range(5)];floor=max(min(pay[g][a] for g in gs) for a,gs in enumerate(ch))
  a=next(a for a,gs in enumerate(ch) if f in gs and pay[f][a]>=floor);policy[h]=a
  for b,gs in enumerate(ch):build(h+(b,),inc(c,b),f if b==a else min(gs,key=lambda g:(pay[g][b],g)))
 for b,f in enumerate(targets):assert f in R(inc(root,b));build((b,),inc(root,b),f)
 out,finish=policy_audit(weights,5,policy);path=finish(());u=pay[idx[tuple(path.count(i) for i in range(5))]][act]
 vs=[];zs=[];branches=[]
 for b in range(5):
  z=finish((b,));c=tuple(z.count(i) for i in range(5));assert c==tuple(saved['branch_counts'][b]);rootprofit=pay[idx[c]][b];assert rootprofit<=u
  W=sum(w for mask,w in weights.items() if any(mask>>a&1 for a in z));vs.append(F(W)-rootprofit);zs.append(rootprofit);branches.append(z)
 W=sum(w for mask,w in weights.items() if any(mask>>a&1 for a in path));opt=max(sum(w for mask,w in weights.items() if any(c[i] and mask>>i&1 for i in range(5))) for c in finals)
 assert u*60==saved['u1_over_60'] and [v*60 for v in vs]==saved['tail_over_60'] and W==saved['W'] and opt==saved['O']
 gap=5997*sum(vs)+4985*u-25994*W;assert gap*60==saved['gap_over_60'] and gap>0
 out.update(root_ordered_paths=branches,root_profits=list(map(str,zs)),tail_profits=list(map(str,vs)),W=W,OPT5=opt,root_profit=str(u),coarse_gap=str(gap),DP_counts_states=R.cache_info().currsize,DP_terminal_counts=len(finals),strategy_origin='new deterministic completion of old saved count targets, not recovery of an old full strategy')
 dump(E/'replay/direct-complete-policy.json',{'topics':list(range(5)),'weights':weights,'players':5,'strategy':{'/'.join(map(str,h)):a for h,a in sorted(policy.items(),key=lambda t:(len(t[0]),t[0]))}})
 saved2=read(O/'security/last_menu_probe.json');inst=saved2['game'];weights2={sum(1<<a for a in c['topics']):c['multiplicity'] for c in inst['customers']};p=7
 policy2={h:5 for d in range(5) for h in product(range(p),repeat=d)};two,_=policy_audit(weights2,p,policy2);assert list(two['actual_path'])==saved2['path'] and two['actual_payoffs']==['10']*5
 pref=(5,)*4;mat=[[sum((F(w,1+sum(bool(mask>>a&1) for a in pref)+bool(mask>>b&1)) for mask,w in weights2.items() if mask>>t&1),F()) for b in range(p)] for t in range(p)]
 upper=max(row[5] for row in mat);assert upper==F(17,2)<10
 two.update(menu_matrix=[[str(v) for v in row] for row in mat],pure_blocker=5,exact_menu_upper_bound=str(upper),original_float_menu=saved2['menu_value'],original_float_ratio=saved2['ratio'],exact_optimum_of_menu_certified=False,W=50,total_customers=sum(weights2.values()),strategy_origin='new all-histories constant-5 certificate for the old actual path; original full policy not saved')
 dump(E/'replay/security-complete-policy.json',{'topics':inst['topics'],'customers':inst['customers'],'players':5,'strategy':{'/'.join(map(str,h)):a for h,a in sorted(policy2.items(),key=lambda t:(len(t[0]),t[0]))}})
 return {'direct':out,'security':two}

def exchange_metadata():
 out=[]
 for name in ['five_player_indexed_bound.json','enhanced_2396_exact_obstruction.json']:
  c=read(D/name);aa=c['primal']['atoms'] if 'primal' in c else c['atom_masses'];weights=[F(a['mass_numerator'],c['primal']['denominator']) if 'primal' in c else F(a['mass']) for a in aa]
  assert all(w>0 for w in weights);ds=sorted(set(sum(a['AB_hist'][4:]) for a in aa));assert ds==[1]
  out.append({'input':name,'atoms':len(aa),'positive_mass':True,'optimal_index_multiplicities':ds,'all_nonzero_customers_in_comparison_union':True})
 reports={}
 for name in ['template/optimality_probe.json','template/optimality_multi_probe.json','exchange/optimality_union_probe.json']:
  data=read(O/name);reports[name]=[{'saved_rows':len(z.get('slacks',{})) if 'slacks' in z else z['rows'],'negative_saved_rows':len(z['violated'] if 'violated' in z else z['negative_rows'])} for z in data]
 return {'input_structural_binding':out,'saved_report_shapes':reports,'original_probe_main_or_function_runs':0,'exchange_slacks_numerically_recomputed':0,'analytical_reason':'all positive-mass atoms have d=1; each reported optimality row is a sum of nonnegative gain indicators and zero d=0 loss terms, including anchored keep/drop; no inference of SPE or true OPT completion'}

def main():
 t=time.perf_counter();start=time.time();result={'scope':'fixed original saved-data binding and explicitly new full policies; not global LP or random search','table_binding':first_table_binding(),'cg':cg_audit(),'games':fixed_games(),'exchange':exchange_metadata()};dump(E/'replay/fixed-audit.json',result)
 record={'python':sys.version,'started_unix':start,'duration_seconds':time.perf_counter()-t,'exit_code':0,'original_aligned_rows_isolated_calls':3,'original_aligned_module_main_Universe_LP_pricing':0,'original_random_2000_direct_and_150_security':0,'original_three_optimality_probe_entrypoints':0,'generic_1999_1280_or_4096_rechecks':0,'new_initial_min8_binding_values':1280,'new_game_DP_and_literal_IC':True,'script':hashed(Path(__file__)),'primary_manifest':hashed(E/'source-manifest.json'),'dependencies_manifest':hashed(E/'reused-dependencies.json')};dump(E/'replay/execution.json',record)
 print(json.dumps({'seconds':record['duration_seconds'],'cg_new_names':result['cg']['nine_new_names'],'cg_negative_rows_beyond_1e-8':result['cg']['negative_rows_beyond_1e-8'],'original_exceptions':result['cg']['original_function_exceptions'],'games':result['games']},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
