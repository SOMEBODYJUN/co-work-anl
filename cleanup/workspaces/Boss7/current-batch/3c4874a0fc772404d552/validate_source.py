#!/usr/bin/env python3
"""Exact source-level replay for R-373d fixed_bridge_mult3.json."""
from __future__ import annotations
import hashlib, json, sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
DEP = ROOT / "archives/customer-attraction/tools/evidence/R-373d-coupling-credible-20261031/dependencies"
sys.path.insert(0, str(DEP))
sys.path.insert(0, str(DEP / "tests_audits"))
from customer_attraction import StrategyCertificate, verify_certificate
from customer_attraction_strategy_lp import integer_clones, instance_from_clones

source = Path(__file__).with_name("source.json")
data = json.loads(source.read_text())
sha = hashlib.sha256(source.read_bytes()).hexdigest()
if sha != "c3b17b2b8b9e03caafcd3656ddb6904613e1430b5e75f9c3348310e09f283d84":
    raise SystemExit(f"unexpected source sha256: {sha}")
if data["p"] != 6 or data["m"] != 3 or data["mult"] != 3:
    raise SystemExit("unexpected p/m/mult")
if len(data["weights"]) != (1 << data["p"]) - 1:
    raise SystemExit("weights are not indexed by all nonempty provider subsets")
if len(data["strategy"]["actions"]) != 1 + data["p"] + data["p"] ** 2:
    raise SystemExit("strategy does not contain all depth 0,1,2 histories")
if sum(data["strategy"]["terminal_counts"]) != data["m"]:
    raise SystemExit("terminal count does not have m actions")

clones = integer_clones(tuple(Fraction(x) for x in data["weights"]))
instance = instance_from_clones(data["p"], data["m"], clones)
certificate = StrategyCertificate.from_dict(data["strategy"])
verification = verify_certificate(instance, certificate)
verification.assert_valid()
actual_utilities = [str(x) for x in instance.player_payoffs(tuple(data["path"]))]
welfare = instance.welfare(certificate.terminal_counts)
optimum = instance.optimal_welfare()
if list(clones) != data["weights"]:
    raise SystemExit("source weights are not a primitive integer clone vector")
if actual_utilities != data["utilities"] or welfare != data["welfare"] or optimum != data["optimum"]:
    raise SystemExit("source summary fields disagree with exact replay")

result = {
    "source_id": "3c4874a0fc772404d552",
    "source_path": "research/workspaces/customer-attraction/R-373daba10913464c93771a808d88fce3/credible/fixed_bridge_mult3.json",
    "source_sha256": sha,
    "source_size": source.stat().st_size,
    "parameters": {"providers": data["p"], "topics": data["m"], "multiplier": data["mult"]},
    "weights": {"length": len(data["weights"]), "sum": sum(data["weights"]), "nonzero": sum(x != 0 for x in data["weights"])},
    "strategy": {"actions": len(data["strategy"]["actions"]), "histories": {"depth0": 1, "depth1": data["p"], "depth2": data["p"] ** 2}, "terminal_counts": data["strategy"]["terminal_counts"]},
    "exact_replay": {"certificate_valid": True, "histories_checked": verification.checked_histories, "utilities": actual_utilities, "welfare": welfare, "optimum": optimum, "two_welfare_minus_optimum": 2 * welfare - optimum},
    "bridge_screen": {"objective": data["objective"], "portfolio": data["portfolio"], "path": data["path"]},
    "comparison": {"sibling_mult2_source_id": "7cdb308f85a723cb0b0d", "sibling_mult2_objective": "-6/23", "sibling_mult2_welfare": 138, "sibling_mult2_optimum": 198, "existing_object": "archives/customer-attraction/state/障碍/R-373d耦合桥与计数MILP有限证书--障碍.md"},
}
print(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
