"""Exact n5 payment test of the new binary four-tail theorem and its own rho.

No substitution into the old RHOMIN is made. The new residual is minimized
over its own eight genuine-deviation membership states. No row is added
unless it strictly separates the current exact five-player target.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
from math import lcm
import json,hashlib
import trueH_fixed_closure_pricing as fc
cm=fc.cm;HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'certificate/exact_current_source_actual13_v1.json'
CERT=HERE.parent/'root/binary_four_tail_uncorrected_certificate.json'
LABELS=list(cm.mp.LABELS)+[f'z{i}' for i in range(5)]
def q(n,d):return F(n,d) if n else F(0)
def run():
    src=json.loads(SOURCE.read_text());atoms=src['atoms'];masses=[F(a['exact_mass']) for a in atoms];cert=json.loads(CERT.read_text());beta=F(cert['beta'])
    rho={(p,t):min(F(r['rho']) for r in cert['residues'] if r['p']==p and tuple(r['bits'][:4])==t) for p in (0,1) for t in product((0,1),repeat=4)}
    denominator=lcm(*(m.denominator for m in masses));mi=[int(m*denominator) for m in masses]
    allbits=[tuple(map(int,a['bits']))+tuple(map(int,a['max_bits'])) for a in atoms]
    countmenus={f'{tag}:{menu}':[cm.counts(a,tag)[menu] for a in atoms] for tag,menus in cm.mp.MENUS.items() for menu in menus}
    cases=[];negative=[]
    for node in ('actual','max'):
        pathbits=[tuple(map(int,a['bits'][:5] if node=='actual' else a['max_bits'])) for a in atoms];ps=[b[0] for b in pathbits]
        profits=[q(sum(b[1:]),sum(b)) for b in pathbits];res=[rho[b[0],tuple(b[1:])] for b in pathbits]
        base=sum((m*(beta*v-r) for m,v,r in zip(masses,profits,res)),F(0));plain=sum((m*beta*v for m,v in zip(masses,profits)),F(0))
        R=[[int(60*q(e,p+e)) for e in range(5)] for p in (0,1)]
        best=None;tested=0
        def check(desc,copies,total):
            nonlocal best,tested
            target=F(total,60*denominator);slack=copies*base-target;tested+=1
            rec={'query':desc,'copies':copies,'exact_slack_with_NEW_RHOMIN':str(slack),'exact_uncorrected_slack_without_rho':str(copies*plain-target)}
            if best is None or slack<F(best['exact_slack_with_NEW_RHOMIN']):best=rec
            if slack<0:negative.append(dict(source_node=node,**rec))
        for qs in combinations_with_replacement(range(15),4):
            total=sum(m*R[p][sum(b[i] for i in qs)] for m,p,b in zip(mi,ps,allbits));check('fixed:'+','.join(LABELS[i] for i in qs),1,total)
        # Same-family five true menu members, each repeated n times, with
        # remaining seats occupied by arbitrary preserved global labels.
        for menu,cc in countmenus.items():
            for n in range(1,5):
                for qs in combinations_with_replacement(range(15),4-n):
                    total=0
                    for m,p,b,c in zip(mi,ps,allbits,cc):
                        s=sum(b[i] for i in qs);total+=m*((5-c)*R[p][s]+c*R[p][s+n])
                    check(f'menu:{menu}:n{n}:'+','.join(LABELS[i] for i in qs),5,total)
        d=[sum(a['AB_hist'][4:]) for a in atoms]
        total=sum(m*int(60*(q(z*(z-1),p+z-1)+q((5-z)*z,p+z))) for m,p,z in zip(mi,ps,d));check('all_five_optimal_four_subsets',5,total)
        cases.append({'source_node':node,'checked_rows':tested,'minimum_row':best,'new_rho_payment':str(sum(m*r for m,r in zip(masses,res)))})
    out={'status':'exact n5 four-tail payment test complete','scope':__doc__,'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'binary_certificate_sha256':hashlib.sha256(CERT.read_bytes()).hexdigest(),'beta':str(beta),'own_new_RHOMIN':{f'{p}:{"".join(map(str,t))}':str(v) for (p,t),v in rho.items()},'checked_rows':sum(c['checked_rows'] for c in cases),'negative_count':len(negative),'negative_rows':negative,'cases':cases}
    HERE.joinpath('new_binary_four_tail_payment_check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('negative_rows','own_new_RHOMIN')},indent=2))
if __name__=='__main__':run()
