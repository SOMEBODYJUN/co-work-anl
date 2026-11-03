"""Construct one exact full-history HALF5-irrelevant terminal-share obstruction.

The canonical solver is used only to produce a strategy.  The companion
audit reads the frozen strategy without importing the solver or game model.
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT))
from customer_attraction import CustomerType, ExactSPESolver, Instance, verify_certificate

HERE = Path(__file__).resolve().parent
inst = Instance(tuple(map(str, range(5))), (
    CustomerType(frozenset({0}), 1),
    CustomerType(frozenset({1}), 1),
    CustomerType(frozenset({1, 2}), 1),
    CustomerType(frozenset({0, 3}), 1),
    CustomerType(frozenset({2, 3}), 3),
    CustomerType(frozenset({4}), 3),
), 5)
path = (4, 4, 0, 1, 3)
sol = ExactSPESolver(inst)
cert = sol.certificate(on_path=path)
check = verify_certificate(inst, cert)
check.assert_valid()
obj = {
    'status': 'exact full-history SPE counterexample to C2 only; HALF5 unaffected',
    'candidate': '2 W >= 6 u_5',
    'instance': inst.to_dict(),
    'path': list(path),
    'payoffs': list(map(str, inst.player_payoffs(path))),
    'welfare': inst.welfare(inst.counts(path)),
    'optimum': inst.optimal_welfare(),
    'candidate_violation': str(6 * inst.player_payoffs(path)[-1]
                               - 2 * inst.welfare(inst.counts(path))),
    'canonical_check': {
        'checked_histories': check.checked_histories,
        'checked_deviations': check.checked_deviations,
        'valid': check.valid,
    },
    'certificate': cert.to_dict(),
}
dest = HERE / 'terminal_share_padding_exact.json'
dest.write_text(json.dumps(obj, indent=2) + '\n')
print(json.dumps({k: v for k, v in obj.items() if k != 'certificate'}, indent=2))
