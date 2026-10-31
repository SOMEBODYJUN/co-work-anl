import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
src = root / "source"
replay = root / "replay"
assert hashlib.sha256((src / "audit_tail_disagreement.py").read_bytes()).hexdigest() == "5261fc42d1cc935746f0580de12df21e57eb9cf97dcdf77fadefdec9f3fb83a8"
assert hashlib.sha256((src / "tail_disagreement_audit.json").read_bytes()).hexdigest() == "b435864e4da03006ea88647f2c285b8752b4b478aaf92da4c07123a78cb142a1"
assert (replay / "audit.stderr.txt").read_bytes() == b""
assert (replay / "audit.stdout.json").read_bytes() == (replay / "tail_disagreement_audit.generated.json").read_bytes()
report = json.loads((src / "tail_disagreement_audit.json").read_text())
stdout = json.loads((replay / "audit.stdout.json").read_text())
assert report == stdout
assert report["claim_status"] == "exact identity and conditional no-go; no half counterexample"
assert report["scalar_checks"] == 972
assert report["triangle_full_spe"]["nodes"] == 13
assert report["triangle_full_spe"]["comparisons"] == 39
assert report["existing_aggregate_theta_full_spe"]["nodes"] == 43
assert report["existing_aggregate_theta_full_spe"]["comparisons"] == 258
assert report["existing_aggregate_theta_full_spe"]["decomposition"] == {"root": "10", "tail_mean": "12", "g_drift": "0", "C": "1/2", "D": "5/2"}
print("PASS")
