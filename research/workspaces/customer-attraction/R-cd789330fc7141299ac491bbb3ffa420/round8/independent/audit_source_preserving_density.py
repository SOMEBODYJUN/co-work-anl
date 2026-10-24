"""Independent raw-JSON/unit-client/Fraction implementation QA, not welfare evidence.
No solver, verifier, or author kernel imports. Output is exclusive-created.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from pathlib import Path
import hashlib
import json
P = Path(__file__).resolve().parent
BASE = P.parents[2]

def audit(name, I, actions, T, digest=None):
    m=I['players']; k=len(I['topics'])
    X=[frozenset(z['topics']) for z in I['customers'] for _ in range(z.get('multiplicity',1))]
    sigma={tuple(z['history']):z['action'] for z in actions}
    histories={h for i in range(m) for h in product(range(k),repeat=i)}
    assert set(sigma)==histories and len(T)==m
    assert all(0<=a<k for a in sigma.values())
    def finish(h):
        h=tuple(h)
        while len(h)<m:h+=(sigma[h],)
        return h
    def counts(z):return [sum(a in v for a in z) for v in X]
    def pay(z,i):
        c=counts(z)
        return sum((F(1,c[x]) for x,v in enumerate(X) if z[i] in v),F())
    def cover(z):return sum(any(a in v for a in z) for v in X)
    ic=0
    for h in sorted(histories,key=lambda g:(len(g),g)):
        i=len(h); V=finish(h)
        for a in range(k):assert pay(V,i)>=pay(finish(h+(a,)),i);ic+=1
    B=finish(()); cb=counts(B); ct=counts(T); u=[pay(B,i) for i in range(m)]
    opt=max(map(cover,combinations_with_replacement(range(k),m)))
    assert cover(T)==opt
    O=[x for x in range(len(X)) if ct[x]]
    p=[[F(1,ct[x]) if T[i] in v else F() for x,v in enumerate(X)] for i in range(m)]
    H=[[F() for _ in X] for _ in range(m)]
    C=[[F() for _ in X] for _ in range(m)]
    ai=[[F() for _ in X] for _ in range(m)]
    flow=defaultdict(lambda:defaultdict(F)) # history -> (unit client, origin)
    initial=[]; rows_out=[]
    for i in range(m):
        W=finish(B[:i]+(T[i],)); cw=counts(W); rows=[]
        for x,v in enumerate(X):
            if not p[i][x]:continue
            d=cb[x]+1-int(B[i] in v); pb=nb=qraw=nw=F(); edges={}
            for j in range(m):
                if j!=i:
                    if B[j] in v and T[j] not in v:z=p[i][x]/d;pb+=z;H[j][x]+=z
                    if T[j] in v and B[j] not in v:nb+=p[i][x]/d
                if j>i:
                    if W[j] in v and B[j] not in v:
                        qraw+=F(1,d*cw[x]);edges[j]=min(p[i][x],F(1,d))/cw[x]
                    if B[j] in v and W[j] not in v:nw+=F(1,d*cw[x])
            assert p[i][x]==F(1,cw[x])+pb-nb+qraw-nw
            r=p[i][x]-pb; qhat=sum(edges.values(),F())
            assert r>=0 and max(F(),r-qhat)<=F(1,cw[x])
            rows.append((x,pb,r,qhat,edges))
        R=sum((r for _,_,r,_,_ in rows),F())
        S=sum((min(r,q) for _,_,r,q,_ in rows),F())
        b=max(F(),R-u[i]);assert b<=S
        assert sum((max(F(),r-q) for _,_,r,q,_ in rows),F())<=pay(W,i)<=u[i]
        for x,pb,r,q,edges in rows:
            a=b/S*min(r,q) if S else F(); ai[i][x]=a; C[i][x]=r-a; sent=F()
            for j,cap in edges.items():
                z=a*cap/q if q else F();sent+=z
                assert z<=cap<=F(1,(cb[x]+1-int(B[i] in X[x]))*cw[x])
                assert z*cw[x]<=p[i][x]
                if z:
                    assert W[:j]!=B[:j];flow[W[:j]][x,i]+=z
                    initial.append({'owner':i,'role':j,'client':x,'history':W[:j],'amount':str(z)})
            assert sent==a<=p[i][x] and p[i][x]==pb+C[i][x]+sent
        assert sum(C[i],F())==min(R,u[i])
        rows_out.append({'owner':i,'W':W,'r':str(R),'current':str(sum(C[i],F())),
                         'future':str(b),'query_profit':str(pay(W,i))})
    for j in range(m):
        for x,v in enumerate(X):assert H[j][x]<=(F(1,cb[x]) if B[j] in v else F())
    E=[[F() for _ in X] for _ in range(m)]
    current=[[F() for _ in X] for _ in range(m)]
    contexts=[]; edge_records=[]
    for i in range(m):
        for g in sorted(h for h in list(flow) if len(h)==i):
            incoming=flow[g]
            if not sum(incoming.values(),F()):continue
            assert g!=B[:i]
            V=finish(g);a=sigma[g];A=finish(B[:i]+(a,));cv=counts(V);ca=counts(A)
            first=next(q for q in range(i) if g[q]!=B[q]); D=pay(A,i);assert D<=u[i]
            hs=defaultdict(F)
            for (x,origin),z in incoming.items():hs[x]+=z;assert origin<i
            L=F();refund=u[i]-D;maxdensity=F();client_records=[]
            for x,v in enumerate(X):
                if a not in v:assert not hs[x];continue
                h=hs[x];f=h*cv[x]
                bound=p[first][x]+sum((ai[q][x] for q in range(first)),F())
                assert 0<=f<=bound<=1;maxdensity=max(maxdensity,f)
                old={j for j in range(m) if j!=i and V[j] in v}
                new={j for j in range(m) if j!=i and A[j] in v}
                positive=new-old;negative=old-new
                N=F(len(negative),cv[x]*ca[x]);local=h-len(positive)*h/ca[x]
                assert local==f*(F(1,ca[x])-N) and 0<=local<=F(1,ca[x])
                current[i][x]+=local;L+=local;refund+=(1-f)/ca[x]+f*N
                if h:client_records.append({'client':x,'input':str(h),'density':str(f),
                                             'prefix_bound':str(bound),'current':str(local)})
                for j in sorted(positive):
                    amount=h/ca[x]
                    if not amount:continue
                    if j<i:
                        kind='past_actual';assert B[j] in v;E[j][x]+=amount
                    elif A[:j]==B[:j]:
                        kind='actual_prefix';assert B[j] in v;E[j][x]+=amount
                    else:
                        kind='future_context'
                        for (xx,origin),z in incoming.items():
                            if xx==x:flow[A[:j]][x,origin]+=z/ca[x]
                    edge_records.append({'history':g,'role':i,'client':x,'target_role':j,
                                         'target_history':A[:j],'kind':kind,'amount':str(amount)})
            assert 0<=L<=D<=u[i] and u[i]-L==refund>=0
            contexts.append({'history':g,'role':i,'first_divergence':first,'action':a,
                             'old_leaf':V,'reset_leaf':A,'input':str(sum(hs.values(),F())),
                             'current':str(L),'query_profit':str(D),'actual_profit':str(u[i]),
                             'refund':str(refund),'max_density':str(maxdensity),'clients':client_records})
        for origin in range(i):
            for x in O:
                level=sum((z for g,data in flow.items() if len(g)==i
                           for (xx,oo),z in data.items() if xx==x and oo==origin),F())
                assert level<=ai[origin][x]
    inventory=[]
    for x in O:
        parts=[sum((M[i][x] for i in range(m)),F()) for M in (H,C,current,E)]
        assert sum(parts,F())==1
        inventory.append({'client':x,'H_Csrc_current_E':list(map(str,parts))})
    total=lambda M:sum((sum(row,F()) for row in M),F())
    totals=[total(M) for M in (H,C,current,E)];assert sum(totals,F())==len(O)
    return {'fixture':name,'sha256':digest,'clients':len(X),'players':m,'topics':k,
            'ordered_nodes':len(histories),'full_IC_including_self':ic,'T':T,'actual':B,
            'actual_profit':list(map(str,u)),'W':cover(B),'OPT':opt,'initial_rows':rows_out,
            'initial_nonzero_edges':initial,'contexts':contexts,'positive_edges':edge_records,
            'nonzero_context_count':len(contexts),'nonzero_edge_count':len(edge_records),
            'nonzero_sink_edge_count':sum(e['kind']!='future_context' for e in edge_records),
            'totals_H_Csrc_current_E':list(map(str,totals)),
            'per_client_inventory':inventory,'status':'passed'}

def main():
    sources=[('old_static_assignment_52',BASE/'R-a0bb57fa24044a8794bc7991918a19c6/static_matching/static_matching_counterexample.json',(0,1,4,5)),
             ('high_insertion_2cycle_348',BASE/'R-d22a706a03c5499d941a6a97f94128a8/representation/high_insertion_2cycle_348_exact.json',(5,2,4))]
    results=[]
    for name,path,T in sources:
        raw=path.read_bytes();obj=json.loads(raw)
        results.append(audit(name,obj['instance'],obj['certificate']['actions'],T,hashlib.sha256(raw).hexdigest()))
    results.append(audit('zero_clients_m1_only_empty',{'players':1,'topics':['empty'],'customers':[]},
                         [{'history':[],'action':0}],(0,)))
    results.append(audit('m2_empty_singleton_always_singleton',
                         {'players':2,'topics':['empty','singleton'],'customers':[{'topics':[1],'multiplicity':1}]},
                         [{'history':[],'action':1},{'history':[0],'action':1},{'history':[1],'action':1}],(0,1)))
    out={'scope':'Independent exact implementation QA only; no general welfare or capacity evidence.',
         'implementation_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'fixtures':results,'status':'passed'}
    target=P/'source_preserving_density_exact.json'
    with target.open('x') as f:json.dump(out,f,indent=2);f.write('\n')
    print(json.dumps({'status':'passed','output':str(target),'fixtures':[
        {key:r[key] for key in ('fixture','clients','nonzero_context_count','nonzero_edge_count','nonzero_sink_edge_count')} for r in results]}))

if __name__=='__main__':main()
