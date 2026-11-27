#!/usr/bin/env python3
"""Install the locked methods environment, without cloning upstream repositories."""
import argparse
import os
from pathlib import Path
import subprocess
import sys
import venv


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--environment", default=".venv-methods")
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--wheelhouse", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    destination = (root / args.environment).resolve()
    if not destination.is_relative_to(root):
        parser.error("environment须位于当前仓库")
    if args.offline and not args.wheelhouse:
        parser.error("offline需指定已有wheelhouse")
    executable = destination / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if not executable.exists():
        venv.EnvBuilder(with_pip=True).create(destination)
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
