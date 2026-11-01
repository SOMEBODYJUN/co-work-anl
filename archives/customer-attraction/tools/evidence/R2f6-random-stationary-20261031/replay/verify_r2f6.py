from pathlib import Path
import hashlib, json

base = Path(__file__).resolve().parent.parent
src = base / "source"
owner = json.loads((src / "arbitrary_owner_budget_audit.json").read_text())
floor = json.loads((src / "state_floor_blind_audit.json").read_text())
expected_sha = {
    "arbitrary_owner_budget_audit.json": "2ef1eff32e8b152add0ea1b3d45227ed1b4826068632a4374cff78d77951d69c",
    "audit_arbitrary_owner_budget.py": "7dcfaf718d9a22bbcbe3bf0168d359a4ed849a6be682175668efd0acbb179b8d",
    "audit_state_floor_blind.py": "d2890cc366fa982f5bc9ff6c2ae909bd474a99c7c273f6b960dc0ded4aa4b0b4",
    "state_floor_blind_audit.json": "c780550274562c7aa3323819189022a37a2f7a0e362294c460f3e5773ae4cf5a",
}
for name, digest in expected_sha.items():
    got = hashlib.sha256((src / name).read_bytes()).hexdigest()
    assert got == digest, (name, got)
assert json.loads((base / "replay/owner/generated.json").read_text()) == owner
assert json.loads((base / "replay/floor/generated.json").read_text()) == floor
assert owner == {
    "status": "PASS",
    "scope": "single-customer algebra regression; no SPE or half claim",
    "max_m_regression_only": 8,
    "prefix_states": 188302,
    "arbitrary_owner_prefix_budgets": 1793,
    "uniform_owner_fixed_endpoint_states": 510,
    "claims": ["rank bound", "arbitrary fixed owner H_a-1 bound", "prefix-only algebraic sharpness", "uniform owner endpoint F", "uniform owner endpoint error", "symmetric error monotonicity"],
}
assert floor["scope"] == "Exact auxiliary-interface counterexample; profiles are not SPE"
assert floor["customers"] == 10 and floor["players"] == 3
assert floor["root_payoff"] == "3/2" and floor["v4"] == "33/20" and floor["root_gap"] == "3/20"
assert floor["uniform_query_lower_checked_competitor_tuples"] == 1000
assert len(floor["all_rotations"]) == 10
assert all(row["last_deviation_payoff"] == "3" for row in floor["all_rotations"])
assert (base / "replay/owner/stderr.txt").read_bytes() == b""
assert (base / "replay/floor/stderr.txt").read_bytes() == b""
print("PASS")
