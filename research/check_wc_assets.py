#!/usr/bin/env python3
"""Validate and render the branch-to-canonical-file WC inventory."""
import argparse
import hashlib
import json
from pathlib import Path
from build_catalog import load_data, validate, render_topic

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
def render(data):
    catalog = load_data()
    validate(catalog)
    lines = ["# 加权拥塞资产链：按数学成果包读取", "",
             "先读[当前数学地图](../current/weighted_congestion/README.md)，再选择下方成果包。每包依次连接数学正文、问题或方法边界、实际审查、核验代码与冻结证据；名称和用途来自[人工命名登记](../catalog.json)，不再从 basename 自动猜测。",
             "文件角色不代替审查等级。精确命题查 [CLAIMS](CLAIMS.md)，证明、重构、内审、外审与实现查[五轴账本](../review_status.json)。原稿中的 pending 等标签保留其历史时点含义，不能覆盖现行逐命题状态。",
             "原分支、commit、原文件 SHA-256、当前去处与退役原因在 [INTEGRATION](INTEGRATION.json)。全仓其他研究线见[中文资产总目录](../CATALOG.md)。",
             "核验通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择，再将代码路径传入同一程序。旧相对布局只在临时目录重建，原冻结证据不覆盖；浮点筛选、有限精确检查和一般证明按各自用途区分。", "",
             render_topic(catalog, "weighted_congestion", SCOPE),
             "## 来源缺口", "",
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
