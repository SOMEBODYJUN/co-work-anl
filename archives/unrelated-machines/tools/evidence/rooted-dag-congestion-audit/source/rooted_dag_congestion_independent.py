"""Independent exact audit of the DAG congestion-certificate extraction.

The circulation constructor and edge-subset oracle do not import the canonical
solver. main() additionally cross-checks the canonical public extract interface
against the independent graph verifier. Default JSON is sent only to stdout.
"""
from fractions import Fraction as F
from collections import deque
from itertools import product, combinations
import hashlib,json,random,platform
from pathlib import Path

def bounded_flow(arcs):
    # Independent circulation reduction, integer Edmonds-Karp.
    labels=sorted({x for u,v,l,c in arcs for x in (u,v)})
    ids={x:i for i,x in enumerate(labels)}
    N=len(labels); ss=N; tt=N+1; adj=[[] for _ in range(N+2)]; bal=[0]*N
    def edge(u,v,c):
        a=[v,c,len(adj[v])]; b=[u,0,len(adj[u])]
        adj[u].append(a); adj[v].append(b)
        return (u,len(adj[u])-1,c)
    refs=[]
    for u,v,l,c in arcs:
        assert 0<=l<=c
        a,b=ids[u],ids[v]; refs.append(edge(a,b,c-l)); bal[a]-=l;bal[b]+=l
    need=0
    for v,b in enumerate(bal):
        if b>0: edge(ss,v,b);need+=b
        elif b<0:edge(v,tt,-b)
    total=0
    while True:
        par=[None]*(N+2);par[ss]=(-1,-1);q=deque([ss])
        while q and par[tt] is None:
            u=q.popleft()
            for i,e in enumerate(adj[u]):
                if e[1] and par[e[0]] is None:
                    par[e[0]]=(u,i);q.append(e[0])
        if par[tt] is None:break
        v=tt;delta=need-total
        while v!=ss:
            u,i=par[v];delta=min(delta,adj[u][i][1]);v=u
        v=tt
        while v!=ss:
            u,i=par[v];e=adj[u][i];e[1]-=delta;adj[v][e[2]][1]+=delta;v=u
        total+=delta
    if total!=need:return None
    return [l+c-adj[u][i][1] for (u,i,c),(a,b,l,h) in zip(refs,arcs)]

def construct(n,E,k,K,r=0):
    if k[r]==0:return {r},[]
    d=[0]*n
    for u,v in E:d[u]+=1
    arcs=[];edge_indices=[];s='s';t='t'
    add=lambda u,v,l,c:arcs.append((u,v,l,c))
    for v in range(n):
        vi=f'i{v}';vo=f'o{v}';vg=f'g{v}'
        if v!=r:add(vi,vo,0,1)
        if k[v]==0:add(vo,t,0,1)
        elif k[v]>=K:
            add(s,vo,0,d[v]);add(vo,vg,k[v]//K,d[v])
        elif v==r:add(s,vo,1,d[v])
    for u,v in E:
        edge_indices.append(len(arcs));add(f'g{u}' if k[u]>=K else f'o{u}',f'i{v}',0,1)
    add(t,s,0,max(1,sum(d)+n))
    answer=bounded_flow(arcs)
    if answer is None:raise AssertionError(('network infeasible',n,E,k,K))
    used=[e for e,i in zip(E,edge_indices) if answer[i]]
    reached={r}
    changed=True
    while changed:
        changed=False
        for u,v in used:
            if u in reached and v not in reached:reached.add(v);changed=True
    H=[(u,v) for u,v in used if u in reached]
    ind={v:0 for v in reached};out={v:0 for v in reached}
    for u,v in H:ind[v]+=1;out[u]+=1
    assert all(ind[v]==(0 if v==r else 1) for v in reached)
    assert all(out[v]*(2*K-1)>=k[v] for v in reached if k[v]>0)
    return reached,H

def valid_certificate(n,E,k,K,f,r=0):
    if K<=0:return False
    indeg=[F(0)]*n;out=[F(0)]*n;din=[0]*n;dout=[0]*n
    for (u,v),a in zip(E,f):
        if a<0:return False
        out[u]+=a;indeg[v]+=a;din[v]+=1;dout[u]+=1
    if din[r]:return False
    for v in range(n):
        if k[v]==0 and dout[v]:return False
        if k[v]>=K:
            if out[v]<k[v] or indeg[v]>K:return False
        elif k[v]>0:
            if v==r:
                if out[v]<K:return False
            elif out[v]!=indeg[v] or indeg[v]>K:return False
        elif indeg[v]>K:return False
    return True

def all_trees(n,E,r=0):
    trees=[]
    for bits in product((0,1),repeat=len(E)):
        use=[e for e,b in zip(E,bits) if b]
        seen={r}
        for _ in range(n):
            seen.update(v for u,v in use if u in seen)
        if any(u not in seen or v not in seen for u,v in use):continue
        indeg=[0]*n;out=[0]*n
        for u,v in use:indeg[v]+=1;out[u]+=1
        if any(indeg[v]!=(0 if v==r else 1) for v in seen):continue
        trees.append((seen,out))
    return trees

def brute_score(trees,k):
    return max(min([F(1)]+[F(out[v],k[v]) for v in seen if k[v]]) for seen,out in trees)

def verify_tree(n,E,k,K,H,r=0,W=None):
    allowed=set(E)
    assert len(H)==len(set(H)) and all(e in allowed for e in H)
    W=set(range(n)) if W is None else set(W)
    assert r in W and all(u in W and v in W for u,v in H)
    indeg=[0]*n;out=[0]*n
    for u,v in H:indeg[v]+=1;out[u]+=1
    assert indeg[r]==0 and max(indeg)<=1
    seen={r}
    for _ in range(n):seen.update(v for u,v in H if u in seen)
    assert all(u in seen and v in seen for u,v in H)
    assert len(H)==len(seen)-1
    score=min([F(1)]+[F(out[v],k[v]) for v in seen if k[v]])
    assert score>=F(1,2*K-1)
    return score


def main():
    # The oracle above remains independent. This import is only for a public-
    # interface cross-check; none of its validation/score helpers are imported.
    from rooted_dag_congestion_flow import extract, find_certificate, min_certificate
    crosschecks=0
    def crosscheck(n,E,k,K,f,r=0,W=None):
        nonlocal crosschecks
        if W is None:W=list(range(n))
        flow=dict(zip(E,f))
        H=extract(n,E,k,K,W,flow,r)
        verify_tree(n,E,k,K,H,r,W)
        crosschecks+=1
        return H
    stats={'certificate_cases':0,'distinct_object_cases':0,'fractional_cases':0,'huge_K_cases':0,'root_labels':0}
    observed=set();rng=random.Random(792148)
    # Exhaust all topologically labeled DAGs through 4 vertices, K=1,2, and
    # every integral flow per edge in 0..K. Derive all compatible positive demands.
    for n in range(1,5):
        full=list(combinations(range(n),2))
        for mask in product((0,1),repeat=len(full)):
            E=[e for e,b in zip(full,mask) if b]
            trees=all_trees(n,E);d=[0]*n
            for u,v in E:d[u]+=1
            for K in (1,2):
                for fs in product(range(K+1),repeat=len(E)):
                    ins=[0]*n;outs=[0]*n
                    for (u,v),a in zip(E,fs):outs[u]+=a;ins[v]+=a
                    opts=[]
                    for v in range(n):
                        z=[]
                        if d[v]==0 and ins[v]<=K:z.append(0)
                        if v==0 and outs[v]>=K:z+=list(range(1,K))
                        if v!=0 and ins[v]==outs[v]<=K:z+=list(range(1,K))
                        if ins[v]<=K:z+=list(range(K,outs[v]+1))
                        opts.append(z)
                    for k in product(*opts):
                        if not k[0]:continue
                        assert valid_certificate(n,E,k,K,fs)
                        construct(n,E,k,K)
                        crosscheck(n,E,k,K,fs)
                        stats['certificate_cases']+=1
                        key=(n,tuple(E),k,K)
                        if key not in observed:
                            assert brute_score(trees,k)>=F(1,2*K-1)
                            observed.add(key)
    stats['distinct_object_cases']=len(observed)
    # Exact rational corridors, merges, non-root B sources, and arbitrary root labels.
    for K in (2,3,7,10**100+39):
        for trial in range(60):
            E=[(0,1),(0,2),(1,3),(2,3),(3,4),(3,5)]
            # small root emits K; balanced merge receives K and emits K.
            f=[F(K,2),F(K,2),F(K,2),F(K,2),F(K,3),F(2*K,3)]
            k=(K-1,1,1,1,0,0)
            assert valid_certificate(6,E,k,K,f)
            construct(6,E,k,K)
            crosscheck(6,E,k,K,f)
            stats['fractional_cases']+=1
            if K>10**20:stats['huge_K_cases']+=1
            perm=list(range(6));rng.shuffle(perm)
            Er=[(perm[u],perm[v]) for u,v in E];kr=[0]*6
            for v in range(6):kr[perm[v]]=k[v]
            assert valid_certificate(6,Er,kr,K,f,r=perm[0])
            construct(6,Er,kr,K,r=perm[0]);crosscheck(6,Er,kr,K,f,r=perm[0]);stats['root_labels']+=1
    # Unreachable B component, each independently creates outgoing demand.
    E=[(0,1),(2,3)];k=(2,0,2,0);f=(2,2)
    assert valid_certificate(4,E,k,2,f)
    assert construct(4,E,k,2)[0]=={0,1}
    crosscheck(4,E,k,2,f)
    stats['unreachable_case']=1
    # Sharp obstruction for K: root k=2K-1, 2K-1 tiny corridors sharing K terminals.
    sharp=[]
    for K in range(1,6):
        branches=2*K-1;terms=K;n=1+branches+terms
        E=[(0,v) for v in range(1,branches+1)]+[(v,1+branches+j) for v in range(1,branches+1) for j in range(terms)]
        k=(branches,)+(1,)*branches+(0,)*terms
        f=[F(1)]*branches+[F(1,K)]*(branches*terms)
        assert valid_certificate(n,E,k,K,f)
        nodes,H=construct(n,E,k,K)
        crosscheck(n,E,k,K,f)
        # Real maximum root degree K, hence b*=K/(2K-1), not theorem sharpness.
        sharp.append({'K':K,'tree_nodes':len(nodes),'root_degree':sum(u==0 for u,v in H)})
    stats['shared_resource_examples']=sharp
    # Independent arithmetic audit of the layered sharpness construction.
    width_cases=0
    for K in list(range(2,10001))+[10**100+39,10**300+27]:
        h=(K-1).bit_length();d=h+1;k=2*K-1;ws=[1]
        for layer in range(d):
            ws.append((k*ws[-1]+K-1)//K)
        assert ws[:-1]==[2**layer for layer in range(d)]
        assert ws[-1]==2**d-1
        assert all(k*a<=K*b for a,b in zip(ws,ws[1:]))
        assert all(k*a>K*(b-1) for a,b in zip(ws,ws[1:]))
        width_cases+=1
    stats['sharp_width_cases']=width_cases
    sharp_graphs=[]
    for K in range(2,19):
        h=(K-1).bit_length();widths=[2**l for l in range(h+1)]+[2**(h+1)-1]
        layers=[];nv=0
        for w in widths:layers.append(list(range(nv,nv+w)));nv+=w
        E=[(u,v) for A,B in zip(layers,layers[1:]) for u in A for v in B]
        k=[2*K-1]*(nv-widths[-1])+[0]*widths[-1]
        f=[F(2*K-1,len(B)) for A,B in zip(layers,layers[1:]) for u in A for v in B]
        assert valid_certificate(nv,E,k,K,f)
        vs,H=construct(nv,E,k,K)
        assert verify_tree(nv,E,k,K,crosscheck(nv,E,k,K,f))==F(1,2*K-1)
        deg=[0]*nv
        for u,v in H:deg[u]+=1
        score=min([F(1)]+[F(deg[v],k[v]) for v in vs if k[v]])
        assert score==F(1,2*K-1)
        sharp_graphs.append({'K':K,'vertices':nv,'edges':len(E),'score':str(score)})
    stats['sharp_explicit_graphs']=sharp_graphs
    # Outside-W huge dead B is intentionally unconstrained by the certificate.
    crosscheck(3,[(0,1)],[1,0,10**100],2,[2],W=[0,1])
    # Zero root, empty graph, positive dead-root rejection in the canonical API.
    crosscheck(1,[],[0],10**100,[])
    for K in (1,2,10**100):
        try:extract(1,[],[1],K,[0],{})
        except ValueError:pass
        else:raise AssertionError('positive dead root accepted')
    # Fixed W,K search is checked against exhaustive original-edge integer
    # certificate enumeration, rather than either flow implementation.
    finder_cases=feasible_finder=monotonic_pairs=0
    finder_cache={}
    for n in range(1,4):
        full=list(combinations(range(n),2))
        for ebits in product((0,1),repeat=len(full)):
            E=[e for e,b in zip(full,ebits) if b]
            for k in product(range(4),repeat=n):
                if any(k[u]==0 for u,v in E):continue
                for wbits in product((0,1),repeat=n-1):
                    W=[0]+[v for v,b in zip(range(1,n),wbits) if b]
                    remap={v:i for i,v in enumerate(W)}
                    Ew=[e for e in E if e[0] in remap and e[1] in remap]
                    Es=[(remap[u],remap[v]) for u,v in Ew]
                    ks=[k[v] for v in W]
                    feasible_by_K=[]
                    for K in range(1,max(k)+2):
                        oracle=any(valid_certificate(len(W),Es,ks,K,fs)
                                   for fs in product(range(K+1),repeat=len(Es)))
                        found=find_certificate(n,E,k,K,W)
                        assert (found is not None)==oracle
                        if found is not None:
                            assert all(type(a) is int for a in found.values())
                            assert valid_certificate(len(W),Es,ks,K,
                                                     [found.get(e,0) for e in Ew])
                            H=extract(n,E,k,K,W,found)
                            verify_tree(n,E,k,K,H,W=W)
                            feasible_finder+=1
                        feasible_by_K.append(oracle);finder_cases+=1
                    expected_min=next((i+1 for i,b in enumerate(feasible_by_K) if b),None)
                    minimum=min_certificate(n,E,k,W)
                    assert (None if minimum is None else minimum[0])==expected_min
                    if minimum is not None:
                        mk,mf=minimum
                        assert valid_certificate(len(W),Es,ks,mk,[mf.get(e,0) for e in Ew])
                    assert feasible_by_K==sorted(feasible_by_K)
                    monotonic_pairs+=max(0,len(feasible_by_K)-1)
                    finder_cache[(n,tuple(E),k,tuple(W))]=feasible_by_K
    stats['fixed_support_finder_cases']=finder_cases
    stats['fixed_support_feasible_cases']=feasible_finder
    stats['fixed_support_monotonic_adjacent_pairs']=monotonic_pairs
    stats['fixed_support_object_cases']=len(finder_cache)
    # Huge binary supplies exercise the capacity-independent search interface.
    for K in (10**100+39,10**300+27):
        for E,k in [([(0,1),(0,2)],[2*K-1,0,0]),
                    ([(0,1),(1,2)],[1,1,0])]:
            got=find_certificate(3,E,k,K,list(range(3)))
            assert got is not None
            assert valid_certificate(3,E,k,K,[got.get(e,0) for e in E])
            verify_tree(3,E,k,K,extract(3,E,k,K,list(range(3)),got))
    stats['huge_binary_finder_cases']=4
    for K in (10**100+39,10**300+27):
        mk,mf=min_certificate(3,[(0,1),(0,2)],[2*K-1,0,0],[0,1,2])
        assert mk==K
        mk,mf=min_certificate(2,[],[0,K],[0,1])
        assert mk==K+1 and mf=={}
    stats['huge_binary_minimum_cases']=4
    stats['minimum_finder_oracle_cases']=len(finder_cache)
    # Activation-corridor LP family, reconstructed from its definition only.
    activation_rows=[]
    for q in range(2,26):
        E=[];k=[1];a=[F(1)];x={};branches=[]
        def vertex(demand,activation):
            k.append(demand);a.append(activation);return len(k)-1
        def arc(u,v,value):E.append((u,v));x[u,v]=value
        for i in range(q):
            v=vertex(q,F(1,q));arc(0,v,F(1,q))
            ws=[vertex(1,F(1,q)) for j in range(q)]
            z=vertex(1,F(1));t=vertex(0,F(1))
            for w in ws:arc(v,w,F(1,q));arc(w,z,F(1,q))
            arc(z,t,F(1));branches.append((v,ws,z,t))
        n=len(k);ins=[F(0)]*n;outs=[F(0)]*n
        for u,v in E:
            assert 0<=x[u,v]<=a[u]
            ins[v]+=x[u,v];outs[u]+=x[u,v]
        assert a[0]==1
        assert all(a[v]==ins[v]<=1 for v in range(1,n))
        assert all(outs[v]>=k[v]*a[v] for v in range(n) if k[v])
        assert n==1+q*(q+3) and len(E)==2*q*q+2*q
        v,ws,z,t=branches[0];path=[(0,v),(v,ws[0]),(ws[0],z),(z,t)]
        assert verify_tree(n,E,k,q,path)==F(1,q)
        optimum=None
        if q==2:
            optimum=brute_score(all_trees(n,E),k)
            assert optimum==F(1,q)
        activation_rows.append({'q':q,'vertices':n,'edges':len(E),
                                'path_score':str(F(1,q)),
                                'edge_subset_oracle_optimum':None if optimum is None else str(optimum)})
    stats['activation_corridor_cases']=activation_rows
    # Given an actual positive-score tree, independently construct the strong
    # certificate for every tested K >= ceil(1/b). This does not search for H.
    tree_certificate_cases=0
    for n in range(1,6):
        full=list(combinations(range(n),2))
        for ebits in product((0,1),repeat=len(full)):
            H=[e for e,b in zip(full,ebits) if b]
            try:verify_tree(n,full,[0]*n,1,H)
            except AssertionError:continue
            seen={0}|{v for e in H for v in e}
            kids=[[] for _ in range(n)]
            for u,v in H:kids[u].append(v)
            internal=[v for v in seen if kids[v]]
            for demands in product((1,2,3,10**100+39),repeat=len(internal)):
                k=[0]*n
                for v,z in zip(internal,demands):k[v]=z
                beta=min([F(1)]+[F(len(kids[v]),k[v]) for v in internal])
                threshold=(beta.denominator+beta.numerator-1)//beta.numerator
                for K in sorted({threshold,threshold+1,max(threshold,10**100+39)}):
                    f={};incoming=[0]*n
                    for v in range(n):
                        if not k[v]:continue
                        target=k[v] if k[v]>=K else K if v==0 else incoming[v]
                        if k[v]>=K:
                            for w in kids[v]:
                                amount=min(target,K);target-=amount
                                f[v,w]=amount;incoming[w]=amount
                            assert target==0
                        else:
                            assert kids[v]
                            w=kids[v][0];f[v,w]=target;incoming[w]=target
                    assert valid_certificate(n,H,k,K,[f.get(e,0) for e in H])
                    verify_tree(n,H,k,K,extract(n,H,k,K,sorted(seen),f))
                    tree_certificate_cases+=1
    stats['actual_tree_to_certificate_cases']=tree_certificate_cases
    # Aggregate all W from the exhaustive finder oracle to test the kappa/b*
    # sandwich on every <=3-vertex object; no W is selected heuristically.
    kappa_by_object={}
    for (n,E,k,W),bits in finder_cache.items():
        key=(n,E,k);mk=next((i+1 for i,b in enumerate(bits) if b),None)
        if key not in kappa_by_object:kappa_by_object[key]=mk
        elif mk is not None:
            old=kappa_by_object[key]
            kappa_by_object[key]=mk if old is None else min(old,mk)
    for (n,E,k),kap in kappa_by_object.items():
        beta=brute_score(all_trees(n,list(E)),k)
        if beta==0:assert kap is None
        else:
            assert kap is not None
            assert (1+1/beta)/2<=kap
            assert kap<=(beta.denominator+beta.numerator-1)//beta.numerator
    stats['kappa_optimum_oracle_cases']=len(kappa_by_object)
    stats['canonical_extract_crosschecks']=crosschecks
    stats['python']=platform.python_version()
    stats['precision']='integers and Fraction; exact'
    stats['seed']=792148
    stats['limits']='Finite audit only; universal theorem relies on the proof, not this search.'
    stats['sha256']=hashlib.sha256(open(__file__,'rb').read()).hexdigest()
    print(json.dumps(stats,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
