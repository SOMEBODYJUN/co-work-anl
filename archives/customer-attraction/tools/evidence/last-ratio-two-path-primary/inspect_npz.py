from pathlib import Path
from fractions import Fraction
from math import lcm
import io
import json
import pickle
import sys
import zipfile
import numpy as np

class ArrayNamesOnly(pickle.Unpickler):
    def find_class(self, module, name):
        if module == 'numpy' and name in ('ndarray', 'dtype'):
            return getattr(np, name)
        if module in ('numpy.core.multiarray', 'numpy._core.multiarray') and name == '_reconstruct':
            return np._core.multiarray._reconstruct
        raise ValueError('Unexpected pickle class: ' + module + '.' + name)

def inspect(path, m):
    n = 2 * m - 1
    with np.load(path, allow_pickle=False) as z:
        assert set(z.files) == {'bits', 'weights', 'rows', 'names'}
        bits, weights, rows = [z[k] for k in ('bits', 'weights', 'rows')]
    with zipfile.ZipFile(path) as archive:
        names_file = io.BytesIO(archive.read('names.npy'))
        version = np.lib.format.read_magic(names_file)
        assert version in ((1, 0), (2, 0)), version
        reader = np.lib.format.read_array_header_1_0 if version == (1, 0) else np.lib.format.read_array_header_2_0
        shape, fortran, dtype = reader(names_file)
        assert dtype == np.dtype(object) and not fortran
        names = ArrayNamesOnly(names_file).load()
        assert names.shape == shape
    import itertools
    expected_bits = np.array(list(itertools.product([0, 1], repeat=n)), float).T
    assert np.array_equal(bits, expected_bits)
    paths = [list(range(m)), [m - 1] + list(range(m, n))]
    counts = [bits[p].sum(axis=0) for p in paths]
    pay = [np.divide(bits[p], c, out=np.zeros((m, len(c))), where=c > 0)
           for p, c in zip(paths, counts)]
    expected_rows, expected_names = [], []
    for r, route in enumerate(paths):
        for i in range(0 if r == 0 else 1, m):
            prefix = bits[route[:i]].sum(axis=0)
            for j in range(n):
                expected_rows.append(pay[r][i] - bits[j] / (prefix + m - i))
                expected_names.append((r, i, j))
    expected_rows.append(pay[0][0] - pay[1][0])
    expected_names.append('root')
    assert np.array_equal(rows, np.array(expected_rows))
    assert names.tolist() == expected_names
    assert weights.shape == (2**n,) and np.isfinite(weights).all()
    W = (counts[0] > 0).astype(float)
    Q = lcm(*range(1, m + 1))
    coeff = np.rint(rows * Q).astype(int)
    assert np.allclose(rows * Q, coeff, atol=1e-12, rtol=0)
    fractions = [Fraction(float(x)).limit_denominator(10**7) for x in weights]
    den = lcm(*(v.denominator for v in fractions))
    integers = [int(v * den) for v in fractions]
    exact_residuals = [sum(int(a) * b for a, b in zip(row, integers)) for row in coeff]
    exact_W = sum(int(a) * b for a, b in zip(W, integers))
    last = np.rint(pay[0][-1] * Q).astype(int)
    exact_last = sum(int(a) * b for a, b in zip(last, integers))
    return {
        'm': m, 'n_themes': n, 'n_types_including_empty': 2**n,
        'rows_shape': list(rows.shape), 'all_bits_rows_and_names_reconstructed_exactly': True,
        'pickle_scope': 'only numpy ndarray/dtype/reconstruct; values checked against all expected row labels',
        'float_min_weight': float(weights.min()),
        'float_min_relaxation_residual': float((rows @ weights).min()),
        'float_actual_coverage': float(W @ weights),
        'float_last_payoff': float(pay[0][-1] @ weights),
        'rationalization': 'same limit_denominator(10**7) as original checker',
        'integer_client_scale': den,
        'integer_total_clients_including_empty_type': sum(integers),
        'integer_actual_coverage': exact_W,
        'integer_last_profit_Q_scaled': exact_last,
        'payoff_scale_Q': Q,
        'exact_last_over_actual_coverage': str(Fraction(exact_last, Q * exact_W)),
        'all_rational_weights_nonnegative': min(integers) >= 0,
        'exact_W_equals_den': exact_W == den,
        'all_rationalized_relaxation_rows_nonnegative': min(exact_residuals) >= 0,
        'minimum_Q_den_scaled_row_residual': min(exact_residuals),
        'nonzero_types': [
            {'interests': ''.join(str(int(x)) for x in bits[:, j]), 'integer_clients': z}
            for j, z in enumerate(integers) if z
        ],
        'semantic_limit': 'These rows are local worst-future lower-bound necessities plus one root comparison; reconstructing every row is not an original complete-history SPE certificate. Original checker only enumerates full SPE outcomes for m<=4.'
    }

if __name__ == '__main__':
    prefix = Path(sys.argv[1])
    destination = Path(sys.argv[2])
    destination.parent.mkdir(parents=True, exist_ok=True)
    result = [inspect(Path(str(prefix) + f'.{m}.npz'), m) for m in (3, 4, 5)]
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    for r in result:
        print(r['m'], r['rows_shape'], r['float_last_payoff'],
              r['exact_last_over_actual_coverage'],
              r['all_rationalized_relaxation_rows_nonnegative'])
