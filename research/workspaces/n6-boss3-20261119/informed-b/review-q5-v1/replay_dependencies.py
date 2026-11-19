"""Read and exactly replay the two registered, frozen antecedents without writing to them."""
from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec,spec_from_file_location
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/"work.py").is_file())
which=sys.argv[1]
assert which in ("B","C")
reg=json.loads((ROOT/"research/registry.json").read_text())
record=next(o for o in reg["objects"] if o["object_id"]==f"CA-SIX-DISJOINT-MAXIMA-FIVE-EXTRAS-{which}-PREFIX-v1")
assert record["truth_status"]=="proved" and record["version"]==1
pins={r["path"]:r["sha256"] for r in [record["body"],*record["evidence"]]}
for path,digest in pins.items():
    assert sha256((ROOT/path).read_bytes()).hexdigest()==digest
home=ROOT/f"tools/evidence/six-five-extra-{which}-prefix"
src=home/f"verify_{which}_all_orbits.py"
spec=spec_from_file_location("formal_"+which,src)
module=module_from_spec(spec)
spec.loader.exec_module(module)
live=module.verify()
expected=home/f"{which}-all-orbit-exact-replay.json"
assert (json.dumps(live,indent=2)+"\n").encode()==expected.read_bytes()
assert Fraction(live["minimum_dual_bound"]) == {"B":Fraction(325,632),"C":Fraction(1001,1896)}[which]
out={"object_id":record["object_id"],"bound_applied_in_new_proof":"1/2",
     "all_registry_evidence_hashes_checked":pins,"canonical_replay_byte_identical":True,
     "canonical_replay_sha256":sha256(expected.read_bytes()).hexdigest(),
     "exact_replay_summary":{k:v for k,v in live.items() if k!="summaries"}}
(HERE/f"replayed-{which}.json").write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n")
print(which,live["orbits"],live["minimum_dual_bound"])
