#!/usr/bin/env python3
"""Validate the current goal, three roles, old-save isolation and retired bytes."""
from __future__ import annotations
import ast
import hashlib
import json
from pathlib import Path
import re
ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise ValueError(detail)


def local(path: str) -> Path:
    candidate = (ROOT / path).resolve()
    require(candidate.is_relative_to(ROOT) and candidate.is_file(), ("missing active entry", path))
    return candidate


def literal_assignment(path: str, name: str):
    tree = ast.parse(local(path).read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return ast.literal_eval(node.value)
    raise ValueError(("missing routing constant", path, name))


def prompt_body(path: str) -> str:
    matches = re.findall(r"(?ms)^~~~text\n(.*?)^~~~\s*$", local(path).read_text(encoding="utf-8"))
    require(len(matches) == 1, ("expected one complete pasteable task", path))
    return matches[0]


def check() -> dict:
    manifest = json.loads(local("research/active_research.json").read_text())
    require(manifest["schema_version"] == 2, "unsupported active routing contract")
    save, target = manifest["default_save"], manifest["target_id"]
    program, submitter = manifest["program"], manifest["submitter"]
    require(literal_assignment(program, "DEFAULT_SAVE") == save,
            "standalone work.py default disagrees with the active topic")
    require(literal_assignment(submitter, "DEFAULT_SAVE") == save,
            "unbound checkpoint default disagrees with the active topic")
    entries = literal_assignment(program, "RESEARCH_ENTRIES")
    require(entries[save] == {"research_entry": manifest["mathematical_entry"],
                             "research_prompt": manifest["prompt"],
                             "research_runbook": manifest["runbook"]},
            "start receipt points outside the active mathematical entry/prompt")
    for old_save, old_entry in manifest["legacy_entries"].items():
        require(entries.get(old_save) == old_entry, ("legacy save routing changed", old_save))
    roles = manifest["roles"]
    require(set(roles) == {"boss", "cleaner", "editor"} and len(set(roles.values())) == 3
            and manifest["role_prompts"] == list(roles.values()),
            "exactly three unique current roles are required")
    require(literal_assignment(program, "ROLE_PROMPTS") == roles,
            "role receipt disagrees with the three current prompts")
    require(roles["boss"] == manifest["prompt"], "boss prompt is not the current target")
    all_paths = list(dict.fromkeys(manifest["active_entrypoints"] + manifest["role_prompts"] +
                                   [manifest["runbook"], manifest["mathematical_entry"]]))
    stale = (r"当前(?:唯一)?主攻(?:是|：|:)?\s*(?:\*\*)?\[?(?:加权|UM-TARGET|一般不相关)",
             r"默认存档(?:为|是)?\s*`?(?:shared|unrelated-machines)",
             r"所有(?:研究)?对话(?:共同解决|自主推进)\s*WC-TARGET")
    links = 0
    mathematical_targets = set()
    for path in all_paths:
        file = local(path)
        text = file.read_text(encoding="utf-8")
        require(target in text and save in text, ("active entry lacks topic/scope", path))
        for pattern in stale:
            require(not re.search(pattern, text), ("stale unconditional topic instruction", path, pattern))
        prose = re.sub(r"(?ms)^(```|~~~).*?^\1\s*$", "", text)
        for match in re.finditer(r"(?<!\\)\[[^\]\n]+\]\(([^)\s]+)\)", prose):
            ref = match.group(1).strip("<>")
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", ref) or ref.startswith("#"):
                continue
            dest = (file.parent / ref.split("#", 1)[0]).resolve()
            require(dest.is_relative_to(ROOT) and dest.exists(), ("broken active navigation", path, ref))
            links += 1
            if path == manifest["mathematical_entry"]:
                mathematical_targets.add(dest)
    mathematical_entry = local(manifest["mathematical_entry"])
    mathematical_files = {p.resolve() for p in mathematical_entry.parent.rglob("*.md")}
    missing = mathematical_files - {mathematical_entry} - mathematical_targets
    require(not missing, ("active mathematical map omits files",
                          sorted(p.relative_to(ROOT).as_posix() for p in missing)))
    for path in roles.values():
        body = prompt_body(path)
        for marker in (target, save, "完整历史", "纯", "OPEN", "work.py", "checkpoint"):
            require(marker in body, ("incomplete current role task", path, marker))
    for path, destination in manifest["compatibility_redirects"].items():
        text = local(path).read_text()
        require("~~~text" not in text and "```text" not in text, ("retired role still duplicates a full task", path))
        require(Path(destination).name in text, ("retired role has no current redirect", path))
    retirement = json.loads(local(manifest["retired_operations_manifest"]).read_text())
    require(retirement["base_commit"] and retirement["entries"], "retirement lacks provenance")
    for row in retirement["entries"]:
        require(hashlib.sha256(local(row["archived_path"]).read_bytes()).hexdigest() == row["sha256"],
                ("retired original bytes changed", row["original_path"]))
    return {"target": target, "save": save, "roles": list(roles),
            "checked_entrypoints": len(all_paths), "checked_local_links": links,
            "indexed_mathematical_files": len(mathematical_files),
            "retired_originals_verified": len(retirement["entries"]),
            "legacy_saves_preserved": list(manifest["legacy_entries"])}


if __name__ == "__main__":
    print(json.dumps(check(), ensure_ascii=False))
