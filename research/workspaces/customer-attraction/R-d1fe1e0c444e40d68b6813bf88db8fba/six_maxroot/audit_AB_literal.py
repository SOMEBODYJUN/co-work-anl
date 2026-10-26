#!/usr/bin/env python3
"""Independent literal-index audit of the first complete AB projection.

No discovery or author's verification module is imported. Ordered i,j,l sums
are evaluated literally, before maximizing over the complete histogram set.
"""
from pathlib import Path
from itertools import product
from fractions import Fraction as F
import json,time

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'six_lift'

def compositions(total,bins):
    if bins==1:
        yield (total,);return
    for n in range(total+1):
        for rest in compositions(total-n,bins-1):yield (n,)+rest

def shr(bit,den):return 60//den if bit else 0

def literal(p,e,L):
    z=[p+sum(h) for h in e]
    D=[60//(p+sum(h[:3])+1) for h in e]
    A=[60//(p+sum(h[:2])+1) for h in e]
    G=[60//((p+sum(h[:2])+1)*(p+sum(h[:2])+2)) for h in e]
    H=[shr(h[2],zz)+shr(h[3],zz)+h[2]*gg for h,zz,gg in zip(e,z,G)]
    uc=[shr(h[3],zz) for h,zz in zip(e,z)]
    rows={
        'source':-sum(shr(h[0],zz) for h,zz in zip(e,z)),
        'cap:3':-60*sum(h[3] for h in e),
        'floorfamily:3:1:off':sum(uc[i]-e[l][1]*D[i] for i in range(6) for l in range(6) if i!=l),
        'floorfamily:3:2:off':sum(uc[i]-e[l][2]*D[i] for i in range(6) for l in range(6) if i!=l),
        'floorfamily:3:3:all':sum(uc[i]-e[l][3]*D[i] for i in range(6) for l in range(6)),
        'pairfamily:2:3:query_equal':sum(H[i]-(e[j][2]+e[j][3])*A[i]+e[j][2]*e[j][3]*G[i]
                                          for i in range(6) for j in range(6) if i!=j),
    }
    for q in (1,2):
        rows[f'pairfamily:{q}:{q}:all_distinct']=sum(
            H[i]-(e[j][q]+e[l][q])*A[i]+e[j][q]*e[l][q]*G[i]
            for i in range(6) for j in range(6) for l in range(6) if len({i,j,l})==3)
    constant=sum(L[k]*v for k,v in rows.items())
    answer={}
    for pf in range(p,p+3):
        score=constant
        for q in (1,2):
            v=sum(-(h[q]+h[3])*(60//(pf+1))+h[q]*h[3]*(60//((pf+1)*(pf+2))) for h in e)
            score+=L[f'fixedpair:actual:{q}:3']*v
        answer[pf]=score
    return answer

def run():
    start=time.time()
    raw=json.loads((SOURCE/'full_AB_extension.json').read_text())
    projected=json.loads((SOURCE/'AB_projected_row.json').read_text())
    L=raw['integer_row_weights'];assert len(L)==10 and all(v>0 for v in L.values())
    patterns=list(product((0,1),repeat=3))
    maxima={};count=0
    for d in range(7):
        hs0=list(compositions(6-d,8));hs1=list(compositions(d,8))
        for h0,h1 in product(hs0,hs1):
            e=[(t,)+pat for t,hist in ((0,h0),(1,h1)) for pat,mass in zip(patterns,hist) for _ in range(mass)]
            assert len(e)==6
            for p in range(3):
                scores=literal(p,e,L);count+=1
                for pf,value in scores.items():
                    key=(p,pf,d);maxima[key]=max(maxima.get(key,value),value)
        print('d',d,'histograms',len(hs0)*len(hs1),flush=True)
    lookup={}
    for bits in product((0,1),repeat=6):
        z=sum(bits);p=sum(bits[:2]);pf=sum(bits[:4])
        u3=shr(bits[2],z)
        H=shr(bits[4],z)+shr(bits[5],z)+bits[4]*(60//((pf+1)*(pf+2)))
        const=6*L['source']*u3+6*(L['fixedpair:actual:1:3']+L['fixedpair:actual:2:3'])*H
        for d in range(7):lookup[(''.join(map(str,bits)),d)]=const+maxima[p,pf,d]
    saved={(x['actual_bits'],x['d']):x['coefficient'] for x in projected['coefficients']}
    assert len(saved)==448 and saved==lookup
    kap=360*L['cap:3'];assert kap==raw['K_integer_coefficient']==projected['K_integer_coefficient']
    point=json.loads((SOURCE/'fixed_graph_priced.json').read_text())
    upper=F(kap)*F(point['K'])
    values=[]
    for s in point['support']:
        value=lookup[s['bits'][:6],s['d']];values.append(value);upper+=F(s['weight'])*value
    assert values==raw['per_fixed_type_integer_maxima']
    assert upper==F(raw['exact_upper_bound'])<0
    result=dict(verified=True,imports_discovery=False,imports_author_verifier=False,
                literal_histogram_backgrounds=count,complete_histograms_per_background=count//3,
                visible_coefficients=448,conditional_maxima=len(maxima),
                K_integer_coefficient=kap,exact_separation_upper=str(upper),elapsed_seconds=time.time()-start)
    (HERE/'AB_literal_audit.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2),flush=True)

if __name__=='__main__':run()
