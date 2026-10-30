#!/usr/bin/env python3
"""Independent original-P/config audit; no normative imports or big-parameter NO test."""
import hashlib,json
from fractions import Fraction as F
from itertools import product,permutations
from collections import Counter


def audit_one(D,Q,pi):
    assert all(sorted(row)==list(range(Q)) for row in pi.values())
    assert all(pi[i,j][0]==i+1 for i in range(D) for j in range(D))
    times={}; sigma={}; incoming={}; outgoing={}; resource_ports={}
    def private(i,a,path): return ('private',i,a,path)
    def resource(j,x): return ('resource',j,x)
    machines=set()
    for i in range(D):
        for a in range(Q):
            for z in range(Q):
                for path in product(range(D),repeat=z):
                    m=private(i,a,path);machines.add(m);outgoing[m]=[]
    for j in range(D):
        for x in product(range(D),repeat=Q):
            m=resource(j,x);machines.add(m);resource_ports[m]=[]
    def selected(i,path):
        if not path:return True
        if path[0]>=D-1:return False
        free=[b for b in range(Q) if b!=i+1]
        for c,val in zip(free,path[1:]):
            forbidden=c-1 if 1<=c<=D else D-1
            if val==forbidden:return False
        return True
    for i in range(D):
        job=('selector',i)
        times[job]={private(i,a,()):F(1) for a in range(Q)}
        sigma[job]=private(i,0,())
        for a in range(Q):incoming[private(i,a,())]=job
    for i in range(D):
        for a in range(Q):
            for z in range(Q):
                for path in product(range(D),repeat=z):
                    parent=private(i,a,path)
                    for value in range(D):
                        cp=path+(value,);job=('arc',i,a,cp)
                        if len(cp)<Q:
                            child=private(i,a,cp);incoming[child]=job
                        else:
                            j=cp[0];beta=pi[i,j][a]
                            free=[b for b in range(Q) if b!=beta]
                            x=[None]*Q;x[beta]=i
                            for c,v in zip(free,cp[1:]):x[c]=v
                            child=resource(j,tuple(x));resource_ports[child].append(job)
                        times[job]={parent:F(1,D),child:F(1)}
                        outgoing[parent].append(job)
                        sigma[job]=child if a==0 and selected(i,cp) else parent
    loads={m:F(0) for m in machines}
    for j,dest in sigma.items():assert dest in times[j];loads[dest]+=times[j][dest]
    assert len(sigma)==len(times)
    assert max(loads.values())==1+F(1,D)
    coverage={j:F(0) for j in times};config_count=0;machine_mass={m:F(0) for m in machines}
    def config(m,js,weight):
        nonlocal config_count
        assert len(set(js))==len(js)
        load=sum((times[j][m] for j in js),F(0))
        assert load<=1 and weight>=0
        for j in js:coverage[j]+=weight
        machine_mass[m]+=weight;config_count+=1
    for m in machines:
        if m[0]=='private':
            config(m,[incoming[m]],F(1,Q))
            config(m,outgoing[m],1-F(1,Q))
        else:
            assert len(resource_ports[m])==Q
            for j in resource_ports[m]:config(m,[j],F(1,Q))
    assert all(x==1 for x in coverage.values())
    assert all(x==1 for x in machine_mass.values())
    return {'D':D,'Q':Q,'machines':len(machines),'jobs':len(times),
            'configs':config_count,'actual_max_load':str(max(loads.values())),
            'actual_load_histogram':dict(sorted(Counter(map(str,loads.values())).items())),
            'every_job_config_coverage':'1','every_machine_config_mass':'1',
            'every_resource_eligible_leaf_ports':Q}


def audit():
    D,Q=2,3
    options=[]
    for i in range(D):
        rows=[]
        for tail in permutations([a for a in range(Q) if a!=i+1]):rows.append((i+1,)+tail)
        options.append(rows)
    results=[]
    for choices in product(*(options[i] for i in range(D) for j in range(D))):
        pi={(i,j):choices[i*D+j] for i in range(D) for j in range(D)}
        results.append(audit_one(D,Q,pi))
    D,Q=3,4
    pi={}
    for i in range(D):
        for j in range(D):
            rest=[a for a in range(Q) if a!=i+1]
            if (i+j)%2:rest.reverse()
            pi[i,j]=(i+1,)+tuple(rest)
    third=audit_one(D,Q,pi)
    return {'status':'passed','independent_implementation':True,'normative_imports':[],
            'scope':'physical/config structural identities only; small parameters do not satisfy v4 probabilistic NO constants',
            'all_D2_Q3_conditioned_permutation_arrays':len(results),
            'D2_Q3_result_invariants':results[0],
            'D2_Q3_all_results_identical':all(x==results[0] for x in results),
            'one_D3_Q4_array':third,
            'unverified':'No cheap-list NO assertion and no original scheduling OPT oracle are run by this audit.'}

if __name__=='__main__':
    result=audit()
    result['script_sha256']=hashlib.sha256(open(__file__,'rb').read()).hexdigest()
    print(json.dumps(result,indent=2,sort_keys=True))
