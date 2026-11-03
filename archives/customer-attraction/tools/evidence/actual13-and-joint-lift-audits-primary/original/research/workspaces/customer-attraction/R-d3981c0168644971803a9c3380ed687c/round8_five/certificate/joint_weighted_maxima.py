"""Two genuinely different histories choose maxima in one common catalog.

First test each selected-H marginal alone. Only if both are feasible can a
joint failure be attributed to the two new reciprocal catalog inequalities.
The four hidden states are the two selected-theme membership bits.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json,sys,hashlib
import numpy as np
from scipy.optimize import linprog
import max_indexed_coupling as cm
import weighted_maximum_query as wm
import trueH_table_certificate as cert

STATES=list(product((0,1),repeat=2))


def context(a,node):
    b=dict(zip(cm.mp.LABELS,map(int,a['bits'])));mb=tuple(map(int,a['max_bits']))
    if node=='max':return sum(mb[:2]),cm.lm.q(mb[2],sum(mb))
    path=cm.mp.PATHS[node]
    return sum(b[t] for t in path[:2]),cm.lm.q(b[path[2]],sum(b[t] for t in path))


def rows(a,h,node):
    b=dict(zip(cm.mp.LABELS,map(int,a['bits'])));mb=tuple(map(int,a['max_bits']));d=sum(a['AB_hist'][4:])
    p,u=context(a,node);K=cm.lm.q(h,p+3)
    out={'bare-cap':F(mb[0]-h),'current-floor':u-K}
    def query(t):
        if t=='opt':return d,5
        if t.startswith('z'):return mb[int(t[1:])],1
        return b[t],1
    for t in wm.FIXED:
        q,n=query(t)
        out[f'cap:{t}']=n*K-cm.lm.q(q,p+3)
        out[f'BNS:{t}']=8*n*u-7*n*K-cm.lm.q(h*q,p+3)-cm.lm.q((1-h)*q,p+1)
    for tag,menus in cm.mp.MENUS.items():
        cc=cm.counts(a,tag)
        for menu in menus:
            q=cc[menu]
            out[f'{tag}:cap:{menu}']=5*K-cm.lm.q(q,p+3)
            out[f'{tag}:BNS:{menu}']=40*u-35*K-cm.lm.q(h*q,p+3)-cm.lm.q((1-h)*q,p+1)
    # This is (P) with J chosen as H five times; it bounds the actual K.
    out['trueQR:K-envelope']=17040*u+1085*mb[0]-13395*K-cert.TARGET[p][d]
    for pn,i in wm.NODES:
        path=cm.mp.PATHS[pn];oldp=sum(b[t] for t in path[:i]);profit=cm.lm.q(b[path[i]],sum(b[t] for t in path))
        out[f'oldK:{pn}:{i}']=profit-cm.lm.q(h,oldp+5-i)
    for i in range(1,5):
        out[f'maxK:{i}']=cm.lm.q(mb[i],sum(mb))-cm.lm.q(h,sum(mb[:i])+5-i)
    return out


def test(source):
    raw=source.read_bytes();src=json.loads(raw);atoms=src['atoms'];masses=[F(a['exact_mass']) for a in atoms]
    nodes=('actual','max');data={n:[[rows(a,h,n) for h in (0,1)] for a in atoms] for n in nodes};names=list(data['actual'][0][0]);rhs=np.array(list(map(float,masses)))
    singles={}
    for node in nodes:
        mat=np.array([[float(data[node][j][h][n]) for j in range(len(atoms)) for h in (0,1)] for n in names])
        eq=np.zeros((len(atoms),2*len(atoms)))
        for j in range(len(atoms)):eq[j,2*j:2*j+2]=1
        lp=linprog(np.zeros(2*len(atoms)),A_ub=-mat,b_ub=np.zeros(len(names)),A_eq=eq,b_eq=rhs,bounds=(0,None),method='highs')
        singles[node]={'floating_lift_feasible':bool(lp.success),'message':lp.message}
    allnames=[f'{node}:{n}' for node in nodes for n in names]+['cross:actual-dominates-maxH','cross:max-dominates-actualH']
    columns=[];exact_columns=[]
    for j,a in enumerate(atoms):
        pa,_=context(a,'actual');pm,_=context(a,'max')
        for ha,hm in STATES:
            values=[data[node][j][ha if node=='actual' else hm][n] for node in nodes for n in names]
            values += [cm.lm.q(ha-hm,pa+3),cm.lm.q(hm-ha,pm+3)]
            exact_columns.append(values);columns.append(list(map(float,values)))
    mat=np.array(columns).T;eq=np.zeros((len(atoms),4*len(atoms)))
    for j in range(len(atoms)):eq[j,4*j:4*j+4]=1
    lp=linprog(np.zeros(4*len(atoms)),A_ub=-mat,b_ub=np.zeros(len(allnames)),A_eq=eq,b_eq=rhs,bounds=(0,None),method='highs')
    report={'scope':'Fixed-point compatibility of weighted maxima at actual and maximum-root third histories. No half or original-game claim.',
            'source_sha256':hashlib.sha256(raw).hexdigest(),'source_atoms':len(atoms),'single_history_diagnostics':singles,
            'joint_rows':len(allnames),'hidden_states':4,'floating_joint_lift_feasible':bool(lp.success),'message':lp.message,
            'new_compatibility_attribution_allowed':all(v['floating_lift_feasible'] for v in singles.values())}
    if not lp.success:
        width=4*len(atoms)
        aux=linprog(np.r_[np.zeros(width),1.],A_ub=np.column_stack([-mat,-np.ones(len(allnames))]),b_ub=np.zeros(len(allnames)),
                    A_eq=np.column_stack([eq,np.zeros(len(atoms))]),b_eq=rhs,bounds=(0,None),method='highs');assert aux.success
        lam={i:F(float(-v)).limit_denominator(10**8) for i,v in enumerate(aux.ineqlin.marginals) if -v>1e-9}
        gap=F(0);values=[]
        for j,m in enumerate(masses):
            vv=max(sum((w*exact_columns[4*j+s][i] for i,w in lam.items()),F(0)) for s in range(4))
            gap+=m*vv;values.append(str(vv))
        assert gap<0
        report.update({'exact_projected_slack':str(gap),'negative_slack_float':float(gap),
                       'exact_row_multipliers':{allnames[i]:str(v) for i,v in lam.items()},'projected_coefficients':values})
    report['code_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out=cm.HERE/f'joint_weighted_maxima_{source.stem}.json';out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='projected_coefficients'},indent=2))


if __name__=='__main__':test(Path(sys.argv[1]) if len(sys.argv)>1 else cm.HERE/'exact_current_source_source_last_v1.json')
