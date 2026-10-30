#!/usr/bin/env python3
"""Exact orbit/literal-resource cross-check; no floating point or random seed."""
from fractions import Fraction as F
from itertools import product
import hashlib
import json
import platform
from pathlib import Path


def poly(coefficients, x):
    return sum((F(a) * x**k for k, a in enumerate(coefficients)), F(0))


def ratio(current, deviation):
    if deviation:
        return current / deviation
    return None if current else F(1)  # None denotes +infinity.


def maximum(values):
    return None if None in values else max(values)


def orbit(n, w, P, Q):
    h = [poly(P, 1+m*w)+(n-m)*poly(Q,1+w)+m*poly(Q,1) for m in range(n+1)]
    A = [poly(P,1+m*w)+poly(Q,w) for m in range(n+1)]
    D = [poly(P,(n-m+1)*w)+poly(Q,1+w) for m in range(n+1)]
    rows=[]
    for m in range(n+1):
        H=ratio(h[m],h[n-m])
        L=ratio(A[m],D[m]) if m else 'absent'
        O=ratio(D[m+1],A[m+1]) if m<n else 'absent'
        values=[F(1),H]+([L] if m else [])+([O] if m<n else [])
        rows.append({'m':m,'heavy':H,'same':L,'opposite':O,'q':maximum(values)})
    return rows


def strategies(n):
    heavy=(tuple(range(n+1)), tuple(range(n+1,2*(n+1))))
    lights=[((0,n+1+i),(n+1,i)) for i in range(1,n+1)]
    return [heavy,*lights]


def literal_costs(profile,n,w,P,Q):
    choices=strategies(n)
    weights=[F(1)]+[w]*n
    loads=[F(0)]*(2*(n+1))
    for i,choice in enumerate(profile):
        for resource in choices[i][choice]:
            loads[resource]+=weights[i]
    latencies=[poly(P if resource%(n+1)==0 else Q,x) for resource,x in enumerate(loads)]
    return [sum((latencies[e] for e in choices[i][profile[i]]),F(0)) for i in range(n+1)]


def serialize(value):
    if isinstance(value,F):return str(value)
    if isinstance(value,list):return [serialize(x) for x in value]
    if isinstance(value,dict):return {k:serialize(v) for k,v in value.items()}
    return value


def verify():
    functions=[(0,),(1,),(0,1),(1,0,2),(0,0,0,1)]
    weights=[F(1,10),F(1,5),F(1,2),F(1),F(2)]
    profiles=deviations=cases=0
    for n,w,P,Q in product(range(1,6),weights,functions,functions):
        rows=orbit(n,w,P,Q)
        cases+=1
        for s in product(range(2),repeat=n+1):
            profiles+=1
            current=literal_costs(s,n,w,P,Q)
            ratios=[F(1)]
            m=sum(s[i]==s[0] for i in range(1,n+1))
            for i in range(n+1):
                t=list(s);t[i]=1-t[i]
                new=literal_costs(t,n,w,P,Q)
                actual=ratio(current[i],new[i])
                expected=rows[m]['heavy' if i==0 else 'same' if s[i]==s[0] else 'opposite']
                assert actual==expected,(n,w,P,Q,s,i,actual,expected)
                ratios.append(actual);deviations+=1
            assert maximum(ratios)==rows[m]['q']
    rows=orbit(3,F(1,5),(0,1),(0,0,F(1,2)))
    threshold=min(row['q'] for row in rows)
    assert threshold==F(157,156)
    assert min(rows[0]['heavy'],rows[1]['same'])==F(61,66)
    for row in rows:
        assert row['q']>=threshold
    # Reverse-check every quotient by multiplication using literal costs.
    reverse_checks=0
    for s in product(range(2),repeat=4):
        current=literal_costs(s,3,F(1,5),(0,1),(0,0,F(1,2)))
        for i in range(4):
            t=list(s);t[i]=1-t[i]
            new=literal_costs(t,3,F(1,5),(0,1),(0,0,F(1,2)))
            r=ratio(current[i],new[i])
            assert r*new[i]==current[i]
            reverse_checks+=1
    return {'schema':1,'claim_ids':['WC-R2-ORBIT v1','WC-R2-COARSE-LOSS v1'],
            'arithmetic':'fractions.Fraction; exact','seed':None,
            'python':platform.python_version(),'functions':serialize([list(x) for x in functions]),
            'weights':serialize(weights),'n_range':[1,5],
            'parameter_cases':cases,'literal_profiles':profiles,'literal_deviations':deviations,
            'reverse_checks':reverse_checks,'counterexample_rows':serialize(rows),
            'instance_threshold':str(threshold),'coarse_certificate':str(F(61,66)),
            'limitations':'Finite cross-check supports the implementation; general proof is in proof.md. No optimization or novelty claim.',
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__=='__main__':
    report=verify()
    destination=Path(__file__).with_name('evidence.json')
    destination.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False))
