"""Regression checks for mathematical admission, preservation and deletion routes."""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import curation


class CurationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=ROOT / "tests", prefix="curation-fixture-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.git("init", "--quiet")
        self.git("config", "user.name", "Curation fixture")
        self.git("config", "user.email", "curation@example.invalid")
        self.a = self.note("A")
        self.m = self.note("Metadata", kind="metadata", tag="资料", body="actor and UUID only")
        self.commit()

    def git(self, *args):
        result = subprocess.run(["git", *args], cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def commit(self):
        self.git("add", ".")
        self.git("commit", "--quiet", "-m", "fixed original mathematical notes")

    def note(self, name, kind="theorem", tag="定理", body="For real x, x squared is nonnegative."):
        path = f"archives/demo/state/{tag}/{name}--{tag}.md"
        p = self.root / path; p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("---\n" + "\n".join([
            f'id: "demo/{name}"', f'kind: "{kind}"', f'type_tag: "{tag}"',
            f'title: "{name}"', 'status: "complete"', 'summary: "exact scope in body"',
            'source_refs:', '  - "source:' + 'a'*40 + ':raw/source.md"',
        ]) + "\n---\n\n" + body + "\n")
        return path

    def freeze(self):
        curation.freeze(self.root, manifest_out=curation.DEFAULT_MANIFEST)
        self.manifest = json.loads((self.root / curation.DEFAULT_MANIFEST).read_text())
        self.baseline = {r["path"]: r for r in json.loads((self.root / curation.DEFAULT_BASELINE).read_text())["files"]}

    def save(self):
        (self.root / curation.DEFAULT_MANIFEST).write_text(json.dumps(self.manifest))

    def obj(self, name, nid=None, status="proved"):
        p = self.root / name
        return {"path": name, "sha256": curation.digest(p.read_bytes()), "role": "mathematics",
                "object_id": nid or ("demo/" + p.name.split("--")[0]),
                "statement": "For every real x, x squared is nonnegative.",
                "conditions": "x is a real number", "support": "nonnegative product by ordered-field axioms",
                "use": "bound quadratic terms", "status": status, "dependency_scope": "single-object"}

    def decision(self, path, action, targets=(), **extra):
        record = {"path": path, "sha256": self.baseline[path]["sha256"], "action": action,
                  "targets": list(targets), "reason": "Exact content compared with the declared target."}
        record.update(extra)
        self.manifest["decisions"] = [d for d in self.manifest["decisions"] if d["path"] != path] + [record]

    def retain_a_delete_metadata(self):
        self.manifest["objects"] = [self.obj(self.a)]
        self.decision(self.a, "keep", [self.a])
        self.decision(self.m, "delete", delete_kind="non-mathematical")

    def check(self, final=False):
        self.save()
        return curation.check(self.root, final=final)

    def error_contains(self, report, phrase):
        self.assertTrue(any(phrase in e["error"] for e in report["errors"]), report)

    def test_formal_scope_excludes_evidence_and_workspaces(self):
        for name in [
            "archives/demo/tools/evidence/comparison/archives/demo/state/定理/copy--定理.md",
            "archives/demo/workspaces/A/state/定理/copy--定理.md",
            "cleanup/workspaces/state/定理/copy--定理.md",
        ]:
            p = self.root/name; p.parent.mkdir(parents=True,exist_ok=True);p.write_text("copy")
        child="archives/demo/subarchives/child/state/引理/C--引理.md"
        p=self.root/child;p.parent.mkdir(parents=True);p.write_text("candidate")
        self.assertEqual({p.relative_to(self.root).as_posix() for p in curation.formal_paths(self.root)}, {self.a,self.m,child})

    def test_freeze_protects_uncommitted_original_changes(self):
        (self.root/self.a).write_text("lost original proof")
        with self.assertRaisesRegex(ValueError,"pinned Git bytes"):
            self.freeze()
        self.assertFalse((self.root/curation.DEFAULT_BASELINE).exists())

    def test_freeze_rejects_prior_unrecorded_deletion(self):
        (self.root/self.a).unlink()
        with self.assertRaisesRegex(ValueError,"every formal file"):
            self.freeze()

    def test_freeze_never_overwrites_baseline(self):
        self.freeze(); original=(self.root/curation.DEFAULT_BASELINE).read_bytes()
        with self.assertRaisesRegex(ValueError,"already exists"):
            curation.freeze(self.root)
        self.assertEqual((self.root/curation.DEFAULT_BASELINE).read_bytes(),original)

    def test_pending_is_explicit_and_not_final(self):
        self.freeze(); self.assertFalse(self.check()["errors"])
        self.assertEqual(len(self.check()["pending"]),2)
        self.error_contains(self.check(final=True),"cannot leave original unreviewed")
        self.assertEqual(curation.admitted_paths(self.root),())

    def test_missing_manifest_has_no_implicit_admission(self):
        with self.assertRaisesRegex(ValueError,"no automatic mathematical admission"):
            curation.admitted_paths(self.root)

    def test_keep_retains_good_mathematical_bytes(self):
        self.freeze();self.retain_a_delete_metadata();(self.root/self.m).unlink()
        self.assertFalse(self.check(final=True)["errors"])
        self.assertEqual(curation.admitted_paths(self.root,final=True),(self.root/self.a,))

    def test_stale_original_declaration_is_rejected(self):
        self.freeze();self.retain_a_delete_metadata()
        self.manifest["decisions"][0]["sha256"]="b"*64
        self.error_contains(self.check(),"stale decision")

    def test_changed_admitted_body_expires_admission(self):
        self.freeze();self.retain_a_delete_metadata();self.save()
        with (self.root/self.a).open("a") as f:f.write("changed quantifier\n")
        self.error_contains(curation.check(self.root),"SHA changed")

    def test_keep_cannot_be_used_for_rewritten_original(self):
        self.freeze();self.retain_a_delete_metadata()
        with (self.root/self.a).open("a") as f:f.write("new header or proof\n")
        self.manifest["objects"][0]=self.obj(self.a)
        self.error_contains(self.check(),"keep changed original")

    def test_undecided_original_cannot_disappear(self):
        self.freeze();(self.root/self.m).unlink()
        self.error_contains(self.check(),"unreviewed original was removed")

    def test_metadata_cannot_be_admitted_by_filling_generic_fields(self):
        self.freeze();self.manifest["objects"]=[self.obj(self.m)]
        self.decision(self.m,"keep",[self.m])
        self.error_contains(self.check(),"metadata is not a mathematical node")

    def test_definition_and_gap_do_not_need_a_proof_claim(self):
        self.freeze();self.retain_a_delete_metadata()
        self.manifest["objects"][0].update(status="gap",support="Missing uniform bound over all histories; no proof is claimed.")
        self.assertFalse(self.check()["errors"])

    def test_unknown_math_is_not_admitted_or_auto_deleted(self):
        self.freeze();self.retain_a_delete_metadata();self.manifest["objects"][0]["status"]="unknown"
        self.error_contains(self.check(),"unknown is not admission")

    def test_mathematical_deletion_needs_replacement(self):
        self.freeze();self.decision(self.a,"delete",delete_kind="non-mathematical")
        self.error_contains(self.check(),"classification_correction")

    def test_explicit_misclassification_can_correct_wrong_kind(self):
        (self.root/self.a).write_text((self.root/self.a).read_text().replace("For real x, x squared is nonnegative.","Only actor identity and task schedule."))
        self.commit();self.freeze()
        self.decision(self.a,"delete",delete_kind="non-mathematical",classification_correction={
            "original_kind":"theorem","why_nonmathematical":"Body contains actor and task schedule only.",
            "why_no_mathematics_lost":"No mathematical statement, definition, proof or question is present.","reviewed_by":"fixture semantic reader"})
        self.assertFalse(self.check()["errors"])

    def test_no_proof_is_not_a_deletion_reason(self):
        self.freeze();self.decision(self.a,"delete",delete_kind="non-mathematical",classification_correction={
            "original_kind":"theorem","why_nonmathematical":"no proof",
            "why_no_mathematics_lost":"old","reviewed_by":"fixture"})
        self.error_contains(self.check(),"absence of proof")

    def test_merge_requires_math_destination_and_preservation(self):
        self.freeze();self.decision(self.a,"merge",["archives/demo/state/定理/missing--定理.md"])
        report=self.check();self.error_contains(report,"not declared");self.error_contains(report,"preservation declaration")

    def test_attachment_is_not_a_mathematical_node(self):
        self.freeze();self.manifest["objects"]=[self.obj(self.a)]
        self.decision(self.a,"keep",[self.a])
        evidence="archives/demo/tools/evidence/identity.json"
        path=self.root/evidence;path.parent.mkdir(parents=True);path.write_text('{"identity":"fixture"}')
        self.manifest["objects"].append({"path":evidence,"sha256":curation.digest(path.read_bytes()),"role":"evidence", "owner_ids":["demo/A"],"use":"Input provenance of this exact example."})
        self.decision(self.m,"attach",[evidence]);(self.root/self.m).unlink()
        self.assertFalse(self.check(final=True)["errors"])
        self.assertEqual(curation.admitted_paths(self.root,final=True),(self.root/self.a,))
        resolved=curation.resolve_legacy_target(self.root,self.m)
        self.assertEqual(resolved["action"],"attach");self.assertEqual(resolved["targets"][0]["path"],evidence)

    def test_attachment_needs_an_admitted_math_owner(self):
        self.freeze();evidence="tools/evidence/log.json"
        path=self.root/evidence;path.parent.mkdir(parents=True);path.write_text('{}')
        self.manifest["objects"]=[{"path":evidence,"sha256":curation.digest(path.read_bytes()),"role":"evidence","owner_ids":["unknown"],"use":"reported check"}]
        self.decision(self.m,"attach",[evidence])
        self.error_contains(self.check(),"owner is not an admitted")

    def test_protected_math_cannot_only_become_an_attachment(self):
        self.freeze();self.decision(self.a,"attach",[])
        self.error_contains(self.check(),"cannot disappear into evidence")

    def test_unparsed_complete_proof_cannot_be_silently_demoted_to_attachment(self):
        (self.root/self.a).write_text("# Lemma\nFor every real x, x² >= 0.\nProof: the product of two equally signed numbers is nonnegative.\n")
        b=self.note("B");self.commit();self.freeze()
        # Even an existing admitted theorem B does not explain the independent
        # proof in A; a bare owner link must not authorize its disappearance.
        self.manifest["objects"]=[self.obj(b)];self.decision(b,"keep",[b])
        self.decision(self.m,"delete",delete_kind="non-mathematical");(self.root/self.m).unlink()
        evidence="tools/evidence/proof.txt";path=self.root/evidence;path.parent.mkdir(parents=True);path.write_bytes((self.root/self.a).read_bytes())
        self.manifest["objects"].append({"path":evidence,"sha256":curation.digest(path.read_bytes()),"role":"evidence","owner_ids":["demo/B"],"use":"an unrelated retained input"})
        self.decision(self.a,"attach",[evidence]);(self.root/self.a).unlink()
        self.error_contains(self.check(final=True),"classification_correction")

    def test_computation_header_does_not_hide_a_general_proof(self):
        c=self.note("GeneralProof",kind="computation",tag="计算",body="For every positive integer n the displayed exact identity holds; full induction proof follows.")
        self.commit();self.freeze();self.manifest["objects"]=[self.obj(self.a)]
        self.decision(self.a,"keep",[self.a])
        self.decision(self.m,"delete",delete_kind="non-mathematical");(self.root/self.m).unlink()
        evidence="tools/evidence/general-proof.txt";path=self.root/evidence;path.parent.mkdir(parents=True);path.write_bytes((self.root/c).read_bytes())
        self.manifest["objects"].append({"path":evidence,"sha256":curation.digest(path.read_bytes()),"role":"evidence","owner_ids":["demo/A"],"use":"an alleged output"})
        self.decision(c,"attach",[evidence]);(self.root/c).unlink()
        self.error_contains(self.check(final=True),"classification_correction")

    def test_unknown_original_cannot_be_deleted_without_content_classification(self):
        (self.root/self.a).write_text("A precise mathematical statement whose header is absent.\n")
        self.commit();self.freeze();self.decision(self.a,"delete",delete_kind="non-mathematical")
        self.error_contains(self.check(),"classification_correction")

    def test_final_requires_retiring_originals_to_be_removed(self):
        self.freeze();self.retain_a_delete_metadata()
        self.assertFalse(self.check()["errors"])
        self.error_contains(self.check(final=True),"obsolete original still exists")

    def test_new_formal_files_cannot_bypass_final_review(self):
        self.freeze();self.retain_a_delete_metadata();(self.root/self.m).unlink()
        new=self.note("C")
        self.assertIn(new,self.check()["new_unreviewed"])
        self.error_contains(self.check(final=True),"new formal object")

    def test_legacy_nonmath_deletion_is_explicit_not_silent(self):
        self.freeze();self.retain_a_delete_metadata();(self.root/self.m).unlink();self.save()
        route=curation.resolve_legacy_target(self.root,self.m)
        self.assertEqual(route["delete_kind"],"non-mathematical")
        self.assertEqual(route["targets"],[])
        self.assertIsNone(curation.resolve_legacy_target(self.root,"unregistered/file.md"))

    def test_plan_does_not_delete_files(self):
        self.freeze();self.retain_a_delete_metadata();self.save()
        result=curation.plan(self.root)
        self.assertFalse(result["mutates_files"]);self.assertTrue((self.root/self.m).is_file())

    def test_path_escape_is_not_a_target(self):
        self.freeze();self.manifest["objects"]=[dict(self.obj(self.a),path="../escape.md")]
        self.decision(self.a,"rewrite",["../escape.md"],preservation="scope and proof retained")
        self.error_contains(self.check(),"unsafe repository path")

    def test_bundle_is_retained_without_claiming_one_dependency_set(self):
        self.freeze();self.retain_a_delete_metadata();self.manifest["objects"][0]["dependency_scope"]="bundle-pending-split"
        report=self.check();self.assertFalse(report["errors"])
        self.assertEqual(report["admitted"][0]["dependency_scope"],"bundle-pending-split")
        self.assertEqual(report["admitted"][0]["status"],"unresolved-bundle")
        self.assertEqual(report["admitted"][0]["declared_status"],"proved")
        self.error_contains(self.check(final=True),"independent claims bundled")

    def test_baseline_tampering_is_bound_to_original_git_bytes(self):
        self.freeze();p=self.root/curation.DEFAULT_BASELINE;data=json.loads(p.read_text())
        data["files"][0]["sha256"]="b"*64;p.write_text(json.dumps(data))
        self.manifest["baseline_sha256"]=curation.digest(p.read_bytes());self.save()
        with self.assertRaisesRegex(ValueError,"pinned Git bytes"):
            curation.check(self.root)

    def test_baseline_cannot_relabel_a_protected_theorem_as_metadata(self):
        self.freeze();p=self.root/curation.DEFAULT_BASELINE;data=json.loads(p.read_text())
        next(r for r in data["files"] if r["path"]==self.a)["kind"]="metadata"
        p.write_text(json.dumps(data));self.manifest["baseline_sha256"]=curation.digest(p.read_bytes());self.save()
        with self.assertRaisesRegex(ValueError,"classification differs"):
            curation.check(self.root)

    def test_batch_legacy_routes_keep_explicit_nonmath_deletion(self):
        self.freeze();self.retain_a_delete_metadata();(self.root/self.m).unlink();self.save()
        routes=curation.legacy_target_routes(self.root)
        self.assertEqual(set(routes),{self.m})
        self.assertEqual(routes[self.m]["delete_kind"],"non-mathematical")

    def test_baseline_cannot_erase_uncertain_header_signal(self):
        path=self.root/self.m
        path.write_text(path.read_text().replace('kind: "metadata"','kind: "metadata"\nlegacy_ids: [unclosed'))
        self.commit();self.freeze()
        file=self.root/curation.DEFAULT_BASELINE;data=json.loads(file.read_text())
        next(r for r in data["files"] if r["path"]==self.m).pop("parse_error")
        file.write_text(json.dumps(data));self.manifest["baseline_sha256"]=curation.digest(file.read_bytes());self.save()
        with self.assertRaisesRegex(ValueError,"classification differs"):
            curation.check(self.root)

    def test_cli_partial_and_final_are_distinct(self):
        self.freeze()
        cmd=[sys.executable,str(ROOT/"tools/curation.py"),"--repo",str(self.root),"check"]
        partial=subprocess.run(cmd,capture_output=True,text=True)
        final=subprocess.run(cmd+["--final"],capture_output=True,text=True)
        self.assertEqual(partial.returncode,0,partial.stderr)
        self.assertEqual(json.loads(partial.stdout)["status"],"valid-partial-not-complete")
        self.assertEqual(final.returncode,1)


if __name__ == "__main__":
    unittest.main()
