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
DEFAULT_SAVE = "repository-cleanup"
COMMON_PATHS = ["README.md", "AGENTS.md"]
SAVE_PATHS = {"repository-cleanup": ["cleanup", "prompts", "tools", "map", "work.py"]}
SAVE_PATTERNS = {}
SECRET = re.compile(rb"(?:github_pat_|gh[pousr]_)[A-Za-z0-9_]{12,}|-----BEGIN [A-Z ]*PRIVATE KEY-----")
ROUTING = ("GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR", "GIT_INDEX_FILE",
           "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES",
           "GIT_IMPLICIT_WORK_TREE", "GIT_GRAFT_FILE", "GIT_SHALLOW_FILE",
           "GIT_PREFIX", "GIT_INTERNAL_SUPER_PREFIX")


class Stop(RuntimeError):
    pass


def token(path):
    values = set(re.findall(rb"(?:github_pat_|ghp_)[A-Za-z0-9_]{12,}", Path(path).read_bytes()))
    if len(values) != 1:
        raise Stop("Credential file must contain exactly one GitHub token.")
    return values.pop().decode()


def git(repo, *args, check=True):
    env = {k: v for k, v in os.environ.items() if k not in ROUTING}
    env["GIT_TERMINAL_PROMPT"] = "0"
    try:
        result = subprocess.run(["git", *args], cwd=repo, env=env,
                                capture_output=True, timeout=45)
    except subprocess.TimeoutExpired:
        raise Stop("Git timed out. Rerun the same command; local commits are retained.")
    if check and result.returncode:
        detail = SECRET.sub(b"[REDACTED]", result.stderr).decode(errors="replace")
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
        paths.append(("cleanup/workspaces/" + actor) if save == "repository-cleanup" else (archive_base + "/workspaces/" + actor))
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
    credential = args.token_file or os.environ.get("WCG_CHECKPOINT_TOKEN_FILE")
    if not credential:
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
    for p, spec in zip(paths, specs):
        if not (repo / p).exists() and not git(repo, "ls-files", "--", spec).stdout:
            raise Stop("Unknown checkpoint path: " + p)
    staged = set(names(git(repo, "diff", "--cached", "--name-only", "-z")))
    selected = set(names(git(repo, "diff", "--cached", "--name-only", "-z", "--", *specs)))
    if staged - selected:
        raise Stop("Staged files outside scope; include them explicitly or unstage them: " +
                   ", ".join(sorted(staged - selected)))
    changed = set(names(git(repo, "diff", "HEAD", "--name-only", "-z", "--", *specs)))
    changed.update(selected)
    changed.update(names(git(repo, "ls-files", "--others", "--exclude-standard", "-z", "--", *specs)))
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
    if changed:
        git(repo, "add", "-A", "--", *specs)
    # Deleted raw-source files have no newly introduced whitespace to check.
    git(repo, "diff", "--cached", "--check", "--no-renames", "--diff-filter=ACMR")
    files = names(git(repo, "diff", "--cached", "--name-only", "-z"))
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
                frozen=repo/"cleanup/sources.json"
                if frozen.is_file():
                    source_contract=json.loads(frozen.read_text())
                    anchor=source_contract.get("main_at_freeze")
                    if source_contract.get("target_branch")==branch and anchor:
                        if git(repo,"merge-base","--is-ancestor",anchor,private,check=False).returncode:
                            raise Stop("Frozen source anchor is not on current remote main")
                        git(repo,"update-ref",private,anchor)
                if git(repo, "merge-base", "--is-ancestor", private, head, check=False).returncode:
                    raise Stop("New branch must descend from its verified remote-main source anchor; local snapshot retained.")
            else:
                detail = SECRET.sub(b"[REDACTED]", before.stderr).decode(errors="replace").strip()[:500]
                if exists.returncode == 2:
                    detail = "Remote branch does not exist; first publication requires --create-branch."
                break
        baseline = value(repo, "rev-parse", private)
        commits, outgoing = audit_outgoing(repo, head, baseline, paths)
        result["outgoing_commits"] = list(dict.fromkeys(result["outgoing_commits"] + commits))
        result["outgoing_files"] = sorted(set(result["outgoing_files"]) | set(outgoing))
        result["files"] = sorted(set(result["files"]) | set(outgoing))
        result["assets"] = describe_assets(repo, record_dir, head, result["files"], branch)
        result["checked_head"] = head
        receipt.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
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
    args = parser.parse_args()
    print(json.dumps(save(args), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (Stop, OSError, ValueError) as exc:
        print("ERROR: " + str(exc), file=sys.stderr)
        raise SystemExit(2)
