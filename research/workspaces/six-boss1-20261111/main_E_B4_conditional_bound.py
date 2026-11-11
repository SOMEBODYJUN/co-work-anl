"""Main: exact nested Z/H1 transport diagnostic at the new cb45 point.

No optimization.  A zero old H2-to-Z marginal upper bound forces maximal
Z/H1 overlap; only on that certified face is the sharper E/H1 bound used.
This excludes an E marginal completion, never the underlying old point.
"""
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
PP=HERE/'full624_augmented_lp/recovery/augmented_lp_exact.json'
EP=HERE/'z_successor_20910/exact_certificate.json'
LP=HERE/'z_successor_20910/symbolic_lift.json'
assert sha256(PP.read_bytes()).hexdigest()=='cb45ee6f8df153764c91bd77d0543527cc44719ff7cc43646ffce06a7921a932'
assert sha256(EP.read_bytes()).hexdigest()=='00c78a5f23de4ff30d5fc66af362d95767a8b67c101dfa863ad701cffa225c30'
assert sha256(LP.read_bytes()).hexdigest()=='76573a43318fd55f38b5ccab8eee04b4c2e2bb7f54ea5b68a4c5bc4930f6c48b'
point=json.loads(PP.read_bytes()); exact=json.loads(EP.read_bytes()); lift=json.loads(LP.read_bytes())
hist={};rz=defaultdict(dict);b4=defaultdict(dict)
def group(g):
    f,d,wi,wj=g
    return f,d,tuple(wi),tuple(wj)
for j,c in enumerate(point['columns'][:4849]):
    if c['kind']=='hist':h=j;hist[h]=c
    elif c['kind']=='joint-reply':rz[h,group(c['group'])][tuple(c['state'])]=F(c['weight'])
    elif c['kind']=='actual-B-family-state' and c['source']==4:
        b4[c['hist_column']][tuple(c['hidden'])+(c['ell']//6,)]=F(c['weight'])
for (h,g),ss in rz.items():ss[0,0]=F(hist[h]['weight'])-sum(ss.values(),F())
ee=defaultdict(dict)
for c,x in zip(lift['new_columns'],exact['new_values']):
    key=(c['hist_column'],group(c['group']))
    ee[key][tuple(c['old_state'])]=F(x)
assert set(ee)==set(rz)
for key,ss in ee.items():
    assert set(ss)==set(product((0,1),repeat=2))
    assert all(0<=v<=rz[key][s] for s,v in ss.items())
nodes=[(f,i,j) for f,i,j in product(range(2),range(6),range(6)) if f or i!=j]
orbits=defaultdict(list)
for e in nodes:orbits[e[0],int(e[1]==e[2])].append(e)
BF=F()
for h,c in hist.items():
    a=tuple(map(int,c['actual_bits']));d=sum(a[:3])+a[5]+1
    assert sum(b4[h].values(),F())==F(c['weight'])
    BF+=sum((m*F(s[1],d+s[0]) for s,m in b4[h].items()),F())
rows=[]
for orbit,indices in sorted(orbits.items()):
    old=BF;plain=BF;nested=BF;blocks=[]
    for h,c in hist.items():
        a=tuple(map(int,c['actual_bits']));d=sum(a[:3])+a[5]+1
        words=[w for w,n in zip(product((0,1),repeat=3),c['hist']) for _ in range(n)]
        high=sum((m*s[0] for s,m in b4[h].items()),F())
        for f,i,j in indices:
            key=(h,(f,int(i==j),words[i],words[j]));ss=rz[key];xx=ee[key]
            z=ss[0,1]+ss[1,1];e=sum(xx.values(),F());ez=xx[0,1]+xx[1,1]
            zh=min(z,high);eh0=min(e,high)
            eh1=min(ez,zh)+min(e-ez,high-zh)
            assert 0<=eh1<=eh0 and 0<=ez<=min(e,z)
            fac=F(1,len(indices));tax=F(1,d*(d+1))
            old-=fac*(z/d-zh*tax)
            plain-=fac*(e/d-eh0*tax)
            nested-=fac*(e/d-eh1*tax)
            blocks.append(dict(hist=h,node=(f,i,j),Z=z,H1=high,E=e,EZ=ez,
                               forced_ZH1=zh,plain_EH1_upper=eh0,nested_EH1_upper=eh1,
                               strict_improvement=eh1<eh0))
    rows.append(dict(orbit=orbit,old_H2_to_Z_upper=old,
                     saturation_certified=old==0,plain_H2_to_E_upper=plain,
                     nested_H2_to_E_upper=nested if old==0 else None,
                     improvement=plain-nested if old==0 else None,
                     strict_blocks=sum(b['strict_improvement'] for b in blocks),blocks=blocks))

def serial(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):serial(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [serial(v) for v in x]
    return x
out=dict(scope='Fixed cb45 plus fixed own RZE completion; nested bound only where old H2-to-Z upper is exactly zero.',
         point_sha256=sha256(PP.read_bytes()).hexdigest(),E_certificate_sha256=sha256(EP.read_bytes()).hexdigest(),
         script_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),histograms=len(hist),
         zero_histograms=[h for h,c in hist.items() if F(c['weight'])==0],true_H2_income=BF,rows=rows,
         optimizer_calls=0,no_original_point_exclusion=True)
(HERE/'main_E_B4_conditional_bound.json').write_text(json.dumps(serial(out),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(serial([{k:v for k,v in r.items() if k!='blocks'} for r in rows]),ensure_ascii=False,indent=2))
