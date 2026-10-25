"""Conditional true-maximum-theme root branch diagnostic, not a certificate.

A source necessary-condition primal is fixed. Its atoms may split among all
32 membership states of a largest legal theme M and its four true successors.
This relaxes global theme/history consistency and cannot certify a game.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
import argparse, hashlib, json
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csc_matrix, hstack

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'customer_attraction/__init__.py').exists())
DEFAULT=ROOT/'research/workspaces/customer-attraction/R-bfbfe64dd5f94fa09d36b75198633f2b/five_only/ap_binary_discovery.json'
LABELS='ABCDEUVWXY'; PATHS=('ABCDE','AEUVW','ABEXY'); START=(0,2,3)
STATES=list(product((0,1),repeat=5))
TY3=list(product((0,1),repeat=3)); TY4=list(product((0,1),repeat=4));TY5=list(product((0,1),repeat=5))
def q(a,b): return F(int(a),int(b)) if a else F(0)

def rows(atom,mb,include_ap=True):
    b=dict(zip(LABELS,map(int,atom['bits'])))
    d=sum(atom['AB_hist'][4:]); o=int(d>0); m=mb[0]; total=sum(mb)
    out={};actual=[q(b[t],sum(b[x] for x in PATHS[0])) for t in PATHS[0]]
    out['max:root:IC']=actual[0]-q(m,total)
    # One shared globally largest theme pays every cap.
    for t in LABELS: out[f'max:cap:{t}']=F(m-b[t])
    for i in range(1,5): out[f'max:cap:reply{i}']=F(m-mb[i])
    out['max:cap:optimal-sum']=F(5*m-d)
    for g,field,ty in (('AB','AB_hist',TY3),('AE','AE_hist',TY3),('second','second_hist',TY4)):
        for i in range(1,len(ty[0])):
            out[f'max:cap:{g}:menu{i}']=F(5*m-sum(n*t[i] for n,t in zip(atom[field],ty)))
    for i,(ell,h) in enumerate(atom['menus_lh']):out[f'max:cap:oldmenu{i}']=F(5*m-ell)
    if 'root_hist' in atom:
        for i in range(1,5):out[f'max:cap:rootmenu{i}']=F(5*m-sum(n*t[i] for n,t in zip(atom['root_hist'],TY5)))
    # Exact-max root BNS, coefficient (k-1)(m-1)=16.
    for t in LABELS:out[f'max:BNS:{t}']=80*actual[0]-15*m-(5-4*m)*b[t]
    out['max:BNS:optimal-sum']=400*actual[0]-75*m-(5-4*m)*d
    # Every old genuinely optimizing node can query every new legal theme.
    for pn,path,start in zip(('actual','second','third'),PATHS,START):
        load=sum(b[x] for x in path)
        for i in range(start,5):
            u=q(b[path[i]],load); p=sum(b[x] for x in path[:i]); k=5-i
            for j in range(5):out[f'max:oldK:{pn}:{i}:{j}']=u-q(mb[j],p+k)
    # The four successors of the forced M root are genuine SPE actors.
    for i in range(1,5):
        p=sum(mb[:i]);k=5-i;u=q(mb[i],total)
        for t in LABELS:out[f'max:tailK:{i}:{t}']=u-q(b[t],p+k)
        for j in range(5):out[f'max:tailownK:{i}:{j}']=u-q(mb[j],p+k)
        out[f'max:tailopt:{i}']=5*u-q(d,p+k)
        for g,field,ty in (('AB','AB_hist',TY3),('AE','AE_hist',TY3),('second','second_hist',TY4)):
            for j in range(1,len(ty[0])):
                out[f'max:tailmenu:{i}:{g}:{j}']=5*u-q(sum(n*t[j] for n,t in zip(atom[field],ty)),p+k)
        if include_ap and i<4:
            aa=8*(k-1)+k*k
            for c in LABELS:
                for e in LABELS:
                    cv,dv=b[c],b[e]
                    out[f'max:tailAP:{i}:{c}:{e}']=aa*u-q((aa-2)*cv+2*cv*dv,p+k)-q(2*dv*(1-cv),p+1)
    p=sum(mb[:3]);h=q(mb[3]+mb[4],total)+q(mb[3],(p+1)*(p+2))
    out['max:tax:opt-union']=F(5,2)*h+q(p,p+1)-o
    out['max:tax:opt-pairs']=10*h-q(d*(5-d),p+1)-q(d*(d-1),p+2)
    for c,e in combinations_with_replacement(LABELS,2):
        cv,dv=b[c],b[e]
        out[f'max:tax:{c}:{e}']=h-q(cv+dv-2*cv*dv,p+1)-q(2*cv*dv,p+2)
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,default=DEFAULT);ap.add_argument('--no-ap',action='store_true');args=ap.parse_args()
    args.source=args.source.resolve();src=json.loads(args.source.read_text()); exact='primal_float' not in src
    masses=[F(a['exact_mass']) for a in src['atoms']] if exact else [F(str(v)) for v in src['primal_float']]
    support=[(a,m) for a,m in zip(src['atoms'],masses) if m>F(1,10**10)]
    names=list(rows(support[0][0],STATES[0],not args.no_ap));n=len(support)*32
    ri=[];ci=[];data=[];eqri=[];eqci=[]
    for ai,(a,mass) in enumerate(support):
        for si,s in enumerate(STATES):
            j=32*ai+si;rr=rows(a,s,not args.no_ap)
            for r,name in enumerate(names):
                v=rr[name]
                if v:ri.append(r);ci.append(j);data.append(float(v))
            eqri.append(ai);eqci.append(j)
    mat=csc_matrix((data,(ri,ci)),shape=(len(names),n));eq=csc_matrix((np.ones(n),(eqri,eqci)),shape=(len(support),n))
    rhs=np.array([float(m) for a,m in support])
    out=linprog(np.zeros(n),A_ub=-mat,b_ub=np.zeros(len(names)),A_eq=eq,b_eq=rhs,bounds=(0,None),method='highs')
    report={'scope':'Conditional maximum-theme true-branch lifting diagnostic; not a universal bound, game, or SPE counterexample','source':str(args.source.relative_to(ROOT)),'source_sha256':hashlib.sha256(args.source.read_bytes()).hexdigest(),'source_support':len(support),'new_states_per_atom':32,'new_rows':len(names),'source_exact':exact,'status':out.status,'message':out.message,'feasible_float':bool(out.success),'row_names':names}
    if out.success:
        report.update({'minimum_new_slack_float':float(min(mat@out.x)),'maximum_mass_error_float':float(max(abs(eq@out.x-rhs))),'lift':[{'source_atom':ai,'max_bits':''.join(map(str,STATES[si])),'mass_float':float(out.x[32*ai+si])} for ai in range(len(support)) for si in range(32) if out.x[32*ai+si]>1e-9]})
    else:
        aug=hstack([-mat,-np.ones((len(names),1))],format='csc');eqa=hstack([eq,np.zeros((len(support),1))],format='csc')
        aux=linprog(np.r_[np.zeros(n),1.],A_ub=aug,b_ub=np.zeros(len(names)),A_eq=eqa,b_eq=rhs,bounds=(0,None),method='highs')
        report['minimum_uniform_violation_float']=float(aux.fun) if aux.success else None
        if aux.success:report['diagnostic_dual_float']={name:float(-v) for name,v in zip(names,aux.ineqlin.marginals) if -v>1e-9}
    target=HERE/('maximum_lift_'+args.source.stem+('_noap' if args.no_ap else '')+'.json');target.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('row_names','lift','diagnostic_dual_float')},indent=2))
if __name__=='__main__':main()
