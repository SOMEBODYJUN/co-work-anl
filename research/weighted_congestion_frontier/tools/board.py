#!/usr/bin/env python3
"""Equal-peer Git blackboard. Ordinary push + revalidation, never claim rebase.

The board is an append-only event stream on a dedicated branch. Claims reserve
small mathematical work units, not fields. They do not prohibit discussion or
independent attacks. All operations use temporary Git workspaces and leave the
caller's working tree untouched. UTC leases are cooperative, not job schedulers.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import tempfile
import time
import uuid

PREFIX = Path("research/weighted_congestion_frontier/board")
SCHEMA = 1
SECRET = re.compile(r"(?:github_pat_|gh[pousr]_)[A-Za-z0-9_]{12,}")
UUID = re.compile(r"[0-9a-f]{32}")
KINDS = {"discussion", "progress", "help", "objection", "review_request",
         "review", "barrier", "result", "handoff", "overlap"}
SCOPE = ("claim_version", "statement", "obligation", "mechanism")


class BoardError(Exception):
    pass


class Conflict(BoardError):
    pass


class ValidationError(BoardError):
    pass


def encode(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def guard(value):
    if SECRET.search(encode(value)):
        raise BoardError("Credential-like content cannot enter the public board.")


def fingerprint(body):
    # Mathematical symbols and claim IDs are case-sensitive (W is not w).
    scope = {key: " ".join(body[key].split()) for key in SCOPE}
    return hashlib.sha256(encode(scope).encode()).hexdigest()


def empty_state():
    return {"ideas": {}, "members": {}, "events": [], "last_time": 0}


def valid_id(value):
    if not isinstance(value, str) or not UUID.fullmatch(value):
        raise BoardError("Event and idea IDs must be 32 lowercase hex characters.")


def lease_length(body):
    seconds = body.get("lease_seconds", 3600)
    if type(seconds) is not int or not 60 <= seconds <= 10800:
        raise BoardError("Lease must be an integer between 60 and 10800 seconds.")
    return seconds


def require_owner(idea, event, active=True):
    if (idea.get("owner") != event["actor"] or
            idea.get("lease_token") != event["body"].get("lease_token")):
        raise Conflict("Current owner/token differs. Read the board before resuming.")
    if active and idea.get("lease_until", 0) <= event["time"]:
        raise Conflict("Lease expired. Claim again before changing its state.")


def transition(state, event):
    """Validate and apply one committed event; no mutating input on failure."""
    guard(event)
    valid_id(event["id"])
    if type(event["seq"]) is not int or event["seq"] != len(state["events"]) + 1:
        raise BoardError("Noncontiguous sequence; board history is invalid.")
    if (type(event["time"]) is not int or event["time"] < 0 or
            event.get("schema") != SCHEMA):
        raise BoardError("Invalid schema or event time.")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._/-]{0,100}", event["actor"]):
        raise BoardError("Use a globally unique simple team/member ID.")
    if any(old["id"] == event["id"] for old in state["events"]):
        raise BoardError("Duplicate event ID.")
    body, kind = event["body"], event["kind"]
    if not isinstance(body, dict):
        raise BoardError("Body must be an object.")
    if body.get("reply_to") and not any(
            old["id"] == body["reply_to"] for old in state["events"]):
        raise BoardError("reply_to is not an existing event.")
    out = copy.deepcopy(state)
    idea = out["ideas"].get(body.get("idea"))
    if kind == "register":
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*/[A-Za-z0-9][A-Za-z0-9._-]*", event["actor"]):
            raise BoardError("Registration needs a unique team/member ID.")
        members = out.setdefault("members", {})
        if event["actor"] in members:
            raise Conflict("Identity already registered; reuse it or choose a new session ID.")
        for key in ("runtime_id", "requested_model", "actual_model", "requested_effort", "actual_effort"):
            if (not isinstance(body.get(key), str) or not body[key].strip() or
                    len(body[key]) > 160 or "\n" in body[key] or "\r" in body[key]):
                raise BoardError("Identity needs bounded single-line runtime/model/effort fields.")
        if body.get("role") not in {"researcher", "paper_writer", "extractor", "deployment"}:
            raise BoardError("Unknown participation role.")
        budget = body.get("budget_seconds")
        if type(budget) is not int or not 1 <= budget <= 86400:
            raise BoardError("Reported work budget must be 1 to 86400 seconds.")
        parent = body.get("parent")
        if parent is not None:
            if (parent not in members or
                    parent.split("/")[0] != event["actor"].split("/")[0]):
                raise BoardError("Parent must be an already registered member of the same team.")
        members[event["actor"]] = dict(body, actor=event["actor"],
                                        registered_event=event["id"], registered_at=event["time"])
    elif kind == "propose":
        for key in ("title", "next_check", *SCOPE):
            if not isinstance(body.get(key), str) or not body[key].strip():
                raise BoardError("A proposal needs title, exact scope and next_check.")
        fp = fingerprint(body)
        duplicate = next((x for x in out["ideas"].values()
                          if x["fingerprint"] == fp), None)
        if duplicate:
            raise Conflict("This work unit is already public: " + duplicate["id"])
        idea = {key: body[key] for key in ("title", "next_check", *SCOPE)}
        idea.update(id=event["id"], fingerprint=fp, status="open",
                    proposer=event["actor"], owner=None, lease_token=None,
                    lease_until=0)
        out["ideas"][idea["id"]] = idea
        if body.get("claim"):
            idea.update(status="claimed", owner=event["actor"],
                        lease_token=event["id"],
                        lease_until=event["time"] + lease_length(body))
    elif kind in {"claim", "renew", "release", "finish"}:
        if idea is None:
            raise BoardError("Unknown idea.")
        if kind == "claim":
            if idea["status"] == "done":
                raise Conflict("This work unit is concluded; propose a distinct obligation.")
            if idea.get("owner") and idea["lease_until"] > event["time"]:
                raise Conflict("Already claimed by " + idea["owner"])
            if not isinstance(body.get("next_check"), str) or not body["next_check"].strip():
                raise BoardError("Claim needs a concrete next_check.")
            idea.update(status="claimed", owner=event["actor"],
                        lease_token=event["id"], next_check=body["next_check"],
                        lease_until=event["time"] + lease_length(body))
        else:
            require_owner(idea, event, active=kind != "release")
            if kind == "renew":
                idea["lease_until"] = event["time"] + lease_length(body)
                if body.get("next_check"):
                    idea["next_check"] = body["next_check"]
            else:
                if not isinstance(body.get("text"), str) or not body["text"].strip():
                    raise BoardError("Release/finish needs a useful conclusion or handoff.")
                if kind == "finish" and not body.get("asset"):
                    raise BoardError("Finish needs a pushed, frozen asset.")
                idea.update(status="done" if kind == "finish" else "open",
                            owner=None, lease_token=None, lease_until=0)
    elif kind in KINDS:
        if not isinstance(body.get("text"), str) or not body["text"].strip():
            raise BoardError("Messages need useful text.")
        if body.get("idea") and idea is None:
            raise BoardError("Unknown related idea.")
        if kind == "result" and not body.get("asset"):
            raise BoardError("Result needs a pushed, frozen asset.")
        # An objection/result never edits ownership or upgrades a theorem.
    else:
        raise BoardError("Unknown event kind: " + str(kind))
    out["events"].append(copy.deepcopy(event))
    out["last_time"] = event["time"]
    return out


def git(cwd, *args, check=True, timeout=45):
    env = os.environ.copy()
    # Scratch Git commands must never inherit the caller's index/worktree/object
    # overrides. Keep authentication (e.g. GIT_ASKPASS), not repository routing.
    for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR", "GIT_INDEX_FILE",
                "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES",
                "GIT_IMPLICIT_WORK_TREE", "GIT_GRAFT_FILE", "GIT_SHALLOW_FILE",
                "GIT_PREFIX", "GIT_INTERNAL_SUPER_PREFIX"):
        env.pop(key, None)
    env["GIT_TERMINAL_PROMPT"] = "0"
    try:
        result = subprocess.run(["git", *args], cwd=cwd, env=env,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        raise BoardError("Git timed out; recover using the saved event ID.") from exc
    if check and result.returncode:
        # Origins with embedded credentials are refused at client construction.
        detail = SECRET.sub("[REDACTED]", result.stderr.decode(errors="replace"))
        raise BoardError("Git operation failed: " + detail.strip()[:1000])
    return result


def utc(value):
    return time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(value))


def retry_pause(event_id, attempt):
    jitter = int(hashlib.sha256(
        f"{event_id}:{attempt}".encode()).hexdigest()[:4], 16) / 65535
    time.sleep(min(0.5, 0.03 * 2 ** min(attempt, 4)) * (0.5 + jitter))


def render(state, now):
    lines = ["# 平等解题公屏", "",
             "所有成员自行提出、认领、分享和回应。没有派单者。",
             "认领只防相同推进单元重复；补充、异议和独立审查始终开放。",
             "时间租约请按下列 UTC 截止检查；当前状态以 board.py view 为准。", "",
             "完整协议和工具在 main 的 research/weighted_congestion_frontier/。",
             "这里只保存交流，不自动成为数学 canonical state。", ""]
    if state.get("members"):
        lines += ["## 已登记身份", "",
                  "模型和运行身份由发布者如实登记；这是署名与来源追踪，不是独立账号认证。",
                  "登记不表示成员仍在线，不会启动 agent 或延长运行时间。", "",
                  "| Actor | 参与入口 | Runtime | 实际模型 / effort | 父成员 | 登记时间 |",
                  "| --- | --- | --- | --- | --- | --- |"]
        def cell(value):
            return str(value).replace("|", r"\|").replace("\n", " ")
        for member in state["members"].values():
            fields = [member["actor"], member["role"], member["runtime_id"],
                      member["actual_model"] + " / " + member["actual_effort"],
                      member.get("parent", "—"), utc(member["registered_at"])]
            lines.append("| " + " | ".join(cell(v) for v in fields) + " |")
        lines.append("")
    lines += [
             "## Ideas", "",
             "| ID | 具体 idea | 状态 | 当前 owner | 租约截止 |",
             "| --- | --- | --- | --- | --- |"]
    for idea in state["ideas"].values():
        title = idea["title"].replace("|", r"\|").replace("\n", " ")
        status = idea["status"]
        if idea.get("owner") and idea["lease_until"] <= now:
            status = "expired / 可接替"
        deadline = utc(idea["lease_until"]) if idea["lease_until"] else "—"
        lines.append(f"| {idea['id']} | {title} | {status} | "
                     f"{idea.get('owner') or '—'} | {deadline} |")
    lines += ["", "## 最近消息", ""]
    for event in state["events"][-30:]:
        path = f"events/{event['seq']:08d}_{event['id']}.json"
        lines += [f"### {event['seq']} · {event['actor']} · {event['kind']}",
                  "", f"[完整事件]({path}) · {utc(event['time'])}", ""]
        body = event["body"]
        if event["kind"] == "register":
            lines += ["登记身份：" + event["actor"], "", encode(body).strip(), ""]
        elif event["kind"] == "propose":
            lines += [body["title"], "", "命题：" + body["statement"], "",
                      "义务：" + body["obligation"], "",
                      "机制：" + body["mechanism"], "",
                      "下一检验：" + body["next_check"], ""]
        else:
            lines += [body.get("text", body.get("next_check", "")), ""]
        if body.get("asset"):
            lines += ["冻结资产：" + encode(body["asset"]).strip(), ""]
    return "\n".join(lines) + "\n"


class Board:
    def __init__(self, repo, branch="wcg/board", retries=20, clock=time.time):
        if type(retries) is not int or not 1 <= retries <= 50:
            raise BoardError("Retry budget must be an integer from 1 to 50.")
        self.repo = Path(git(repo, "rev-parse", "--show-toplevel").stdout.decode().strip())
        self.remote = git(self.repo, "remote", "get-url", "origin").stdout.decode().strip()
        if SECRET.search(self.remote) or re.search(r"https?://[^/]*@", self.remote):
            raise BoardError("Origin must not embed a credential.")
        git(self.repo, "check-ref-format", "refs/heads/" + branch)
        self.branch, self.retries, self.clock = branch, retries, clock
        common = git(self.repo, "rev-parse", "--git-common-dir").stdout.decode().strip()
        self.cache = (self.repo / common).resolve() / "wcg"
        self.cache.mkdir(parents=True, exist_ok=True)
        # Separate outboxes if one clone intentionally uses different board branches.
        namespace = hashlib.sha256(branch.encode()).hexdigest()[:12]
        self.outbox = self.cache / namespace
        self.outbox.mkdir(exist_ok=True)

    def scratch(self):
        return tempfile.TemporaryDirectory(prefix="board-", dir=self.cache)

    def setup(self, directory):
        git(directory, "init", "--quiet")
        git(directory, "config", "user.name", "WCG Researcher")
        git(directory, "config", "user.email", "wcg@users.noreply.github.com")
        git(directory, "remote", "add", "origin", self.remote)

    def load(self, directory):
        git(directory, "fetch", "--quiet", "--no-tags", "--depth=1",
            "origin", "refs/heads/" + self.branch)
        git(directory, "checkout", "--quiet", "--detach", "FETCH_HEAD")
        meta_path = Path(directory) / PREFIX / "meta.json"
        if not meta_path.exists() or json.loads(meta_path.read_text()) != {"schema": SCHEMA}:
            raise BoardError("Board is not initialized with the supported schema.")
        state = empty_state()
        files = sorted((Path(directory) / PREFIX / "events").glob("*.json"))
        for path in files:
            event = json.loads(path.read_text())
            expected = f"{event['seq']:08d}_{event['id']}.json"
            if path.name != expected:
                raise BoardError("Event filename/sequence mismatch.")
            state = transition(state, event)
        return state

    def initialize(self):
        # Only create a new branch. Never overwrite an existing branch.
        found = git(self.repo, "ls-remote", "--exit-code", "origin",
                    "refs/heads/" + self.branch, check=False)
        if found.returncode == 0:
            self.read()
            return "already initialized"
        if found.returncode != 2:
            raise BoardError("Cannot establish whether board branch exists.")
        with self.scratch() as directory:
            self.setup(directory)
            root = Path(directory) / PREFIX
            root.mkdir(parents=True)
            (root / "meta.json").write_text(encode({"schema": SCHEMA}))
            (root / "README.md").write_text(
                "# GitHub 公屏\n\n[实时 Ideas 和交流](BOARD.md)。\n\n"
                "所有团队使用 main 分支的 tools/board.py。自主认领，不等待派单。\n")
            (root / "BOARD.md").write_text(render(empty_state(), int(self.clock())))
            git(directory, "add", ".")
            git(directory, "commit", "--quiet", "-m", "Initialize equal-peer WCG board")
            pushed = git(directory, "push", "--quiet", "origin",
                         "HEAD:refs/heads/" + self.branch, check=False)
            if pushed.returncode:
                self.read()  # A concurrent initializer may have won; validate it.
            else:
                self.read()  # Verify the remote, not only the local push response.
        return "initialized"

    def read(self):
        with self.scratch() as directory:
            self.setup(directory)
            return self.load(directory)

    def check_asset(self, asset):
        required = {"branch", "commit", "path", "sha256"}
        if not isinstance(asset, dict) or set(asset) != required:
            raise ValidationError("Asset needs exactly branch, commit, path and sha256.")
        git(self.repo, "check-ref-format", "refs/heads/" + asset["branch"])
        if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", asset["commit"]):
            raise ValidationError("Use a full immutable commit ID.")
        path = PurePosixPath(asset["path"])
        if path.is_absolute() or ".." in path.parts or not path.parts or ":" in str(path):
            raise ValidationError("Asset path must be repository-relative.")
        if not re.fullmatch(r"[0-9a-f]{64}", asset["sha256"]):
            raise ValidationError("Use a full SHA-256 digest.")
        # Validate in isolation: FETCH_HEAD of the user's research repo is untouched.
        with self.scratch() as directory:
            self.setup(directory)
            git(directory, "fetch", "--quiet", "--no-tags", "origin",
                "refs/heads/" + asset["branch"])
            ancestor = git(directory, "merge-base", "--is-ancestor",
                           asset["commit"], "FETCH_HEAD", check=False)
            if ancestor.returncode:
                raise ValidationError("Asset commit is not on the named remote branch.")
            object_id = asset["commit"] + ":" + str(path)
            if git(directory, "cat-file", "-t", object_id).stdout.strip() != b"blob":
                raise ValidationError("Asset must name a file, not a directory/tree.")
            content = git(directory, "cat-file", "blob", object_id).stdout
            if hashlib.sha256(content).hexdigest() != asset["sha256"]:
                raise ValidationError("Asset hash disagrees with the pushed frozen file.")

    def publish(self, intent):
        guard(intent)
        valid_id(intent["id"])
        pending = self.outbox / (intent["id"] + ".json")
        # Atomic create before networking. Another same-ID retry may remove a
        # confirmed intent between any two operations; handle that normally.
        while True:
            try:
                saved = json.loads(pending.read_text())
            except FileNotFoundError:
                saved = None
            if saved is not None:
                if saved != intent:
                    raise BoardError("An event ID cannot be reused for changed content.")
                break
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8",
                                             dir=self.outbox, delete=False) as f:
                temporary = Path(f.name)
                f.write(encode(intent))
                f.flush()
                os.fsync(f.fileno())
            try:
                try:
                    os.link(temporary, pending)
                except FileExistsError:
                    continue  # Read again; the winner may already have removed it.
            finally:
                temporary.unlink(missing_ok=True)
            break
        error = None
        for attempt in range(self.retries):
            try:
                with self.scratch() as directory:
                    self.setup(directory)
                    state = self.load(directory)
                    existing = next((e for e in state["events"]
                                     if e["id"] == intent["id"]), None)
                    if existing:
                        core = {k: existing[k] for k in ("id", "actor", "kind", "body")}
                        if core != intent:
                            raise Conflict("Remote event ID belongs to different content.")
                        pending.unlink(missing_ok=True)
                        return existing
                    # Recover committed receipts even if asset branches vanished.
                    if intent["body"].get("asset"):
                        self.check_asset(intent["body"]["asset"])
                    event = dict(intent, schema=SCHEMA, seq=len(state["events"]) + 1,
                                 time=int(self.clock()))
                    try:
                        updated = transition(state, event)
                    except Conflict:
                        raise
                    except BoardError as exc:
                        raise ValidationError(str(exc)) from exc
                    root = Path(directory) / PREFIX
                    events = root / "events"
                    events.mkdir(exist_ok=True)
                    (events / f"{event['seq']:08d}_{event['id']}.json").write_text(encode(event))
                    (root / "BOARD.md").write_text(render(updated, event["time"]))
                    git(directory, "add", str(PREFIX))
                    git(directory, "commit", "--quiet", "-m",
                        f"board: {event['actor']} {event['kind']} {event['id']}")
                    # Never rebase a rejected event. Every retry loads latest state.
                    git(directory, "push", "--quiet", "origin",
                        "HEAD:refs/heads/" + self.branch)
                    # A lost response is handled by the same stable event ID.
                    confirmed = self.read()
                    found = next((e for e in confirmed["events"]
                                  if e["id"] == intent["id"]), None)
                    if found:
                        pending.unlink(missing_ok=True)
                        return found
                    raise BoardError("Remote confirmation missing; event remains pending.")
            except (Conflict, ValidationError):
                raise
            except BoardError as exc:
                error = exc
                # Small, bounded, event-specific jitter prevents busy peers
                # repeatedly colliding in lockstep. Every retry still reloads
                # and revalidates; this is network backoff, not work padding.
                if attempt + 1 < self.retries:
                    retry_pause(intent["id"], attempt)
        raise BoardError(f"{error} Pending event ID: {intent['id']}")


def make_intent(actor, kind, body, event_id=None):
    return {"id": event_id or uuid.uuid4().hex, "actor": actor,
            "kind": kind, "body": body}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".")
    parser.add_argument("--branch", default="wcg/board")
    parser.add_argument("--retries", type=int, default=20,
                        help="Bounded publish retry budget (1 to 50); failed intents remain recoverable")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    view = sub.add_parser("view")
    view.add_argument("--json", action="store_true")
    sub.add_parser("pending")
    register = sub.add_parser("register", help="Publish a self-reported, collision-checked member identity")
    register.add_argument("--actor", help="Unique team/member; omitted generates a fresh team/root")
    register.add_argument("--event-id")
    register.add_argument("--parent", help="Already registered same-team parent for a real child agent")
    register.add_argument("--role", choices=("researcher", "paper_writer", "extractor", "deployment"), default="researcher")
    register.add_argument("--runtime-id", required=True)
    register.add_argument("--requested-model", default="unspecified")
    register.add_argument("--actual-model", default="unknown")
    register.add_argument("--requested-effort", default="unspecified")
    register.add_argument("--actual-effort", default="unknown")
    register.add_argument("--budget-seconds", type=int, default=3600)
    for command in ("retry", "discard"):
        p = sub.add_parser(command)
        p.add_argument("--event-id", required=True)
    propose = sub.add_parser("propose")
    propose.add_argument("--actor", required=True)
    propose.add_argument("--event-id")
    for field in ("title", "claim-version", "statement", "obligation", "mechanism", "next-check"):
        propose.add_argument("--" + field, required=True)
    propose.add_argument("--claim", action="store_true")
    propose.add_argument("--lease-seconds", type=int, default=3600)
    for command in ("claim", "renew", "release", "finish", "say"):
        p = sub.add_parser(command)
        p.add_argument("--actor", required=True)
        p.add_argument("--event-id")
        p.add_argument("--idea", required=command != "say")
        if command in ("renew", "release", "finish"):
            p.add_argument("--lease-token", required=True)
        if command in ("claim", "renew"):
            p.add_argument("--next-check", required=command == "claim")
            p.add_argument("--lease-seconds", type=int, default=3600)
        if command in ("release", "finish", "say"):
            p.add_argument("--text", required=True)
            p.add_argument("--asset-json", help="Path to frozen asset JSON descriptor")
        if command == "say":
            p.add_argument("--kind", choices=sorted(KINDS), default="discussion")
            p.add_argument("--reply-to")
    args = parser.parse_args()
    client = Board(args.repo, args.branch, retries=args.retries)
    if args.command == "init":
        print(client.initialize())
    elif args.command == "view":
        state = client.read()
        print(encode(state) if args.json else render(state, int(client.clock())), end="")
    elif args.command == "pending":
        print(encode([p.stem for p in sorted(client.outbox.glob("*.json"))]), end="")
    elif args.command in ("retry", "discard"):
        valid_id(args.event_id)
        path = client.outbox / (args.event_id + ".json")
        if args.command == "discard":
            path.unlink(missing_ok=True)
            print("Local pending intent discarded; no remote history changed.")
        else:
            try:
                saved = json.loads(path.read_text())
            except FileNotFoundError:
                saved = None  # Concurrent retry may have confirmed and removed it.
            if saved is not None:
                print(encode(client.publish(saved)), end="")
            else:
                found = next((e for e in client.read()["events"]
                              if e["id"] == args.event_id), None)
                if found is None:
                    raise BoardError("No pending or remote event with that ID.")
                print(encode(found), end="")
    else:
        data = vars(args)
        excluded = {"repo", "branch", "retries", "command", "actor", "event_id",
                    "kind", "asset_json"}
        body = {k: v for k, v in data.items() if k not in excluded and v is not None}
        if data.get("asset_json"):
            body["asset"] = json.loads(Path(args.asset_json).read_text())
        kind = args.kind if args.command == "say" else args.command
        actor = args.actor
        if args.command == "register" and actor is None:
            actor = "wcg_" + uuid.uuid4().hex + "/root"
        event = client.publish(make_intent(actor, kind, body, args.event_id))
        print(encode(event), end="")


if __name__ == "__main__":
    try:
        main()
    except (BoardError, ValueError, KeyError, TypeError) as exc:
        print("ERROR: " + str(exc), file=__import__("sys").stderr)
        raise SystemExit(2)
