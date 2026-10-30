#!/usr/bin/env python3
"""Literal complete-anchor-gate audit of class endpoint quote DP (FQDP)."""
from fractions import Fraction as F
from itertools import product,combinations
from bisect import bisect_left
from pathlib import Path
import random,json,hashlib
from quote_dp_audit import poly, true_costs, welfare, stable, brute


def front(bits):return sum(x!=y for x,y in zip(bits,bits[1:]))<=1

def front_domain(n):return tuple(bits for bits in product(range(2),repeat=n) if front(bits))

def endpoints(bits):
    out=[]
    for i in range(len(bits)):
        nxt=list(bits);nxt[i]^=1
        if front(nxt):out.append(i)
    assert 1<=len(out)<=2
    return out


def build(rng,sizes,beta):
    starts=[];N=0;classes=[]
    for n in sizes:starts.append(N);classes.append(tuple(range(N,N+n)));N+=n
    weights_by_class=[F(a+1) for a in range(len(sizes))]
    weights=[weights_by_class[a] for a,n in enumerate(sizes) for _ in range(n)]
    acts=[[set(),set()] for _ in weights];res=[]
    # Cross-class base resources, only between consecutive classes.
    for a in range(len(sizes)-1):
        e=len(res);degree=rng.randint(1,3)
        coeff=[F(rng.randint(0,3),rng.randint(1,5)) for _ in range(degree+1)]
        res.append((coeff,F(0)))
        for aa in (a,a+1):
            for i in classes[aa]:
                if rng.randrange(3):acts[i][rng.randrange(2)].add(e)
    # Independent, distinct private action labels, costs can be zero.
    for i in range(N):
        for bit in range(2):
            e=len(res);res.append(([F(rng.randint(0,5),rng.randint(1,3))],F(0)));acts[i][bit].add(e)
    Ebase=len(res);potential=[]
    for e in range(Ebase):potential.append(sum((weights[i] for i in range(N) if any(e in a for a in acts[i])),F(0)))
    B=[]
    for cl in classes:
        B.append(max(sum((poly(res[e][0],potential[e]) for e in acts[i][0]|acts[i][1]),F(0)) for i in cl))
    gate_cert=[]
    for a,cl in enumerate(classes):
        n=len(cl);L=(n-1)*(n-2)//2;gate_degree=12
        v=4*beta*(B[a]+1);wa=weights_by_class[a]
        u=v*F(2,3)**gate_degree
        assert v>beta*(B[a]+L*u)
        gate_cert.append({'B':str(B[a]),'L':L,'v':str(v),'u':str(u),'RD_margin':str(v-beta*(B[a]+L*u))})
        coeff=[F(0)]*gate_degree+[v/(3*wa)**gate_degree]
        for j,k in combinations(range(1,n),2):
            pair=[]
            for side in range(2):pair.append(len(res));res.append((coeff,F(0)))
            for pos,xor in ((0,0),(j,1),(k,0)):
                i=cl[pos]
                for bit in range(2):acts[i][bit].add(pair[bit^xor])
    return (weights,acts,res),classes,gate_cert


def local_factors(game,classes,domains):
    w,acts,res=game;classof={i:a for a,cl in enumerate(classes) for i in cl};posof={i:j for cl in classes for j,i in enumerate(cl)}
    factors=[]
    for e,(coeff,bg) in enumerate(res):
        users=[i for i in range(len(w)) if any(e in a for a in acts[i])]
        scope=tuple(sorted({classof[i] for i in users}));tab={}
        for vals in product(*(range(len(domains[a])) for a in scope)):
            ds=dict(zip(scope,vals));bits={i:domains[a][ds[a]][posof[i]] for a in scope for i in classes[a]}
            x=bg+sum((w[i] for i in users if e in acts[i][bits[i]]),F(0));quotes={}
            for a in scope:
                out=[]
                for pos in endpoints(domains[a][ds[a]]):
                    i=classes[a][pos];oldbit=bits[i];oldinc=e in acts[i][oldbit];newinc=e in acts[i][oldbit^1]
                    old=poly(coeff,x) if oldinc else F(0)
                    new=poly(coeff,x+w[i]*(newinc-oldinc)) if newinc else F(0)
                    out.extend((old,new))
                quotes[a]=tuple(out+[F(0)]*(4-len(out)))
            tab[vals]=(quotes,x*poly(coeff,x))
        factors.append((scope,tab))
    return factors


def solve(domains,factors,bags,children,beta,eps):
    T=len(bags);H=2*T;delta=eps/(4*H);D=(1+delta)**H
    pos=[x for scope,tab in factors for quotes,z in tab.values() for row in quotes.values() for x in row if x]
    assert pos
    m=min(pos);U=sum((max((x for quotes,z in tab.values() for row in quotes.values() for x in row),default=F(0)) for scope,tab in factors),F(0))
    grid=[F(0),m]
    while grid[-1]<D*U:grid.append(grid[-1]*(1+delta))
    def rnd(x):return grid[bisect_left(grid,x)] if x else F(0)
    assigned=[[] for _ in bags]
    for scope,tab in factors:
        t=next(t for t,b in enumerate(bags) if set(scope)<=set(b));assigned[t].append((scope,tab))
    parent=[None]*T
    for t,chs in enumerate(children):
        for u in chs:parent[u]=t
    sep=[tuple(a for a in bags[t] if parent[t] is not None and a in bags[parent[t]]) for t in range(T)]
    sizes=[];psizes=[]
    def keep(table,key,val):
        if key not in table or val[0]<table[key][0]:table[key]=val
    def visit(t):
        B=bags[t];I=sep[t];dims=[(a,c) for a in B for c in range(4)];childmsgs=[(u,visit(u)) for u in children[t]];out={}
        for vals in product(*(range(len(domains[a])) for a in B)):
            sigma=dict(zip(B,vals));loc={a:[F(0)]*4 for a in B};zloc=F(0)
            for scope,tab in assigned[t]:
                quotes,z=tab[tuple(sigma[a] for a in scope)];zloc+=z
                for a,row in quotes.items():
                    for c,x in enumerate(row):loc[a][c]+=x
            rr=tuple(rnd(loc[a][c]) for a,c in dims);part={rr:(zloc,dict(sigma))}
            for u,msg in childmsgs:
                J=sep[u];jdims=[(a,c) for a in J for c in range(4)]
                suitable=[(r,z,wit) for (ds,r),(z,wit) in msg.items() if ds==tuple(sigma[a] for a in J)];nxt={}
                for r,(z,wit) in part.items():
                    for cr,cz,cwit in suitable:
                        crmap=dict(zip(jdims,cr));nr=tuple(rnd(x+crmap.get(dim,F(0))) for dim,x in zip(dims,r));nw={**wit,**cwit}
                        assert all(nw[a]==sigma[a] for a in B);keep(nxt,nr,(z+cz,nw))
                part=nxt;psizes.append(len(part))
            for r,(z,wit) in part.items():
                rm=dict(zip(dims,r))
                if any(rm[a,2*l]>beta*D*rm[a,2*l+1] for a in B if a not in I for l in range(2)):continue
                key=(tuple(sigma[a] for a in I),tuple(rm[a,c] for a in I for c in range(4)));keep(out,key,(z,wit))
        sizes.append(len(out));return out
    root=visit(0);stats={'grid':len(grid),'message_max':max(sizes),'partial_max':max(psizes,default=1),'D':str(D),'H':H}
    if not root:return None,stats
    z,ds=root[((),())];return (tuple(ds[a] for a in range(len(domains))),z),stats


def run():
    rng=random.Random(774621);records=[]
    layouts=[(3,3),(4,3),(3,4),(3,3,3),(3,4,3)]
    for test in range(15):
        sizes=layouts[test%len(layouts)];beta=[F(1),F(6,5),F(2)][test%3];eps=F(1,4)
        game,classes,cert=build(rng,sizes,beta);domains=[front_domain(n) for n in sizes];factors=local_factors(game,classes,domains)
        bags=[(a,a+1) for a in range(len(sizes)-1)];children=[[t+1] if t+1<len(bags) else [] for t in range(len(bags))]
        result,stats=solve(domains,factors,bags,children,beta,eps)
        full=brute(game,beta)
        front_best=None;front_count=0
        for ds in product(*(range(len(D)) for D in domains)):
            bits=tuple(bit for a,d in enumerate(ds) for bit in domains[a][d])
            if stable(game,bits,beta):
                front_count+=1;val=(welfare(game,bits),bits)
                if front_best is None or val<front_best:front_best=val
        assert full==front_best,'RD did not exclude every nonfront beta equilibrium'
        if full is not None:assert result is not None
        if result:
            ds,z=result;s=tuple(bit for a,d in enumerate(ds) for bit in domains[a][d])
            assert z==welfare(game,s)
            assert stable(game,s,beta*(1+eps))
            if full:assert z<=full[0]
        else:s=None;z=None
        records.append({'test':test,'class_sizes':sizes,'players':sum(sizes),'resources':len(game[2]),'beta':str(beta),'epsilon':str(eps),'beta_pne_count_front':front_count,'full_original_opt_beta':str(full[0]) if full else None,'output_bits':s,'output_W':str(z) if z is not None else None,'RD_certificates':cert,**stats})
    out={'status':'all assertions passed','seed':774621,'literal_cases':len(records),'full_original_state_checks':sum(2**r['players'] for r in records),'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'quote_dp_helper_sha256':hashlib.sha256(Path(__file__).with_name('quote_dp_audit.py').read_bytes()).hexdigest(),'records':records}
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='records'},ensure_ascii=False))

if __name__=='__main__':run()
