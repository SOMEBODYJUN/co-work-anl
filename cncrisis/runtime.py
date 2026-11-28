"""Bind a stable research identity and report real work before completion.

This is a checkpoint/acceptance interface, not an LLM scheduler. Economic and
scientific review is performed by researchers and recorded against file hashes.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import subprocess
import uuid

from . import engine

ACTOR = re.compile(r"[A-Za-z0-9][A-Za-z0-9_. -]{0,63}\Z")
ACCEPTANCE = "research/acceptance.json"
DELIVERABLES = ("formal/report.md", "formal/calculator.html",
                "formal/judgments.json", "formal/scenarios.json", "research/final_review.md")
CHECKS = ("sources", "frameworks", "models", "hyperedges", "judgments",
          "household_engine", "offline_ui", "independent_review", "fresh_restore")
REPORT_DELIVERABLES = ('formal/report.md', 'formal/judgments.json',
                       'research/thinking_context.txt', 'research/article_selection.json',
                       'research/question_map.json', 'research/final_review.md')
REPORT_CHECKS = ('sources', 'frameworks', 'coverage', 'models', 'hyperedges', 'judgments',
                 'editorial', 'independent_review', 'fresh_restore')


def checked_actor(value):
    if not ACTOR.fullmatch(value) or value.endswith(" "):
        raise argparse.ArgumentTypeError("身份号须为1—64位ASCII字母、数字、点、下划线、连字符或普通空格，首位为字母或数字，末位不能是空格")
    return value


def location(workspace):
    result = subprocess.run(["git", "-C", str(workspace), "rev-parse", "--show-toplevel"],
                            capture_output=True, text=True)
    if result.returncode:
        return {"workspace_key": Path(workspace).name, "branch": None}
    root = Path(result.stdout.strip()).resolve()
    branch = subprocess.run(["git", "-C", str(root), "branch", "--show-current"],
                            capture_output=True, text=True, check=True).stdout.strip()
    if not branch:
        raise engine.EngineError("身份工作区须处于明确分支；先处理detached HEAD")
    return {"workspace_key": str(Path(workspace).relative_to(root)), "branch": branch}


def binding(db, actor):
    saved = db.state.get("runtime")
    if not saved:
        raise engine.EngineError("先运行 session start --actor <原身份号> 绑定或恢复工作区")
    if saved["actor"] != actor:
        raise engine.EngineError(f"本工作区属于 {saved['actor']}；不得改号、截断编号或复用他人工作区")
    if saved["location"] != location(db.root):
        raise engine.EngineError("工作区路径或分支与绑定记录不同；恢复原相对路径和分支，不自动切换")
    return saved


def start(args):
    checked_actor(args.actor)
    # Existing cycles are preserved by initialise; it never starts an update here.
    engine.initialise(argparse.Namespace(workspace=args.workspace, mode="first"))
    with engine.Store(args.workspace) as db:
        db.require()
        if not db.state.get("runtime"):
            db.state["runtime"] = {"schema": 1, "actor": args.actor,
                                   "run_id": uuid.uuid4().hex, "created_at": engine.now(),
                                   "location": location(db.root)}
            db.event("bind_runtime", {"actor": args.actor})
            db.save()
        binding(db, args.actor)
        if getattr(args, 'profile', None) == 'report-first' and not db.report_first():
            db.state['runtime']['profile'] = 'report-first'
            db.state['stages'].pop('s18_calculator', None)
            # Carry the existing receipts into the new dependency contract.
            # New report/editorial work and a fresh final review are still due.
            for stage_id in db.stages():
                receipt = db.state['stages'].get(stage_id)
                if receipt is not None:
                    receipt['dependency_receipts'] = {
                        x: engine.digest(db.state['stages'][x])
                        for x in db.stage_dependencies(stage_id) if x in db.state['stages']}
            db.state['review'] = None
            db.state['release'] = None
            db.event('report_priority', {'calculator_in_scope': False})
            db.save()
        return inspect(db, args.actor)


def acceptance_blockers(db, actor, state):
    problems = []
    review = state["review"] or {}
    reviewed_files = review.get("files", {})
    review_passed = review.get('verdict') == 'pass'
    if not review_passed:
        problems.append('当前版本尚未获发布通过；保留已审范围，继续具体研究/返修')
    release = state["release"] or {}
    try:
        document = engine.read_json(db.path(ACCEPTANCE))
        if not isinstance(document, dict):
            raise engine.EngineError("验收记录须为JSON对象")
        if document.get("schema") != "cncrisis-acceptance.v1":
            problems.append("验收记录schema应为cncrisis-acceptance.v1")
        if document.get("input_kind") != "real_research":
            problems.append("正式完成要求real_research；合成工程演练不充当经济研究完成")
        if document.get("cycle") != state["cycle"]:
            problems.append("验收记录不属于当前研究周期")
        if document.get("author") != actor or (review.get('author') is not None and review.get("author") != actor):
            problems.append("验收作者与实际绑定身份、最终复核作者须一致")
        reviewer = document.get("reviewer")
        if not isinstance(reviewer, str) or not reviewer.strip() or reviewer == actor or reviewer != review.get("reviewer"):
            problems.append("验收复核者须独立于作者，并与最终复核记录一致")
        rows = document.get("checks", [])
        if not isinstance(rows, list) or any(not isinstance(x, dict) for x in rows):
            raise engine.EngineError("checks须为对象列表")
        ids = [row.get("id") for row in rows]
        if any(not isinstance(x, str) for x in ids) or len(ids) != len(set(ids)):
            raise engine.EngineError("每项验收须有唯一文本ID")
        checks = {row["id"]: row for row in rows}
        checks_required = REPORT_CHECKS if db.report_first() else CHECKS
        deliverables = REPORT_DELIVERABLES if db.report_first() else DELIVERABLES
        for key in checks_required:
            row = checks.get(key, {})
            if row.get("verdict") != "pass":
                problems.append(f"验收未通过: {key}")
            evidence = row.get("evidence")
            if not isinstance(evidence, str) or not evidence.strip():
                problems.append(f"须记录实际检查、结果和采用范围: {key}")
            paths = row.get("artifacts")
            if not isinstance(paths, list) or not paths or any(not isinstance(p, str) for p in paths):
                problems.append(f"须绑定检查证据文件: {key}")
                continue
            for path in paths:
                # Resolve even unreviewed paths, rejecting traversal/symlink escapes.
                db.path(path)
                if review_passed and path not in reviewed_files:
                    problems.append(f"验收证据未进入当前复核快照: {key}: {path}")
        required = {*deliverables, ACCEPTANCE}
        if review_passed and not required.issubset(reviewed_files):
            problems.append("当前复核缺少必要交付物或验收记录: " + ", ".join(sorted(required - reviewed_files.keys())))
        published = deliverables[:-1] if db.report_first() else deliverables[:4]
        missing_release = set(published) - release.get("files", {}).keys()
        if review_passed and missing_release:
            problems.append("正式发布未包含: " + ", ".join(sorted(missing_release)))
    except (engine.EngineError, TypeError) as exc:
        problems.append(str(exc))
    return problems


def inspect(db, actor):
    saved = binding(db, actor)
    state = engine.status_result(db)
    blockers = []
    if state["remaining_stages"]:
        blockers.append({"kind": "stages", "items": state["remaining_stages"]})
    unresolved = state["graph"]["unresolved"] + state["graph"]["unresolved_edges"]
    if unresolved:
        blockers.append({"kind": "graph", "items": unresolved})
    pending = [p["id"] for p in db.state["proposals"].values() if p["status"] == "pending"]
    if pending:
        blockers.append({"kind": "proposals", "items": pending})
    if not state["release"] or not state["release"].get("current"):
        blockers.append({"kind": "release", "items": ["完成当前版本独立复核并发布；旧通过不能覆盖新修改"]})
    acceptance = acceptance_blockers(db, actor, state)
    if acceptance:
        blockers.append({"kind": "substantive_acceptance", "items": acceptance})
    complete = not blockers
    remaining = state["remaining_stages"]
    if complete:
        action = "当前周期已验收，可停止；新证据或新的研究任务再进入update周期"
    elif remaining:
        action = "完成或修复 " + next(iter(remaining)) + " 的实质产物，继续当前周期"
    elif unresolved or pending:
        action = "研究并裁决未决机制和提案，修订受影响产物后重新登记阶段"
    else:
        action = "修复验收缺项，重新提交受影响阶段、独立复核与正式发布"
    return {"actor": actor, "run_id": saved["run_id"], "workspace": str(db.root),
            "profile": saved.get('profile', 'legacy-report-and-calculator'),
            "mode": state["mode"], "cycle": state["cycle"], "complete": complete,
            "next_action": action, "blockers": blockers,
            "completed_stages": state["completed_stages"],
            "latest_event": db.state["history"][-1] if db.state["history"] else None}


def progress(args):
    with engine.Store(args.workspace) as db:
        db.require()
        return inspect(db, args.actor)


def register_cli(subparsers):
    parser = subparsers.add_parser("session", help="固定身份恢复；实质验收通过后才完成")
    commands = parser.add_subparsers(dest="session_command", required=True)
    for name, handler in (("start", start), ("next", progress), ("check", progress)):
        command = commands.add_parser(name)
        command.add_argument("--actor", required=True, type=checked_actor)
        if name == 'start':
            command.add_argument('--profile', choices=['report-first'],
                                 help='报告/思维/覆盖优先；移除计算器与离线UI依赖')
        command.set_defaults(func=handler)
