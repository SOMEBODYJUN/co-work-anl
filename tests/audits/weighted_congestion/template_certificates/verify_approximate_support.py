"""小用户支持近似表示：逐列收费界及有限参数的精确核验。

Run from the repository root. No solver, randomness or floating-point arithmetic.
The general representation obstruction is proved in selector_local_moments.md.
"""
from fractions import Fraction as F
from itertools import combinations, product
from hashlib import sha256
from pathlib import Path
import json
import platform
import sys


def main():
    columns = parameters = zero_faces = 0
    # Alternate representation weights, unrelated to the original (1,eps,...).
    for n in range(2, 8):
        for weights in (tuple(F(1) for _ in range(n)),
                        tuple(F(i + 1, 2 * i + 1) for i in range(n))):
            for phases in product((-1, 0, 1), repeat=n):
                # -1 means no use; 0/1 means the labelled action using the resource.
                if 0 not in phases:
                    continue
                i = phases.index(0)
                load = sum((w for w, a in zip(weights, phases) if a >= 0), F())
                assert load >= weights[i] > 0
                for degree in (0, 1, 2, 5):
                    assert load ** degree > 0
                    zero_faces += 1
            for r in range(1, n + 1):
                for size in range(1, r + 1):
                    for users in combinations(range(n), size):
                        full_load = sum((weights[i] for i in users), F())
                        for degree in (0, 1, 2, 5):
                            heavy = full_load ** degree if 0 in users else F()
                            delta_sum = F()
                            for light in range(1, n):
                                if 0 in users and light in users:
                                    delta_sum += ((weights[0] + weights[light]) ** degree
                                                  - weights[light] ** degree)
                            assert delta_sum <= (r - 1) * heavy
                            columns += 1
    # Both algebraic directions and finite eps witnesses, including beta*r=1.
    witnesses = []
    for m in range(1, 31):
        for r in range(1, m + 3):
            for eps in (F(1, m ** 3), F(1, 1000), F(1), F(2)):
                den = (r - 1) * (1 + m * eps) + m * eps
                bound = m * (1 + eps) / den
                for beta in (F(1), F(3, 2), F(m + 1)):
                    assert (beta >= bound) == (m * (1 + eps) <= beta * den)
                    parameters += 1
                if eps == 1 and r == 2:
                    assert bound == F(2 * m, 2 * m + 1) < 1
            if m > 2 * (r - 1):
                beta = F(2)
                edge = F(m - beta * (r - 1), m * (beta * r - 1))
                eps = edge / 2
                den = (r - 1) * (1 + m * eps) + m * eps
                bound = m * (1 + eps) / den
                assert bound > beta
                assert beta * den < m * (1 + eps)  # reverse multiplication
                witnesses.append([m, r, str(eps), str(bound)])
    print(json.dumps({
        "status": "all exact assertions passed",
        "claim": "WC-APPROXIMATE-SUPPORT-DISTORTION-v1",
        "scope": "Finite column/zero-face and algebra checks; no universal theorem inferred from enumeration.",
        "arithmetic": "fractions.Fraction; exact; no randomness or solver",
        "parameters": {"n": [2, 7], "m": [1, 30], "degrees": [0, 1, 2, 5],
                       "alternate_weights": ["all ones", "(i+1)/(2i+1)"]},
        "column_charge_checks": columns, "zero_face_checks": zero_faces,
        "parameter_checks": parameters, "strict_beta2_witnesses": witnesses,
        "command": "python3 tests/audits/weighted_congestion/template_certificates/verify_approximate_support.py",
        "python": platform.python_version(), "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
