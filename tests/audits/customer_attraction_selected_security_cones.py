"""Independent Fraction check of all-coordinate full-cone safety identities.

Reads only a self-contained frozen policy/certificate pack. No optimizer,
generator, repository solver, or candidate verifier is imported.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import sys

def verify(path):
    pack=json.loads(Path(path).read_text());results=[]
    for case in pack['cases']:
        n,m=case['players'],case['topics'];k=(1<<m)-1
        raw=case['policy'];policy={tuple(r['history']):r['action'] for r in raw}
        histories={h for d in range(n) for h in product(range(m),repeat=d)}
        assert len(policy)==len(raw) and set(policy)==histories
        assert all(0<=a<m for a in policy.values())
        def finish(h):
            z=list(h)
            while len(z)<n:z.append(policy[tuple(z)])
            return tuple(z)
        def rho(action,z,mask):
            if not mask&(1<<action):return F(0)
            return F(1,sum(bool(mask&(1<<b)) for b in z))
        def static(a,B,mask):
            if not mask&(1<<a):return F(0)
            return F(1,1+sum(bool(mask&(1<<b)) for b in B))
        gamma=set()
        for h in histories:
            actual=finish(h)
            for a in range(m):
                alternative=finish(h+(a,))
                gamma.add(tuple(rho(policy[h],actual,mask)-rho(a,alternative,mask) for mask in range(1,k+1)))
        z=finish(())
        for cert in case['certificates']:
            if cert['target']=='aggregate':
                target=[F(any(mask&(1<<a) for a in z),n) for mask in range(1,k+1)]
            else:
                i=int(cert['target']);assert 0<=i<n
                target=[rho(z[i],z,mask) for mask in range(1,k+1)]
            Q=[(tuple(B),F(q)) for B,q in cert['Q']]
            assert sum(q for B,q in Q)==1 and min(q for B,q in Q)>=0
            assert all(len(B)==n-1 and all(0<=b<m for b in B) for B,q in Q)
            assert len(cert['lambda'])==m
            all_res=[];nonzeros=0
            for a,rawlam in enumerate(cert['lambda']):
                lams=[]
                for item in rawlam:
                    row=tuple(map(F,item['row']));coefficient=F(item['coefficient'])
                    assert row in gamma and coefficient>=0
                    lams.append((row,coefficient));nonzeros+=1
                residual=[target[j]-sum(q*static(a,B,j+1) for B,q in Q)-sum(mu*row[j] for row,mu in lams) for j in range(k)]
                assert min(residual)>=0,(case['name'],cert['target'],a,min(residual))
                all_res.extend(residual)
            results.append({'case':case['name'],'target':cert['target'],'outcome':z,
                            'coordinate_identities':m*k,'full_ordered_histories':len(histories),
                            'full_comparisons':m*len(histories),'nonzero_Gamma_multipliers':nonzeros,
                            'Q':[[list(B),str(q)] for B,q in Q],'minimum_residual':str(min(all_res))})
    return {'status':'PASS','scope':pack['scope'],'identities':sum(r['coordinate_identities'] for r in results),'results':results}

if __name__=='__main__':
    path=sys.argv[1] if len(sys.argv)>1 else Path(__file__).resolve().parents[2]/'evidence/certificates/customer_attraction/selected_security_cones.json'
    print(json.dumps(verify(path),indent=2))
