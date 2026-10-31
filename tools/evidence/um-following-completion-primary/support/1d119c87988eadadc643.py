"""Exact executable task bridge for rooted DAG degree requirements.

Stdlib, Fraction only. Exponential audit oracles are bounded to small inputs;
construct/decode/tree_to_schedule/candidate_thresholds are the polynomial interfaces.
Writes JSON only to stdout; never overwrites frozen evidence.
"""
from fractions import Fraction as F
from itertools import product
from collections import deque
from pathlib import Path
import json,hashlib,platform

def validate(n,edges,k,root=0):
    if type(n) is not int or n<1 or type(root) is not int or not 0<=root<n:raise ValueError('vertices/root')
    if len(k)!=n or any(type(a) is not int or a<0 for a in k):raise ValueError('demands')
    if len(edges)!=len(set(edges)):raise ValueError('parallel edges')
    out=[[] for _ in range(n)];ind=[0]*n
    for u,v in edges:
        if type(u) is not int or type(v) is not int or not 0<=u<n or not 0<=v<n or u==v:raise ValueError('edge')
        out[u].append(v);ind[v]+=1
    if ind[root] or any(k[v]==0 and out[v] for v in range(n)):raise ValueError('root/terminal')
    q=deque(v for v in range(n) if ind[v]==0);seen=0
    while q:
        v=q.popleft();seen+=1
        for w in out[v]:
            ind[w]-=1
            if ind[w]==0:q.append(w)
    if seen!=n:raise ValueError('cycle')
    return out

def construct(n,edges,k,root=0):
    out=validate(n,edges,k,root);jobs=[(('root',root,0),[(root,F(1))])]
    for u in range(n):
        if not k[u]:continue
        q=min(k[u],len(out[u]))
        for a in range(q):jobs.append((('token',u,a),[(u,F(1,k[u]))]+[(v,F(1)) for v in out[u]]))
        if q<k[u]:jobs.append((('filler',u,0),[(u,F(k[u]-q,k[u]))]))
    assert len(jobs)<=1+len(edges)+n
    return jobs

def loads(n,jobs,s):
    if len(jobs)!=len(s):raise ValueError('assignment length')
    L=[F(0)]*n
    for (_,dom),i in zip(jobs,s):
        if type(i) is not int or i not in dict(dom):raise ValueError('unavailable assignment')
        L[i]+=dict(dom)[i]
    return L

def score(n,chosen,k,root=0):
    out=[[] for _ in range(n)];ind=[0]*n
    for u,v in chosen:out[u].append(v);ind[v]+=1
    if ind[root] or any(a>1 for a in ind):raise ValueError('not a tree')
    reach={root};todo=[root]
    while todo:
        for v in out[todo.pop()]:
            if v not in reach:reach.add(v);todo.append(v)
    if any(u not in reach for u,v in chosen):raise ValueError('disconnected')
    return min([F(1)]+[F(len(out[u]),k[u]) for u in reach if k[u]])

def decode(n,edges,k,jobs,s,root=0):
    L=loads(n,jobs,s);C=max(L)
    if C>=2:raise ValueError('decoder requires makespan below two')
    moved=[(u,i) for ((kind,u,a),dom),i in zip(jobs,s) if kind=='token' and i!=u]
    out=[[] for _ in range(n)]
    for u,v in moved:out[u].append(v)
    reach={root};todo=[root];chosen=[]
    while todo:
        for v in out[todo.pop()]:
            if v in reach:raise ValueError('reused child')
            reach.add(v);todo.append(v)
    chosen=[(u,v) for u,v in moved if u in reach]
    assert all(e in edges for e in chosen)
    assert score(n,chosen,k,root)>=2-C
    return chosen

def tree_to_schedule(n,edges,k,chosen,root=0):
    jobs=construct(n,edges,k,root);alpha=score(n,chosen,k,root)
    out=[[] for _ in range(n)]
    for u,v in chosen:out[u].append(v)
    kept={root};todo=[root];sent={}
    while todo:
        u=todo.pop();sent[u]=out[u][:k[u]] if k[u] else []
        kept.update(sent[u]);todo.extend(sent[u])
    s=[]
    for (kind,u,a),dom in jobs:s.append(sent.get(u,[])[a] if kind=='token' and a<len(sent.get(u,[])) else u)
    assert max(loads(n,jobs,s))<=2-alpha
    return jobs,s

def candidate_thresholds(n,edges,k,root=0):
    out=validate(n,edges,k,root)
    return sorted({F(1)}|{F(h,k[u]) for u in range(n) if k[u] for h in range(1,min(k[u],len(out[u]))+1)})

def tree_oracle(n,edges,k):
    best=F(-1);witness=[];count=0
    for bits in product([False,True],repeat=len(edges)):
        chosen=[e for e,b in zip(edges,bits) if b]
        try:b=score(n,chosen,k)
        except ValueError:continue
        count+=1
        if b>best:best=b;witness=chosen
    return best,witness,count

def audit_case(n,edges,k):
    jobs=construct(n,edges,k);beta,tree,ntree=tree_oracle(n,edges,k)
    tree_to_schedule(n,edges,k,tree)
    best=None;count=decoded=0
    for s in product(*[[i for i,p in dom] for _,dom in jobs]):
        count+=1;C=max(loads(n,jobs,s));best=C if best is None else min(best,C)
        if C<2:decode(n,edges,k,jobs,s);decoded+=1
    assert best==2-beta
    gamma=candidate_thresholds(n,edges,k)
    assert len(gamma)<=1+len(edges)
    if beta:
        assert beta in gamma
        kp=[-(-(beta*k[u]).numerator//(beta*k[u]).denominator) if k[u] else 0 for u in range(n)]
        scaled,_,_=tree_oracle(n,edges,kp);assert scaled==1
    return {'vertices':n,'edges':edges,'demands':k,'capped_degree_optimum':str(beta),'scheduling_optimum':str(best),'jobs':len(jobs),'trees_enumerated':ntree,'schedules_enumerated':count,'below_two_decoded':decoded,'thresholds':[str(x) for x in gamma]}

def main():
    cases=[]
    for leaves in range(4):
        pool=[(0,v) for v in range(1,leaves+1)]
        for bits in product([0,1],repeat=len(pool)):
            edges=[e for e,b in zip(pool,bits) if b]
            for k0 in range(1,6):cases.append((leaves+1,edges,[k0]+[0]*leaves))
    pool=[(u,v) for u in range(4) for v in range(u+1,4)]
    for bits in product([0,1],repeat=len(pool)):
        edges=[e for e,b in zip(pool,bits) if b]
        for demands in product(range(1,4),repeat=3):cases.append((4,edges,list(demands)+[0]))
    cases.extend([(1,[],[0]),(4,[],[10**100,10**101+1,10**102+3,0]),(4,[(0,1),(1,2),(1,3)],[10**100,2,10**100+7,0]),(4,[(0,1),(0,2),(1,3),(2,3)],[2,1,1,0])])
    rows=[audit_case(*a) for a in cases]
    bad=[(0,[],[],0),(2,[(0,1)],[0,0],0),(2,[(0,1),(1,0)],[1,1],0),(2,[(0,1),(0,1)],[1,0],0),(1,[],[True],0),(2,[(0,1)],[1,0],1)]
    for a in bad:
        try:construct(*a)
        except ValueError:pass
        else:raise AssertionError('invalid DAG accepted')
    # Nonzero root labels and huge binary demand do not induce large task lists.
    jobs=construct(3,[(2,0),(2,1)],[0,0,10**100],2)
    assert len(jobs)==4
    assert candidate_thresholds(3,[(2,0),(2,1)],[0,0,2],2)==[F(1,2),F(1)]
    decoded=decode(3,[(2,0),(2,1)],[0,0,1],construct(3,[(2,0),(2,1)],[0,0,1],2),[2,0],2)
    assert decoded==[(2,0)]
    out={'title':'有向需求树的压缩任务桥梁精确审计','python':platform.python_version(),'precision':'fractions.Fraction / integers; exact','seed':None,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'instances':len(rows),'schedules_enumerated':sum(r['schedules_enumerated'] for r in rows),'below_two_decoded':sum(r['below_two_decoded'] for r in rows),'invalid_cases_rejected':len(bad),'records':rows,'limits':'Bounded exponential oracles only; no MMDA approximation algorithm, hierarchy transfer or hardness theorem. Standard functions construct/decode/tree_to_schedule are polynomial interfaces.'}
    print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
