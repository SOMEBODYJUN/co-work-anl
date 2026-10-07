"""Quick regression entry for the new complete greedy-box constructor.

Run from the repository root: python3 -m tests.test_greedy_box_global.
The larger frozen audit is tests/audits/kfac_greedy_box_global.py.
"""
from tests.audits.kfac_greedy_box_global import run


if __name__ == '__main__':
    report = run(random_cases=12)
    print('PASS: greedy-box full continuation, exact microsteps and H-guard boundary')
