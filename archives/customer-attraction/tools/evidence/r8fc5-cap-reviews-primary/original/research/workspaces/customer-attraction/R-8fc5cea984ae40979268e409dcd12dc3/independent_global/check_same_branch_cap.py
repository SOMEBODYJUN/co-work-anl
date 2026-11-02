"""Exact finite attack on same-branch deletion/refund cap; no SPE claims."""
from fractions import Fraction
import json

def recip(n):
    return Fraction(1,n) if n else Fraction(0)

def value(p,c,a,d0,d):
    return p*max(Fraction(0),recip(c)-recip(d0)) + a*(recip(d0)-recip(d))

def proposed(p,c,a,d):
    return max(Fraction(0),a*recip(p+a)-a*recip(d), p*(recip(c)-recip(d)))

checked=0
params=0
for m in range(1,16):
    for c in range(m+1):
        for p in range(c+1):
            for a in (0,1):
                for d in range(max(1,p+a),m+1):
                    vals=[value(p,c,a,d0,d) for d0 in range(p+a,d+1)]
                    cap=proposed(p,c,a,d)
                    assert max(vals)==cap, (m,p,c,a,d,max(vals),cap)
                    assert cap<=1-Fraction(1,d)<=1-Fraction(1,m)
                    checked+=len(vals)
                    params+=1
print(json.dumps({'status':'pass','m_range':[1,15], 'parameter_tuples':params,
 'load_tuples':checked,'arithmetic':'Fraction',
 'assertions':['exact endpoint cap','cap <= 1-1/d <= 1-1/m'],
 'scope':'finite algebra check only; no strategy tree or SPE enumeration'},indent=2))
