#!/usr/bin/env python3
"""Restore one research conversation, collaborate, and checkpoint its own archive."""
from __future__ import annotations

import argparse
import contextlib
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import signal
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import uuid

REMOTE = "https://github.com/SOMEBODYJUN/co-work-anl.git"
TOOLS = "tools"
DEFAULT_SAVE = "customer-attraction"
DEFAULT_BRANCH = "rebuild/research-v2"
START_COMMAND = "__wcg_start_v1__"
START_RECEIPT = "WCG_START_HANDOFF_V1"
# Stable launcher inputs, independent of the public CLI and its defaults.
START_FIELDS = ("remote", "branch", "actor", "save", "role", "subarchive",
                "resume", "adopt_legacy", "token_file", "auth", "create_archive")
TRANSFER_TIMEOUT = 600
ROLE_PROMPTS = {"boss": "prompts/research-runtime.md"}
IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,63}")
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


def environment(path=None, mode='token'):
    env = {k: v for k, v in os.environ.items() if k not in ROUTING}
    env["GIT_TERMINAL_PROMPT"] = "0"
    if mode=='ssh':
        for key in ('GIT_ASKPASS','WCG_WORK_ASKPASS','WCG_CHECKPOINT_ASKPASS','WCG_CHECKPOINT_TOKEN_FILE'):
            env.pop(key,None)
        env.setdefault('GIT_SSH_COMMAND','ssh -o BatchMode=yes')
        return env
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
        count=int(env.get('GIT_CONFIG_COUNT','0'));env['GIT_CONFIG_COUNT']=str(count+1)
        env['GIT_CONFIG_KEY_'+str(count)]='credential.helper';env['GIT_CONFIG_VALUE_'+str(count)]=''
    return env


def run(repo, *args, env=None, check=True, timeout=45):
    command = ["git", *args]
    with subprocess.Popen(command, cwd=repo, env=env or environment(),
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          start_new_session=True) as process:
        try:
            stdout, stderr = process.communicate(timeout=timeout)
        except (subprocess.TimeoutExpired, KeyboardInterrupt) as exc:
            with contextlib.suppress(ProcessLookupError):
                os.killpg(process.pid, signal.SIGKILL)
            process.communicate()
            if isinstance(exc, KeyboardInterrupt):
                raise
            raise Stop(f"Git {args[0]} 在 {timeout} 秒后超时；本地工作已保留，可重试同一命令。") from exc
        r = subprocess.CompletedProcess(command, process.returncode, stdout, stderr)
    if check and r.returncode:
        detail = SECRET.sub(b"[REDACTED]", r.stderr).decode(errors="replace")
        raise Stop(detail.strip()[:1200])
    return r


def value(repo, *args, env=None):
    return run(repo, *args, env=env).stdout.decode().strip()


def checked_branch(repo, name):
    if (not name or name.startswith("-") or name == "HEAD"
            or SECRET.search(name.encode())
            or run(repo, "check-ref-format", "refs/heads/" + name,
                   check=False).returncode):
        raise Stop("分支名不合法。")
    if name == "wcg/board" or name.startswith("wcg/board-"):
        raise Stop("公屏分支不能用作研究文件分支。")
    return name


def branch_id(repo, requested=None):
    saved = local_config(repo, "wcg.branch")
    current = value(repo, "branch", "--show-current")
    fallback = DEFAULT_BRANCH if current == DEFAULT_BRANCH else "main"
    chosen = checked_branch(repo, requested or saved or fallback)
    if saved and requested and chosen != saved:
        raise Stop("本clone已绑定文件分支 " + saved + "；其他分支使用独立clone。")
    return chosen


def local_config(repo, key):
    return run(repo, "config", "--local", "--get", key, check=False).stdout.decode().strip()


def default_repo():
    # The exact same file works both inside a clone and as an uploaded program.
    p = Path(__file__).resolve()
    for parent in p.parents:
        if ((parent / "work.py") == p or (parent / TOOLS / "work.py") == p) and (parent / ".git").exists():
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


def auth(repo, args, *, bind=True):
    mode = args.auth or local_config(repo, "wcg.auth") or "token"
    path = (args.token_file or local_config(repo, "wcg.tokenFile")) if mode == "token" else None
    if path:
        path = Path(path).expanduser().resolve()
        if path.is_relative_to(repo):
            raise Stop("凭据文件请放在仓库外。")
    env = environment(path, mode=mode)
    if bind:
        bind_auth(repo, args, mode)
    return env


def bind_auth(repo, args, mode):
    if args.auth:
        run(repo, "config", "--local", "wcg.auth", args.auth)
    if mode == "token" and args.token_file:
        run(repo, "config", "--local", "wcg.tokenFile", str(Path(args.token_file).expanduser().resolve()))


def actor(repo, requested=None, adopt_legacy=False, *, bind=True):
    saved = local_config(repo, "wcg.actor")
    # A caller may pin a role without putting it in the command line.  This is
    # useful for an explicitly assigned research lead while preserving the
    # historical random fallback for ordinary sessions.
    requested_from_env = os.environ.get("WCG_ACTOR", "").strip()
    chosen = requested if requested is not None else (requested_from_env or saved)
    if not chosen or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,63}", chosen):
        raise Stop('首次启动必须按提示词给出 --actor Boss编号；程序不再随机分配身份。')
    if saved and saved != chosen:
        if not (adopt_legacy and re.fullmatch(r"R-[0-9a-f]{32}", saved)
                and re.fullmatch(r"Boss[1-9][0-9]*", chosen)):
            raise Stop("本目录已绑定 " + saved + "；同一旧对话迁移需明确 --adopt-legacy，其他对话用独立 clone。")
        if bind:
            run(repo, "config", "--local", "wcg.legacyActor", saved)
    if bind and saved != chosen:
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


def sync(repo, env, allow_legacy=False, target=None):
    with write_lock(repo):
        target = branch_id(repo, target)
        branch = value(repo, "branch", "--show-current")
        if branch != target and not (allow_legacy and target == "main" and branch.startswith("wcg/work/")):
            raise Stop("当前分支与绑定分支 " + target + " 不同；保留本地工作，不自动切换。")
        for item in ("MERGE_HEAD", "CHERRY_PICK_HEAD", "REVERT_HEAD", "rebase-merge", "rebase-apply"):
            p = Path(value(repo, "rev-parse", "--git-path", item))
            if ((repo / p).resolve()).exists():
                raise Stop("请先处理已有 Git 操作：" + item)
        if run(repo, "ls-files", "-u").stdout:
            raise Stop("请先处理现有文件冲突；本地内容和同步备份仍保留。")
        tracking = "refs/remotes/origin/" + target
        run(repo, "fetch", "--quiet", "--no-tags", "origin",
            "+refs/heads/" + target + ":" + tracking, env=env, timeout=TRANSFER_TIMEOUT)
        tip = value(repo, "rev-parse", tracking)
        if run(repo, "merge-base", "--is-ancestor", tip, "HEAD", check=False).returncode == 0:
            return finish_sync(repo,{"status": "synced", "branch": target, "remote_tip": tip,
                    **({"main": tip} if target == "main" else {}), "preserved_work": True})
        stash = None
        if run(repo, "status", "--porcelain", timeout=TRANSFER_TIMEOUT).stdout:
            run(repo, "stash", "push", "--quiet", "--include-untracked", "-m", "work sync " + uuid.uuid4().hex,
                timeout=TRANSFER_TIMEOUT)
            stash = value(repo, "rev-parse", "refs/stash")
        merged = run(repo, "-c", "user.name=WCG Researcher", "-c",
                     "user.email=wcg@users.noreply.github.com", "merge", "--no-edit", tip,
                     check=False, timeout=TRANSFER_TIMEOUT)
        if merged.returncode:
            run(repo, "merge", "--abort", check=False, timeout=TRANSFER_TIMEOUT)
        restored = None
        if stash:
            restored = run(repo, "stash", "apply", "--index", stash, check=False, timeout=TRANSFER_TIMEOUT)
            if restored.returncode == 0:
                # Remove only our own saved copy after every byte was reapplied.
                if value(repo, "rev-parse", "refs/stash") == stash:
                    run(repo, "stash", "drop", "--quiet", "stash@{0}")
            else:
                raise Stop("同步后恢复遇到文件冲突；本地内容和完整备份 " + stash + " 均保留。")
        if merged.returncode:
            raise Stop(target + " 有真实文件冲突；合并已撤回，本地成果已恢复。")
        return finish_sync(repo,{"status": "synced", "branch": target, "remote_tip": tip,
                **({"main": tip} if target == "main" else {}), "preserved_work": True})


def finish_sync(repo, result):
    # Research state is explicit RUN/workspace data; no retired stage reset hook.
    return result


def save_id(repo, requested=None, *, bind=True):
    saved = local_config(repo, "wcg.save")
    chosen = requested if requested is not None else (saved or DEFAULT_SAVE)
    if not IDENTIFIER.fullmatch(chosen):
        raise Stop("研究存档请使用安全 ID：字母、数字、点、下划线或连字符。")
    if saved and requested and requested != saved:
        raise Stop("本目录已绑定存档 " + saved + "；其他存档请使用独立 clone。")
    if bind and not saved:
        run(repo, "config", "--local", "wcg.save", chosen)
    return chosen


def role_id(repo, requested=None, *, bind=True):
    saved = local_config(repo, "wcg.role")
    chosen = requested if requested is not None else (saved or "boss")
    if chosen not in ROLE_PROMPTS:
        raise Stop("本存档支持角色：" + "、".join(ROLE_PROMPTS))
    if saved and saved != chosen:
        raise Stop("本clone已绑定角色 " + saved + "；另一个角色使用独立clone。")
    if bind and not saved:
        run(repo, "config", "--local", "wcg.role", chosen)
    return chosen


def archive_path(repo, save, subarchive):
    if not IDENTIFIER.fullmatch(save):
        raise Stop("存档 ID 不合法。")
    base = Path("archives") / save
    if subarchive:
        if not IDENTIFIER.fullmatch(subarchive):
            raise Stop("子存档 ID 不合法。")
        base /= Path("subarchives") / subarchive
    if any(path.is_symlink() for path in (repo / base, *(repo / p for p in base.parents))):
        raise Stop("存档路径不能经过符号链接。")
    return base


def prepare_archive(repo, base, *, create, already_bound):
    entry = base / "README.md"
    path = repo / entry
    if path.is_symlink():
        raise Stop("存档入口不能是符号链接。")
    if not create:
        if not path.is_file():
            raise Stop("研究启动所需文件缺失：" + entry.as_posix() +
                       "。请核对 ID；明确创建时使用 --create-archive。")
        return False
    with write_lock(repo):
        outline = f"# {base.name}\n\n## 研究范围\n\n填写本存档的原题、模型和适用范围。\n"
        if path.is_file():
            tracked = run(repo, "cat-file", "-e", "HEAD:" + entry.as_posix(), check=False)
            if already_bound or (tracked.returncode and path.read_text(encoding="utf-8") == outline):
                return False
            raise Stop("存档已存在：" + base.as_posix() + "。使用现有存档时去掉 --create-archive。")
        if len(base.parts) > 2 and not (repo / base.parents[1] / "README.md").is_file():
            raise Stop("先创建或选择现有父存档，再创建子存档。")
        if path.parent.exists() and (not path.parent.is_dir() or any(path.parent.iterdir())):
            raise Stop("存档目录已有内容，已保留：" + base.as_posix())
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("x", encoding="utf-8") as stream:
            stream.write(outline)
        return True


def workspace_path(repo, save, who, *, subarchive=None):
    if not IDENTIFIER.fullmatch(who):
        raise Stop("工作区 ID 不合法。")
    if local_config(repo, "wcg.workflowRun"):
        raise Stop("旧阶段运行绑定已退役；请从研究 RUN 和个人工作区接续。")
    if subarchive is None:
        subarchive = local_config(repo, "wcg.subarchive")
    relative = archive_path(repo, save, subarchive) / "workspaces" / who
    cursor = repo
    for part in relative.parts:
        cursor /= part
        if cursor.is_symlink(): raise Stop("工作区路径不能经过符号链接。")
    return relative


def workspace_init(repo, save, who, resume=False, *, branch=None, subarchive=None):
    with write_lock(repo):
        target = branch_id(repo, branch)
        if value(repo, "branch", "--show-current") != target:
            raise Stop("个人工作区只能在绑定分支 " + target + " 准备。")
        relative = workspace_path(repo, save, who, subarchive=subarchive)
        root = repo / relative
        profile = root / "workspace.json"
        readme = root / "README.md"
        if profile.is_symlink() or readme.is_symlink():
            raise Stop("工作区文件不能是符号链接。")
        instance = run(repo, "config", "--local", "--get", "wcg.instance", check=False).stdout.decode().strip()
        if not instance:
            instance = uuid.uuid4().hex
        if not re.fullmatch(r"[0-9a-f]{32}", instance):
            raise Stop("本地工作区身份配置损坏；先保留并核对。")
        created = not profile.exists()
        if not created:
            old = json.loads(profile.read_text())
            if (not isinstance(old, dict) or set(old) != {"schema", "save", "actor", "instance"}
                    or type(old["schema"]) is not int or old["schema"] != 1
                    or old["save"] != save or old["actor"] != who
                    or not isinstance(old["instance"], str)
                    or not re.fullmatch(r"[0-9a-f]{32}", old["instance"])):
                raise Stop("已存在的工作区身份不相容；保留原内容，不覆盖。")
            if old["instance"] != instance:
                if not resume:
                    raise Stop("这个编号已有其他工作区；新对话换编号，确实接续旧身份时用 start --resume。")
                instance = old["instance"]
        root.mkdir(parents=True, exist_ok=True)
        run(repo, "config", "--local", "wcg.instance", instance)
        if created:
            with tempfile.NamedTemporaryFile(mode="w", dir=root, delete=False) as stream:
                json.dump({"schema": 1, "save": save, "actor": who, "instance": instance},
                          stream, ensure_ascii=False, indent=2)
                stream.write("\n")
            os.replace(stream.name, profile)
        if not readme.exists():
            with readme.open("x") as stream:
                stream.write(f"# {who} 的个人研究工作区\n\n研究存档：`{save}`；发布身份：`{who}`。\n\n"
                             "## 当前研究与恢复\n\n写下正在做什么、文件位置、当前卡点与下一步，恢复时从这里接续。\n\n"
                             "## 个人材料与备份\n\n在此自由建立目录，保存推导、代码、实验和失败尝试。"
                             "未完成、未核验或后来发现错误的研究也可以提交，标明现状即可；不要等结果成熟才备份。\n\n"
                             f"保存本人目录：python3 work.py checkpoint {relative.as_posix()} -m '阶段备份：当前推导与下一步'\n\n"
                             "共享正文与研究地图按数学对象组织，不按角色分区；材料检查整理后再正式入库，此处链接正文。\n\n"
                             "## 交流与状态\n\n通过研究 RUN 留下反馈；其他人可访问已推送材料。"
                             "本地草稿只有完成 checkpoint 并确认 pushed 后才对其他 clone 可见。\n")
        remote = run(repo, "ls-tree", "refs/remotes/origin/" + target,
                     "--", relative.as_posix(), check=False)
        return {"path": relative.as_posix(), "created": created,
                "remote_directory_exists": bool(remote.returncode == 0 and remote.stdout),
                "note": "local preparation; checkpoint and remote confirmation publish new changes"}


def visit(repo, env, save, who, path="README.md", branch=None):
    target_branch = checked_branch(repo, branch or branch_id(repo))
    relative = workspace_path(repo, save, who)
    tail = Path(path)
    if (tail.is_absolute() or not tail.parts or any(p in {".", ".."} for p in tail.parts)
            or "\\" in path or any(c in path for c in "\x00\r\n:")):
        raise Stop("访问路径必须是工作区内的普通相对文件路径。")
    target = (relative / tail).as_posix()
    with write_lock(repo):
        run(repo, "fetch", "--quiet", "--no-tags", "origin",
            "+refs/heads/" + target_branch + ":refs/remotes/origin/" + target_branch,
            env=env, timeout=TRANSFER_TIMEOUT)
        tip = value(repo, "rev-parse", "refs/remotes/origin/" + target_branch)
        entry = run(repo, "ls-tree", tip, "--", ":(literal)" + target).stdout
        if not entry.startswith((b"100644 blob ", b"100755 blob ")):
            raise Stop("远端尚无这个普通文件；本地未推送材料不可被访问。")
        content = run(repo, "show", tip + ":" + target).stdout.decode()
    return {"actor": who, "save": save, "branch": target_branch,
            "commit": tip, "path": target, "text": content}


def clone_for_start(repo, remote, target, env):
    repo.parent.mkdir(parents=True, exist_ok=True)
    # Publish a complete checkout atomically. A killed transfer can only leave a
    # disposable staging directory, never a half-initialized research clone.
    with (repo.parent / f".{repo.name}.wcg-start.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if (repo / ".git").exists():
            return False
        if repo.exists() and (not repo.is_dir() or any(repo.iterdir())):
            raise Stop("目标目录有其他文件；请为仓库指定空目录。")
        with tempfile.TemporaryDirectory(prefix=f".{repo.name}.download-", dir=repo.parent) as stage:
            checkout = Path(stage) / "checkout"
            run(repo.parent, "clone", "--quiet", "--depth=1", "--single-branch",
                "--branch", target, "--", remote, str(checkout), env=env, timeout=TRANSFER_TIMEOUT)
            checkout.rename(repo)
        return True


def finish_legacy_checkout(repo, head):
    pending = local_config(repo, "wcg.bootstrapCheckout")
    if not pending:
        return
    with write_lock(repo):
        if pending != head or local_config(repo, "wcg.instance"):
            raise Stop("旧启动器留下的首次检出标记与当前工作区不一致；已保留本地工作。")
        index = repo / value(repo, "rev-parse", "--git-path", "index")
        if not index.exists():
            run(repo, "read-tree", "HEAD", timeout=TRANSFER_TIMEOUT)
        if run(repo, "diff", "--cached", "--quiet", "HEAD", check=False).returncode:
            raise Stop("首次检出中有暂存改动；已保留本地内容。")
        # Without --force, existing files cannot be overwritten.
        run(repo, "checkout-index", "--all", "--quiet", check=False, timeout=TRANSFER_TIMEOUT)
        if run(repo, "diff", "--quiet", "HEAD", check=False).returncode:
            raise Stop("首次检出中的本地改动已保留；保全草稿后重试。")
        run(repo, "config", "--local", "--unset", "wcg.bootstrapCheckout")


def verified_receipt(receipt, repo, target, head, program_sha):
    return (
        isinstance(receipt, dict)
        and receipt.get("repo") == str(repo)
        and receipt.get("branch") == target
        and receipt.get("head") == head
        and receipt.get("program_sha256") == program_sha
        and isinstance(receipt.get("result"), dict)
        and receipt["result"].get("status") == "synced"
        and receipt["result"].get("branch") == target
    )


def consume_start_handoff():
    # Reserved entry point. Public flags may change without changing this ABI.
    encoded = os.environ.pop(START_RECEIPT, "")
    receipt = json.loads(encoded) if encoded else None
    if not isinstance(receipt, dict) or not isinstance(receipt.get("inputs"), dict):
        raise Stop("启动交接凭据缺失；请直接重跑 start。")
    inputs = receipt["inputs"]
    args = SimpleNamespace(repo=receipt.get("repo"), **{key: inputs.get(key) for key in START_FIELDS})
    if args.repo != str(Path(__file__).resolve().parent):
        raise Stop("启动交接目录不匹配；请直接重跑 start。")
    return start(args, receipt=receipt, require_receipt=True)


def start(args, *, receipt=None, require_receipt=False):
    running_source = Path(__file__).read_bytes()
    if not require_receipt:
        # Compatibility with uploaded launchers issued before the fixed interface.
        try:
            receipt = json.loads(os.environ.pop("WCG_START_HANDOFF", "null"))
        except ValueError:
            receipt = None
    repo = Path(args.repo).expanduser().resolve()
    if not args.save and (args.create_archive or not (repo / ".git").exists()):
        raise Stop("首次启动或创建存档须带明确的 --save ID。")
    if (args.save == "repository-cleanup" or getattr(args, "curation_run", None)
            or getattr(args, "workflow_run", None) or getattr(args, "board_branch", None)
            or getattr(args, "board_limit", 0)):
        raise Stop("旧阶段及公屏已退役；请选择数学存档并使用研究 RUN。")
    if args.token_file:
        args.token_file = str(Path(args.token_file).expanduser().resolve())
        if Path(args.token_file).is_relative_to(repo):
            raise Stop("凭据文件请放在仓库外。")

    remote = args.remote
    auth_mode = args.auth or (local_config(repo, "wcg.auth") if (repo / ".git").exists() else "") or "token"
    if auth_mode == "ssh" and remote == "https://github.com/SOMEBODYJUN/co-work-anl.git":
        remote = "git@github.com:SOMEBODYJUN/co-work-anl.git"
    if not remote or remote.startswith("-") or SECRET.search(remote.encode()) or re.search(r"https?://[^/]*@", remote):
        raise Stop("仓库地址请使用普通 Git URL。")

    created = False
    if not (repo / ".git").exists():
        if require_receipt:
            raise Stop("启动交接的检出目录缺失；请直接重跑 start。")
        who = args.actor or os.environ.get("WCG_ACTOR", "").strip()
        if not IDENTIFIER.fullmatch(who):
            raise Stop("首次启动须带 --actor Boss编号。")
        target = checked_branch(Path.cwd(), args.branch or DEFAULT_BRANCH)
        clone_env = environment(args.token_file, mode=auth_mode)
        created = clone_for_start(repo, remote, target, clone_env)
    repo = checked_repo(repo)
    origin = value(repo, "remote", "get-url", "--all", "origin")
    if origin != remote or value(repo, "remote", "get-url", "--push", "--all", "origin") != origin:
        raise Stop("目标目录的 origin 与本研究仓库不一致；请使用本研究的独立目录。")
    if local_config(repo, "wcg.curationRun") or local_config(repo, "wcg.workflowRun"):
        raise Stop("当前目录绑定旧阶段；请为研究使用独立目录。")
    target = branch_id(repo, args.branch)
    branch = value(repo, "branch", "--show-current")
    legacy = target == "main" and branch.startswith("wcg/work/") and not args.branch
    if branch != target and not legacy:
        raise Stop("当前分支不是 " + target + "；请使用独立 clone，已有工作已保留。")

    head = value(repo, "rev-parse", "HEAD")
    finish_legacy_checkout(repo, head)
    current_program = repo / "work.py"
    env = auth(repo, args, bind=False)
    valid = current_program.is_file() and verified_receipt(
        receipt, repo, target, head, hashlib.sha256(current_program.read_bytes()).hexdigest())
    if valid:
        result = receipt["result"]
    elif require_receipt:
        raise Stop("启动交接与当前分支或程序版本不一致；请直接重跑 start。")
    elif created:
        result = {"status": "synced", "branch": target, "remote_tip": head, "preserved_work": True}
    else:
        result = sync(repo, env, allow_legacy=legacy, target=target)

    if not current_program.is_file() or current_program.is_symlink():
        raise Stop("研究分支缺少普通文件 work.py；请核对所选版本。")
    program_bytes = current_program.read_bytes()
    if Path(__file__).resolve() != current_program or program_bytes != running_source:
        if require_receipt:
            raise Stop("启动交接期间工作区程序发生变化；请直接重跑 start。")
        if not valid and run(repo, "diff", "--quiet", "HEAD", "--", "work.py", check=False).returncode:
            raise Stop("检出的 work.py 有本地改动；请保全修改后再启动。")
        payload = {
            "repo": str(repo), "branch": target, "head": value(repo, "rev-parse", "HEAD"),
            "program_sha256": hashlib.sha256(program_bytes).hexdigest(), "result": result,
            "inputs": {**{key: getattr(args, key) for key in START_FIELDS}, "remote": remote},
        }
        # Do not forward public CLI options or inherited defaults.
        return subprocess.call([sys.executable, str(current_program), START_COMMAND], cwd=repo,
                               env=dict(env, **{START_RECEIPT: json.dumps(payload)}))

    who = actor(repo, args.actor, args.adopt_legacy, bind=False)
    previous_save = local_config(repo, "wcg.save")
    if not args.save and not previous_save:
        raise Stop("首次启动须带明确的 --save ID。")
    save = save_id(repo, args.save, bind=False)
    if save == "repository-cleanup":
        raise Stop("旧阶段存档已退役；请为研究使用独立目录。")
    role = role_id(repo, args.role, bind=False)
    saved_sub = local_config(repo, "wcg.subarchive")
    if args.subarchive and previous_save and args.subarchive != saved_sub:
        raise Stop("子存档变更请使用独立 clone；已有绑定已保留。")
    subarchive = args.subarchive or saved_sub
    base = archive_path(repo, save, subarchive)
    entry = base / "README.md"
    role_prompt = ROLE_PROMPTS[role]
    for required in (Path(role_prompt), Path(TOOLS) / "research_runtime.py"):
        if not (repo / required).is_file():
            raise Stop("研究启动所需文件缺失：" + required.as_posix())
    archive_created = prepare_archive(repo, base, create=args.create_archive,
                                      already_bound=previous_save == save and saved_sub == subarchive)

    if legacy:
        with write_lock(repo):
            previous = run(repo, "rev-parse", "--verify", "refs/heads/main", check=False)
            if previous.returncode == 0:
                run(repo, "update-ref", "refs/wcg/recovery/main-" + uuid.uuid4().hex,
                    previous.stdout.decode().strip())
            run(repo, "branch", "-M", "main")

    workspace = workspace_init(repo, save, who, args.resume, branch=target, subarchive=subarchive)
    actor(repo, who, args.adopt_legacy)
    save_id(repo, save)
    role_id(repo, role)
    for key, val in {"wcg.branch": target, "wcg.subarchive": subarchive,
                     "user.name": "WCG " + who, "user.email": "wcg@users.noreply.github.com"}.items():
        if val and not local_config(repo, key):
            run(repo, "config", "--local", key, val)
    bind_auth(repo, args, auth_mode)

    result.update(actor=who, save=save, workspace=workspace, repo=str(repo), branch=target,
                  archive_scope=base.as_posix(), archive_created=archive_created,
                  context_entry=entry.as_posix(), research_entry=entry.as_posix(),
                  research_prompt=role_prompt, role_prompt=role_prompt, role=role,
                  research_runbook="research/agent-design/README.md",
                  research_status="runtime-ready-problem-not-started",
                  research_collaboration={
                      "discover": "python work.py research peers RUN",
                      "initialize": "python work.py research studio init RUN --spec PATH --expect-branch " + target,
                      "restore": "python work.py research studio status RUN --session-tag CURRENT_SESSION",
                  })
    if subarchive:
        result["subarchive"] = subarchive
    print(json.dumps(result, ensure_ascii=False), flush=True)
    return 0


def main():
    if os.environ.get("WCG_WORK_ASKPASS") == "1" and len(sys.argv) == 2:
        if sys.argv[1].startswith("Username"):
            print("x-access-token")
            return 0
        if sys.argv[1].startswith("Password"):
            print(credential(os.environ["WCG_CHECKPOINT_TOKEN_FILE"]))
            return 0
    if sys.argv[1:] == [START_COMMAND]:
        return consume_start_handoff()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", default=default_repo())
    p.add_argument("--token-file")
    p.add_argument("--auth", choices=("token", "ssh"))
    p.add_argument("--save", help="研究存档 ID；首次启动显式指定")
    sub = p.add_subparsers(dest="command", required=True)
    start_parser = sub.add_parser("start", help="恢复研究仓库并绑定数学研究身份")
    start_parser.add_argument("--actor", help="显式 Boss 编号；首次启动必须提供")
    start_parser.add_argument("--adopt-legacy", action="store_true")
    start_parser.add_argument("--auth", choices=("token", "ssh"), default=argparse.SUPPRESS)
    start_parser.add_argument("--role", choices=tuple(ROLE_PROMPTS))
    start_parser.add_argument("--token-file", default=argparse.SUPPRESS)
    start_parser.add_argument("--remote", default=REMOTE)
    start_parser.add_argument("--save", default=argparse.SUPPRESS)
    start_parser.add_argument("--resume", action="store_true")
    start_parser.add_argument("--subarchive")
    start_parser.add_argument("--create-archive", action="store_true",
                              help="创建明确选择的新存档；指定子存档时父存档须已存在")
    start_parser.add_argument("--branch")
    # These names are only parsed to accept the former default (0) or explain
    # that an explicit legacy workflow has been retired.
    start_parser.add_argument("--board-limit", type=int, default=0, help=argparse.SUPPRESS)
    for retired in ("board-branch", "curation-run", "workflow-run"):
        start_parser.add_argument("--" + retired, help=argparse.SUPPRESS)
    sub.add_parser("sync", help="只同步绑定研究分支并保留本地工作")
    research = sub.add_parser("research", help="读取超边、恢复 RUN、保存研究结果")
    research.add_argument("--registry")
    research.add_argument("args", nargs=argparse.REMAINDER)
    computation = sub.add_parser("compute", help="执行明确登记的研究计算")
    computation.add_argument("args", nargs=argparse.REMAINDER)
    github = sub.add_parser("github", help="读取或操作明确的 GitHub 研究资源")
    github.add_argument("args", nargs=argparse.REMAINDER)
    workspace = sub.add_parser("workspace", help="准备当前研究身份的个人工作区")
    workspace.add_argument("--resume", action="store_true")
    visit = sub.add_parser("visit", help="只读访问已推送的研究文件")
    visit.add_argument("actor")
    visit.add_argument("--path", default="README.md")
    visit.add_argument("--branch")
    checkpoint = sub.add_parser("checkpoint", help="保存研究资产并按明确范围推送")
    checkpoint.add_argument("paths", nargs="*")
    checkpoint.add_argument("-m", "--message")
    checkpoint.add_argument("--create-branch", action="store_true")
    checkpoint.add_argument("--local-only", action="store_true")
    checkpoint.add_argument("--publish-only", action="store_true")
    checkpoint.add_argument("--review-plan", action="append", default=[])
    a = p.parse_args()
    if a.command == "start":
        return start(a)
    repo = checked_repo(a.repo)
    if a.command == "research":
        registry = ["--registry", a.registry] if a.registry else []
        return subprocess.call([sys.executable, str(repo / TOOLS / "research_runtime.py"), "--repo", str(repo), *registry, *a.args])
    if a.command == "compute":
        return subprocess.call([sys.executable, str(repo / TOOLS / "compute.py"), "--repo", str(repo), *a.args])
    env = environment() if a.command == "checkpoint" and a.local_only else auth(repo, a)
    if a.command == "github":
        return subprocess.call([sys.executable, str(repo / TOOLS / "github_resources.py"), "--repo", str(repo), *a.args], env=env)
    who = actor(repo)
    save = save_id(repo, a.save)
    if a.command == "sync":
        print(json.dumps(sync(repo, env), ensure_ascii=False)); return 0
    if a.command == "workspace":
        print(json.dumps(workspace_init(repo, save, who, a.resume), ensure_ascii=False)); return 0
    if a.command == "visit":
        print(json.dumps(visit(repo, env, save, a.actor, a.path, a.branch), ensure_ascii=False, indent=2)); return 0
    if a.command == "checkpoint":
        command = [sys.executable, str(repo / TOOLS / "checkpoint.py"), "--repo", str(repo), *a.paths]
        if a.message: command += ["-m", a.message]
        if a.create_branch: command.append("--create-branch")
        if a.local_only: command.append("--local-only")
        if a.publish_only: command.append("--publish-only")
        for plan in a.review_plan: command.extend(["--review-plan", plan])
        return subprocess.call(command, env=env)
    raise Stop("未知研究命令")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("启动或运行已中断；可重跑原命令。", file=sys.stderr)
        raise SystemExit(130)
    except (Stop, OSError, ValueError) as exc:
        message = SECRET.sub(b"[REDACTED]", str(exc).encode()).decode()
        print("ERROR: " + message, file=sys.stderr)
        raise SystemExit(2)
