"""Genuine root-to-D four-follower envelope at the old necessary point.

No histories are identified by equal counts. All new action labels are those of
the fixed full strategy after root D. A failed extension is not a game search.
"""
import itertools
import json
import argparse
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

ROOT=Path(__file__).resolve().parents[6]
SOURCE=ROOT/'evidence/certificates/customer_attraction/five_player_indexed_bound.json'
THIRD=list(itertools.product((0,1),repeat=3))
SECOND=list(itertools.product((0,1),repeat=4))

def sh(n,d):return F(n,d) if n else F(0)

def rows(atom,new,root=3):
    fixed=list(map(int,atom['bits']))
    a,b,c,d,e,u,v,w,x,y=fixed
    path=[fixed[root],*new]
    total=sum(path)
    own=[sh(z,total) for z in path]
    ua=[sh(z,sum(fixed[:5])) for z in fixed[:5]]
    j=sum(cnt*tt for cnt,(tt,rr,ss) in zip(atom['AB_hist'],THIRD))
    out={'rootIC':ua[0]-own[0]}
    menus=[]
    for k,(ell,h) in enumerate(atom['menus_lh']):menus.append((f'old{k}',ell))
    for fam,types in (('AB',THIRD),('AE',THIRD),('second',SECOND)):
        for bit in range(1,len(types[0])):
            menus.append((f'{fam}{bit}',sum(cnt*typ[bit] for cnt,typ in zip(atom[fam+'_hist'],types))))
    # Every successor at the root deviation is genuinely optimizing.
    for pos in range(1,5):
        before=sum(path[:pos]);den=before+5-pos
        for name,z in zip('ABCDEUVWXY',fixed):out[f'new:{pos}:fixed:{name}']=own[pos]-sh(z,den)
        for name,z in zip('FGHI',new):out[f'new:{pos}:new:{name}']=own[pos]-sh(z,den)
        out[f'new:{pos}:opt']=5*own[pos]-sh(j,den)
        for name,count in menus:out[f'new:{pos}:menu:{name}']=5*own[pos]-sh(count,den)
    # Every old genuine optimizer can compare every new catalog theme.
    paths=(('actual',fixed[:5],range(5)),('secondE',[a,e,u,v,w],range(2,5)),('thirdE',[a,b,e,x,y],range(3,5)))
    for family,oldpath,positions in paths:
        for pos in positions:
            val=sh(oldpath[pos],sum(oldpath));den=sum(oldpath[:pos])+5-pos
            for name,z in zip('FGHI',new):out[f'{family}:{pos}:new:{name}']=val-sh(z,den)
    for k,oldbg in enumerate((a+b+c,a+e+u,a+b+e)):
        ell,h=atom['menus_lh'][k]
        for name,z in zip('FGHI',new):out[f'oldmenu{k}:new:{name}']=sh(ell-5*z,oldbg+1)+sh(j*z-h,(oldbg+1)*(oldbg+2))
    for fam,offset in (('AB',a+b),('AE',a+e)):
        for name,z in zip('FGHI',new):
            vals=[F(0),F(0)]
            for cnt,(tt,rr,ss) in zip(atom[fam+'_hist'],THIRD):
                vals[0]+=cnt*(sh(rr,offset+tt+rr+ss)-sh(z,offset+tt+2))
                vals[1]+=cnt*(sh(ss,offset+tt+rr+ss)-sh(z,offset+tt+rr+1))
            for pos,val in enumerate(vals,4):out[f'{fam}:{pos}:new:{name}']=val
    for name,z in zip('FGHI',new):
        vals=[F(0)]*3
        for cnt,(tt,hh,ii,jj) in zip(atom['second_hist'],SECOND):
            den=a+tt+hh+ii+jj
            vals[0]+=cnt*(sh(hh,den)-sh(z,a+tt+3))
            vals[1]+=cnt*(sh(ii,den)-sh(z,a+tt+hh+2))
            vals[2]+=cnt*(sh(jj,den)-sh(z,a+tt+hh+ii+1))
        for pos,val in enumerate(vals,3):out[f'second:{pos}:new:{name}']=val
    return out

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--simple',action='store_true');args=parser.parse_args()
    pr=json.loads(SOURCE.read_text())['primal'];atoms=pr['atoms']
    masses=[F(int(z['mass_numerator']),int(pr['denominator'])) for z in atoms]
    states=list(itertools.product((0,1),repeat=4))
    coeffs=[[rows(atom,state) for state in states] for atom in atoms]
    if args.simple:
        for group in coeffs:
            for co in group:co['AE:4:sumFGH']=sum(co[f'AE:4:new:{name}'] for name in 'FGH')
        names=['rootIC','new:4:fixed:E','actual:0:new:I','AE:4:sumFGH','second:3:new:I']
    else:names=list(coeffs[0][0])
    cols=[co for group in coeffs for co in group]
    mat=np.array([[float(col[name]) for col in cols] for name in names])
    eq=np.kron(np.eye(len(atoms)),np.ones((1,len(states))))
    obj=np.zeros(len(cols)+1);obj[-1]=1
    sol=linprog(obj,A_ub=np.column_stack((-mat,-np.ones(len(names)))),b_ub=np.zeros(len(names)),
                A_eq=np.column_stack((eq,np.zeros(len(atoms)))),b_eq=np.array(list(map(float,masses))),
                bounds=[(0,None)]*len(cols)+[(None,None)],method='highs')
    assert sol.success
    weights={name:F(round(float(-z)*10**8),10**8) for name,z in zip(names,sol.ineqlin.marginals) if abs(z)>1e-9}
    maxima=[max(sum(weight*co[name] for name,weight in weights.items()) for co in group) for group in coeffs]
    gap=sum(m*q for m,q in zip(masses,maxima))
    out={'scope':'Root-D necessary-condition envelope; not an SPE or half proof','root_topic':'D','minimax_violation':float(sol.fun),
         'rows':len(names),'variables':len(cols),'weights':{n:str(wt) for n,wt in weights.items()},'exact_gap':str(gap),'gap_float':float(gap),
         'maximums':list(map(str,maxima))}
    filename=Path(__file__).with_name('root_D_simple.json') if args.simple else Path(__file__).with_suffix('.json')
    filename.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='maximums'},indent=2))

if __name__=='__main__':main()
