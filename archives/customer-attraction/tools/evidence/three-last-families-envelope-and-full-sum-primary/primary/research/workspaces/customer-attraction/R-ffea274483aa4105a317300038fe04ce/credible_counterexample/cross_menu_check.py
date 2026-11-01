"""Exact additional common-catalog last-node rows at the indexed obstruction.
Reads frozen input. Writes no shared asset. Candidate discovery, not universal theorem.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[5]
SOURCE=ROOT/'evidence/certificates/customer_attraction/five_player_indexed_bound.json'
p=json.loads(SOURCE.read_text());atoms=p['primal']['atoms'];D=int(p['primal']['denominator'])
triples=list(product((0,1),repeat=3));quads=list(product((0,1),repeat=4))

def menus(z):
    out={f'L_{r}':z['menus_lh'][i][0] for i,r in enumerate(('actual','second','third'))}
    for g in ('AB','AE'):
        hist=z[g+'_hist']
        out[g+'_R']=sum(n*r for n,(t,r,s) in zip(hist,triples))
        out[g+'_S']=sum(n*s for n,(t,r,s) in zip(hist,triples))
    hist=z['second_hist']
    for j,label in enumerate(('T','H','I','J')):
        out['second_'+label]=sum(n*bits[j] for n,bits in zip(hist,quads))
    return out

def own_and_inverse(z,g):
    bits=list(map(int,z['bits']));a,b,c,d,e,u,v,w,x,y=bits
    own=inv=F(0)
    if g in ('AB','AE'):
        background=a+(b if g=='AB' else e)
        for n,(t,r,s) in zip(z[g+'_hist'],triples):
            denom=background+t+r+1
            own+=F(n*s,denom);inv+=F(n,denom)
    else:
        for n,(t,h,i,j) in zip(z['second_hist'],quads):
            denom=a+t+h+i+1
            own+=F(n*j,denom);inv+=F(n,denom)
    return own,inv

rows=[]
for g in ('AB','AE','second'):
    ownfamilies={g+'_R',g+'_S'} if g!='second' else {'second_H','second_I','second_J'}
    for target in menus(atoms[0]):
        if target=='second_T' or target in ownfamilies:continue
        slack=sum((F(int(z['mass_numerator']),D)*(5*own_and_inverse(z,g)[0]-menus(z)[target]*own_and_inverse(z,g)[1]) for z in atoms),F(0))
        rows.append({'source':g,'comparison_menu':target,'slack':str(slack),'slack_float':float(slack)})
print(json.dumps({'rows':rows,'violations':[r for r in rows if F(r['slack'])<0]},indent=2))
