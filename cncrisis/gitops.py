"""Serial checkpoints; credentials stay outside this repository."""
import json
from pathlib import Path
import subprocess


def git(root, *args):
    result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return result.stdout.strip()


def checkpoint(args):
    root = Path(git(args.workspace, "rev-parse", "--show-toplevel")).resolve()
    paths = []
    for value in args.paths:
        path = (root / value).resolve()
        if not path.is_relative_to(root):
            raise ValueError("checkpoint路径须在当前仓库内")
        if any(part.lower() in {".git", ".env", ".venv-methods", "cache", "private", "githubtoken.txt", "credentials"} for part in path.relative_to(root).parts):
            raise ValueError("凭据、缓存和虚拟环境不进入研究提交")
        paths.append(str(path.relative_to(root)))
    git(root, "add", "--", *paths)
    staged = git(root, "diff", "--cached", "--name-only").splitlines()
    allowed = lambda p: any(p == x or p.startswith(x.rstrip('/') + '/') for x in paths)
    if any(not allowed(p) for p in staged):
        raise ValueError("暂存区有本次路径以外的文件；先由主代理处理")
    if staged:
        git(root, "commit", "-m", args.message)
    sha = git(root, "rev-parse", "HEAD")
    result = {"ok": True, "commit": sha, "saved_files": staged, "pushed": False}
    if args.push:
        branch = git(root, "branch", "--show-current")
        git(root, "push", "origin", "HEAD:refs/heads/" + branch)
        remote = git(root, "ls-remote", "origin", "refs/heads/" + branch).split()[0]
        if remote != sha:
            raise RuntimeError("远端已变化；保留本地提交后同步合并")
        result["pushed"] = True
    return result


def register_cli(subparsers):
    p = subparsers.add_parser("checkpoint", help="主代理串行提交具体研究文件")
    p.add_argument("--message", required=True)
    p.add_argument("--paths", nargs="+", required=True, help="相对仓库根目录的明确路径")
    p.add_argument("--push", action="store_true")
    p.set_defaults(func=checkpoint)
