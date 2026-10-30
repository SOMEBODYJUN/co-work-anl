#!/usr/bin/env python3
"""Read-only coverage/navigation audit of one committed snapshot; no math verdict."""
import hashlib
import json
import posixpath
import re
import subprocess
import sys
from collections import Counter, deque
from urllib.parse import unquote


def git(*args):
    return subprocess.check_output(["git", *args])


revision = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
revision = git("rev-parse", "--verify", revision + "^{commit}").decode().strip()
paths = git("ls-tree", "-r", "--name-only", "-z", revision).decode().split("\0")
paths = {p for p in paths if p}
selected = sorted(p for p in paths if p.endswith(".md") or
                  p.startswith(("cleanup/progress/", "cleanup/increments/")) or
                  p in {"cleanup/sources.json", "cleanup/inventory.jsonl"})
queries = "".join(revision + ":" + p + "\n" for p in selected)
raw = subprocess.check_output(["git", "cat-file", "--batch"], input=queries.encode())
contents = {}
offset = 0
for p in selected:
    end = raw.index(b"\n", offset)
    header = raw[offset:end].split()
    assert len(header) == 3 and header[1] == b"blob", (p, header)
    size = int(header[2])
    contents[p] = raw[end + 1:end + 1 + size]
    offset = end + 2 + size
assert offset == len(raw)

meta = json.loads(contents["cleanup/sources.json"])
inventory = contents["cleanup/inventory.jsonl"]
assert hashlib.sha256(inventory).hexdigest() == meta["inventory_sha256"]
rows = [json.loads(line) for line in inventory.splitlines() if line]
assert len(rows) == meta["inventory_count"]
for inc in meta.get("increments", []):
    data = contents[inc["path"]]
    assert hashlib.sha256(data).hexdigest() == inc["sha256"]
    added = [json.loads(line) for line in data.splitlines() if line]
    assert len(added) == inc["count"]
    rows.extend(added)
assert len({r["id"] for r in rows}) == len(rows)

complete = {"integrated", "retained", "duplicate", "retired"}
states = {r["id"]: json.loads(contents.get("cleanup/progress/" + r["id"] + ".json", b"{}"))
          for r in rows}
errors = []
for row in rows:
    d = states[row["id"]]
    if d.get("disposition") not in complete:
        continue
    for k in ("full_file_reviewed", "related_material_checked", "unique_content_accounted_for"):
        if d.get(k) is not True:
            errors.append([row["id"], "missing declaration", k])
    for k in ("read_note", "comparison_note", "decision_note"):
        if not isinstance(d.get(k), str) or not d[k].strip():
            errors.append([row["id"], "missing explanation", k])
    if not d.get("owner") or d.get("source_sha256") != row["sha256"]:
        errors.append([row["id"], "owner/source binding"])
    targets = d.get("targets", [])
    if d["disposition"] in {"integrated", "retained", "duplicate"} and not targets:
        errors.append([row["id"], "missing targets"])
    for name in targets:
        if name.split("#")[0] not in paths:
            errors.append([row["id"], "missing committed target", name])
    if d["disposition"] == "integrated" and not any(".md" in p for p in targets):
        errors.append([row["id"], "missing explanatory Markdown"])


def links(p):
    text = contents[p].decode()
    for match in re.finditer(r"\[[^\]\n]*\]\(([^)\n]+)\)", text):
        name = match.group(1)
        if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", name) or name.startswith("#"):
            continue
        name = unquote(name.split("#")[0])
        yield posixpath.normpath(posixpath.join(posixpath.dirname(p), name))


formal = {p for p in paths if p.startswith("archives/") and "/state/" in p and p.endswith(".md")}
queue = deque(["README.md"])
seen = set()
while queue:
    p = queue.popleft()
    if p in seen or p not in contents or not p.endswith(".md"):
        continue
    seen.add(p)
    queue.extend(links(p))
broken = [[p, q] for p in sorted(formal) for q in links(p)
          if q not in paths and not any(x.startswith(q.rstrip("/") + "/") for x in paths)]
scopes = ["archives/customer-attraction", "archives/facility-games/subarchives/common-many",
          "archives/weighted-congestion", "archives/unrelated-machines", "archives/positive-kernels"]
scope_results = []
for scope in scopes:
    local = {p for p in formal if p.startswith(scope + "/state/")}
    scope_results.append({"scope": scope, "formal": len(local), "reachable_from_root": len(local & seen)})
print(json.dumps({
    "snapshot": revision,
    "source_versions": len(rows),
    "distinct_paths": len({r["path"] for r in rows}),
    "completed": sum(d.get("disposition") in complete for d in states.values()),
    "claimed": sum(d.get("owner") is not None and d.get("disposition") not in complete for d in states.values()),
    "unresolved": sum(d.get("disposition") == "needs-decision" for d in states.values()),
    "recorded_states": dict(sorted(Counter(d.get("disposition", "unread") for d in states.values()).items())),
    "receipt_structure_errors": errors,
    "formal_objects": len(formal),
    "formal_reachable_from_root_markdown_links": len(formal & seen),
    "unreachable_formal": sorted(formal - seen),
    "broken_local_links_in_formal": broken,
    "scopes": scope_results,
    "limits": "Declarations and existing targets do not establish full reading or mathematical correctness. Reachability follows explicit Markdown file links, ignores anchors, and excludes directory browsing, search, raw source refs and JSON graph links."
}, ensure_ascii=False, indent=2))
