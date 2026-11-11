"""Standard-library independent 66-row lower-bound replay.

First replay the original 58 rows and MAX:Z using the independent 59 checker.
Then evaluate the seven hidden-successor queries by explicit five indices.
No cone module, optimizer, or source feature/maximization oracle is imported.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROLES = [('AB', 4), ('AB', 5), ('AE', 4), ('AE', 5),
         ('Sbranch', 3), ('Sbranch', 4), ('Sbranch', 5)]


def q(n, d):
    return F(n, d) if n else F(0)


def main():
    cert_path = HERE/'free66_lower_certificate.json'
    cert = json.loads(cert_path.read_text())
    base_path = HERE/'capacity59/archived_lower_certificate.json'
    base = json.loads(base_path.read_text())
    assert cert['cone'] == 'shifted-53-plus-twelve-Z-safe-queries-and-MAX-Z'
    assert hashlib.sha256(base_path.read_bytes()).hexdigest() == cert['base59_certificate_sha256']
    for field in ('atoms', 'capacity_mass', 'lower_bound'):
        assert cert[field] == base[field], field
    subprocess.run([sys.executable, str(HERE/'capacity59/verify_archived_lower.py')], check=True)
    base_audit_path = HERE/'capacity59/archived_lower_independent_audit.json'
    base_audit = json.loads(base_audit_path.read_text())
    extra = {f'{tag}:{seat}:K:Z': F(0) for tag, seat in ROLES}
    for atom in cert['atoms']:
        mass = F(atom['mass'])
        w = atom['witness']
        b = w['background']
        fixed = dict(zip('ABCDEUVWXY', map(int, w['bits'])))
        for tag, seat in ROLES:
            k = 4 if tag == 'Sbranch' else 3
            position = seat-(6-k)
            assert 1 <= position < k
            prefix = b+fixed['A']+(fixed['B'] if tag == 'AB' else fixed['E'] if tag == 'AE' else 0)
            literal = [t for t, count in zip(product((0, 1), repeat=k), w['histograms'][tag]) for _ in range(count)]
            assert len(literal) == 5
            value = sum(q(t[position], prefix+sum(t))-
                        q(b, prefix+sum(t[:position])+k-position) for t in literal)
            extra[f'{tag}:{seat}:K:Z'] += mass*value
    assert all(v > 0 for v in extra.values())
    all_rows = base_audit['all_59_raw_row_slacks'] | {n: str(v) for n, v in extra.items()}
    assert len(all_rows) == 66 and all(F(v) >= 0 for v in all_rows.values())
    out = {'status': 'EXACT-LITERAL-66-ROW-LOWER-BOUND-PASSED',
           'certificate_sha256': hashlib.sha256(cert_path.read_bytes()).hexdigest(),
           'base59_audit_sha256': hashlib.sha256(base_audit_path.read_bytes()).hexdigest(),
           'cone_rows': 66, 'atoms': len(cert['atoms']), 'lower_bound': cert['lower_bound'],
           'lower_bound_float': float(F(cert['lower_bound'])), 'exclusive_mass': base_audit['exclusive_mass'],
           'capacity_mass': cert['capacity_mass'], 'hidden_Z_rows': {n: str(v) for n, v in extra.items()},
           'all_66_raw_row_slacks': all_rows,
           'forced_comparison_player_IC_used': False, 'actual_income_substitution_used': False,
           'not_an_SPE_counterexample': True, 'not_claimed_optimal': True}
    (HERE/'free66_lower_independent_audit.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k: v for k, v in out.items() if k not in ('all_66_raw_row_slacks', 'hidden_Z_rows')}, indent=2))


if __name__ == '__main__':
    main()
