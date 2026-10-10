"""Independent definition-level Fraction check; no optimizer/generator imported."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product,combinations_with_replacement
from pathlib import Path
import argparse,gzip,hashlib,json
from math import lcm

def certify_cones(path):
    with gzip.open(path,'rt',encoding='utf-8') as stream:pack=json.load(stream)
    assert len(pack['cases'])==21
    results=[]
    for case in pack['cases']:
        n,m=case['players'],case['topics'];k=(1<<m)-1
        hist=tuple(h for d in range(n) for h in product(range(m),repeat=d))
        policy={tuple(r['history']):r['action'] for r in case['policy']}
        assert len(policy)==len(case['policy']) and set(policy)==set(hist)
        assert all(type(a)==int and 0<=a<m for a in policy.values())
        @lru_cache(None)
        def terminal(h):return h if len(h)==n else terminal(h+(policy[h],))
        L=lcm(*range(1,n+1))
        @lru_cache(None)
        def cts(z):return tuple(z.count(a) for a in range(m))
        @lru_cache(None)
        def row(a,q):
            # Exact common-denominator representation of the Fraction rows.
            return tuple(L//sum(q[b] for b in range(m) if mask&(1<<b)) if mask&(1<<a) else 0 for mask in range(1,k+1))
        gamma=set();pairs=set()
        for h in hist:
            q=cts(terminal(h))
            for a in range(m):
                qdev=cts(terminal(h+(a,)));key=(policy[h],q,a,qdev)
                if key not in pairs:
                    pairs.add(key);gamma.add(tuple(x-y for x,y in zip(row(policy[h],q),row(a,qdev))))
        cert=case['certificate'];assert cert['exact_certified'] and cert['Gamma_scale']==L
        Q=[(tuple(r['rivals']),F(r['probability'])) for r in cert['Q']]
        assert Q and min(q for B,q in Q)>=0 and sum(q for B,q in Q)==1
        assert all(len(B)==n-1 and all(type(b)==int and 0<=b<m for b in B) for B,q in Q)
        z=terminal(());c=[F(any(mask&(1<<a) for a in z),n) for mask in range(1,k+1)]
        assert len(cert['lambda'])==m
        minimum=F(0);nnz=0
        for a,terms in enumerate(cert['lambda']):
            lam=[]
            for term in terms:
                ints=tuple(term['row']);g=tuple(F(x,L) for x in ints);mu=F(term['coefficient'])
                assert ints in gamma and mu>=0
                lam.append((g,mu));nnz+=1
            for j in range(k):
                mask=j+1
                bg=sum((q*F(int(bool(mask&(1<<a))),1+sum(bool(mask&(1<<b)) for b in B)) for B,q in Q),F(0))
                residual=c[j]-bg-sum((mu*g[j] for g,mu in lam),F(0))
                assert residual>=0,(case['name'],a,mask,residual)
                minimum=min(minimum,residual)
        results.append(dict(name=case['name'],players=n,topics=m,root=z,ordered_histories=len(hist),all_action_comparisons=len(hist)*m,unique_Gamma_rows=len(gamma),coordinate_identities=m*k,Q_support=len(Q),Gamma_multiplier_support=nnz,min_residual=str(minimum)))
    return dict(status='PASS',source=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),scope=pack['scope'],cases=len(results),all_ordered_histories=sum(r['ordered_histories'] for r in results),all_comparisons=sum(r['all_action_comparisons'] for r in results),identities=sum(r['coordinate_identities'] for r in results),results=results)


if __name__=='__main__':
    ROOT=Path(__file__).resolve().parents[2]
    ap=argparse.ArgumentParser()
    ap.add_argument('path',nargs='?',type=Path,default=ROOT/'evidence/certificates/customer_attraction/new_policy_security_cones.json.gz')
    ap.add_argument('--output',type=Path)
    args=ap.parse_args();raw=json.dumps(certify_cones(args.path),indent=2)+'\n'
    if args.output:
        with args.output.open('x') as stream:stream.write(raw)
    print(raw,end='')
