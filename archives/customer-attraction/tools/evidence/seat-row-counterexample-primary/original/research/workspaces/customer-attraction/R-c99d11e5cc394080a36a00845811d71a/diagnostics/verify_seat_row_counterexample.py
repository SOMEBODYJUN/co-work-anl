"""Exact definition-level SPE and invalid-seat-row check."""
import json
from fractions import Fraction
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[5]))
from customer_attraction import Instance, StrategyCertificate, verify_certificate

ROOT = Path(__file__).resolve().parents[1]
obj = json.loads((ROOT / "seat_row_counterexample_certificate.json").read_text())
instance = Instance.from_dict(obj["instance"])
cert = StrategyCertificate.from_dict(obj["certificate"])
check = verify_certificate(instance, cert)
check.assert_valid()
# At root all six B0 providers share the six B0-private customers.
root_u = instance.player_payoffs((0, 0, 0, 0, 0, 0))[0]
assert root_u == Fraction(1)
seat_k1 = Fraction(6, 1)  # six singleton-incidence customers, h=0, k=1
assert root_u < seat_k1
report = {
    "status": "exact_pass",
    "checked_histories": check.checked_histories,
    "checked_deviations": check.checked_deviations,
    "root_payoff": str(root_u),
    "invalid_seat_row_k1_rhs": str(seat_k1),
    "welfare": instance.welfare(cert.terminal_counts),
    "optimum": instance.optimal_welfare(),
}
(Path(__file__).with_suffix(".json")).write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
