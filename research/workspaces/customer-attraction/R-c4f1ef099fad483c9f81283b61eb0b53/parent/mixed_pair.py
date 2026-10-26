"""Six-provider fourth-source indexed terminal and mixed-pair comparisons.

Every row is an SPE necessary inequality. Float LP only discovers multipliers;
reported cuts use integer coefficients and the full compatible histogram domain.
No strategy sufficiency or half-coverage conclusion is inferred from feasibility.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
import json, sys
import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p/'work.py').exists())
PREV = ROOT/'research/workspaces/customer-attraction/R-964def22ed03479582e83410444f2ea2/parent'
OLD = ROOT/'research/workspaces/customer-attraction/R-d1fe1e0c444e40d68b6813bf88db8fba'
sys.path[:0] = [str(PREV), str(OLD/'parent')]
import fourth_indexed_projection as fp
import joint_system as js
PAT = np.array(fp.PATTERNS, dtype=np.int64)
TYPES = [(a,d) for a in product((0,1), repeat=6) for d in range(7)]
PAIRS = [(x,y) for x in range(3) for y in range(x,3)]
SPECS = [('source',)]
SPECS += [('price',x) for x in (1,2)] + [('cap',x) for x in (1,2)]
SPECS += [('actual_pair',x,y,e) for x,y in PAIRS for e in ('diag','off')]
SPECS += [('last',x,e) for x in range(3) for e in ('diag','off')]
SPECS += [('branch_pair',x,y,e) for x,y in PAIRS
          for e in ('iii','iij','iji','ijj','ijk')]
CAP = np.array([360 if s[0]=='cap' else 0 for s in SPECS], dtype=np.int64)


def div60(n,d):
    if not n: return 0
    assert d and 60 % d == 0, (n,d)
    return n*(60//d)


@lru_cache(None)
def structural(p,pa,d):
    """Rows excluding actual-payoff constants, all scaled by 60."""
    out = []
    for hist in fp.HISTS[d]:
        totals = np.array(hist) @ PAT
        both = {(x,y):sum(n*z[x]*z[y] for n,z in zip(hist,PAT)) for x,y in PAIRS}
        row=[]
        source = sum(-n*div60(int(t),p+int(t+b+c)) for n,(t,b,c) in zip(hist,PAT))
        for s in SPECS:
            kind=s[0]
            if kind=='source': row.append(source)
            elif kind in ('price','cap'):
                # Price uses a different denominator for each actual atom;
                # leave its negative membership count here, complete later.
                row.append(-int(totals[s[1]])*(60 if kind=='cap' else 1))
            elif kind=='actual_pair':
                _,x,y,e=s
                sx,sy,xy=int(totals[x]),int(totals[y]),int(both[x,y])
                if e=='diag': row.append(-div60(sx+sy,pa+1)+div60(xy,(pa+1)*(pa+2)))
                else: row.append(-5*div60(sx+sy,pa+1)+div60(sx*sy-xy,(pa+1)*(pa+2)))
            else:
                acc=0
                for n,z in zip(hist,PAT):
                    if not n: continue
                    t,b,c=map(int,z);den=p+t+b+1
                    if kind=='last':
                        _,x,e=s;xx=int(z[x]);sx=int(totals[x])
                        v=div60(c,p+t+b+c)
                        acc += n*((v-div60(xx,den)) if e=='diag' else (5*v-div60(sx-xx,den)))
                    else:
                        _,x,y,e=s
                        xx,yy=int(z[x]),int(z[y]);sx,sy=int(totals[x]),int(totals[y]);xy=int(both[x,y])
                        h=div60(b+c,p+t+b+c)+div60(b,(p+t+1)*(p+t+2))
                        fden=p+t+1;gden=(p+t+1)*(p+t+2)
                        if e=='iii': mult,num,over=1,xx+yy,xx*yy
                        elif e=='iij': mult,num,over=5,5*xx+sy-yy,xx*(sy-yy)
                        elif e=='iji': mult,num,over=5,sx-xx+5*yy,(sx-xx)*yy
                        elif e=='ijj': mult,num,over=5,sx-xx+sy-yy,xy-xx*yy
                        else: mult,num,over=20,4*(sx-xx+sy-yy),(sx-xx)*(sy-yy)-(xy-xx*yy)
                        acc+=n*(mult*h-div60(num,fden)+div60(over,gden))
                row.append(acc)
        out.append(row)
    return np.array(out,dtype=np.int64).T


def matrix(a,d):
    p=sum(a[:3]);pa=p+a[3];whole=sum(a);ell=sum(a[:5])
    u4=div60(a[3],whole);u6=div60(a[5],whole)
    h=div60(a[4]+a[5],whole)+div60(a[4],(pa+1)*(pa+2))
    mat=structural(p,pa,d).copy()
    for j,s in enumerate(SPECS):
        if s[0]=='source':mat[j]+=6*u4
        elif s[0]=='price':mat[j]*=60//(ell+1);mat[j]+=6*u6
        elif s[0]=='actual_pair':mat[j]+=(6 if s[-1]=='diag' else 30)*h
    return mat


def cut(weights):
    weights=np.array(weights,dtype=np.int64)
    assert min(weights)>=0
    vals=[int((weights@matrix(a,d)).max()) for a,d in TYPES]
    k=int(weights@CAP)
    norm=max(1,int(weights.max()))*60
    return [F(v,norm) for v in vals]+[F(k,norm)], vals, k, norm


def separate(record):
    masses={(tuple(map(int,z['actual_bits'])),z['d']):F(z['weight']) for z in record['support']}
    active=[(a,d,masses[a,d]) for a,d in TYPES if (a,d) in masses]
    mats=[matrix(a,d) for a,d,mass in active]
    ends=np.cumsum([0]+[m.shape[1] for m in mats]);mat=np.concatenate(mats,axis=1)
    eq=np.zeros((len(active),mat.shape[1]+1))
    for j,(lo,hi) in enumerate(zip(ends[:-1],ends[1:])):eq[j,lo:hi]=1
    aub=np.c_[-mat.astype(float),-np.ones(len(SPECS))]
    sol=linprog(np.r_[np.zeros(mat.shape[1]),1.],A_ub=aub,b_ub=CAP.astype(float)*float(F(record['K'])),
                A_eq=eq,b_eq=[float(z[2]) for z in active],bounds=(0,None),method='highs')
    assert sol.success,sol.message
    res={'phase_I_float':sol.fun,'rows':len(SPECS),'columns':mat.shape[1],
         'scope':'necessary response extension, not an SPE witness or half proof'}
    if sol.fun>1e-8:
        weights=np.rint(np.maximum(-sol.ineqlin.marginals,0)*10**10).astype(np.int64)
        cc,vals,k,norm=cut(weights)
        n=js.decode(record,TYPES)
        value=sum(x*y for x,y in zip(cc,n))
        if value>=0:
            res.update(discovery_rejected=True,exact_proposed_cut_slack=str(value),
                       weight_sum=int(weights.sum()),weights=[int(z) for z in weights])
            return res,None
        res.update(weights=[int(z) for z in weights],specs=[list(s) for s in SPECS],
                   exact_cut_slack=str(value),coefficients=[str(v) for v in vals],K_integer=k,norm=norm)
        return res,cc
    return res,None


def load_system():
    types,rows=js.build();assert types==TYPES
    old=json.loads((OLD/'parent/joint_system.json').read_text())
    for i,c in enumerate(old['menu_cuts']):rows.append(('same-menu-joint:'+str(i),js.from_weights(c['weights'])))
    for c in old['pair_cuts']:rows.append(js.row(types,{k:v for k,v in c.items() if k!='separation_slack'}))
    saved=json.loads((PREV/'fourth_indexed_projection.json').read_text())
    look={(tuple(map(int,z['actual_bits'])),z['d']):F(z['coefficient']) for z in saved['coefficients']}
    norm=F(saved['scale']*saved['integer_weights'][0])
    rows.append(('fourth-indexed-v1',[look[t]/norm for t in types]+[F()]))
    assert len(rows)==702
    return types,rows


def run():
    target=HERE/'mixed_pair_results.json'
    types,rows=load_system();record=json.loads((PREV/'combined_702.json').read_text())
    js.verify_primal(record,types,rows)
    results=[]
    for step in range(12):
        res,cc=separate(record);results.append(res)
        print('step',step,'W',float(F(record['W'])),'extension',res['phase_I_float'],flush=True)
        target.write_text(json.dumps({'status':'research necessary system, not half proof','steps':results,'certificate':record},indent=2)+'\n')
        if cc is None:break
        rows.append(('mixed-pair:'+str(step),cc))
        record,n=js.solve_primal(types,rows)
        if F(record['W'])>=F(1,2):print('HALF candidate requires full dual',flush=True);break
    target.write_text(json.dumps({'status':'research necessary system, not half proof','steps':results,'certificate':record},indent=2)+'\n')


if __name__=='__main__':run()
