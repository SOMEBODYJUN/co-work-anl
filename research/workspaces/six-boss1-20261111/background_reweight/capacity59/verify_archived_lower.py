"""Independent 59-row audit: replay all 58 literal rows, then exact MAX:Z.

No optimizer, cone module or full-domain oracle is imported. The 65 atoms are
identical to the self-contained 58-row certificate, which is replayed by the
standard-library literal-index checker before adding the new capacity row.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent


def main():
    cert_path = HERE/'archived_lower_certificate.json'
    cert = json.loads(cert_path.read_text())
    base_path = PARENT/'free58_lower_certificate.json'
    base = json.loads(base_path.read_text())
    assert cert['cone'] == 'shifted-53-plus-five-actual-Z-safe-queries-and-MAX-Z'
    assert cert['base_certificate_sha256'] == hashlib.sha256(base_path.read_bytes()).hexdigest()
    for field in ('atoms', 'capacity_mass', 'lower_bound'):
        assert cert[field] == base[field], field
    base_report = HERE/'archived_lower_base58_replay.json'
    subprocess.run([sys.executable, str(PARENT/'lower_replay_independent.py'), str(base_path), '--output', str(base_report)], check=True)
    report = json.loads(base_report.read_text())
    background = sum(F(a['mass'])*a['witness']['background'] for a in cert['atoms'])
    max_z = F(cert['capacity_mass'])-background
    assert max_z > 0
    raw = report['raw_row_slacks']
    assert F(raw['MAXROOT-NEW']) == 0
    replacement = F(raw['MAXROOT-NEW']) + 1983898*max_z
    assert replacement > 0
    out = {'status': 'EXACT-LITERAL-59-ROW-LOWER-BOUND-PASSED',
           'certificate_sha256': hashlib.sha256(cert_path.read_bytes()).hexdigest(),
           'base58_audit_sha256': hashlib.sha256(base_report.read_bytes()).hexdigest(),
           'cone_rows': 59, 'atoms': len(cert['atoms']), 'lower_bound': cert['lower_bound'],
           'lower_bound_float': float(F(cert['lower_bound'])), 'exclusive_mass': report['exclusive_mass'],
           'background_membership_mass': str(background), 'capacity_mass': cert['capacity_mass'],
           'MAX_Z_slack': str(max_z), 'fee_cancelled_MAXROOT_slack': str(replacement),
           'fee_cancelled_MAXROOT_contract': '46313177*u_A-5428464*K-1000000*R_Z>=0',
           'all_59_raw_row_slacks': raw | {'MAX:Z': str(max_z)},
           'not_an_SPE_counterexample': True, 'not_claimed_optimal': True}
    (HERE/'archived_lower_independent_audit.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k: v for k, v in out.items() if k != 'all_59_raw_row_slacks'}, indent=2))


if __name__ == '__main__':
    main()
