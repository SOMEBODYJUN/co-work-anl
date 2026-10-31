"""New literal-input reconstruction, not a replay of missing source programs."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import json
import sys

TYPES = [(1,3),(3,7),(5,1),(6,1),(11,1),(15,2),(14,1),
         (19,5),(20,2),(26,2),(28,10)]
PARAMETER_TYPE = 8
TARGET = (2,1,0,0,2)
NORMAL = (4,4,1,0,0)


def encode(x):
    if isinstance(x, F): return str(x)
    if isinstance(x, dict): return {str(k):encode(v) for k,v in x.items()}
    if isinstance(x, (tuple,list)): return [encode(v) for v in x]
    return x


def write(p, obj): p.write_text(json.dumps(encode(obj), ensure_ascii=False, indent=2)+'\n')


def add(q,a): return q[:a]+(q[a]+1,)+q[a+1:]


def tuples(n,total):
    if n==1:
        yield (total,)
    else:
        for first in range(total+1):
            for tail in tuples(n-1,total-first): yield (first,)+tail


def line(q,a):
    alpha=sum((F(w,sum(q[j] for j in range(5) if B>>j&1))
               for B,w in TYPES if B>>a&1),F())
    return alpha, F(1,q[3]) if a==3 else F()


def parameter_audit(output):
    terminal=list(tuples(5,5))
    affine={(q,a):line(q,a) for q in terminal for a in range(5) if q[a]}
    lines=sorted(set(affine.values()))
    cuts={F(0),F(1)}
    for (a,b),(c,d) in combinations(lines,2):
        if b!=d:
            t=(c-a)/(b-d)
            if 0<=t<=1: cuts.add(t)
    cuts=sorted(cuts)
    reps=sorted(set(cuts+[(a+b)/2 for a,b in zip(cuts,cuts[1:])]))
    assert len(lines)==211 and len(cuts)==65 and len(reps)==129
    all_rows=[]
    endpoint_sets={}
    certificates=[]
    total_states=0
    for t in reps:
        values={key:a+b*t for key,(a,b) in affine.items()}
        @lru_cache(None)
        def solve(q):
            if sum(q)==5: return frozenset([q]),None
            children=[solve(add(q,a))[0] for a in range(5)]
            threshold=max(min(values[z,a] for z in children[a]) for a in range(5))
            outcomes=frozenset(z for a in range(5) for z in children[a] if values[z,a]>=threshold)
            assert outcomes
            return outcomes,threshold
        root,threshold=solve((0,)*5)
        assert (TARGET in root)==(t>=F(3,4))
        assert threshold==(F(33,4) if t<F(3,4) else F(7))
        normal_ok=True
        q=(0,)*5
        for a in NORMAL:
            if TARGET not in solve(add(q,a))[0] or values[TARGET,a]<solve(q)[1]: normal_ok=False
            q=add(q,a)
        assert normal_ok==(t>=F(3,4))
        all_rows.append(dict(t=t,is_cut=t in cuts,root_outcomes=sorted(root),threshold=threshold,
                             target_in_root=TARGET in root,normal_order_realizable=normal_ok))
        if t in (F(0),F(1,2),F(3,4),F(1)):
            endpoint_sets[str(t)]=sorted(root)
        if t==0:
            short=[]
            for a in range(3):
                for c in range(2):
                    q=(a,c,0,0,1)
                    forced=solve(add(q,2))[0]
                    assert forced==frozenset([(2,1,1,0,1)])
                    profit=min(values[z,2] for z in forced)
                    assert profit==F(47,6)>values[TARGET,4]==F(46,6)
                    short.append(dict(prefix=q,D_outcomes=sorted(forced),D_profit=profit,
                                      target_F_profit=values[TARGET,4]))
            write(output/'deletion-six-prefix-cut.json',short)
        if t in (F(3,4),F(1)):
            policy={}
            def build(h,q,target):
                if len(h)==5: return
                threshold=solve(q)[1]
                candidates=[a for a in range(5) if target in solve(add(q,a))[0] and values[target,a]>=threshold]
                assert candidates
                a=NORMAL[len(h)] if h==NORMAL[:len(h)] else candidates[0]
                assert a in candidates
                policy[h]=a
                for b in range(5):
                    child_target=target if b==a else min(solve(add(q,b))[0],key=lambda z:(values[z,b],z))
                    build(h+(b,),add(q,b),child_target)
            build((),(0,)*5,TARGET)
            def leaf(h):
                h=tuple(h)
                while len(h)<5: h=h+(policy[h],)
                return tuple(h.count(j) for j in range(5))
            comparisons=0
            for h,a in policy.items():
                chosen=values[leaf(h),a]
                for b in range(5):
                    assert chosen>=values[leaf(h+(b,)),b]
                    comparisons+=1
            assert len(policy)==781 and comparisons==3905 and leaf(())==TARGET
            name='complete-strategy-t-'+str(t).replace('/','-')+'.json'
            write(output/name,dict(t=t,normal_actions=NORMAL,terminal=TARGET,
                                   decision_histories=len(policy),IC_including_self=comparisons,
                                   policy=[dict(history=h,action=a) for h,a in sorted(policy.items(),key=lambda x:(len(x[0]),x[0]))]))
            certificates.append(dict(t=t,path=name,nodes=len(policy),IC_including_self=comparisons))
        total_states+=solve.cache_info().currsize
    write(output/'parameter-partition.json',dict(affine_lines=lines,cuts=cuts,representatives=all_rows))
    # Literal last-node switch and integer scaling, distinct from all-parameter proof.
    for k in range(1,31):
        q=4*k+1
        assert F(3*k+1,q)>F(3,4)>F(3*k,q)
        assert (3*k+1)-F(3,4)*q==F(1,4)
        assert 3*k-F(3,4)*q==F(-3,4)
        assert F(33,4)*q-7*q==F(5,4)*q
    return dict(literal_covered_customers=sum(w for B,w in TYPES),terminal_count_vectors=len(terminal),
                affine_lines=len(lines),cuts=len(cuts),representatives=len(reps),
                all_target_and_threshold_checks=True,root_endpoint_sets=endpoint_sets,
                complete_strategy_certificates=certificates,all_count_states=total_states,
                scaling_k_checked=[1,30],original_program_replays=0)


def reentry_audit():
    # T,B disjoint; all customers are expanded as distinct integer IDs.
    topics1=(frozenset(range(2)),frozenset([2]))
    topics2=(frozenset(range(3,5)),frozenset(range(5,7)))
    def p1(h): return 1 if not h else 0
    def p2(h): return 0 if not h else 1-h[0]
    prod=tuple(a|b for a,b in product(topics1,topics2))
    def pp(h):
        if not h: return 2  # (B,T)
        a,b=divmod(h[0],2)
        return 2*p1((a,))+p2((b,))
    def utility(topics,sequence,position):
        return sum((F(1,sum(x in topics[a] for a in sequence)) for x in topics[sequence[position]]),F())
    def run(topics,policy,forced):
        h=()
        for pos in range(2): h=h+(forced[pos] if pos in forced else policy(h),)
        return h
    def query(topics,h,chosen):
        return sum((F(1,1+sum(x in topics[a] for a in h)) for x in topics[chosen]),F())
    rows=0
    prices=[]
    for topics,policy in ((topics1,p1),(topics2,p2),(prod,pp)):
        for h in [()]+[(a,) for a in range(len(topics))]:
            prescribed=run(topics,policy,{0:h[0]} if h else {})
            chosen=utility(topics,prescribed,len(h))
            for a in range(len(topics)):
                forced={0:h[0]} if h else {}
                forced[len(h)]=a
                assert chosen>=utility(topics,run(topics,policy,forced),len(h))
                rows+=1
        by_J={}
        for J in ((),(0,),(1,),(0,1)):
            endpoints={run(topics,policy,dict(zip(J,actions))) for actions in product(range(len(topics)),repeat=len(J))}
            by_J[J]=endpoints
        assert by_J[()]<=by_J[(0,)]<=by_J[(0,1)]
        assert by_J[()]<=by_J[(1,)]<=by_J[(0,1)]
        prices.append([min(query(topics,h,0) for h in by_J[J]) for J in ((0,),(1,),(0,1))])
    assert prices==[[F(2,3),F(1),F(2,3)],[F(1),F(2,3),F(2,3)],[F(5,3),F(5,3),F(4,3)]]
    return dict(unit_customers=7,component_and_product_IC_including_self=rows,
                query='component T / product (T,T)',prices=prices,
                product_root=[1,0],product_W=7,product_W_over_m=F(7,2),
                fixed_query_not_minimax=True)


def main():
    output=Path(sys.argv[1]);assert output.is_dir() and not list(output.iterdir())
    result=dict(kind='new-literal-definition-reconstruction-not-original-replay',
                deletion=parameter_audit(output),reentry=reentry_audit(),
                input_from_fully_read_markdown=True,external_input_files=0,
                libraries='Python standard library only')
    write(output/'result.json',result)
    print(json.dumps(encode(result),ensure_ascii=False,indent=2))


if __name__=='__main__': main()
