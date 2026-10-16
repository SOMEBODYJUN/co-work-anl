"""扩区守恒合同的独立原边流、全树与参数算法审计。
No imports from the root researcher's implementation or repository solver.
"""
from fractions import Fraction as F
from itertools import combinations,product
from collections import deque
from pathlib import Path
import hashlib,json,platform,importlib.util,argparse


def cert(n,E,k,K,W,flow,old=False,r=0):
    W=set(W);I=[F(0)]*n;O=[F(0)]*n
    if r not in W or K<1:return False
    for u,v in E:
        a=F(flow.get((u,v),0))
        if a<0 or (a and (u not in W or v not in W)):return False
        O[u]+=a;I[v]+=a
    threshold=K if old else 2*K
    for v in W:
        if v!=r and I[v]>K:return False
        if k[v]>=threshold:
            if O[v]<k[v]:return False
        elif k[v]>0:
            if r==v:
                if O[v]<K:return False
            elif O[v]!=I[v]:return False
    return True


def flow_network(n,E,k,K,W,r=0,extract=False,old=False):
    # Independent Edmonds-Karp adjacency-list implementation.
    W=set(W);s=2*n;t=s+1;A=[[] for _ in range(t+1)];refs={};required=0
    def add(u,v,c):
        i=len(A[u]);j=len(A[v]);A[u].append([v,c,j]);A[v].append([u,0,i]);return (u,i,c)
    threshold=K if old else 2*K;unit=1 if extract else K
    for v in sorted(W):
        high=k[v]>=threshold
        supply=(k[v]//K if extract else k[v]) if high else (1 if extract else K) if v==r and k[v]>0 else 0
        if supply:add(s,2*v+1,supply);required+=supply
        if high or k[v]==0:add(2*v,t,unit)
        elif v!=r:add(2*v,2*v+1,unit)
    for u,v in E:
        if u in W and v in W:refs[u,v]=add(2*u+1,2*v,unit)
    value=0
    while True:
        parents=[None]*len(A);parents[s]=(-1,-1);q=deque([s])
        while q and parents[t] is None:
            u=q.popleft()
            for i,(v,c,j) in enumerate(A[u]):
                if c>0 and parents[v] is None:parents[v]=(u,i);q.append(v)
        if parents[t] is None:break
        v=t;amount=None
        while v!=s:
            u,i=parents[v];c=A[u][i][1];amount=c if amount is None else min(amount,c);v=u
        v=t
        while v!=s:
            u,i=parents[v];a=A[u][i];a[1]-=amount;A[v][a[2]][1]+=amount;v=u
        value+=amount
    if value!=required:return None
    return {e:c-A[u][i][1] for e,(u,i,c) in refs.items() if c-A[u][i][1]}


def reachable_tree(n,E,k,r=0):
    if len(E)!=len(set(E)):return None
    I=[0]*n;O=[0]*n;seen={r}
    for u,v in E:I[v]+=1;O[u]+=1
    if I[r] or max(I)>1:return None
    for _ in range(n):seen.update(v for u,v in E if u in seen)
    if any(u not in seen or v not in seen for u,v in E):return None
    if len(E)!=len(seen)-1:return None
    return min([F(1)]+[F(O[v],k[v]) for v in seen if k[v]])


def oracle(n,E,k,r=0):
    ans=F(0);witness=[]
    for bits in product((0,1),repeat=len(E)):
        H=[e for e,b in zip(E,bits) if b]
        score=reachable_tree(n,H,k,r)
        if score is not None and score>=ans:ans=score;witness=H
    return ans,witness


def choose_support(n,E,k,K,r=0):
    high=[v for v in range(n) if k[v]>=2*K];free={v for v in range(n) if k[v]<2*K}
    for bits in product((0,1),repeat=len(high)):
        W=free|{v for v,b in zip(high,bits) if b}
        if r not in W:continue
        f=flow_network(n,E,k,K,W,r)
        if f is not None:
            assert cert(n,E,k,K,W,f,r=r)
            return sorted(W),f
    return None


def extract_tree(n,E,k,K,W,r=0):
    if not k[r]:return []
    used=flow_network(n,E,k,K,W,r,extract=True)
    assert used is not None
    seen={r}
    for _ in range(n):seen.update(v for u,v in used if u in seen)
    H=[e for e in used if e[0] in seen]
    score=reachable_tree(n,H,k,r)
    assert score is not None and score>=F(1,2*K-1)
    return H


def exact(n,E,k,r=0):
    gamma={F(1)}
    out=[0]*n
    for u,v in E:out[u]+=1
    for v in range(n):
        if k[v]:gamma.update(F(a,k[v]) for a in range(1,min(k[v],out[v])+1))
    answer=[];score=reachable_tree(n,answer,k,r)
    h=sum(z>=2 for z in k)
    for tau in sorted(gamma):
        scaled=[(tau.numerator*z+tau.denominator-1)//tau.denominator for z in k]
        assert sum(z>=2 for z in scaled)<=h
        witness=choose_support(n,E,scaled,1,r)
        if witness is None:continue
        W,f=witness;H=extract_tree(n,E,scaled,1,W,r)
        beta=reachable_tree(n,H,k,r)
        assert beta>=tau
        if beta>=score:answer,score=H,beta
    return score,answer


def old_to_new(n,E,k,K,W,f,r=0):
    # Natural labels are a topological order in this audit.
    assert cert(n,E,k,K,W,f,old=True,r=r)
    W=set(W);g={};incoming=[F(0)]*n
    for v in range(n):
        if v not in W:continue
        target=F(k[v]) if k[v]>=2*K else F(K) if v==r and k[v]>0 else incoming[v] if k[v]>0 else F(0)
        for u,w in E:
            if u!=v or w not in W:continue
            a=min(target,F(f.get((u,w),0)));g[u,w]=a;incoming[w]+=a;target-=a
        assert target==0
    assert cert(n,E,k,K,W,g,r=r)
    return g


def main():
    # Import the reviewed implementation only after the independent functions
    # have been written. Oracle/verifier functions never import its helpers.
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--implementation',type=Path,
                        default=Path(__file__).with_name('rooted_dag_transit_branch_search.py'),
                        help='canonical implementation; defaults to the sibling module')
    args=parser.parse_args()
    spec=importlib.util.spec_from_file_location('reviewed_transit',args.implementation)
    reviewed=importlib.util.module_from_spec(spec);spec.loader.exec_module(reviewed)
    implementation_hash=hashlib.sha256(Path(spec.origin).read_bytes()).hexdigest()
    support_checks=0;minimum_checks=0
    counts={'exact_oracle_cases':0,'fixed_support_cases':0,'fixed_support_feasible':0,'old_to_new_cases':0,'free_extension_cases':0}
    for n in range(1,5):
        full=list(combinations(range(n),2))
        for ebits in product((0,1),repeat=len(full)):
            E=[e for e,b in zip(full,ebits) if b]
            for k in product(range(4),repeat=n):
                if any(k[u]==0 for u,v in E):continue
                expected,H=oracle(n,E,k)
                actual,S=exact(n,E,k)
                assert actual==expected
                theirs,TH=reviewed.optimize(n,E,list(k))
                assert theirs==expected and reachable_tree(n,TH,k)==expected
                counts['exact_oracle_cases']+=1
                if n>3:continue
                feasible=[];byW={}
                for K in range(1,max(k)+2):
                    any_cert=False
                    for wbits in product((0,1),repeat=n-1):
                        W=[0]+[v for v,b in zip(range(1,n),wbits) if b]
                        Ew=[(u,v) for u,v in E if u in W and v in W]
                        fs=flow_network(n,E,k,K,W)
                        independent=any(cert(n,E,k,K,W,dict(zip(Ew,vals))) for vals in product(range(K+1),repeat=len(Ew)))
                        assert (fs is not None)==independent
                        rf=reviewed.find(n,E,list(k),K,set(W))
                        assert (rf is not None)==independent
                        if rf is not None:
                            assert cert(n,E,k,K,W,rf)
                            RH=reviewed.extract(n,E,list(k),K,set(W),rf)
                            assert reachable_tree(n,RH,k)>=F(1,2*K-1)
                        byW.setdefault(tuple(W),[]).append(independent)
                        counts['fixed_support_cases']+=1
                        if fs is not None:
                            counts['fixed_support_feasible']+=1;any_cert=True
                            Wplus=set(W)|{v for v in range(n) if k[v]<2*K}
                            assert cert(n,E,k,K,Wplus,fs)
                            extract_tree(n,E,k,K,Wplus)
                            counts['free_extension_cases']+=1
                        old=flow_network(n,E,k,K,W,old=True)
                        if old is not None:
                            old_to_new(n,E,k,K,W,old);counts['old_to_new_cases']+=1
                    reduced=choose_support(n,E,k,K)
                    assert (reduced is not None)==any_cert
                    feasible.append(any_cert)
                assert feasible==sorted(feasible)
                assert all(bits==sorted(bits) for bits in byW.values())
                for W,bits in byW.items():
                    expected_min=next((i+1 for i,b in enumerate(bits) if b),None)
                    minimum_checks+=1
                    got=reviewed.min_certificate(n,E,list(k),set(W))
                    assert (None if got is None else got[0])==expected_min
                    if got is not None:assert cert(n,E,k,got[0],W,got[1])
                for K,expected_any in enumerate(feasible,1):
                    support_checks+=1
                    selected=reviewed.search_support(n,E,list(k),K)
                    assert (selected is not None)==expected_any
                    if selected is not None:
                        W,f,H=selected
                        assert cert(n,E,k,K,W,f)
                        assert reachable_tree(n,H,k)>=F(1,2*K-1)
    rows=[]
    for K in list(range(1,101))+[10**100+39,10**300+27]:
        k=[2*K-1,0];E=[(0,1)];f={(0,1):K}
        assert cert(2,E,k,K,[0,1],f)
        score,H=exact(2,E,k)
        assert score==F(1,2*K-1)
        assert reachable_tree(2,extract_tree(2,E,k,K,[0,1]),k)==score
        if K>1:assert flow_network(2,E,k,K,[0,1],old=True) is None
        rows.append({'K':K,'score':str(score)})
    counts['sharp_single_edge_cases']=rows
    # Boundary fixtures specifically added with the canonical support/min API.
    huge=10**100+39
    answer=reviewed.min_certificate(2,[],[0,huge],{0,1})
    assert answer[0]==huge//2+1 and cert(2,[],[0,huge],answer[0],{0,1},answer[1])
    chosen=reviewed.search_support(2,[],[0,huge],1)
    assert chosen==({0},{},[])
    E=[(0,1),(1,2),(1,3),(1,4)];k=[1,3,0,0,0];K=2;W=set(range(5))
    old_f={(0,1):2,(1,2):1,(1,3):1,(1,4):1}
    assert cert(5,E,k,K,W,old_f,old=True) and not cert(5,E,k,K,W,old_f)
    got=reviewed.find(5,E,k,K,W);assert got is not None and cert(5,E,k,K,W,got)
    counts['canonical_new_boundary_fixtures']=3
    counts['canonical_minimum_crosschecks']=minimum_checks
    counts['canonical_support_search_crosschecks']=support_checks
    counts['reviewed_implementation_sha256']=implementation_hash
    counts['python']=platform.python_version();counts['precision']='int/Fraction exact'
    counts['sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    print(json.dumps(counts,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
