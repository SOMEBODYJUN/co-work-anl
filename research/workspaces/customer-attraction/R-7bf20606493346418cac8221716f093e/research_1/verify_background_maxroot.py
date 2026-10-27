"""Independent exact reconstruction; Python standard library only."""
from fractions import Fraction
from itertools import product
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
source=json.loads((HERE/'background_maxroot_certificate.json').read_text())
weights={n:Fraction(v) for n,v in source['multipliers'].items()}
B=Fraction(source['B']);C=Fraction(source['C']);M=int(source['M'])
assert B>0 and all(x>=0 for x in weights.values()) and M==6
names='ZTABCDQRSXY'
paths={'actual':'TABCD','root':'TDQRS','second':'TADXY'}

def ratio(n,d):
    return Fraction(n,d) if n else Fraction(0)

def payoff(bits,path,position):
    return ratio(bits[path[position]],bits['Z']+sum(bits[s] for s in path))

def inequality(bits,covered,label):
    parts=label.split(':')
    if parts[0]=='CAP':
        return Fraction(bits['T']-bits[parts[1]])
    if parts[0]=='copy':
        position={'root':1,'second':2}[parts[1]]
        return payoff(bits,paths['actual'],position)-payoff(bits,paths[parts[1]],position)
    path=paths[parts[0]]
    if parts[1].isdigit():
        position=int(parts[1])+1
        earliest={'actual':1,'root':2,'second':3}[parts[0]]
        assert position>=earliest
        past=bits['Z']+sum(bits[s] for s in path[:position])
        remaining=5-position
        return payoff(bits,path,position)-ratio(bits[parts[3]],past+remaining)
    if parts[1]=='pairO':
        past=bits['Z']+sum(bits[s] for s in path[:3])
        current=payoff(bits,path,3)+payoff(bits,path,4)
        bonus=ratio(bits[path[3]],(past+1)*(past+2))
        return 3*(current+bonus)+ratio(past,past+1)-covered
    assert parts[1]=='lastO'
    past=bits['Z']+sum(bits[s] for s in path[:4])
    return 6*payoff(bits,path,4)+ratio(past,past+1)-covered

minimum=None;count=0;zero=0
for bits in product((0,1),repeat=11):
    b=dict(zip(names,bits));res=[]
    for covered in (0,1):
        remainder=B*payoff(b,paths['actual'],0)+C*b['T']-covered
        remainder-=sum(w*inequality(b,covered,n) for n,w in weights.items())
        assert remainder>=0,(bits,covered,remainder)
        minimum=remainder if minimum is None else min(minimum,remainder)
        zero+=remainder==0;count+=1;res.append(remainder)
    assert res[0]==res[1]
union_weight=sum(w for n,w in weights.items() if n.endswith('O'))
assert union_weight==1
print(json.dumps({'passed':True,'states':count,'positive_multipliers':len(weights),
 'minimum_residual':str(minimum),'zero_states':zero,'union_weight':str(union_weight),
 'B':str(B),'C':str(C)},indent=2))
