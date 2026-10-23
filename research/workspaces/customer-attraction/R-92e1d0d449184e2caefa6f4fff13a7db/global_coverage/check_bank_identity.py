"""Exact implementation audit of README (B), not a proof of half coverage."""
from fractions import Fraction


def main():
    cases = 0
    for m in range(1, 30):
        for c in range(1, m + 1):
            for b in range(c + 1):
                for k in range(m - b + 1):
                    denominator = b + k
                    branch_tail = Fraction(k, denominator) if denominator else Fraction(0)
                    branch_old = Fraction(b, denominator) if denominator else Fraction(0)
                    suffix = Fraction(c - b, c)
                    prefix_loss = Fraction(b, c) - branch_old
                    missing = int(denominator == 0)
                    assert branch_tail == suffix + prefix_loss - missing
                    cases += 1
    print({"status": "PASS", "exact_cases": cases,
           "scope": "scalar bank-share identity only; no general equilibrium bound"})


if __name__ == "__main__":
    main()
