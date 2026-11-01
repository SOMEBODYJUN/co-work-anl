"""One original fixed-input pipeline per frozen record; no original main/RNG."""
from pathlib import Path
import contextlib, datetime, hashlib, importlib.util, io, json, platform, shutil, sys, time
import numpy, scipy
ROOT=Path(__file__).resolve().parent
REPO=Path('/workspace/scratch/c0ab78c47566/boss7-cleaner')
SOURCE=ROOT/'original/background_pair_probe.py'
OLD=REPO/'archives/customer-attraction/tools/evidence/coverage-step-background/research/workspaces/customer-attraction/R-7e9f44beea424d469713364afe7dd180/background_induction/search_background.py'
RUNTIME=ROOT/'runtime'
OUT=ROOT/'replay'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def main():
    assert not OUT.exists(), 'one event only; inspect existing evidence instead of overwriting'
    OUT.mkdir()
    program=RUNTIME/'research/workspaces/customer-attraction/R-731efdb50dd844178e597d804bdd4596/security_induction/background_pair_probe.py'
    dependency=RUNTIME/'research/workspaces/customer-attraction/R-7e9f44beea424d469713364afe7dd180/background_induction/search_background.py'
    for src,dst in [(SOURCE,program),(OLD,dependency)]:
        dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
    (RUNTIME/'AGENTS.md').write_text('Isolated runtime marker for frozen dynamic import; not the live repository.\n')
    started=datetime.datetime.now(datetime.timezone.utc).isoformat();t0=time.perf_counter()
    stream=io.StringIO();errors=io.StringIO();records=[];lp_calls=[]
    with contextlib.redirect_stdout(stream),contextlib.redirect_stderr(errors):
        spec=importlib.util.spec_from_file_location('frozen_background_pair_probe',program)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        original_lp=module.linprog
        def observed_lp(*args,**kwargs):
            result=original_lp(*args,**kwargs)
            lp_calls.append({'c':numpy.asarray(args[0]).tolist(),
                'A_ub':kwargs['A_ub'].tolist(),'b_ub':kwargs['b_ub'].tolist(),
                'A_eq':kwargs['A_eq'].tolist(),'b_eq':kwargs['b_eq'],
                'bounds':kwargs['bounds'],'method':kwargs['method'],
                'result':{'success':bool(result.success),'status':int(result.status),'message':str(result.message),
                    'x':result.x.tolist(),'fun':float(result.fun),'nit':int(result.nit),
                    'ineqlin_residual':result.ineqlin.residual.tolist(),
                    'ineqlin_marginals':result.ineqlin.marginals.tolist(),
                    'eqlin_residual':result.eqlin.residual.tolist(),'eqlin_marginals':result.eqlin.marginals.tolist()}})
            return result
        module.linprog=observed_lp
        for name in ['background_pair_best_6_3.json','background_pair_best_6_4.json','background_pair_best_7_5.json']:
            path=ROOT/'original'/name; data=json.loads(path.read_text());weights={int(k):v for k,v in data['weights'].items()}
            module.old.BackgroundSolver.solve.cache_clear()
            tick=time.perf_counter()
            sol=module.old.BackgroundSolver(data['q'],data['r'],data['prefix'],weights)
            init_cache=sol.solve.cache_info()._asdict()
            pair,witness=module.minimum_pair(sol)
            v,p=module.security(sol.q,sol.r,sol.prefix,weights)
            original_seconds=time.perf_counter()-tick
            # Restore a complete ordered-history pure policy from already-computed exact sets.
            # This is new deterministic witness extraction, not part of the frozen producer.
            actions=[]; q,r=sol.q,sol.r; first,second,target=witness;target=tuple(target)
            def expand(h,c,t):
                if len(h)==r:return
                idx=sol.tidx[t]; bit=1<<idx;floor=sol.thresholds[c]
                valid=[]
                for a in range(q):
                    ca=tuple(c[j]+int(j==a)for j in range(q))
                    if sol.solve(ca)&bit and sol.pays[idx][a]>=floor:valid.append(a)
                chosen=first if not h else second if len(h)==1 and h==(first,) else min(valid)
                assert chosen in valid
                actions.append([list(h),chosen])
                for a in range(q):
                    ca=tuple(c[j]+int(j==a)for j in range(q))
                    if a==chosen:child=t
                    else:
                        bits=sol.solve(ca);indexes=[]
                        while bits:
                            low=bits&-bits;bits-=low;indexes.append(low.bit_length()-1)
                        child=sol.terminals[min(indexes,key=lambda k:(sol.pays[k][a],k))]
                    expand(h+(a,),ca,child)
            expand((),(0,)*q,target)
            count_states=[]
            for depth in range(r+1):
                for c in module.old.compositions(depth,q):
                    count_states.append({'counts':c,'outcomes_bitset_hex':hex(sol.solve(c)),
                                         'scaled_threshold':sol.thresholds.get(c)})
            rec={'source':name,'input_sha256':sha(path),'q':q,'r':r,'background_providers':sum(sol.prefix),
                 'original_calls':{'BackgroundSolver':1,'minimum_pair':1,'security':1,'linprog':1,'main':0,'random_trials':0},
                 'original_pipeline_seconds':original_seconds,'pair':str(pair),'witness':witness,
                 'v':v,'p':p.tolist(),'ratio':float(pair)/(2*v) if v else 1.,
                 'initial_solve_cache':init_cache,'scale':sol.scale,'terminals':sol.terminals,
                 'scaled_topic_payoffs':sol.pays,'remaining_total_profits':[str(x) for x in sol.profits],
                 'count_states':count_states,'strategy':actions,'new_strategy_extraction':'all ordered histories; smallest admissible action except prescribed first two; each off-action child minimizes deviator scaled payoff, then terminal index',
                 'original_lp_call_index':len(lp_calls)-1}
            records.append(rec)
    dump(OUT/'saved-point-capture.json',records);dump(OUT/'lp-capture.json',lp_calls)
    (OUT/'stdout.txt').write_text(stream.getvalue());(OUT/'stderr.txt').write_text(errors.getvalue())
    dump(OUT/'execution.json',{'started_at_utc':started,'finished_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'elapsed_seconds':time.perf_counter()-t0,'exit_code':0,'python':sys.version,'platform':platform.platform(),
        'numpy':numpy.__version__,'scipy':scipy.__version__,'assertions_enabled':__debug__,
        'counts':{'original_main':0,'random_trials':0,'BackgroundSolver':3,'minimum_pair':3,'security':3,'linprog':3,'new_complete_strategy_extractions':3},
        'scope':'three frozen fixed inputs, not replay of historical random trajectories; original functions unchanged except passive linprog wrapper',
        'bindings':[{'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)}for p in [Path(__file__),SOURCE,OLD]+list((ROOT/'original').glob('*.json'))],
        'outputs':[{'path':p.name,'bytes':p.stat().st_size,'sha256':sha(p)}for p in OUT.iterdir() if p.is_file()]})
    print(json.dumps({'status':'PASS','cases':len(records),'original_main':0,'DP':3,'LP':len(lp_calls),'seconds':time.perf_counter()-t0}))
if __name__=='__main__':main()
