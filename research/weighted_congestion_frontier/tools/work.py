#!/usr/bin/env python3
"""Start and operate one Work conversation using its role number and token file."""
from __future__ import annotations

import argparse
import contextlib
import fcntl
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import tempfile
import uuid

REMOTE = "https://github.com/SOMEBODYJUN/co-work-anl.git"
TOOLS = "research/weighted_congestion_frontier/tools"
TOKEN = re.compile(rb"(?:github_pat_|ghp_)[A-Za-z0-9_]{12,}")
SECRET = re.compile(rb"(?:github_pat_|gh[pousr]_)[A-Za-z0-9_]{12,}")
ROUTING = {"GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR", "GIT_INDEX_FILE",
           "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES",
           "GIT_IMPLICIT_WORK_TREE", "GIT_GRAFT_FILE", "GIT_SHALLOW_FILE",
           "GIT_PREFIX", "GIT_INTERNAL_SUPER_PREFIX"}
_ASKPASS_DIRECTORIES = []


class Stop(RuntimeError):
    pass


def credential(path):
    tokens = set(TOKEN.findall(Path(path).read_bytes()))
    if len(tokens) != 1:
        raise Stop("凭据 txt 应包含一个 GitHub PAT。")
    return tokens.pop().decode()


def environment(path=None):
    env = {k: v for k, v in os.environ.items() if k not in ROUTING}
    env["GIT_TERMINAL_PROMPT"] = "0"
    if path:
        credential(path)
        base = Path.cwd()
        local = subprocess.run(["git", "rev-parse", "--git-common-dir"],
                               env=env, capture_output=True, timeout=5)
        if local.returncode == 0:
            base = (base / local.stdout.decode().strip()).resolve()
        directory = tempfile.TemporaryDirectory(prefix=".wcg-askpass-", dir=base)
        _ASKPASS_DIRECTORIES.append(directory)
        helper = Path(directory.name) / "askpass"
        helper.write_text("#!/bin/sh\nexec " + shlex.join(
            [sys.executable, str(Path(__file__).resolve())]) + ' "$@"\n')
        helper.chmod(0o700)
        env.update(GIT_ASKPASS=str(helper),
                   WCG_WORK_ASKPASS="1", WCG_CHECKPOINT_TOKEN_FILE=str(path))
    return env


def run(repo, *args, env=None, check=True):
    try:
        r = subprocess.run(["git", *args], cwd=repo, env=env or environment(),
                           capture_output=True, timeout=45)
    except subprocess.TimeoutExpired as exc:
        raise Stop("Git 超时；本地工作已保留，可重试同一命令。") from exc
    if check and r.returncode:
        detail = SECRET.sub(b"[REDACTED]", r.stderr).decode(errors="replace")
        raise Stop(detail.strip()[:1200])
    return r


def value(repo, *args, env=None):
    return run(repo, *args, env=env).stdout.decode().strip()


def default_repo():
    # The exact same file works both inside a clone and as an uploaded program.
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / TOOLS / "work.py") == p and (parent / ".git").exists():
            return str(parent)
    return str(Path.cwd() / "co-work-anl")


def checked_repo(path):
    repo = Path(path).resolve()
    if not repo.is_dir() or not (repo / ".git").exists():
        raise Stop("先执行 start 恢复这个工作目录。")
    actual = Path(value(repo, "rev-parse", "--show-toplevel")).resolve()
    if actual != repo:
        raise Stop("--repo 应指向仓库根目录。")
    return repo


def auth(repo, args):
    supplied = getattr(args, "token_file", None)
    path = supplied or run(repo, "config", "--local", "--get", "wcg.tokenFile",
                           check=False).stdout.decode().strip()
    if path:
        path = Path(path).expanduser().resolve()
        if path.is_relative_to(repo):
            raise Stop("凭据文件请放在仓库外。")
        credential(path)
        if supplied:
            run(repo, "config", "--local", "wcg.tokenFile", str(path))
    return environment(path)


def actor(repo, requested=None):
    saved = run(repo, "config", "--local", "--get", "wcg.actor", check=False).stdout.decode().strip()
    # A caller may pin a role without putting it in the command line.  This is
    # useful for an explicitly assigned research lead while preserving the
    # historical random fallback for ordinary sessions.
    requested_from_env = os.environ.get("WCG_ACTOR", "").strip()
    chosen = requested or requested_from_env or saved or ("W" + uuid.uuid4().hex[:12])
    if not chosen or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,63}", chosen):
        raise Stop("start --actor 使用提示词里的角色号，例如 001 或 R1。")
    if saved and saved != chosen:
        raise Stop("这个工作目录使用角色号 " + saved + "；新对话请使用自己的目录。")
    if not saved:
        run(repo, "config", "--local", "wcg.actor", chosen)
    return chosen


@contextlib.contextmanager
def write_lock(repo):
    common = Path(value(repo, "rev-parse", "--git-common-dir"))
    common = (repo / common).resolve()
    cache = common / "wcg-checkpoint"
    cache.mkdir(exist_ok=True)
    with (cache / "writer.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise Stop("这个工作目录正在提交，操作完成后重试。") from exc
        yield


def sync(repo, env):
    with write_lock(repo):
        for item in ("MERGE_HEAD", "CHERRY_PICK_HEAD", "REVERT_HEAD", "rebase-merge", "rebase-apply"):
            p = Path(value(repo, "rev-parse", "--git-path", item))
            if ((repo / p).resolve()).exists():
                raise Stop("请先处理已有 Git 操作：" + item)
        if run(repo, "ls-files", "-u").stdout:
            raise Stop("请先处理现有文件冲突；本地内容和同步备份仍保留。")
        run(repo, "fetch", "--quiet", "--no-tags", "origin",
            "+refs/heads/main:refs/remotes/origin/main", env=env)
        tip = value(repo, "rev-parse", "origin/main")
        if run(repo, "merge-base", "--is-ancestor", tip, "HEAD", check=False).returncode == 0:
            return {"status": "synced", "main": tip, "preserved_work": True}
        stash = None
        if run(repo, "status", "--porcelain").stdout:
            run(repo, "stash", "push", "--quiet", "--include-untracked", "-m", "work sync " + uuid.uuid4().hex)
            stash = value(repo, "rev-parse", "refs/stash")
        merged = run(repo, "-c", "user.name=WCG Researcher", "-c",
                     "user.email=wcg@users.noreply.github.com", "merge", "--no-edit", tip, check=False)
        if merged.returncode:
            run(repo, "merge", "--abort", check=False)
        restored = None
        if stash:
            restored = run(repo, "stash", "apply", "--index", stash, check=False)
            if restored.returncode == 0:
                # Remove only our own saved copy after every byte was reapplied.
                if value(repo, "rev-parse", "refs/stash") == stash:
                    run(repo, "stash", "drop", "--quiet", "stash@{0}")
            else:
                raise Stop("同步后恢复遇到文件冲突；本地内容和完整备份 " + stash + " 均保留。")
        if merged.returncode:
            raise Stop("main 有真实文件冲突；合并已撤回，本地成果已恢复。")
        return {"status": "synced", "main": tip, "preserved_work": True}


def start(args):
    repo = Path(args.repo).expanduser().resolve()
    if not (repo / ".git").exists():
        if repo.exists() and any(repo.iterdir()):
            raise Stop("目标目录有其他文件；请为仓库指定空目录。")
        path = Path(args.token_file).expanduser().resolve() if args.token_file else None
        if path and path.is_relative_to(repo):
            raise Stop("凭据文件请放在仓库外。")
        env = environment(path)
        repo.parent.mkdir(parents=True, exist_ok=True)
        remote = args.remote
        if SECRET.search(remote.encode()) or re.search(r"https?://[^/]*@", remote):
            raise Stop("仓库地址请使用普通 Git URL。")
        run(repo.parent, "clone", "--quiet", "--single-branch", "--branch", "main", remote, str(repo), env=env)
    repo = checked_repo(repo)
    origin = value(repo, "remote", "get-url", "--all", "origin")
    push_origin = value(repo, "remote", "get-url", "--push", "--all", "origin")
    if origin != args.remote or push_origin != origin:
        raise Stop("目标目录的 origin 与本研究仓库不一致；请使用本研究的独立目录。")
    env = auth(repo, args)
    who = actor(repo, args.actor)
    if not run(repo, "config", "--local", "--get", "user.name", check=False).stdout:
        run(repo, "config", "--local", "user.name", "WCG " + who)
    if not run(repo, "config", "--local", "--get", "user.email", check=False).stdout:
        run(repo, "config", "--local", "user.email", "wcg@users.noreply.github.com")
    branch = value(repo, "symbolic-ref", "--quiet", "--short", "HEAD")
    if branch == "wcg/board":
        raise Stop("请在研究工作目录中执行 start。")
    if branch != "main" and not branch.startswith("wcg/work/"):
        raise Stop("当前分支不是 main 或旧研究工作分支；请先保存并处理这个独立主题。")
    result = sync(repo, env)
    if branch != "main":
        # sync has already preserved staged/unstaged/untracked work and stopped
        # on any real conflict. Keep any existing local main under a local ref
        # before renaming the old work branch. No remote branch is created.
        with write_lock(repo):
            previous = run(repo, "rev-parse", "--verify", "refs/heads/main", check=False)
            if previous.returncode == 0:
                run(repo, "update-ref", "refs/wcg/recovery/main-" + uuid.uuid4().hex,
                    previous.stdout.decode().strip())
            run(repo, "branch", "-M", "main")
    result.update(actor=who, repo=str(repo), branch=value(repo, "branch", "--show-current"))
    print(json.dumps(result, ensure_ascii=False), flush=True)
    return board(repo, env, "view", [])


def board(repo, env, command, extra):
    path = repo / TOOLS / "board.py"
    if not path.is_file():
        raise Stop("仓库缺少公屏程序；请运行 sync 更新程序。")
    return subprocess.call([sys.executable, str(path), "--repo", str(repo), command, *extra], env=env)


def main():
    if os.environ.get("WCG_WORK_ASKPASS") == "1" and len(sys.argv) == 2:
        if sys.argv[1].startswith("Username"):
            print("x-access-token")
            return 0
        if sys.argv[1].startswith("Password"):
            print(credential(os.environ["WCG_CHECKPOINT_TOKEN_FILE"]))
            return 0
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", default=default_repo())
    p.add_argument("--token-file")
    sub = p.add_subparsers(dest="command", required=True)
    s = sub.add_parser("start", help="恢复项目，固定角色号，同步并读取公屏")
    s.add_argument("--actor", help="可选；省略时为本对话生成并记住唯一发布标识")
    s.add_argument("--token-file", default=argparse.SUPPRESS)
    s.add_argument("--remote", default=REMOTE)
    sub.add_parser("sync", help="同步 main 并保留本地工作")
    r = sub.add_parser("read", help="读取异步公屏")
    r.add_argument("--json", action="store_true")
    s = sub.add_parser("send", help="署名发言，回复和资产引用均可选")
    text = s.add_mutually_exclusive_group(required=True)
    text.add_argument("--text")
    text.add_argument("--text-file")
    for name in ("thread", "reply-to", "asset-json", "kind", "event-id"):
        s.add_argument("--" + name)
    c = sub.add_parser("checkpoint", help="立即保存阶段资产并推送")
    c.add_argument("paths", nargs="*")
    c.add_argument("-m", "--message")
    sub.add_parser("pending", help="查看待发送消息")
    r = sub.add_parser("retry", help="以原消息 ID 重试发送")
    r.add_argument("event_id")
    r = sub.add_parser("discard", help="删除一条未发送的本地草稿")
    r.add_argument("event_id")
    a = p.parse_args()
    if a.command == "start":
        return start(a)
    repo = checked_repo(a.repo)
    env = auth(repo, a)
    who = actor(repo)
    if a.command == "sync":
        print(json.dumps(sync(repo, env), ensure_ascii=False))
        return 0
    if a.command == "read":
        return board(repo, env, "view", ["--json"] if a.json else [])
    if a.command == "send":
        extra = ["--actor", who]
        for name in ("text", "text_file", "thread", "reply_to", "asset_json", "kind", "event_id"):
            v = getattr(a, name)
            if v is not None:
                extra += ["--" + name.replace("_", "-"), v]
        return board(repo, env, "say", extra)
    if a.command in ("pending", "retry", "discard"):
        return board(repo, env, a.command, ["--event-id", a.event_id] if a.command != "pending" else [])
    if a.command == "checkpoint":
        command = [sys.executable, str(repo / TOOLS / "checkpoint.py"), "--repo", str(repo), *a.paths]
        if a.message:
            command += ["-m", a.message]
        return subprocess.call(command, env=env)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Stop, OSError, ValueError) as exc:
        message = SECRET.sub(b"[REDACTED]", str(exc).encode()).decode()
        print("ERROR: " + message, file=sys.stderr)
        raise SystemExit(2)
