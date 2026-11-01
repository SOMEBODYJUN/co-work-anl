"""Parent reconstruction of the ordered early-floor certificate, from raw rows."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

EARLY_WEIGHTS = (F(1, 3), F(1, 2), F(1, 2), F(2, 3))


def quotient(n, d):
    return F(n, d) if n else F(0)


def main():
    rho = {}
    reduced_count = 0
    count_with_overlap = 0
    minimum = None
    by_load = {k: None for k in range(5)}
    for early in product((0, 1), repeat=4):
        p = sum(early)
        for a, b in product((0, 1), repeat=2):
            load = p + a + b
            actual = [quotient(bit, load) for bit in (*early, a, b)]
            assert sum(actual) == int(load > 0)
            early_gaps = [actual[j] - F(a, sum(early[:j]) + 6 - j)
                          for j in range(4)]
            last_gap = actual[5] - F(a, p + a + 1)
            local_min = None
            for d, ell in product(range(7), repeat=2):
                admissible = not a or p >= 3
                reduced_count += admissible
                pair_values = set()
                for h in range(max(0, d + ell - 6), min(d, ell) + 1):
                    pair_den = (p + 1) * (p + 2)
                    S = 6 * actual[4] - F(d, p + 1) + F(h, pair_den)
                    Z = 6 * actual[5] - F(ell, p + a + 1)
                    V = F(d * ell - 6 * h, pair_den)
                    certificate = (S + Z / 12 + V / 6
                                   + sum(w * g for w, g in zip(EARLY_WEIGHTS, early_gaps))
                                   + F(3, 2) * last_gap)
                    residual = 2 * int(load > 0) - int(d > 0) - certificate
                    pair_values.add(residual)
                    if admissible:
                        count_with_overlap += 1
                        assert residual >= 0, (early, a, b, d, ell, h, residual)
                        minimum = residual if minimum is None else min(minimum, residual)
                assert len(pair_values) == 1  # Exact h cancellation, not an independence assumption.
                value = pair_values.pop()
                local_min = value if local_min is None else min(local_min, value)
            key = ''.join(map(str, (*early, a, b)))
            rho[key] = str(local_min)
            if a:
                by_load[p] = local_min if by_load[p] is None else min(by_load[p], local_min)
            else:
                assert local_min >= 0
    expected = (F(-1079, 360), F(-299, 360), F(-93, 360), F(2, 360), F(42, 360))
    assert tuple(by_load.values()) == expected
    source_path = Path(__file__).with_name('research_1') / 'threefold_penultimate_exact.json'
    source = json.loads(source_path.read_text())
    assert source['rho_actual_membership'] == rho
    assert source['complete_restricted_state_count'] == reduced_count
    assert reduced_count == 2058 and count_with_overlap == 3528
    return {
        'status': 'passed',
        'scope': 'conditional HALF-6 and unrestricted residual formula only',
        'reduced_state_count': reduced_count,
        'state_count_with_overlap': count_with_overlap,
        'minimum_residual': str(minimum),
        'rho_table_equal_to_author': True,
        'minimum_A_residual_by_early_load': {str(k): str(v) for k, v in by_load.items()},
        'rho_actual_membership': rho,
    }


if __name__ == '__main__':
    print(json.dumps(main(), ensure_ascii=False, indent=2))
