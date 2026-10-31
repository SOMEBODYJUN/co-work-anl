"""Independent audit of frozen Hall coupling implementation; no repository writes.
Original-matrix feasible-threshold DFS, with own output verification.
"""
from fractions import Fraction as Q
from itertools import product
from functools import lru_cache
from random import Random
import hashlib, json
from pathlib import Path
import importlib.util,sys,platform
base=Path(__file__).resolve().parent
source=Path(sys.argv[1]) if len(sys.argv)>1 else next(p for p in (base/'hall_group_joint_flow.py',base/'hall_joint_coupling.py') if p.exists())
spec=importlib.util.spec_from_file_location('hall_group_candidate',source)
candidate=importlib.util.module_from_spec(spec)
spec.loader.exec_module(candidate)


def matrix(groups, eligibility, macros, k):
    h=len(groups)
    A=[]
    for p in macros:
        A.append(tuple((i,Q(x)) for i,x in enumerate(p) if x is not None))
    for i,G in enumerate(groups):
        for w in G:
            A.append(((i,Q(w)),)+tuple((h+z,Q(w)) for z in eligibility[i]))
    return tuple(A)


def oracle(A,m,T):
    # No network/Hall test and no imported constructor. Original individual jobs.
    A=tuple(sorted(A,key=lambda C:(len(C),-max((w for _,w in C),default=Q(0)))))
    @lru_cache(None)
    def dfs(t,L):
        if t==len(A): return True
        for i,w in A[t]:
            if L[i]+w<=T:
                K=list(L);K[i]+=w
                if dfs(t+1,tuple(K)):return True
        return False
    return dfs(0,(Q(0),)*m)


def check(groups,E,B,k,q,d,T,record):
    A=matrix(groups,E,B,k)
    yes=oracle(A,len(groups)+k,T)
    out=candidate.solve(groups,E,B,k,q,d,T)
    assert not yes or out is not None
    if out is not None:
        S=list(out['macro_assignment'])+[i for row in out['assignment'] for i in row]
        assert len(S)==len(A)
        loads=[Q(0)]*(len(groups)+k)
        for C,(kind,i) in zip(A,S):
            assert kind in {'h','z'}
            z=i if kind=='h' else len(groups)+i
            D=dict(C)
            assert z in D
            loads[z]+=D[z]
        r=Q(2*q+q*d,q+1)
        assert loads==out['loads']
        assert all(w<=r*T for w in loads)
    record['instances']+=1;record['original_T_feasible']+=yes
    record['success']+=out is not None
    record['rejection']+=out is None


def run():
    record={'instances':0,'original_T_feasible':0,'success':0,'rejection':0}
    for q,d,templates in [
        (2,Q(1,2),[(Q(1,2),Q(1,2)),(Q(0),Q(1,3),Q(1,3),Q(1,3))]),
        (3,Q(1,3),[(Q(1,3),Q(1,3),Q(1,6)),(Q(1,3),)*3]),
        (4,Q(1,4),[(Q(1,4),)*3,(Q(1,4),)*4]),
    ]:
        for h in [1,2]:
            k=2
            support=[tuple(i for i in range(k) if mask>>i&1) for mask in range(1<<k)]
            pvalues=[None,Q(1,2)+Q(1,2**81),Q(1),Q(3,2)]
            rows=[row for row in product(pvalues,repeat=h) if any(p is not None for p in row)]
            for G in product(templates,repeat=h):
                for E in product(support,repeat=h):
                    for n in range(h+1):
                        # macro support and time assignments: all one-macro, selected two-macro.
                        M=product(rows,repeat=n) if n<=1 else ((rows[i],rows[j]) for i in range(0,len(rows),3) for j in range(0,len(rows),3))
                        for B in M:check(G,E,B,k,q,d,Q(1),record)
    # Original matrix feasibility independent random enumeration for 3 homes, 3 sinks.
    rng=Random(230782)
    for z in range(150):
        q=rng.choice([2,3,4]);d=Q(1,q)
        G=[[Q(1,q)]*rng.randint((q+1)//2+1,q) for _ in range(3)]
        # exact contract lower bound at all q, redo W if necessary.
        for row in G:
            while sum(row,Q(0))<Q(1,2)+Q(1,q):row.append(Q(1,q))
        E=[tuple(i for i in range(3) if rng.getrandbits(1)) for _ in range(3)]
        B=[]
        for j in range(rng.randint(0,3)):
            R=tuple(rng.choice([None,Q(3,4),Q(1),Q(5,4)]) for i in range(3))
            if all(v is None for v in R):R=(Q(1),None,None)
            B.append(R)
        check(G,E,B,3,q,d,Q(1),record)
    # T0 with no private zero assumption, zero jobs, empty H and very large q.
    fixtures=[
        ([[]],[()],[],1,2,Q(0),Q(0)),
        ([[Q(0),Q(0)]],[()],[],1,2,Q(0),Q(0)),
        ([[Q(0)]],[(0,)],[(Q(1,2),)],1,2,Q(0),Q(0)),
        ([],[],[],1,2**400,Q(1,2**400),Q(1)),
    ]
    for args in fixtures:check(*args,record)
    invalid=[
      lambda:candidate.solve([[Q(1,19)]],[(0,)],[],1,2,Q(0),Q(0)),
      lambda:candidate.solve([[0.5,0.5]],[(0,)],[],1,2,Q(1,2)),
      lambda:candidate.solve([[True,Q(0)]],[(0,)],[],1,2,Q(1,2)),
      lambda:candidate.solve([[Q(1,2)]*2],[(0,)],[],1,2,0.5),
      lambda:candidate.solve([[Q(1,2)]*2],[(0,)],[],1,3.0,Q(1,2)),
      lambda:candidate.solve([[Q(1,2)]*2],[(0,)],[],True,2,Q(1,2)),
      lambda:candidate.solve([],[],[],0,2,Q(0),Q(0)),
    ]
    rejected=0
    for case in invalid:
      try:case()
      except (TypeError,ValueError):rejected+=1
      else:raise AssertionError('invalid contract input was accepted')
    record['explicit_invalid_rejections']=rejected
    check([['1/2','1/2']],[(0,)],[('3/4',)],1,2,Q(1,2),Q(1),record)
    return {**record,'proof_scope':'finite original-matrix threshold DFS; no Hall oracle',
      'python':platform.python_version(),'seed':230782,
      'source_sha256':hashlib.sha256(Path(candidate.__file__).read_bytes()).hexdigest(),
      'review_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'status':'PASS'}

if __name__=='__main__':print(json.dumps(run(),indent=2))
