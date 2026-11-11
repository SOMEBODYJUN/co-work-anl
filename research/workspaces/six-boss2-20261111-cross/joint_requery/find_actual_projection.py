"""Find an actual-signature local-cone witness; does not construct an SPE."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog
from explore_projection import features, BASE_NAMES, div

HERE=Path(__file__).resolve().parent
THETA={'sourceT':F(50142),'sourceC':F(21056),'cap:b':F(925),'last1:q':F(6052),'last1:j':F(2782),'last1:v':F(4014),'last2:b':F(4004),'safeJ:v':F(924),'pair1:j,v':F(736)}


def main():
    minima={}
    for p in range(4):
        for t,q in product((0,1),repeat=2):
            vals=[]
            for h in product((0,1),repeat=4):
                fs,_=features(p,p,t,q,*h)
                vals.append(sum(THETA[n]*fs[n] for n in THETA))
            minima[p,t,q]=min(vals)
    names=BASE_NAMES+[f'actualprice:{x}' for x in ['t','q']+[f'a{i}' for i in range(6)]]+[f'actualcap:{x}' for x in ['t','q']+[f'a{i}' for i in range(6)]]
    columns=[];rows=[];costs=[]
    for a in product((0,1),repeat=6):
        p,ell=sum(a[:3]),sum(a[:5]);r,u=div(a[3],sum(a)),div(a[5],sum(a))
        for t,q in product((0,1),repeat=2):
            for h in product((0,1),repeat=4):
                fs,bud=features(p,ell,t,q,*h)
                bits={'t':t,'q':q,**{f'a{i}':a[i] for i in range(6)}}
                coef=[fs[n]-bud[n][0]*r-bud[n][1]*u for n in BASE_NAMES]
                coef.extend(div(bits[x],ell+1)-u for x in bits)
                coef.extend(F(bits[x]) for x in bits)
                columns.append((a,t,q,h));rows.append(coef)
                costs.append(71198*r-minima[p,t,q])
    Kcoef=[-bud[n][2] for n in BASE_NAMES]+[0]*8+[-1]*8
    A=np.column_stack((np.array(rows,dtype=float).T,Kcoef))
    objective=np.array(costs+[F(925)],dtype=float)
    eq=np.ones((1,len(columns)+1));eq[0,-1]=0
    res=linprog(objective,A_ub=A,b_ub=np.zeros(len(names)),A_eq=eq,b_eq=[1],bounds=(0,None),method='highs')
    assert res.success,res.message
    support=[]
    mass=[]
    for ci,value in enumerate(res.x[:-1]):
        if value>1e-9:
            w=F(float(value)).limit_denominator(10**8)
            a,t,q,h=columns[ci]
            support.append({'a':a,'t':t,'q':q,'hidden':h,'mass':str(w)})
            mass.append((ci,w))
    K=F(float(res.x[-1])).limit_denominator(10**8)
    slacks={n:-sum(w*rows[ci][ni] for ci,w in mass)-Kcoef[ni]*K for ni,n in enumerate(names)}
    newslack=sum(w*costs[ci] for ci,w in mass)+925*K
    r=sum(w*div(columns[ci][0][3],sum(columns[ci][0])) for ci,w in mass)
    u=sum(w*div(columns[ci][0][5],sum(columns[ci][0])) for ci,w in mass)
    out={'scope':'Actual six-bit signature with 34 rows plus actual terminal prices and capacities; local relaxation only, not an SPE.', 'theta_integer':{n:str(w) for n,w in THETA.items()},'source_sum':71198,'K':str(K),'r_u4':str(r),'u6':str(u),'sum_mass':str(sum(w for _,w in mass)),'min_old_slack':str(min(slacks.values())),'new_slack_integer_scale':str(newslack),'new_slack_normalized':str(newslack/71198),'new_slack_float':res.fun,'support':support,'slacks':{n:str(v) for n,v in slacks.items()},'minima_integer_scale':{str(key):str(value) for key,value in minima.items()}}
    (HERE/'actual_signature_witness.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('support','slacks','minima_integer_scale')},ensure_ascii=False,indent=2));print('support',len(support));print(json.dumps(support,ensure_ascii=False))
    assert out['sum_mass']=='1'
    assert min(slacks.values())>=0
    assert newslack<0


if __name__=='__main__':main()
