"""Actual/max third histories retain H and both same-strategy successors.

Tests both 747-row marginals first. Only then tests the 64-state joint
common-catalog lift, with reciprocal weighted maxima and true suffix ICs.
Exact source masses and rational projected cuts are mandatory.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
import json,sys,hashlib,time
import numpy as np
from scipy.optimize import linprog
import weighted_true_branch as old
cm=old.cm;STATES=old.STATES;FIXED=old.FIXED


def context(a,source):
    b=dict(zip(cm.mp.LABELS,map(int,a['bits'])));mb=tuple(map(int,a['max_bits']))
    if source=='max':return sum(mb[:2]),cm.lm.q(mb[2],sum(mb))
    assert source=='actual'
    return b['A']+b['B'],cm.lm.q(b['C'],sum(b[t] for t in 'ABCDE'))


def rows(a,fb,source):
    mb=tuple(map(int,a['max_bits']));p,current=context(a,source);h,q,r=fb;s=p+sum(fb)
    b=dict(zip(cm.mp.LABELS,map(int,a['bits'])));d=sum(a['AB_hist'][4:])
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
        for pn,i in old.wm.NODES:
            path=cm.mp.PATHS[pn];oldp=sum(b[t] for t in path[:i]);oldu=cm.lm.q(b[path[i]],sum(b[t] for t in path))
            out[f'trueH:oldK:{pn}:{i}:{j}']=oldu-cm.lm.q(x,oldp+5-i)
        for i in range(1,5):
            out[f'trueH:maxK:{i}:{j}']=cm.lm.q(mb[i],sum(mb))-cm.lm.q(x,sum(mb[:i])+5-i)
    for c,t in combinations_with_replacement(FIXED,2):
        x,nx=query(c);y,ny=query(t)
        out[f'trueH:tax:{c}:{t}']=nx*ny*Htax-cm.lm.q(ny*x+nx*y-2*x*y,p+h+1)-cm.lm.q(2*x*y,p+h+2)
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
    assert len(out)==747
    if source=='max':assert out==old.rows(a,fb)
    return out


def projected_cut(exact_columns,names,atom_count,states_per_atom,mass,mat,eq,rhs):
    width=states_per_atom*atom_count
    aux=linprog(np.r_[np.zeros(width),1.],A_ub=np.column_stack([-mat,-np.ones(len(names))]),b_ub=np.zeros(len(names)),
                A_eq=np.column_stack([eq,np.zeros(atom_count)]),b_eq=rhs,bounds=(0,None),method='highs')
    assert aux.success
    lam={i:F(float(-v)).limit_denominator(10**8) for i,v in enumerate(aux.ineqlin.marginals) if -v>1e-9}
    assert min(lam.values())>0
    values=[];gap=F(0)
    for j,m in enumerate(mass):
        value=max(sum((w*exact_columns[states_per_atom*j+s][i] for i,w in lam.items()),F(0)) for s in range(states_per_atom))
        values.append(str(value));gap+=m*value
    assert gap<0
    return {'exact_projection_slack':str(gap),'negative_slack_float':float(gap),
            'exact_nonnegative_row_multipliers':{names[i]:str(w) for i,w in lam.items()},'projected_coefficients':values}


def cross_rows(a,fa,fm):
    pa,_=context(a,'actual');pm,_=context(a,'max');ha,qa,ra=fa;hm,qm,rm=fm
    ca=pa+sum(fa);cmx=pm+sum(fm)
    out={}
    # Each chosen maximum must dominate all three legal actions of the other
    # original branch in its own background. No ancestor-profit cap is used.
    for side,p,f,g in (('actual',pa,fa,fm),('max',pm,fm,fa)):
        h,q,r=f;total=p+sum(f);vq=cm.lm.q(q,total);vr=cm.lm.q(r,total)
        for i,x in enumerate(g):
            out[f'cross:{side}:weighted-cap:{i}']=cm.lm.q(h-x,p+3)
            out[f'cross:{side}:Q:K:{i}']=vq-cm.lm.q(x,p+h+2)
            out[f'cross:{side}:R:K:{i}']=vr-cm.lm.q(x,p+h+q+1)
    return out


def run(source,joint=True):
    start=time.time();raw=source.read_bytes();src=json.loads(raw);atoms=src['atoms'];mass=[F(a['exact_mass']) for a in atoms];N=len(atoms)
    rhs=np.array(list(map(float,mass)));data={};singles={}
    for node in ('actual','max'):
        data[node]=[[rows(a,s,node) for s in STATES] for a in atoms];names=list(data[node][0][0])
        columns=[[rr[n] for n in names] for peratom in data[node] for rr in peratom]
        mat=np.array(columns,dtype=float).T;eq=np.zeros((N,8*N))
        for j in range(N):eq[j,8*j:8*j+8]=1
        lp=linprog(np.zeros(8*N),A_ub=-mat,b_ub=np.zeros(len(names)),A_eq=eq,b_eq=rhs,bounds=(0,None),method='highs')
        result={'floating_lift_feasible':bool(lp.success),'message':lp.message,'rows':len(names)}
        if not lp.success:result.update(projected_cut(columns,names,N,8,mass,mat,eq,rhs))
        singles[node]=result
        print(json.dumps({'single_history':node,**{k:v for k,v in result.items() if k!='projected_coefficients'}}),flush=True)
    report={'scope':'True same-strategy HQR lift at actual/max third histories, first independent then shared common catalog. No half or SPE counterexample claim.',
            'source_sha256':hashlib.sha256(raw).hexdigest(),'source_atoms':N,'single_history_diagnostics':singles,
            'new_joint_attribution_allowed':all(v['floating_lift_feasible'] for v in singles.values())}
    if joint and report['new_joint_attribution_allowed']:
        cns=list(cross_rows(atoms[0],STATES[0],STATES[0]));allnames=[f'{node}:{n}' for node in ('actual','max') for n in names]+cns
        columns=[]
        for j,a in enumerate(atoms):
            for ia,fa in enumerate(STATES):
                for im,fm in enumerate(STATES):
                    cc=cross_rows(a,fa,fm)
                    columns.append([data[node][j][ia if node=='actual' else im][n] for node in ('actual','max') for n in names]+[cc[n] for n in cns])
        mat=np.array(columns,dtype=float).T;eq=np.zeros((N,64*N))
        for j in range(N):eq[j,64*j:64*j+64]=1
        lp=linprog(np.zeros(64*N),A_ub=-mat,b_ub=np.zeros(len(allnames)),A_eq=eq,b_eq=rhs,bounds=(0,None),method='highs')
        result={'floating_lift_feasible':bool(lp.success),'message':lp.message,'rows':len(allnames),'hidden_states':64}
        if not lp.success:result.update(projected_cut(columns,allnames,N,64,mass,mat,eq,rhs))
        report['joint_history_diagnostic']=result
        print(json.dumps({'joint':{k:v for k,v in result.items() if k!='projected_coefficients'}}),flush=True)
    report['seconds']=time.time()-start;report['code_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    target=cm.HERE/f'two_real_branches_{source.stem}.json';target.write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':run(Path(sys.argv[1]) if len(sys.argv)>1 else cm.HERE/'exact_current_source_own_index_v1.json')
