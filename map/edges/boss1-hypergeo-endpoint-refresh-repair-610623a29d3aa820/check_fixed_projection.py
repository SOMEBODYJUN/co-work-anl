"""Exact, bounded P7 refresh check; writes only a sibling report.

Run from the repository root. No old executable is imported or run; no LP,
5484-row reconstruction, game construction, or full-domain oracle is invoked.
"""
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
from pathlib import Path
import json

ROOT = Path.cwd()
OUT = Path(__file__).resolve().parent
TASK = "boss1-hypergeo-endpoint-refresh-repair-610623a29d3aa820"
PREVIOUS = "boss6-query-sum-repair-repair-4d00534e13bf89ba"
P7 = "M-049f49c6150f4a8b969b1b33c33523ac"
OLD_EDGE = "map/edges/customer-attraction-3a-3a-56e27e52f43a3848/p7-excludes-5484-source-point.json"
SOURCE = "archives/customer-attraction/tools/evidence/weighted-source-contracts-resumed-boss3/original/research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round8_five/certificate/exact_weighted_source.json"
PROJECTION = "archives/customer-attraction/tools/evidence/weighted-source-contracts-resumed-boss3/comparison/research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round8_five/certificate/exact_trueH_projection.json"
AUDIT = "archives/customer-attraction/tools/evidence/five-root-parent-audits-primary/source-root/research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round8_five/root/audit_trueH_seven_rows.json"


def read(path):
    return json.loads((ROOT / path).read_text())


def pin(record):
    return sha256(json.dumps(record, ensure_ascii=False, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def ref(path):
    return {"path": path, "sha256": sha256((ROOT / path).read_bytes()).hexdigest()}


task = read(f"research/operations/map-v2/tasks/{TASK}.json")["definition"]
previous = read(f"research/operations/map-v2/tasks/{PREVIOUS}.json")["definition"]
receipt = read(f"map/receipts/{PREVIOUS}.json")
objects = {o["object_id"]: o for o in read("research/registry.json")["objects"]}
assert all(pin(objects[oid]) == value for oid, value in task["input_pins"].items())
changed = [oid for oid, value in previous["input_pins"].items()
           if task["input_pins"][oid] != value]
assert changed == [P7]
original = next(o for o in read("research/registration/batches/register-ab98f323ad-0032.json")["objects"]
                if o["object_id"] == P7)
changed_fields = [k for k in original if original[k] != objects[P7][k]]
assert changed_fields == ["version", "evidence"]
old_evidence = original["evidence"]
new_evidence = objects[P7]["evidence"]
assert len(old_evidence) == len(new_evidence)
changed_refs = [(a, b) for a, b in zip(old_evidence, new_evidence) if a != b]
assert len(changed_refs) == 1
assert changed_refs[0][0]["path"] == changed_refs[0][1]["path"]
assert changed_refs[0][0]["section"] == changed_refs[0][1]["section"]

asset_checks = []
for asset in receipt["assets"]:
    assert ref(asset["path"]) == asset
    edge = read(asset["path"])
    mismatches = [oid for oid, p in edge["endpoint_pins"].items()
                  if pin(objects[oid]) != p]
    assert mismatches == ([P7] if asset["path"] == OLD_EDGE else [])
    for evidence in edge["evidence"]:
        assert ref(evidence["path"])["sha256"] == evidence["sha256"]
    assert edge["premises_mode"] == "all"
    asset_checks.append({**asset, "edge_id": edge["edge_id"],
                         "changed_endpoints": mismatches,
                         "disposition": "replaced" if mismatches else "retained"})

table = [[Q(v) for v in row] for row in
         ((0, 960, 1220, 1480, 1740, 2000),
          (0, "1665/4", "2745/4", "3785/4", "4825/4", "5865/4"),
          (0, 320, 524, 728, 932, 1136))]


def hidden(p, d, h, q, r):
    total = p + h + q + r
    share = lambda a: Q(a, total) if a else Q(0)
    vh, vq, vr = map(share, (h, q, r))
    b = p + h
    return (-17040 * vh + 9000 * Q(h - q, p + 3)
            + 10080 * Q(h - r, p + 3)
            + 600 * (5 * vr - Q(d, p + h + q + 1)) - 1085 * h
            + 360 * (5 * (vq + vr + Q(q, (b + 1) * (b + 2)))
                     - Q(5 * r + d - 2 * r * d, b + 1)
                     - Q(2 * r * d, b + 2)) + 2679 * Q(5 * h, p + 3))


residues = []
maxima = {}
for p, d in product(range(3), range(6)):
    vals = []
    for state in product((0, 1), repeat=3):
        g = hidden(p, d, *state)
        residue = -table[p][d] - g
        assert residue >= 0
        vals.append(g)
        residues.append({"p": p, "d": d, "hidden": list(state), "residue": str(residue)})
    maxima[p, d] = max(vals)
    assert maxima[p, d] == -table[p][d]
audit = read(AUDIT)
assert residues == audit["residues"]
assert [[str(v) for v in row] for row in table] == audit["F"]

source, projection = read(SOURCE), read(PROJECTION)
assert source["source_sha256"] == projection["source_sha256"]
assert len(source["atoms"]) == 64 and len(projection["projected_atoms"]) == 55
weights = tuple(map(Q, projection["exact_nonnegative_row_multipliers"].values()))
assert tuple(w * 40844 for w in weights) == (17040, 9000, 10080, 600, 1085, 360, 2679)
assert sum(weights) == 1
states_ab = list(product((0, 1), repeat=3))
states_s = list(product((0, 1), repeat=4))


def key(atom):
    return json.dumps({k: v for k, v in atom.items() if k not in {"H_bit", "exact_mass"}},
                      sort_keys=True, separators=(",", ":"))


def counts(atom):
    da = sum(n * s[0] for n, s in zip(atom["AB_hist"], states_ab))
    de = sum(n * s[0] for n, s in zip(atom["AE_hist"], states_ab))
    ds = sum(n * s[0] for n, s in zip(atom["second_hist"], states_s))
    assert da == de == ds
    assert sum(atom["AB_hist"]) == sum(atom["AE_hist"]) == sum(atom["second_hist"]) == 5
    j = sum(n * s[3] for n, s in zip(atom["second_hist"], states_s))
    return da, j


grouped = defaultdict(Q)
welfare, coverage = Q(0), Q(0)
for atom in source["atoms"]:
    mass = Q(atom["exact_mass"])
    assert mass > 0
    grouped[key(atom)] += mass
    d, _ = counts(atom)
    welfare += mass * int("1" in atom["bits"][:5])
    coverage += mass * int(d > 0)
assert len(grouped) == 55
assert welfare == 1 and coverage > 2
assert coverage == Q("200041434567641869132724720689474222359301995810509781/99438097246361783714692320494742010504191176408217548")
assert sum(a["H_bit"] == 0 for a in source["atoms"]) == 43
assert sum(a["H_bit"] == 1 for a in source["atoms"]) == 21

total = Q(0)
inner_outer_differ = []
rows = []
seen = set()
for i, row in enumerate(projection["projected_atoms"]):
    atom = row["atom"]
    atom_key = key(atom)
    assert atom_key not in seen
    seen.add(atom_key)
    mass = Q(row["exact_mass"])
    assert grouped[atom_key] == mass
    if Q(atom["exact_mass"]) != mass:
        inner_outer_differ.append(i)
    maxbits = tuple(map(int, atom["max_bits"]))
    p, u = sum(maxbits[:2]), Q(maxbits[2], sum(maxbits)) if maxbits[2] else Q(0)
    d, j = counts(atom)
    common = 17040 * u + 1085 * maxbits[0] - 2679 * Q(j, p + 3)
    coefficient = (common + maxima[p, d]) / 40844
    assert coefficient == Q(row["coefficient"])
    assert hidden(p, d, *row["maximizing_state"]) == maxima[p, d]
    total += mass * coefficient
    rows.append({"index": i, "p": p, "d": d, "j": j, "u": str(u),
                 "mass": str(mass), "coefficient": str(coefficient)})
assert seen == set(grouped)
assert inner_outer_differ == [0, 15, 16, 17, 19, 23, 24, 42, 51]
assert total == Q(projection["exact_projection_slack"]) < 0
report = {"status": "PASS", "task_id": TASK, "changed_input_ids": changed,
          "changed_registration_fields": changed_fields,
          "changed_registration_evidence": [{"old": a, "current": b} for a, b in changed_refs],
          "source_refs": [ref(p) for p in (SOURCE, PROJECTION, AUDIT)],
          "asset_dispositions": asset_checks, "hidden_states": len(residues),
          "F": [[str(v) for v in row] for row in table],
          "all_144_residues_equal_frozen_audit": True,
          "source_atoms": 64, "merged_atoms": 55,
          "inner_outer_mass_discrepancies": inner_outer_differ,
          "all_55_coefficients_and_witness_states_match": True,
          "W": str(welfare), "O": str(coverage), "projection_slack": str(total),
          "projection_rows": rows,
          "not_executed": ["5484-row source recovery", "747-row LP", "game/SPE construction", "global pricing"],
          "limitation": "Only the specified fixed source and its fixed-mass HQR lift; no universal welfare bound."}
path = OUT / "fixed-projection-check.json"
path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({k: report[k] for k in ("status", "changed_input_ids", "hidden_states", "source_atoms", "merged_atoms", "W", "O", "projection_slack")}, ensure_ascii=False))
