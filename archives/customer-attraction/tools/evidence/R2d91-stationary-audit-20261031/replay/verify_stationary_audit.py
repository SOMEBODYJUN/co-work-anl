from pathlib import Path
import hashlib, json

base = Path(__file__).resolve().parent.parent
src = base / "source"
rep = base / "replay"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

expected = {
    "audit_stationary_extra_fractional.json": "dfabbae544977de0513427fe029718dd54398f8e30fbf15355bfc92c67886cd6",
    "audit_stationary_extra_fractional.py": "97cd6a52e771603531d61dab179ee58ad690a57a4912e95c40f097045e45bd23",
    "abandoned_probe_uncovered_budget.py": "346cc864013934ae21ca1585d36682b4cc2195f6307765938b49ae99c5c2e64b",
}
for name, digest in expected.items():
    assert sha(src / name) == digest, (name, sha(src / name))
original = json.loads((src / "audit_stationary_extra_fractional.json").read_text())
generated = json.loads((rep / "generated.json").read_text())
assert original == generated
assert original["unit_customers"] == 1274
assert original["ordered_histories"] == 43
assert original["comparisons_including_self"] == 258
assert original["query_2_minus_root"] == "1149/910"
assert original["uniform_fractional_cap"] == "441/2"
assert original["pure_two_slot_cap"] == "252"
assert "ABANDONED AND NOT RUN" in (src / "abandoned_probe_uncovered_budget.py").read_text()
assert "already has an exact counterexample" in (src / "abandoned_probe_uncovered_budget.py").read_text()
print("PASS")
