"""Exact definition-level audit; no imports from canonical solver or graph_probe."""
from collections import defaultdict, deque
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import random

RNG=random.Random(271828)


def weak_counts(h,p):
    return tuple(sum(x==a for x in h) for a in range(p))


def payoff(a,q,p):
    ans=[]
    for mask in range(1,1<<p):
        ans.append(F(1,sum(q[b] for b in range(p) if mask&(1<<b))) if mask&(1<<a) else F(0))
    return tuple(ans)


def build(p,n,actions):
    terminals={}
    for d in range(n,-1,-1):
        for h in product(range(p),repeat=d):
            terminals[h]=weak_counts(h,p) if d==n else terminals[h+(actions[h],)]
    edges={}
    for h,a in actions.items():
        for t in range(p):
            if t==a:continue
            v=(t,terminals[h+(t,)])
            z=(a,terminals[h])
            edges.setdefault((v,z),(h,t))
    vertices=sorted(set(x for e in edges for x in e))
    if not vertices:
        vertices=sorted({(a,q) for h,q in terminals.items() if len(h)==n for a in range(p) if q[a]})
    return terminals,vertices,edges


def divergence(flow,vertices):
    b={v:F(0) for v in vertices}
    for (v,z),x in flow.items():
        b[v]-=x;b[z]+=x
    return b


def exact_flow(vertices,edges,b):
    """Edmonds-Karp with explicit antiparallel arcs; returns exact primal flow."""
    if sum(b.values())!=0:return None
    M=sum(-x for x in b.values() if x<0)
    if not M:return {} if all(not x for x in b.values()) else None
    index={v:i for i,v in enumerate(vertices)}
    N=len(vertices);s=N;t=N+1
    net=[[] for _ in range(N+2)];stored={}
    def arc(u,v,c):
        f=[v,len(net[v]),F(c)];r=[u,len(net[u]),F(0)]
        net[u].append(f);net[v].append(r)
        return f
    for v,z in edges:stored[v,z]=arc(index[v],index[z],M)
    for v,x in b.items():
        if x<0:arc(s,index[v],-x)
        elif x>0:arc(index[v],t,x)
    value=F(0)
    while True:
        prev={s:None};q=deque([s])
        while q and t not in prev:
            u=q.popleft()
            for j,e in enumerate(net[u]):
                if e[2]>0 and e[0] not in prev:
                    prev[e[0]]=(u,j);q.append(e[0])
        if t not in prev:break
        delta=M;v=t
        while v!=s:
            u,j=prev[v];delta=min(delta,net[u][j][2]);v=u
        v=t
        while v!=s:
            u,j=prev[v];e=net[u][j];e[2]-=delta;net[v][e[1]][2]+=delta;v=u
        value+=delta
    if value!=M:return None
    flow={e:M-a[2] for e,a in stored.items() if M-a[2]}
    assert divergence(flow,vertices)==b
    return flow


def forestify(original,vertices):
    flow={e:F(x) for e,x in original.items() if x}
    while True:
        par={v:v for v in vertices};forest=defaultdict(list);cycle=None
        def find(v):
            while par[v]!=v:
                par[v]=par[par[v]];v=par[v]
            return v
        for e in sorted(flow):
            u,v=e;ru,rv=find(u),find(v)
            if ru!=rv:
                par[ru]=rv;forest[u].append((v,e));forest[v].append((u,e))
                continue
            prev={v:None};q=deque([v])
            while u not in prev:
                x=q.popleft()
                for y,f in forest[x]:
                    if y not in prev:prev[y]=(x,f);q.append(y)
            path=[];y=u
            while y!=v:
                x,f=prev[y];path.append((f,1 if f==(x,y) else -1));y=x
            cycle=path+[(e,1)]
            break
        if cycle is None:break
        if all(s>0 for e,s in cycle):cycle=[(e,-s) for e,s in cycle]
        eps=min(flow[e] for e,s in cycle if s<0)
        for e,s in cycle:
            flow[e]+=eps*s
            assert flow[e]>=0
            if not flow[e]:del flow[e]
    assert divergence(flow,vertices)==divergence(original,vertices)
    assert len(flow)<=max(0,len(vertices)-1)
    return flow


def feature_sum(flow,p):
    out=[F(0)]*((1<<p)-1)
    for (v,z),x in flow.items():
        for j,(a,b) in enumerate(zip(payoff(*z,p),payoff(*v,p))):out[j]+=x*(a-b)
    return tuple(out)


def closedsets(vertices,edges):
    ix={v:i for i,v in enumerate(vertices)}
    ans=[]
    for mask in range(1<<len(vertices)):
        if all(not(mask>>ix[v]&1) or (mask>>ix[z]&1) for v,z in edges):
            ans.append([v for v in vertices if mask>>ix[v]&1])
    return ans


def rank(rows):
    basis={}
    for row in rows:
        a=list(row)
        for k in sorted(basis):
            f=a[k]
            if f:a=[x-f*y for x,y in zip(a,basis[k])]
        j=next((k for k,x in enumerate(a) if x),None)
        if j is not None:
            f=a[j];basis[j]=[x/f for x in a]
    return len(basis)


def sccs(vertices,edges):
    adj=defaultdict(list)
    for v,z in edges:adj[v].append(z)
    reaches={}
    for v in vertices:
        seen={v};q=deque([v])
        while q:
            for z in adj[q.popleft()]:
                if z not in seen:seen.add(z);q.append(z)
        reaches[v]=seen
    todo=set(vertices);cs=[]
    while todo:
        v=min(todo);c=sorted(z for z in todo if z in reaches[v] and v in reaches[z]);cs.append(c);todo-=set(c)
    return cs


def audit():
    strategies=0;cuts=0;transports=0;featurechecks=0;maximum_before=maximum_after=0
    for n in [2,3]:
        p=2;hist=[h for d in range(n) for h in product(range(p),repeat=d)]
        for choices in product(range(p),repeat=len(hist)):
            actions=dict(zip(hist,choices));terminal,vs,es=build(p,n,actions);strategies+=1
            expected=p*n
            assert len(vs)==expected
            for (v,z),(h,t) in es.items():
                f=payoff(*z,p);g=payoff(*v,p)
                # Rebuild the two terminal player payoffs from ordered histories.
                def direct(branch,a):
                    q=terminal[branch]
                    return tuple(F(1,sum(q[b] for b in range(p) if mask>>b&1)) if mask>>a&1 else F(0) for mask in range(1,1<<p))
                assert f==direct(h,actions[h]) and g==direct(h+(t,),t)
            cs=closedsets(vs,es)
            for k in range(4):
                vals=[F(RNG.randint(-3,3)) for v in vs[:-1]];vals+=[-sum(vals)]
                b=dict(zip(vs,vals));cutok=all(sum(b[v] for v in U)>=0 for U in cs)
                flow=exact_flow(vs,es,b)
                assert (flow is not None)==cutok
                cuts+=1
                if flow is not None:
                    small=forestify(flow,vs);assert feature_sum(small,p)==feature_sum(flow,p)
                    transports+=1
            flow={e:F(RNG.randint(0,7),RNG.randint(1,5)) for e in es}
            small=forestify(flow,vs)
            assert feature_sum(small,p)==feature_sum(flow,p)
            b=divergence(flow,vs)
            lhs=feature_sum(flow,p)
            rhs=tuple(sum(b[v]*payoff(*v,p)[j] for v in vs) for j in range((1<<p)-1))
            assert lhs==rhs
            featurechecks+=1
            maximum_before=max(maximum_before,sum(bool(x) for x in flow.values()))
            maximum_after=max(maximum_after,len(small))
    # Strict H_terminal < H_graph example, read serialized complete strategy,
    # but rebuild every terminal payoff and all best-response checks independently.
    doc=json.loads(Path(__file__).with_name('graph_probe.json').read_text())
    p,n=doc['topics'],doc['players'];actions={tuple(x['h']):x['a'] for x in doc['actions']}
    term,vs,es=build(p,n,actions);masses={int(k):v for k,v in doc['masses'].items()}
    comparisons=0
    for h,a in actions.items():
        actual=sum(masses.get(mask,0)*x for mask,x in enumerate(payoff(a,term[h],p),1))
        for t in range(p):
            deviating=sum(masses.get(mask,0)*x for mask,x in enumerate(payoff(t,term[h+(t,)],p),1))
            assert actual>=deviating;comparisons+=1
    byq=defaultdict(set)
    for h,a in actions.items():
        if len(h)==n-1:byq[weak_counts(h,p)].add(a)
    assert all(len(a)==1 for a in byq.values())
    hs=[]
    for C in sccs(vs,es):
        rep=C[0]
        for v in C[1:]:hs.append(tuple(x-y for x,y in zip(payoff(*v,p),payoff(*rep,p))))
    dim=rank(hs);assert dim==1
    # Universal graph transport equality and forest reduction also on this graph.
    flow={e:F(RNG.randint(0,9),RNG.randint(1,7)) for e in es}
    small=forestify(flow,vs)
    assert feature_sum(small,p)==feature_sum(flow,p)
    assert len(small)<=len(vs)-1
    return {'status':'passed','complete_two_topic_strategies':strategies,'integer_divergence_cut_vs_flow_checks':cuts,'feasible_cut_flows_reconstructed':transports,'rational_feature_and_forest_checks':featurechecks+1,'largest_small_case_support_before':maximum_before,'largest_small_case_support_after':maximum_after,'strict_example':{'ordered_nodes':len(actions),'complete_action_comparisons':comparisons,'payoff_form_vertices':len(vs),'distinct_graph_edges':len(es),'terminal_tie_subspace_dimension':0,'full_depth_scc_subspace_dimension':dim,'root_counts':term[()],'nontrivial_scc_sizes':[len(C) for C in sccs(vs,es) if len(C)>1],'random_support_before':sum(bool(x) for x in flow.values()),'forest_support_after':len(small)},'scope':'finite regression of exact graph identities; not a universal half-coverage proof'}

if __name__=='__main__':
    result=audit()
    Path(__file__).with_name('graph_flow_audit.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
