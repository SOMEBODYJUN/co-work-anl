"""Joint actual4->B Q/R identity with the explicit old Ti,Bi,Ci histogram.

Read-only use of research_5's current master build. Only this directory may
receive outputs. Fixed 16-histogram support: no full-domain claim if infeasible.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json,sys,time
import numpy as np
from scipy.optimize import linprog

HERE=Path(__file__).resolve().parent
if '--latest' not in sys.argv:sys.argv.append('--latest')
sys.path.insert(0,str(HERE.parent/'research_5'))
import combined_branch_master as base
import new_reply_budget as nr
from max_branch_lp import branch_rows

def share(bit,den):return F(bit,den) if bit else F(0)
def cross_rows(a,h,q,r):
    p=sum(a[:3]);b=a[5];den=p+b+q+r
    vq=share(q,den);vr=share(r,den)
    means=[sum(F(count*word[j],6) for word,count in zip(nr.PAT,h)) for j in range(3)]
    vals=[]
    for avg in means:vals.append(vq-avg/F(p+b+2))
    for avg in means:vals.append(vr-avg/F(p+b+q+1))
    vb=sum(F(count,6)*share(word[1],p+sum(word)) for word,count in zip(nr.PAT,h))
    vc=sum(F(count,6)*share(word[2],p+sum(word)) for word,count in zip(nr.PAT,h))
    floorB=sum(F(count,6*(p+word[0]+2)) for word,count in zip(nr.PAT,h))
    floorC=sum(F(count,6*(p+word[0]+word[1]+1)) for word,count in zip(nr.PAT,h))
    vals += [vb-q*floorB,vb-r*floorB,vc-q*floorC,vc-r*floorC]
    return vals

def build():
    cols,names,m,obj,norm=base.build();hist=[j for j,c in enumerate(cols) if c['kind']=='hist']
    offset=len(cols);states=list(product(range(2),range(2),(0,6)))
    for hj in hist:
        for q,r,ell in states:cols.append({'kind':'actual-B-branch-state','hist_column':hj,'Q':q,'R':r,'ell':ell})
    added=len(cols)-offset
    for row in m:row.extend([F()]*added)
    obj.extend([F()]*added);norm.extend([F()]*added)
    bn,_=branch_rows((0,)*7,(3,5),(0,0),0,0)
    block=[[F()]*len(cols) for _ in range(len(bn)+10)]
    for i,name in enumerate(bn):
        if name.startswith('CAP:'):block[i][0]=F(1)
    equations=[]
    for hi,hj in enumerate(hist):
        c=cols[hj];a=tuple(map(int,c['actual_bits']));d=c['d'];h=tuple(c['hist']);eq=[F()]*len(cols);eq[hj]=-F(1)
        for si,(q,r,ell) in enumerate(states):
            col=offset+hi*len(states)+si;eq[col]=F(1)
            nn,vals=branch_rows(a+(0,),(3,5),(q,r),d,ell);assert nn==bn
            vals+=cross_rows(a,h,q,r)
            for i,v in enumerate(vals):block[i][col]=v
        equations.append(eq)
    names += ['actualB-explicit:'+name for name in bn]+['actualB-cross:'+str(i) for i in range(10)]
    m.extend(block)
    for i,eq in enumerate(equations):
        names += ['actualB-marginal:'+str(i),'actualB-marginal-reverse:'+str(i)]
        m += [eq,[-v for v in eq]]
    return cols,names,m,obj,norm

def main():
    start=time.time();cols,names,m,obj,norm=build();print('built',len(m),'rows',len(cols),'columns',time.time()-start,flush=True)
    if '--verify' in sys.argv:
        j=json.loads((HERE/'coupled_B_master_exact.json').read_text());ys=[F(c['weight']) for c in j['columns']]
        assert min(ys)>=0 and sum(x*y for x,y in zip(norm,ys))==1
        slacks=[sum(x*y for x,y in zip(row,ys)) for row in m];assert min(slacks)>=0
        W=sum(x*y for x,y in zip(obj,ys));assert W==F(j['W']);print({'rows':len(m),'W':str(W),'minimum_slack':str(min(slacks))});return
    mat=np.array([[float(v) for v in row] for row in m]);sc=np.max(abs(mat),axis=1);sc[sc==0]=1
    sol=linprog([float(v) for v in obj],A_ub=-mat/sc[:,None],b_ub=np.zeros(len(m)),A_eq=[[float(v) for v in norm]],b_eq=[1],bounds=(0,None),method='highs',options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
    out={'scope':'same SPE actual4->B joint Q/R identity with explicit Ti/Bi/Ci graph; fixed16 hist support only, not SPE or universal bound','success':bool(sol.success),'status':sol.message,'W':sol.fun,'rows':len(m),'columns':len(cols),'seconds':time.time()-start}
    print(json.dumps(out,indent=2),flush=True)
    if sol.success and sol.fun<.5:
        exact=base.cl.exact_point(cols,names,m,obj,norm,sol.x);exact['scope']=out['scope']
        target=HERE/'coupled_B_master_exact.json'
        if target.exists():raise FileExistsError(target)
        target.write_text(json.dumps(exact,indent=2)+'\n');out['exact_verified']=True
    target=HERE/'coupled_B_master_status.json'
    if target.exists():raise FileExistsError(target)
    target.write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
