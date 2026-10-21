#!/usr/bin/env python3
"""Independent exact-Fraction prototype for the nonnegative quote DP.
Not a production package; all claims about arbitrary inputs are proved in note.md.
"""
from fractions import Fraction as F
from itertools import product
from bisect import bisect_left
import random, json, hashlib, pathlib


def poly(coeffs, x):
    out=F(0)
    for a in reversed(coeffs): out=out*x+a
    return out


def tables(game):
    w,actions,resources=game
    factors=[]
    positives=[]
    U=F(0)
    for e,(coeffs,bg) in enumerate(resources):
        scope=tuple(i for i,A in enumerate(actions) if any(e in a for a in A))
        tab={}
        mx=F(0)
        for vals in product(*(range(len(actions[i])) for i in scope)):
            s=dict(zip(scope,vals))
            x=bg+sum((w[i] for i in scope if e in actions[i][s[i]]),F(0))
            quotes={}
            for i in scope:
                other=x-(w[i] if e in actions[i][s[i]] else 0)
                quotes[i]=tuple(poly(coeffs,other+w[i]) if e in a else F(0) for a in actions[i])
                for z in quotes[i]:
                    if z: positives.append(z);mx=max(mx,z)
            tab[vals]=(quotes,x*poly(coeffs,x))
        U+=mx
        factors.append((scope,tab))
    return factors, min(positives) if positives else None,U


def true_costs(game,s):
    w,actions,resources=game
    out=[]
    for i,A in enumerate(actions):
        row=[]
        for a in A:
            z=F(0)
            for e in a:
                coeff,bg=resources[e]
                x=bg+w[i]+sum((w[j] for j in range(len(w)) if j!=i and e in actions[j][s[j]]),F(0))
                z+=poly(coeff,x)
            row.append(z)
        out.append(row)
    return out


def welfare(game,s):
    w,actions,resources=game
    return sum(((x:=bg+sum((w[i] for i in range(len(w)) if e in actions[i][s[i]]),F(0)))*poly(coeff,x) for e,(coeff,bg) in enumerate(resources)),F(0))


def stable(game,s,beta):
    costs=true_costs(game,s)
    return all(row[s[i]]<=beta*z for i,row in enumerate(costs) for z in row)


def brute(game,beta):
    ans=[]
    for s in product(*(range(len(A)) for A in game[1])):
        if stable(game,s,beta):ans.append((welfare(game,s),s))
    return min(ans) if ans else None


def validate_td(game,bags,children):
    n=len(game[0]);edges=[]
    for t,C in enumerate(children):
        for u in C:edges.append((t,u))
    assert len(edges)==len(bags)-1
    assert set().union(*(set(b) for b in bags))==set(range(n))
    adj=[[] for _ in bags]
    for t,u in edges:adj[t].append(u);adj[u].append(t)
    for i in range(n):
        occ={t for t,b in enumerate(bags) if i in b};seen=set();stack=[next(iter(occ))]
        while stack:
            t=stack.pop()
            if t in seen:continue
            seen.add(t);stack.extend(u for u in adj[t] if u in occ)
        assert seen==occ


def solve(game,bags,children,beta,eps):
    validate_td(game,bags,children)
    factors,m,U=tables(game)
    if m is None:
        # Degenerate audit branch only; production uses ordinary factor DP.
        ans=brute(game,F(1));return ans[1],{'degenerate':True}
    T=len(bags);H=2*T;delta=eps/(4*H);D=(1+delta)**H
    assert D*D<=1+eps
    grid=[F(0),m]
    while grid[-1]<D*U:grid.append(grid[-1]*(1+delta))
    def rnd(x):return grid[bisect_left(grid,x)] if x else F(0)
    assigned=[[] for _ in bags]
    for scope,tab in factors:
        candidates=[t for t,b in enumerate(bags) if set(scope)<=set(b)]
        assert candidates,'factor clique missing from decomposition'
        assigned[candidates[0]].append((scope,tab))
    parents=[None]*T
    for t,C in enumerate(children):
        for u in C:parents[u]=t
    separators=[tuple(i for i in bags[t] if parents[t] is not None and i in bags[parents[t]]) for t in range(T)]
    counts=[];partial_counts=[]
    def improve(table,key,value):
        if key not in table or value[0]<table[key][0]:table[key]=value
    def visit(t):
        B=bags[t];I=separators[t];dims=[(i,a) for i in B for a in range(len(game[1][i]))]
        childmsgs=[(u,visit(u)) for u in children[t]]
        out={}
        for vals in product(*(range(len(game[1][i])) for i in B)):
            sigma=dict(zip(B,vals));local={i:[F(0)]*len(game[1][i]) for i in B};zlocal=F(0)
            for scope,tab in assigned[t]:
                quotes,z=tab[tuple(sigma[i] for i in scope)];zlocal+=z
                for i,row in quotes.items():
                    for a,x in enumerate(row):local[i][a]+=x
            r=tuple(rnd(local[i][a]) for i,a in dims)
            partial={r:(zlocal,dict(sigma))}
            for u,msg in childmsgs:
                J=separators[u];jdims=[(i,a) for i in J for a in range(len(game[1][i]))]
                suitable=[(rj,z,witness) for (acts,rj),(z,witness) in msg.items() if acts==tuple(sigma[i] for i in J)]
                nxt={}
                for oldr,(zold,wold) in partial.items():
                    for rj,zchild,wchild in suitable:
                        rmap=dict(zip(jdims,rj))
                        rnew=tuple(rnd(x+rmap.get(dim,F(0))) for dim,x in zip(dims,oldr))
                        both={**wold,**wchild}
                        assert all(both[i]==sigma[i] for i in B)
                        improve(nxt,rnew,(zold+zchild,both))
                partial=nxt;partial_counts.append(len(partial))
            for r,(z,witness) in partial.items():
                rmap=dict(zip(dims,r))
                if any(rmap[i,sigma[i]]>beta*D*rmap[i,a] for i in B if i not in I for a in range(len(game[1][i]))):continue
                key=(tuple(sigma[i] for i in I),tuple(rmap[i,a] for i in I for a in range(len(game[1][i]))))
                improve(out,key,(z,witness))
        counts.append(len(out));return out
    msg=visit(0)
    stats={'grid_size':len(grid),'max_message':max(counts),'H':H,'delta':str(delta),'D':str(D),'messages':counts,'max_partial':max(partial_counts,default=1)}
    if not msg:return None,stats
    z,witness=msg[((),())]
    s=tuple(witness[i] for i in range(len(game[0])))
    assert welfare(game,s)==z
    assert stable(game,s,beta*(1+eps))
    return s,stats


def random_star(rng,n):
    w=[F(rng.randint(1,5),rng.randint(1,3)) for _ in range(n)]
    actions=[[set(),set()] for _ in range(n)];resources=[]
    # shared center-leaf resources; each selected side may differ by player
    for leaf in range(1,n):
        e=len(resources);degree=rng.randint(1,4)
        coeff=[F(rng.randint(0,5),rng.randint(1,4)) for _ in range(degree+1)]
        resources.append((coeff,F(rng.randint(0,2),rng.randint(1,3))))
        actions[0][rng.randrange(2)].add(e);actions[leaf][rng.randrange(2)].add(e)
    # A distinct private constant resource in every action ensures distinct actions.
    for i in range(n):
        for a in range(2):
            e=len(resources);resources.append(([F(rng.randint(0,20),rng.randint(1,5))],F(0)));actions[i][a].add(e)
    bags=[(0,leaf) for leaf in range(1,n)]
    children=[list(range(1,n-1))]+[[] for _ in range(n-2)]
    return (w,actions,resources),bags,children


def run():
    rng=random.Random(20261021);records=[]
    for test in range(80):
        n=rng.randint(3,7);game,bags,children=random_star(rng,n)
        beta=[F(1),F(6,5),F(2)][test%3];eps=[F(1,2),F(1,4)][test%2]
        exact=brute(game,beta);s,stats=solve(game,bags,children,beta,eps)
        if exact is not None:
            assert s is not None
            assert welfare(game,s)<=exact[0]
        if s is not None:assert stable(game,s,beta*(1+eps))
        records.append({'test':test,'n':n,'beta':str(beta),'epsilon':str(eps),'beta_pne_exists':exact is not None,'output':list(s) if s is not None else None,'output_welfare':str(welfare(game,s)) if s is not None else None,'optimal_beta_welfare':str(exact[0]) if exact else None,**stats})
    # Zero-cost boundary. No cost ratios or positive lower bounds are taken here.
    zero=([F(1)]*3,[[{0},{1}],[{0},{2}],[{0},{3}]], [([F(0)],F(0)) for _ in range(4)])
    s,_=solve(zero,[(0,1,2)],[[]],F(1),F(1,2));assert stable(zero,s,F(1)) and welfare(zero,s)==0
    # Width-one two-player weighted quadratic game with no exact PNE.
    cyc=([F(1),F(2)],[[{0,2},{1}],[{0,1},{3}]], [([F(0),F(0),F(1)],F(0)),([F(0),F(9,2)],F(0)),([F(4)],F(0)),([F(71,4)],F(0))])
    assert brute(cyc,F(1)) is None
    assert all(not stable(cyc,s,F(101,100)) for s in product(range(2),repeat=2))
    no_s,no_stats=solve(cyc,[(0,1)],[[]],F(1),F(1,100));assert no_s is None
    relaxed_s,relaxed_stats=solve(cyc,[(0,1)],[[]],F(1),F(1,10))
    assert relaxed_s is not None and stable(cyc,relaxed_s,F(11,10))
    one=([F(1)],[[{0},{1}]], [([F(7)],F(0)),([F(0)],F(0))])
    zero_best,_=solve(one,[(0,)],[[]],F(1),F(1,2));assert zero_best==(1,)
    output={'status':'all assertions passed','seed':20261021,'random_star_cases':len(records),'source_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),'max_grid_size':max(r['grid_size'] for r in records),'max_message_size':max(r['max_message'] for r in records),'records':records,'zero_cost_boundary':'passed','positive_current_zero_alternative':'passed','width_one_no_pne_gap':{'epsilon_1_100':'correctly rejected','epsilon_1_10_output':list(relaxed_s),'epsilon_1_10_welfare':str(welfare(cyc,relaxed_s))}}
    path=pathlib.Path(__file__).with_name('quote_dp_audit.json');path.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k!='records'},ensure_ascii=False))

if __name__=='__main__':run()
