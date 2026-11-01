"""One additional definition-level audit of the observed finite-search minimizer."""
from independent_client_audit import HERE, audit_one
import json
import time

started = time.time()
row = audit_one((6, 4, 0, 7, 4, 3))
assert row['threshold_times_12'] == 84
assert row['target_profit_times_12'] == 72
assert row['target_D1_D2_tail_supported']
assert not row['target_C_D1_D2_path_supported']
out = {
    'status': 'PASS',
    'scope': 'one observed minimizing parameter tuple; not a second full search',
    'original_or_canonical_calls': 0,
    'elapsed_seconds': time.time()-started,
    'case': row,
    'guaranteed_profitable_root_actions': [c['root_action'] for c in row['children']
                                          if c['root_min_times_12'] > 72],
}
(HERE/'minimum-supported-tail-case.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps({k: v for k, v in out.items() if k != 'case'}))
