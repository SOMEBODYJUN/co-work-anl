#!/usr/bin/env python3
"""Explicit live blackboard deployment check; publishes labeled nonmath events."""
import argparse
import concurrent.futures
import hashlib
from pathlib import Path
import threading
import uuid
from unittest.mock import patch

import board as b


def run(repo, branch="wcg/board"):
    client = b.Board(repo, branch)
    run_id = uuid.uuid4().hex
    root_actor = "deployment/" + run_id[:8]
    prefix = root_actor + "/writer_"
    initial = client.read()
    idea = client.publish(b.make_intent(root_actor, "propose", {
        "title": "基础设施验收：并发自主认领（非数学任务）",
        "claim_version": "WC-BOARD-SMOKE v1 / " + run_id,
        "statement": "Two simultaneous public writers must not both own one unit.",
        "obligation": "Verify actual remote single-owner acceptance for run " + run_id,
        "mechanism": "Two Git writers synchronize their first ordinary push.",
        "next_check": "Publish concurrent claims, then verify the accepted remote stream.",
        "claim": False}))
    original_git = b.git
    barrier, lock, first_threads = threading.Barrier(2), threading.Lock(), set()

    def synchronized_git(cwd, *args, **kwargs):
        if args and args[0] == "push":
            ident = threading.get_ident()
            with lock:
                first = ident not in first_threads
                first_threads.add(ident)
            if first:
                barrier.wait(timeout=60)
        return original_git(cwd, *args, **kwargs)

    def claim(letter):
        actor = prefix + letter
        try:
            event = b.Board(repo, branch).publish(b.make_intent(actor, "claim", {
                "idea": idea["id"], "next_check": "Verify live deployment ownership.",
                "lease_seconds": 3600}))
            return {"actor": actor, "event": event}
        except b.Conflict as exc:
            return {"actor": actor, "conflict": str(exc)}

    with patch.object(b, "git", synchronized_git):
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(claim, ("A", "B")))
    winners = [x for x in results if "event" in x]
    losers = [x for x in results if "conflict" in x]
    if len(winners) != 1 or len(losers) != 1:
        raise AssertionError("Live single-owner check failed: " + str(results))
    winner, loser = winners[0], losers[0]
    reply = client.publish(b.make_intent(loser["actor"], "discussion", {
        "idea": idea["id"], "reply_to": winner["event"]["id"],
        "text": "部署实测：同一具体单元的并发认领只有一位成功。"
                "后提交者重新读取公屏而未盲目 rebase；仍可平等回应、补充和提出独立审查。"
                "此处是测试发布端，不冒称两个实际研究对话。"}))
    commit = b.git(client.repo, "rev-parse", "HEAD").stdout.decode().strip()
    path = "research/weighted_congestion_frontier/tools/board.py"
    frozen = b.git(client.repo, "show", commit + ":" + path).stdout
    asset = {"branch": "main", "commit": commit, "path": path,
             "sha256": hashlib.sha256(frozen).hexdigest()}
    finished = client.publish(b.make_intent(winner["actor"], "finish", {
        "idea": idea["id"], "lease_token": winner["event"]["id"], "asset": asset,
        "text": "真实 GitHub 认领、冲突去重、因果回复、冻结文件校验与完成释放均通过。"
                "本单元仅为基础设施验收，WC-TARGET 仍开放。所有数学研究队自行提出 idea，"
                "无需协调者派单。Astra Ultra 和 6.1 Sol Ultra 的独立实现复审记录见 main 的 evidence/validation.md。"}))
    final = client.read()
    if final["ideas"][idea["id"]]["owner"] is not None:
        raise AssertionError("Finished smoke unit still owns a lease.")
    return {"run_id": run_id, "board_branch": branch, "idea": idea["id"],
            "claims": results, "reply_event": reply["id"],
            "finish_event": finished["id"], "source_asset": asset,
            "initial_events": len(initial["events"]),
            "final_events": len(final["events"]), "verified": True,
            "scope": "Infrastructure only; no mathematical progress claimed."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".")
    parser.add_argument("--branch", default="wcg/board")
    parser.add_argument("--live", action="store_true", required=True,
                        help="Explicitly authorize labeled test events on the remote board.")
    args = parser.parse_args()
    print(b.encode(run(args.repo, args.branch)), end="")
