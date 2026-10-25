"""Selected weighted maximum H and its actual two original successors.

At the original maximum-root history (M,z2), force H and follow the same
complete original strategy to (H,Q,R). H is not called an optimizer;
Q and R are genuine optimizers. The complete new membership block is 8
states. This is a projection/separation interface, not a welfare proof.
"""
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from pathlib import Path
import json,sys,hashlib
import numpy as np
from scipy.optimize import linprog
from scipy.linalg import qr
import max_indexed_coupling as cm
import weighted_maximum_query as wm
from exact_cross_primal import evaluator
from frozen_pair_reoptimization import fraction_solve

STATES=list(product((0,1),repeat=3))
FIXED=list(cm.mp.LABELS)+[f'z{j}' for j in range(5)]+[f'f{j}' for j in range(3)]+['opt']


def rows(a,fb):
    mb=tuple(map(int,a['max_bits']));p=sum(mb[:2]);h,q,r=fb;s=p+sum(fb)
    b=dict(zip(cm.mp.LABELS,map(int,a['bits'])));d=sum(a['AB_hist'][4:]);current=cm.lm.q(mb[2],sum(mb))
    K=cm.lm.q(h,p+3);v=cm.lm.q(h,s);vq=cm.lm.q(q,s);vr=cm.lm.q(r,s)
    out={'trueH:source-IC':current-v}
    def query(t):
        if t=='opt':return d,5
        if t.startswith('z'):return mb[int(t[1:])],1
        if t.startswith('f'):return fb[int(t[1:])],1
        return b[t],1
    Htax=vq+vr+cm.lm.q(q,(p+h+1)*(p+h+2))
    for t in FIXED:
        x,n=query(t)
        out[f'trueH:weighted-cap:{t}']=n*K-cm.lm.q(x,p+3)
        out[f'trueH:Q:K:{t}']=n*vq-cm.lm.q(x,p+h+2)
        out[f'trueH:R:K:{t}']=n*vr-cm.lm.q(x,p+h+q+1)
    for j,x in enumerate(fb):
        out[f'trueH:global-size:{j}']=F(mb[0]-x)
        for pn,i in wm.NODES:
            path=cm.mp.PATHS[pn];oldp=sum(b[t] for t in path[:i]);oldu=cm.lm.q(b[path[i]],sum(b[t] for t in path))
            out[f'trueH:oldK:{pn}:{i}:{j}']=oldu-cm.lm.q(x,oldp+5-i)
        for i in range(1,5):
            out[f'trueH:maxK:{i}:{j}']=cm.lm.q(mb[i],sum(mb))-cm.lm.q(x,sum(mb[:i])+5-i)
    # A single suffix Htax pays every legal comparison pair in this history.
    for c,t in combinations_with_replacement(FIXED,2):
        x,nx=query(c);y,ny=query(t)
        out[f'trueH:tax:{c}:{t}']=nx*ny*Htax-cm.lm.q(ny*x+nx*y-2*x*y,p+h+1)-cm.lm.q(2*x*y,p+h+2)
    # Shared old indexed menus are queried from the actual new Q and R nodes.
    for tag,menus in cm.mp.MENUS.items():
        cc=cm.counts(a,tag)
        def menuquery(t):return (cc[t],5) if t in cc else query(t)
        for c in menus:
            x=cc[c]
            out[f'{tag}:trueH:weighted-cap:{c}']=5*K-cm.lm.q(x,p+3)
            out[f'{tag}:trueH:Q:K:{c}']=5*vq-cm.lm.q(x,p+h+2)
            out[f'{tag}:trueH:R:K:{c}']=5*vr-cm.lm.q(x,p+h+q+1)
            for t in FIXED+list(menus):
                y,ny=menuquery(t)
                out[f'{tag}:trueH:Q:AP:{c}:{t}']=cm.mp.ap_value(vq,p+h,2,x,y,5,ny)
                out[f'{tag}:trueH:Q:AP:{t}:{c}']=cm.mp.ap_value(vq,p+h,2,y,x,ny,5)
                out[f'{tag}:trueH:tax:{c}:{t}']=5*ny*Htax-cm.lm.q(ny*x+5*y-2*x*y,p+h+1)-cm.lm.q(2*x*y,p+h+2)
    return out


def exact_source(source):
    """Restore a floating selected-H source on exact active equations."""
    src=json.loads(source.read_text());names=src['row_names']
    if 'primal_float' not in src:
        return src['atoms'],names
    chosen=[(a,v) for a,v in zip(src['atoms'],src['primal_float']) if v>1e-8]
    atoms=[a for a,v in chosen];approx=np.array([v for a,v in chosen]);U=evaluator();U.__class__=wm.Universe;U.specs=cm.mp.menu_specs()
    cols=[];ww=[]
    for a in atoms:
        rr=U.atom_rows(a);assert set(rr)==set(names)
        cols.append([rr[n] for n in names]);ww.append(int(any(map(int,a['bits'][:5]))))
    mat=np.array(cols,dtype=float).T;active=np.where(abs(mat@approx)<1e-7)[0]
    eq=[ww]+[[cols[j][r] for j in range(len(atoms))] for r in active]
    _,r,piv=qr(np.array(eq,dtype=float).T,pivoting=True,mode='economic')
    rank=np.count_nonzero(abs(np.diag(r))>1e-8);assert rank==len(atoms)
    picks=list(piv[:len(atoms)]);m=fraction_solve([eq[j] for j in picks],[int(j==0) for j in picks]);assert min(m)>0
    sl=[sum((m[j]*cols[j][r] for j in range(len(atoms))),F(0)) for r in range(len(names))];assert min(sl)>=0
    report={'scope':'Exact source reconstruction for the subsequent true-branch projection only. No game or new numerical welfare bound.',
            'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_rows':len(names),'positive_atoms':len(atoms),
            'minimum_source_slack':str(min(sl)),'atoms':[dict(a,exact_mass=str(v)) for a,v in zip(atoms,m)]}
    (cm.HERE/'exact_weighted_source.json').write_text(json.dumps(report,indent=2)+'\n')
    return report['atoms'],names


def lift(source):
    source=source.resolve();atoms,_=exact_source(source)
    # H may be reselected; merge any previously retained H-bit split first.
    merged={}
    for a in atoms:
        key=cm.mp.atom_key(a)+(a['max_bits'],)
        if key not in merged:merged[key]=[a,F(0)]
        merged[key][1]+=F(a['exact_mass'])
    support=list(merged.values());allrows=[[rows(a,fb) for fb in STATES] for a,m in support]
    names=list(allrows[0][0]);width=8*len(support)
    mat=np.array([[float(allrows[j][si][n]) for j in range(len(support)) for si in range(8)] for n in names])
    eq=np.zeros((len(support),width))
    for j in range(len(support)):eq[j,8*j:8*j+8]=1
    rhs=np.array([float(m) for a,m in support])
    lp=linprog(np.zeros(width),A_ub=-mat,b_ub=np.zeros(len(names)),A_eq=eq,b_eq=rhs,bounds=(0,None),method='highs')
    report={'scope':'Exact-source lifting to the actual weighted-maximum H,Q,R continuation; a conditional projection diagnostic, not HALF(5).',
            'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_atoms':len(support),'new_states':8,'new_rows':len(names),
            'floating_lift_feasible':bool(lp.success),'message':lp.message}
    if not lp.success:
        aux=linprog(np.r_[np.zeros(width),1.],A_ub=np.column_stack([-mat,-np.ones(len(names))]),b_ub=np.zeros(len(names)),
                    A_eq=np.column_stack([eq,np.zeros(len(support))]),b_eq=rhs,bounds=(0,None),method='highs')
        assert aux.success,aux.message
        multipliers={n:F(float(-v)).limit_denominator(10**7) for n,v in zip(names,aux.ineqlin.marginals) if -v>1e-9}
        assert min(multipliers.values())>0
        projected=[];total=F(0)
        for j,(a,m) in enumerate(support):
            vals=[sum((w*rr[n] for n,w in multipliers.items()),F(0)) for rr in allrows[j]]
            value=max(vals);total+=m*value
            projected.append({'atom':a,'exact_mass':str(m),'coefficient':str(value),'maximizing_state':STATES[vals.index(value)]})
        assert total<0,(total,float(total))
        report.update({'exact_projection_slack':str(total),'negative_slack_float':float(total),
                       'exact_nonnegative_row_multipliers':{n:str(v) for n,v in multipliers.items()},
                       'projection_definition':'g(a)=max_(H,Q,R bits in {0,1}^3) sum_r lambda_r s_r(a,H,Q,R). For every original SPE, sum_clients g>=0.',
                       'projected_atoms':projected})
    report['code_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (cm.HERE/'exact_trueH_projection.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('projected_atoms','exact_nonnegative_row_multipliers')},indent=2))
    if not lp.success:print(json.dumps(report['exact_nonnegative_row_multipliers'],indent=2))
    return report


if __name__=='__main__':lift(Path(sys.argv[1]) if len(sys.argv)>1 else cm.HERE/'weighted_discovery.json')
