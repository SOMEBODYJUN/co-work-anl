"""Reconstruct mixed-pair rows by labeled i,j,k integer sums.

Does not use the compact moment formulas to compute reference coefficients.
All d-compatible triplet histograms and all distinct background cases checked.
"""
import json
from pathlib import Path
from itertools import product
import numpy as np
import mixed_pair as m


def share60(num,den):
    den=np.maximum(den,1)
    assert np.all((num==0)|(60%den==0))
    return num*(60//den)


def literal(a,d):
    words=np.array([tuple(z for n,z in zip(h,m.fp.PATTERNS) for _ in range(n)) for h in m.fp.HISTS[d]],dtype=np.int64)
    p=sum(a[:3]);pa=p+a[3];whole=sum(a)
    t,b,c=words[:,:,0],words[:,:,1],words[:,:,2]
    u4=m.div60(a[3],whole);u6=m.div60(a[5],whole)
    hstar=m.div60(a[4]+a[5],whole)+m.div60(a[4],(pa+1)*(pa+2))
    z=p+t+b+c;v=share60(c,z)
    h=share60(b+c,z)+share60(b,(p+t+1)*(p+t+2))
    rows=[]
    for s in m.SPECS:
        row=np.zeros(len(words),dtype=np.int64)
        if s[0]=='source':row=6*u4-share60(t,z).sum(axis=1)
        elif s[0]=='price':row=6*u6-share60(words[:,:,s[1]],sum(a[:5])+1).sum(axis=1)
        elif s[0]=='cap':row=-60*words[:,:,s[1]].sum(axis=1)
        elif s[0]=='actual_pair':
            _,x,y,e=s
            for j,k in product(range(6),repeat=2):
                if (j==k)!=(e=='diag'):continue
                xx,yy=words[:,j,x],words[:,k,y]
                row+=hstar-share60(xx+yy,pa+1)+share60(xx*yy,(pa+1)*(pa+2))
        elif s[0]=='last':
            _,x,e=s
            for i,j in product(range(6),repeat=2):
                if (i==j)!=(e=='diag'):continue
                row+=v[:,i]-share60(words[:,j,x],p+t[:,i]+b[:,i]+1)
        else:
            _,x,y,e=s
            for i,j,k in product(range(6),repeat=3):
                relation='iii' if i==j==k else 'iij' if i==j else 'iji' if i==k else 'ijj' if j==k else 'ijk'
                if relation!=e:continue
                xx,yy=words[:,j,x],words[:,k,y];q=p+t[:,i]
                row+=h[:,i]-share60(xx+yy,q+1)+share60(xx*yy,(q+1)*(q+2))
        rows.append(row)
    return np.array(rows)


def run():
    cases=0
    for p,a4,a5,a6 in product(range(4),(0,1),(0,1),(0,1)):
        a=(1,)*p+(0,)*(3-p)+(a4,a5,a6)
        for d in range(7):
            direct=literal(a,d);compact=m.matrix(a,d)
            assert np.array_equal(direct,compact),(a,d,np.argwhere(direct!=compact)[0])
            cases+=compact.shape[1]
    out={'status':'all compact row formulas equal labeled i,j,k reconstruction',
         'row_families':len(m.SPECS),'customer_reply_configurations':cases,
         'scope':'complete histogram domain; all 32 distinct actual background/tail cases; all rows scale60 integers'}
    (Path(__file__).parent/'verify_mixed_pair.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':run()
