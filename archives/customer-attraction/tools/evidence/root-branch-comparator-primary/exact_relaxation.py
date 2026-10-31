from pathlib import Path
from fractions import Fraction as F
from math import comb, lcm
import itertools
import json
import numpy as np

base = Path(__file__).resolve().parent
source = base / 'original/research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round13/direct/root_branch_lp.py.npz'
with np.load(source, allow_pickle=False) as z:
    assert set(z.files) == {'bits', 'j', 'rows', 'W', 'weights', 'names'}
    bits, tags, frozen_rows, W, weights, names = [z[k] for k in ('bits', 'j', 'rows', 'W', 'weights', 'names')]
expected = np.repeat(np.array(list(itertools.product([0, 1], repeat=9)), int).T, 6, axis=1)
assert np.array_equal(bits, expected)
assert np.array_equal(tags, np.tile(np.arange(6), 512))
bits = expected
Q = 9000
rows, row_names, all_pay = [], [], []
o = (tags > 0).astype(int)

def add(name, values):
    values = list(values)
    assert all(v.denominator == 1 if isinstance(v, F) else True for v in values)
    rows.append([int(v) for v in values])
    row_names.append(name)

for r, path in enumerate(([0, 1, 2, 3, 4], [4, 5, 6, 7, 8])):
    c = bits[path].sum(axis=0)
    pay = np.array([[Q // int(cx) * int(bit) if cx else 0 for bit, cx in zip(bits[t], c)] for t in path], dtype=int)
    all_pay.append(pay)
    for i in range(0 if r == 0 else 1, 5):
        p = bits[path[:i]].sum(axis=0)
        k = 5 - i
        inv = np.array([Q // int(v + k) for v in p])
        assert all(Q % int(v + k) == 0 for v in p)
        for t in range(9):
            add(f'{r}:{i}:K{t}', pay[i] - inv * bits[t])
        add(f'{r}:{i}:sumopt', 5 * pay[i] - inv * tags)
        add(f'{r}:{i}:O', 5 * k * pay[i] + p * inv - Q * o)
        if k in (3, 4):
            alpha = F(5, 3) if k == 3 else F(1499, 750)
            tail = pay[i:].sum(axis=0)
            values = []
            for px, d, u in zip(p, tags, tail):
                benchmark = sum((F(comb(int(d), q) * comb(5 - int(d), k - q) * q, int(px) + q)
                                 for q in range(1, k + 1) if q <= d and 0 <= k - q <= 5 - d), F(0))
                values.append(comb(5, k) * alpha * int(u) - Q * benchmark)
            add(f'{r}:{i}:profit{k}', values)
    p = bits[path[:3]].sum(axis=0)
    H = pay[3] + pay[4] + np.array([Q * int(b) // ((int(px)+1)*(int(px)+2)) for b, px in zip(bits[path[3]], p)])
    add(f'{r}:twoO', [F(5, 2)*int(h) + F(Q*int(px),int(px)+1) - Q*int(ox) for h, px, ox in zip(H,p,o)])
    add(f'{r}:twoj', [10*int(h) - F(Q*int(d)*(5-int(d)),int(px)+1) - F(Q*int(d)*(int(d)-1),int(px)+2) for h,px,d in zip(H,p,tags)])
add('root', all_pay[0][0] - all_pay[1][0])
assert row_names == names.tolist()
assert np.array_equal(W, (bits[:5].sum(axis=0)>0))
exact_float = np.array(rows, dtype=float) / Q
coefficient_error = float(np.max(np.abs(exact_float - frozen_rows)))
assert coefficient_error < 1e-12

support = np.flatnonzero(weights > 1e-8).tolist()
active = np.flatnonzero(np.abs(frozen_rows @ weights) < 1e-8).tolist()
basis = {}
chosen = []
equations = [('W', [int(W[j]) for j in support], F(1))]
equations += [(row_names[i], [rows[i][j] for j in support], F(0)) for i in active]
for name, coefficients, rhs in equations:
    row = list(map(F, coefficients))
    for pivot in sorted(basis):
        if row[pivot]:
            factor = row[pivot]
            previous, previous_rhs = basis[pivot]
            row = [a - factor*b for a,b in zip(row,previous)]
            rhs -= factor*previous_rhs
    pivot = next((j for j,a in enumerate(row) if a), None)
    if pivot is None:
        continue
    value = row[pivot]
    basis[pivot] = ([a/value for a in row], rhs/value)
    chosen.append(name)
    if len(basis) == len(support):
        break
assert len(basis) == len(support)
solution = [F(0)] * len(support)
for pivot in sorted(basis, reverse=True):
    row, rhs = basis[pivot]
    solution[pivot] = rhs - sum((row[j]*solution[j] for j in range(pivot+1,len(solution))),F(0))
x = [F(0)] * len(tags)
for j, value in zip(support, solution):
    x[j] = value
assert min(x) >= 0
assert sum((F(int(w))*a for w,a in zip(W,x)),F(0)) == 1
residuals = [sum((F(row[j])*x[j] for j in support),F(0)) for row in rows]
assert min(residuals) >= 0
beta = sum((x[j] for j in support if tags[j]>0),F(0))
assert beta > 2
den = lcm(*(v.denominator for v in solution))
record = {
    'fields_read': ['bits','j','rows','W','weights','names'],
    'all_type_columns_and_108_named_rows_reconstructed': True,
    'rational_interpretation_scale_Q': Q,
    'maximum_float_coefficient_difference': coefficient_error,
    'frozen_float_benchmark': float(o @ weights),
    'frozen_float_min_residual': float((frozen_rows @ weights).min()),
    'positive_support_columns': len(support),
    'selected_exact_equations': chosen,
    'recovery': 'exact Gaussian elimination on W and independent near-tight source rows; all 108 rational rows verified afterwards',
    'exact_benchmark': str(beta), 'exact_benchmark_minus_two': str(beta-2),
    'exact_minimum_Q_scaled_residual': str(min(residuals)),
    'integer_scale_and_W': den,
    'integer_benchmark': int(beta*den),
    'integer_total_mass': int(sum(x,F(0))*den),
    'maximum_weight_distance_from_frozen_float': max(abs(float(x[j])-float(weights[j])) for j in range(len(x))),
    'nonzero_augmented_types': [{'nine_theme_bits': ''.join(map(str,bits[:,j].tolist())), 'comparison_multiplicity_j': int(tags[j]), 'weight': str(x[j]), 'integer_mass': int(x[j]*den)} for j in support],
    'exact_Q_scaled_residuals': [{'name':name,'residual':str(v)} for name,v in zip(row_names,residuals)],
    'scope': 'exact finite witness for the rational interpretation of this 108-row relaxation only; no complete catalog, comparator-optimality, complete SPE or original-half counterexample certified'
}
(base/'exact-relaxation-witness.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print('exact beta', beta, 'gap', beta-2, 'scale', den, 'support',len(support),'coefficient error',coefficient_error)
