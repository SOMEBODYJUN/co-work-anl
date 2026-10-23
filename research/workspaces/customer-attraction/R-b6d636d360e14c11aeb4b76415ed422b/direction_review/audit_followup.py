"""Reproducible direction-review checks, not a new mathematical result.

Replay existing audits in temporary copies so their frozen outputs stay intact.
Independently rebuild the protected-price witness without any game library.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "work.py").is_file())
WORK = ROOT / "research/workspaces/customer-attraction"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def protected_price(k):
    assert k >= 3
    rows = [((0,), 4*k-2), ((0,4,5), 2*k), ((1,), 5*k-2),
            ((1,4,5), 2*k-2), ((1,2,4,5), 1), ((1,3,4,5), 1),
            ((2,), 3*k-1), ((2,4), 2*k-1), ((2,5), 2*k-1),
            ((3,), 3*k-1), ((3,4), 2*k-1), ((3,5), 2*k-1)]
    customers = [frozenset(s) for s,n in rows for _ in range(n)]
    replies = (1,5,4,5,5,4)

    def pay(a, terminal):
        return sum((F(1, sum(t in c for t in terminal))
                    for c in customers if a in c), F(0))

    root_values = [pay(a, (a,replies[a])) for a in range(6)]
    assert root_values == [F(6*k-2)] * 6
    slacks = [root_values[0]-v for v in root_values]
    slacks += [pay(replies[a], (a,replies[a]))-pay(b, (a,b))
               for a in range(6) for b in range(6)]
    assert min(slacks) >= 0
    cov = lambda z: sum(any(t in c for t in z) for c in customers)
    all_pairs = [(p, cov(p)) for p in combinations_with_replacement(range(6), 2)]
    optimum = max(v for _,v in all_pairs)
    assert [p for p,v in all_pairs if v == optimum] == [(2,3)]
    omitted = [c for c in customers if not c.intersection((0,1))]
    a, b = root_values[0], pay(1, (0,1))
    primal = F(len(omitted))-2*a
    marked = {i for t in (2,3)
              for i in [i for i,c in enumerate(omitted) if c == {t}][:k-1]}
    dual = F(len(marked))
    residual = [sum(i not in marked and t in c
                    for i,c in enumerate(omitted)) for t in range(6)]
    assert primal == dual == 2*k-2
    assert max(residual) <= a
    assert primal > b-a
    assert primal-(b-a) == k-2
    assert 2*cov((0,1)) >= optimum
    return {"k": k, "histories": 7, "comparisons": len(slacks),
            "unit_customers": len(customers), "u_A": str(a), "u_B": str(b),
            "price_primal_and_dual": str(primal), "proposed_budget": str(b-a),
            "strict_violation": str(primal-(b-a)),
            "W": cov((0,1)), "OPT": optimum}


def replay_copied_audit(relative, output_name):
    source = WORK / relative
    with tempfile.TemporaryDirectory(prefix="direction-review-", dir=ROOT/".git") as temp:
        target = Path(temp) / source.name
        shutil.copy2(source, target)
        run = subprocess.run([sys.executable, str(target)], cwd=ROOT,
                             capture_output=True, text=True, timeout=90, check=True)
        report = json.loads((Path(temp)/output_name).read_text())
        assert json.loads(run.stdout) == report
    frozen = source.with_name(output_name)
    assert json.loads(frozen.read_text()) == report
    return {"source": source.relative_to(ROOT).as_posix(),
            "source_sha256": digest(source), "matches_frozen_report": True,
            "result": report}


def main():
    product = replay_copied_audit(
        "R-75bfd8f0f91740408bf08f0c9f5e2aa1/dynamic_credit/audit_product_credit.py",
        "product_credit_independent_audit.json")
    iid = replay_copied_audit(
        "R-75bfd8f0f91740408bf08f0c9f5e2aa1/parent/audit_iid_support_hub.py",
        "iid_support_hub_independent_audit.json")
    relay = WORK / "R-12bf6a96d24c48eca828620d6642e203/direct_cover/verify_actual_prefix_obstruction.py"
    certificate = relay.with_name("actual_root_B_certificate.json")
    run = subprocess.run([sys.executable, str(relay)], cwd=ROOT,
                         capture_output=True, text=True, timeout=30, check=True)
    lower = F(product["result"]["obstruction"]["LOW_forced_G_lower"])
    upper = F(product["result"]["obstruction"]["UPPER_forced_G_upper"])
    assert lower-upper == 272 and upper+272 == lower
    assert F(9) < F(3,4)*13
    assert F(3,4)*13-F(9) == F(3,4)
    source_note = WORK / "R-ab183d14fb74403091d09db766b05f73/credible2/protected_excess_price_boundary.md"
    stale_note = WORK / "R-6e3a5707f1f94c1d86bcbc61b4db4345/continuation_induction/prefix_price_induction.md"
    report = {
        "scope": "Direction review: replay existing finite certificates and independently reconstruct a known price witness; no new general half theorem or external review.",
        "review_base_commit": "799b5242c99f1524842ceaf5bbabaf6adc52edb5",
        "product_credit": product, "iid_support": iid,
        "actual_prefix_relay": {"source": relay.relative_to(ROOT).as_posix(),
            "source_sha256": digest(relay), "certificate_sha256": digest(certificate),
            "stdout": run.stdout.strip(), "strict_proportional_gap": "3/4"},
        "protected_price": {"source_note": source_note.relative_to(ROOT).as_posix(),
            "source_sha256": digest(source_note), "stale_note_sha256": digest(stale_note),
            "independent_cases": [protected_price(k) for k in (3,4,7,20)]},
        "all_checks_passed": True}
    HERE.joinpath("followup_verification.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps({"all_checks_passed": True,
                      "report": str(HERE/"followup_verification.json")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
