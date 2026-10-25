"""A three-player SPE whose proposed two-D prefix is not even terminal BR."""
from pathlib import Path
from fractions import Fraction as F
import sys
import json

ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT))
from customer_attraction import CustomerType, ExactSPESolver, Instance, verify_certificate

HERE = Path(__file__).resolve().parent
inst = Instance(('0', '1', '2', '3'), (
    CustomerType(frozenset({0}), 1),
    CustomerType(frozenset({1, 2}), 2),
    CustomerType(frozenset({3}), 2),
    CustomerType(frozenset({1, 3}), 1),
), 3)
path = (1, 3, 3)
cert = ExactSPESolver(inst).certificate(on_path=path)
check = verify_certificate(inst, cert)
check.assert_valid()
u = inst.player_payoffs(path)
obj = {
    'status': 'counterexample to universal DD padding, not to HALF5',
    'proposed_padding': 'Add D disjoint from every core theme, |D|=2u_1; prepend (D,D).',
    'core_instance': inst.to_dict(),
    'core_certificate': cert.to_dict(),
    'core_path': list(path),
    'core_payoffs': list(map(str, u)),
    'D_size': str(2 * u[0]),
    'integer_realization': 'Multiply every core multiplicity by 3 and use 14 new D-only clients.',
    'last_prescribed_payoff': str(u[-1]),
    'last_D_deviation_payoff': str(2 * u[0] / 3),
    'strict_improvement': str(2 * u[0] / 3 - u[-1]),
    'canonical_core_check': {'valid': check.valid,
                             'decision_histories': check.checked_histories,
                             'nonself_deviations': check.checked_deviations},
}
(HERE / 'generic_padding_failure_exact.json').write_text(json.dumps(obj, indent=2) + '\n')
print(json.dumps({k: v for k, v in obj.items() if k != 'core_certificate'}, indent=2))
