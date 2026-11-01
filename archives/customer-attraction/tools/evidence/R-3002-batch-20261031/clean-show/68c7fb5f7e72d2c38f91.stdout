"""Independent semantic/integer audit of research_4's root rows.

No author verifier or discovery code is imported. First merge every
repeated path-player payoff across all rows; then evaluate the reduced
symbolic expression over the complete membership cube.
"""
from pathlib import Path
from collections import defaultdict
from fractions import Fraction as F
import hashlib,json,sys
import numpy as np

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'research_4'

def audit(path):
    raw=path.read_bytes();data=json.loads(raw)
    paths=data['paths'];names=data['names'];first=data['first_genuine']
    edges={(s,i,t) for s,i,t in data['copy_edges']}
    weights=data['multipliers_numerators'];D=data['denominator'];z=data['equality_numerator']
    assert len(set(names))==len(names)
    assert set(names)==set(''.join(paths))
    assert all(len(P)==6 and P[0]=='T' for P in paths)
    assert first[0]==1
    pay=defaultdict(int);pay[0,0]=D
    cap=defaultdict(int);cap['T']=-z
    quotes=[];taxes=[];cross=[];opt=0
    for label,v in weights.items():
        assert isinstance(v,int) and v>=0
        p=label.split(':')
        if p[0]=='CAP':
            assert p[1] in names and p[1]!='T';cap[p[1]]+=v
        elif p[0]=='COPY':
            s,i,t=map(int,p[1:]);assert (s,i,t) in edges
            assert paths[s][:i]==paths[t][:i] and i>=first[s] and first[t]==i+1
            pay[t,i]+=v;pay[s,i]-=v
        elif p[0]=='SAFE':
            tag,i=int(p[1]),int(p[2]);q=p[3]
            assert i>=first[tag] and q in names
            pay[tag,i]-=v;quotes.append((v,q,paths[tag][:i],6-i))
        elif p[0]=='LASTO':
            tag=int(p[1]);assert first[tag]<=5
            pay[tag,5]-=6*v;taxes.append((-v,paths[tag][:5]));opt+=v
        elif p[0]=='PAIRO':
            tag=int(p[1]);assert first[tag]<=4
            pay[tag,4]-=3*v;pay[tag,5]-=3*v
            taxes.append((-v,paths[tag][:4]));cross.append((-3*v,paths[tag][4],paths[tag][:4]));opt+=v
        else:raise ValueError(label)
    # All denominators are divisors of 60. Each quote/payout is at most
    # 60; a tax is at most 60; a cross term is at most 30.
    bound=60*(sum(abs(v) for v in pay.values())+sum(abs(v) for v in cap.values())+
              sum(abs(v) for v,*_ in quotes)+sum(abs(v) for v,*_ in taxes)+sum(abs(v) for v,*_ in cross))
    assert bound<2**63
    lowest=None;lowest_nonzero=None;zeros=0;states=0
    for lo in range(0,1<<len(names),16384):
        codes=np.arange(lo,min(lo+16384,1<<len(names)),dtype=np.int64)
        bit={a:(codes>>i)&1 for i,a in enumerate(names)}
        def load(s):return sum((bit[a] for a in s),np.zeros_like(codes))
        def frac60(n,d):
            assert np.all((n==0)|(d>0))
            den=np.maximum(d,1)
            assert np.all((n==0)|(60%den==0))
            return n*(60//den)
        rho=np.zeros_like(codes)
        for a,v in cap.items():rho+=60*v*bit[a]
        for (tag,i),v in pay.items():
            if v:rho+=v*frac60(bit[paths[tag][i]],load(paths[tag]))
        for v,q,prefix,k in quotes:rho+=v*frac60(bit[q],load(prefix)+k)
        for v,prefix in taxes:
            b=load(prefix);rho+=v*frac60(b,b+1)
        for v,q,prefix in cross:
            b=load(prefix);rho+=v*frac60(bit[q],(b+1)*(b+2))
        value=int(rho.min());lowest=value if lowest is None else min(lowest,value)
        nz=rho[codes!=0]
        if len(nz):lowest_nonzero=int(nz.min()) if lowest_nonzero is None else min(lowest_nonzero,int(nz.min()))
        zeros+=int(np.count_nonzero(rho==0));states+=len(codes)
    a=F(opt,D);beta=F(z-sum(v for key,v in weights.items() if key.startswith('CAP:')),D)
    assert lowest>=0
    return {'file':path.name,'sha256':hashlib.sha256(raw).hexdigest(),'states':states,'rows':len(weights),
            'min_integer_residual':lowest,'min_nonzero_type_integer_residual':lowest_nonzero,'zero_types':zeros,
            'a':str(a),'beta':str(beta),'int64_absolute_bound':bound,
            'status':'independent full-cube coefficient and source-history semantic audit passed; local row only'}

if __name__=='__main__':
    names=sys.argv[1:] or ['root_requery_o4.2_exact.json','root_requery_third_L_o4.2_exact.json','root_requery_branch_D_o4.2_exact.json','root_requery_baseline_o4.2_exact.json']
    out={'scope':'independent reconstruction of local necessary inequalities; does not prove six-player half','checks':[audit(SOURCE/name) for name in names]}
    (HERE/'requery_merged_audit.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
