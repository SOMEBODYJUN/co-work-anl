#!/usr/bin/env python3
"""Install the locked methods environment, without cloning upstream repositories."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import venv


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--environment", default=".venv-methods")
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--wheelhouse", type=Path)
    parser.add_argument("--benchmark", action="store_true", help="Also install the optional capacity benchmark dependencies")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    destination = (root / args.environment).resolve()
    if not destination.is_relative_to(root):
        parser.error("environment须位于当前仓库")
    if args.offline and not args.wheelhouse:
        parser.error("offline需指定已有wheelhouse")
    executable = destination / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if not executable.exists():
        try:
            venv.EnvBuilder(with_pip=True).create(destination)
        except subprocess.CalledProcessError:
            # Some Codespaces system Pythons omit ensurepip. Keep this local
            # environment and use a host pip's --python support below.
            venv.EnvBuilder(with_pip=False).create(destination)
    pip_available = subprocess.run([str(executable), "-m", "pip", "--version"],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
    if not pip_available:
        candidates = dict.fromkeys(p for p in [sys.executable, shutil.which("python"), shutil.which("python3")] if p)
        for candidate in candidates:
            probe = subprocess.run([candidate, "-m", "pip", "--version"],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if probe.returncode == 0:
                command = [candidate, "-m", "pip", "--python", str(executable), "install", "pip"]
                if args.offline:
                    command += ["--no-index", "--find-links", str(args.wheelhouse.resolve())]
                subprocess.run(command, cwd=root, check=True)
                break
        else:
            raise SystemExit("当前Python没有ensurepip，也未找到带pip的宿主Python；使用仓库的Python 3.12开发容器后重试。")
    requirement = root / ("requirements-benchmark.txt" if args.benchmark else "requirements-methods-lock.txt")
    if not requirement.exists():
        requirement = root / "requirements-methods.txt"
    if not requirement.exists():
        raise SystemExit("缺少requirements-methods.txt")
    command = [str(executable), "-m", "pip", "install", "-r", str(requirement)]
    if args.offline:
        command += ["--no-index", "--find-links", str(args.wheelhouse.resolve())]
    subprocess.run(command, cwd=root, check=True)
    subprocess.run([str(executable), "crisis.py", "methods", "doctor"], cwd=root, check=True)
    print("下一步：读取 prompts/04_LAUNCH.md，执行首轮20阶段。")


if __name__ == "__main__":
    main()
