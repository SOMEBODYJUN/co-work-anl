#!/usr/bin/env python3
"""Save a scoped research checkpoint, push normally, and verify remote reachability."""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

SCOPE = "tools"
DEFAULT_SAVE = "customer-attraction"
COMMON_PATHS = ["README.md", "AGENTS.md"]
SAVE_PATHS = {}
SAVE_PATTERNS = {}
SECRET = re.compile(rb"(?:github_pat_|gh[pousr]_)[A-Za-z0-9_]{12,}|-----BEGIN [A-Z ]*PRIVATE KEY-----")
ROUTING = ("GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR", "GIT_INDEX_FILE",
           "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES",
           "GIT_IMPLICIT_WORK_TREE", "GIT_GRAFT_FILE", "GIT_SHALLOW_FILE",
           "GIT_PREFIX", "GIT_INTERNAL_SUPER_PREFIX")


class Stop(RuntimeError):
    pass


class MapAssemblyChanged(Stop):
    pass


def token(path):
    values = set(re.findall(rb"(?:github_pat_|ghp_)[A-Za-z0-9_]{12,}", Path(path).read_bytes()))
    if len(values) != 1:
        raise Stop("Credential file must contain exactly one GitHub token.")
    return values.pop().decode()


def git(repo, *args, check=True, input_data=None):
    env = {k: v for k, v in os.environ.items() if k not in ROUTING}
    env["GIT_TERMINAL_PROMPT"] = "0"
    timeout = 600 if args[0] in {"fetch", "push"} else 45
    try:
        result = subprocess.run(["git", *args], cwd=repo, env=env, input=input_data,
                                capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        raise Stop("Git timed out. Rerun the same command; local commits are retained.")
    if check and result.returncode:
        detail = SECRET.sub(b"[REDACTED]", result.stderr or result.stdout).decode(errors="replace")
        raise Stop("Git failed: " + detail.strip()[:1000])
    return result


def value(repo, *args):
    return git(repo, *args).stdout.decode().strip()


def names(result):
    return [os.fsdecode(x) for x in result.stdout.split(b"\0") if x]


def relative(repo, path):
    p = Path(path)
    if ".." in p.parts:
        raise Stop("Paths must stay inside the repository.")
    p = p if p.is_absolute() else repo / p
    try:
        result = p.relative_to(repo).as_posix()
        p.resolve().relative_to(repo)
    except ValueError:
        raise Stop("Paths must stay inside the repository.")
    return result or "."


def audit_review_plans(repo, head, plans):
    """Check existing studio receipts against the commit about to be pushed.

    Read Git objects, never the mutable checkout. A merge retry calls this
    again on its new HEAD; ordinary journal checkpoints need no plan.
    """
    from research_runtime import REGISTRY, edge_digest, pin

    def read(name):
        name = relative(repo, name)
        result = git(repo, "show", head + ":" + name, check=False)
        if result.returncode:
            raise Stop("Reviewed publication is missing from final commit: " + name)
        return result.stdout

    def checked(ref):
        raw = read(ref['path'])
        if hashlib.sha256(raw).hexdigest() != ref['sha256']:
            raise Stop("Reviewed publication bytes changed before push: " + ref['path'])
        if 'revision_pin' in ref and pin(json.loads(raw)) != ref['revision_pin']:
            raise Stop("Reviewed record revision changed before push: " + ref['path'])
        return raw

    checked_plans = []
    for name in dict.fromkeys(plans):
        match = re.fullmatch(r'research/runs/([^/]+)/studio/backflow-plans/[^/]+/[0-9a-f]{64}\.json', name)
        if not match:
            raise Stop("Use the exact immutable plan path returned by studio promote")
        plan = json.loads(read(name))
        frozen = json.loads(checked(plan['freeze_ref']))
        review = json.loads(checked(plan['review_ref']))
        index = json.loads(read('research/runs/' + match[1] + '/studio.json'))
        if (plan.get('status') != 'backflow-plan-ready-local-not-published'
                or index['backflow_plans'].get(plan['plan_id'], {}).get('path') != name
                or index['freezes'].get(frozen['freeze_id']) != plan['freeze_ref']
                or index['artifacts'].get(frozen['artifact_id']) != frozen['artifact_ref']
                or index['reviews'].get(review['review_id']) != plan['review_ref']):
            raise Stop("Publication plan no longer matches its current reviewed artifact")
        checked(index['backflow_plans'][plan['plan_id']])
        checked(frozen['artifact_ref'])
        if (review.get('verdict') != 'approve' or review.get('independent') is not True
                or review['reviewer_agent_id'] in frozen['authors']
                or review['freeze_id'] != frozen['freeze_id']
                or review['freeze_revision_pin'] != plan['freeze_ref']['revision_pin']
                or review.get('reviewed_content_refs') != frozen['content_refs']):
            raise Stop("Publication review does not approve these exact frozen bytes")
        checked(review['report_ref'])
        for reference in frozen['content_refs']:
            checked(reference)
        for review_id, reference in index['reviews'].items():
            other = json.loads(checked(reference))
            if (other['freeze_id'] == frozen['freeze_id']
                    and other['freeze_revision_pin'] == plan['freeze_ref']['revision_pin']
                    and other['verdict'] != 'approve'
                    and review_id not in review.get('resolves_review_ids', [])):
                raise Stop("Unresolved exact-version review objection blocks publication")
        # The proposed full registry and graph projections are local working
        # files. Publish the reviewed delta and canonical registry, without
        # requiring duplicate registries or rebuildable graphs in every clone.
        base_ref = plan.get('base_registry_ref') or {}
        canonical_path = plan.get('registry_path', base_ref.get('path', REGISTRY))
        canonical = json.loads(read(canonical_path))
        batch = json.loads(checked(plan['registration_batch_ref']))
        objects = {row['object_id']: row for row in canonical['objects']}
        if any(objects.get(row['object_id']) != row for row in batch['objects']):
            raise Stop("Reviewed results are not installed in the final canonical registry")
        for reference in plan['edge_refs']:
            edge = json.loads(checked(reference))
            if reference['path'] not in canonical['edge_files']:
                raise Stop("Reviewed edge is not installed in the final canonical registry")
            if edge.get('status') == 'accepted':
                endpoints = {oid: pin(objects[oid]) for oid in set(edge['source_ids'] + edge['target_ids'])}
                if edge.get('endpoint_pins') != endpoints:
                    raise Stop("Reviewed edge has stale endpoints in the final canonical registry")
                if edge.get('review_digest') != edge_digest(edge):
                    raise Stop("Reviewed edge declaration changed before push")
                evidence_pins = {}
                for evidence in edge['evidence']:
                    checked(evidence)
                    evidence_pins[evidence['path']] = evidence['sha256']
                if edge.get('evidence_pins') != evidence_pins:
                    raise Stop("Reviewed edge has stale evidence bindings before push")
        checked_plans.append(name)
    return checked_plans


def audit_outgoing(repo, head, remote_tip, paths):
    """Inspect every unpublished revision, including blobs later overwritten/deleted.

    A scoped ``git add`` does not scope a push: all ancestors of HEAD travel
    with it. Combined merge diffs check new resolutions without treating an
    already-published peer's disjoint changes as our own new changes.
    """
    commits = value(repo, "rev-list", "--reverse", remote_tip + ".." + head).splitlines()
    changed = set()
    checked_blobs = set()
    outside = {}
    for commit in commits:
        metadata = git(repo, "cat-file", "commit", commit).stdout
        if SECRET.search(metadata):
            raise Stop("Credential-like commit metadata in outgoing history: " + commit)
        files = names(git(repo, "diff-tree", "--root", "--no-commit-id",
                          "--no-renames", "--cc", "--name-only", "-r", "-z", commit))
        tree_entries = {item.split(b"\t",1)[1].decode(): item for item in
                        git(repo,"ls-tree","-r","-z",commit).stdout.split(b"\0") if item} if files else {}
        for name in files:
            changed.add(name)
            if not any(p == "." or name == p or name.startswith(p + "/") for p in paths):
                outside.setdefault(name, []).append(commit)
            if re.search(r"(^|/)(?:\.env(?:\..*)?|githubtoken[^/]*|[^/]*\.(?:pem|key))$", name, re.I):
                raise Stop("Credential-like filename in outgoing history: " + name + " at " + commit)
            entry = tree_entries.get(name,b"")
            if not entry:  # A deletion still participates in the scope check.
                continue
            mode, kind, object_id = entry.split(b"\t", 1)[0].split()
            if mode not in (b"100644", b"100755") or kind != b"blob":
                raise Stop("Outgoing nonregular file needs explicit handling: " + name + " at " + commit)
            if object_id not in checked_blobs:
                content = git(repo, "cat-file", "blob", object_id.decode()).stdout
                if SECRET.search(content):
                    raise Stop("Credential-like content in outgoing history: " + name + " at " + commit)
                checked_blobs.add(object_id)
    if outside:
        detail = "; ".join(name + " [" + ", ".join(c[:12] for c in ids) + "]"
                           for name, ids in sorted(outside.items()))
        raise Stop("Outgoing commits include paths outside checkpoint scope; "
                   "include these paths explicitly before pushing: " + detail)
    return commits, sorted(changed)


MAP_REVIEW = "map/integration.json"
MAP_COVERAGE = "map/coverage.json"
MAP_REGISTRY = "research/registry.json"


def map_projection(name):
    return name == "map/graph-v2.json" or re.fullmatch(
        r"archives/[^/]+(?:/subarchives/[^/]+)*/map/graph-v2\.json", name)


def map_json(repo, revision, path):
    result = git(repo, "show", revision + ":" + path, check=False)
    return None if result.returncode else json.loads(result.stdout)


def audit_map_projections(repo, head, remote_tip, paths, rows):
    """Check partial assembly and final projections against the same fetched receipts."""
    from research_runtime import _effective_map_done, _map_registration_pin, pin

    registries = {}
    needs_review = bool({MAP_REVIEW, MAP_COVERAGE} & set(paths))
    final = False
    for name in paths:
        if not map_projection(name):
            continue
        graph = map_json(repo, head, name)
        if graph is None:  # Removing an obsolete projection is allowed.
            continue
        needs_review = True
        registry = graph.get("registry")
        if not isinstance(registry, str) or not registry:
            raise Stop("Map projection has no registered input: " + name)
        if registry not in registries:
            registries[registry] = pin(map_json(repo, head, registry))
        if graph.get("registry_pin") != registries[registry]:
            raise MapAssemblyChanged("Map projection has stale registry inputs after concurrent changes: " + name)
        if graph.get("status") == "registered-coverage":
            final = True
    done = _effective_map_done(rows)
    registry_names = {row["definition"]["registry"] for row in done.values()} or {MAP_REGISTRY}
    for registry in registry_names & set(paths):
        current = map_json(repo, head, registry)
        published = map_json(repo, remote_tip, registry)
        if (current is not None and published is not None
                and current.get("edge_files", []) != published.get("edge_files", [])
                and _map_registration_pin(current) == _map_registration_pin(published)):
            needs_review = True
    if not needs_review:
        return
    if len(registry_names | registries.keys()) != 1:
        raise Stop("Canonical map files must refer to one registry.")
    registry, = registry_names
    review = map_json(repo, head, MAP_REVIEW)
    coverage = map_json(repo, head, MAP_COVERAGE)
    expected = {tid: pin(row["receipt"]) for tid, row in done.items()}
    if (not done or not isinstance(review, dict) or not isinstance(coverage, dict)
            or review.get("registry_pin") != (registries.get(registry) or pin(map_json(repo, head, registry)))
            or review.get("task_receipt_pins", {}) != expected
            or (final and any(row["state"] not in {"done", "withdrawn"} for row in rows))):
        raise MapAssemblyChanged("Map assembly differs from the current published registry or receipts.")


def recover_map_assembly(repo, head, remote_tip, outgoing, namespace):
    """Preserve a losing integration draft, then get a clean peer snapshot."""
    from research_runtime import _map_registration_pin

    role = git(repo, "config", "--local", "--get", "wcg.role", check=False).stdout.decode().strip()
    if (role != "mapper"
            or not any(name in {MAP_REVIEW, MAP_COVERAGE} or map_projection(name) for name in outgoing)
            or any(name not in {MAP_REGISTRY, MAP_REVIEW, MAP_COVERAGE} and not map_projection(name)
                   for name in outgoing)
            or git(repo, "status", "--porcelain", "--untracked-files=no").stdout):
        return None
    base = value(repo, "merge-base", head, remote_tip)
    if MAP_REGISTRY in outgoing and (
            _map_registration_pin(map_json(repo, head, MAP_REGISTRY))
            != _map_registration_pin(map_json(repo, base, MAP_REGISTRY))):
        return None
    old, local, remote = (map_json(repo, rev, MAP_REVIEW) for rev in (base, head, remote_tip))
    backup = "refs/wcg/map-integration-drafts/" + namespace + "/" + head
    git(repo, "update-ref", backup, head)
    if git(repo, "reset", "--keep", remote_tip, check=False).returncode:
        return None
    # Independent reviewed rows can be carried forward on identical math and
    # receipt inputs. A disputed or stale row stays recoverable in the old ref.
    if isinstance(local, dict) and remote is None:
        # A registration correction can beat the first graph publication.
        # Keep actual prose as a draft for assemble's targeted invalidation.
        draft = repo / MAP_REVIEW
        draft.parent.mkdir(parents=True, exist_ok=True)
        draft.write_text(json.dumps(local, ensure_ascii=False, indent=2) + "\n")
    elif isinstance(local, dict) and isinstance(remote, dict):
        inputs = ("registry_pin", "edge_pins", "task_receipt_pins")
        if all(local.get(k) == remote.get(k) for k in inputs):
            previous = old if isinstance(old, dict) and all(old.get(k) == local.get(k) for k in inputs) else {}

            def independent(row, published, original):
                if original is not None:
                    return row != original and published == original
                return bool(row and row.get("comparison_scope")) and not (published or {}).get("comparison_scope")

            carried = False
            for scope, row in local.get("archive_reviews", {}).items():
                if independent(row, remote.get("archive_reviews", {}).get(scope),
                               previous.get("archive_reviews", {}).get(scope)):
                    remote.setdefault("archive_reviews", {})[scope] = row
                    carried = True
            key = "cross_archive_review"
            if independent(local.get(key), remote.get(key), previous.get(key)):
                remote[key] = local[key]
                carried = True
            if carried:
                for key in ("reviewed_by", "review_note"):
                    if not remote.get(key) and local.get(key):
                        remote[key] = local[key]
                (repo / MAP_REVIEW).write_text(json.dumps(remote, ensure_ascii=False, indent=2) + "\n")
    return backup


def audit_map_write_scope(repo, remote_tip, outgoing, head=None):
    """Check map outputs against the ownership at the tip we just fetched."""
    if not outgoing:
        return

    def config(key):
        return git(repo, "config", "--local", "--get", key, check=False).stdout.decode().strip()

    workflow = config("wcg.workflowRun")
    if not workflow or config("wcg.role") != "mapper":
        return
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,95}", workflow):
        raise Stop("Invalid map workflow binding.")
    home = "research/operations/" + workflow
    task_dir = home + "/tasks/"
    if any(name == home + "/lead.json" or name.startswith(task_dir) for name in outgoing):
        raise Stop("Publish map ownership and task state with work.py map. Local checkpoint retained.")

    entries = git(repo, "ls-tree", "-r", "-z", remote_tip, "--", task_dir).stdout
    oids = [entry.split(b"\t", 1)[0].split()[2] for entry in entries.split(b"\0")
            if entry and entry.endswith(b".json")]
    rows = []
    if oids:
        raw = git(repo, "cat-file", "--batch", input_data=b"\n".join(oids) + b"\n").stdout
        offset = 0
        for oid in oids:
            end = raw.find(b"\n", offset)
            header = raw[offset:end].split()
            if end < 0 or len(header) != 3 or header[:2] != [oid, b"blob"]:
                raise Stop("Cannot verify published map task ownership. Local checkpoint retained.")
            size = int(header[2])
            rows.append(json.loads(raw[end + 1:end + 1 + size]))
            offset = end + size + 2
        if offset != len(raw):
            raise Stop("Cannot verify published map task ownership. Local checkpoint retained.")

    canonical = {"research/registry.json", "map/coverage.json", "map/integration.json",
                 "map/graph-v2.json", "map/planned-tasks.json", "map/README.md"}
    canonical.update(row["definition"]["registry"] for row in rows)
    shared_files, task_files = [], []
    for name in outgoing:
        archive_output = re.fullmatch(r"archives/[^/]+(?:/subarchives/[^/]+)*/map/(.+)", name)
        if name in canonical or (archive_output and archive_output[1] == "graph-v2.json"):
            shared_files.append(name)
            continue
        scopes = [row for row in rows
                  if any(name == path or name.startswith(path + "/")
                         for path in row["definition"]["write_paths"])]
        if scopes or name.startswith("map/") or archive_output:
            owners = {row.get("owner") for row in scopes if row["state"] in {"claimed", "blocked"}}
            task_files.append((name, owners))
    if not shared_files and not task_files:
        return

    actor, instance = config("wcg.actor"), config("wcg.instance")
    if not re.fullmatch(r"Boss[1-9][0-9]*", actor) or not re.fullmatch(r"[0-9a-f]{32}", instance):
        raise Stop("Start the registered map conversation before publishing map outputs.")
    registered = git(repo, "show", remote_tip + ":" + home + "/people/" + actor + ".json", check=False)
    if registered.returncode or json.loads(registered.stdout).get("instance") != instance:
        raise Stop("This conversation no longer matches the published map identity. Local checkpoint retained.")
    denied = [name for name, owners in task_files if owners != {actor}]
    if denied:
        raise Stop("Published map task scope is not currently owned by " + actor + ": " +
                   ", ".join(denied) + ". Local checkpoint retained.")
    if shared_files and head is not None:
        audit_map_projections(repo, head, remote_tip, shared_files, rows)


def describe_assets(repo, directory, commit, files, branch="main"):
    assets = []
    present=set(names(git(repo,"ls-tree","-r","--name-only","-z",commit)))
    for name in files:
        if name not in present:
            continue
        blob = git(repo, "cat-file", "blob", commit + ":" + name, check=False)
        if not blob.returncode:
            asset = {"branch": branch, "commit": commit, "path": name,
                     "sha256": hashlib.sha256(blob.stdout).hexdigest()}
            descriptor = directory / (hashlib.sha256(name.encode()).hexdigest()[:16] + ".json")
            descriptor.write_text(json.dumps(asset, ensure_ascii=False, indent=2) + "\n")
            assets.append({"asset": asset, "descriptor": str(descriptor)})
    return assets


def audit_studio_owners(repo, files, baseline, candidate=None):
    runs = set()
    for name in files:
        parts = name.split("/")
        if len(parts) > 3 and parts[0] == "research" and parts[1] in {"runs", "workspaces"}:
            runs.add(parts[2])
    if not runs:
        return
    actor = git(repo, "config", "--local", "--get", "wcg.actor",
                check=False).stdout.decode().strip()
    save = git(repo, "config", "--local", "--get", "wcg.save",
               check=False).stdout.decode().strip()
    subarchive = git(repo, "config", "--local", "--get", "wcg.subarchive",
                     check=False).stdout.decode().strip()
    bound = f"archives/{save}" if save else None
    if bound and subarchive:
        bound += f"/subarchives/{subarchive}"
    for run_id in sorted(runs):
        name = f"research/runs/{run_id}/studio.json"
        before = git(repo, "show", baseline + ":" + name, check=False)
        if candidate is None:
            path = repo / name
            if path.is_symlink():
                raise Stop("Studio index must be an ordinary file: " + name)
            data = path.read_bytes() if path.is_file() else None
        else:
            after = git(repo, "show", candidate + ":" + name, check=False)
            data = after.stdout if after.returncode == 0 else None
        if before.returncode == 0 and data is None:
            raise Stop("Checkpoint cannot remove a studio ownership record: " + name)
        previous = json.loads(before.stdout) if before.returncode == 0 else None
        current = json.loads(data) if data is not None else None
        for exists, record in ((before.returncode == 0, previous), (data is not None, current)):
            if not exists:
                continue
            if not isinstance(record, dict) or record.get("run_id") != run_id:
                raise Stop("Invalid studio ownership record: " + name)
            if not actor or record.get("owner") != actor:
                raise Stop("Checkpoint includes changes in another Boss's studio: " + run_id +
                           ". Keep the draft and publish from the owning clone.")
            if record.get("archive_scope") and record["archive_scope"] != bound:
                raise Stop("Checkpoint requires the clone bound to " + record["archive_scope"] + ": " + run_id)
        if previous and previous.get("archive_scope") and current.get("archive_scope") != previous["archive_scope"]:
            raise Stop("Checkpoint cannot change the studio archive scope: " + run_id)


def default_paths(repo):
    actor = git(repo, "config", "--local", "--get", "wcg.actor", check=False).stdout.decode().strip()
    save = git(repo, "config", "--local", "--get", "wcg.save", check=False).stdout.decode().strip() or DEFAULT_SAVE
    safe_id = r"[A-Za-z0-9][A-Za-z0-9_.-]{0,63}"
    if not re.fullmatch(safe_id, save) or (actor and not re.fullmatch(safe_id, actor)):
        raise Stop("Invalid local actor/save ID; repair the local Work configuration first.")
    # Unknown archives may save shared registers and their own workspace, but
    # must select new mathematical directories explicitly until registered here.
    subarchive=git(repo,"config","--local","--get","wcg.subarchive",check=False).stdout.decode().strip()
    archive_base="archives/"+save
    if subarchive:
        if not re.fullmatch(safe_id,subarchive):raise Stop("Invalid subarchive binding")
        archive_base+="/subarchives/"+subarchive
    paths = list(SAVE_PATHS.get(save, [archive_base])) + COMMON_PATHS
    # Legacy CAG audits are flat files. Include new and tracked-deleted matches
    # without treating glob strings as broad checkpoint pathspecs.
    for pattern in SAVE_PATTERNS.get(save, []):
        matches = {p.relative_to(repo).as_posix() for p in repo.glob(pattern)}
        matches.update(name for name in names(git(repo, "ls-files", "-z", "--", pattern))
                       if Path(name).match(pattern))
        paths.extend(sorted(matches))
    paths = list(dict.fromkeys(paths))
    if actor:
        paths.append(archive_base + "/workspaces/" + actor)
    paths = [p for p in paths if (repo / p).exists()
             or git(repo, "ls-files", "--", ":(literal)" + p).stdout]
    if not paths:
        raise Stop("No default checkpoint paths for archive " + save +
                   "; initialize your workspace or supply explicit paths.")
    return paths


def save(args):
    repo = Path(value(args.repo, "rev-parse", "--show-toplevel"))
    common = Path(value(repo, "rev-parse", "--git-common-dir"))
    common = (repo / common).resolve()
    cache = common / "wcg-checkpoint"
    cache.mkdir(exist_ok=True)
    with (cache / "writer.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise Stop("Another checkpoint is writing this clone. Retry after it finishes.")
        return locked_save(repo, common, cache, args)


def locked_save(repo, common, cache, args):
    branch_result = git(repo, "symbolic-ref", "--quiet", "--short", "HEAD", check=False)
    if branch_result.returncode:
        raise Stop("Detached HEAD: switch to a dedicated work branch first.")
    branch = branch_result.stdout.decode().strip()
    board = git(repo, "config", "--local", "--get", "wcg.boardBranch", check=False).stdout.decode().strip() or "wcg/board"
    if branch == board or branch == "wcg/board" or branch.startswith("wcg/board-"):
        raise Stop("Board messages must use board.py.")
    bound = git(repo, "config", "--local", "--get", "wcg.branch", check=False).stdout.decode().strip() or "main"
    if branch != bound:
        raise Stop("Current branch differs from the bound branch " + bound + "; work is retained.")
    git(repo, "check-ref-format", "refs/heads/" + bound)
    for item in ("MERGE_HEAD", "CHERRY_PICK_HEAD", "REVERT_HEAD", "rebase-merge", "rebase-apply"):
        if Path(value(repo, "rev-parse", "--git-path", item)).is_absolute():
            p = Path(value(repo, "rev-parse", "--git-path", item))
        else:
            p = repo / value(repo, "rev-parse", "--git-path", item)
        if p.exists():
            raise Stop("Finish the existing Git operation first: " + item)
    if git(repo, "ls-files", "-u").stdout:
        raise Stop("Resolve existing merge conflicts first.")
    remote = value(repo, "remote", "get-url", "--all", "origin")
    push_remote = value(repo, "remote", "get-url", "--push", "--all", "origin")
    if remote != push_remote or "\n" in remote:
        raise Stop("origin must have one identical fetch and push destination.")
    if SECRET.search(remote.encode()) or re.search(r"https?://[^/]*@", remote):
        raise Stop("Remove credentials embedded in origin; use external authentication.")
    credential = None
    if not getattr(args, 'local_only', False):
        credential = args.token_file or os.environ.get("WCG_CHECKPOINT_TOKEN_FILE")
        auth_mode=git(repo,'config','--local','--get','wcg.auth',check=False).stdout.decode().strip()
        if auth_mode=='ssh':credential=None
        if not credential and auth_mode!='ssh':
            credential = git(repo, "config", "--local", "--get", "wcg.tokenFile", check=False).stdout.decode().strip()
        if credential:
            credential = Path(credential).resolve()
            if credential.is_relative_to(repo):
                raise Stop("Keep the credential file outside the repository.")
            token(credential)  # Validate silently; only the file path is remembered locally.
            if args.token_file:
                git(repo, "config", "--local", "wcg.tokenFile", str(credential))
            os.environ["WCG_CHECKPOINT_TOKEN_FILE"] = str(credential)
            os.environ["GIT_ASKPASS"] = str(Path(__file__).resolve())
            os.environ["WCG_CHECKPOINT_ASKPASS"] = "1"
    paths = [relative(repo, p) for p in (args.paths or default_paths(repo))]
    specs = [":(literal)" + p for p in paths]
    stage_specs = []
    historical_deletions = None
    for p, spec in zip(paths, specs):
        if (repo / p).exists() or git(repo, "ls-files", "--", spec).stdout:
            stage_specs.append(spec)
            continue
        # A prior local commit may already have deleted this exact path. It
        # still belongs to the outgoing audit scope, but cannot be git-added.
        if historical_deletions is None:
            historical_deletions = set()
            tracking = "refs/remotes/origin/" + bound
            if not git(repo, "rev-parse", "--verify", tracking, check=False).returncode:
                for commit in value(repo, "rev-list", tracking + "..HEAD").splitlines():
                    historical_deletions.update(names(git(repo, "diff-tree", "--root", "--no-commit-id",
                        "--name-only", "--diff-filter=D", "-r", "-z", commit)))
        if p not in historical_deletions:
            raise Stop("Unknown checkpoint path: " + p)
    publish_only = getattr(args, 'publish_only', False)
    staged = set(names(git(repo, "diff", "--cached", "--name-only", "-z"))) if not publish_only else set()
    selected = set(names(git(repo, "diff", "--cached", "--name-only", "-z", "--", *specs)))
    if staged - selected:
        raise Stop("Staged files outside scope; include them explicitly or unstage them: " +
                   ", ".join(sorted(staged - selected)))
    changed = set()
    if not publish_only:
        changed.update(names(git(repo, "diff", "HEAD", "--name-only", "-z", "--", *specs)))
        changed.update(selected)
        changed.update(names(git(repo, "ls-files", "--others", "--exclude-standard", "-z", "--", *specs)))
    audit_studio_owners(repo, changed, "HEAD")
    for name in changed:
        p = repo / name
        if p.is_symlink():
            raise Stop("Changed symlink needs explicit handling: " + name)
        if re.search(r"(^|/)(?:\.env(?:\..*)?|githubtoken[^/]*|[^/]*\.(?:pem|key))$", name, re.I):
            raise Stop("Credential-like filename excluded: " + name)
        if p.is_file() and SECRET.search(p.read_bytes()):
            raise Stop("Credential-like content excluded: " + name)
    message = args.message or "checkpoint: " + ", ".join(Path(p).name for p in sorted(changed)[:3])
    if not message.strip() or SECRET.search(message.encode()):
        raise Stop("Commit message must be nonempty and contain no credentials.")
    if changed and stage_specs:
        git(repo, "add", "-A", "--", *stage_specs)
    # Deleted raw-source files have no newly introduced whitespace to check.
    if not publish_only:
        git(repo, "diff", "--cached", "--check", "--no-renames", "--diff-filter=ACMR")
    files = names(git(repo, "diff", "--cached", "--name-only", "-z")) if not publish_only else []
    created = bool(files)
    options = []
    for key, default in (("user.name", "WCG Researcher"),
                         ("user.email", "wcg@users.noreply.github.com")):
        if git(repo, "config", "--get", key, check=False).returncode:
            options += ["-c", key + "=" + default]
    if created:
        git(repo, *options, "commit", "--quiet", "-m", message)
    snapshot = value(repo, "rev-parse", "HEAD")
    namespace = hashlib.sha256(branch.encode()).hexdigest()[:16]
    record_dir = cache / namespace
    record_dir.mkdir(exist_ok=True)
    receipt = record_dir / "receipt.json"
    if not created and receipt.exists():
        previous = json.loads(receipt.read_text())
        if previous["commit"] == snapshot:
            files = previous["files"]
    if not files:
        files = names(git(repo, "diff-tree", "--root", "--no-commit-id",
                          "--name-only", "-r", "-z", snapshot, "--", *specs))
    assets = describe_assets(repo, record_dir, snapshot, files, branch)
    result = {"status": "local-only", "branch": branch, "commit": snapshot,
              "files": files, "created_commit": created, "assets": assets,
              "outgoing_commits": [], "outgoing_files": []}
    if not created and receipt.exists() and previous["commit"] == snapshot:
        for key in ("outgoing_commits", "outgoing_files"):
            result[key] = previous.get(key, [])
    receipt.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print("LOCAL_CHECKPOINT " + snapshot, file=sys.stderr, flush=True)
    if getattr(args,'local_only',False):return result
    head = snapshot
    ref = "refs/heads/" + branch
    private = "refs/wcg/checkpoint/" + namespace
    detail = ""
    for attempt in range(20):
        if value(repo, "rev-parse", "HEAD") != head:
            raise Stop("HEAD changed outside the checkpoint lock. Local snapshot: " + snapshot)
        # A fetch must succeed before every push. Never infer the outgoing
        # range from a stale tracking ref or upload unexamined local history.
        before = git(repo, "fetch", "--quiet", "--no-tags", "--no-write-fetch-head",
                     "origin", "+" + ref + ":" + private, check=False)
        if before.returncode:
            exists = git(repo, "ls-remote", "--exit-code", "origin", ref, check=False)
            if exists.returncode == 2 and getattr(args, "create_branch", False) and branch != "main":
                # First publication audits every outgoing commit against main.
                # Push remains a normal fast-forward operation if a peer wins
                # the creation race; the next iteration fetches that peer tip.
                git(repo, "fetch", "--quiet", "--no-tags", "--no-write-fetch-head",
                    "origin", "+refs/heads/main:" + private)
                if git(repo, "merge-base", "--is-ancestor", private, head, check=False).returncode:
                    raise Stop("New branch must descend from its verified remote-main source anchor; local snapshot retained.")
            else:
                detail = SECRET.sub(b"[REDACTED]", before.stderr).decode(errors="replace").strip()[:500]
                if exists.returncode == 2:
                    detail = "Remote branch does not exist; first publication requires --create-branch."
                break
        baseline = value(repo, "rev-parse", private)
        commits, outgoing = audit_outgoing(repo, head, baseline, paths)
        plans = list(getattr(args, 'review_plan', []) or [])
        audit_studio_owners(repo, [*outgoing, *plans], baseline, head)
        result["outgoing_commits"] = list(dict.fromkeys(result["outgoing_commits"] + commits))
        result["outgoing_files"] = sorted(set(result["outgoing_files"]) | set(outgoing))
        result["files"] = sorted(set(result["files"]) | set(outgoing))
        result["assets"] = describe_assets(repo, record_dir, head, result["files"], branch)
        result["checked_head"] = head
        receipt.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
        try:
            audit_map_write_scope(repo, baseline, outgoing, head)
        except MapAssemblyChanged as exc:
            backup = recover_map_assembly(repo, head, baseline, outgoing, namespace)
            if backup:
                raise Stop(str(exc) + " Draft retained at " + backup +
                           ". Run work.py sync, then map assemble and rebuild.") from exc
            raise Stop(str(exc) + " Local checkpoint retained. Sync, assemble and rebuild before publishing.") from exc
        result['reviewed_plans'] = audit_review_plans(repo, head, plans)
        if plans:
            result['review_checked_head'] = head
        pushed = git(repo, "push", "--quiet", "origin", head + ":" + ref, check=False)
        fetched = git(repo, "fetch", "--quiet", "--no-tags", "--no-write-fetch-head",
                      "origin", "+" + ref + ":" + private, check=False)
        if fetched.returncode:
            detail = SECRET.sub(b"[REDACTED]", fetched.stderr).decode(errors="replace").strip()[:500]
            continue
        tip = value(repo, "rev-parse", private)
        if not git(repo, "merge-base", "--is-ancestor", head, tip, check=False).returncode:
            result.update(status="pushed", remote_tip=tip, pushed_head=head)
            receipt.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
            return result
        if not git(repo, "merge-base", "--is-ancestor", tip, head, check=False).returncode:
            if pushed.returncode:  # Authentication/policy failure, not divergent history.
                detail = SECRET.sub(b"[REDACTED]", pushed.stderr).decode(errors="replace").strip()[:500]
                break
            continue
        if git(repo, "status", "--porcelain", "--untracked-files=no").stdout:
            raise Stop("Remote diverged and other tracked work is dirty. Snapshot retained: " + snapshot)
        merged = git(repo, *options, "merge", "--no-edit", "-m", "checkpoint sync: " + branch,
                     tip, check=False)
        if merged.returncode:
            conflicts = names(git(repo, "diff", "--name-only", "--diff-filter=U", "-z"))
            git(repo, "merge", "--abort", check=False)
            backup = recover_map_assembly(repo, head, tip, outgoing, namespace)
            if backup:
                raise Stop("A peer published this map assembly first. Draft retained at " + backup +
                           ". Run work.py sync, then map assemble and rebuild.")
            detail = SECRET.sub(b"[REDACTED]", merged.stderr).decode(errors="replace").strip()
            raise Stop("Remote merge stopped; local snapshot retained. Conflicts: " +
                       ", ".join(conflicts) + " " + detail[:500])
        head = value(repo, "rev-parse", "HEAD")
        jitter = int(hashlib.sha256(f"{snapshot}:{attempt}".encode()).hexdigest()[:4], 16) / 65535
        time.sleep(min(0.5, 0.03 * 2 ** min(attempt, 4)) * (0.5 + jitter))
    raise Stop("Remote confirmation unavailable. " + detail +
               " Rerun the same command. Receipt: " + str(receipt))


def main():
    if os.environ.get("WCG_CHECKPOINT_ASKPASS") == "1" and len(sys.argv) == 2:
        if sys.argv[1].startswith("Username"):
            print("x-access-token")
            return
        if sys.argv[1].startswith("Password"):
            print(token(os.environ["WCG_CHECKPOINT_TOKEN_FILE"]))
            return
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="Repository-root paths; default: this research directory")
    parser.add_argument("--repo", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("-m", "--message")
    parser.add_argument("--token-file", help="Optional external token file; remembers only its path locally")
    parser.add_argument("--create-branch", action="store_true",
                        help="Allow first publication of the bound branch, audited against remote main")
    parser.add_argument('--local-only',action='store_true')
    parser.add_argument('--publish-only', action='store_true', help='Publish existing commits without staging or committing workspace changes')
    parser.add_argument('--review-plan', action='append', default=[], help='Existing studio promote receipt checked against the final commit before every push')
    args = parser.parse_args()
    print(json.dumps(save(args), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (Stop, OSError, ValueError) as exc:
        print("ERROR: " + str(exc), file=sys.stderr)
        raise SystemExit(2)
