"""Small distinct original-API cases; no stored R70 point or LP is rerun."""
import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import time

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
assert not args.output.exists(), 'one event only'
spec=importlib.util.spec_from_file_location('frozen_r70_spe_dp', args.source)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
records=[]
clock=time.monotonic()
for name,weights,players,root_outcomes in [
    ('zero_clients', [0,0,0,0], 2, 3),
    ('duplicate_coverage_and_empty_topic', [0,0,0,1,0,0,0,0], 2, 3),
]:
    r=module.solve(weights,players=players,witness=True)
    strategy=r.pop('strategy')
    verified=module.verify_result(weights,strategy,players=players)
    assert r['root_outcomes']==root_outcomes
    assert verified['W']==verified['OPT']==(0 if name=='zero_clients' else 1)
    assert verified['worst_slack']==0
    records.append(dict(case=name,weights=weights,players=players,
                        solve=r,strategy=[dict(history=list(h),action=a) for h,a in strategy.items()],
                        verify=verified))

# A one-player legal integer input: binary64 erases the strict gain of one client.
weights=[0,2**53,2**53+1,0]
r=module.solve(weights,players=1,witness=True)
strategy=r.pop('strategy')
assert strategy=={():0} and r['root_outcomes']==2
try:
    module.verify_result(weights,strategy,players=1)
except AssertionError as error:
    rejection=error.args[0]
    assert rejection==((),1,Fraction(-1))
else:
    raise AssertionError('Expected exact rejection of float-selected action0')
exact_legal=module.verify_result(weights,{():1},players=1)
assert exact_legal['W']==exact_legal['OPT']==2**53+1
records.append(dict(case='binary64_equalizes_two_distinct_integer_values',weights=weights,players=1,
                    solve=r,strategy=[dict(history=[],action=0)],
                    exact_rejection=dict(history=[],alternative=1,slack=str(rejection[2])),
                    legal_alternative_action1_verification=exact_legal))
report=dict(status='PASS_SMALL_ORIGINAL_API_ACCEPTANCE_AND_EXACT_REJECTION',
            source_sha256=hashlib.sha256(args.source.read_bytes()).hexdigest(),
            python=platform.python_version(),numpy=module.np.__version__,
            elapsed_seconds=time.monotonic()-clock,
            original_solve_calls=3,original_reconstruct_calls=3,original_verify_result_calls=4,
            original_verify_successes=3,original_verify_expected_rejections=1,
            original_terminal_data_calls_inside_solve=3,LP_calls=0,
            stored_random_or_LP_points_rerun=False,
            scope='Three explicit small input games; original APIs unmodified. Large integers show float screening is not exact; verify rejects invalid reconstructed strategy and accepts exact legal one. No all-domain algorithm certification.',
            cases=records)
def encode(x):
    if isinstance(x,Fraction):return str(x)
    if hasattr(x,'item'):return x.item()
    raise TypeError(type(x).__name__)
args.output.write_text(json.dumps(report,indent=2,default=encode)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='cases'},indent=2))
