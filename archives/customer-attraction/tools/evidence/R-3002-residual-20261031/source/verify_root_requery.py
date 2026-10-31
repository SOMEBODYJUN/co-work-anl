"""Independent raw integer coefficient reconstruction for root query graphs.

No LP or discovery module is imported. All coefficient signs use int64;
the program bounds the maximum accumulation well below 2**63.
"""
import argparse,json
from fractions import Fraction
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent


def scan(data):
    names=data['names'];paths=data['paths'];first=data['first_genuine']
    copies={f'COPY:{s}:{i}:{t}':(s,i,t) for s,i,t in data['copy_edges']}
    lam=data['multipliers_numerators'];D=data['denominator'];z=data['equality_numerator']
    assert all(isinstance(v,int) and v>=0 for v in lam.values())
    assert 60*(D+abs(z)+12*sum(lam.values())) < 2**63
    low=None;zero=0;count=0
    for start in range(0,1<<len(names),32768):
        codes=np.arange(start,min(start+32768,1<<len(names)),dtype=np.int64)
        b={a:((codes>>i)&1) for i,a in enumerate(names)}
        def load(path):return sum((b[a] for a in path),np.zeros_like(codes))
        def share(n,d):return np.where(n,60*n//np.maximum(d,1),0)
        pc={}
        def pay(tag,i):
            key=(tag,i)
            if key not in pc:pc[key]=share(b[paths[tag][i]],load(paths[tag]))
            return pc[key]
        def row(key):
            p=key.split(':')
            if p[0]=='CAP':return 60*b[p[1]]
            if p[0]=='COPY':
                s,i,t=copies[key]
                assert paths[s][:i]==paths[t][:i]
                assert i>=first[s]
                assert first[t]==i+1
                return pay(t,i)-pay(s,i)
            tag=int(p[1]);path=paths[tag]
            if p[0]=='SAFE':
                i=int(p[2]);q=p[3]
                assert i>=first[tag]
                return share(b[q],load(path[:i])+6-i)-pay(tag,i)
            if p[0]=='LASTO':
                assert first[tag]<=5
                prefix=load(path[:5])
                return -6*pay(tag,5)-share(prefix,prefix+1)
            if p[0]=='PAIRO':
                assert first[tag]<=4
                prefix=load(path[:4])
                h=pay(tag,4)+pay(tag,5)+share(b[path[4]],(prefix+1)*(prefix+2))
                return -3*h-share(prefix,prefix+1)
            raise ValueError(key)
        rho=D*pay(0,0)-60*z*b['T']
        for k,v in lam.items():rho+=v*row(k)
        lo=int(rho.min());low=lo if low is None else min(low,lo)
        zero+=int(sum(rho==0));count+=len(codes)
    a=Fraction(sum(v for k,v in lam.items() if k.startswith(('LASTO:','PAIRO:'))),D)
    beta=Fraction(z-sum(v for k,v in lam.items() if k.startswith('CAP:')),D)
    return {'states':count,'min_residual_numerator':low,'zero_types':zero,'a':str(a),'beta':str(beta)}


def main():
    p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('--make',action='store_true');args=p.parse_args()
    path=Path(args.input)
    inp=json.loads(path.read_text())
    if args.make:
        D=10**10
        data={k:inp[k] for k in ['names','paths','first_genuine','copy_edges']}
        data.update(denominator=D,equality_numerator=round(inp['eq_dual']*D),
                    multipliers_numerators={k:round(v*D) for k,v in inp['active_dual'].items()})
        initial=scan(data)
        eps=max(0,(-initial['min_residual_numerator']+59)//60)
        for a in data['names']:
            if a!='T':
                key='CAP:'+a
                data['multipliers_numerators'][key]=data['multipliers_numerators'].get(key,0)+eps
        data['equality_numerator']-=eps
        data['rounding_cap_boost_numerator']=eps
        output=path.with_name(path.stem+'_exact.json')
    else:data=inp;output=path
    result=scan(data)
    assert result['min_residual_numerator']>=0
    result.update(evidence='exact full-literal-domain nonnegative coefficient certificate',
                  conclusion='u1 >= a OPT_6 + beta K',status='local necessary inequality; not half theorem')
    data['verification']=result
    output.write_text(json.dumps(data,indent=2))
    print(json.dumps(result))


if __name__=='__main__':main()
