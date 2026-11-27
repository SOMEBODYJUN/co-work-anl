#!/usr/bin/env python3
"""One entry point for research, provenance, causal revisions, and methods."""
import argparse
import json
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser(description="中国经济危机研究工作台")
    parser.add_argument("--workspace", type=Path, default=Path("work/current"))
    commands = parser.add_subparsers(dest="command", required=True)
    from cncrisis import engine, methods, collect, gitops, analysts, compute
    for module in (engine, methods, collect, gitops, analysts, compute):
        module.register_cli(commands)
    args = parser.parse_args()
    args.workspace = args.workspace.resolve()
    try:
        result = args.func(args)
        if result is not None:
            print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    except (ValueError, RuntimeError, OSError, KeyError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
