"""Common maximum M root branch, retaining M and all followers vs old words.

This adds actual-price and old Ti/Bi/Ci identity correlations absent from
scalar maximum-root supporting lines. Fixed16 old histogram support only.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import sys,json,time
import numpy as np
from scipy.optimize import linprog
from coupled_B_families_master import build as previous_build,base,nr,branch_rows,share
HERE=Path(__file__).resolve().parent

def cross(a,h,m,hidden):
    seq=(m,)+hidden;den=sum(seq);p=sum(a[:3])
    means=[sum(F(count*word[j],6) for word,count in zip(nr.PAT,h)) for j in range(3)];vals=[]
    for pos,t in enumerate(hidden,1):
        dd=6-pos+sum(seq[:pos]);v=share(t,den);vals += [v-avg/F(dd) for avg in means]
    vb=sum(F(count,6)*share(word[1],p+sum(word)) for word,count in zip(nr.PAT,h));vc=sum(F(count,6)*share(word[2],p+sum(word)) for word,count in zip(nr.PAT,h))
    floorB=sum(F(count,6*(p+word[0]+2)) for word,count in zip(nr.PAT,h));floorC=sum(F(count,6*(p+word[0]+word[1]+1)) for word,count in zip(nr.PAT,h))
    queries=(m,)+hidden;vals += [vb-t*floorB for t in queries]+[vc-t*floorC for t in queries]
    return vals
def build():
    cols,names,rows,obj,norm=previous_build();hist=[j for j,c in enumerate(cols) if c['kind']=='hist'];states=list(product(range(2),tuple(product(range(2),repeat=5)),(0,6)));offset=len(cols)
    for hj in hist:
        for m,h,ell in states:cols.append({'kind':'maximum-root-family-state','hist_column':hj,'M':m,'hidden':list(h),'ell':ell})
    added=len(cols)-offset
    for row in rows:row.extend([F()]*added)
    obj.extend([F()]*added);norm.extend([F()]*added)
    bn,_=branch_rows((0,)*7,(0,6),(0,)*5,0,0);block=[[F()]*len(cols) for _ in range(len(bn)+6+27)]
    for i,name in enumerate(bn):
        if name.startswith('CAP:'):block[i][0]=F(1)
    size=[F()]*len(cols);size[0]=-F(1);eqs=[]
    for hi,hj in enumerate(hist):
        col=cols[hj];a=tuple(map(int,col['actual_bits']));d=col['d'];histogram=tuple(col['hist']);eq=[F()]*len(cols);eq[hj]=-F(1)
        for si,(m,h,ell) in enumerate(states):
            j=offset+hi*len(states)+si;eq[j]=F(1);size[j]=F(m)
            nn,vals=branch_rows(a+(m,),(0,6),h,d,ell);assert nn==bn
            actualpay=[share(t,sum(a)) for t in a]
            vals += [actualpay[i]-F(m,6-i+sum(a[:i])) for i in range(6)]
            vals += cross(a,histogram,m,h);assert len(vals)==len(block)
            for i,v in enumerate(vals):block[i][j]=v
        eqs.append(eq)
    names += ['maximum-root-explicit:'+name for name in bn]+['maximum-root-actual-M-price:'+str(i) for i in range(6)]+['maximum-root-old-word-cross:'+str(i) for i in range(27)];rows.extend(block)
    eqs.append(size)
    for i,eq in enumerate(eqs):names += ['maximum-root-equality:'+str(i),'maximum-root-equality-reverse:'+str(i)];rows += [eq,[-v for v in eq]]
    return cols,names,rows,obj,norm
def main():
    start=time.time();cols,names,rows,obj,norm=build();print('built',len(rows),'rows',len(cols),'columns',time.time()-start,flush=True)
    if '--verify' in sys.argv:
        report=json.loads((HERE/'maxroot_identity_exact.json').read_text());ys=[F(c['weight']) for c in report['columns']]
        assert min(ys)>=0 and sum(x*y for x,y in zip(norm,ys))==1
        slacks=[sum(x*y for x,y in zip(row,ys)) for row in rows];assert min(slacks)>=0
        W=sum(x*y for x,y in zip(obj,ys));assert W==F(report['W']);print({'W':str(W),'minimum_slack':str(min(slacks))});return
    mat=np.array([[float(v) for v in row] for row in rows]);sc=np.max(abs(mat),axis=1);sc[sc==0]=1
    sol=linprog([float(v) for v in obj],A_ub=-mat/sc[:,None],b_ub=np.zeros(len(rows)),A_eq=[[float(v) for v in norm]],b_eq=[1],bounds=(0,None),method='highs',options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
    out={'scope':'maximum-root M identity and actual-B families vs old Ti/Bi/Ci identities; fixed16hist support only, not SPE or universal bound','success':bool(sol.success),'status':sol.message,'W':sol.fun,'rows':len(rows),'columns':len(cols),'seconds':time.time()-start};print(json.dumps(out,indent=2),flush=True)
    if sol.success and sol.fun<.5:
        exact=base.cl.exact_point(cols,names,rows,obj,norm,sol.x);exact['scope']=out['scope'];target=HERE/'maxroot_identity_exact.json'
        if target.exists():raise FileExistsError(target)
        target.write_text(json.dumps(exact,indent=2)+'\n');out['exact_verified']=True
    target=HERE/'maxroot_identity_status.json'
    if target.exists():raise FileExistsError(target)
    target.write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
