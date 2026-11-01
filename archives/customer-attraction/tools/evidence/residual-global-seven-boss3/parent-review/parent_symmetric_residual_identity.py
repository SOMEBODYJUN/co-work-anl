"""Independent exact check of a symmetric two-player residual payment identity.

No solver or original probe is imported.  The nine reported multipliers are
checked against their saved coefficient vector, then averaged with the role
swap T<->S,Q<->R.  A closed-form, manifestly nonnegative remainder is checked.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import platform
import time


def coefficients(z):
    a,b,t,s,q,r=z
    def U(x,y): return F(x,1+y)
    u,v=U(a,b),U(b,a)
    labels='ABTSQR'
    rows={f'actual_B>={n}':v-U(x,a) for n,x in zip(labels,z)}
    rows.update({f'reply_Q>={n}':U(q,t)-U(x,t) for n,x in zip(labels,z)})
    rows.update({f'reply_R>={n}':U(r,s)-U(x,s) for n,x in zip(labels,z)})
    rows.update({'root_T':u-U(t,q),'root_S':u-U(s,r),
                 'root_Q_floor':2*u-q,'root_R_floor':2*u-r})
    return rows


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--certificate',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    tick=time.monotonic();started=time.time()
    raw=args.certificate.read_bytes();cert=json.loads(raw)
    original={'actual_B>=T':F(3,10),'actual_B>=S':F(3,10),
              'actual_B>=Q':F(6,25),'actual_B>=R':F(4,25),
              'reply_Q>=S':F(1,5),'reply_Q>=R':F(4,25),
              'reply_R>=Q':F(6,25),'root_T':F(3,5),'root_S':F(2,5)}
    symmetric={'actual_B>=T':F(3,10),'actual_B>=S':F(3,10),
               'actual_B>=Q':F(1,5),'actual_B>=R':F(1,5),
               'reply_Q>=S':F(1,10),'reply_R>=T':F(1,10),
               'reply_Q>=R':F(1,5),'reply_R>=Q':F(1,5),
               'root_T':F(1,2),'root_S':F(1,2)}
    assert original=={x['row']:F(x['multiplier']) for x in cert['dual_support']}
    rows=[]
    for index,z in enumerate(product((0,1),repeat=6)):
        a,b,t,s,q,r=z
        G=coefficients(z);W=int(a or b);O=int(not(a or b) and (t or s))
        H=F(W)-F(9,10)*O-sum(c*G[n] for n,c in original.items())
        assert H==F(cert['dual_coordinate_residuals'][index]) and H>=0
        swapped=(a,b,s,t,r,q);Gswap=coefficients(swapped)
        Hswap=F(W)-F(9,10)*O-sum(c*Gswap[n] for n,c in original.items())
        sym=F(W)-F(9,10)*O-sum(c*G[n] for n,c in symmetric.items())
        assert sym==(H+Hswap)/2
        n=t+s;e=q+r
        if a==0:
            closed=[F(e,10),F(0),F(4,5)-F(e,10)][n]+F(9,10)*b*int(n>0)
        else:
            closed=[F(0),F(3,4)-F(e,10),F(7,5)-F(e,5)][n]
        assert closed==sym and closed>=0
        rows.append({'bits':z,'original_remainder':str(H),'symmetric_remainder':str(sym),'closed_form':str(closed)})
    result={'scope':'per-customer Boolean identity, not a new LP or new full SPE search',
            'original_certificate_sha256':hashlib.sha256(raw).hexdigest(),
            'original_nine_multipliers':{n:str(c) for n,c in original.items()},
            'symmetric_ten_multipliers':{n:str(c) for n,c in symmetric.items()},
            'all_64_original_coefficients_match':True,'all_64_symmetrization_identities':True,
            'all_64_closed_form_identities_nonnegative':True,'rows':rows}
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    event={'started_unix':started,'elapsed_seconds':time.monotonic()-tick,
           'python':platform.python_version(),'assertions_enabled':__debug__,
           'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           'output_sha256':hashlib.sha256(args.output.read_bytes()).hexdigest(),
           'new_invocations':1,'Boolean_memberships':64,'original_probe_imports':0,
           'LP_MIP_BI_calls':0,'result':'all exact identities passed'}
    args.output.with_suffix('.event.json').write_text(json.dumps(event,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(event,ensure_ascii=False))


if __name__=='__main__': main()
