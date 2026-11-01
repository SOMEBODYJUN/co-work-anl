"""Independent raw-menu reconstruction for the actual-fourth B projection.

Reads frozen code-derived certificate and only histogram marginals of the old
point. It does not import either author program or solve for an SPE/LP.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import sys


def audit(cert_path, point_path):
    cert = json.loads(cert_path.read_text())
    point = json.loads(point_path.read_text())
    assert hashlib.sha256(cert_path.read_bytes()).hexdigest() == '4d34cd746ce35dd48827c9014a85106c5defac30fc5f1159ae6085d4fd8fa1df'
    point_sha = hashlib.sha256(point_path.read_bytes()).hexdigest()
    assert point_sha == cert['old_point_sha256'] == '24a2f9fa7e7a47e26e065b41ada98e1788a5b448251fb8c1e881557c1f7c9f11'
    assert cert['weights'] == dict(F=3360,G=96,H2Q=660,H2R=595,H3R=220,LQ=522,LR=522,E=108)
    assert all(v >= 0 for v in cert['weights'].values())
    lookup = {(v['actual_bits'],v['d']):F(v['psi']) for v in cert['table']}
    assert len(lookup) == len(cert['table']) == 448
    raw_count = 0
    qr_ell_count = 0
    reconstructed = []
    for a in product((0,1),repeat=6):
        actual_total = sum(a)
        actual = [F(v,actual_total) if v else F() for v in a]
        p = sum(a[:3]) + a[5]
        den2 = (p+1)*(p+2)
        for d in range(7):
            values, endpoints = [], []
            for q,r,ell in product((0,1),(0,1),range(7)):
                qr_ell_count += 1
                total = p+q+r
                uq = F(q,total) if q else F()
                ur = F(r,total) if r else F()
                same_visible = []
                for overlap in range(max(0,d+ell-6),min(d,ell)+1):
                    raw_count += 1
                    # S,Z,V are the uneliminated genuine-menu coefficient sums.
                    s = 6*uq-F(d,p+1)+F(overlap,den2)
                    z = 6*ur-F(ell,p+q+1)
                    v = F(d*ell-6*overlap,den2)
                    g = s+z/12+v/6
                    cancelled = 6*uq+ur/2-F(d,p+1)-F(ell,12*(p+q+1))+F(d*ell,6*den2)
                    assert g == cancelled
                    source = actual[3]-(F(a[5],total) if a[5] else F())
                    value = 3360*source+96*g
                    value += 660*(actual[1]-F(q,5+a[0]))
                    value += 595*(actual[1]-F(r,5+a[0]))
                    value += 220*(actual[2]-F(r,4+a[0]+a[1]))
                    value += 522*(actual[5]-F(q,1+sum(a[:5])))
                    value += 522*(actual[5]-F(r,1+sum(a[:5])))
                    value += 108*(6*ur-F(d,p+q+1))
                    same_visible.append(value)
                assert len(set(same_visible)) == 1
                values.append(same_visible[0])
                if ell in (0,6):endpoints.append(same_visible[0])
            maximum = max(values)
            key = ''.join(map(str,a)),d
            assert maximum == max(endpoints) == lookup[key]
            reconstructed.append({'actual_bits':key[0],'d':d,'psi':str(maximum)})
    assert raw_count == 21504 and qr_ell_count == 12544
    assert reconstructed == cert['table']
    masses = defaultdict(F)
    hist_rows = []
    for j,c in enumerate(point['columns']):
        if c['kind'] != 'hist':continue
        assert len(c['actual_bits']) == 6 and set(c['actual_bits']) <= {'0','1'}
        assert c['d'] in range(7)
        assert len(c['hist']) == 8 and sum(c['hist']) == 6
        assert sum(c['hist'][4:]) == c['d']
        mass = F(c['weight']);assert mass >= 0
        masses[c['actual_bits'],c['d']] += mass
        hist_rows.append({'column':j,**c})
    assert len(hist_rows) == 16 and sum(masses.values()) == 1
    contributions=[]
    for (bits,d),mass in sorted(masses.items()):
        if not mass:continue
        contributions.append({'actual_bits':bits,'d':d,'mass':str(mass),'psi':str(lookup[bits,d]),'contribution':str(mass*lookup[bits,d])})
    value=sum((F(c['contribution']) for c in contributions),F())
    assert len(contributions)==8 and value==F(cert['old_point_value'])<0
    assert float(value)==cert['old_point_value_decimal']
    return {'status':'PASS_RAW_MENU_RECONSTRUCTION_AND_SPECIFIED_OLD_MARGIN_SEPARATION',
            'scope':'All 448 visible cells, 12544 QR-ell states and 21504 feasible-overlap states; exact old 16-hist marginal only. No full old graph verification or complete SPE.',
            'python_version':sys.version,'raw_overlap_states':raw_count,'QR_ell_states':qr_ell_count,
            'visible_cells':len(lookup),'all_448_coefficients_and_order_equal':True,
            'overlap_cancels_in_G':True,'endpoint_equals_full_in_every_visible_cell':True,
            'hist_rows':hist_rows,'positive_hist_rows':sum(F(c['weight'])>0 for c in hist_rows),
            'positive_visible_margins':len(contributions),'old_point_contributions':contributions,
            'old_point_value':str(value),'old_point_sha256':point_sha,
            'certificate_sha256':hashlib.sha256(cert_path.read_bytes()).hexdigest(),
            'audit_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'not_certified':['old 1033 constraints','1097/3889 extension bytes','feasibility of every maximizing hidden assignment','complete-history strategy','six-player half theorem']}


if __name__=='__main__':
    if sys.flags.optimize:raise RuntimeError('assertions must remain enabled')
    if len(sys.argv)!=4:raise SystemExit('usage: audit.py CERTIFICATE POINT OUTPUT')
    result=audit(Path(sys.argv[1]),Path(sys.argv[2]))
    Path(sys.argv[3]).write_text(json.dumps(result,indent=2)+'\n')
