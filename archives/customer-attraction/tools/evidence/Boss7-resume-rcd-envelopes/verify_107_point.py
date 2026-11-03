"""Independent stdlib check of the frozen 21-atom, 107-row feasible point.

No optimization, support recovery, game construction, or import of legacy code.
The row definitions implement the formulas documented in the cleaned object.
"""
from fractions import Fraction as Q
from math import comb
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
EXACT = HERE / 'original/root_family_pressure_exact.json'
DISCOVERY = HERE / 'original/root_family_pressure_discovery.json'
BETA = {1: Q(1), 2: Q(3, 2), 3: Q(5, 3), 4: Q(1499, 750)}


def gain(numerator, denominator):
    return Q(numerator, denominator) if numerator else Q(0)


def comparison(prefix, multiplicity, count):
    return sum((comb(multiplicity, d) * comb(5 - multiplicity, count - d)
                * gain(d, prefix + d)
                for d in range(max(0, count + multiplicity - 5),
                               min(count, multiplicity) + 1)), Q(0))


def coefficients(atom):
    a = atom['actual']
    j = atom['opt_multiplicity']
    x, y = atom['root_if_t1'], atom['root_if_t0']
    assert len(a) == 5 and len(x) == len(y) == 4
    assert all(v in (0, 1) and type(v) is int for v in a + x + y)
    assert type(j) is int and 0 <= j <= 5
    assert j != 0 or x == [0] * 4
    assert j != 5 or y == [0] * 4
    c = sum(a)
    actual = [gain(v, c) for v in a]
    result = {}

    def put(name, value):
        assert name not in result
        result[name] = value

    for i in range(5):
        denominator = sum(a[:i]) + 5 - i
        for q in range(5):
            put(f'act:{i}:a{q}', actual[i] - gain(a[q], denominator))
        put(f'act:{i}:opt', 5 * actual[i] - gain(j, denominator))
    for count in range(1, 5):
        put(f'act:profit{count}', comb(5, count) * BETA[count]
            * sum(actual[5-count:]) - comparison(sum(a[:5-count]), j, count))

    branches = ((1, x, j), (0, y, 5-j))
    future = [sum((multiplicity * gain(z[k], t + sum(z))
                   for t, z, multiplicity in branches), Q(0))
              for k in range(4)]
    put('root:IC', 5 * actual[0] - gain(j, 1 + sum(x)))
    for k in range(4):
        remaining = 4-k

        def query(value):
            return sum((multiplicity * gain(value(t, z), t + sum(z[:k]) + remaining)
                        for t, z, multiplicity in branches), Q(0))

        for q in range(5):
            put(f'root:child{k}:a{q}', future[k] - query(lambda t, z: a[q]))
        put(f'root:child{k}:opt', 5 * future[k] - query(lambda t, z: j))
        put(f'root:child{k}:ownT', future[k] - gain(j, 1 + sum(x[:k]) + remaining))
        for i in range(5):
            put(f'act:{i}:rootmenu{k}', 5 * actual[i]
                - gain(j*x[k] + (5-j)*y[k], sum(a[:i]) + 5-i))
        for ell in range(4):
            put(f'root:child{k}:own{ell}', future[k] - query(lambda t, z: z[ell]))
    for count in range(1, 5):
        offset = 4-count
        lhs = comb(5, count) * BETA[count] * sum(future[offset:])
        for tag, multiplicity in (('opt', j), ('actual', c)):
            rhs = sum((weight * comparison(t + sum(z[:offset]), multiplicity, count)
                       for t, z, weight in branches), Q(0))
            put(f'root:profit{count}:{tag}', lhs - rhs)
    assert len(result) == 107
    return result, int(c > 0), int(j > 0)


def rank(matrix):
    rows = [list(map(Q, row)) for row in matrix]
    pivot = 0
    for column in range(len(rows[0])):
        chosen = next((r for r in range(pivot, len(rows)) if rows[r][column]), None)
        if chosen is None:
            continue
        rows[pivot], rows[chosen] = rows[chosen], rows[pivot]
        divisor = rows[pivot][column]
        rows[pivot] = [v/divisor for v in rows[pivot]]
        for r in range(pivot+1, len(rows)):
            factor = rows[r][column]
            rows[r] = [v-factor*w for v, w in zip(rows[r], rows[pivot])]
        pivot += 1
        if pivot == len(rows):
            break
    return pivot


def main():
    exact = json.loads(EXACT.read_text())
    discovery = json.loads(DISCOVERY.read_text())
    atoms = exact['point']
    assert exact['rows'] == discovery['rows'] == 107
    assert exact['atoms'] == len(atoms) == len(discovery['atoms']) == 21
    assert discovery['columns'] == 33792
    masses = [Q(atom['mass']) for atom in atoms]
    assert min(masses) > 0
    for exact_atom, float_atom in zip(atoms, discovery['atoms']):
        assert {k: v for k, v in exact_atom.items() if k != 'mass'} == {
            k: v for k, v in float_atom.items() if k != 'mass_float'}
    cols = [coefficients(atom) for atom in atoms]
    names = list(cols[0][0])
    assert all(list(col[0]) == names for col in cols)
    assert list(exact['slacks']) == names
    slacks = {name: sum((mass * col[0][name] for mass, col in zip(masses, cols)), Q(0))
              for name in names}
    assert all(Q(exact['slacks'][name]) == value for name, value in slacks.items())
    assert min(slacks.values()) >= 0
    W = sum((mass * col[1] for mass, col in zip(masses, cols)), Q(0))
    O = sum((mass * col[2] for mass, col in zip(masses, cols)), Q(0))
    assert W == Q(exact['W']) == 1
    assert O == Q(exact['O']) and O-2*W == Q(exact['O_minus_2W']) > 0
    assert min(slacks.values()) == Q(exact['min_row_slack']) == 0
    selected = exact['selected_zero_rows']
    assert len(selected) == len(set(selected)) == 20
    assert all(name in slacks and slacks[name] == 0 for name in selected)
    selected_matrix = [[col[1] for col in cols]] + [[col[0][name] for col in cols] for name in selected]
    assert rank(selected_matrix) == 21
    out = {
        'status': 'passed',
        'scope': 'Exact feasible point of named affine relaxation only; no game/SPE or optimality claim',
        'inputs_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (EXACT, DISCOVERY)},
        'atoms': len(atoms), 'rows': len(names), 'coefficient_entries': len(atoms)*len(names),
        'strictly_positive_masses': len(masses), 'W': str(W), 'O': str(O),
        'O_minus_2W': str(O-2*W), 'min_row_slack': str(min(slacks.values())),
        'nonnegative_slacks': len(slacks), 'zero_slacks': sum(v == 0 for v in slacks.values()),
        'selected_zero_rows': selected, 'selected_plus_normalization_rank': 21,
        'all_reported_slacks_equal': True, 'discovery_descriptors_equal': True,
        'all_opt_multiplicities': sorted({a['opt_multiplicity'] for a in atoms}),
        'slacks': {k: str(v) for k, v in slacks.items()},
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
