"""Recheck the saved seed regressions and symbolic budget algebra; no search."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import importlib.util
import json
import platform

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "credible_construction/audit_insurance_menu.py"
FROZEN = SOURCE.with_suffix(".json")

def add(*ps):
    out = [F(0)] * max(map(len, ps))
    for p in ps:
        for i, c in enumerate(p):
            out[i] += c
    while len(out) > 1 and not out[-1]:
        out.pop()
    return out

def mul(p, q):
    out = [F(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i+j] += a*b
    return add(out)

def scale(c, p):
    return [F(c)*x for x in p]

def main():
    # Coefficients in m after clearing the positive denominator 2(m-1).
    mm1 = [-1, 1]
    identities = [
        add(scale(2, mul(mm1, [4,-1])), scale(2, mul([-3,2],[-2,1])),
            scale(-2, add(mul(mm1,mm1),[1]))),
        add(scale(2,mul(mm1,mm1)), scale(-1,mul([-3,2],mm1)),scale(-1,mm1)),
        add(scale(2,mul(mm1,[4,-1])),scale(2,mul([-3,1],[-2,1])),[-4]),
        add(scale(2,mul(mm1,mm1)),scale(-1,mul([-3,1],mm1)),scale(-1,mul([1,1],mm1))),
    ]
    assert identities == [[F(0)]]*4
    spec = importlib.util.spec_from_file_location("saved_seed_audit",SOURCE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    cases = [mod.check(4,3,b) for b in (2,4,6)]
    assert cases == json.loads(FROZEN.read_text())["cases"]
    result = {
        "scope": "Regression and formal polynomial identity checks; not a proof of half or independent solver audit",
        "python": platform.python_version(),
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "saved_output_sha256": hashlib.sha256(FROZEN.read_bytes()).hexdigest(),
        "cleared_polynomial_identities": [list(map(str,p)) for p in identities],
        "replayed_cases_equal_saved_output": True,
        "regimes": [case["regime"] for case in cases],
    }
    (HERE / "verification.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))

if __name__ == "__main__":
    main()
