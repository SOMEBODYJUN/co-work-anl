"""Main's read-only exact primal/dual replay; no optimizer or source mutation."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
BASE = HERE / 'universal_union_wallet_lp'
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ip = BASE / 'exact_input.json'
    cp = BASE / 'exact_certificate.json'
    assert sha(ip) == 'f87a60372dee7449332b17721be6aa70012fb3aca251825cb2e9dd755ff01e41'
    assert sha(cp) == 'ccc085060427e2999a8e4f00ac3414d7e20a1c6e66aeba8d3e658ae34cb16c85'
    inp, cert = json.loads(ip.read_text()), json.loads(cp.read_text())
    n = len(inp['nonnegative_columns'])
    assert inp['nonnegative_columns'] == list(range(n))
    p = {int(k): F(v) for k, v in cert['primal'].items()}
    assert all(v >= 0 for v in p.values())
    def dot(a):
        return sum((F(v)*p.get(int(k), F(0)) for k, v in a.items()), F(0))
    eq = inp['equality']
    assert dot(eq['a']) == F(eq['rhs']) == 1
    rows = {r['name']: r for r in inp['raw_rows']}
    assert len(rows) == 217
    slacks = {name: dot(r['a'])-F(r['rhs']) for name, r in rows.items()}
    assert min(slacks.values()) >= 0
    assert all(slacks[k] == F(v) for k, v in cert['raw_row_slacks'].items())
    obj = dot(inp['objective'])
    assert obj == F(cert['objective']) == F(243427385229576983115, 571565195660569935844)
    dual = cert['dual']
    lam = {k: F(v) for k, v in dual['row_weights'].items()}
    assert len(lam) == 13 and min(lam.values()) > 0
    nu = F(dual['normalization_multiplier'])
    residual = []
    for j in range(n):
        s = str(j)
        r = F(inp['objective'].get(s, '0'))-nu*F(eq['a'].get(s, '0'))
        r -= sum((v*F(rows[k]['a'].get(s, '0')) for k, v in lam.items()), F(0))
        assert r >= 0
        assert r == F(dual['nonnegative_column_residual'].get(s, '0'))
        assert r*p.get(j, F(0)) == 0
        residual.append(r)
    dual_obj = nu*F(eq['rhs']) + sum((v*F(rows[k]['rhs']) for k, v in lam.items()), F(0))
    assert dual_obj == obj
    assert all(slacks[k] == 0 for k in lam)
    assert residual[inp['K_column']] == 0
    D = obj.denominator
    positive = [r for r in residual[:256] if r > 0]
    assert len(positive) == 239
    assert min(positive)*D == 410276723457467770
    out = {
        'status': 'PASS', 'scope': 'Main exact matrix replay; separate audit rebuilds source coefficients',
        'input_sha256': sha(ip), 'certificate_sha256': sha(cp),
        'raw_rows': len(rows), 'nonnegative_columns': n, 'positive_dual_rows': len(lam),
        'atom_residual_zero': 256-len(positive), 'atom_residual_positive': len(positive),
        'K_residual': '0', 'objective': str(obj), 'objective_decimal': float(obj),
        'dual_objective': str(dual_obj), 'half_gap': str(F(1, 2)-obj),
        'min_positive_D_scaled_atom_residual': str(min(positive)*D),
        'released_for_new_obligations': ['true largest-label membership completion', 'four true forced-X branch completion'],
        'not_claimed': ['half coverage', 'complete SPE realization', 'best-known lower bound']
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return out

if __name__ == '__main__':
    main()
