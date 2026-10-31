"""Exact audit of explicitly saved count policies under three weight readings.

The verifier checks every count state and action, not millions of separate
ordered histories. A count-dependent policy has identical continuation and
IC at every ordered history with the same count; the report records the
number of ordered histories covered by that proved equivalence separately.
No numpy/scipy, canonical solver, or source search code is imported.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache,reduce
from itertools import combinations
from math import comb,factorial,gcd,lcm
from collections import Counter
import hashlib,json

E=Path(__file__).resolve().parent
SUB=Path('research/workspaces/customer-attraction/R-e6796fb9db2a4ae9994cee93ac9bd152/independent')

def compositions(n,k):
    if k==1:yield(n,);return
    for a in range(n+1):
        for z in compositions(n-a,k-1):yield(a,)+z

def jsonable(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):jsonable(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [jsonable(v) for v in x]
    return x

def review(path,origin):
    data=path.read_bytes();raw=json.loads(data);exact=json.loads(data,parse_float=F)
    m,k=raw['m'],raw['k']
    records=raw['policy'];policy={tuple(q):a for q,a in records}
    expected=[q for d in range(m-1,-1,-1) for q in compositions(d,k)]
    assert [tuple(q) for q,a in records]==expected and len(policy)==len(records)
    assert all(0<=a<k for a in policy.values())
    @lru_cache(None)
    def end(q):
        if sum(q)==m:return q
        a=policy[q];return end(q[:a]+(q[a]+1,)+q[a+1:])
    path_actions=[];q=(0,)*k
    while sum(q)<m:
        a=policy[q];path_actions.append(a);q=q[:a]+(q[a]+1,)+q[a+1:]
    assert tuple(raw['root_counts'])==q==end((0,)*k)
    literal={int(mask):F(w) for mask,w in exact['weights']}
    binary={mask:F.from_float(float(w)) for mask,w in literal.items()}
    small={mask:w.limit_denominator(10**6) for mask,w in binary.items()}
    for weights in [literal,binary,small]:assert all(w>=0 for w in weights.values())
    supports=list(combinations(range(k),min(m,k)))
    def welfare(q,w):return sum((v for mask,v in w.items() if any(q[a] and mask>>a&1 for a in range(k))),F(0))
    interpretations=[]
    for mode,weights in [('literal_decimal',literal),('exact_binary_float',binary),('small_denominator_reconstruction',small)]:
        @lru_cache(None)
        def payoff(q,a):
            return sum((v/F(sum(q[b] for b in range(k) if mask>>b&1))
                        for mask,v in weights.items() if mask>>a&1),F(0))
        minimum=None;first_bad=None;checks=0;nonself=0
        for d in range(m):
            for q in compositions(d,k):
                a=policy[q];u=payoff(end(q),a)
                for b in range(k):
                    child=q[:b]+(q[b]+1,)+q[b+1:]
                    gap=u-payoff(end(child),b)
                    minimum=gap if minimum is None else min(minimum,gap)
                    checks+=1;nonself+=b!=a
                    if gap<0 and first_bad is None:first_bad={'past_counts':q,'chosen':a,'alternative':b,'margin':gap}
        root=end((0,)*k);W=welfare(root,weights)
        cov=lambda support:sum((w for mask,w in weights.items() if any(mask>>a&1 for a in support)),F(0))
        best=max((cov(t),t) for t in supports);saved_support=cov(raw['support'])
        D=lcm(*(x.denominator for x in weights.values()))
        ints={a:int(v*D) for a,v in weights.items()};g=reduce(gcd,ints.values());ints={a:n//g for a,n in ints.items()}
        signatures={a:tuple(mask for mask,w in weights.items() if w and mask>>a&1) for a in range(k)}
        interpretations.append({'mode':mode,'weights':sorted(weights.items()),'exact_policy_SPE':first_bad is None,
          'minimum_IC_margin':minimum,'first_violation':first_bad,'count_state_action_comparisons_including_self':checks,
          'count_state_action_comparisons_excluding_self':nonself,'W':W,'OPT':best[0],'OPT_over_W':best[0]/W,
          'saved_support_coverage':saved_support,'saved_support_is_optimal':saved_support==best[0],
          'some_optimal_support':best[1],'root_payoffs':[payoff(root,a) for a in path_actions],
          'primitive_integer_types':sorted(ints.items()),'primitive_unit_customers':sum(ints.values()),
          'primitive_root_welfare':welfare(root,ints),'primitive_OPT':max(cov2 for cov2 in [sum(n for mask,n in ints.items() if any(mask>>a&1 for a in t)) for t in supports]),
          'distinct_topic_coverages':len(set(signatures.values())),'labels':k})
    core=[mask for mask,w in literal.items() if w==1 and mask.bit_count()>1]
    all_core=len(core)==1 and all(core[0]>>a&1 for a in policy.values())
    layers=[];pos=0
    for d in range(m-1,-1,-1):
        n=comb(d+k-1,k-1);block=records[pos:pos+n];pos+=n
        ss=''.join(str(a) for q,a in block)
        assert len(ss)==n and [[list(q),int(a)] for q,a in zip(compositions(d,k),ss)]==block
        layers.append({'depth':d,'canonical_composition_order':'ascending first coordinate recursively',
                       'count_states':n,'all_actions_in_source_order':ss,'action_frequencies':dict(Counter(ss))})
    ordered=sum(k**d for d in range(m));states=len(policy)
    assert sum(factorial(sum(q))//reduce(lambda a,b:a*b,(factorial(n) for n in q),1) for q in policy)==ordered
    return {'origin':origin,'source_path':str(path.relative_to(E)),'source_sha256':hashlib.sha256(data).hexdigest(),
      'm':m,'k':k,'all_nonpolicy_fields':{a:b for a,b in exact.items() if a!='policy'},
      'count_policy_entries':states,'complete_ordered_decision_histories_covered':ordered,
      'ordered_comparisons_including_self_covered':ordered*k,'ordered_comparisons_excluding_self_covered':ordered*(k-1),
      'explicit_ordered_histories_enumerated':False,'quotient_coverage_argument':'same past counts imply identical saved action, all subsequent counts and current/deviation payoffs; every count tuple has multinomial many ordered histories',
      'root_path':path_actions,'root_counts':end((0,)*k),'all_prescribed_actions_in_single_core':all_core,
      'core_mask':core[0] if len(core)==1 else None,'total_action_frequencies':dict(Counter(policy.values())),
      'lossless_policy_layers':layers,'interpretations':interpretations}

frozen=[review(E/'original'/SUB/file,'frozen primary') for file in ['policy_m5k7.json','policy_m6k8.json','policy_m8k8.json']]
fresh=E/'replay-cone/new_policy_cone.json'
new=review(fresh,'new original default m5 main output') if fresh.exists() else None
out={'status':'completed','new_independent_review_runs':1,'timing_recorded':False,'solver_calls':0,
     'original_imports':False,'frozen_policies':frozen,'new_original_output':new,
     'floating_values_not_automatically_true_certificates':True,
     'small_denominator_reconstruction_is_new_explicit_input_version':True}
(E/'independent-policy-review.json').write_text(json.dumps(jsonable(out),ensure_ascii=False,indent=2)+'\n')
for item in frozen+([new] if new else []):
    print(json.dumps(jsonable({k:v for k,v in item.items() if k not in ['lossless_policy_layers','all_nonpolicy_fields','interpretations']}),ensure_ascii=False))
    for a in item['interpretations']:
        print(json.dumps(jsonable({k:v for k,v in a.items() if k not in ['weights','primitive_integer_types']}),ensure_ascii=False))
