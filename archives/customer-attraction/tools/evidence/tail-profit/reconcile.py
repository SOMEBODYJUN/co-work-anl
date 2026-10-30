#!/usr/bin/env python3
"""Compare preserved exact reports and both symbolic implementations.

This is an implementation reconciliation, not a new independent mathematical
review. Original scripts remain byte-for-byte preserved in source/.
"""
from contextlib import redirect_stdout
from fractions import Fraction
from io import StringIO
from pathlib import Path
import hashlib
import json
import runpy
import sys

BASE = Path(__file__).resolve().parent
NAMES = ('three_remaining_profit', 'three_remaining_independent',
         'four_remaining_profit', 'four_remaining_independent')
META = {'base_commit', 'python_version', 'replay_commands'}

def load_original(name):
    return json.loads((BASE/'original'/('customer_attraction_'+name+'.json')).read_text())

def load_replay(name):
    return json.loads((BASE/'replay'/('customer_attraction_'+name+'.json')).read_text())

def execute(name):
    path = BASE/'source'/('customer_attraction_'+name+'.py')
    old = sys.argv
    try:
        sys.argv = [str(path)]
        with redirect_stdout(StringIO()):
            return runpy.run_path(str(path), run_name='audit_reconciliation')
    finally:
        sys.argv = old

def main():
    reports = {}
    for name in NAMES:
        original, replay = load_original(name), load_replay(name)
        a = {k:v for k,v in original.items() if k not in META}
        b = {k:v for k,v in replay.items() if k not in META}
        assert a == b, name
        path = BASE/'source'/('customer_attraction_'+name+'.py')
        sha = hashlib.sha256(path.read_bytes()).hexdigest()
        assert sha == original['source_sha256'] == replay['source_sha256']
        reports[name] = {'mathematical_report_equal': True, 'source_sha256': sha,
                         'original_base_commit': original['base_commit'],
                         'replay_base_commit': replay['base_commit']}
    three_main, three_ind = execute(NAMES[0]), execute(NAMES[1])
    for key, polynomial in three_ind['states'].items():
        assert tuple(Fraction(x) for x in three_main['coefficients'](*key)) == polynomial[:3]
        assert polynomial[3] == 0
    four_main = execute(NAMES[2])
    four_ind = load_replay(NAMES[3])
    from itertools import product
    for bits in product((0,1), repeat=7):
        key = ''.join(map(str,bits))
        assert four_main['rho_poly'](bits) == tuple(4*x for x in four_ind['scaled_rho_coefficients_3000D4'][key])
    for row in four_ind['pair_comparison_cases']:
        assert four_main['pair_gap_poly'](row['prefix_membership_count'], row['comparison_membership_count']) == tuple(map(Fraction,row['coefficients_3D4'][:4]))
    for row in four_ind['last_comparison_cases']:
        assert four_main['last_gap_poly'](row['prefix_membership_count'], row['comparison_membership_count']) == tuple(map(Fraction,row['coefficients_D4'][:4]))
    report = {'scope':'original-implementation-replay-and-symbolic-reconciliation',
              'new_independent_review_claimed':False,
              'reports':reports, 'three_full_coefficient_vectors_equal':512,
              'four_rho_full_coefficient_vectors_equal_after_scale_four':128,
              'four_pair_full_coefficient_vectors_equal':15,
              'four_last_full_coefficient_vectors_equal':20,
              'all_checks_passed':True,
              'replay_commands':[
                  'python3 archives/customer-attraction/tools/evidence/tail-profit/source/customer_attraction_'+name+'.py'
                  for name in NAMES]}
    destination = BASE/'replay/reconciliation.json'
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__=='__main__':
    main()
