#!/usr/bin/env python3
"""Replay preserved binary four-tail evidence in an isolated local layout.

Default: standard-library exact verification of the frozen rational certificate.
--rediscover: also rerun both original NumPy/SciPy discovery generators.
Neither mode is a new independent mathematical review.
"""
from fractions import Fraction
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

BASE=Path(__file__).resolve().parent
CERTS=('binary_four_tail_certificate','binary_four_tail_uncorrected_certificate')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rediscover',action='store_true')
    args=parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='binary-replay-',dir=BASE) as tmp:
        tmp=Path(tmp);(tmp/'root').mkdir();(tmp/'direct').mkdir()
        comparisons={}
        for name in CERTS:
            if args.rediscover:
                script=tmp/'root'/(name+'.py')
                shutil.copyfile(BASE/'source'/(name+'.py'),script)
                subprocess.run([sys.executable,str(script)],check=True,capture_output=True,text=True)
            else:
                shutil.copyfile(BASE/'original'/(name+'.json'),tmp/'root'/(name+'.json'))
            actual=tmp/'root'/(name+'.json')
            original=BASE/'original'/(name+'.json')
            assert json.loads(actual.read_text())==json.loads(original.read_text()),name
            shutil.copyfile(actual,BASE/'replay'/(name+'.json'))
            comparisons[name]={'all_fields_and_256_residues_equal':True,
                              'frozen_sha256':hashlib.sha256(original.read_bytes()).hexdigest(),
                              'replay_sha256':hashlib.sha256(actual.read_bytes()).hexdigest()}
        script=tmp/'direct/audit_binary_four_tail_independent.py'
        shutil.copyfile(BASE/'source'/script.name,script)
        subprocess.run([sys.executable,str(script)],check=True,capture_output=True,text=True)
        actual=script.with_suffix('.json')
        original=BASE/'original'/actual.name
        assert json.loads(actual.read_text())==json.loads(original.read_text())
        shutil.copyfile(actual,BASE/'replay'/actual.name)
    corr=json.loads((BASE/'original'/(CERTS[0]+'.json')).read_text())
    unc=json.loads((BASE/'original'/(CERTS[1]+'.json')).read_text())
    beta=Fraction(corr['beta']);weights={k:Fraction(v) for k,v in corr['weights'].items()}
    assert corr['weights']==unc['weights'] and corr['beta']==unc['beta']
    c={(r['p'],tuple(r['bits'])):Fraction(r['rho']) for r in corr['residues']}
    u={(r['p'],tuple(r['bits'])):Fraction(r['rho']) for r in unc['residues']}
    floor=[]
    from itertools import product
    for bits in product((0,1),repeat=4):
        row={'actual_bits':''.join(map(str,bits))}
        for p in (0,1):
            for label,data in [('corrected',c),('uncorrected',u)]:
                row[f'{label}_p{p}']=str(min(data[p,(*bits,*q)] for q in product((0,1),repeat=3)))
        floor.append(row)
    for (p,bits),value in c.items():
        a,b,cc,d,q,r,s=bits;D=(p+1)*(p+2)*(p+3)*(p+4)
        extraP=Fraction(2*p*p,3*D) if a+b==2 else 0
        extraE=Fraction(p*p+p,D) if a+b+cc==3 else 0
        assert u[p,bits]==value+weights['P']*extraP+weights['E']*extraE>=value>=0
    report={'scope':'original-generator-and-original-standard-library-audit-replay' if args.rediscover else 'original-standard-library-audit-replay',
            'new_independent_reviewer_claimed':False,'rediscovery_run':args.rediscover,
            'certificate_comparisons':comparisons,'independent_report_all_fields_equal':True,
            'beta':str(beta),'gap_below_two':str(2-beta),
            'improvement_over_old':str(Fraction(1499,750)-beta),
            'corrected_uncorrected_identity_checked_states':len(c),
            'corrected_zero_states':sum(x==0 for x in c.values()),
            'uncorrected_zero_states':sum(x==0 for x in u.values()),
            'residual_floors':floor,'all_checks_passed':True}
    (BASE/'replay/reconciliation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
