"""Prepare a fresh original-layout runtime from this published evidence only.

Copies the25 actually read dependency files and the frozen primary schema.
Creates only a comment-only work.py path marker; no stub modules or math runs.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil

HERE = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_relative(value):
    path = Path(value)
    assert not path.is_absolute() and ".." not in path.parts
    return path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime", required=True, type=Path)
    args = parser.parse_args()
    runtime = args.runtime.resolve()
    # Reject an existing directory so that no old files or reports are replaced.
    runtime.mkdir(parents=True, exist_ok=False)
    manifest = json.loads((HERE / "dependency-manifest.json").read_text())
    copied = []
    dependencies = manifest["old_verifier_actual_read_dependencies"]
    assert len(dependencies) == 25
    for entry in dependencies:
        source = HERE / safe_relative(entry["preserved_path"])
        assert digest(source) == entry["sha256"]
        target = runtime / safe_relative(entry["path"])
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        assert digest(target) == entry["sha256"]
        copied.append({"path": entry["path"], "sha256": entry["sha256"]})
    primary = json.loads((HERE / "source-manifest.json").read_text())
    schema = next(entry for entry in primary if entry["id"] == "78cf2169b99848113caa")
    source = HERE / safe_relative(schema["preserved_path"])
    assert digest(source) == schema["sha256"]
    target = runtime / safe_relative(schema["path"])
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    assert digest(target) == schema["sha256"]
    copied.append({"path": schema["path"], "sha256": schema["sha256"]})
    marker = runtime / "work.py"
    marker.write_text("# Inert path-discovery marker for original mathematics; never executed.\n")
    report = {"runtime": str(runtime), "dependency_files": 25,
              "primary_schema_files": 1, "copied_files": copied,
              "marker": "work.py contains only a comment; no controller or stub module",
              "mathematical_functions_executed": 0}
    (runtime / "runtime-preparation.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: value for key, value in report.items()
                      if key != "copied_files"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
