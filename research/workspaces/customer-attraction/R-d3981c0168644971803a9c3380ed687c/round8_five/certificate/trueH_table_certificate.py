"""A universal 3x6 coefficient certificate using seven original SPE rows.

Independent standard-library reconstruction of the seven raw coefficients.
No imports of the discovery, indexed-row evaluators, or SPE solver.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json, hashlib

HERE=Path(__file__).resolve().parent
WEIGHTS={
    'current_IC':17040,
    'weighted_cap_Q':9000,
    'weighted_cap_R':10080,
    'last_optimal_menu_IC':600,
    'largest_theme_cap_H':1085,
    'two_tail_tax_R_optimal_menu':360,
    'weighted_cap_J_menu':2679,
}
TARGET=[list(map(F,[0,960,1220,1480,1740,2000])),
        [F(0),F(1665,4),F(2745,4),F(3785,4),F(4825,4),F(5865,4)],
        list(map(F,[0,320,524,728,932,1136]))]
STATES=list(product((0,1),repeat=3))


def share(num,den):return F(num,den) if num else F(0)


def hidden_score(p,d,h,q,r):
    """Seven-row weighted coefficient after removing the common terms.

    Common terms: 17040*u_x +1085*1_M(x) -2679*Jcount_x/(p+3).
    p is the original first-two load, and H,Q,R are from one real branch.
    """
    s=p+h+q+r
    Vh=share(h,s);Vq=share(q,s);Vr=share(r,s)
    tax=Vq+Vr+F(q,(p+h+1)*(p+h+2))
    rows={
        'current_IC':-Vh,
        'weighted_cap_Q':F(h-q,p+3),
        'weighted_cap_R':F(h-r,p+3),
        'last_optimal_menu_IC':5*Vr-F(d,p+h+q+1),
        'largest_theme_cap_H':-F(h),
        'two_tail_tax_R_optimal_menu':5*tax-F(5*r+d-2*r*d,p+h+1)-F(2*r*d,p+h+2),
        'weighted_cap_J_menu':F(5*h,p+3),
    }
    return sum((WEIGHTS[n]*v for n,v in rows.items()),F(0))


def coefficient(u_x,membership_M,p,d,jcount):
    return 17040*u_x+1085*membership_M-F(2679*jcount,p+3)-TARGET[p][d]


def atom_coefficient(a,tag='Sbranch',menu='mW'):
    mb=list(map(int,a['max_bits']));p=sum(mb[:2]);u=share(mb[2],sum(mb));d=sum(a['AB_hist'][4:])
    field={'AB':'AB_hist','AE':'AE_hist','Sbranch':'second_hist'}[tag]
    labels=('mU','mV','mW') if tag=='Sbranch' else ('mX','mY')
    pos=labels.index(menu)+1;types=list(product((0,1),repeat=len(labels)+1))
    j=sum(n*t[pos] for n,t in zip(a[field],types))
    return coefficient(u,mb[0],p,d,j)


def certify():
    residuals={};maximizers={}
    for p in range(3):
        for d in range(6):
            scores=[hidden_score(p,d,*state) for state in STATES]
            assert max(scores)==-TARGET[p][d]
            maximizers[f'{p},{d}']=[state for state,v in zip(STATES,scores) if v==max(scores)]
            for state,v in zip(STATES,scores):
                gap=-TARGET[p][d]-v;assert gap>=0
                residuals[f'{p},{d}:{"".join(map(str,state))}']=str(gap)
    # Independent check against the frozen selected-H true-branch separator.
    source=HERE/'exact_trueH_projection.json';src=json.loads(source.read_text());slack=F(0)
    for entry in src['projected_atoms']:
        value=atom_coefficient(entry['atom']);assert value==40844*F(entry['coefficient'])
        slack+=F(entry['exact_mass'])*value
    assert slack==40844*F(src['exact_projection_slack'])<0
    report={'scope':'Universal necessary relation for the original five-provider model. All 144 hidden coefficient states checked exactly. Not a factor-two welfare proof.',
            'relation':'sum_x [17040*u3_x +1085*1_M(x) -2679*Jcount_x/(p_x+3) -F(p_x,d_x)] >=0',
            'notation':{'M':'one largest unweighted legal theme; the membership is not the provider count',
                        'p':'load of the first two themes on the real maximum-root path',
                        'u3':'third provider payoff on that real path',
                        'HQR':'at that exact third-provider history, force a maximizer H of sum_H 1/(p+3), then follow the same original strategy to Q,R',
                        'd':'membership count in five arbitrary legal comparison themes',
                        'Jcount':'membership count in five arbitrary legal menu themes'},
            'nonnegative_integer_row_weights':WEIGHTS,'F_table':[[str(v) for v in row] for row in TARGET],
            'complete_hidden_domain':{'p':[0,1,2],'d':list(range(6)),'HQR_membership_states':STATES},
            'hidden_state_residuals':residuals,'maximizing_states':maximizers,
            'exact_separation_slack_on_frozen_source':str(slack),
            'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'trueH_table_certificate.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':'passed','complete_hidden_states':len(residuals),'minimum_exact_residual':str(min(map(F,residuals.values()))),
                      'exact_separation_slack':str(slack)},indent=2))
    return report


if __name__=='__main__':certify()
