"""Check three saved exact duals by their original full-type pricing code.

Build the original JointTerminalUniverse once, reuse its common precomputed
arrays for717/727/728, and do not run LP/QR/recovery or any original main.
Check the new65-point728 matrix, reusing the two already verified AE single-O
coefficients. This is shared-original-code arithmetic, not an independent
implementation or a full-game/SPE certificate.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib, importlib, json, shutil, sys, time

E = Path(__file__).resolve().parent
REPO = next(p for p in E.parents if (p/'cleanup/OBJECTS.md').exists())
STAGE = REPO.parent/'boss2-resume-20261102/C3-stage'
STAGE.mkdir(parents=True, exist_ok=True)
OUT = STAGE/'three-duals-and-65-check.json'
if OUT.exists():
    raise SystemExit('Successful output already exists; do not repeat')
RUNTIME = STAGE/'runtime'
ACT = RUNTIME/'research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae'
PREFIX = REPO/'archives/customer-attraction/tools/evidence'
sources = {
 'round4_pricing/full_pricing.py': PREFIX/'ra277-root-saturation-primary/related-original/research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round4_pricing/full_pricing.py',
 'round4_pricing/cross_pair_pricing.py': PREFIX/'round4-pricing-resumed-boss2/original/cross_pair_pricing.py',
 'round4_pricing/exact_cross_primal.py': PREFIX/'round4-pricing-resumed-boss2/original/exact_cross_primal.py',
 'round4_pricing/exact_primal.py': PREFIX/'round4-pricing-resumed-boss2/original/exact_primal.py',
 'round3_closure/partition_pair_closure.py': PREFIX/'ra277-root-saturation-primary/related-original/research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round3_closure/partition_pair_closure.py',
 'round3_closure/frozen_pair_reoptimization.py': PREFIX/'round4-pricing-resumed-boss2/related/frozen_pair_reoptimization.py',
 'continuation_completion/offdiagonal_closure.py': PREFIX/'continuation-closure-resumed-boss2/original/offdiagonal_closure.py',
 'round4_coupling/joint_transport.py': PREFIX/'round4-joint-transport-resumed-boss2/original/research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round4_coupling/joint_transport.py',
 'round5_pricing/terminal_cross_pricing.py': E/'original/terminal_cross_pricing.py',
 'round5_pricing/joint_terminal_pricing.py': E/'original/joint_terminal_pricing.py'}
bindings = []
for rel, original in sources.items():
    dest = ACT/rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(original, dest)
    bindings.append({'runtime':str(dest.relative_to(RUNTIME)), 'original':str(original.relative_to(REPO)), 'sha256':hashlib.sha256(original.read_bytes()).hexdigest()})
for rel, original in {
 'tests/audits/customer_attraction_five_indexed.py':PREFIX/'five-player-indexed/tests/audits/customer_attraction_five_indexed.py',
 'evidence/certificates/customer_attraction/five_player_indexed_bound.json':PREFIX/'five-player-indexed/evidence/certificates/customer_attraction/five_player_indexed_bound.json'}.items():
    dest=RUNTIME/rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(original,dest)
    bindings.append({'runtime':rel,'original':str(original.relative_to(REPO)),'sha256':hashlib.sha256(original.read_bytes()).hexdigest()})
(RUNTIME/'customer_attraction').mkdir(exist_ok=True)
(RUNTIME/'customer_attraction/__init__.py').write_text('# Path existence marker only; never imported.\n')
sys.path.insert(0,str(ACT/'round5_pricing'))
start=time.perf_counter()
jt=importlib.import_module('joint_terminal_pricing')
fp=importlib.import_module('full_pricing')
cp=importlib.import_module('cross_pair_pricing')
tp=importlib.import_module('terminal_cross_pricing')
U=jt.JointTerminalUniverse()
assert len(U.names)==728
report={'scope':'Original-code full-type arithmetic checks of saved717/727/728 duals and saved65-point728 primal only; no original solver/CLI and no full SPE/trueOPT theorem',
        'successful_wrapper_invocations':1,'original_cli_or_recovery_invocations':0,'optimizer_or_QR_invocations':0,
        'reused_single_joint_universe_initializations':1,'original_source_bindings':bindings,'initialization_seconds':time.perf_counter()-start,'duals':{}}
for mode, rows in [('cross_pair',717),('terminal_cross',727),('joint_terminal',728)]:
    p=E/f'original/exact_dual_{mode}.json'
    d=json.loads(p.read_text());D=int(d['common_denominator']);B=int(d['beta_numerator'])
    assert F(B,D)==F(d['dual_beta']) and d['row_count']==rows
    assert set(d['integer_multipliers'])==set(d['multipliers'])
    assert all(F(v)==F(int(d['integer_multipliers'][n]),D)>=0 for n,v in d['multipliers'].items())
    names=U.names[:rows]
    assert set(d['integer_multipliers'])<=set(names)
    lam=[int(d['integer_multipliers'].get(n,0)) for n in names]
    t=time.perf_counter()
    # All three modes share base data. For717 explicitly call CrossUniverse's
    # original method; for727, the11th single row has no multiplier and is
    # therefore ignored by the original zip exactly as for a ten-row instance.
    price=cp.CrossUniverse.price if rows==717 else tp.TerminalUniverse.price
    minimum, negative, contexts=price(U,lam,B,batch=100,integer='object',objective_scale=D)
    assert minimum>=0 and not negative
    assert int(d['minimum_scaled_integer_residual'])==minimum and d['score_contexts']==contexts
    result={'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'row_count':rows,'positive_integer_weights':sum(v>0 for v in lam),
            'beta':d['dual_beta'],'D':str(D),'B':str(B),'minimum_scaled_integer_residual':str(minimum),'negative_columns':[],
            'full1024_masks_and6_common_d':True,'score_contexts':contexts,'original_report_residual_and_contexts_match':True,
            'seconds':time.perf_counter()-t}
    report['duals'][mode]=result
    (STAGE/f'progress-dual-{mode}.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'completed_saved_dual':mode,**result}),flush=True)

manifest=json.loads((E/'source-manifest.json').read_text())
primalpath=REPO/next(a['published_path'] for a in manifest['primary_sources'] if a['path'].endswith('/exact_optimum_primal_joint_terminal.json'))
primal=json.loads(primalpath.read_text())
reusepath=PREFIX/'round5-shared-matching-resumed-boss2/new-728-run/new-728-joint-only-check.json'
reuse=json.loads(reusepath.read_text())
assert reuse['source_sha256']==hashlib.sha256(primalpath.read_bytes()).hexdigest()
assert len(primal['atoms'])==len(reuse['records'])==65
evaluator=importlib.import_module('exact_cross_primal').evaluator()
verify=importlib.import_module('exact_primal').verify_atom
slacks={n:F(0) for n in primal['slacks']};W=O=F(0);coefficients=[]
t=time.perf_counter()
for i,a in enumerate(primal['atoms']):
    bits, hs, d=verify(a);mass=F(a['exact_mass']);assert mass>0
    assert reuse['records'][i]['atom_index']==i and F(reuse['records'][i]['mass'])==mass
    rr=cp.CrossUniverse.atom_rows(evaluator,a)
    for n,target,pos,kind in U.single:
        if target=='AE' and kind=='O':
            assert pos in (1,2)
            rr[n]=F(reuse['records'][i]['single_coefficients'][pos-1])
        else:
            components=((2,'O',F(1)),(3,'O',F(1))) if kind=='OO' else ((pos,kind,F(1)),)
            rr[n]=tp.joint_row(a,'AB','second' if target=='Sbranch' else target,components)
    assert len(rr)==728 and set(rr)==set(slacks)
    for n in slacks:slacks[n]+=mass*rr[n]
    W+=mass*int(any(bits[:5]));O+=mass*int(d>0)
    coefficients.append([str(rr[n]) for n in slacks])
assert W==F(primal['welfare'])==1 and O==F(primal['comparison_cover'])>2
assert min(slacks.values())>=0 and all(v==F(primal['slacks'][n]) for n,v in slacks.items())
assert O==F(report['duals']['joint_terminal']['beta'])
report['primal65']={'input_sha256':hashlib.sha256(primalpath.read_bytes()).hexdigest(),'rows':728,'atoms':65,'welfare':str(W),'comparison_cover':str(O),
                    'all728_saved_slacks_match':True,'zero_slacks':[n for n,v in slacks.items() if not v],
                    'coefficient_rows_in_order':list(slacks),'coefficients_by_atom':coefficients,'slacks':{n:str(v) for n,v in slacks.items()},
                    'new_coefficients':726*65,'same65_mature_singleO_coefficients_reused':2*65,
                    'mature_reuse_input':str(reusepath.relative_to(REPO)),'mature_reuse_sha256':hashlib.sha256(reusepath.read_bytes()).hexdigest(),
                    'specified_AB_to_AE_joint_only_rerun':False,'seconds':time.perf_counter()-t}
report['total_seconds']=time.perf_counter()-start
OUT.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'primal65_all728_saved_values_match':True,'zero_slacks':len(report['primal65']['zero_slacks']),'total_seconds':report['total_seconds']}),flush=True)
