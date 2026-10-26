"""Parent audit: reconstruct all new-reply rows by labeled indices.

Reads the witness, not the author's compact coefficient generator. Original
702 rows are replayed through their existing exact generator. New 137 rows
are independently computed with Fraction and literal ordered edge queries.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
import json,sys,hashlib
import mixed_pair as mix

HERE=Path(__file__).resolve().parent
OTHER=HERE.parent/'six_astra'


def frac(n,d):return F(n,d) if n else F()


def pattern(values):
    seen=[];out=[]
    for x in values:
        if x not in seen:seen.append(x)
        out.append(seen.index(x))
    return tuple(out)


def run():
    source=OTHER/'full_new_reply_closure_exact.json';data=json.loads(source.read_text());cols=data['columns']
    k=F(cols[0]['weight']);assert cols[0]['kind']=='K'
    histories={i:c for i,c in enumerate(cols) if c['kind']=='hist'}
    replies=defaultdict(dict)
    bounds=0
    for c in cols:
        if c['kind']=='new-reply':
            i=c['hist_column'];g=c['group'];key=(g[0],g[1],tuple(g[2]),tuple(g[3]));y=F(c['weight'])
            assert key not in replies[i];assert 0<=y<=F(histories[i]['weight'])
            replies[i][key]=y;bounds+=1
    raw=[F() for _ in range(37)];raw[5+15]=30*k;raw[5+16+15]=36*k
    extra=defaultdict(F);type_masses=defaultdict(F);edge_queries=0
    for index,c in histories.items():
        a=tuple(map(int,c['actual_bits']));d=c['d'];mass=F(c['weight']);h=c['hist']
        assert sum(h)==6
        words=[w for w,n in zip(product((0,1),repeat=3),h) for _ in range(n)]
        assert sum(w[0] for w in words)==d
        type_masses[a,d]+=mass
        p=sum(a[:3]);pa=sum(a[:4]);ell=sum(a[:5]);whole=sum(a)
        hactual=frac(a[4]+a[5],whole)+F(a[4],(pa+1)*(pa+2))
        u4=frac(a[3],whole);u6=frac(a[5],whole)
        vbs=[frac(b,p+t+b+c) for t,b,c in words]
        vcs=[frac(c,p+t+b+c) for t,b,c in words]
        hs=[vbs[i]+vcs[i]+F(words[i][1],(p+words[i][0]+1)*(p+words[i][0]+2)) for i in range(6)]
        raw[0]+=mass*(6*u4-sum(frac(t,p+t+b+c) for t,b,c in words))
        raw[1]+=mass*sum(hactual-F(b+c,pa+1)+F(b*c,(pa+1)*(pa+2)) for t,b,c in words)
        for i,(t,b,cc) in enumerate(words):
            for j,(_,bj,cj) in enumerate(words):
                if i!=j:
                    raw[2]+=mass*(vcs[i]-F(bj,p+t+b+1))
                    raw[4]+=mass*(hs[i]-F(bj+cj,p+t+1)+F(bj*cj,(p+t+1)*(p+t+2)))
                raw[3]+=mass*(vcs[i]-F(cj,p+t+b+1))
        edges=[(f,i,j) for f,i,j in product(range(2),range(6),range(6)) if f or i!=j]
        def r(e):
            f,i,j=e
            return replies[index][f,int(i==j),words[i],words[j]]
        def denominator(e):
            f,i,j=e
            return p+words[i][0]+words[j][1+f]+1
        for e in edges:
            f,i,j=e;t,b,cc=words[i];y=words[j][1+f];rm=r(e);de=denominator(e);off=5+16*f
            raw[off]+=mass*(vbs[i]-frac(y,p+t+y))+rm*frac(y,(p+t+y)*(p+t+y+1))
            query=(b,cc,t,F(d,6),*a,F(sum(z[1] for z in words),6),F(sum(z[2] for z in words),6))
            for z,q in enumerate(query,1):raw[off+z]+=rm/F(de)-mass*F(q,de)
            raw[off+13]+=mass*vcs[i]-rm/F(p+t+b+1)
            raw[off+14]+=mass*u6-rm/F(ell+1)
            raw[off+15]-=rm
            for v in edges:
                g,ii,jj=v
                extra['new-new',f,g,pattern((i,j,ii,jj))]+=(rm-r(v))/F(de)
                edge_queries+=1
            for kk,(tk,bk,ck) in enumerate(words):
                for q in range(3):
                    extra['new-old',f,q,pattern((i,j,kk))]+=rm/F(de)-mass*F(words[kk][q],de)
                extra['old-new',f,pattern((kk,i,j))]+=mass*vcs[kk]-rm/F(p+tk+bk+1)
    # Some impossible orbit classes produce zero rows. Reconstruct all 100.
    p3=sorted({pattern(x) for x in product(range(3),repeat=3)})
    p4=sorted({pattern(x) for x in product(range(4),repeat=4)})
    keys=[('new-new',f,g,pat) for f,g,pat in product(range(2),range(2),p4)]
    keys += [('new-old',f,q,pat) for f,q,pat in product(range(2),range(3),p3)]
    keys += [('old-new',f,pat) for f,pat in product(range(2),p3)]
    assert len(keys)==100
    assert min(raw)>=0,(raw.index(min(raw)),min(raw))
    assert min(extra[key] for key in keys)>=0
    record={'O':'1','W':data['W'],'K':str(k),'support':[{'actual_bits':''.join(map(str,a)),'d':d,'weight':str(v)} for (a,d),v in type_masses.items() if v]}
    types,rows=mix.load_system();mix.js.verify_primal(record,types,rows)
    assert F(record['W'])<F(1,2)
    report={'status':'parent literal reconstruction passed',
            'scope':'exact necessary-system stopping witness, not a game, SPE, half proof, or exact optimum',
            'original_exact_rows':702,'literal_raw_rows':37,'literal_index_class_rows':100,
            'reply_upper_bounds':bounds,'total_verified_rows':702+37+100+bounds,
            'literal_new_reply_comparisons':edge_queries,
            'W_over_O':record['W'],'strict_half_gap':str(1-2*F(record['W'])),
            'minimum_new_raw_slack':str(min(raw)),'minimum_closure_slack':str(min(extra[key] for key in keys)),
            'witness_sha256':hashlib.sha256(source.read_bytes()).hexdigest()}
    (HERE/'audit_full_closure.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2),flush=True)


if __name__=='__main__':run()
