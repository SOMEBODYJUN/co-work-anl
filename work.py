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
import subprocess
import sys
import tempfile
import uuid

REMOTE = "https://github.com/SOMEBODYJUN/co-work-anl.git"
TOOLS = "tools"
WORKSPACES = "research/workspaces"
# Legacy unbound non-start/checkpoint fallback; preserve topic compatibility.
# New-conversation phase defaults are separate below and are applied by start.
DEFAULT_SAVE = "customer-attraction"
# New conversations share this long-lived branch and board. Existing bound
# clones keep their own routes; cleanup is a phase, not a branch lifecycle.
DEFAULT_BRANCH = "rebuild/research-v2"
DEFAULT_BOARD_BRANCH = "wcg/board-cleanup-20261028"
DEFAULT_START_SAVE = "repository-cleanup"
RESEARCH_ENTRIES = {
    "repository-cleanup": {"research_entry": "cleanup/README.md", "research_prompt": "prompts/02-clean.md", "research_runbook": "tools/README.md"},
    "customer-attraction": {"research_entry": "archives/customer-attraction/README.md", "research_prompt": "archives/customer-attraction/prompts/README.md", "research_runbook": "tools/README.md"},
    "facility-games": {"research_entry": "archives/facility-games/README.md", "research_prompt": "archives/facility-games/prompts/README.md", "research_runbook": "tools/README.md"},
    "weighted-congestion": {"research_entry": "archives/weighted-congestion/README.md", "research_prompt": "archives/weighted-congestion/prompts/README.md", "research_runbook": "tools/README.md"},
    "unrelated-machines": {"research_entry": "archives/unrelated-machines/README.md", "research_prompt": "archives/unrelated-machines/prompts/README.md", "research_runbook": "tools/README.md"},
    "positive-kernels": {"research_entry": "archives/positive-kernels/README.md", "research_prompt": "archives/positive-kernels/prompts/README.md", "research_runbook": "tools/README.md"},
}
ROLE_PROMPTS = {"boss": "prompts/README.md", "cleaner": "prompts/02-clean.md", "mapper": "prompts/03-map.md"}
CLEANUP_ROLE_PROMPTS = ROLE_PROMPTS
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


def checked_branch(repo, name, board=False):
    if (not name or name.startswith("-") or name == "HEAD"
            or SECRET.search(name.encode())
            or run(repo, "check-ref-format", "refs/heads/" + name,
                   check=False).returncode):
        raise Stop("分支名不合法。")
    if not board and (name == "wcg/board" or name.startswith("wcg/board-")):
        raise Stop("公屏分支不能用作研究文件分支。")
    return name


def branch_id(repo, requested=None):
    saved = run(repo, "config", "--local", "--get", "wcg.branch",
                check=False).stdout.decode().strip()
    current = value(repo, "branch", "--show-current")
    fallback = DEFAULT_BRANCH if current == DEFAULT_BRANCH else "main"
    chosen = checked_branch(repo, requested or saved or fallback)
    if saved and requested and chosen != saved:
        raise Stop("本clone已绑定文件分支 " + saved + "；其他分支使用独立clone。")
    return chosen


def board_branch(repo, requested=None):
    saved = run(repo, "config", "--local", "--get", "wcg.boardBranch",
                check=False).stdout.decode().strip()
    fallback = DEFAULT_BOARD_BRANCH if branch_id(repo) == DEFAULT_BRANCH else "wcg/board"
    chosen = checked_branch(repo, requested or saved or fallback, board=True)
    if chosen == branch_id(repo):
        raise Stop("公屏分支与研究文件分支必须分开。")
    if saved and requested and saved != chosen:
        raise Stop("本clone已绑定公屏 " + saved + "；新公屏使用独立clone。")
    return chosen


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
    chosen = requested if requested is not None else (requested_from_env or saved or ("R-" + uuid.uuid4().hex))
    if not chosen or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,63}", chosen):
        raise Stop("start --actor 应使用安全的发布身份；省略即可自动生成并记住 R-UUID。")
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


def sync(repo, env, allow_legacy=False):
    with write_lock(repo):
        target = branch_id(repo)
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
            "+refs/heads/" + target + ":" + tracking, env=env)
        tip = value(repo, "rev-parse", tracking)
        if run(repo, "merge-base", "--is-ancestor", tip, "HEAD", check=False).returncode == 0:
            return {"status": "synced", "branch": target, "remote_tip": tip,
                    **({"main": tip} if target == "main" else {}), "preserved_work": True}
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
            raise Stop(target + " 有真实文件冲突；合并已撤回，本地成果已恢复。")
        return {"status": "synced", "branch": target, "remote_tip": tip,
                **({"main": tip} if target == "main" else {}), "preserved_work": True}


def save_id(repo, requested=None, default=None):
    saved = run(repo, "config", "--local", "--get", "wcg.save", check=False).stdout.decode().strip()
    chosen = requested if requested is not None else (saved or default or DEFAULT_SAVE)
    if not IDENTIFIER.fullmatch(chosen):
        raise Stop("研究存档请使用安全 ID：字母、数字、点、下划线或连字符。")
    if saved and requested and requested != saved:
        raise Stop("本目录已绑定存档 " + saved + "；其他存档请使用独立 clone。")
    if not saved:
        run(repo, "config", "--local", "wcg.save", chosen)
    return chosen


def role_id(repo, requested=None, prompts=None, default="boss"):
    prompts = prompts or ROLE_PROMPTS
    saved = run(repo, "config", "--local", "--get", "wcg.role", check=False).stdout.decode().strip()
    chosen = requested if requested is not None else (saved or default)
    if chosen not in prompts:
        raise Stop("本存档支持角色：" + "、".join(prompts))
    if saved and saved != chosen:
        raise Stop("本clone已绑定角色 " + saved + "；另一个角色使用独立clone。")
    if not saved:
        run(repo, "config", "--local", "wcg.role", chosen)
    return chosen


def workspace_path(repo, save, who):
    if not IDENTIFIER.fullmatch(save) or not IDENTIFIER.fullmatch(who):
        raise Stop("工作区 ID 不合法。")
    subarchive=run(repo,"config","--local","--get","wcg.subarchive",check=False).stdout.decode().strip()
    base=Path("archives")/save
    if subarchive:
        if not IDENTIFIER.fullmatch(subarchive):raise Stop("子存档绑定不合法。")
        base=base/"subarchives"/subarchive
    relative = (Path("cleanup/workspaces") / who if save == "repository-cleanup"
                else base / "workspaces" / who)
    cursor = repo
    for part in relative.parts:
        cursor /= part
        if cursor.is_symlink():
            raise Stop("工作区路径不能经过符号链接。")
    return relative


def workspace_init(repo, save, who, resume=False):
    with write_lock(repo):
        target = branch_id(repo)
        if value(repo, "branch", "--show-current") != target:
            raise Stop("个人工作区只能在绑定分支 " + target + " 准备。")
        relative = workspace_path(repo, save, who)
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
        if created:
            with profile.open("x") as stream:
                json.dump({"schema": 1, "save": save, "actor": who, "instance": instance},
                          stream, ensure_ascii=False, indent=2)
                stream.write("\n")
        if not readme.exists():
            with readme.open("x") as stream:
                stream.write(f"# {who} 的个人研究工作区\n\n研究存档：`{save}`；发布身份：`{who}`。\n\n"
                             "## 当前研究与恢复\n\n写下正在做什么、文件位置、当前卡点与下一步，恢复时从这里接续。\n\n"
                             "## 个人材料与备份\n\n在此自由建立目录，保存推导、代码、实验和失败尝试。"
                             "未完成、未核验或后来发现错误的研究也可以提交，标明现状即可；不要等结果成熟才备份。\n\n"
                             f"保存本人目录：python3 work.py checkpoint {relative.as_posix()} -m '阶段备份：当前推导与下一步'\n\n"
                             "共享正文与研究地图按数学对象组织，不按角色分区；材料检查整理后再正式入库，此处链接正文。\n\n"
                             "## 交流与状态\n\n可以通过同一 work.py 私聊这个发布身份；其他人可访问已推送材料。"
                             "本地草稿只有完成 checkpoint 并确认 pushed 后才对其他 clone 可见。\n")
        run(repo, "config", "--local", "wcg.instance", instance)
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
            "+refs/heads/" + target_branch + ":refs/remotes/origin/" + target_branch, env=env)
        tip = value(repo, "rev-parse", "refs/remotes/origin/" + target_branch)
        entry = run(repo, "ls-tree", tip, "--", ":(literal)" + target).stdout
        if not entry.startswith((b"100644 blob ", b"100755 blob ")):
            raise Stop("远端尚无这个普通文件；本地未推送材料不可被访问。")
        content = run(repo, "show", tip + ":" + target).stdout.decode()
    return {"actor": who, "save": save, "branch": target_branch,
            "commit": tip, "path": target, "text": content}


def start(args):
    # A downloaded copy stays a bootstrap. After restoring the selected branch
    # it hands control to that branch's current root program, before binding a
    # phase/save/role. Later prompt and phase updates therefore live on GitHub.
    running_source = Path(__file__).read_bytes()
    # Consume a one-hop handoff receipt. The bootstrap has just fetched this
    # exact checkout; its current program need not repeat the same network sync.
    try:handoff=json.loads(os.environ.pop('WCG_START_HANDOFF','null'))
    except (ValueError,TypeError):handoff=None
    created_clone=False
    board_limit = getattr(args, "board_limit", 0)
    if board_limit < 0:
        raise Stop("start --board-limit 必须是非负整数；0 表示不自动读取公屏。")
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
        target = checked_branch(repo.parent, getattr(args, "branch", None) or DEFAULT_BRANCH)
        run(repo.parent, "clone", "--quiet", "--depth=1", "--single-branch", "--branch", target, remote, str(repo), env=env)
        created_clone=True
    repo = checked_repo(repo)
    origin = value(repo, "remote", "get-url", "--all", "origin")
    push_origin = value(repo, "remote", "get-url", "--push", "--all", "origin")
    if origin != args.remote or push_origin != origin:
        raise Stop("目标目录的 origin 与本研究仓库不一致；请使用本研究的独立目录。")
    target = branch_id(repo, getattr(args, "branch", None))
    branch = value(repo, "symbolic-ref", "--quiet", "--short", "HEAD")
    legacy = target == "main" and branch.startswith("wcg/work/") and not getattr(args, "branch", None)
    if branch != target and not legacy:
        raise Stop("当前分支不是 " + target + "；不自动切换或合并其他分支，请使用独立clone。")
    selected_board = board_branch(repo, getattr(args, "board_branch", None))
    if selected_board == target:
        raise Stop("公屏分支与研究文件分支必须分开。")
    env = auth(repo, args)
    run(repo, "config", "--local", "wcg.branch", target)
    current_program = repo / "work.py"
    valid_handoff=(isinstance(handoff,dict) and handoff.get('repo')==str(repo)
                   and handoff.get('branch')==target
                   and handoff.get('head')==value(repo,'rev-parse','HEAD')
                   and handoff.get('program_sha256')==hashlib.sha256(current_program.read_bytes()).hexdigest()
                   and isinstance(handoff.get('result'),dict)
                   and handoff['result'].get('status')=='synced'
                   and handoff['result'].get('branch')==target)
    if valid_handoff:
        result=handoff['result']
    elif created_clone:
        tip=value(repo,'rev-parse','refs/remotes/origin/'+target)
        result={'status':'synced','branch':target,'remote_tip':tip,'preserved_work':True}
    else:
        result = sync(repo, env, allow_legacy=legacy)
    if (Path(__file__).resolve() != current_program.resolve()
            or current_program.read_bytes() != running_source):
        forwarded = ["--repo", str(repo), "start", "--remote", args.remote,
                     "--board-limit", str(board_limit)]
        for name in ("actor", "role", "token_file", "save", "branch", "board_branch", "subarchive"):
            supplied = getattr(args, name, None)
            if supplied is not None:
                forwarded.extend(["--" + name.replace("_", "-"), str(supplied)])
        if getattr(args, "resume", False):
            forwarded.append("--resume")
        forwarded_env=dict(env,WCG_START_HANDOFF=json.dumps({
            'repo':str(repo),'branch':target,'head':value(repo,'rev-parse','HEAD'),
            'program_sha256':hashlib.sha256(current_program.read_bytes()).hexdigest(),'result':result}))
        return subprocess.call([sys.executable, str(current_program), *forwarded], env=forwarded_env)
    who = actor(repo, args.actor)
    if not run(repo, "config", "--local", "--get", "user.name", check=False).stdout:
        run(repo, "config", "--local", "user.name", "WCG " + who)
    if not run(repo, "config", "--local", "--get", "user.email", check=False).stdout:
        run(repo, "config", "--local", "user.email", "wcg@users.noreply.github.com")
    previous_save=run(repo,"config","--local","--get","wcg.save",check=False).stdout.decode().strip()
    saved_sub=run(repo,"config","--local","--get","wcg.subarchive",check=False).stdout.decode().strip()
    requested_sub=getattr(args,"subarchive",None)
    if requested_sub and (not IDENTIFIER.fullmatch(requested_sub) or (previous_save and requested_sub!=saved_sub)):
        raise Stop("子存档变更请使用独立clone；不改写已有绑定。")
    requested_save=getattr(args,"save",None)
    preview_save=requested_save or previous_save or (DEFAULT_START_SAVE if target==DEFAULT_BRANCH else DEFAULT_SAVE)
    if not IDENTIFIER.fullmatch(preview_save):
        raise Stop("研究存档请使用安全ID。")
    selected_sub=requested_sub or saved_sub
    if selected_sub:
        if preview_save=='repository-cleanup' or not (repo/'archives'/preview_save/'subarchives'/selected_sub/'README.md').is_file():
            raise Stop("不存在该研究子存档；先按实际问题建立目录。")
    save = save_id(repo, requested_save,
                   DEFAULT_START_SAVE if target == DEFAULT_BRANCH else DEFAULT_SAVE)
    if selected_sub:
        run(repo,"config","--local","wcg.subarchive",selected_sub)
    requested_role = getattr(args, "role", None)
    prompts = CLEANUP_ROLE_PROMPTS if save == "repository-cleanup" else ROLE_PROMPTS
    valid_archive=(repo/'archives'/save/'README.md').is_file()
    if requested_role is not None and save not in RESEARCH_ENTRIES and not valid_archive:
        raise Stop("请先为明确研究问题建立存档README，再绑定此角色。")
    selected_role = role_id(repo, requested_role, prompts,
                            "cleaner" if save == "repository-cleanup" else "boss") if save in RESEARCH_ENTRIES or valid_archive else None
    run(repo, "config", "--local", "wcg.boardBranch", selected_board)
    if legacy:
        # sync has already preserved staged/unstaged/untracked work and stopped
        # on any real conflict. Keep any existing local main under a local ref
        # before renaming the old work branch. No remote branch is created.
        with write_lock(repo):
            previous = run(repo, "rev-parse", "--verify", "refs/heads/main", check=False)
            if previous.returncode == 0:
                run(repo, "update-ref", "refs/wcg/recovery/main-" + uuid.uuid4().hex,
                    previous.stdout.decode().strip())
            run(repo, "branch", "-M", "main")
    workspace = workspace_init(repo, save, who, getattr(args, "resume", False))
    result.update(actor=who, save=save, workspace=workspace,
                  repo=str(repo), branch=value(repo, "branch", "--show-current"))
    result.update(RESEARCH_ENTRIES.get(save, {
        "research_entry": None, "research_prompt": None,
        "research_note": "Unregistered archive: select its research entry explicitly; no topic is inherited.",
    }))
    if save not in RESEARCH_ENTRIES and valid_archive:
        base=(Path('archives')/save).as_posix()
        prompt=base+'/prompts/README.md'
        result.update(research_entry=base+'/README.md',research_prompt=prompt if (repo/prompt).is_file() else 'prompts/README.md',research_runbook='tools/README.md')
    if result.get('research_entry'):
        result['context_entry']=result['research_entry']
    if selected_sub:
        base=(Path('archives')/save/'subarchives'/selected_sub).as_posix()
        result.update(subarchive=selected_sub,research_entry=base+'/README.md',research_prompt=base+'/prompts/README.md',context_entry=base+'/README.md')
    result.update(role=selected_role,
                  role_prompt=prompts[selected_role] if selected_role else None,
                  board_branch=selected_board)
    if save == "customer-attraction" and not selected_sub:
        result["context_entry"] = "archives/customer-attraction/README.md"
    elif save == "repository-cleanup":
        result["context_entry"] = ("prompts/03-map.md" if selected_role == "mapper" else "cleanup/README.md")
    result["recent_board_limit"] = board_limit
    print(json.dumps(result, ensure_ascii=False), flush=True)
    if not board_limit:
        return 0
    return board(repo, env, "view", ["--save", save, "--limit", str(board_limit)])


def board(repo, env, command, extra):
    path = repo / TOOLS / "board.py"
    if not path.is_file():
        raise Stop("仓库缺少公屏程序；请运行 sync 更新程序。")
    return subprocess.call([sys.executable, str(path), "--repo", str(repo),
                            "--branch", board_branch(repo), command, *extra], env=env)


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
    p.add_argument("--save", help="研究存档 ID；新clone默认 repository-cleanup，已绑定clone保持原存档")
    sub = p.add_subparsers(dest="command", required=True)
    s = sub.add_parser("start", help="恢复项目，固定角色号并同步；公屏按需读取")
    s.add_argument("--actor", help="可选；省略时为本对话生成并记住唯一 R-UUID 发布标识")
    s.add_argument("--role", choices=tuple(ROLE_PROMPTS), help="本轮新清洗clone默认cleaner；既有绑定复用")
    s.add_argument("--token-file", default=argparse.SUPPRESS)
    s.add_argument("--remote", default=REMOTE)
    s.add_argument("--save", default=argparse.SUPPRESS)
    s.add_argument("--resume", action="store_true", help="明确接续已存在的同号工作区")
    s.add_argument("--subarchive", help="父存档下的明确子问题；首次绑定，继续同clone复用")
    s.add_argument("--branch", help="文件分支；新clone默认长期共用分支，既有绑定不变")
    s.add_argument("--board-branch", help="公屏分支；新长期分支clone默认新公屏，既有绑定不变")
    s.add_argument("--board-limit", type=int, default=0,
                   help="启动时读取最近几条公屏；默认0不自动读取，完整历史用read按需查询")
    sub.add_parser("sync", help="只同步绑定分支并保留本地工作")
    sub.add_parser("board-init", help="初始化绑定公屏；已有公屏不删除消息")
    clean = sub.add_parser("clean", help="来源、逐文件认领/勾选与覆盖")
    clean.add_argument("args", nargs=argparse.REMAINDER)
    mapping = sub.add_parser("map", help="检查/生成子存档、存档和全仓超图")
    mapping.add_argument("args", nargs=argparse.REMAINDER)
    r = sub.add_parser("read", help="读取异步公屏")
    r.add_argument("--json", action="store_true")
    r.add_argument("--thread")
    r.add_argument("--limit", type=int,
                   help="只显示最近若干条消息；0 表示全部")
    s = sub.add_parser("send", help="署名发言，回复和资产引用均可选")
    text = s.add_mutually_exclusive_group(required=True)
    text.add_argument("--text")
    text.add_argument("--text-file")
    for name in ("thread", "reply-to", "asset-json", "kind", "event-id"):
        s.add_argument("--" + name)
    s.add_argument("--mention", action="append", default=[])
    s.add_argument("--to", help="定向私聊收件人；省略时为公屏")
    dm = sub.add_parser("dm", help="发送或读取与一位 Worker 的双方私聊")
    dm.add_argument("--to", required=True)
    text = dm.add_mutually_exclusive_group()
    text.add_argument("--text")
    text.add_argument("--text-file")
    dm.add_argument("--json", action="store_true")
    for name in ("thread", "reply-to", "asset-json", "kind", "event-id"):
        dm.add_argument("--" + name)
    inbox = sub.add_parser("inbox", help="查看自己的私聊、提及和回复；默认未读")
    inbox.add_argument("--json", action="store_true")
    inbox.add_argument("--all", action="store_true")
    inbox.add_argument("--limit", type=int)
    ack = sub.add_parser("ack", help="标记收件箱消息已读，不代表数学采用")
    ack.add_argument("ids", nargs="+")
    workspace = sub.add_parser("workspace", help="准备自己的个人研究工作区")
    workspace.add_argument("--resume", action="store_true")
    v = sub.add_parser("visit", help="只读访问别人已推送的工作区文件")
    v.add_argument("actor")
    v.add_argument("--path", default="README.md")
    v.add_argument("--branch", help="只读其他文件分支；默认绑定分支")
    c = sub.add_parser("checkpoint", help="立即保存阶段资产并推送")
    c.add_argument("paths", nargs="*")
    c.add_argument("-m", "--message")
    c.add_argument("--create-branch", action="store_true",
                   help="明确允许首次发布绑定分支；基线为远端main，不覆盖已有分支")
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
    save = save_id(repo, a.save)
    target = getattr(a, "to", None)
    if target is not None and (not IDENTIFIER.fullmatch(target) or target == who):
        raise Stop("私聊必须指定另一位 Worker 的有效编号；不会改发到公屏。")
    if a.command in ("clean", "map"):
        module = "cleanup.py" if a.command == "clean" else "maps.py"
        command=[sys.executable, str(repo / TOOLS / module), "--repo", str(repo), *a.args]
        if a.command=='clean' and a.args and a.args[0] in ('claim','done','release'):
            result=subprocess.run(command,env=env,capture_output=True,text=True)
            if result.stderr:sys.stderr.write(result.stderr)
            if result.returncode:
                sys.stdout.write(result.stdout)
                return result.returncode
            receipt=json.loads(result.stdout)
            if receipt.get('status')=='pushed':
                try:receipt['local_sync']=sync(repo,env)
                except (Stop,OSError) as exc:
                    # The remote operation succeeded even if restoring local
                    # drafts needs attention; keep that success distinguishable.
                    receipt['local_sync']={'status':'needs-attention','detail':str(exc)}
            print(json.dumps(receipt,ensure_ascii=False,indent=2))
            return 0
        return subprocess.call(command, env=env)
    if a.command == "sync":
        print(json.dumps(sync(repo, env), ensure_ascii=False))
        return 0
    if a.command == "board-init":
        return board(repo, env, "init", [])
    if a.command == "read":
        extra = ["--save", save] + (["--json"] if a.json else [])
        if a.thread is not None:
            extra += ["--thread", a.thread]
        if a.limit is not None:
            if a.limit < 0:
                raise Stop("read --limit 必须是非负整数。")
            extra += ["--limit", str(a.limit)]
        return board(repo, env, "view", extra)
    if a.command == "workspace":
        print(json.dumps(workspace_init(repo, save, who, a.resume), ensure_ascii=False))
        return 0
    if a.command == "visit":
        print(json.dumps(visit(repo, env, save, a.actor, a.path, a.branch), ensure_ascii=False, indent=2))
        return 0
    if a.command == "ack":
        extra = ["--actor", who, "--save", save]
        for ident in a.ids:
            extra += ["--event-id", ident]
        return board(repo, env, "ack", extra)
    if a.command == "inbox":
        extra = ["--actor", who, "--save", save, "--inbox"]
        if not a.all:
            extra += ["--unread"]
        if a.json:
            extra += ["--json"]
        if a.limit is not None:
            extra += ["--limit", str(a.limit)]
        return board(repo, env, "view", extra)
    if a.command == "dm" and a.text is None and a.text_file is None:
        extra = ["--actor", who, "--save", save, "--peer", a.to]
        if a.json:
            extra += ["--json"]
        if a.thread:
            extra += ["--thread", a.thread]
        return board(repo, env, "view", extra)
    if a.command in ("send", "dm"):
        extra = ["--actor", who, "--save", save]
        for name in ("text", "text_file", "thread", "reply_to", "asset_json", "kind", "event_id"):
            v = getattr(a, name)
            if v is not None:
                extra += ["--" + name.replace("_", "-"), v]
        if getattr(a, "to", None) is not None:
            extra += ["--to", a.to]
        for person in getattr(a, "mention", []):
            extra += ["--mention", person]
        return board(repo, env, "say", extra)
    if a.command in ("pending", "retry", "discard"):
        return board(repo, env, a.command,
                     ["--event-id", a.event_id, "--actor", who] if a.command != "pending" else [])
    if a.command == "checkpoint":
        command = [sys.executable, str(repo / TOOLS / "checkpoint.py"), "--repo", str(repo), *a.paths]
        if a.message:
            command += ["-m", a.message]
        if a.create_branch:
            command += ["--create-branch"]
        return subprocess.call(command, env=env)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Stop, OSError, ValueError) as exc:
        message = SECRET.sub(b"[REDACTED]", str(exc).encode()).decode()
        print("ERROR: " + message, file=sys.stderr)
        raise SystemExit(2)
