#!/usr/bin/env python3
"""Validate and render the branch-to-canonical-file WC inventory."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
SCOPE = "research/weighted_congestion_frontier"
ROLES = {
    "audit_code": ("tests/",),
    "frozen_evidence": ("evidence/",),
    "review_record": ("research/reviews/",),
    "candidate_or_obligation": ("research/questions/",),
    "mathematical_account": ("research/current/",),
    "source_or_audit": ("history/", "tests/", "evidence/"),
}
STATES = {
    "audit_code": "可重放精确核验；有限范围，不是一般证明",
    "frozen_evidence": "原冻结证据；不原位覆盖",
    "review_record": "内部审查原记录；只覆盖明列版本和命题",
    "candidate_or_obligation": "候选或开放义务；入 main 不升级",
    "mathematical_account": "现行数学稿；逐命题审查另查五轴表",
    "source_or_audit": "原始来源或审计；按其实际合同使用",
}


def render(data):
    lines = ["# 研究资产：逐文件用途与生产状态", "",
             "沿用 GROWTH 的目录合同。文件位置不代替审查等级；精确身份见主题 CLAIMS，五轴状态见 research/review_status.json。",
             "原分支、commit、原文件 SHA-256、当前去处与退役原因见 INTEGRATION.json。原稿中的历史命令不是当前写回证据的入口。",
             "核验统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择，再将代码路径传入同一程序。", "",
             "| 完整路径 | 内容与存在理由 | 生产状态 | 何时读取 |",
             "| --- | --- | --- | --- |"]
    seen = set()
    for old, item in sorted(data["classification"].items(), key=lambda x: x[1].get("path", x[0])):
        name = item.get("path")
        if not name or name in seen:
            continue
        seen.add(name)
        text = (ROOT/name).read_text() if name.endswith(".md") else ""
        title = text.splitlines()[0].lstrip("# ") if text else Path(name).name
        state = STATES[item["role"]]
        if "quadratic_triad/proof.md" in name:
            state = "完整有限证明；所引独立 review 未保存"
        if "NONSEPARABLE_REVIEW" in name:
            state = "审查摘要；原 proof/程序缺失，不能替代证明"
        lines.append(f"| [{name}]({os.path.relpath(name,SCOPE)}) | {title[:100].replace('|','/')} | {state} | {item.get('topic','')} 接口或来源复验时 |")
    lines += ["", "## 来源缺口", "",
              "`resource_cone/review.md`、`nonseparable_frontier/proof.md` 及所引未见程序、`r2_orbit/review.md` 未在已观察分支中找到。不得补造为已审或已证明。",
              "原参数旧 family 和重复导航稿退出当前文件树；其不可变原提交保留在 main 的 Git 祖先中。", ""]
    return "\n".join(lines)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check",action="store_true")
    args=parser.parse_args()
    data=json.loads((ROOT/SCOPE/"INTEGRATION.json").read_text())
    assert set(data["source_files"]) == set(data["classification"]), "source lacks disposition"
    count=0
    for old,item in data["classification"].items():
        if "path" not in item:
            assert item["disposition"]=="git_history_only" and item["reason"]
            continue
        name=item["path"]
        assert name.startswith(ROLES[item["role"]]), (old,name,item["role"])
        content=(ROOT/name).read_bytes()
        if name.endswith((".py",".json")):
            assert hashlib.sha256(content).hexdigest() in {x["sha256"] for x in data["source_files"][old]}, ("frozen code/evidence changed",name)
        count+=1
    result=render(data)
    target=ROOT/SCOPE/"FILES.md"
    if args.check:
        assert target.read_text()==result, "run research/check_wc_assets.py"
    else:
        target.write_text(result)
    print(f"Validated {count} retained source routes and all explicit retirement decisions")


if __name__=="__main__":
    main()
