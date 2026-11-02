"""Independent report check using direct unit-customer payoff, not author module."""
from pathlib import Path
from fractions import Fraction
from itertools import product
from collections import Counter
import hashlib
import json

ROOT=Path(__file__).resolve().parent
source=ROOT/'audit_background_two_player.json'
raw=source.read_bytes()
data=json.loads(raw)
assert set(data)=={'backgrounds','binary_cases_per_background','checks','minimum_psi','status'}
assert data['backgrounds']==[0,1,2,3,4,7,10,100,10**9]
assert data['binary_cases_per_background']==2**6
assert data['checks']==len(data['backgrounds'])*2**6
assert data['status']=='exact identities and nonnegative residual verified; arbitrary background theorem uses symbolic proof'
counts=Counter()
checks=0
min_psi=None
correction_positive=0
for bg in data['backgrounds']:
    # Direct payoff of one unit customer with binary own/other coverage.
    def share(own,other):
        return Fraction(own,bg+1+other)
    f=Fraction(1,bg+1)
    g=Fraction(1,(bg+1)*(bg+2))
    for c,d,t1,t2,r1,r2 in product((0,1),repeat=6):
        alpha,beta=share(c,d),share(d,c)
        FF=2*alpha-share(t1,r1)-share(t2,r2)
        PP=2*beta-share(t1,c)-share(t2,c)
        ZZ=2*beta-share(r1,c)-share(r2,c)
        VV=share(r1,t1)-share(t2,t1)+share(r2,t2)-share(t1,t2)
        G=3*FF+PP+4*ZZ+4*VV
        R=share(t1,t2)+share(t2,t1)
        t,r=t1+t2,r1+r2
        h,z=t1*r1+t2*r2,t1*t2
        psi=8*c-c*t+h-4*c*r+8*z
        six_case=((0,h,8+r) if c==0 else (8-4*r,7+h-4*r,14-3*r))[t]
        assert psi==six_case
        assert psi>=0
        # Expanded polynomial identity and target slack.
        expanded=6*alpha+10*beta-8*f*t+g*c*t-g*h+4*g*c*r+8*g*z
        assert G==expanded
        assert 6*alpha+10*beta+8*g*c-8*R-G==g*psi
        correction=4*g*c*(d-bg)
        assert 6*alpha+10*beta+8*g*c==10*(alpha+beta)+correction
        Inew=int(bg==0 and c==d==1)
        assert correction<=2*Inew
        correction_positive+=int(correction>0)
        min_psi=psi if min_psi is None else min(min_psi,psi)
        counts[(c,t,psi==0)]+=1
        checks+=1
assert checks==data['checks']
assert min_psi==data['minimum_psi']==0
# A separate arithmetic boundary check: integer loads matter for the correction.
bg=Fraction(1,2)
g=1/((bg+1)*(bg+2))
noninteger_correction=4*g*(1-bg)
assert noninteger_correction==Fraction(8,15)>0
report={
 'source_id':'a688a554b33bce8def2f',
 'source_bytes':len(raw),
 'source_sha256':hashlib.sha256(raw).hexdigest(),
 'json_all_fields_checked':True,
 'direct_payoff_implementation':'own/(background+1+other)',
 'imported_author_program':False,
 'checked_binary_background_cases':checks,
 'minimum_psi':min_psi,
 'positive_correction_cases':correction_positive,
 'zero_psi_cases':sum(n for (c,t,is_zero),n in counts.items() if is_zero),
 'per_background_psi_zero_count':sum(n for (c,t,is_zero),n in counts.items() if is_zero)//len(data['backgrounds']),
 'noninteger_boundary':{'background':'1/2','c':1,'d':1,'correction':str(noninteger_correction),'Inew':0,'meaning':'newborn-overlap upper correction requires integer background'},
 'status':'PASS: exact finite field and direct-payoff checks; theorem remains analytic',
 'scope':'576 local membership types, not 576 games or complete SPE certificates'
}
(ROOT/'independent-json-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
