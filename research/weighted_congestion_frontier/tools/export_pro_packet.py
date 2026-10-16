#!/usr/bin/env python3
"""Pro任务与数学简报的单提交冻结导出器。

All content, source mappings and review statuses are read with ``git show``.
The output directory and ZIP must be new paths outside the repository.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import quote, unquote, urlsplit
import zipfile

BASE = "research/weighted_congestion_frontier/"
MAPPING = BASE + "PRO_BRIEF_SOURCES.json"
SCRIPT = BASE + "tools/export_pro_packet.py"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def safe_path(value):
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        raise ValueError("invalid repository/archive path")
    p = PurePosixPath(value)
    if p.is_absolute() or any(x in ("", ".", "..") for x in value.split("/")):
        raise ValueError("unsafe repository/archive path: " + value)
    return value


def git(repo, *args):
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True)
    if result.returncode:
        raise ValueError("Git read failed: " + " ".join(args[:2]) + ": " +
                         result.stderr.decode("utf-8", "replace").strip())
    return result.stdout


def frozen_reader(repo, commit):
    cache = {}

    def read(path):
        safe_path(path)
        if not path.startswith("research/"):
            raise ValueError("source must be under research/: " + path)
        if path not in cache:
            cache[path] = git(repo, "show", commit + ":" + path)
        return cache[path]
    return read


def extract_task(data):
    text = data.decode("utf-8")
    blocks = re.findall(r"^~~~text[ \t]*\r?\n(.*?)^~~~[ \t]*(?:\r?\n|$)",
                        text, flags=re.M | re.S)
    if len(blocks) != 1:
        raise ValueError("PRO_ATTACK must contain exactly one ~~~text block")
    return (blocks[0].rstrip("\r\n") + "\n").encode("utf-8")


def rewrite_links(data, source, repository, commit):
    """Change Markdown link destinations only; keep code fences/inline code."""
    changed = []

    def target(value):
        angled = value.startswith("<") and value.endswith(">")
        raw = value[1:-1] if angled else value
        parts = urlsplit(raw)
        if parts.scheme or parts.netloc or raw.startswith(("#", "/")):
            return value
        if not parts.path:
            return value
        path_part = re.sub(r"\\([() ])", r"\1", parts.path)
        if "\\" in unquote(path_part):
            raise ValueError("unsafe Markdown link in " + source)
        dest = posixpath.normpath(posixpath.join(posixpath.dirname(source),
                                               unquote(path_part)))
        safe_path(dest)
        kind = "tree" if parts.path.endswith("/") else "blob"
        url = repository.rstrip("/") + "/" + kind + "/" + commit + "/" + quote(dest, safe="/")
        if parts.query:
            url += "?" + parts.query
        if parts.fragment:
            url += "#" + parts.fragment
        changed.append({"original": raw, "repository_path": dest})
        return "<" + url + ">" if angled else url

    inline = re.compile(r"\[[^\]\n]*\]\(")
    reference = re.compile(r"^(\s{0,3}\[[^\]\n]+\]:\s*)(<[^>\n]+>|\S+)")

    def prose(piece):
        result, cursor = [], 0
        for match in inline.finditer(piece):
            begin = match.end()
            if begin < cursor:
                continue
            end = begin
            if piece[begin:begin+1] == "<":
                close = piece.find(">", begin+1)
                if close == -1:
                    continue
                end = close+1
            else:
                depth = 0
                while end < len(piece):
                    char = piece[end]
                    if char == "\\" and end+1 < len(piece):
                        end += 2
                        continue
                    if (char.isspace() or char == ")") and depth == 0:
                        break
                    depth += (char == "(") - (char == ")")
                    end += 1
            if end == begin:
                continue
            result.extend((piece[cursor:begin], target(piece[begin:end])))
            cursor = end
        result.append(piece[cursor:])
        piece = "".join(result)
        return reference.sub(lambda m: m[1] + target(m[2]), piece)

    lines, fence = [], None
    for line in data.decode("utf-8").splitlines(keepends=True):
        mark = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if mark:
            if fence is None:
                fence = (mark[1][0], len(mark[1]))
            elif mark[1][0] == fence[0] and len(mark[1]) >= fence[1]:
                fence = None
            lines.append(line)
            continue
        if fence:
            lines.append(line)
            continue
        # Split out complete inline-code spans, including multi-backtick spans.
        result, start = [], 0
        for code in re.finditer(r"(`+)(.*?)(?<!`)\1(?!`)", line):
            result.extend((prose(line[start:code.start()]), code[0]))
            start = code.end()
        result.append(prose(line[start:]))
        lines.append("".join(result))
    return "".join(lines).encode("utf-8"), changed


def external_new_path(value, repo):
    raw = Path(value).expanduser()
    if os.path.lexists(raw):
        raise ValueError("refusing existing output: " + str(raw))
    path = raw.resolve()
    if path == repo or repo in path.parents:
        raise ValueError("output must be outside repository: " + str(path))
    if os.path.lexists(path):
        raise ValueError("refusing existing output: " + str(path))
    if not path.parent.is_dir():
        raise ValueError("output parent does not exist: " + str(path.parent))
    return path


def prepare(repo, commit):
    read = frozen_reader(repo, commit)
    mapping_bytes = read(MAPPING)
    mapping = json.loads(mapping_bytes)
    math_commit = mapping["brief_mathematical_source_commit"]
    if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", math_commit):
        raise ValueError("mathematical source snapshot must be a full commit hash")
    mathematical_read = frozen_reader(repo, math_commit)
    repository = mapping["source_repository"].rstrip("/")
    parsed = urlsplit(repository)
    if parsed.scheme != "https" or parsed.netloc != "github.com" or len(parsed.path.strip("/").split("/")) != 2:
        raise ValueError("source_repository must be a credential-free GitHub repository URL")
    sources = mapping["sources"]
    expected_labels = {"S" + str(i) for i in range(21)}
    if len(sources) != 21 or {s["id"] for s in sources} != expected_labels:
        raise ValueError("source mapping must register S0 through S20 exactly once")
    status_bytes = read(mapping["review_status_path"])
    status_entries = json.loads(status_bytes)["entries"]
    statuses = {entry["id"]: entry for entry in status_entries}
    if len(statuses) != len(status_entries):
        raise ValueError("duplicate Claim IDs in frozen review_status.json")
    task_path, brief_path = mapping["task_source"], mapping["brief_source"]
    task_source, brief = read(task_path), read(brief_path)
    if sha(brief) != mapping["reviewed_brief_sha256"]:
        raise ValueError("PRO_BRIEF differs from its reviewed source mapping hash")
    if sha(task_source) != mapping["reviewed_task_source_sha256"]:
        raise ValueError("PRO_ATTACK differs from its reviewed source mapping hash")
    content = {"TASK.md": extract_task(task_source), "PRO_BRIEF.md": brief}
    files = [
        {"path": "TASK.md", "source_path": task_path, "original_source_sha256": sha(task_source),
         "transform": "extract complete single ~~~text body; normalize final newline"},
        {"path": "PRO_BRIEF.md", "source_path": brief_path, "original_source_sha256": sha(brief),
         "transform": "verbatim"},
    ]
    labels_used = set(re.findall(r"\bS\d+\b", (content["TASK.md"] + brief).decode("utf-8")))
    if not labels_used <= expected_labels:
        raise ValueError("unregistered S labels: " + ", ".join(sorted(labels_used - expected_labels)))
    references = re.findall(r"^\[(S\d+)\]:\s*(\S+)\s*$", brief.decode("utf-8"), re.M)
    if len(references) != len(sources) or {label for label, _ in references} != expected_labels:
        raise ValueError("PRO_BRIEF must define S0-S20 exactly once")
    reference_urls = dict(references)
    for source in sources:
        expected = repository + "/blob/" + math_commit + "/" + source["source_files"][0]["path"]
        if unquote(reference_urls[source["id"]]) != expected:
            raise ValueError("brief source link differs from mapping: " + source["id"])
    section_sources = []
    for source in sources:
        item = {k: v for k, v in source.items() if k != "optional_path"}
        item["source_files"] = []
        for p in source["source_files"]:
            original = read(p["path"])
            mathematical_original = mathematical_read(p["path"])
            if original != mathematical_original:
                raise ValueError("source differs from reviewed mathematical snapshot: " + p["path"])
            item["source_files"].append({**p, "sha256": sha(original),
                                         "mathematical_source_sha256": sha(mathematical_original),
                                         "mathematical_source_commit": math_commit})
        item["reviews"] = [{"path": p, "document_sha256": sha(read(p)),
                            "frozen_url": repository + "/blob/" + commit + "/" + quote(p, safe="/")}
                           for p in source["review_paths"]]
        missing = set(source["claim_ids"]) - statuses.keys()
        if missing:
            raise ValueError("Claim IDs absent from frozen review ledger: " + ", ".join(sorted(missing)))
        # Copy the actual ledger records; never infer status from a README/review vote.
        item["claim_review_status"] = [statuses[c] for c in source["claim_ids"]]
        section_sources.append(item)
        if "optional_path" in source:
            output = safe_path(source["optional_path"])
            if not output.startswith("optional/") or output in content:
                raise ValueError("invalid/duplicate optional output: " + output)
            path = source["source_files"][0]["path"]
            original = read(path)
            converted, changes = rewrite_links(original, path, repository, math_commit)
            content[output] = converted
            files.append({"path": output, "source_path": path, "source_label": source["id"],
                          "original_source_sha256": sha(original),
                          "transform": "Markdown relative link destinations to frozen GitHub URLs only",
                          "rewritten_link_count": len(changes)})
    if len([p for p in content if p.startswith("optional/")]) != 19:
        raise ValueError("expected the nineteen S2-S20 optional mathematical source files")
    for entry in files:
        entry["sha256"] = sha(content[entry["path"]])
        entry["bytes"] = len(content[entry["path"]])
    manifest = {
        "format_version": 1, "source_repository": repository, "exported_commit": commit,
        "brief_mathematical_source_commit": math_commit,
        "default_reading": ["TASK.md", "PRO_BRIEF.md"],
        "optional_policy": "Mathematical source texts only; all assumptions remain in force. Optional does not mean universally applicable.",
        "review_hash_note": "Review document hashes below identify their bytes at exported_commit. Historical proof freeze hashes quoted inside those reviews do not claim to hash current source files.",
        "brief_snapshot_note": "PRO_BRIEF is copied verbatim, including its declared mathematical snapshot and absolute source links. Every selected mathematical source was byte-compared between exported_commit and brief_mathematical_source_commit. Optional relative links point to the latter; status records come from exported_commit.",
        "mapping": {"path": MAPPING, "sha256": sha(mapping_bytes)},
        "brief_reviews": [{"path": p, "document_sha256": sha(read(p))}
                          for p in mapping["brief_review_paths"]],
        "review_status_source": {"path": mapping["review_status_path"], "sha256": sha(status_bytes)},
        "exporter_source": {"path": SCRIPT, "sha256": sha(read(SCRIPT))},
        "sources": section_sources, "files": files,
        "manifest_integrity_note": "files hashes every payload except this self-referential manifest; the exporter additionally verifies the manifest and every ZIP entry against the prepared bytes after extraction.",
    }
    content["MANIFEST.json"] = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    return content


def write_and_verify(content, output, archive):
    output.mkdir(mode=0o700)
    archive_created = False
    try:
        for name, data in content.items():
            target = output / safe_path(name)
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as handle:
                handle.write(data)
        with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as handle:
            archive_created = True
            for name in sorted(content):
                entry = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                entry.compress_type = zipfile.ZIP_DEFLATED
                entry.external_attr = 0o100644 << 16
                handle.writestr(entry, content[name], compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        with tempfile.TemporaryDirectory(prefix="pro-packet-check-", dir=output.parent) as temp:
            with zipfile.ZipFile(archive) as handle:
                names = handle.namelist()
                if len(names) != len(set(names)) or set(names) != set(content):
                    raise ValueError("archive member set mismatch")
                for name in names:
                    safe_path(name)
                    if handle.read(name) != content[name]:
                        raise ValueError("archive content mismatch: " + name)
                handle.extractall(temp)
            extracted = Path(temp)
            manifest = json.loads((extracted / "MANIFEST.json").read_bytes())
            for entry in manifest["files"]:
                if sha((extracted / entry["path"]).read_bytes()) != entry["sha256"]:
                    raise ValueError("extracted manifest hash mismatch: " + entry["path"])
            for name, data in content.items():
                if (extracted / name).read_bytes() != data or (output / name).read_bytes() != data:
                    raise ValueError("extracted/output reread mismatch: " + name)
    except Exception:
        if archive_created:
            archive.unlink(missing_ok=True)
        shutil.rmtree(output)
        raise


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--zip", required=True, dest="archive")
    args = parser.parse_args(argv)
    try:
        repo = Path(args.repo).expanduser().resolve()
        top = Path(git(repo, "rev-parse", "--show-toplevel").decode().strip()).resolve()
        if repo != top:
            raise ValueError("--repo must be the repository root")
        commit = git(repo, "rev-parse", "--verify", "--end-of-options", args.commit + "^{commit}").decode().strip()
        if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", commit):
            raise ValueError("invalid resolved commit")
        output = external_new_path(args.output_dir, repo)
        archive = external_new_path(args.archive, repo)
        if archive == output or output in archive.parents or archive in output.parents:
            raise ValueError("output directory and ZIP must be separate paths")
        content = prepare(repo, commit)
        write_and_verify(content, output, archive)
        print(json.dumps({"status": "verified", "frozen_commit": commit, "files": len(content),
                          "output_dir": str(output), "zip": str(archive),
                          "zip_sha256": sha(archive.read_bytes()),
                          "manifest_sha256": sha(content["MANIFEST.json"])}, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, KeyError, UnicodeError, json.JSONDecodeError) as error:
        print("export_pro_packet: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
