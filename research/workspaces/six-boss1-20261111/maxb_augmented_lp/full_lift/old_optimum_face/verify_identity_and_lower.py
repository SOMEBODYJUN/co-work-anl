"""Independent exact whole-old-face identity and improved-full-dual audit.

No elimination or bound-construction module is imported. Checks the old
dual itself, every20585 signed-identity coefficient and every21021 new-dual
residual directly from frozen matrices and independently loaded weights.
"""
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import gzip
import json
import time

HERE = Path(__file__).resolve().parent
FULL = HERE.parent
WORK = HERE.parents[2]
BASE = WORK / 'full624_augmented_lp/recovery'


def sha(path): return sha256(path.read_bytes()).hexdigest()


def read(path):
    if path.suffix == '.gz':
        with gzip.open(path, 'rt') as f: return json.load(f)
    return json.loads(path.read_text())


@lru_cache(maxsize=None)
def frac(value): return F(value)


def main():
    start = time.monotonic()
    assert sha(BASE / 'exact_matrix.json.gz') == '96388092e21621f157b4428ce99f98b93afa99ed3a0c12c72b1d6475c26fba30'
    assert sha(BASE / 'exact_dual_certificate.json') == '22381bc9844aa5452b45a5bd8ef4a6148808388455b80666b49475df0f7377b3'
    assert sha(FULL / 'exact_matrix.json.gz') == 'c054aadf745ea4540233a3da693917498527d19d4ccecb0fdd34ad884e461e4b'
    old = read(BASE / 'exact_matrix.json.gz'); full = read(FULL / 'exact_matrix.json.gz')
    assert full['rows'][:20910] == old['rows'] and full['columns'][:20585] == old['columns']
    dual = read(BASE / 'exact_dual_certificate.json'); w = F(dual['normalization_multiplier'])
    residual = [F(c) - w * F(a) for c, a in zip(old['objective'], old['normalization'])]
    positive_rows = {}
    for i, text in dual['row_multipliers']:
        value = F(text); assert value > 0 and i not in positive_rows
        positive_rows[i] = value
        for j, a in old['rows'][i]: residual[j] -= value * frac(a)
    assert min(residual) >= 0 and residual == list(map(F, dual['residuals']))
    identity = read(HERE / 'old_optimal_face_cut_identity.json')
    alpha = F(identity['normalization_coefficient']); assert alpha < 0
    lhs = [alpha * F(a) for a in old['normalization']]
    for i, text in identity['row_coefficients']:
        assert i in positive_rows
        for j, a in old['rows'][i]: lhs[j] += F(text) * frac(a)
    for j, text in identity['zero_column_coefficients']:
        assert residual[j] > 0
        lhs[j] += F(text)
    cut = [F()] * 20585
    cut_certificate = read(WORK / 'terminal_response_cycles/max_b_exact_certificate.json')
    assert sha(WORK / 'terminal_response_cycles/max_b_exact_certificate.json') == 'f6189600d6ccccdbd9fcbc4ae4af9e768c9382af8de1ae41d6e6a7ee7662f664'
    for j, text in cut_certificate['sparse_original4849_row_K_normalized']: cut[j] = F(text)
    assert lhs == cut and alpha == F(cut_certificate['K_normalized_point_value'])
    new_dual = read(HERE / 'strict_lower_bound_certificate.json')
    lower = F(new_dual['normalization_multiplier']); assert lower > w
    new_residual = [F(c) - lower * F(a) for c, a in zip(full['objective'], full['normalization'])]
    seen = set()
    for i, text in new_dual['row_multipliers']:
        assert 0 <= i < 22297 and i not in seen; seen.add(i)
        value = F(text); assert value > 0
        for j, a in full['rows'][i]: new_residual[j] -= value * frac(a)
    assert len(new_residual) == 21021 and min(new_residual) >= 0
    assert new_residual == list(map(F, new_dual['residuals']))
    assert new_dual['matrix_sha256'] == sha(FULL / 'exact_matrix.json.gz')
    report = {'status': 'PASS', 'old_dual_coefficients_checked': 20585,
              'whole_face_identity_coefficients_checked': 20585,
              'identity_row_support_subset_of_old_strictly_positive_dual_rows': True,
              'identity_column_support_subset_of_old_strictly_positive_residual_columns': True,
              'whole_old_optimum_face_cut_value': str(alpha), 'whole_old_optimum_face_excluded': True,
              'new_dual_residuals_checked': 21021, 'new_dual_nonnegative_row_weights': len(seen),
              'old_lower': str(w), 'new_lower': str(lower), 'new_lower_float': float(lower),
              'exact_improvement': str(lower - w), 'improvement_float': float(lower - w),
              'exact_optimum_claim': False, 'optimizer_calls': 0,
              'identity_sha256': sha(HERE / 'old_optimal_face_cut_identity.json'),
              'strict_lower_certificate_sha256': sha(HERE / 'strict_lower_bound_certificate.json'),
              'verifier_sha256': sha(Path(__file__)), 'seconds': time.monotonic() - start,
              'scope': 'Exact strict lower bound for the full common-X fixed16-hist LP; original six-player SPE half remains open.'}
    p = HERE / 'independent_audit.json'; assert not p.exists()
    p.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)


if __name__ == '__main__': main()
