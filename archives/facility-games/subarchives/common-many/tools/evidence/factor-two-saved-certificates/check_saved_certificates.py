"""Check the four frozen certificates, without constructing or enumerating equilibria."""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
from fractions import Fraction as F
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
CHECKER = ROOT.parent / "factor-two-reverse-review" / "definition_check.py"
CHECKER_HASH = "8d67c24a98643b79aa7f4f8d6c8cd1386516d95d3f04aff914b37663129a0cc1"
assert hashlib.sha256(CHECKER.read_bytes()).hexdigest() == CHECKER_HASH
sys.path.insert(0, str(CHECKER.parent))
from definition_check import check_certificate


def examine(cert):
    assert set(cert) == {"schema", "instance", "factor", "on_path", "deviations",
                         "default_rule", "search_audit", "complexity"}
    assert cert["schema"] == "SC-K-2-E/v1" and cert["factor"] == "2"
    assert cert["complexity"] == "exhaustive finite construction; no polynomial-time claim"
    assert cert["default_rule"] == "least-index initial pure assignment, then strict pure best responses"
    instance, onpath = cert["instance"], cert["on_path"]
    k, m = instance["k"], instance["m"]
    clients = instance["clients"]
    weights = [F(c["weight"]) for c in clients]
    layout = onpath["layout"]
    assert set(onpath) == {"layout", "site_assignment", "probabilities"}
    assert len(onpath["site_assignment"]) == len(clients)
    probabilities = [[F(x) for x in row] for row in onpath["probabilities"]]
    for i, t in enumerate(onpath["site_assignment"]):
        occupied_options = set(clients[i]["sites"]) & set(layout)
        assert t in occupied_options if occupied_options else t == -1
        expected = [F(1, layout.count(t)) if s == t else F(0) for s in layout]
        assert probabilities[i] == expected
    base = [sum((w * probabilities[i][f] for i, w in enumerate(weights)), F(0)) for f in range(k)]
    assert set(cert["search_audit"]) == {"site_allocations_evaluated", "lex_key"}
    assert list(map(F, cert["search_audit"]["lex_key"])) == sorted(base)
    assert type(cert["search_audit"]["site_allocations_evaluated"]) is int
    assert cert["search_audit"]["site_allocations_evaluated"] > 0
    # Exactly one on-path NE and all actual deviation NEs are checked here.
    checked = check_certificate(cert, all_layouts=False)
    details = []
    for d in cert["deviations"]:
        assert set(d) == {"facility", "site", "pure_assignment", "audit"}
        f, r, assignment, audit = d["facility"], d["site"], d["pure_assignment"], d["audit"]
        assert set(audit) == {"strict_improvement_steps", "isolated_giants", "final_loads",
                              "deviator", "target_site", "source_multiplicity",
                              "departed_site_disappears", "target_previously_occupied",
                              "on_path_load", "bins_used"}
        final = [sum((w for w, g in zip(weights, assignment) if g == h), F(0)) for h in range(k)]
        assert list(map(F, audit["final_loads"])) == final
        assert audit["deviator"] == f and audit["target_site"] == r
        assert audit["source_multiplicity"] == layout.count(layout[f])
        assert audit["departed_site_disappears"] is (layout.count(layout[f]) == 1)
        assert audit["target_previously_occupied"] is (r in layout)
        assert F(audit["on_path_load"]) == base[f]
        for field in ["strict_improvement_steps", "isolated_giants", "bins_used"]:
            assert type(audit[field]) is int and audit[field] >= 0
        assert audit["bins_used"] <= k - 1
        cap = 2 * base[f]
        giants = [i for i, w in enumerate(weights) if assignment[i] >= 0 and w > cap]
        assert len(giants) == audit["isolated_giants"]
        giant_facilities = {assignment[i] for i in giants}
        assert len(giant_facilities) == len(giants) and f not in giant_facilities
        for i in giants:
            assert assignment.count(assignment[i]) == 1 and final[assignment[i]] == weights[i]
        assert all(L <= cap for h, L in enumerate(final) if h not in giant_facilities)
        static_sites = {s for g, s in enumerate(layout) if g != f}
        orphan_rehang_mass = sum(
            (weights[i] for i, t in enumerate(onpath["site_assignment"])
             if t == layout[f] and audit["departed_site_disappears"]
             and set(clients[i]["sites"]) & static_sites), F(0))
        details.append(dict(facility=f, target=r, independently_checked_NE=True,
                            deviator_load=str(final[f]), on_path_load=str(base[f]),
                            raw_gain_ratio=str(final[f] / base[f]),
                            final_loads_verified=True,
                            isolated_giants_verified=len(giants),
                            ordinary_cap_verified=True,
                            disappearing_source_rehang_mass=str(orphan_rehang_mass),
                            recorded_steps_not_replayed=audit["strict_improvement_steps"],
                            recorded_initial_stationary_bins=audit["bins_used"]))
    return dict(instance=instance, on_path_layout=layout,
                on_path_loads=[str(x) for x in base], checked=checked,
                source_search_candidates_not_recomputed=cert["search_audit"]["site_allocations_evaluated"],
                source_step_total_not_replayed=sum(d["audit"]["strict_improvement_steps"] for d in cert["deviations"]),
                verified_giant_occurrences=sum(d["isolated_giants_verified"] for d in details),
                positive_rehang_deviations=sum(F(d["disappearing_source_rehang_mass"]) > 0 for d in details),
                unlisted_layouts_not_evaluated=m ** k - 1 - k * (m - 1),
                deviations=details)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Refusing to overwrite an existing certificate check report")
    sources = json.loads((ROOT / "certificate_sources.json").read_text())
    rows = []
    for entry in sources["files"]:
        raw = (ROOT / entry["retained_file"]).read_bytes()
        assert len(raw) == entry["size_bytes"] and hashlib.sha256(raw).hexdigest() == entry["sha256"]
        rows.append(dict(source_id=entry["id"], retained_file=entry["retained_file"],
                         sha256=entry["sha256"], **examine(json.loads(raw))))
    assert len(rows) == 4
    result = dict(frozen_commit=sources["frozen_commit"], definition_checker_sha256=CHECKER_HASH,
                  certificates=rows, on_path_NE_checks=4,
                  actual_deviation_NE_checks=sum(len(r["deviations"]) for r in rows),
                  default_continuation_evaluations=0, unlisted_layout_enumerations=0,
                  constructors_executed=0, lexmax_enumerations=0,
                  recorded_step_trajectories_replayed=False,
                  scope="Direct exact conditional-cost certificate verification plus static metadata/cap checks.")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(dict(certificates=4, on_path_NE_checks=4,
                         actual_deviation_NE_checks=result["actual_deviation_NE_checks"],
                         default_continuation_evaluations=0, constructors_executed=0)))


if __name__ == "__main__":
    main()
