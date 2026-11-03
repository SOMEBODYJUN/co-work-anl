#!/usr/bin/env python3
"""Exact report arithmetic and source identity checks; no optimizer or SPE claims."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
OLD = HERE.parent/'five-prefix-interface-and-root-D-primary/source-root'
REL = Path('research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/n5/low_prefix')
RUN = HERE/'replay-001/tree'/REL


def share(n, d):
    return F(n, d) if n else F(0)


def main():
    manifest = json.loads((HERE/'source-manifest.json').read_text())
    for item in manifest:
        assert hashlib.sha256((REPO/item['preserved']).read_bytes()).hexdigest() == item['sha256']
    source = json.loads((OLD/'evidence/certificates/customer_attraction/five_player_indexed_bound.json').read_text())['primal']
    atoms = source['atoms']
    masses = [F(int(a['mass_numerator']), int(source['denominator'])) for a in atoms]
    original = json.loads((RUN/'audit_root_D_payment.json').read_text())
    gap = sum(m*F(a['max']) for m,a in zip(masses, original['per_atom']))
    assert gap == F(original['exact_projected_gap']) < 0
    checks = {'source_files_sha256_checked': len(manifest),
              'exact_audit_mass_weighted_gap': str(gap), 'root_reports': {}}
    for name in ('root_D_envelope.json', 'root_D_simple.json'):
        report = json.loads((RUN/name).read_text())
        assert all(F(w) >= 0 for w in report['weights'].values())
        assert len(report['maximums']) == len(atoms) == 64
        value = sum(m*F(v) for m,v in zip(masses,report['maximums']))
        assert value == F(report['exact_gap']) < 0
        checks['root_reports'][name] = {'weights_nonnegative': True, 'exact_gap': str(value),
                                       'maximums_arithmetic_checked': 64,
                                       'full_181_row_coefficients_independently_reconstructed': False}
    simple = json.loads((RUN/'root_D_simple.json').read_text())
    chain = json.loads((RUN/'root_reply_chain2.json').read_text())
    sw = simple['weights'];cw = chain['weights']
    assert cw == {'0:rootIC':sw['rootIC'], '0:lastE':sw['new:4:fixed:E'],
                  '0:AE4intermediates':sw['AE:4:sumFGH'],
                  '0:second3last':sw['second:3:new:I'],
                  '1:rootIC':sw['actual:0:new:I']}
    weights = list(map(F, (sw['rootIC'],sw['new:4:fixed:E'],sw['actual:0:new:I'],
                          sw['AE:4:sumFGH'],sw['second:3:new:I'])))
    alpha,gamma,beta,delta,epsilon = weights
    chain_cases = 0
    simple_maxima = []
    for atom in atoms:
        a,b,c,d,e,*_ = map(int,atom['bits'])
        root = share(a,a+b+c+d+e)
        kae=cae=kh=ch=F(0)
        for n,(t,r,s) in zip(atom['AE_hist'],product((0,1),repeat=3)):
            kae += n*share(r,a+e+t+r+s)
            cae += n*F(1,a+e+t+2)
        for n,(t,h,i,j) in zip(atom['second_hist'],product((0,1),repeat=4)):
            kh += n*share(h,a+t+h+i+j)
            ch += n*F(1,a+t+3)
        maximum = None
        for n,z in product(range(4),range(2)):
            first = (alpha*(root-share(d,d+n+z))+gamma*(share(z,d+n+z)-share(e,d+n+1))
                     +delta*(3*kae-n*cae)+epsilon*(kh-z*ch))
            simple_value = first+beta*(root-F(z,5))
            second_values = [first+beta*(root-share(z,z+n2+z2))
                             for n2,z2 in product(range(4),range(2))]
            assert max(second_values) == simple_value
            chain_cases += len(second_values)
            maximum = simple_value if maximum is None else max(maximum,simple_value)
        simple_maxima.append(maximum)
    assert list(map(str,simple_maxima)) == simple['maximums']
    assert sum(m*v for m,v in zip(masses,simple_maxima)) == F(chain['exact_gap']) == F(simple['exact_gap'])
    checks['chain_support_equals_simple'] = True
    checks['chain_eight_by_eight_states_checked'] = chain_cases
    checks['simple_maxima_independently_reconstructed'] = len(simple_maxima)
    row3 = json.loads((HERE/'replay-001/tree'/REL.parent/'parent/row3_relaxation.json').read_text())
    assert (row3['types'],row3['rows'],len(row3['support'])) == (19008,78,11)
    frozen77 = json.loads((HERE/'related/frozen_row3_source_support.json').read_text())
    assert row3['support'] != [{'state':x['state'],'weight':x['weight']} for x in frozen77['support']]
    checks['row3_current_78_support_differs_from_frozen_77'] = True
    checks['row3_exact_feasibility_or_global_optimality_certified'] = False
    (HERE/'report-inspection.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(checks,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
