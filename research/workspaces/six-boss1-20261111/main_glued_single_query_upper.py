"""Exact marginal-only upper bounds for new root versus old terminal queries.

The fixed root239 old-word/root law is part of the hypothesis.  A negative
upper bound excludes every gluing with those marginals, not all root laws.
"""
from pathlib import Path
from collections import defaultdict
from itertools import product
from fractions import Fraction as F
from hashlib import sha256
import json

W=Path(__file__).resolve().parent


def canonical(s):
    d={}
    return tuple(d.setdefault(a,len(d)) for a in s)


def main():
    pp=W/'union_augmented_lp/augmented_lp_exact.json'
    rp=W/'root_pair_joint_19662/joint_completion_exact.json'
    p=json.loads(pp.read_bytes());r=json.loads(rp.read_bytes())
    assert sha256(pp.read_bytes()).hexdigest()=='b0ca65cfe61e5e3ef09537cba2a986c171aeaa7106f673077f803c80ee2b68e3'
    hist={};own=defaultdict(dict);b4=defaultdict(dict)
    for j,c in enumerate(p['columns'][:4849]):
        if c['kind']=='hist':h=j;hist[h]=c
        elif c['kind']=='joint-reply':
            f,d,wi,wj=c['group']
            own[h].setdefault((f,d,tuple(wi),tuple(wj)),{})[tuple(c['state'])]=F(c['weight'])
        elif c['kind']=='actual-B-family-state' and c['source']==4:
            b4[c['hist_column']][tuple(c['hidden'])+(c['ell']//6,)]=F(c['weight'])
    y=defaultdict(F)
    for a in r['atoms']:
        h=a['hist'];m=F(a['mass'])
        for word,n in enumerate(hist[h]['hist']):
            if not n:continue
            for k in range(5):
                y[h,word,k]+=m*sum((a['new_words'][i]>>(4-k))&1 for i in range(6) if a['old_words'][i]==word)/n
    nodes=[e for e in product(range(2),range(6),range(6)) if e[0] or e[1]!=e[2]]
    orbits=defaultdict(list)
    for i in range(6):
        for f,j,k in nodes:orbits[f,canonical((i,j,k))].append((i,j,k))
    vals=defaultdict(F)
    for h,c in hist.items():
        H=F(c['weight']);a=list(map(int,c['actual_bits']));P=sum(a[:4])
        words=[t for t,n in enumerate(c['hist']) for _ in range(n)]
        bits=[tuple((t>>(2-k))&1 for k in range(3)) for t in words]
        for (f,ty),ii in orbits.items():
            for i,j,k in ii:
                s=own[h][f,int(j==k),bits[j],bits[k]]
                q=s[1,0]+s[1,1];z=s[0,1]+s[1,1];t=s[1,1]
                zp=(z-t)/F(P+1)+t/F(P+2)
                for l in range(5):
                    yl=y[h,words[i],l];assert 0<=yl<=H
                    vals['Z-to-Y',f,ty,l]+=(zp-yl/F(P+1)+min(q,yl)/F((P+1)*(P+2)))/len(ii)
        base=sum(a[:3])+a[5]+1
        H1=sum((v*s[0] for s,v in b4[h].items()),F())
        fp=sum((v*F(s[1],base+s[0]) for s,v in b4[h].items()),F())
        for i in range(6):
            for l in range(5):
                yl=y[h,words[i],l]
                vals['F-to-Y',l]+=(fp-yl/F(base)+min(H1,yl)/F(base*(base+1)))/6
    assert len(vals)==45
    out=dict(scope='Single-query Frechet upper bounds preserving the root239 full old-word/root marginals; negative excludes those marginals, not other root239 completions or the fixed point.',
        rows=[dict(query=k,upper=str(v),float=float(v)) for k,v in vals.items()],
        negative=sum(v<0 for v in vals.values()),zero=sum(v==0 for v in vals.values()),
        point_sha256=sha256(pp.read_bytes()).hexdigest(),root_sha256=sha256(rp.read_bytes()).hexdigest(),
        script_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        root_conditional_marginals=[dict(hist=h,word=w,tail_position=k,mass=str(v)) for (h,w,k),v in sorted(y.items())])
    target=W/'main_glued_single_query_upper.json'
    if target.exists():
        old=json.loads(target.read_bytes())
        for key in ('rows','negative','zero','point_sha256','root_sha256'):
            assert old[key]==json.loads(json.dumps(out[key]))
    target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('rows','root_conditional_marginals')},ensure_ascii=False))


if __name__=='__main__':main()
