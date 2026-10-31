"""Exact independent audit of a waterfill-to-SPE obstruction.

Reads immutable source packets, expands unit customers, verifies the original
SPE and minimax certificates, then verifies symbolic same-tree and unavoidable
last-BR flips. No canonical solver/verifier, author audit, sympy or LP imports.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product, combinations_with_replacement
from pathlib import Path
import hashlib
import json

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'tail'
I=json.loads((SOURCE/'endogenous_53_instance.json').read_text())
S=json.loads((SOURCE/'endogenous_53_strategy.json').read_text())
CUSTOMERS=tuple(frozenset(x['topics']) for x in I['customers'] for _ in range(x['multiplicity']))
ACTIONS={tuple(x['history']):x['action'] for x in S['actions']}


@lru_cache(None)
def finish(h):
    return h if len(h)==4 else finish(h+(ACTIONS[h],))


def density(path,who,weights=(F(1),)*4):
    return sum((1/sum((weights[j] for j,t in enumerate(path) if t in c),F())
                for c in CUSTOMERS if path[who] in c),F())


def query(topic,opponents):
    return sum((F(1,1+sum(t in c for t in opponents))
                for c in CUSTOMERS if topic in c),F())


def symbolic(path,who):
    constant=F();terms={}
    for c in CUSTOMERS:
        if path[who] not in c:
            continue
        fixed=sum(path[j] in c for j in (0,2,3))
        if path[1] in c:
            terms[fixed]=terms.get(fixed,F())+1
        else:
            constant += F(1,fixed)
    return constant,{k:v for k,v in terms.items() if v}


def difference(z,zprime,who):
    c,x=symbolic(z,who);d,y=symbolic(zprime,who)
    return c-d,{k:x.get(k,F())-y.get(k,F()) for k in x.keys()|y.keys()
                if x.get(k,F())!=y.get(k,F())}


def bernstein_certificate(constant,terms,lower):
    """Multiply by (rho+1)(rho+2), certify on open (lower,1)."""
    assert set(terms)<={1,2}
    x=terms.get(1,F());y=terms.get(2,F())
    p0,p1,p2=2*constant+2*x+y,3*constant+x+y,constant
    scale=1-lower
    q0=p0+p1*lower+p2*lower*lower
    q1=scale*(p1+2*p2*lower)
    q2=scale*scale*p2
    bern=(q0,q0+q1/2,q0+q1+q2)
    assert all(t>=0 for t in bern) and any(t>0 for t in bern)
    return {'power_coefficients':[str(t) for t in (p0,p1,p2)],
            'bernstein_coefficients':[str(t) for t in bern],
            'open_interval':[str(lower),'1']}


def main():
    output=HERE/'waterfill_credibility_audit.json'
    if output.exists():
        raise FileExistsError(output)
    expected={h for depth in range(4) for h in product(range(7),repeat=depth)}
    assert set(ACTIONS)==expected and len(CUSTOMERS)==53
    minimum=None;comparisons=0
    for h in expected:
        z=finish(h);who=len(h);chosen=ACTIONS[h]
        for t in range(7):
            alternative=finish(h+(t,))
            slack=density(z,who)-density(alternative,who)
            assert slack>=0,(h,t,slack)
            comparisons+=1;minimum=slack if minimum is None else min(minimum,slack)
    assert finish(())==(6,0,3,4)
    assert tuple(density(finish(()),i) for i in range(4))==(F(19),F(29,3),F(67,6),F(67,6))
    assert tuple(density((6,0,1,2),i) for i in range(4))==(F(19),F(67,6),F(67,6),F(32,3))

    t=F(28481,2924);D=t-F(29,3)
    primary=tuple(F(x,5848) for x in (570,570,1197,570,570,1197,1174))
    dual={a:F(n,14620) for a,n in (((0,1,2),370),((0,1,6),3941),((0,2,6),1481),
                                   ((1,2,6),1481),((3,4,6),4089),((3,5,6),1629),((4,5,6),1629))}
    assert sum(primary)==sum(dual.values())==1
    backgrounds=tuple(combinations_with_replacement(range(7),3))
    assert min(sum((primary[a]*query(a,b) for a in range(7)),F()) for b in backgrounds)==t
    assert all(sum((prob*query(a,b) for b,prob in dual.items()),F())==t for a in range(7))
    assert D==F(647,8772)

    root_diff=difference((6,0,3,4),(6,2,3,4),1)
    third_diff=difference((6,0,3,4),(6,0,1,2),2)
    assert root_diff==(0,{0:F(-1),2:F(3)})
    assert third_diff==(0,{1:F(-6),2:F(9)})
    expected_rows=(
        ((F(9,2),{2:F(-6)}),(F(-3,2),{1:F(3)}),(F(-5,2),{1:F(3),2:F(3)}),
         (F(3,2),{1:F(6),2:F(-6)}),(F(),{}),(F(-1),{2:F(3)}),
         (F(-5),{1:F(6),2:F(11)})),
        ((F(11,2),{2:F(-12)}),(F(1),{1:F(9),2:F(-12)}),(F(),{}),
         (F(5,2),{1:F(3),2:F(-9)}),(F(5,2),{1:F(3),2:F(-9)}),
         (F(3,2),{1:F(3),2:F(-6)}),(F(-4),{1:F(9),2:F(2)})))
    last_certificates=[]
    for number,(history,chosen,lower) in enumerate((((6,0,3),4,F(0)),((6,0,1),2,F(2,11)))):
        for candidate in range(7):
            row=difference(history+(chosen,),history+(candidate,),3)
            assert row==expected_rows[number][candidate]
            if candidate!=chosen:
                proof=bernstein_certificate(*row,lower)
                last_certificates.append({'history':history,'chosen':chosen,'alternative':candidate,**proof})
    q=lambda w:F(12,2+w)+F(11,3+w)
    assert q(0)-q(1)==F(35,12)>D
    assert q(F(2,11))-q(1)==F(309,140)>D
    assert F(1,3+F(2,11))-F(1,4)==F(9,140)

    core_cases=[]
    for core in (0,1,1000):
        threshold=t+F(core,4)
        g=lambda w:F(12,1+w)+F(11,2+w)+F(core,3+w)
        assert g(1)<threshold<g(0)
        lo,hi=F(0),F(1)
        for _ in range(80):
            mid=(lo+hi)/2
            if g(mid)>threshold:lo=mid
            else:hi=mid
        assert F(2,11)<lo<hi<1
        # Verify all legal query credit bounds with a rational enclosing weight.
        def weighted_query(topic,w):
            old=sum((F(1,1+sum((w if j==0 else F(1)) for j,x in enumerate((0,3,4)) if x in c))
                     for c in CUSTOMERS if topic in c),F())
            return old+F(core,3+w)
        query_credits=[weighted_query(a,lo)-weighted_query(a,F(1)) for a in range(7)]
        assert all(F(0)<=delta<=D for delta in query_credits)
        root_gain_lower=F(2)*(1-hi)/(hi+2)
        third_gain_lower=F(3)*(1-hi)/((hi+1)*(hi+2))
        assert root_gain_lower>0 and third_gain_lower>0
        core_cases.append({'common_core':core,'rho_interval':[str(lo),str(hi)],
                           'strict_root_profit_improvement_lower':str(root_gain_lower),
                           'strict_third_profit_improvement_lower':str(third_gain_lower),
                           'all_query_credit_max_upper':str(max(query_credits))})

    # The completely explicit 3-unit-customer, two-player source game.
    small_customers=(frozenset({0}),frozenset({0}),frozenset({1}))
    def small_u(path,who,w):
        weights=(F(1),w)
        return sum((weights[who]/sum((weights[j] for j,a in enumerate(path) if a in c),F())
                    for c in small_customers if path[who] in c),F())
    assert small_u((0,0),0,F(1))==small_u((1,0),0,F(1))==1
    assert small_u((0,0),1,F(1))==small_u((0,1),1,F(1))==1
    assert small_u((1,0),1,F(1))==2>small_u((1,1),1,F(1))
    assert small_u((0,1),1,F(1,2))-small_u((0,0),1,F(1,2))==F(1,3)

    report={'status':'independent_exact_obstruction_pass',
            'source_packet_hashes':{name:hashlib.sha256((SOURCE/name).read_bytes()).hexdigest()
                                    for name in ('endogenous_53_instance.json','endogenous_53_strategy.json')},
            'original_unit_customers':len(CUSTOMERS),'original_histories':len(expected),
            'original_action_comparisons_including_self':comparisons,'original_minimum_slack':str(minimum),
            'true_v4':str(t),'matching_static_backgrounds':len(backgrounds),'deficit':str(D),
            'zero_mass_query_excess':str(F(35,12)),
            'rho_at_most_2_over_11_query_excess':str(F(309,140)),
            'last_BR_polynomial_certificates':last_certificates,'waterfill_core_cases':core_cases,
            'small_free_threshold_example':{'unit_customers':3,'players':2,'topics':2,
                                             'threshold':'4/3','unique_admissible_weight':'1/2',
                                             'strict_tail_profit_improvement':'1/3'},
            'scope':'No common waterfill weights preserve the original child SPE; the endogenous family even loses its original leaf under any reoptimized last-player policy. No claim excludes a newly reoptimized weighted equilibrium with a different leaf.'}
    payload=json.dumps(report,ensure_ascii=False,indent=2)+'\n'
    with output.open('x') as f:f.write(payload)
    print(json.dumps({k:v for k,v in report.items() if k not in ('last_BR_polynomial_certificates','waterfill_core_cases')},ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
