"""Copy the statically selected default runtime, checking all frozen bytes.

This does not execute/import the original program or run an optimizer. The
historical one-run evidence used a larger shared tree, recorded separately.
"""
from argparse import ArgumentParser
from hashlib import sha256
from pathlib import Path
import json
import shutil


def main():
    parser = ArgumentParser()
    parser.add_argument("--dest", type=Path, required=True)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    dest = args.dest.resolve()
    if dest.exists():
        raise ValueError("Choose a new destination; existing trees are not overwritten")
    manifest = json.loads((here / "source-manifest.json").read_text())
    sources = manifest["default_runtime_sources"]
    prepared = []
    for source in sources:
        stored = (here / source["preserved_as"]).resolve()
        relative = Path(source["original_path"])
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError("Nonlocal original path")
        data = stored.read_bytes()
        assert len(data) == source["bytes"]
        assert sha256(data).hexdigest() == source["sha256"]
        prepared.append((stored, relative, source))
    dest.mkdir(parents=True)
    (dest / "work.py").write_text("# Inert root marker; never execute this file.\n")
    for stored, relative, source in prepared:
        target = dest / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(stored, target)
        assert sha256(target.read_bytes()).hexdigest() == source["sha256"]
    entry = dest / manifest["primary"]["original_path"]
    print(json.dumps({"status": "MATERIALIZED_HASH_CHECKED_ONLY", "files": len(sources),
                      "bytes": sum(s["bytes"] for s in sources), "dest": str(dest),
                      "optional_future_argv": ["python", "-B", str(entry), "--verify"],
                      "original_main_calls": 0, "LP_calls": 0}, indent=2))


if __name__ == "__main__":
    main()
