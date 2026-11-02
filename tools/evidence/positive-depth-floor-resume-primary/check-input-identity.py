"""Data-only integrity and identity check; does not run an IC/LP/SPE oracle."""
from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
from itertools import product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def distinct_keys(pairs):
    result = {}
    for key, value in pairs:
        assert key not in result, ("duplicate JSON key", key)
        result[key] = value
    return result


def load_file(path):
    return json.loads(path.read_text(), object_pairs_hook=distinct_keys)


def no_float(value):
    assert not isinstance(value, float)
    if isinstance(value, dict):
        for child in value.values():
            no_float(child)
    elif isinstance(value, list):
        for child in value:
            no_float(child)


primary = load_file(HERE / "primary-source-manifest.json")
related = load_file(HERE / "comparison-source-manifest.json")
loaded = {}
for entry in primary + related:
    path = ROOT / entry["preserved_path"]
    blob = path.read_bytes()
    assert len(blob) == entry["size"]
    assert sha256(blob).hexdigest() == entry["sha256"]
    if path.suffix == ".json":
        value = load_file(path)
        no_float(value)
        loaded[entry.get("role", entry["id"])] = value

game = loaded["d250ec1aefa9ac03e914"]
cert = loaded["e0c5edd8647cbfbf42c0"]
canonical_game = loaded["canonical_game"]
canonical_strategy = loaded["canonical_strategy"]
canonical_security = loaded["canonical_security"]
literal = loaded["literal_certificate"]
assert set(game) == {"players", "topics", "customers"}
assert type(game["players"]) is int and game["players"] == 4
assert game["topics"] == ["X0", "X1", "X2", "Y0", "Y1", "Y2", "B"]
for bucket in game["customers"]:
    assert set(bucket) == {"topics", "multiplicity"}
    assert type(bucket["multiplicity"]) is int and bucket["multiplicity"] > 0
    assert bucket["topics"] and len(set(bucket["topics"])) == len(bucket["topics"])
    assert all(type(a) is int and 0 <= a < 7 for a in bucket["topics"])
assert sum(bucket["multiplicity"] for bucket in game["customers"]) == 53
assert set(cert) == {"scope", "strategy", "security"}
assert set(cert["strategy"]) == {"actions", "terminal_counts"}
assert set(cert["security"]) == {"value", "primary", "dual"}
rows = cert["strategy"]["actions"]
expected = [h for depth in range(4) for h in product(range(7), repeat=depth)]
for row in rows:
    assert set(row) == {"history", "action"}
    assert all(type(a) is int and 0 <= a < 7 for a in row["history"])
    assert type(row["action"]) is int and 0 <= row["action"] < 7
assert [tuple(row["history"]) for row in rows] == expected
assert all(type(c) is int and c >= 0 for c in cert["strategy"]["terminal_counts"])
assert len(cert["strategy"]["terminal_counts"]) == 7
assert sum(cert["strategy"]["terminal_counts"]) == 4
for row in cert["security"]["dual"]:
    assert set(row) == {"rivals", "probability"}
    assert all(type(a) is int and 0 <= a < 7 for a in row["rivals"])
    assert len(row["rivals"]) == 3
    assert type(row["probability"]) is str
assert all(type(s) is str for s in cert["security"]["primary"])
assert type(cert["security"]["value"]) is str

# Complete parsed strategy object, not merely the actual leaf, is identical.
assert cert["strategy"] == canonical_strategy
cg = deepcopy(canonical_game)
cg["topics"][-1] = "B"
assert cg == game
security = cert["security"]
assert Fraction(security["value"]) == Fraction(canonical_security["value"])
assert list(map(Fraction, security["primary"])) == list(map(Fraction, canonical_security["primary"]))
assert [(r["rivals"], Fraction(r["probability"])) for r in security["dual"]] == [
    (r["rivals"], Fraction(r["probability"])) for r in canonical_security["dual"]
]
literal_copy = deepcopy(literal)
note = literal_copy.pop("construction_note")
literal_rows = literal_copy["strategy"].pop("actions")
base_copy = deepcopy(cert)
base_copy["strategy"].pop("actions")
assert literal_copy == base_copy
assert [tuple(r["history"]) for r in literal_rows] == expected
policy = {tuple(r["history"]): r["action"] for r in rows}
literal_policy = {tuple(r["history"]): r["action"] for r in literal_rows}
differences = [
    {"history": list(h), "original_action": policy[h], "literal_action": literal_policy[h]}
    for h in expected if policy[h] != literal_policy[h]
]
assert len(differences) == 14
assert all(len(row["history"]) == 3 and row["history"][0] == 6
           and 6 not in row["history"][1:] for row in differences)

# Reversible all-action display, with every other original field preserved.
view = ["depth0 root => " + str(policy[()])]
rebuilt = [{"history": [], "action": policy[()]}]
for depth in range(1, 4):
    view.append("DEPTH " + str(depth))
    for prefix in product(range(7), repeat=depth - 1):
        actions = "".join(str(policy[prefix + (a,)]) for a in range(7))
        view.append(("".join(map(str, prefix)) or "_") + " => " + actions)
        rebuilt.extend({"history": list(prefix + (a,)), "action": int(value)}
                       for a, value in enumerate(actions))
assert rebuilt == rows
reading = HERE / "reading"
reading.mkdir(exist_ok=True)
(reading / "all400-actions.txt").write_text("\n".join(view) + "\n")
nonactions = deepcopy(cert)
nonactions["strategy"].pop("actions")
(reading / "all-non-action-fields.json").write_text(json.dumps(nonactions, ensure_ascii=False, indent=2) + "\n")
reconstructed = deepcopy(nonactions)
reconstructed["strategy"]["actions"] = rebuilt
assert reconstructed == cert
result = {
    "status": "PASS",
    "scope": "Byte identity, complete JSON fields and all400-action mapping only; not a new IC/static-value replay",
    "json_duplicate_keys": 0,
    "json_float_values": 0,
    "policy_rows": len(rows),
    "history_depth_counts": [sum(len(h) == d for h in policy) for d in range(4)],
    "original_row_order": "depth then lexicographic labels",
    "complete_parsed_strategy_equals_canonical": True,
    "game_equals_canonical_after_last_display_label_P_to_B": True,
    "security_equals_canonical_as_exact_rationals": True,
    "literal_other_fields_equal_after_construction_note_removed": True,
    "literal_construction_note": note,
    "literal_action_differences": differences,
    "reversible_action_and_nonaction_view_equals_original_json": True,
    "old_report_field_count": len(loaded["ee9f26f5886df39992b4"]),
}
(HERE / "input-identity.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(result, ensure_ascii=False, indent=2))
