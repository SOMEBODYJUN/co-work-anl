#!/usr/bin/env python3
"""Check current-topic routing without changing legacy mathematics or messages."""
from __future__ import annotations

import ast
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise ValueError(detail)


def literal_assignment(path: str, name: str):
    tree = ast.parse((ROOT / path).read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == name for t in node.targets
        ):
            return ast.literal_eval(node.value)
    raise ValueError(("missing routing constant", path, name))


def prompt_body(path: str) -> str:
    content = (ROOT / path).read_text(encoding="utf-8")
    matches = re.findall(r"(?ms)^~~~text\n(.*?)^~~~\s*$", content)
    require(len(matches) == 1, ("expected one complete pasteable task", path))
    return matches[0]


def check_topic_selection(manifest: dict) -> dict:
    target, save = manifest["target_id"], manifest["default_save"]
    require(target == "TOPIC-SELECTION-OR-OPT-v1" and save == "topic-selection",
            "topic selection identity mismatch")
    contract = json.loads((ROOT / "research/topic_selection/active_research.json").read_text())
    require(contract["target_id"] == target and contract["save"] == save
            and contract["branch"] == manifest["branch"]
            and re.fullmatch(r"research/topic-selection-[A-Za-z0-9_.-]+", manifest["branch"]),
            "topic branch contract mismatch")
    legacy = manifest["legacy_default_save"]
    require(literal_assignment(manifest["program"], "DEFAULT_SAVE") == legacy,
            "standalone legacy default changed without an explicit route")
    require(literal_assignment(manifest["submitter"], "DEFAULT_SAVE") == legacy,
            "checkpoint legacy default changed without an explicit route")
    entries = literal_assignment(manifest["program"], "RESEARCH_ENTRIES")
    require(entries[save] == {"research_entry": manifest["mathematical_entry"],
                             "research_prompt": manifest["prompt"]},
            "topic start receipt points outside current entry/prompt")
    require(entries["shared"]["research_prompt"] is None, "legacy shared acquired a new task")
    links = 0
    for path in manifest["active_entrypoints"]:
        file = (ROOT/path).resolve()
        require(file.is_relative_to(ROOT) and file.is_file(), ("missing active entry", path))
        text = file.read_text()
        require(target in text and save in text, ("active entry lacks topic/scope", path))
        for match in re.finditer(r"(?<!\\)\[[^\]\n]+\]\(([^)\s]+)\)", text):
            ref = match.group(1)
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", ref) or ref.startswith("#"):
                continue
            dest = (file.parent/ref.split("#",1)[0]).resolve()
            require(dest.is_relative_to(ROOT) and dest.exists(), ("broken active navigation",path,ref))
            links += 1
    prompt = (ROOT/manifest["prompt"]).read_text()
    for marker in ("原子博弈", "Nash", "公平分配", "广义指派", "gpt-6.1-sol", "ultra",
                   "20天", "12小时", "工具", "分类", "玩具模型", "停止条件", "--branch"):
        require(marker in prompt, ("incomplete topic selection prompt", marker))
    return {"target": target, "save": save, "branch": manifest["branch"],
            "checked_entrypoints": len(manifest["active_entrypoints"]),
            "checked_local_links": links, "legacy_defaults_retained": True}


def check() -> dict:
    manifest = json.loads((ROOT / "research/active_research.json").read_text())
    require(manifest["schema_version"] == 1, "unsupported active routing contract")
    if manifest.get("mode") == "topic-selection":
        return check_topic_selection(manifest)
    save, target = manifest["default_save"], manifest["target_id"]
    program, submitter = manifest["program"], manifest["submitter"]
    require(literal_assignment(program, "DEFAULT_SAVE") == save,
            "standalone work.py default disagrees with the active topic")
    require(literal_assignment(submitter, "DEFAULT_SAVE") == save,
            "unbound checkpoint default disagrees with the active topic")
    entries = literal_assignment(program, "RESEARCH_ENTRIES")
    require(entries[save] == {"research_entry": manifest["mathematical_entry"],
                             "research_prompt": manifest["prompt"]},
            "start receipt points outside the active mathematical entry/prompt")
    # Old clones must not be handed the now-current TEAM compatibility prompt.
    require(entries["shared"]["research_entry"] == manifest["legacy_shared_entry"]
            and entries["shared"]["research_prompt"] is None,
            "legacy shared start must retain its own entry and no new-topic task")
    all_paths = list(dict.fromkeys(manifest["active_entrypoints"] +
                                  list(manifest["role_prompts"]) +
                                  [manifest["prompt"], manifest["runbook"]]))
    links = 0
    stale = (
        r"当前主攻(?:是|：|:)?\s*(?:\*\*)?\[?加权",
        r"所有(?:研究)?对话(?:共同解决|自主推进)\s*WC-TARGET",
        r"默认存档(?:为|是)?\s*`?shared",
        r"shared/未绑定",
    )
    for path in all_paths:
        file = (ROOT / path).resolve()
        require(file.is_relative_to(ROOT) and file.is_file(), ("missing active entry", path))
        text = file.read_text(encoding="utf-8")
        require(target in text and save in text, ("active entry lacks topic/scope", path))
        for pattern in stale:
            require(not re.search(pattern, text), ("stale unconditional topic instruction", path, pattern))
        # Validate repository destinations. Fragments remain prose-level navigation.
        text = re.sub(r"(?ms)^(```|~~~).*?^\1\s*$", "", text)
        for match in re.finditer(r"(?<!\\)\[[^\]\n]+\]\(([^)\s]+)\)", text):
            ref = match.group(1)
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", ref) or ref.startswith("#"):
                continue
            dest = (file.parent / ref.split("#", 1)[0]).resolve()
            require(dest.is_relative_to(ROOT) and dest.exists(), ("broken active navigation", path, ref))
            links += 1
    body = prompt_body(manifest["prompt"])
    require(body == prompt_body(manifest["team_compatibility_prompt"]),
            "TEAM compatibility task has drifted from the complete BOSS task")
    for marker in (target, save, "ε", "总二进制编码长度", "OPT(P)=0",
                   "start --save unrelated-machines", "work.py checkpoint", "work.py dm"):
        require(marker in body, ("incomplete current BOSS task", marker))
    for path in manifest["role_prompts"]:
        text = (ROOT / path).read_text()
        require("WC-TARGET" not in text and "Cd/ln d" not in text,
                ("current role still assigns an old mathematical goal", path))
    return {"target": target, "save": save, "checked_entrypoints": len(all_paths),
            "checked_local_links": links, "complete_boss_and_team_agree": True}


if __name__ == "__main__":
    print(json.dumps(check(), ensure_ascii=False))
