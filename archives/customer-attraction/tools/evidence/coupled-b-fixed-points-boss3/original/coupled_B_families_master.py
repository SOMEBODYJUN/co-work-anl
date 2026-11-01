"""All actual sources 2/3/4->B, sharing complete old Ti/Bi/Ci histograms.

Each family keeps its entire true follower path; every genuine new follower
queries the three old theme families, and old Bi/Ci query each new follower.
No cross-family hidden products are included. Fixed16 hist support only.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json,sys,time
import numpy as np
from scipy.optimize import linprog
from coupled_B_branch_master import base,nr,branch_rows,share
HERE=Path(__file__).resolve().parent

def cross(a,h,hidden,source):
    i=source-1;seq=a[:i]+(a[5],)+hidden;den=sum(seq);p=sum(a[:3])
    means=[sum(F(count*word[j],6) for word,count in zip(nr.PAT,h)) for j in range(3)]
    vals=[]
    for k,t in enumerate(hidden,1):
        pos=i+k;dd=6-pos+sum(seq[:pos]);v=share(t,den)
        vals += [v-avg/F(dd) for avg in means]
    vb=sum(F(count,6)*share(word[1],p+sum(word)) for word,count in zip(nr.PAT,h))
    vc=sum(F(count,6)*share(word[2],p+sum(word)) for word,count in zip(nr.PAT,h))
    floorB=sum(F(count,6*(p+word[0]+2)) for word,count in zip(nr.PAT,h))
    floorC=sum(F(count,6*(p+word[0]+word[1]+1)) for word,count in zip(nr.PAT,h))
    vals += [vb-t*floorB for t in hidden]+[vc-t*floorC for t in hidden]
    return vals

def build(sources=(2,3,4)):
    cols,names,m,obj,norm=base.build();hist=[j for j,c in enumerate(cols) if c['kind']=='hist'];offset=len(cols);families=[]
    for source in sources:
        states=list(product(tuple(product(range(2),repeat=6-source)),(0,6)));start=len(cols)
        for hj in hist:
            for hidden,ell in states:cols.append({'kind':'actual-B-family-state','source':source,'hist_column':hj,'hidden':list(hidden),'ell':ell})
        families.append((source,states,start))
    added=len(cols)-offset
    for row in m:row.extend([F()]*added)
    obj.extend([F()]*added);norm.extend([F()]*added)
    for source,states,start in families:
        bn,_=branch_rows((0,)*7,(source-1,5),(0,)*(6-source),0,0);nextra=5*(6-source)
        block=[[F()]*len(cols) for _ in range(len(bn)+nextra)]
        for i,name in enumerate(bn):
            if name.startswith('CAP:'):block[i][0]=F(1)
        equations=[]
        for hi,hj in enumerate(hist):
            c=cols[hj];a=tuple(map(int,c['actual_bits']));d=c['d'];h=tuple(c['hist']);eq=[F()]*len(cols);eq[hj]=-F(1)
            for si,(hidden,ell) in enumerate(states):
                col=start+hi*len(states)+si;eq[col]=F(1)
                nn,vals=branch_rows(a+(0,),(source-1,5),hidden,d,ell);assert nn==bn
                vals+=cross(a,h,hidden,source);assert len(vals)==len(block)
                for i,v in enumerate(vals):block[i][col]=v
            equations.append(eq)
        names += [f'actualB-{source}-explicit:'+name for name in bn]+[f'actualB-{source}-cross:'+str(i) for i in range(nextra)]
        m.extend(block)
        for i,eq in enumerate(equations):
            names += [f'actualB-{source}-marginal:'+str(i),f'actualB-{source}-marginal-reverse:'+str(i)];m += [eq,[-v for v in eq]]
    return cols,names,m,obj,norm

def main():
    start=time.time();cols,names,m,obj,norm=build();print('built',len(m),'rows',len(cols),'columns',time.time()-start,flush=True)
    if '--verify' in sys.argv:
        j=json.loads((HERE/'coupled_B_families_exact.json').read_text());ys=[F(c['weight']) for c in j['columns']]
        assert min(ys)>=0 and sum(x*y for x,y in zip(norm,ys))==1
        slacks=[sum(x*y for x,y in zip(row,ys)) for row in m];assert min(slacks)>=0
        W=sum(x*y for x,y in zip(obj,ys));assert W==F(j['W']);print({'rows':len(m),'W':str(W),'minimum_slack':str(min(slacks))});return
    mat=np.array([[float(v) for v in row] for row in m]);sc=np.max(abs(mat),axis=1);sc[sc==0]=1
    sol=linprog([float(v) for v in obj],A_ub=-mat/sc[:,None],b_ub=np.zeros(len(m)),A_eq=[[float(v) for v in norm]],b_eq=[1],bounds=(0,None),method='highs',options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
    out={'scope':'actual sources2/3/4->B jointly coupled with old indexed branches; fixed16hist support only, not SPE or universal bound','success':bool(sol.success),'status':sol.message,'W':sol.fun,'rows':len(m),'columns':len(cols),'seconds':time.time()-start}
    print(json.dumps(out,indent=2),flush=True)
    if sol.success and sol.fun<.5:
        exact=base.cl.exact_point(cols,names,m,obj,norm,sol.x);exact['scope']=out['scope'];target=HERE/'coupled_B_families_exact.json'
        if target.exists():raise FileExistsError(target)
        target.write_text(json.dumps(exact,indent=2)+'\n');out['exact_verified']=True
    target=HERE/'coupled_B_families_status.json'
    if target.exists():raise FileExistsError(target)
    target.write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
