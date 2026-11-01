"""New proof-aware definition reconstruction of the documented 24-client input.

No repository solver, optimizer, original audit code or report is imported.
Four supplied JSON inputs and the exact manuscript witnesses are the full input.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import sys


def enc(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,dict): return {str(k):enc(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)): return [enc(v) for v in x]
    return x


def read_inputs(manifest):
    data=json.loads(manifest.read_text());result={}
    for row in data['rows']:
        p=manifest.parent/row['package_relative_path'];raw=p.read_bytes()
        assert len(raw)==row['size'] and hashlib.sha256(raw).hexdigest()==row['sha256']
        result[row['role']]=json.loads(raw)
    assert set(result)=={'example0','certificate0','example1','certificate1'}
    return result


def expand(example,offset):
    assert example['players']==3 and len(example['topics'])==4
    topics=[set() for _ in range(4)];next_id=offset
    for row in example['customers']:
        assert isinstance(row['multiplicity'],int) and row['multiplicity']>0
        for _ in range(row['multiplicity']):
            for a in row['topics']: topics[a].add(next_id)
            next_id+=1
    return tuple(frozenset(t) for t in topics),next_id


def policy(certificate):
    p={tuple(row['history']):row['action'] for row in certificate['actions']}
    expected={h for length in range(3) for h in product(range(4),repeat=length)}
    assert set(p)==expected and len(p)==len(certificate['actions'])==21
    assert all(0<=a<4 for a in p.values())
    return p


def finish(p,h=()):
    h=tuple(h)
    while len(h)<3: h=h+(p[h],)
    return h


def payoff(topics,z,i):
    return sum((F(1,sum(x in topics[a] for a in z)) for x in topics[z[i]]),F())


def covered(topics,z): return len(set().union(*(topics[a] for a in z)))


def verify(topics,p):
    worst=None;comparisons=0
    for h,a in p.items():
        current=payoff(topics,finish(p,h),len(h))
        for b in range(len(topics)):
            slack=current-payoff(topics,finish(p,h+(b,)),len(h))
            assert slack>=0
            worst=slack if worst is None else min(worst,slack)
            comparisons+=1
    return dict(decision_histories=len(p),IC_including_self=comparisons,min_slack=worst)


def kernel(topics,p):
    actual=finish(p);K=[];Z=[]
    for i in range(3):
        endpoints=[finish(p,actual[:i]+(a,)) for a in range(len(topics))]
        Z.append(endpoints)
        K.append([[sum((F(1,1+sum(x in topics[a] for a in z)) for x in topics[t]),F())
                   for z in endpoints] for t in range(len(topics))])
    return K,Z


def psi(K,p):
    return [min(sum(p[t]*K[i][t][a] for t in range(len(p)))
                for a in range(len(p))) for i in range(3)]


def coupling(p,q,kind):
    if kind=='independent': return [a*b for a in p for b in q]
    order=list(range(4)) if kind=='same-order-greedy' else list(reversed(range(4)))
    result=[F()]*16;remaining=list(q)
    for i,mass in enumerate(p):
        for j in order:
            weight=min(mass,remaining[j]);result[4*i+j]+=weight
            mass-=weight;remaining[j]-=weight
        assert mass==0
    assert all(x==0 for x in remaining)
    assert [sum(result[4*i+j] for j in range(4)) for i in range(4)]==p
    assert [sum(result[4*i+j] for i in range(4)) for j in range(4)]==q
    return result


def main():
    manifest=Path(sys.argv[1]);output=Path(sys.argv[2]);assert output.is_dir() and not list(output.iterdir())
    inputs=read_inputs(manifest)
    t0,next_id=expand(inputs['example0'],0);t1,total=expand(inputs['example1'],next_id)
    assert next_id==8 and total==24
    p0=policy(inputs['certificate0']);p1=policy(inputs['certificate1'])
    for p,c in [(p0,inputs['certificate0']),(p1,inputs['certificate1'])]:
        z=finish(p);assert [z.count(a) for a in range(4)]==c['terminal_counts']
    tp=tuple(a|b for a,b in product(t0,t1));assert len(set(tp))==16
    pp={h:4*p0[tuple(a//4 for a in h)]+p1[tuple(a%4 for a in h)]
        for length in range(3) for h in product(range(16),repeat=length)}
    checks=[verify(t0,p0),verify(t1,p1),verify(tp,pp)]
    assert checks[2]['decision_histories']==273 and checks[2]['IC_including_self']==4368
    actual=finish(pp);profits=[payoff(tp,actual,i) for i in range(3)]
    assert actual==(0,7,7) and profits==[F(23,3),F(20,3),F(20,3)] and covered(tp,actual)==21
    K0,Z0=kernel(t0,p0);K1,Z1=kernel(t1,p1);KP,ZP=kernel(tp,pp)
    entries=0
    for i in range(3):
        for a in range(16):
            assert tuple(j//4 for j in ZP[i][a])==Z0[i][a//4]
            assert tuple(j%4 for j in ZP[i][a])==Z1[i][a%4]
            for t in range(16):
                assert KP[i][t][a]==K0[i][t//4][a//4]+K1[i][t%4][a%4]
                entries+=1
    pairs=[
        ([F(i,10) for i in [1,2,3,4]],[F(i,10) for i in [4,3,2,1]],'manuscript-index-order-witness'),
        ([F(0),F(5,9),F(0),F(4,9)],[F(0),F(1,3),F(0),F(2,3)],'manuscript-optimal-marginals'),
        ([F(i,7) for i in [3,1,1,2]],[F(i,8) for i in [2,4,1,1]],'new-positive-marginals'),
        ([F(0),F(1,2),F(1,2),F(0)],[F(1,3),F(0),F(2,3),F(0)],'new-zero-marginals')]
    query_rows=[]
    for p,q,label in pairs:
        c0,c1=psi(K0,p),psi(K1,q)
        for kind in ['independent','same-order-greedy','reverse-order-greedy']:
            joint=coupling(p,q,kind);prices=psi(KP,joint)
            assert prices==[a+b for a,b in zip(c0,c1)]
            query_rows.append(dict(label=label,coupling=kind,p=p,q=q,joint=joint,component_prices=[c0,c1],product_prices=prices))
    order_row=query_rows[0]
    assert order_row['component_prices']==[[F(77,60),F(43,30),F(43,30)],[F(199,60),F(97,30),F(97,30)]]
    assert min(order_row['product_prices'])==F(23,5)
    assert sum(min(r) for r in order_row['component_prices'])==F(271,60)
    V=F(277,54);primal=[F()]*16
    for a,b,w in [(1,1,F(1,3)),(1,3,F(2,9)),(3,3,F(4,9))]:primal[4*a+b]=w
    dual=[(0,5,F(5,9)),(0,8,F(2,5)),(0,9,F(2,45))]
    assert sum(primal)==sum(w for i,a,w in dual)==1 and all(w>=0 for w in primal)
    primal_slacks=[sum(primal[t]*KP[i][t][a] for t in range(16))-V for i in range(3) for a in range(16)]
    dual_slacks=[V-sum(w*KP[i][t][a] for i,a,w in dual) for t in range(16)]
    assert min(primal_slacks)==min(dual_slacks)==0
    assert all(x>=0 for x in primal_slacks+dual_slacks)
    result=dict(kind='new-definition-audit-not-original-replay',input_clients=[8,16],product_clients=24,
                full_strategy_checks=checks,actual_product=actual,payoffs=profits,W=21,W_over_m=7,
                exact_kernel_entries=entries,query_couplings=len(query_rows),
                coupling_input_scope='First two marginal pairs from source; last two are new explicit controls, not certification of unspecified original four pairs.',
                index_order=dict(correct=F(23,5),separate=F(271,60),gap=F(1,12)),
                exact_menu_value=V,primal_probabilities=primal,dual_columns=dual,
                primal_slacks=primal_slacks,dual_slacks=dual_slacks,LP_runs=0,MIP_runs=0,
                original_source_program_runs=0,no_general_menu_or_half_claim=True)
    full=dict(summary=result,product_strategy=[dict(history=h,action=a) for h,a in sorted(pp.items(),key=lambda x:(len(x[0]),x[0]))],
              product_menu_endpoints=ZP,component0_kernel=K0,component1_kernel=K1,product_kernel=KP,query_rows=query_rows)
    (output/'full-result.json').write_text(json.dumps(enc(full),ensure_ascii=False,indent=2)+'\n')
    (output/'summary.json').write_text(json.dumps(enc(result),ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(enc(result),ensure_ascii=False,indent=2))


if __name__=='__main__':main()
