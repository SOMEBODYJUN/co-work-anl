#!/usr/bin/env python3
"""Main's proposed next-family source check; zero optimization, no input change."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from hashlib import sha256
import json

HERE=Path(__file__).resolve().parent
N=257
vec=lambda d:[F(d.get(str(j),'0')) for j in range(N)]
dot=lambda a,b:sum((x*y for x,y in zip(a,b)),F(0))

def m25(p,n,t,q):
    return F(n+1,2)*t+F(24*t,p+n+1)+F(q,p+1+n*t)

def cost(p,n,t,q,o):
    c=F(n+1,2);D=p+n+1
    if t is not None and q is not None:return m25(p,n,t,q)
    if t is not None:return c*t+F(24*t,D)+F(o,6*(p+1+n*t))
    if q is not None:return F(q,p+1)+F(o,6)*(c+F(24,D)-F(n*q,(p+1)*D))
    return o*(c/6+F(4,D)+F(1,6*(p+1)))

def main():
    inp=json.loads((HERE/'exact_input.json').read_text())
    cert=json.loads((HERE/'exact_certificate.json').read_text())
    assert sha256((HERE/'exact_input.json').read_bytes()).hexdigest()=='3b2065e702c5590d50ebc8acd5ea30337e82db2a84585f87040acd36e91db553'
    assert sha256((HERE/'exact_certificate.json').read_bytes()).hexdigest()=='5e5a2377ed780f4a9c9f58ca8703fc5a473d41ea1945a654aa0ee6c0efa0deda'
    states=minima=menus=mixed=0
    for i in range(1,6):
        n=6-i
        for p in range(i):
            for t,q in product((0,1),repeat=2):
                values=[]
                for tails in product((0,1),repeat=n):
                    s,z=sum(tails[:-1]),tails[-1];den=p+t+s+z
                    phi=(F(25*t-z,den) if den else F(0))+F(s,2)+z+F(q,p+t+s+1)
                    values.append(phi);states+=1
                assert min(values)==m25(p,n,t,q)
                minima+=1
            for menu in product((0,1),repeat=6):
                o=int(any(menu));d=sum(menu)
                exact=sum((m25(p,n,menu[k],menu[l]) for k in range(6) for l in range(6) if k!=l),F(0))/30
                assert exact>=cost(p,n,None,None,o);menus+=1
                for b in (0,1):
                    assert sum((m25(p,n,b,q) for q in menu),F(0))/6>=cost(p,n,b,None,o)
                    assert sum((m25(p,n,t,b) for t in menu),F(0))/6>=cost(p,n,None,b,o)
                    mixed+=2
    assert (states,minima,menus,mixed)==(456,60,960,3840)
    oldrows={r['name']:r for r in inp['raw_rows']};atoms=inp['atom_columns'];z=vec(cert['primal'])
    checks=0;values={};tight_values={}
    for row in inp['raw_rows'][225:545]:
        i,T,Q=row['source'],row['T'],row['Q'];n=6-i;c=F(n+1,2)
        new=[];cap=[]
        for a in atoms:
            bits=a['a'];roles=bits+[a['x']];p=sum(bits[:i-1]);load=sum(bits)
            t=roles[T-1] if T<8 else None;q=roles[Q-1] if Q<8 else None
            ui=F(bits[i-1],load) if load else F(0)
            new.append(25*ui-cost(p,n,t,q,a['o']))
            cap.append(-F(t) if t is not None else -F(a['o'],6))
        new.append(c);cap.append(F(1))
        safe=vec(oldrows[f'SAFE_{i}_{T}']['a'])
        old=vec(row['a'])
        assert all(old[j]==new[j]+6*safe[j]+F(n-1,2)*cap[j] for j in range(N))
        checks+=N
        v=dot(new,z);values[row['name'].replace('PORTFOLIO31','PORTFOLIO25')]=str(v)
        if row['name'] in cert['dual']['row_weights']:
            assert dot(old,z)==0 and v<0
            tight_values[row['name'].replace('PORTFOLIO31','PORTFOLIO25')]=str(v)
    assert checks==320*257
    result={'status':'PASS','optimizer_calls':0,'new_rows_added_to_v5':0,'scope':'Prospective Main 25-family source diagnostic; not used for the frozen v5 optimization or global identity.',
        'literal_states':states,'exact_minima':minima,'menu30_cases':menus,'mixed_menu_cases':mixed,
        'full257_column_decompositions_checked':checks,
        'formula':'R31_i(T,Q)=R25_i(T,Q)+6 SAFE_i(T)+(n-1)/2 CAP(T)',
        'CAP_mean_semantics':'K-O/6 is a weakening of the average of six real legal size caps, not a synthetic O action.',
        'negative25_rows_at_v5_point':sum(F(v)<0 for v in values.values()),
        'three_tight31_rows_replaced_values':tight_values,
        'all320_v5_values':values}
    (HERE/'source25_diagnostic.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='all320_v5_values'},indent=2))

if __name__=='__main__':main()
