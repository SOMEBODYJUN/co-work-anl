"""Exact standalone compressed-column audit; no model or LP imports."""
from fractions import Fraction as Q
import json
from pathlib import Path
import hashlib

def floors(n,s=7):
    aa=[Q(n+t,(t+1)*(s*n-(s-2)*t)) for t in range(n-1)]+[Q(1,n+s-1)]
    bb=[Q(2,s*n-(s-2)*t) for t in range(n-1)]+[Q(n+1,n*(n+s-1))]
    return sum((min(aa[t:]) for t in range(n-2)),Q()),sum((min(bb[t:]) for t in range(n-2)),Q())

def slacks(n,s,f,k,p,d):
    fp,fv=floors(n,s)
    z=s-1; pairs=Q(z*(z-1),2); m=f+k
    F=Q(n-2,n) if m==s else fp if m==1 else fv
    count=p+d+f
    pay=lambda numerator: Q(numerator,count) if count else Q()
    g=Q(k,p+1) if not f else Q(z-k,p+1)+Q(2*k,p+2)
    h=Q(k*(z-k),p+1)+Q(k*(k-1),p+2)
    tax=Q(d,(p+1)*(p+2))
    return [pay(p)-F,pay(z*f)-Q(k,p+d+1),pay(z*(d+f))+z*tax-g,pay(pairs*(d+f))+pairs*tax-h]

def check(n,weights,s=7):
    counts=0; minimum=None; minimum_type=None
    for f in range(2):
      for k in range(s):
        if f+k==0: continue
        for p in range(n-1):
          for d in range(2):
            w=Q(int(bool(p+d+f)))
            residual=w-Q(1,2)-sum((a*b for a,b in zip(weights,slacks(n,s,f,k,p,d))),Q())
            assert residual>=0,(n,f,k,p,d,residual)
            counts+=1
            if minimum is None or residual<minimum:
                minimum,minimum_type=residual,(f,k,p,d)
    return {'n':n,'cases':counts,'minimum':str(minimum),'minimum_type':minimum_type,'weights':[str(x) for x in weights]}

def literal_check(cert):
    n=cert['n']; scale=cert['denominator']
    raw_private=[Q(n+t,(t+1)*(7*n-5*t)) for t in range(n-1)]+[Q(1,n+6)]
    private=[min(raw_private[t:]) for t in range(n)]
    shared=[Q(2,7*n-5*t) for t in range(n-1)]+[Q(n+1,n*(n+6))]
    weights=[Q(v,scale) for v in cert['numerators']]
    assert len(weights)==n+35 and all(v>=0 for v in weights)
    minimum=Q(1); cases=0; witness=None
    for incidence in range(1,128):
      f=incidence&1
      for earlier in range(1<<(n-1)):
        actual=earlier | (f<<(n-1)); count=actual.bit_count()
        share=[Q((actual>>t)&1,count) if count else Q() for t in range(n)]
        membership=incidence.bit_count()
        rows=[]
        for t in range(n):
            floor=Q(1,n) if membership==7 else private[t] if membership==1 else shared[t]
            rows.append(share[t]-floor)
        for j in range(7):
            rows.append(share[-1]-Q((incidence>>j)&1,earlier.bit_count()+1))
        p=(actual&((1<<(n-2))-1)).bit_count(); d=(actual>>(n-2))&1
        for j in range(7):
          for k in range(j,7):
            comparison=((incidence>>j)&1)+((incidence>>k)&1)
            rows.append(share[-2]+share[-1]+Q(d,(p+1)*(p+2))-(Q(comparison,p+comparison) if comparison else Q()))
        residual=Q(int(bool(count)))-Q(1,2)-sum((w*r for w,r in zip(weights,rows)),Q())
        assert residual>=0,(n,incidence,actual,residual)
        cases+=1
        if residual<minimum: minimum,witness=residual,(incidence,actual)
    assert cases==cert['columns'] and minimum==Q(cert['minimum_residual'])
    return {'n':n,'literal_columns':cases,'minimum_residual':str(minimum),'minimum_type':witness}

if __name__=='__main__':
    tail=[Q(3,4),Q(2,19),Q(11,133),Q(6,665)]
    package=json.loads(Path(__file__).with_name('n7_n8_exact_duals.json').read_text())
    records=[literal_check(cert) for cert in package]
    files={name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
           for name in ('seven_tail_audit.py','n7_n8_exact_duals.json','seven_maxima_seven_plus.md')}
    print(json.dumps({'status':'passed','small_literal_certificates':records,
                      'tail_compressed_coefficients':[check(n,tail) for n in range(9,13)],
                      'source_sha256':files},indent=2))
