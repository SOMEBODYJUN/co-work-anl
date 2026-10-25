"""Parent's exact mixed-five-menu audit; no discovery/pricing imports.

The finite input is a necessary-condition point, never a claimed SPE.
All hypergeometric coefficients and row evaluations are rational.
"""
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path
import json,hashlib

BASE=Path(__file__).resolve().parent.parent
source=BASE/'certificate/exact_current_source_own_index_v1.json'
raw=source.read_bytes(); data=json.loads(raw)
table=[list(map(F,(0,960,1220,1480,1740,2000))),
       list(map(F,(0,'1665/4','2745/4','3785/4','4825/4','5865/4'))),
       list(map(F,(0,320,524,728,932,1136)))]
choose=lambda n,k: comb(n,k) if 0<=k<=n else 0
def mixed(p,d,q,r):
    return sum((F(choose(d,s)*choose(5-d,r-s),choose(5,r))*
                table[p][s+(5-r)*q] for s in range(r+1)),F(0))
for p,d,q,r in product(range(3),range(6),range(2),range(6)):
    v=mixed(p,d,q,r)
    assert v>=F(r,5)*table[p][d]+F(5-r,5)*table[p][5*q]

records=[]
for a in data['atoms']:
    b=dict(zip('ABCDEUVWXY',map(int,a['bits'])))
    z=tuple(map(int,a['max_bits']));d=sum(a['AB_hist'][4:])
    queries={**b,**{f'z{i}':z[i] for i in range(5)}}
    banks={name:5*bit for name,bit in queries.items()}
    banks['OPT']=d
    for tag,field,k in [('AB','AB_hist',3),('AE','AE_hist',3),('S','second_hist',4)]:
        types=list(product((0,1),repeat=k))
        for j in range(1,k):
            banks[f'{tag}:{j}']=sum(n*t[j] for n,t in zip(a[field],types))
    div=lambda x,y:F(x,y) if x else F(0)
    contexts={
        'actual':(b['A']+b['B'],div(b['C'],sum(b[x] for x in 'ABCDE'))),
        'second':(b['A']+b['E'],div(b['U'],sum(b[x] for x in 'AEUVW'))),
        'max':(sum(z[:2]),div(z[2],sum(z)))}
    records.append((F(a['exact_mass']),z[0],d,queries,banks,contexts))

out=[]
for name in ('actual','second','max'):
    bankvalues={j:sum(mass*F(banks[j],ctx[name][0]+3)
                     for mass,M,d,queries,banks,ctx in records)
                for j in records[0][4]}
    best=max(bankvalues,key=bankvalues.get)
    base=sum(mass*(17040*ctx[name][1]+1085*M)
             for mass,M,d,queries,banks,ctx in records)-2679*bankvalues[best]
    for Q in records[0][3]:
        vals=[]
        for r in range(6):
            cost=sum(mass*mixed(ctx[name][0],d,queries[Q],r)
                     for mass,M,d,queries,banks,ctx in records)
            vals.append(base-cost)
        for r in range(1,5):
            if vals[r]<0:
                out.append({'source':name,'fixed_Q':Q,'optimal_slots':r,'J':best,
                            'slack':str(vals[r]),
                            'r0_slack':str(vals[0]),'r5_slack':str(vals[5]),
                            'both_endpoint_rows_nonnegative':min(vals[0],vals[5])>=0})
out.sort(key=lambda r:F(r['slack']))
report={'status':'PASS exact mixed-menu coefficients','source_sha256':hashlib.sha256(raw).hexdigest(),
        'coefficient_states':3*6*2*6,'negative_mixed_rows':len(out),
        'strict_vs_nonnegative_endpoints':sum(x['both_endpoint_rows_nonnegative'] for x in out),
        'negative_rows':out,
        'limitation':'A necessary-row point is not an SPE or HALF5 counterexample.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='negative_rows'}))
print(json.dumps(out[:3]))
