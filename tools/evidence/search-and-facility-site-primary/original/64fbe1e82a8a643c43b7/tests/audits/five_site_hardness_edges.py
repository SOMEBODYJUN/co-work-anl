"""Additional exact edge-case regression; no repository-level checks."""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json
import runpy
import time

AUDIT = runpy.run_path(str(Path(__file__).with_name("five_site_hardness.py")))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    start = time.perf_counter()
    specs = [
        ([2], 0, F(3, 2), True),        # empty selected subset
        ([2, 2], 0, F(3, 2), False),   # repeated source values
        ([2, 2], 1, F(3, 2), False),   # NO with repeated values
        ([2, 2], 2, F(3, 2), False),
        ([2, 2], 4, F(3, 2), False),   # total-sum target
        ([2], 1, F(1000001, 1000000), True),
        ([2], 2, F(1000001, 1000000), True),
        ([2], 1, F(161803398874989, 100000000000000), True),
        ([2], 2, F(161803398874989, 100000000000000), True),
    ]
    cases = []
    for numbers, target, a, full in specs:
        row, instance, parameters, certificate = AUDIT["audit_case"](
            numbers, target, a, full)
        if certificate is not None:
            # Test the saved representation, not only the in-memory Fractions.
            restored = json.loads(json.dumps(AUDIT["serial"](certificate)))
            assert AUDIT["verify_complete_certificate"](instance, restored)
        cases.append(row)
    rejected = 0
    for numbers, target in [([], 0), ([0], 0), ([-1], 0),
                            ([2], -1), ([2], 3), ([True], 1)]:
        try:
            AUDIT["reduction"](numbers, target, F(3, 2))
        except ValueError:
            rejected += 1
        else:
            raise AssertionError("invalid source input was accepted")
    result = AUDIT["serial"](dict(
        claim="SC-FIVE-DECa-HARD",
        scope="Additional finite exact regression, not a universal proof.",
        cases=cases, invalid_source_inputs_rejected=rejected,
        all_assertions_passed=True, repository_checks_run=False,
        elapsed_seconds=round(time.perf_counter()-start, 3),
    ))
    with open(args.output, "x", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
        f.write("\n")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
