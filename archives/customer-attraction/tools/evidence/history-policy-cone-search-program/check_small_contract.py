"""One small-domain source replay plus independent literal-history verification.
This is not an exhaustive SPE search and does not invoke the sibling verifier.
"""
from pathlib import Path
from fractions import Fraction
from itertools import product, combinations
import importlib.util, json, math, platform
import numpy as np
import scipy

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('frozen_policy_cone_search', HERE/'original/policy_cone_search.py')
source = importlib.util.module_from_spec(spec)
spec.loader.exec_module(source)


def counts(h, k):
    return tuple(h.count(j) for j in range(k))


def history_index(h, k):
    out = 0
    for a in h:
        out = out*k+a
    return out


def coeff(h, a, k):
    return tuple(Fraction(int(bool(b & (1 << a))), sum(bool(b & (1 << j)) for j in h))
                 if b & (1 << a) else Fraction(0)
                 for b in range(1, 1 << k))


def full_action(C, act, h, ordered):
    return int(act[len(h)][history_index(h, C.k)]) if ordered else int(act[counts(h, C.k)])


def finish(C, act, h, ordered):
    h = tuple(h)
    while len(h) < C.m:
        h += (full_action(C, act, h, ordered),)
    return h


def dot(x, y):
    return sum(a*b for a, b in zip(x, y))


def run(ordered):
    k=m=3
    C=(source.OrderedCone if ordered else source.Cone)(k,m)
    rng=np.random.default_rng(731)
    seed=np.zeros((1 << k)-1);seed[-1]=1.
    act, terminal=C.policy(seed,rng)
    hs=[h for t in range(m) for h in product(range(k), repeat=t)]
    independent={}
    for h in hs:
        a=full_action(C,act,h,ordered)
        end=finish(C,act,h,ordered)
        p=coeff(end,a,k)
        for b in range(k):
            if b==a: continue
            alt=finish(C,act,h+(b,),ordered)
            key=(a,C.tidx[counts(end,k)],b,C.tidx[counts(alt,k)])
            row=tuple(x-y for x,y in zip(coeff(alt,b,k),p))
            assert key not in independent or independent[key]==row
            independent[key]=row
    capture={}
    real=source.linprog
    def capture_and_solve(*args,**kwargs):
        capture['A']=kwargs['A_ub'].toarray()
        capture['b']=np.asarray(kwargs['b_ub'])
        capture['eq']=np.asarray(kwargs['A_eq'])
        capture['beq']=kwargs['b_eq']
        return real(*args,**kwargs)
    source.linprog=capture_and_solve
    try:
        ans,root=C.optimize(act,terminal)
    finally:
        source.linprog=real
    if ordered:
        expected=[independent[key] for key in sorted(independent)]
    else:
        expected=[]
        for q in C.states:
            h=tuple(j for j,n in enumerate(q) for _ in range(n))
            a=full_action(C,act,h,False)
            end=finish(C,act,h,False)
            for b in range(k):
                if b==a:continue
                alt=finish(C,act,h+(b,),False)
                expected.append(tuple(x-y for x,y in zip(coeff(alt,b,k),coeff(end,a,k))))
    assert capture['A'].shape==(len(expected),(1 << k)-1)
    errors=[]
    for actual, want in zip(capture['A'],expected):
        for value, exact in zip(actual,want):
            errors.append(abs(float(value)-float(exact)))
            assert Fraction(float(value)).limit_denominator(6)==exact
    assert max(errors,default=0)<1e-15
    root_end=finish(C,act,(),ordered)
    root_cov=tuple(int(any(b & (1 << a) for a in root_end)) for b in range(1,1 << k))
    assert tuple(capture['eq'][0])==root_cov and tuple(capture['beq'])==(1.,)
    assert np.all(capture['b']==0)
    assert ans.success
    x=[Fraction(float(v)).limit_denominator(10**6) for v in ans.x]
    assert min(x)>=0 and dot(root_cov,x)==1
    slacks=[]
    for h in hs:
        a=full_action(C,act,h,ordered)
        end=finish(C,act,h,ordered)
        for b in range(k):
            alt=finish(C,act,h+(b,),ordered)
            slacks.append(dot(coeff(end,a,k),x)-dot(coeff(alt,b,k),x))
    assert min(slacks)>=0
    opt=max(sum(x[b-1] for b in range(1,1 << k) if any(b & (1 << a) for a in J))
            for J in combinations(range(k),min(m,k)))
    divisor=math.lcm(*(v.denominator for v in x))
    integers=[int(v*divisor) for v in x]
    candidate=HERE/('small_ordered_candidate.json' if ordered else 'small_count_candidate.json')
    C.write_candidate(candidate,ans.x,act,terminal,-ans.fun)
    saved=json.loads(candidate.read_text())
    for h in hs:
        restored=(saved['ordered_policy'][str(len(h))][history_index(h,k)] if ordered
                  else saved['policy'][','.join(map(str,counts(h,k)))])
        assert restored==full_action(C,act,h,ordered)
    groups={}
    for h in hs: groups.setdefault(counts(h,k),set()).add(full_action(C,act,h,ordered))
    return {'class':'OrderedCone' if ordered else 'Cone','k':k,'m':m,'seed':731,
            'source_policy_calls':1,'source_optimize_calls':1,'solver_calls':1,'source_write_candidate_calls':1,
            'count_states':len(C.states),'ordered_decision_histories':len(hs),'nonself_literal_comparisons':len(hs)*(k-1),
            'lp_rows':len(expected),'lp_columns':len(x),'matrix_coordinates_compared':len(expected)*len(x),
            'maximum_float_coefficient_error':max(errors,default=0),'all_matrix_coordinates_match_literal_rational_rows':True,
            'same_count_groups_with_different_actions':sum(len(v)>1 for v in groups.values()),
            'float_solver_status':int(ans.status),'float_objective':float(-ans.fun),'float_weights':ans.x.tolist(),
            'reconstruction':'Fraction(float).limit_denominator(1000000), newly chosen rational point',
            'rational_weights':list(map(str,x)),'exact_all_history_including_self_comparisons':len(slacks),
            'minimum_exact_slack':str(min(slacks)),'root_history':list(root_end),'W':'1','true_OPT':str(opt),
            'integer_scale':divisor,'integer_weights':integers,'candidate_full_policy_roundtrip':True,
            'scope':'one generated small policy; fixed-point feasibility only; no exact dual or universal bound'}

report={'source_id':'984ad082aeaf3857d562','python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,
        'original_main_calls':0,'sibling_verifier_calls':0,'source_import_calls':1,'total_source_policy_calls':2,
        'total_source_optimize_calls':2,'total_solver_calls':2,'cases':[run(False),run(True)]}
(HERE/'small-contract-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
