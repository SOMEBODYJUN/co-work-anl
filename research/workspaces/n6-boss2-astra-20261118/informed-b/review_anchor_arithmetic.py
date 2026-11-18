"""Independent integer replay of the 41 anchored rows. No author code imported."""
from fractions import Fraction
from itertools import product
import hashlib
import json
from math import lcm
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PACK = ROOT / 'tools/evidence/six-fractional-cover-49-10'
PIN = '1430755204c6a154ab87204214bdecc1295303731478efb28cfcaa86cff6e8f5'
FREEZE = ROOT / f'research/runs/n6-boss2-astra-20261118/studio/freezes/SIX-ANCHOR-49-10-R1/{PIN}.json'
manifest = json.loads(FREEZE.read_bytes())
for item in manifest['content_refs']:
    assert hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest() == item['sha256']

data = json.loads((PACK/'anchor-menu-49-10-certificate.json').read_bytes())
alpha = Fraction(data['coverage_coefficient'])
weights = {k:{r:Fraction(v) for r,v in w.items()} for k,w in data['weights'].items()}
den = lcm(alpha.denominator, *(v.denominator for w in weights.values() for v in w.values()))
multipliers = {k:{r:int(v*den) for r,v in w.items()} for k,w in weights.items()}
assert all(v>0 for w in multipliers.values() for v in w.values())
assert 2*alpha>1 and Fraction(data['tau'])==Fraction(49,10)
# Scale 600 is a multiple of all denominators including (49/10)*1/c.
scale=600
def scaled_pay(bits, pos):
    return 0 if not bits[pos] else scale//sum(bits)
def subtotal(group, source, bits, anchor, o, tails):
    result=0
    for name, mult in multipliers[group].items():
        if name[0]=='F':
            i=int(name[1:]); assert i>source
            val=49*scaled_pay(bits,i)//10-o*(scale//(6-i+sum(bits[:i])))
        elif name[0]=='H':
            i,j=map(int,name[1:].split('-')); assert i>source and j==7+len(tails)-1
            val=scaled_pay(bits,i)-bits[-1]*(scale//(6-i+sum(bits[:i])))
        elif name[0]=='R':
            assert source<4 and name=='R1/2'
            p=sum(bits[:4])
            val=49*scaled_pay(bits,4)//10+scaled_pay(bits,5)//2-o*(scale//(1+p))
            if not p and bits[4]:val+=o*(scale//4)
        elif name=='IC-own':
            assert source>=0
            val=scaled_pay(anchor[:6],source)-scaled_pay(bits,source)
        else:
            assert name.startswith('CAP')
            j=int(name[3:])
            q=tails[j] if source>=0 else anchor[j]
            val=scale*(anchor[6]-q)
        result+=mult*val
    return result

branches=[(0,6),(1,6),(2,6),(2,4),(3,5)]
assert set(multipliers)=={'actual'}|{f'{i}:{j}' for i,j in branches}
residuals=[]; cases=0
for anchor in product(range(2),repeat=7):
    for o in (0,1):
        e=anchor[:6]
        score=subtotal('actual',-1,e,anchor,o,())
        for i,j in branches:
            local=[]
            for tail in product(range(2),repeat=5-i):
                leaf=e[:i]+(anchor[j],)+tail
                local.append(subtotal(f'{i}:{j}',i,leaf,anchor,o,tail))
                cases+=1
            score+=max(local)
        gap=scale*(den*int(any(e))-int(den*alpha)*o)-score
        assert gap>=0
        residuals.append(gap)
print(json.dumps({'verified_file_refs':len(manifest['content_refs']), 'rows':sum(map(len,multipliers.values())),
    'anchors':len(residuals),'tails':cases,'zero_anchors':residuals.count(0),'minimum':str(min(residuals)),
    'minimum_positive':str(Fraction(min(q for q in residuals if q>0),scale*den))},indent=2))
