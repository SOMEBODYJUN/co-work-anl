from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


def rows(v, y, t):
    a1, a2, a3, a4, _, a6, x, o = v
    b = a1 + a2 + a3
    h = b + x + 1
    d = b + a4 + 1
    theta = Fraction(o, 6)
    wallet = Fraction(y, h + t) + Fraction(t, h + y) + Fraction(y, h * (h + 1))
    return (
        Fraction(x, b + 1 + y + t),
        Fraction(y, d),
        Fraction(t),
        (theta - t) / (h + y),
        (a6 + theta) / h - a6 * theta / (h * (h + 1)) - wallet,
        (t + theta) / d - t * theta / (d * (d + 1)),
    )


def check_released_point():
    relative = Path('research/workspaces/six-boss1-20261111/universal_union_wallet_lp')
    candidates = (Path.cwd(), *Path(__file__).resolve().parents)
    folder = next(base / relative for base in candidates if (base / relative).is_dir())
    input_bytes = (folder / 'exact_input.json').read_bytes()
    certificate_bytes = (folder / 'exact_certificate.json').read_bytes()
    assert sha256(input_bytes).hexdigest() == 'f87a60372dee7449332b17721be6aa70012fb3aca251825cb2e9dd755ff01e41'
    assert sha256(certificate_bytes).hexdigest() == 'ccc085060427e2999a8e4f00ac3414d7e20a1c6e66aeba8d3e658ae34cb16c85'
    atoms = json.loads(input_bytes)['atom_columns']
    primal = {int(k): Fraction(v) for k, v in json.loads(certificate_bytes)['primal'].items()}
    weights = (4096, 800, 71, 384, 512, 900)
    bounds = [Fraction(0) for _ in range(6)]
    bounds[2] = primal[256]
    separate = [Fraction(0) for _ in range(6)]
    joint = Fraction(0)
    for atom in atoms:
        v = tuple(atom['a']) + (atom['x'], atom['o'])
        mass = primal.get(atom['index'], Fraction(0))
        assert mass >= 0
        pay = [rows(v, y, t) for y, t in product(range(2), repeat=2)]
        for r in range(6):
            separate[r] += mass * min(row[r] for row in pay)
        joint += mass * min(sum(weight * value for weight, value in zip(weights, row)) for row in pay)
        cover = sum(v[:6]) or 1
        potential = Fraction(v[6], sum(v[:4]) + 1)
        bounds[0] += mass * Fraction(v[3], cover)
        bounds[1] += mass * potential
        bounds[5] += mass * (Fraction(v[4], cover) + potential)
    individual_residuals = [rhs - lhs for rhs, lhs in zip(bounds, separate)]
    assert all(residual > 0 for residual in individual_residuals)
    independent_residual = sum(weight * value for weight, value in zip(weights, individual_residuals))
    combined_residual = sum(weight * value for weight, value in zip(weights, bounds)) - joint
    assert independent_residual == Fraction(6709377370147572650596141, 6430108451181411778245)
    assert combined_residual == Fraction(-128742478797765148513379, 2572043380472564711298)
    assert independent_residual - combined_residual == joint - sum(weight * value for weight, value in zip(weights, separate))
    print('Individual projected rows at released point:', *individual_residuals)
    print('Combined residuals at released point (separate, joint):', independent_residual, combined_residual)


def main():
    tails = tuple(product(range(2), repeat=2))
    fixed = (4096, 800, 71, 384, 512, 900)
    gaps = []
    for v in product(range(2), repeat=8):
        h = sum(v[:3]) + v[6] + 1
        pay = {tail: rows(v, *tail) for tail in tails}
        row_minima = [min(row[i] for row in pay.values()) for i in range(6)]
        exact_sets = [
            {tail for tail, row in pay.items() if row[i] == row_minima[i]}
            for i in range(6)
        ]
        predicted_sets = [
            {(1, 1)} if v[6] else set(tails),
            {(0, 0), (0, 1)},
            {(0, 0), (1, 0)},
            {(0, 1)},
            {(1, 0), (1, 1)} if h == 1 else {(1, 1)},
            {(0, 0), (1, 0)},
        ]
        assert exact_sets == predicted_sets, (v, exact_sets)
        for support in product(range(2), repeat=6):
            predicted = set(tails)
            for is_active, minimizers in zip(support, predicted_sets):
                if is_active:
                    predicted &= minimizers
            joint = min(sum(x * y for x, y in zip(support, row)) for row in pay.values())
            independent = sum(x * y for x, y in zip(support, row_minima))
            assert (joint == independent) == bool(predicted), (v, support)
        d = sum(v[:4]) + 1
        theta = Fraction(v[7], 6)
        for weight2, weight3, weight5 in product((0, 1, 5), repeat=3):
            sparse = (0, 0, weight2, weight3, 0, weight5)
            minimum = min(sum(x * y for x, y in zip(sparse, row)) for row in pay.values())
            independent = sum(x * y for x, y in zip(sparse, row_minima))
            bound = min(
                weight3 * (h + 1 - theta) / (h * (h + 1)),
                weight2 + weight5 * (d + 1 - theta) / (d * (d + 1)),
            )
            uniform = min(Fraction(7, 36) * weight3, weight2 + Fraction(7, 36) * weight5)
            assert minimum - independent == bound >= uniform
            if h == d == 5 and theta == Fraction(1, 6):
                assert bound == uniform

        joint = min(sum(x * y for x, y in zip(fixed, row)) for row in pay.values())
        independent = sum(x * y for x, y in zip(fixed, row_minima))
        gaps.append((joint - independent, v, joint, independent))

    smallest = min(gaps)
    largest = max(gaps)
    assert smallest[:2] == (Fraction(1632, 5), (1, 1, 1, 0, 0, 0, 0, 0))
    assert largest[0] == 1760
    assert gaps[0][2:] == (0, -1152)
    assert all(gap == joint - independent for gap, _, joint, independent in gaps)
    print('Types:', len(gaps), 'tail states:', len(tails), 'support patterns per type:', 2**6)
    print('Smallest (gap, type, joint, independent):', smallest)
    print('Largest (gap, type, joint, independent):', largest)
    print('Zero type (gap, type, joint, independent):', gaps[0])


if __name__ == '__main__':
    main()
    check_released_point()
