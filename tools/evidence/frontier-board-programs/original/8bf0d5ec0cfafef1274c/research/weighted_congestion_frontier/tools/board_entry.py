#!/usr/bin/env python3
"""Board CLI with the same external credential-file setup as checkpoint.sh."""
import argparse
import os
from pathlib import Path
import subprocess
import sys

import checkpoint as c


def main():
    parser = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
    parser.add_argument("--repo", default=".")
    parser.add_argument("--token-file")
    args, remaining = parser.parse_known_args()
    tools = Path(__file__).resolve().parent
    command = [sys.executable, str(tools / "board.py"), "--repo", args.repo, *remaining]
    # Help needs neither a clone nor credential initialization.
    if "--help" in remaining or "-h" in remaining:
        return subprocess.call(command)
    repo = Path(c.value(args.repo, "rev-parse", "--show-toplevel"))
    credential = (args.token_file or os.environ.get("WCG_CHECKPOINT_TOKEN_FILE") or
                  c.git(repo, "config", "--local", "--get", "wcg.tokenFile",
                        check=False).stdout.decode().strip())
    env = {k: v for k, v in os.environ.items() if k not in c.ROUTING}
    env["GIT_TERMINAL_PROMPT"] = "0"
    if credential:
        path = Path(credential).resolve()
        if path.is_relative_to(repo):
            raise c.Stop("Keep the credential file outside the repository.")
        c.token(path)  # Validate without printing or storing its contents.
        if args.token_file:
            c.git(repo, "config", "--local", "wcg.tokenFile", str(path))
        env.update(GIT_ASKPASS=str(tools / "checkpoint.py"),
                   WCG_CHECKPOINT_TOKEN_FILE=str(path), WCG_CHECKPOINT_ASKPASS="1")
    return subprocess.call(command, env=env)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (c.Stop, OSError, ValueError) as exc:
        message = c.SECRET.sub(b"[REDACTED]", str(exc).encode()).decode()
        print("ERROR: " + message, file=sys.stderr)
        raise SystemExit(2)
