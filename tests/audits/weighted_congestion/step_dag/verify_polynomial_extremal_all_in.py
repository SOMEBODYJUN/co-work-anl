"""Exact finite literal-resource audit of the extremal-amplitude all-in state.

No numerical root is used. Small DAGs with integer q_D are selected by the
exact path equation, supplemented by edgeless graphs m=q(q-1). Fractions
verify the rational majorant B_d(q); logarithmic uniform bounds are proved
in the manuscript, not inferred from floating samples.
"""
from fractions import Fraction as F
from itertools import combinations, product
import json
import argparse
import hashlib
import platform
from pathlib import Path


def graph_data(n,edges):
    incoming=[[] for _ in range(n)]; outgoing=[[] for _ in range(n)]
    for u,v in edges: incoming[v].append(u); outgoing[u].append(v)
    ending=[[0]*(n+1) for _ in range(n)]
    for v in range(n):
        ending[v][1]=1
        for u in incoming[v]:
            for k in range(1,n): ending[v][k+1]+=ending[u][k]
    P=[sum(ending[v][k] for v in range(n)) for k in range(1,n+1)]
    c=[sum(row) for row in ending]
    return incoming,outgoing,P,c


def raw_poly(kind,d):
    a=[F(0) for _ in range(d+1)]
    if kind=='monomial': a[d]=1
    elif kind=='constant': a[0]=1
    elif kind=='mixed':
        for k in range(d+1): a[k]=F((k%3)+1)
    else: raise ValueError(kind)
    return a


def eval_poly(a,x): return sum((v*x**k for k,v in enumerate(a)),F(0))


def audit(n,edges,q,d,theta,kind):
    incoming,outgoing,P,c=graph_data(n,edges)
    assert 1+sum((F(p)*q**(-k-1) for k,p in enumerate(P)),F(0))==q
    h=[]
    for v in range(n): h.append((1+sum((h[u] for u in incoming[v]),F(0)))/q)
    T=sum(h,F(0)); assert T==q-1
    if theta=='uniform':
        assert not edges
        w=[F(1,n+1) for _ in range(n)]
    else: w=[theta/F(2)**(v+1) for v in range(n)]
    W=sum(w,F(0)); assert 0<W<1
    t=[sum((w[u] for u in outgoing[v]),F(0)) for v in range(n)]
    delta=[w[v]-t[v] for v in range(n)]
    assert all(x>0 for x in delta)
    assert W==sum((F(c[v])*delta[v] for v in range(n)),F(0))
    assert all(F(c[v])>=q*h[v] for v in range(n))
    mu=sum((h[v]*delta[v] for v in range(n)),F(0))
    assert mu<1/q
    # Each resource j uses polynomial a[j], and j+(n+1) its symmetric copy.
    core=raw_poly(kind,d); norm=eval_poly(core,F(1))
    a=[[x/norm for x in core]]
    for v in range(n):
        shape=raw_poly(kind,d); norm=eval_poly(shape,1+w[v])
        a.append([x*h[v]/norm for x in shape])
    a=a+a
    size=n+1
    strategies=[(tuple(range(size)),tuple(range(size,2*size)))]
    for v in range(n):
        strategies.append((tuple([0,size+v+1]+[u+1 for u in incoming[v]]),
                           tuple([size,v+1]+[size+u+1 for u in incoming[v]])))
    weights=[F(1)]+w
    state=[0]+[1]*n
    def cost(profile,i):
        loads=[F(0) for _ in range(2*size)]
        for j,choice in enumerate(profile):
            for e in strategies[j][choice]: loads[e]+=weights[j]
        return sum((eval_poly(a[e],loads[e]) for e in strategies[i][profile[i]]),F(0))
    root_now=cost(state,0); assert root_now==q
    moved=state.copy(); moved[0]=1
    root_new=cost(moved,0)
    leakage=sum((eval_poly(a[v+1],1+t[v]) for v in range(n)),F(0))
    assert root_new==eval_poly(a[0],1+W)+leakage
    assert root_new>=1+leakage
    lower1=sum((h[v]*(1+delta[v])**(-d) for v in range(n)),F(0))
    lower2=T*(1+mu/T)**(-d)
    lower3=T*(1+1/(q*T))**(-d)
    assert leakage>=lower1>=lower2>lower3
    B=q/(1+lower3)
    assert root_now<B*root_new
    worst_light=F(0)
    for v in range(n):
        now=cost(state,v+1)
        moved=state.copy(); moved[v+1]=0
        new=cost(moved,v+1)
        formula_now=eval_poly(a[0],W)+sum((eval_poly(a[u+1],t[u]) for u in incoming[v]),F(0))+h[v]
        formula_new=eval_poly(a[0],1+w[v])+sum((eval_poly(a[u+1],1+w[u]+w[v]) for u in incoming[v]),F(0))+eval_poly(a[v+1],w[v]+t[v])
        assert now==formula_now and new==formula_new
        assert now<=(q+1)*h[v] and new>=q*h[v]>0
        assert now<=(1+1/q)*new
        worst_light=max(worst_light,now/new)
    # The globally exchanged state has the same actual costs by direct check.
    exchanged=[1-x for x in state]
    assert all(cost(state,i)==cost(exchanged,i) for i in range(n+1))
    return {'n':n,'edges':edges,'q':str(q),'d':d,'weight_mode':str(theta),
            'kind':kind,'root_ratio':str(root_now/root_new),'B_d_q':str(B),
            'worst_light_ratio':str(worst_light)}


selected=[]
searched=0
for n in range(1,6):
    pairs=list(combinations(range(n),2))
    for bits in product((0,1),repeat=len(pairs)):
        edges=[e for e,b in zip(pairs,bits) if b]
        _,_,P,_=graph_data(n,edges)
        searched+=1
        for qi in range(2,7):
            q=F(qi)
            if 1+sum((F(p)*q**(-k-1) for k,p in enumerate(P)),F(0))==q:
                selected.append((n,edges,q))
# Large support and uniform-weight cases are explicit finite inputs.
selected += [(q*(q-1),[],F(q)) for q in (3,4,5)]
counts={'forward_DAGs_searched':searched,'selected_graphs':len(selected),
        'literal_games':0,'literal_deviations':0}
examples=[]
for n,edges,q in selected:
    for d in (1,2,5,10,20):
        for theta in (F(1,4),F(1,2),F(1)) + (() if edges else ('uniform',)):
            for kind in ('monomial','constant','mixed'):
                item=audit(n,edges,q,d,theta,kind)
                counts['literal_games']+=1
                counts['literal_deviations']+=n+1
                if len(examples)<4: examples.append(item)
result = {'status':'passed','arithmetic':'fractions.Fraction exact',
                  'parameters':{'topological_vertex_counts':[1,2,3,4,5],
                                'extra_empty_graph_q':[3,4,5],
                                'integer_q_candidates':[2,3,4,5,6],
                                'degrees':[1,2,5,10,20],
                                'weight_scales':['1/4','1/2','1','uniform for empty DAG'],
                                'polynomial_shapes':['monomial','constant','mixed'],
                                'seed':None,'randomization':'none; exhaustive finite products'},
                  'scope':'explicit actual state and all unilateral deviations; no arbitrary-degree inference from tests',
                  'counts':counts,'examples':examples}
result.update(python=platform.python_version(), code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
parser=argparse.ArgumentParser(description=__doc__)
group=parser.add_mutually_exclusive_group()
group.add_argument('--output',type=Path)
group.add_argument('--check',type=Path)
args=parser.parse_args()
if args.output:
    with args.output.open('x',encoding='utf-8') as f: json.dump(result,f,ensure_ascii=False,indent=2);f.write('\n')
elif args.check:
    assert json.loads(args.check.read_text()) == result, 'Recomputation differs from frozen record'
else: print(json.dumps(result,ensure_ascii=False,indent=2))
if args.output or args.check:print(json.dumps({k:result[k] for k in ('status','counts','code_sha256')}))
