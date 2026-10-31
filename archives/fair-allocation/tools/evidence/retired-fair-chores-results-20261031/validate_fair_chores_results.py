#!/usr/bin/env python3
"""Integrity and semantic-shape checks for the three frozen fair_chores result files.

This checks hashes, sizes, and the recorded finite-run fields.  It does not
prove any fairness theorem and it does not rerun the unclaimed scripts.
"""
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).parent
EXPECTED = {
    "construct_rank2_results.json": ("de64d82efac0cbf667e6af8cf3594177a1861acd8657d8d2f9f72c4d112b94b4", 356),
    "mixed_extension_results.json": ("715fc947fd2b4de815d1781aad500d7c17c4d4dd12b742381b996ed06ae319e9", 1803),
    "rank2_cap_results.json": ("e0d37e6b62c3fb25377ed8d3d69d0c1afc0cef95ec195bc106d3f47501f16162", 737),
}

def read(name):
    p = ROOT / name
    b = p.read_bytes()
    sha = hashlib.sha256(b).hexdigest()
    ex_sha, ex_size = EXPECTED[name]
    assert (sha, len(b)) == (ex_sha, ex_size), (name, sha, len(b))
    return json.loads(b)

construct = read("construct_rank2_results.json")
assert construct["lemma"] == "FC-LEMMA-R2-2C-v1"
assert construct["random_n"] == [2,3,4,5,6,7,8]
assert construct["random_m"] == "n-1,n,2n,4n,100"
assert construct["random_trials_per_pair"] == 100
assert construct["total_cases_including_full_cube"] == 3507
assert construct["max_matching_flip_rounds_observed"] == 2
assert "EFX always" in construct["assertions"] and "EF if m>=n" in construct["assertions"]

mixed = read("mixed_extension_results.json")
assert len(mixed) == 4
c3, c4, n6, n5 = mixed
assert c3["graph"] == "cycle" and c3["vertices"] == 3 and c3["exhaustive"] and c3["profiles_checked"] == 729 and c3["no_EFXplus0_witness"] is None
assert c4["graph"] == "cycle" and c4["vertices"] == 4 and c4["exhaustive"] and c4["profiles_checked"] == 6561 and c4["no_EFXplus0_witness"] is None
assert n6["n"] == 6 and n6["completed_trials"] == n6["requested_trials"] == 10000 and n6["counterexample_to_universal_EFXplus0"] is None
assert n5["n"] == 5 and n5["completed_trials"] == 687 < n5["requested_trials"] == 1000
w = n5["counterexample_to_universal_EFXplus0"]
assert w["trial"] == 686 and w["endpoint_utilities"] == [[1,2],[-2,-2],[-2,-2],[-2,0],[-2,-1],[-2,0]]

caps = read("rank2_cap_results.json")
assert len(caps) == 3
assert [(r["n"], r["m"], r["loops"], r["completed_trials"], r["allocations_per_profile"]) for r in caps] == [
    (3,9,False,1000,19683), (3,9,True,1000,19683), (4,8,True,250,65536)
]
assert all(r["rank_cap"] == 2 and r["parallel_classes"] == 3 and r["counterexample"] is None and r["requested_trials"] == r["completed_trials"] for r in caps)

out = {
    "status": "pass",
    "checks": {
        "hashes_and_sizes": True,
        "construct_rank2_shape": True,
        "mixed_extension_shape": True,
        "rank2_cap_shape": True,
    },
    "interpretation": "Integrity/field checks only; finite observations remain finite evidence and are not universal fairness proofs.",
}
(ROOT / "validation.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(out, ensure_ascii=False, indent=2))
