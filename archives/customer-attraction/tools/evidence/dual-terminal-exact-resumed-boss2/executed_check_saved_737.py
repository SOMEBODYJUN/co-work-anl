"""Check the two frozen737 certificates with their original exact row/pricing code.

This is an arithmetic replay with shared production code, not an independent
implementation, LP recovery, or an actual SPE construction. No original main
is invoked. A successful saved output is never overwritten.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib, importlib, json, shutil, sys, time

E = Path(__file__).resolve().parent
REPO = next(p for p in E.parents if (p/'cleanup/OBJECTS.md').exists())
PREFIX = REPO/'archives/customer-attraction/tools/evidence'
STAGE = REPO.parent/'parent-737-stage'
STAGE.mkdir(exist_ok=True)
OUT = STAGE/'saved-737-check.json'
if OUT.exists():
    raise SystemExit('Successful result already exists; do not repeat')
ACT = STAGE/'runtime/research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae'
RUNTIME = STAGE/'runtime'
OLD = PREFIX/'round5-terminal-pricing-resumed-boss2'
sources = {
 'round4_pricing/full_pricing.py': PREFIX/'ra277-root-saturation-primary/related-original/research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round4_pricing/full_pricing.py',
 'round4_pricing/cross_pair_pricing.py': PREFIX/'round4-pricing-resumed-boss2/original/cross_pair_pricing.py',
 'round4_pricing/exact_cross_primal.py': PREFIX/'round4-pricing-resumed-boss2/original/exact_cross_primal.py',
 'round4_pricing/exact_primal.py': PREFIX/'round4-pricing-resumed-boss2/original/exact_primal.py',
 'round3_closure/partition_pair_closure.py': PREFIX/'ra277-root-saturation-primary/related-original/research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round3_closure/partition_pair_closure.py',
 'round3_closure/frozen_pair_reoptimization.py': PREFIX/'round4-pricing-resumed-boss2/related/frozen_pair_reoptimization.py',
 'continuation_completion/offdiagonal_closure.py': PREFIX/'continuation-closure-resumed-boss2/original/offdiagonal_closure.py',
 'round4_coupling/joint_transport.py': PREFIX/'round4-joint-transport-resumed-boss2/original/research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round4_coupling/joint_transport.py',
 'round5_pricing/terminal_cross_pricing.py': OLD/'original/terminal_cross_pricing.py',
 'round5_pricing/dual_terminal_pricing.py': REPO/'cleanup/workspaces/Boss2/resume-20261103b/pricing/source/dual_terminal_pricing.py',
}
bindings=[]
for rel,original in sources.items():
    dest=ACT/rel;dest.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(original,dest)
    bindings.append({'runtime':rel,'original':str(original.relative_to(REPO)),
                     'sha256':hashlib.sha256(original.read_bytes()).hexdigest()})
for rel,original in {
 'tests/audits/customer_attraction_five_indexed.py':PREFIX/'five-player-indexed/tests/audits/customer_attraction_five_indexed.py',
 'evidence/certificates/customer_attraction/five_player_indexed_bound.json':PREFIX/'five-player-indexed/evidence/certificates/customer_attraction/five_player_indexed_bound.json'}.items():
    dest=RUNTIME/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original,dest)
    bindings.append({'runtime':rel,'original':str(original.relative_to(REPO)),
                     'sha256':hashlib.sha256(original.read_bytes()).hexdigest()})
(RUNTIME/'customer_attraction').mkdir(exist_ok=True)
(RUNTIME/'customer_attraction/__init__.py').write_text('# Unimported path marker.\n')
sys.path.insert(0,str(ACT/'round5_pricing'))
started=time.perf_counter()
dt=importlib.import_module('dual_terminal_pricing')
ev=importlib.import_module('exact_cross_primal').evaluator()
ev.__class__=dt.DualTerminalUniverse
ev.single=[(f'crossfinal:{s}:{t}:{p}{k}',s,t,p,k)
    for s in ('AB','AE') for t in ('AB','AE','Sbranch') if s!=t
    for p in range(1,4 if t=='Sbranch' else 3) for k in ('D','O')]
verify=importlib.import_module('exact_primal').verify_atom
primal=json.loads((E/'original/exact_optimum_primal_dual_terminal.json').read_text())
dual=json.loads((E/'original/exact_dual_dual_terminal.json').read_text())
D=int(dual['common_denominator']);B=int(dual['beta_numerator'])
assert F(B,D)==F(dual['dual_beta'])==F(primal['comparison_cover'])
assert primal['row_count']==dual['row_count']==737
assert dual['source_sha256']==primal['source_sha256']
assert set(dual['integer_multipliers'])==set(dual['multipliers'])
assert all(F(v)==F(int(dual['integer_multipliers'][n]),D)>=0 for n,v in dual['multipliers'].items())
names=list(primal['slacks']);assert len(names)==737
assert set(dual['multipliers'])<=set(names)
slacks={n:F(0) for n in names};W=O=F(0);matrix=[];residuals=[];metadata=[]
for i,a in enumerate(primal['atoms']):
    bits,hs,d=verify(a);mass=F(a['exact_mass']);assert mass>0
    rr=ev.atom_rows(a);assert set(rr)==set(names)
    for n in names:slacks[n]+=mass*rr[n]
    w=int(any(bits[:5]));o=int(d>0);W+=mass*w;O+=mass*o
    rho=F(B,D)*w-o-sum((F(v)*rr[n] for n,v in dual['multipliers'].items()),F(0))
    assert rho==0
    residuals.append(str(rho));matrix.append([str(rr[n]) for n in names])
    metadata.append({'atom':i,'mass':str(mass),'w':w,'o':o,'common_d':d,'extra_fields':sorted(set(a)-{'bits','AB_hist','AE_hist','second_hist','menus_lh','exact_mass'})})
assert W==F(primal['welfare'])==1 and O==F(primal['comparison_cover'])>2
assert min(slacks.values())>=0 and all(v==F(primal['slacks'][n]) for n,v in slacks.items())
assert all(not slacks[n] for n,v in dual['multipliers'].items() if F(v)>0)
report={'scope':'Shared-original-code exact arithmetic of737 primal and complete-type dual; no optimizer/QR/recovery/CG main and no SPE realization',
 'bindings':bindings,'primal':{'rows':737,'atoms':len(primal['atoms']),'welfare':str(W),'comparison_cover':str(O),
 'all_saved_slacks_match':True,'zero_slacks':[n for n,v in slacks.items() if not v],
 'row_names':names,'coefficients_by_atom':matrix,'atom_metadata':metadata,'slacks':{n:str(v) for n,v in slacks.items()},
 'support_dual_residuals':residuals,'positive_multiplier_rows_are_zero':True},
 'dual_metadata':{'positive_multipliers':len(dual['multipliers']),'D':str(D),'B':str(B),
 'integer_and_rational_weights_match':True,'beta_equals_primal':True},
 'original_main_LP_QR_recovery_CG_runs':0,'wrapper_successful_invocations':1}
(STAGE/'primal-completed.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'primal737_complete':True,'atoms':len(primal['atoms']),'zero_slacks':len(report['primal']['zero_slacks']),'elapsed':time.perf_counter()-started}),flush=True)
U=dt.DualTerminalUniverse();assert U.names==names
lam=[int(dual['integer_multipliers'].get(n,0)) for n in names]
t=time.perf_counter();minimum,negative,contexts=U.price(lam,B,batch=100,integer='object',objective_scale=D)
assert minimum>=0 and not negative
assert minimum==int(dual['minimum_scaled_integer_residual']) and contexts==dual['score_contexts']
report['dual_full_type']={'minimum_scaled_integer_residual':str(minimum),'negative_columns':[],
 'score_contexts':contexts,'original_report_matches':True,'fixed_masks':1024,'common_d_values':6,
 'AB_AE_histograms_each':792,'Sbranch_histograms':15504,'old_menu_corners_each':4,
 'integer_mode':'arbitrary precision object','seconds':time.perf_counter()-t}
report['total_seconds']=time.perf_counter()-started
OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'dual737_complete':True,**report['dual_full_type'],'total_seconds':report['total_seconds']}),flush=True)
