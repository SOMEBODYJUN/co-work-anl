"""Logical-branch and repository-routing regressions for the read-only report."""
import copy
from pathlib import Path
import subprocess
import tempfile
import unittest

import research_frontier as frontier


def obj(oid, truth="open", current=True):
    return {"object_id": oid, "truth_status": truth,
            "binding_status": "current" if current else "requires-refresh",
            "registration_pin": "pin-" + oid, "objections": "Exact obligation " + oid}


def edge(eid, sources, targets, *, kind="implies", mode="unconditional", current=True, partial=False):
    result = {"edge_id": eid, "kind": kind, "status": "accepted",
              "source_ids": sources, "target_ids": targets, "premises_mode": "all",
              "relation_mode": mode, "conditions": "Same model and all stated side conditions",
              "scope": "Exact scope", "explanation": "Complete stated relation",
              "binding_status": "current" if current else "requires-refresh",
              "binding_errors": [] if current else ["changed evidence"],
              "evidence": [{"path": eid + ".md", "sha256": "a" * 64}],
              "declaration_pin": "edge-pin-" + eid, "endpoint_pins": {},
              "evidence_pins": {eid + ".md": "a" * 64}, "review_digest": "review-" + eid}
    if partial:
        result["contribution"] = {"result": "A useful local identity", "remaining": "The global budget is unpaid"}
    else:
        result["whole_result"] = "ALL sources give all targets"
    return result


def context(objects, edges, targets, leads=None):
    options = {target: [] for target in targets}
    by_id = {o["object_id"]: o for o in objects}
    for e in edges:
        directions = [("forward", e["source_ids"], e["target_ids"])]
        if e["kind"] == "equivalent_to":
            directions.append(("reverse", e["target_ids"], e["source_ids"]))
        for direction, premises, conclusions in directions:
            for target in set(conclusions) - set(premises):
                options.setdefault(target, []).append({
                    "edge_id": e["edge_id"], "direction": direction,
                    "all_premises": list(premises), "conclusion_ids": list(conclusions),
                    "conditions": e["conditions"], "scope": e["scope"],
                    "relation_mode": e["relation_mode"], "evidence": e["evidence"],
                    "unpaid_premises": [{"object_id": oid, "truth_status": by_id.get(oid, {}).get("truth_status", "unknown")}
                                        for oid in premises if by_id.get(oid, {}).get("truth_status") not in {"definition", "proved"}],
                    "unknown_endpoints": [], "endpoint_binding_changes": [],
                    "current_declared_support": e["binding_status"] == "current",
                })
    return {"seed_ids": targets, "objects": objects, "edges": edges,
            "support_options": options, "research_leads": leads or [], "refutations": [],
            "registry": "research/registry.json", "registry_pin": "registry-pin"}


class FrontierTests(unittest.TestCase):
    def test_AND_missing_one_premise_preserves_the_full_route(self):
        ctx = context([obj("A", "proved"), obj("B"), obj("C")], [edge("joint", ["A", "B"], ["C"])], ["C"])
        report = frontier.frontier_report(ctx)
        self.assertEqual(report["structural_assuming_conditions_closure"], ["A"])
        self.assertEqual(report["routes"][0]["all_premises"], ["A", "B"])
        self.assertEqual(report["routes"][0]["unresolved_premises_after_structural_closure"][0]["object_id"], "B")
        self.assertEqual(report["registry_pin"], "registry-pin")

    def test_OR_alternative_does_not_require_every_branch(self):
        ctx = context([obj("A", "proved"), obj("B"), obj("C")],
                      [edge("good", ["A"], ["C"]), edge("unpaid", ["B"], ["C"])], ["C"])
        report = frontier.frontier_report(ctx)
        self.assertIn("C", report["structural_assuming_conditions_closure"])
        self.assertEqual(len(report["routes"]), 2)
        self.assertEqual([r["structurally_ready_assuming_conditions"] for r in report["routes"]], [True, False])

    def test_reverse_equivalence_requires_every_target(self):
        ctx = context([obj("A"), obj("B", "proved"), obj("D")],
                      [edge("equiv", ["A"], ["B", "D"], kind="equivalent_to", mode="conditional")], ["A"])
        report = frontier.frontier_report(ctx)
        self.assertNotIn("A", report["structural_assuming_conditions_closure"])
        reverse = next(r for r in report["routes"] if r["direction"] == "reverse")
        self.assertEqual(reverse["all_premises"], ["B", "D"])
        ctx["objects"][2] = obj("D", "proved")
        self.assertIn("A", frontier.frontier_report(ctx)["structural_assuming_conditions_closure"])

    def test_open_equivalence_cycle_never_supplies_its_own_base(self):
        ctx = context([obj("A"), obj("B")], [edge("equiv", ["A"], ["B"], kind="equivalent_to", mode="conditional")], ["A"])
        report = frontier.frontier_report(ctx)
        self.assertEqual(report["structural_assuming_conditions_closure"], [])
        self.assertEqual(report["cyclic_dependency_components"][0]["unresolved_object_ids"], ["A", "B"])
        self.assertFalse(report["cyclic_dependency_components"][0]["self_payment_allowed"])

    def test_partial_contribution_never_pays_whole_even_if_in_support(self):
        partial = edge("step", ["A"], ["C"], partial=True)
        ctx = context([obj("A", "proved"), obj("C")], [partial], ["C"], leads=[partial])
        report = frontier.frontier_report(ctx)
        self.assertNotIn("C", report["structural_assuming_conditions_closure"])
        self.assertFalse(report["contributions"][0]["pays_whole_target"])
        self.assertEqual(report["contributions"][0]["remaining"], "The global budget is unpaid")

    def test_conditional_route_is_structural_only_and_needs_application_review(self):
        ctx = context([obj("A", "proved"), obj("C")], [edge("cond", ["A"], ["C"], mode="conditional")], ["C"])
        original = copy.deepcopy(ctx)
        report = frontier.frontier_report(ctx)
        self.assertIn("C", report["structural_assuming_conditions_closure"])
        self.assertTrue(report["routes"][0]["condition_application_review_required"])
        self.assertEqual(report["routes"][0]["actionable_frontier"][0]["kind"], "condition-application-review")
        self.assertIn("not an actually usable proof", report["closure_assumption"])
        self.assertEqual(ctx, original)

    def test_stale_route_does_not_revoke_independent_base_or_alternative(self):
        ctx = context([obj("A", "proved"), obj("D", "definition"), obj("C")],
                      [edge("stale", ["A"], ["C"], current=False), edge("fresh", ["D"], ["C"])], ["C"])
        report = frontier.frontier_report(ctx)
        self.assertEqual(report["declared_bases"], ["A", "D"])
        self.assertIn("C", report["structural_assuming_conditions_closure"])
        stale = next(r for r in report["routes"] if r["edge_id"] == "stale")
        self.assertFalse(stale["structurally_eligible"])
        self.assertIn("bindings-require-refresh", stale["structural_blockers"])

    def test_legacy_undeclared_whole_scope_requires_review(self):
        legacy = edge("legacy", ["A"], ["C"])
        del legacy["whole_result"]
        report = frontier.frontier_report(context([obj("A", "proved"), obj("C")], [legacy], ["C"]))
        self.assertNotIn("C", report["structural_assuming_conditions_closure"])
        self.assertIn("whole-result-scope-requires-review", report["routes"][0]["structural_blockers"])

    def test_refutation_preserves_precise_target(self):
        ctx = context([obj("P"), obj("bridge")], [], ["P"])
        refutation = edge("no-bridge", ["P"], ["bridge"], kind="refutes")
        ctx["refutations"] = [refutation]
        report = frontier.frontier_report(ctx)
        self.assertEqual(report["refutations"][0]["precise_target_ids"], ["bridge"])
        self.assertNotIn("P", report["structural_assuming_conditions_closure"])

    def test_expected_branch_guards_snapshot_and_records_commit_remote(self):
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as tmp:
            root = Path(tmp)

            def git(*args):
                return subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, text=True).stdout.strip()

            git("init", "-q", "-b", "rebuild/research-v2")
            git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "snapshot", "--allow-empty")
            git("remote", "add", "origin", "https://github.com/example/research.git")
            snapshot = frontier.repository_snapshot(root, "rebuild/research-v2")
            self.assertEqual(snapshot["commit"], git("rev-parse", "HEAD"))
            self.assertEqual(snapshot["remote"], "https://github.com/example/research.git")
            self.assertFalse(snapshot["worktree_dirty"])
            with self.assertRaisesRegex(ValueError, "Expected branch main"):
                frontier.repository_snapshot(root, "main")


if __name__ == "__main__":
    unittest.main()
