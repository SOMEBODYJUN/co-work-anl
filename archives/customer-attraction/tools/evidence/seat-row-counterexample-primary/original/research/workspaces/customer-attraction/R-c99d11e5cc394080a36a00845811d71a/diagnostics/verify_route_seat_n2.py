"""Exact n=2 route-specific seat-row obstruction."""
import json
from fractions import Fraction
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[5]))
from customer_attraction import CustomerType, Instance, StrategyCertificate, verify_certificate
instance = Instance(("B0", "B1"), (CustomerType(frozenset({0}), 2), CustomerType(frozenset({1}), 1)), 2)
cert = StrategyCertificate({(): 1, (0,): 0, (1,): 0}, (1, 1))
check = verify_certificate(instance, cert)
check.assert_valid()
root_path = (1, 0)
root_u = instance.player_payoffs(root_path)[0]
assert root_u == Fraction(1)
assert root_u < Fraction(2)
report = {"status": "exact_pass", "checked_histories": check.checked_histories, "checked_deviations": check.checked_deviations, "root_path": list(root_path), "root_payoff": str(root_u), "route_seat_rhs": "2", "welfare": instance.welfare((1, 1)), "optimum": instance.optimal_welfare()}
Path(__file__).with_suffix(".json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
