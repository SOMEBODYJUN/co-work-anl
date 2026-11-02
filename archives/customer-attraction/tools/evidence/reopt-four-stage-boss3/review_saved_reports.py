"""Bind four frozen reports without executing their LP generators.

Only one atom is sent through borrowed row definitions to bind ordered row names.
The 200 new three-player coefficients are evaluated on all 64 original atoms.
No old 2196-row matrix, exact recovery, pricing, or optimizer is rerun.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
import argparse, ast, hashlib, json, math, platform, time

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo', required=True, type=Path)
    ap.add_argument('--output', type=Path)
    args=ap.parse_args()
    base=Path(__file__).resolve().parent
    repo=args.repo.resolve()
    ev=repo/'archives/customer-attraction/tools/evidence'
    prior=ev/'aligned-dual-five-boss3'
    helpers=ev/'global-indexed-reviews-boss3/related'
    inputs={}
    def read(p):
        p=p.resolve()
        inputs[str(p.relative_to(repo)) if p.is_relative_to(repo) else str(p)]={'size':p.stat().st_size,'sha256':sha(p)}
        return p.read_text()
    start=time.monotonic()
    tags=('support','cross','tax','triple')
    reports={t:json.loads(read(base/'original'/('reopt_'+t+'.json'))) for t in tags}
    aligned=json.loads(read(prior/'original/reopt_aligned.json'))
    exact=json.loads(read(prior/'original/aligned_support_exact_dual.json'))
    negative=json.loads(read(prior/'original/aligned_dual_exact_negative.json'))
    oldreview=json.loads(read(prior/'parameter-and-one-column-comparison.json'))
    cert=json.loads(read(prior/'related/evidence/certificates/customer_attraction/five_player_indexed_bound.json'))['primal']
    atoms=cert['atoms']
    assert len(atoms)==64
    # Borrow definitions only; the canonical audit's top-level full-domain run is excluded.
    source=read(prior/'related/tests/audits/customer_attraction_five_indexed.py')
    ns={}
    exec(compile(source.split('from pathlib import Path')[0],'<borrowed canonical definitions>','exec'),ns)
    env={'F':F,'product':product,'combinations_with_replacement':combinations_with_replacement,
         'types':list(product((0,1),repeat=3)), 'quads':list(product((0,1),repeat=4)),
         'labels':'ABCDEUVWXY','paths':{'actual':'ABCDE','second':'AEUVW','third':'ABEXY'}}
    funs={}
    for tag,file in [('off','offdiagonal_probe.py'),('cross','crossmenu_probe.py'),('tax','menutax_probe.py'),('align','alignedtax_probe.py'),('triple','tripleprofit_probe.py')]:
        tree=ast.parse(read(helpers/file))
        funcs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('q','rows')]
        scope=dict(env)
        if 'q' not in scope: scope['q']=lambda n,d:F(n,d) if n else F()
        exec(compile(ast.Module(body=funcs,type_ignores=[]),'<borrowed '+file+' functions only>','exec'),scope)
        funs[tag]=scope['rows']
    a=atoms[0]
    rows=ns['evaluate'](list(map(int,a['bits'])),[a['AB_hist'],a['AE_hist'],a['second_hist']],a['menus_lh'],True)
    assert len(rows)==437
    stage_names={}
    for tag,fs in [('support',('off',)),('cross',('cross',)),('tax',('tax',)),('aligned',('align',)),('triple',('triple',))]:
        for f in fs: rows.update(funs[f](a))
        stage_names[tag]=list(rows)
    assert [len(stage_names[t]) for t in ('support','cross','tax','aligned','triple')]==[464,534,1920,2196,2396]
    assert aligned['names']==stage_names['aligned']
    w=[int(any(map(int,a['bits'][:5]))) for a in atoms]
    o=[int(any(a['AB_hist'][4:])) for a in atoms]
    summaries={}
    for t,d in reports.items():
        wanted=['scope','status','objective','point','names']+(['dual_lambda','dual_beta'] if t=='triple' else [])
        assert list(d)==wanted and d['names']==stage_names[t]
        assert len(d['names'])==len(set(d['names']))
        assert len(d['point'])==64 and all(type(v) is float and math.isfinite(v) and v>=0 for v in d['point'])
        assert isinstance(d['scope'],str) and isinstance(d['status'],str)
        assert type(d['objective']) is float and math.isfinite(d['objective'])
        x=list(map(F,d['point']))
        W=sum((wi*xi for wi,xi in zip(w,x)),F())
        O=sum((oi*xi for oi,xi in zip(o,x)),F())
        out={'fields_accounted_for':wanted,'scope':d['scope'],'status':d['status'],
             'objective':d['objective'],'ordered_names_matched_to_borrowed_definitions':True,
             'ordered_names_count':len(d['names']),'names_unique':True,'point_length':64,
             'positive_point_indices':[i for i,v in enumerate(x) if v>0],
             'positive_point_count':sum(v>0 for v in x),'all_point_coordinates_nonnegative':True,
             'W_from_saved_binary_floats':str(W),'W_minus_one':str(W-1),'W_minus_one_float':float(W-1),
             'O_from_saved_binary_floats':str(O),'O_minus_saved_objective':str(O-F(d['objective'])),
             'O_minus_saved_objective_float':float(O-F(d['objective'])),
             'point_semantics':'64 new masses in frozen original-atom order; not original mass_numerator',
             'exact_primal_feasibility_not_claimed':True}
        if t=='triple':
            assert len(d['dual_lambda'])==len(d['names']) and all(type(v)is float and math.isfinite(v) and v>=0 for v in d['dual_lambda'])
            assert type(d['dual_beta'])is float and math.isfinite(d['dual_beta'])
            out.update(dual_beta=d['dual_beta'],positive_dual_count=sum(v>0 for v in d['dual_lambda']),
                       positive_dual=[{'row':n,'value':v} for n,v in zip(d['names'],d['dual_lambda']) if v>0],
                       beta_minus_objective=str(F(d['dual_beta'])-F(d['objective'])))
        summaries[t]=out
    diffs={}
    for p,q in [('support','cross'),('cross','tax'),('tax','triple')]:
        x,y=reports[p],reports[q]
        entries=[{'index':i,'before':a,'after':b,'exact_binary_difference':str(F(b)-F(a)),
                  'difference_float':b-a}for i,(a,b) in enumerate(zip(x['point'],y['point'])) if a!=b]
        diffs[p+'->'+q]={'names_prefix_equal':y['names'][:len(x['names'])]==x['names'],
                         'added_names':y['names'][len(x['names']):],
                         'same_point_exactly':x['point']==y['point'],
                         'same_positive_indices':summaries[p]['positive_point_indices']==summaries[q]['positive_point_indices'],
                         'changed_coordinates':len(entries),'max_abs_point_difference':max(abs(a-b)for a,b in zip(x['point'],y['point'])),
                         'all_point_differences':entries,
                         'objective_difference':y['objective']-x['objective']}
    triple=reports['triple']; n=len(aligned['names'])
    identical={'point_all64_equal':triple['point']==aligned['point'],
               'names_first2196_equal':triple['names'][:n]==aligned['names'],
               'dual_first2196_equal':triple['dual_lambda'][:n]==aligned['dual_lambda'],
               'objective_equal':triple['objective']==aligned['objective'],
               'dual_beta_equal':triple['dual_beta']==aligned['dual_beta'],
               'new200_dual_all_exact_float_zero':all(v==0. for v in triple['dual_lambda'][n:])}
    assert all(identical.values())
    # New-row diagnostics only; deliberately do not rebuild the already audited old matrix.
    trcols=[funs['triple'](a) for a in atoms]
    assert all(list(c)==triple['names'][n:] for c in trcols)
    newslack={name:sum((F(x)*c[name] for x,c in zip(triple['point'],trcols)),F()) for name in triple['names'][n:]}
    assert len(newslack)==200 and min(newslack.values())>0
    # Reuse the already audited exact old certificate, algebraically extend by zero.
    lam={name:F(v)for name,v in exact['multipliers'].items()}
    beta=F(exact['beta']); residuals=list(map(F,exact['support_column_residuals']))
    assert len(lam)==36 and all(v>0 for v in lam.values()) and set(lam)<=set(aligned['names'])
    assert len(residuals)==64 and min(residuals)>=0 and beta<2
    assert all(name not in lam for name in triple['names'][n:])
    assert F(negative['residual'])==F(oldreview['outside_column']['new_rational_residual'])<0
    result={'scope':'static full-field/element version binding; one-atom row-name contract; new200 coefficient diagnostics only',
            'reports':summaries,'stage_differences':diffs,'triple_vs_aligned':identical,
            'new200_slacks_at_saved_binary_point':{'count':200,'all_strictly_positive':True,
               'minimum':str(min(newslack.values())),'minimum_float':float(min(newslack.values())),
               'minimum_rows':[k for k,v in newslack.items() if v==min(newslack.values())],
               'all_rows':{k:str(v)for k,v in newslack.items()},
               'not_a_recovered_exact_primal':True},
            'reused_exact64_column_dual_extended_by200zeros':{'beta':str(beta),'gap_below_two':str(2-beta),
               'positive_old_multipliers':len(lam),'new_multipliers':0,'new_zero_entries':200,
               'same_all64_residuals_without_recomputation':True,'source_residuals':list(map(str,residuals)),
               'outside_column_same_negative_residual':negative['residual'],
               'outside_column_is_not_rescanned':True,'not_all2396_duals_invalidated':True},
            'inputs':inputs,'execution':{'python':platform.python_version(),'elapsed_seconds':time.monotonic()-start,
               'original_reopt_runs_or_imports':0,'LP_calls':0,'canonical_main_runs':0,
               'old2196_matrix_rechecks':0,'old_exact_dual_recoveries':0,'all_type_pricing_runs':0,
               'borrowed_name_contract_atoms':1,'new200_coefficients':200*64,
               'new_math_independent_implementation_claimed':False}}
    target=args.output or base/'saved-report-review.json'
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'reports':{t:{k:v for k,v in d.items()if k in ('objective','positive_point_count','ordered_names_count','W_minus_one_float','dual_beta')}for t,d in summaries.items()},'triple_vs_aligned':identical,'new200_minimum_float':float(min(newslack.values())),'execution':result['execution']},ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
