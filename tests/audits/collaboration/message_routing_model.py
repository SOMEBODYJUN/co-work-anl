#!/usr/bin/env python3
"""核对大规模研究协作的定向消息、工作区及负载模型。

这是有限规格模型，不是部署中的聊天后端，也不测试 Work 并发容量。
只使用本地数据，不访问 GitHub，不发送真实消息。
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import tempfile


@dataclass(frozen=True)
class Message:
    save: str
    ident: str
    sender: str
    kind: str
    recipients: frozenset[str] = frozenset()
    mentions: frozenset[str] = frozenset()
    text: str = "待核查的数学发现"


class Model:
    def __init__(self, rosters):
        self.rosters = rosters
        self.messages = {}
        self.public = defaultdict(list)
        self.inbox = defaultdict(list)
        self.conversations = defaultdict(list)
        self.read = defaultdict(set)
        self.adopted = defaultdict(set)
        self.active = set()

    def publish(self, message):
        m = message
        known = self.rosters.get(m.save, set())
        if not m.ident or not m.text.strip() or m.sender not in known:
            raise ValueError("消息身份、正文或来源不合法")
        if not (m.recipients | m.mentions) <= known:
            raise ValueError("收件人必须属于当前研究存档")
        if m.kind == "public":
            if m.recipients:
                raise ValueError("公屏和定向范围不能混淆")
            targets = m.mentions - {m.sender}
        elif m.kind in {"dm", "room"}:
            if m.sender in m.recipients or not m.recipients:
                raise ValueError("定向会话需要其他参与者")
            if m.kind == "dm" and len(m.recipients) != 1:
                raise ValueError("双方私聊只能有一位对端")
            if m.mentions - m.recipients - {m.sender}:
                raise ValueError("私聊内提及不能把内容路由给会话外人员")
            targets = m.recipients
        else:
            raise ValueError("未知通信范围")
        # Validate everything before persisting: invalid requests have no side effects.
        key = (m.save, m.ident)
        if key in self.messages:
            if self.messages[key] != m:
                raise ValueError("不能以同一 ID 重用不同内容")
            return
        self.messages[key] = m
        if m.kind == "public":
            self.public[m.save].append(m.ident)
        else:
            members = tuple(sorted(m.recipients | {m.sender}))
            self.conversations[(m.save, m.kind, members)].append(m.ident)
        for receiver in targets:
            self.inbox[(m.save, receiver)].append(m.ident)


def audit():
    actors = {f"R{i:04d}" for i in range(1, 501)}
    model = Model({"S1": actors, "S2": actors})
    assert len(actors) == 500
    directed_pairs = sum(a != b for a in actors for b in actors)
    assert directed_pairs == 500 * 499
    assert not model.conversations

    model.publish(Message("S1", "m1", "R0001", "dm", frozenset({"R0002"})))
    model.publish(Message("S1", "m2", "R0003", "public",
                          mentions=frozenset({"R0002", "R0004"})))
    model.publish(Message("S1", "m3", "R0005", "room", frozenset({"R0002", "R0006"})))
    model.publish(Message("S2", "m4", "R0001", "dm", frozenset({"R0002"})))
    assert model.inbox[("S1", "R0002")] == ["m1", "m2", "m3"]
    assert model.inbox[("S2", "R0002")] == ["m4"]
    assert model.public["S1"] == ["m2"] and not model.public["S2"]
    assert model.inbox[("S1", "R0004")] == ["m2"]
    assert model.inbox[("S1", "R0006")] == ["m3"]
    for actor in actors - {"R0002", "R0004", "R0006"}:
        assert not model.inbox[("S1", actor)]

    before = (len(model.messages), sum(map(len, model.inbox.values())))
    model.publish(Message("S1", "m1", "R0001", "dm", frozenset({"R0002"})))
    assert before == (len(model.messages), sum(map(len, model.inbox.values())))
    invalid = [
        Message("S1", "m1", "R0001", "dm", frozenset({"R0002"}), text="changed"),
        Message("S1", "bad1", "R0001", "dm", frozenset({"R9999"})),
        Message("S1", "bad2", "R0001", "dm", frozenset({"R0001"})),
        Message("S1", "bad3", "R0001", "dm", frozenset({"R0002", "R0003"})),
        Message("S1", "bad4", "R0001", "dm", frozenset({"R0002"}), frozenset({"R0003"})),
        Message("S1", "bad5", "R0001", "public", frozenset({"R0002"})),
        Message("missing-save", "bad6", "R0001", "public"),
        Message("S1", "bad7", "R0001", "room"),
        Message("S1", "bad8", "R0001", "unknown"),
    ]
    for message in invalid:
        try:
            model.publish(message)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid request accepted")
        assert before == (len(model.messages), sum(map(len, model.inbox.values())))

    model.active.add("R0001")
    model.publish(Message("S1", "m5", "R0001", "dm", frozenset({"R0500"})))
    assert "R0500" not in model.active
    assert model.inbox[("S1", "R0500")] == ["m5"]
    model.read[("S1", "R0500")].add("m5")
    assert "m5" not in model.adopted[("S1", "R0500")]

    repo = Path(__file__).resolve().parents[3]
    common = Path(subprocess.check_output(
        ["git", "rev-parse", "--git-common-dir"], cwd=repo, text=True).strip())
    fixture_root = (repo / common).resolve()
    with tempfile.TemporaryDirectory(prefix="collaboration-model-", dir=fixture_root) as tmp:
        base = Path(tmp)
        for actor in sorted(actors):
            desk = base / "S1" / "workers" / actor
            desk.mkdir(parents=True)
            (desk / "README.md").write_text(f"# {actor} 已发布研究桌面\n", encoding="utf-8")
        assert len(list((base / "S1/workers").iterdir())) == len(actors)
        assert (base / "S1/workers/R0500/README.md").read_text().startswith("# R0500")

    workload = []
    for interval in (1, 5, 10, 60):
        pushes = Fraction(len(actors), interval)
        hourly = pushes * 60
        assert hourly * interval / 60 == len(actors)
        workload.append({"one_message_every_minutes": interval,
                         "pushes_per_minute_if_one_message_per_push": str(pushes),
                         "writes_per_hour_if_one_message_per_request": str(hourly)})
    polls = len(actors) * 60
    assert polls // 60 == len(actors)
    contention = []
    for writers in (1, 10, 100, 500):
        # Adversarial, synchronized rounds; all survivors always retry the same head.
        attempts = sum(range(1, writers + 1))
        assert attempts == writers * (writers + 1) // 2
        contention.append({"writers": writers, "attempts_in_this_adversarial_model": attempts,
                           "rejected_attempts": attempts - writers})
    return {"schema_version": 1, "python_version": platform.python_version(),
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "replay_command": "python tests/audits/collaboration/message_routing_model.py",
            "logical_workers": len(actors), "directed_pairs_checked": directed_pairs,
            "routing_and_boundary_checks": "passed", "workload_assumptions": workload,
            "requests_hour_if_each_worker_makes_one_REST_poll_per_minute": polls,
            "synchronized_contention_model": contention,
            "limitations": ["Finite local specification model, not a production message server.",
                            "No remote GitHub or real Work concurrent load test.",
                            "Routing visibility is not an access-control guarantee.",
                            "Contention figures are conditional model outputs, not throughput predictions."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = json.dumps(audit(), ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as stream:
            stream.write(report)
    else:
        print(report, end="")


if __name__ == "__main__":
    main()
