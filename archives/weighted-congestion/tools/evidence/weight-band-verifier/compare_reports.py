"""Compare preserved JSON data; does not import or execute the original audit."""
from pathlib import Path
import hashlib
import json


def differences(old, new, path=""):
    if type(old) is not type(new):
        return [{"path": path, "old": old, "new": new}]
    if isinstance(old, dict):
        result = []
        for key in sorted(old.keys() | new.keys()):
            if key not in old or key not in new:
                result.append({"path": path + "/" + key,
                               "old_present": key in old, "new_present": key in new})
            else:
                result += differences(old[key], new[key], path + "/" + key)
        return result
    if isinstance(old, list):
        if len(old) != len(new):
            return [{"path": path, "old": old, "new": new}]
        return [item for i, (left, right) in enumerate(zip(old, new))
                for item in differences(left, right, path + "/" + str(i))]
    return [] if old == new else [{"path": path, "old": old, "new": new}]


root = Path(__file__).resolve().parent
old = (root / "comparison/frozen-verification.json").read_bytes()
new = (root / "rerun/generated-verification.json").read_bytes()
diff = differences(json.loads(old), json.loads(new))
result = {
    "comparison_only_no_original_audit_execution": True,
    "old_bytes": len(old), "new_bytes": len(new),
    "old_sha256": hashlib.sha256(old).hexdigest(),
    "new_sha256": hashlib.sha256(new).hexdigest(),
    "byte_identical": old == new,
    "full_json_equal": not diff,
    "excluded_fields": [],
    "differences": diff,
}
print(json.dumps(result, indent=2))
if diff or old != new:
    raise SystemExit(1)
