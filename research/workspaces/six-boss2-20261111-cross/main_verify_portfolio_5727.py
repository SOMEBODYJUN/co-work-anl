"""Main's separate exact construction of discounted cuts.
Uses literal six indices, literal middle bits and four deterministic policies.
It imports none of the discovering agent's modules or row helpers.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
from collections import defaultdict
import hashlib,json,time
B=Path(__file__).resolve().parent
pointpath=B/'master_cuts/dynamic_5727_exact.json';packpath=B/'coverage_bridge/new5727_single_portfolio_cut.json'
point=json.loads(pointpath.read_text());pack=json.loads(packpath.read_text());cols=point['columns'];x=[F(c['weight']) for c in cols]
assert hashlib.sha256(pointpath.read_bytes()).hexdigest()==pack['input_sha256']
PATS=list(product((0,1),repeat=3))
def share(a,b):return a/b if a else F(0)

def psi_from_policies(edges,theta,initial):
    options=[[],[]]
    for c0,c1 in product((0,1),repeat=2):
        a=1-theta*(c0==0);b=-theta*(c0==1)
        c=-theta*(c1==0);d=1-theta*(c1==1)
        det=a*d-b*c
        v0=(edges[0,c0]*d-b*edges[1,c1])/det
        v1=(a*edges[1,c1]-c*edges[0,c0])/det
        options[0].append(v0);options[1].append(v1)
    v=list(map(min,options))
    for t in (0,1):assert v[t]==min(edges[t,c]+theta*v[c] for c in (0,1))
    return (1-theta)*v[initial]

def rebuild(rec):
    pars={k:F(v) for k,v in rec['parameters'].items()};theta=F(rec['theta']);source=rec['source']-1;middle=4-source;orb=tuple(rec['orbit']);member=rec['member'];ct=6 if orb[1] else 30
    assert min(pars.values())>=0 and 0<=theta<1
    row=[F(0)]*len(cols);row[0]=middle*pars.get('beta_mid',F(0))+pars.get('beta_last',F(0))
    blocks=[];cur=None
    for ci,col in enumerate(cols):
        if col['kind']=='hist':cur=[ci,col,[]];blocks.append(cur)
        elif col['kind']=='joint-reply':cur[2].append((ci,col))
    comparisons=0
    @lru_cache(None)
    def project(a,words,i,j,state):
        p=sum(a[:source]);ell=sum(a[:5]);others=[l for l in range(6) if l not in {i,j}]
        qs={f'A{l+1}':F(a[l]) for l in range(6)}
        qs.update(dict(zip(['Ti','Bi','Ci','Tj','Bj','Cj'],map(F,words[i]+words[j]))))
        qs.update(R=F(state[0]),Z=F(state[1]))
        for bit,name in enumerate(['other_T','other_B','other_C']):qs[name]=F(sum(words[l][bit] for l in others),len(others))
        e={}
        for t,c in product((0,1),repeat=2):
            vals=[]
            for midbits in product((0,1),repeat=middle):
                s=sum(midbits);z=p+t+s+c
                val=pars.get('source',F(0))*share(F(t),z)
                val+=pars.get('alpha_mid',F(0))*F(s,ell+1)+pars.get('alpha_last',F(0))*F(c,ell+1)
                val+=pars.get('beta_mid',F(0))*s+pars.get('beta_last',F(0))*c
                for name,w in pars.items():
                    if not name.startswith('mu_'):continue
                    label=name[3:];q=F(t) if label=='current' else qs[label]
                    val+=w*(q/(p+t+s+1)-share(F(c),z))
                vals.append(val)
            e[t,c]=min(vals)
        return psi_from_policies(e,theta,state[member])
    for hi,h,js in blocks:
        aa=tuple(map(int,h['actual_bits']));words=tuple(w for w,n in zip(PATS,h['hist']) for _ in range(n))
        pairs=[(i,j) for i in range(6) for j in range(6) if (i==j)==bool(orb[1])]
        assert len(pairs)==ct
        increments=defaultdict(F)
        value0=F(0)
        for i,j in pairs:
            z=project(aa,words,i,j,(0,0));value0+=z/ct
            for st in [(0,1),(1,0),(1,1)]:increments[(words[i],words[j],st)]+=(project(aa,words,i,j,st)-z)/ct
        row[hi]=pars.get('source',F(0))*share(F(aa[source]),sum(aa))+(middle*pars.get('alpha_mid',F(0))+pars.get('alpha_last',F(0)))*share(F(aa[5]),sum(aa))-value0
        for ci,col in js:
            f,d,wi,wj=col['group']
            if (f,d)==orb:row[ci]=-increments[(tuple(wi),tuple(wj),tuple(col['state']))]
    target=[F(0)]*len(cols)
    for ci,v in rec['row_nonzero']:target[ci]=F(v)
    assert target==row,[(i,str(a),str(b)) for i,(a,b) in enumerate(zip(target,row)) if a!=b][:3]
    value=sum((c*w for c,w in zip(row,x)),F(0));assert value==F(rec['exact_slack'])<0
    return {'source':source+1,'member':member,'orb':list(orb),'theta':str(theta),'exact_slack':str(value),'same_full_4849_coefficients':True,'row_sha256':hashlib.sha256(json.dumps(list(map(str,row)),separators=(',',':')).encode()).hexdigest()}
start=time.time();out=[]
for rec in pack['results']:
    if F(rec.get('exact_slack','0'))<0:out.append(rebuild(rec))
report={'status':'PASS','scope':'Separate literal-index/literal-middle/four-policy reconstruction of the one retained exact single-step portfolio row at the 5727 point; general validity from the same-source weak IC portfolio inequality, not just this finite check','input_sha256':pack['input_sha256'],'pack_sha256':hashlib.sha256(packpath.read_bytes()).hexdigest(),'rows':out,'seconds':time.time()-start}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
