"""Phase 2.5: byte-bound decisions and explicit mathematical admission.

This module validates a review contract, not mathematical truth.  It never
deletes files, guesses dispositions, or promotes a note because it exists.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path, PurePosixPath

from vendor.matek.frontmatter import parse_flat_frontmatter

DEFAULT_BASELINE = "research/curation/baseline.json"
DEFAULT_MANIFEST = "research/curation/manifest.json"
ACTIONS = {"keep", "rewrite", "merge", "attach", "delete", "pending"}
STATUSES = {"definition", "proved", "refuted", "conditional", "finite",
            "conjecture", "gap", "algorithm"}
MATH_KINDS = {
    "definition", "theorem", "lemma", "proof", "question", "problem",
    "open-problem", "conjecture", "candidate", "construction", "algorithm",
    "counterexample", "counterexample-family", "obstruction", "obstacle",
    "method-obstruction", "corollary", "conditional-corollary", "equivalence",
    "reduction", "method", "idea", "mathematical-object", "computation",
    "calculation", "computational-evidence", "bridge",
}
_FORMAL = re.compile(r"^archives/[^/]+/(?:subarchives/[^/]+/)*(?:state/.+\.md|问题--问题\.md)$")
_RESERVED = {"tools", "evidence", "workspaces", "cleanup", "history", ".git", ".rsync-tmp",
             "original", "comparison", "comparisons", "formal-comparison"}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _safe_path(root: Path, name: str) -> Path:
    if not isinstance(name, str) or not name or "\\" in name:
        raise ValueError("a nonempty repository-relative POSIX path is required")
    pure = PurePosixPath(name)
    if pure.is_absolute() or ".." in pure.parts or ".git" in pure.parts or pure.as_posix() != name:
        raise ValueError("unsafe repository path: " + name)
    root = root.resolve()
    target = root.joinpath(*pure.parts)
    if not target.resolve().is_relative_to(root):
        raise ValueError("path escapes repository: " + name)
    cursor = root
    for part in pure.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise ValueError("symlink is not an admitted artifact path: " + name)
    return target


def is_formal_path(name: str) -> bool:
    return isinstance(name,str) and bool(_FORMAL.fullmatch(name)) and not (_RESERVED & set(PurePosixPath(name).parts))


def formal_paths(root: Path) -> tuple[Path, ...]:
    """Only current archive objects, never nested evidence comparison copies."""
    root = Path(root).resolve()
    archive = root / "archives"
    if not archive.exists():
        return ()
    result = []
    for path in archive.rglob("*.md"):
        name = path.relative_to(root).as_posix()
        if is_formal_path(name):
            _safe_path(root, name)
            if path.is_file():
                result.append(path)
    return tuple(sorted(result))


def _meta(text: str) -> tuple[dict, str | None]:
    try:
        meta, _ = parse_flat_frontmatter(text)
        return meta, None
    except ValueError as exc:
        # Signals only: a broken header does not erase an original theorem's
        # protection or turn the file into a nonmathematical deletion candidate.
        meta = {}
        header = text.split("\n---\n", 1)[0] if text.startswith("---\n") else ""
        for key in ("id", "kind", "type_tag", "title", "status"):
            found = re.search(r"^" + key + r":\s*([^\n]+)", header, re.M)
            if found:
                meta[key] = found.group(1).strip().strip("\"'")
        return meta, str(exc)


def scan(root: Path) -> dict:
    root = Path(root).resolve()
    files = []
    for path in formal_paths(root):
        data = path.read_bytes()
        meta, error = _meta(data.decode("utf-8", errors="replace"))
        row = {"path": path.relative_to(root).as_posix(), "sha256": digest(data)}
        for src, dst in (("id", "object_id"), ("kind", "kind")):
            if isinstance(meta.get(src), str):
                row[dst] = meta[src]
        if error:
            row["parse_error"] = error
        files.append(row)
    return {"version": 1, "files": files,
            "status": "inventory-signals-only-not-mathematical-review"}


def _git(root: Path, *args: str, input_data: bytes | None = None) -> bytes:
    result = subprocess.run(["git", *args], cwd=root, input=input_data,
                            capture_output=True, timeout=45)
    if result.returncode:
        raise ValueError("cannot bind curation to the local Git snapshot")
    return result.stdout


def _check_snapshot(root: Path, baseline: dict) -> None:
    commit = baseline.get("commit")
    if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("baseline must name an exact Git commit")
    rows = baseline.get("files")
    if not isinstance(rows, list):
        raise ValueError("baseline files must be a list")
    names = []
    for row in rows:
        if not isinstance(row, dict) or not is_formal_path(row.get("path", "")):
            raise ValueError("baseline contains a nonformal path")
        _safe_path(root, row["path"])
        if not re.fullmatch(r"[0-9a-f]{64}", str(row.get("sha256", ""))):
            raise ValueError("baseline must bind every file to SHA-256")
        names.append(row["path"])
    if len(set(names)) != len(names):
        raise ValueError("duplicate baseline path")
    committed = {n for n in _git(root,"ls-tree","-r","--name-only","-z",commit).decode().split("\0") if is_formal_path(n)}
    if set(names) != committed:
        raise ValueError("baseline must cover every formal file in its pinned commit")
    # Verify original bytes against Git, not against a later edited worktree.
    if names:
        raw = _git(root, "cat-file", "--batch",
                   input_data="".join(commit + ":" + n + "\n" for n in names).encode())
        offset = 0
        for row in rows:
            end = raw.find(b"\n", offset)
            head = raw[offset:end].split()
            if len(head) != 3 or head[1] != b"blob":
                raise ValueError("baseline path absent in pinned commit: " + row["path"])
            size = int(head[2]); data = raw[end + 1:end + 1 + size]
            if digest(data) != row["sha256"]:
                raise ValueError("baseline SHA differs from pinned Git bytes: " + row["path"])
            meta,parse_error = _meta(data.decode("utf-8",errors="replace"))
            if (row.get("kind") != meta.get("kind") or row.get("object_id") != meta.get("id") or
                bool(row.get("parse_error")) != bool(parse_error)):
                raise ValueError("baseline identity/classification differs from pinned Git bytes: " + row["path"])
            offset = end + 2 + size
        if offset != len(raw):
            raise ValueError("invalid baseline Git response")


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def _shape(record: dict, allowed: set[str], required: set[str], label: str) -> None:
    if not isinstance(record,dict) or not required.issubset(record) or set(record)-allowed:
        raise ValueError(label + " has missing or unsupported fields")


def _needs_content_classification(original: dict) -> bool:
    # A resource/computation/program/review can contain a complete general
    # proof.  Parse failure is uncertainty, never evidence of nonmathematics.
    return original.get("kind") != "metadata" or bool(original.get("parse_error"))


def _classification_error(original: dict, decision: dict) -> str | None:
    correction=decision.get("classification_correction")
    fields={"original_kind","why_nonmathematical","why_no_mathematics_lost","reviewed_by"}
    if not isinstance(correction,dict) or set(correction)!=fields or any(not isinstance(correction.get(k),str) or not correction[k].strip() for k in fields):
        return "explicit classification_correction must account for the original independent mathematical content"
    if correction["original_kind"]!=(original.get("kind") or "unparsed"):
        return "classification correction does not bind the original kind"
    empty_grounds={"old","outdated","unproved","no proof","旧","未证明","无证明","没有证明"}
    if any(correction[k].strip().casefold() in empty_grounds for k in ("why_nonmathematical","why_no_mathematics_lost")):
        return "age or absence of proof is not evidence of nonmathematical content"
    return None


def freeze(root: Path, out: str = DEFAULT_BASELINE,
           manifest_out: str | None = None) -> dict:
    root = Path(root).resolve(); destination = _safe_path(root, out)
    if destination.exists():
        raise ValueError("baseline already exists; do not replace reviewed original bytes")
    manifest_path = _safe_path(root, manifest_out) if manifest_out else None
    if manifest_path and manifest_path.exists():
        raise ValueError("manifest already exists; do not overwrite decisions")
    current = scan(root)
    current.pop("status")
    current["commit"] = _git(root, "rev-parse", "HEAD").decode().strip()
    _check_snapshot(root, current)
    _write_json(destination, current)
    if manifest_path:
        pending = {"version": 1, "baseline": out,
                   "baseline_sha256": digest(destination.read_bytes()),
                   "objects": [], "decisions": [
                       {"path": r["path"], "sha256": r["sha256"], "action": "pending",
                        "targets": [], "reason": "尚未作数学准入判断"}
                       for r in current["files"]]}
        _write_json(manifest_path, pending)
    return {"status": "baseline-frozen-no-admission-decisions", "baseline": out,
            "files": len(current["files"]), "commit": current["commit"],
            "manifest": manifest_out}


def _load(root: Path, manifest: str | Path | None) -> tuple[dict, dict]:
    name = str(manifest or DEFAULT_MANIFEST)
    file = _safe_path(root, name)
    if not file.is_file():
        raise ValueError("missing phase-2.5 admission manifest; no automatic mathematical admission")
    data = json.loads(file.read_text())
    if not isinstance(data, dict) or type(data.get("version")) is not int or data.get("version") != 1:
        raise ValueError("unsupported curation manifest version")
    _shape(data,{"version","baseline","baseline_sha256","objects","decisions"},
           {"version","baseline","baseline_sha256","objects","decisions"},"curation manifest")
    base_path = _safe_path(root, data.get("baseline", ""))
    if not base_path.is_file() or digest(base_path.read_bytes()) != data.get("baseline_sha256"):
        raise ValueError("missing or changed fixed curation baseline")
    baseline = json.loads(base_path.read_text())
    if not isinstance(baseline,dict) or type(baseline.get("version")) is not int or baseline.get("version") != 1:
        raise ValueError("unsupported baseline version")
    _shape(baseline,{"version","commit","files"},{"version","commit","files"},"baseline")
    if not isinstance(baseline.get("files"),list):raise ValueError("baseline files must be a list")
    for row in baseline["files"]:
        _shape(row,{"path","sha256","object_id","kind","parse_error"},{"path","sha256"},"baseline file")
    _check_snapshot(root, baseline)
    return data, baseline


def check(root: Path, manifest: str | Path | None = None, final: bool = False) -> dict:
    """Validate declarations and byte bindings; a successful check is not a proof."""
    root = Path(root).resolve()
    data, baseline = _load(root, manifest)
    originals = {r["path"]: r for r in baseline["files"]}
    errors = []; objects = {}; math_ids = {}; decisions = {}
    def error(path, message): errors.append({"path": str(path), "error": message})
    for field in ("objects","decisions"):
        if not isinstance(data.get(field),list):
            raise ValueError("manifest " + field + " must be a list")
    for row in data.get("objects", []):
        if not isinstance(row, dict):
            error("objects", "object must be a record"); continue
        name = row.get("path", "")
        fields={"path","sha256","role","object_id","statement","conditions","support","use","status","dependency_scope"} if row.get("role")=="mathematics" else {"path","sha256","role","owner_ids","use"}
        try:_shape(row,fields,fields,"admitted object")
        except ValueError as exc:error(name,str(exc))
        try: path = _safe_path(root, name)
        except ValueError as exc: error(name, str(exc)); continue
        if name in objects:
            error(name, "duplicate target path"); continue
        objects[name] = row
        if not path.is_file() or digest(path.read_bytes()) != row.get("sha256"):
            error(name, "target missing or SHA changed since admission declaration"); continue
        role = row.get("role")
        if role == "mathematics":
            if not is_formal_path(name):
                error(name, "mathematics must have a canonical formal Markdown path"); continue
            for field in ("object_id", "statement", "conditions", "support", "use"):
                if not isinstance(row.get(field), str) or not row[field].strip():
                    error(name, "missing mathematical declaration: " + field)
            if not isinstance(row.get("status"),str) or row.get("status") not in STATUSES:
                error(name, "mathematical status must be explicit; unknown is not admission")
            if not isinstance(row.get("dependency_scope"),str) or row.get("dependency_scope") not in {"single-object","bundle-pending-split"}:
                error(name, "declare single-object or bundle-pending-split dependency_scope")
            try:
                meta, body = parse_flat_frontmatter(path.read_text())
                if not body.strip(): error(name, "empty mathematical body")
                for field in ("id", "kind", "type_tag", "title", "status", "summary"):
                    if not isinstance(meta.get(field), str) or not meta[field].strip():
                        error(name, "missing formal field: " + field)
                if not isinstance(meta.get("kind"),str) or meta.get("kind") not in MATH_KINDS:
                    error(name, "resource, operational review or metadata is not a mathematical node")
                if meta.get("id") != row.get("object_id"):
                    error(name, "object_id disagrees with actual Markdown identity")
                if not name.endswith("--" + str(meta.get("type_tag")) + ".md"):
                    error(name, "filename/type_tag mismatch")
                refs = meta.get("source_refs")
                if not isinstance(refs, list) or not refs or not all(isinstance(x,str) and x for x in refs):
                    error(name, "mathematical object needs its source binding")
            except ValueError as exc: error(name, str(exc))
            nid = row.get("object_id")
            if isinstance(nid,str):
                if nid in math_ids: error(name, "duplicate admitted mathematical ID: " + nid)
                else: math_ids[nid] = name
        elif role == "evidence":
            if is_formal_path(name): error(name, "attachments must leave the formal mathematical tree")
            owners = row.get("owner_ids")
            if not isinstance(owners,list) or not owners or not all(isinstance(x,str) and x for x in owners):
                error(name, "attachment needs explicit mathematical owner_ids")
            if not isinstance(row.get("use"),str) or not row["use"].strip():
                error(name, "attachment needs an actual supporting use")
        else: error(name, "role must be mathematics or evidence")
    for name,row in objects.items():
        if row.get("role") == "evidence":
            for owner in row.get("owner_ids", []) if isinstance(row.get("owner_ids"),list) else []:
                if not isinstance(owner,str) or owner not in math_ids: error(name, "attachment owner is not an admitted mathematical object: " + str(owner))
    used = set()
    for row in data.get("decisions", []):
        if not isinstance(row, dict): error("decisions", "decision must be a record"); continue
        name = row.get("path", "")
        try:_shape(row,{"path","sha256","action","targets","reason","preservation","delete_kind","classification_correction"},
                   {"path","sha256","action","targets","reason"},"curation decision")
        except ValueError as exc:error(name,str(exc))
        try:_safe_path(root,name)
        except ValueError as exc:error(name,str(exc));continue
        if name not in originals: error(name, "decision path is outside fixed baseline"); continue
        if name in decisions: error(name, "duplicate original decision"); continue
        decisions[name] = row; original = originals[name]; action = row.get("action")
        if row.get("sha256") != original["sha256"]: error(name, "stale decision: original SHA differs from baseline")
        if not isinstance(action,str) or action not in ACTIONS: error(name, "unknown curation action"); continue
        if not isinstance(row.get("reason"),str) or not row["reason"].strip(): error(name,"decision needs a substantive reason")
        targets = row.get("targets", [])
        if not isinstance(targets,list) or not all(isinstance(x,str) and x for x in targets):
            error(name, "targets must be repository paths"); continue
        if len(set(targets)) != len(targets): error(name, "duplicate target in decision")
        used.update(targets)
        if action == "pending":
            if targets: error(name, "pending content cannot supply admitted targets")
            path = _safe_path(root,name)
            if not path.is_file() or digest(path.read_bytes()) != original["sha256"]:
                error(name, "unreviewed original was removed or changed")
            continue
        for target in targets:
            if target not in objects: error(name, "target is not declared in objects: " + target)
        mathematical = [t for t in targets if objects.get(t,{}).get("role") == "mathematics"]
        if action == "keep":
            if targets != [name] or not mathematical: error(name, "keep must retain the same mathematical file")
            if objects.get(name,{}).get("sha256") != original["sha256"]:
                error(name, "keep changed original mathematical bytes; use rewrite with preservation declaration")
        elif action in {"rewrite", "merge"}:
            if not mathematical: error(name, "rewrite/merge requires an admitted mathematical replacement")
            if not isinstance(row.get("preservation"),str) or not row["preservation"].strip():
                error(name, "rewrite/merge needs scope, argument and boundary preservation declaration")
        elif action == "attach":
            if not targets or any(objects.get(t,{}).get("role") != "evidence" for t in targets):
                error(name, "attach requires evidence targets with mathematical owners")
            if _needs_content_classification(original):
                issue=_classification_error(original,row)
                if issue:error(name,"original cannot disappear into evidence without a mathematical replacement or " + issue)
        elif action == "delete":
            mode = row.get("delete_kind")
            if mode == "non-mathematical":
                if targets: error(name, "nonmathematical deletion must not manufacture replacement nodes")
                if _needs_content_classification(original):
                    issue=_classification_error(original,row)
                    if issue:error(name,"protected original needs a mathematical replacement or " + issue)
            elif mode == "redundant":
                if not mathematical: error(name, "redundant deletion needs an admitted mathematical replacement")
                if not isinstance(row.get("preservation"),str) or not row["preservation"].strip():
                    error(name, "redundant deletion needs a mathematical coverage explanation")
            else: error(name, "delete_kind must be non-mathematical or redundant")
        old = _safe_path(root,name)
        if name not in targets and old.exists():
            if digest(old.read_bytes()) != original["sha256"]:
                error(name, "retiring original changed outside its declared target binding")
            if final: error(name, "obsolete original still exists; plan does not perform deletion")
    # Undecided originals are protected even in a partial batch.
    for name, original in originals.items():
        if name not in decisions:
            path = _safe_path(root,name)
            if not path.is_file() or digest(path.read_bytes()) != original["sha256"]:
                error(name, "original changed or disappeared without a curation decision")
    for name in objects:
        if name not in used: error(name, "orphan target has no source disposition")
    current = {p.relative_to(root).as_posix() for p in formal_paths(root)}
    additions = sorted(current - set(originals) - {n for n,o in objects.items() if o.get("role")=="mathematics"})
    pending = sorted(set(originals) - set(decisions) | {n for n,d in decisions.items() if d.get("action")=="pending"})
    if final:
        for name in pending: error(name, "final admission cannot leave original unreviewed")
        for name in additions: error(name, "new formal object has no explicit admission decision")
        for name,row in objects.items():
            if row.get("role")=="mathematics" and row.get("dependency_scope")=="bundle-pending-split":
                error(name,"final admission cannot leave independent claims bundled without separate identities")
    admitted = []
    for name,row in sorted(objects.items()):
        if row.get("role")!="mathematics" or name not in used:continue
        exported=dict(row)
        if exported.get("dependency_scope")=="bundle-pending-split":
            exported["declared_status"]=exported["status"]
            exported["status"]="unresolved-bundle"
        admitted.append(exported)
    return {"status": "invalid" if errors else ("ready-for-stage3-with-declared-math-review" if final else "valid-partial-not-complete"),
            "errors": errors, "baseline_files": len(originals), "decisions": len(decisions),
            "pending": pending, "new_unreviewed": additions, "admitted": admitted,
            "limit": "Validates declared scope and byte bindings, not mathematical truth or proof completeness."}


def admitted_paths(root: Path, manifest: str | Path | None = None,
                   final: bool = False) -> tuple[Path, ...]:
    report = check(root,manifest,final)
    if report["errors"]:
        first=report["errors"][0]
        raise ValueError("curation admission invalid: " + first["path"] + ": " + first["error"])
    root=Path(root).resolve()
    return tuple(root / row["path"] for row in report["admitted"])


def legacy_target_routes(root: Path, manifest: str | Path | None = None) -> dict:
    """Validate once for a single batch, then return explicit old-target routes.

    Callers must not retain this result across file edits or separate checks.
    This avoids re-reading the full baseline for each historical done target.
    """
    root=Path(root).resolve()
    if manifest is None and not (root/DEFAULT_MANIFEST).is_file(): return {}
    report=check(root,manifest,False)
    if report["errors"]:
        raise ValueError("legacy target resolution requires a valid curation manifest")
    data,baseline=_load(root,manifest)
    by_path={o["path"]:o for o in data.get("objects",[])}
    return {decision["path"]:{"action":decision["action"],"delete_kind":decision.get("delete_kind"),
                             "baseline_commit":baseline["commit"],
                             "original_sha256":decision["sha256"],"reason":decision["reason"],
                             "targets":[by_path[n] for n in decision.get("targets",[])]}
            for decision in data["decisions"] if decision.get("action") not in {"pending","keep"}}


def resolve_legacy_target(root: Path, target: str,
                          manifest: str | Path | None = None) -> dict | None:
    """Resolve an old completion target through a checked curation decision."""
    return legacy_target_routes(root,manifest).get(target.split("#",1)[0])


def plan(root: Path, manifest: str | Path | None = None) -> dict:
    report=check(root,manifest,False); data,_=_load(Path(root).resolve(),manifest)
    report["operations"]=[{"action":d["action"],"original":d["path"],
                           "targets":d.get("targets",[]),"reason":d.get("reason","")}
                          for d in data.get("decisions",[]) if d.get("action")!="pending"]
    report["mutates_files"]=False
    return report


def main() -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo",type=Path,default=Path(__file__).resolve().parents[1])
    sub=p.add_subparsers(dest="command",required=True)
    s=sub.add_parser("scan");s.add_argument("--out")
    f=sub.add_parser("freeze");f.add_argument("--out",default=DEFAULT_BASELINE);f.add_argument("--manifest-out")
    for command in ("check","plan","export"):
        q=sub.add_parser(command);q.add_argument("--manifest",default=DEFAULT_MANIFEST);q.add_argument("--out")
        if command!="plan":q.add_argument("--final",action="store_true")
    a=p.parse_args();root=a.repo.resolve()
    if a.command=="scan":result=scan(root)
    elif a.command=="freeze":result=freeze(root,a.out,a.manifest_out)
    elif a.command=="plan":result=plan(root,a.manifest)
    else:
        result=check(root,a.manifest,a.final)
        if a.command=="export":
            if result["errors"]:raise ValueError("cannot export invalid admission manifest")
            result={"version":1,"status":result["status"],"objects":result["admitted"],
                    "pending_count":len(result["pending"]),"new_unreviewed":result["new_unreviewed"],
                    "limit":result["limit"]}
    if getattr(a,"out",None) and a.command!="freeze":_write_json(_safe_path(root,a.out),result)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 1 if result.get("errors") else 0


if __name__=="__main__":
    try:raise SystemExit(main())
    except (ValueError,OSError,KeyError,TypeError) as exc:
        raise SystemExit(str(exc))
