"""Exact price corollary of Boss5's existing optimal-omission counterexample.

No optimizer; no new underlying instance or claim against half coverage.
The full ordered strategy is replayed by the canonical verifier and its root
terminal checked by the canonical all-outcomes solver.
"""
from pathlib import Path
from fractions import Fraction as F
import json,sys
BASE=Path(__file__).resolve().parent
ROOT=next(p for p in BASE.parents if (p/'customer_attraction/__init__.py').is_file())
sys.path.insert(0,str(ROOT))
from customer_attraction import Instance, CustomerType, StrategyCertificate, verify_certificate, ExactSPESolver


def audit(k):
    if k<3:raise ValueError('existing source family assumes k>=3')
    # A,B,T,Q,R,S are respectively 0,...,5.
    raw=[((0,),4*k-2),((0,4,5),2*k),((1,),5*k-2),((1,4,5),2*k-2),
         ((1,2,4,5),1),((1,3,4,5),1),((2,),3*k-1),((2,4),2*k-1),((2,5),2*k-1),
         ((3,),3*k-1),((3,4),2*k-1),((3,5),2*k-1)]
    game=Instance(('A','B','T','Q','R','S'),tuple(CustomerType(frozenset(s),n) for s,n in raw),2)
    actions={():0,**{(a,):b for a,b in enumerate((1,5,4,5,5,4))}}
    cert=StrategyCertificate(actions,(1,1,0,0,0,0));check=verify_certificate(game,cert);check.assert_valid()
    solver=ExactSPESolver(game)
    if cert.terminal_counts not in solver.outcomes():raise AssertionError('canonical root rejection')
    a=F(6*k-2);b=F(7*k-2);budget=F(2*k-2)
    if game.player_payoffs((0,1))!=(a,b):raise AssertionError('source utility formulas')
    D=[(s,n) for s,n in raw if not set(s)&{0,1}]
    # Primal z_T=z_Q=1 covers every D customer exactly once.
    primal=sum(n for s,n in D)-2*a
    # Dual y=1 on k-1 T-private and k-1 Q-private clients, zero elsewhere.
    # A cardinality k-1 is possible inside each private group of size 3k-1.
    residual=[]
    for theme in range(6):
        covered=sum(n for s,n in D if theme in s)
        deleted=k-1 if theme in (2,3) else 0
        residual.append(F(covered-deleted))
    if any(x>a for x in residual) or primal!=budget:raise AssertionError('exact primal/dual mismatch')
    return {'k':k,'u_A':str(a),'u_B':str(b),'B_D_u_A':str(budget),'excess_tail_profit':str(b-a),
            'violation':str(budget-(b-a)),'ratio':str(budget/(b-a)),
            'dual_residual_theme_values':list(map(str,residual)),
            'W':game.welfare(cert.terminal_counts),'OPT':game.optimal_welfare(),
            'histories':check.checked_histories,'deviations':check.checked_deviations,'canonical_root_checked':True}


if __name__=='__main__':
    out={'scope':'exact price corollary of existing Boss5 family, not a new half counterexample',
         'source':'R-171cd7d518434f36a48cd50df29c9303/global/optimal_omission_exchange_counterexample.md',
         'records':[audit(k) for k in (3,4,7,20)],'passed':True}
    BASE.joinpath('protected_price_boundary.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
