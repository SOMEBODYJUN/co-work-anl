"""Discovery relaxation for ROW3, not an SPE solver or a proof by sampling.

All 19008 membership/histogram types are included. Any eventual certificate
must be rationalized and independently reconstructed before claiming a bound.
"""
from itertools import product
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog


def comps(n,k):
    if k==1:
        yield (n,)
    else:
        for v in range(n+1):
            for z in comps(n-v,k-1):
                yield (v,)+z


TRS=np.array(list(product((0,1),repeat=3)),dtype=float)
HIST=np.array(list(comps(5,8)),dtype=float)


def coeffs(p,c,d,e,h):
    t,r,s=TRS.T
    jt,jr,js=h@TRS
    cur=c/(p+c+d+e) if c else 0.
    vd=d/(p+c+d+e) if d else 0.
    ve=e/(p+c+d+e) if e else 0.
    dt=h@(t/(p+t+r+s+((t+r+s)==0)))
    vr=h@(r/(p+t+r+s+((t+r+s)==0)))
    vs=h@(s/(p+t+r+s+((t+r+s)==0)))
    H=vd+ve+d/((p+c+1)*(p+c+2))
    Hi=vr+vs+h@(r/((p+t+1)*(p+t+2)))
    rows={"current:sumT":5*cur-dt}
    menus={"C":5*c,"D":5*d,"E":5*e,"T":jt,"R":jr,"S":js}
    for name,total in menus.items():
        rows['actual:D:'+name]=5*vd-total/(p+c+2)
        rows['actual:E:'+name]=5*ve-total/(p+c+d+1)
        rows['query:R:'+name]=5*vr-total*(h@(1/(p+t+2)))
        rows['query:S:'+name]=5*vs-total*(h@(1/(p+t+r+1)))
    rows['query:R:ownT']=vr-h@(t/(p+t+2))
    rows['query:R:ownS']=vr-h@(s/(p+t+2))
    rows['query:S:ownT']=vs-h@(t/(p+t+r+1))
    rows['query:S:ownR']=vs-h@(r/(p+t+r+1))
    # Ordered pairs, including equal indices, from any pair of five menus.
    for ix,(name,m) in enumerate(menus.items()):
        for name2,n in list(menus.items())[ix:]:
            num1=m*(5-n)+(5-m)*n
            num2=2*m*n
            rows['actual:tax:'+name+name2]=25*H-num1/(p+c+1)-num2/(p+c+2)
            rows['query:tax:'+name+name2]=25*Hi-num1*(h@(1/(p+t+1)))-num2*(h@(1/(p+t+2)))
    # Diagonal first comparator is query-specific and hence retains correlation.
    for name,n in menus.items():
        num1=t*(5-n)+(1-t)*n
        num2=2*t*n
        rows['query:tax:ownT:'+name]=5*Hi-h@(num1/(p+t+1)+num2/(p+t+2))
    # Proposed crossed-real-reply elimination, currently under independent review.
    rows['query:decorrelation_with_refund']=dt-(jt/5)*(h@(1/(p+r+s+1)))+h@(r*(1-s)/((p+t+1)*(p+t+2)))
    w=float(p+c+d+e>0)
    obj=float(jt>0)-dt
    return rows,w,obj


def main():
    states=[]; cols=[]; ws=[]; objs=[]; names=None
    for p in range(3):
        for c,d,e in product((0,1),repeat=3):
            for h in HIST:
                rr,w,obj=coeffs(p,c,d,e,h)
                if names is None:names=list(rr)
                assert list(rr)==names
                cols.append(list(rr.values())); ws.append(w); objs.append(obj)
                states.append((p,c,d,e,h.astype(int).tolist()))
    mat=np.array(cols).T
    res=linprog(-np.array(objs),A_ub=-mat,b_ub=np.zeros(len(names)),A_eq=[ws],b_eq=[1.],bounds=(0,None),method='highs')
    out={'status':int(res.status),'message':res.message,'types':len(states),'rows':len(names),'scope':'necessary-condition relaxation only; not full SPE'}
    if res.success:
        out['max_O_minus_row_over_W']=float(-res.fun)
        out['positive_rows']={n:float(-z) for n,z in zip(names,res.ineqlin.marginals) if z < -1e-8}
        out['support']=[{'state':st,'weight':float(z)} for st,z in zip(states,res.x) if z>1e-8]
    path=Path(__file__).with_suffix('.json')
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='support'}))


if __name__=='__main__':main()
