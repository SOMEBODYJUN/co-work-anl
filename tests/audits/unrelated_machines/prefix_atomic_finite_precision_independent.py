from fractions import Fraction as F
from itertools import product
from math import prod
import json


def sharp_path(degrees, alpha):
    nleaves = prod(degrees)
    if nleaves == 1:
        return F(1)
    used_error = min(alpha, F(1, 2 * (nleaves - 1)))
    parent = F(1)
    cumulative = 1
    for d in degrees:
        cumulative *= d
        chosen = (1 + 2 * used_error) / cumulative - 2 * used_error
        others = [chosen + 2 * used_error] * (d - 1)
        assert chosen >= 0
        assert chosen + sum(others, F(0)) == parent
        estimates = [chosen + used_error] + [x - used_error for x in others]
        assert all(abs(h - x) <= alpha for h, x in zip(estimates, [chosen] + others))
        assert estimates[0] == max(estimates)
        parent = chosen
    expected = max(F(0), (1 - 2 * alpha * (nleaves - 1)) / nleaves)
    assert parent == expected
    return parent


def main():
    equality_paths = 0
    precision_cases = 0
    for n in range(5):
        for degrees in product(range(1, 5), repeat=n):
            nleaves = prod(degrees)
            alphas = [F(0), F(1, 4 * nleaves), F(1, 2 * nleaves), F(1), F(2)]
            if nleaves > 1:
                alphas += [F(1, 2 * (nleaves - 1)), F(1, nleaves - 1)]
            for alpha in alphas:
                sharp_path(degrees, alpha)
                equality_paths += 1
            alpha = F(1, 4 * nleaves)
            bound = (1 - 2 * alpha * (nleaves - 1)) / nleaves
            assert bound == F(nleaves + 1, 2 * nleaves ** 2)
            assert bound > F(1, 2 * nleaves)
            for q in [1, 2, 7, 37, 2 ** 127 + 7]:
                tau = F(1, 4 * q * nleaves)
                assert tau / bound == F(nleaves, 2 * q * (nleaves + 1))
                assert tau / bound < F(1, 2 * q)
                assert F(1, q) > tau / bound
                precision_cases += 1

    local_adversaries = 0
    # Exhaust all mass compositions on denominator 8 and all endpoint errors.
    def compositions(total, parts):
        if parts == 1:
            yield (total,)
            return
        for first in range(total + 1):
            for tail in compositions(total - first, parts - 1):
                yield (first,) + tail

    for d in range(1, 5):
        for numerators in compositions(8, d):
            true = [F(x, 8) for x in numerators]
            for alpha in [F(0), F(1, 16), F(1, 8), F(1, 2)]:
                for signs in product((-1, 1), repeat=d):
                    estimates = [x + sign * alpha for x, sign in zip(true, signs)]
                    chosen = max(range(d), key=lambda j: estimates[j])
                    bound = (1 - 2 * alpha * (d - 1)) / d
                    assert true[chosen] >= max(F(0), bound)
                    local_adversaries += 1

    dilution_cases = []
    for k in [0, 1, 2, 5, 20, 100]:
        nleaves = 2 ** k
        for d in [F(1), F(1, 7), F(11, 37)]:
            q = d.denominator
            absolute = d / nleaves
            proposed_tau = F(1, 4 * q * nleaves)
            assert absolute > proposed_tau
            for delta in [d / 2, d, 2 * d]:
                assert (-d / nleaves >= -delta / nleaves) == (d <= delta)
            dilution_cases.append({"k": k, "N": str(nleaves), "d": str(d), "absolute_bad_localizer": str(absolute)})

    print(json.dumps({
        "sharp_equalities_with_nonnegative_truncation": equality_paths,
        "precision_grid_constant_checks": precision_cases,
        "local_extreme_error_adversaries": local_adversaries,
        "dilution_examples": len(dilution_cases),
        "largest_uniform_leaf_count": str(2 ** 100),
        "author_proof_read": False,
        "oracle_generated_or_validated": False,
        "status": "all exact finite audits passed"
    }, indent=2))


if __name__ == "__main__":
    main()
