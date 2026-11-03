---
id: "customer-attraction/direct-cover-verify-incumbent-obstruction"
kind: computation
type_tag: 计算
title: "直接覆盖 incumbent 障碍定义级有理复核"
status: "finite-fraction-regression-passed"
truth_status: "finite-regression-evidence; no-general-proof-by-execution"
review_level: "full-1811-byte-read; standalone-execution; direct-cover-comparison"
scope: "R-12bf direct_cover/verify_incumbent_obstruction.py; 102 positive background counts"
summary: "独立 Fraction 脚本不导入 canonical model/solver/探索 LP，对 102 个正背景计数核验硬编码三主题收益表、唯一最佳回应和比例 bridge；一次执行 exit 0，但只属有限回归证据。"
source_refs:
  - "clean:c885e1e95fad531e7e7c:research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/direct_cover/verify_incumbent_obstruction.py"
  - "local:archives/customer-attraction/tools/evidence/direct-cover-verify-incumbent-20261031/original/verify_incumbent_obstruction.py"
  - "local:archives/customer-attraction/tools/evidence/direct-cover-verify-incumbent-20261031/replay/execution.json"
  - "local:archives/customer-attraction/state/反例/实际前缀单主题比例中继的四人反例--反例.md"
  - "local:archives/customer-attraction/state/审查/customer-attraction直接覆盖分支README、义务分层与前缀障碍路由--审查.md"
source_identity:
  inventory_blob: "acff9181ae248c187315a98849a65792f164ed95"
  source_sha256: "227c15293633967e7e6508afa517828018c0c897b037f60654d1b5774cc556c3"
  source_size_bytes: 1811
  frozen_commits:
    - "68fad804ec5946cb296f77dc5b336308a66abf12"
    - "aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c"
evidence_paths:
  - "archives/customer-attraction/tools/evidence/direct-cover-verify-incumbent-20261031/original/verify_incumbent_obstruction.py"
  - "archives/customer-attraction/tools/evidence/direct-cover-verify-incumbent-20261031/comparisons/comparison-notes.md"
  - "archives/customer-attraction/tools/evidence/direct-cover-verify-incumbent-20261031/replay/execution.json"
  - "archives/customer-attraction/tools/evidence/direct-cover-verify-incumbent-20261031/replay/verify.stdout.txt"
related_objects:
  - "archives/customer-attraction/state/反例/实际前缀单主题比例中继的四人反例--反例.md"
  - "archives/customer-attraction/state/反例/customer-attraction实际前缀Lipschitz失败证书--反例.md"
  - "archives/customer-attraction/state/审查/customer-attraction直接覆盖分支README、义务分层与前缀障碍路由--审查.md"
---

# 直接覆盖 incumbent 障碍定义级有理复核

## 身份与执行记录

本源为 `R-12bf6a96d24c48eca828620d6642e203/direct_cover/verify_incumbent_obstruction.py`，clean source ID `c885e1e95fad531e7e7c`，大小 1811 字节，SHA-256 `227c15293633967e7e6508afa517828018c0c897b037f60654d1b5774cc556c3`，inventory blob `acff9181ae248c187315a98849a65792f164ed95`。原程序保存在 [script evidence](../../tools/evidence/direct-cover-verify-incumbent-20261031/original/verify_incumbent_obstruction.py)，实际运行命令、exit code、stdout hash 和 scope 保存在 [execution.json](../../tools/evidence/direct-cover-verify-incumbent-20261031/replay/execution.json)。

本批在仓库根执行一次：

```text
python3 cleanup/workspaces/Boss3/agent-gamma/verify_incumbent_obstruction.py
```

退出码 0，stderr 为空，stdout 为：

```text
PASS: all histories and payoff formulas for 102 positive background counts; ratio bridge 1 < 4/3.
```

处置为 `integrated` 的有限计算对象。执行通过确认了脚本硬编码的公式和断言在列出的 102 个背景计数上通过；它没有把 source 中的 all-k 解析说明自动变成一份新证明。

## 程序的数学内容

脚本固定三组主题：`TOPICS=({0,2},{1,2},{3,4})`。`utility` 用 `Fraction` 按固定背景计数 `b` 和最终两个动作计算客户分母；`check(k)`：

- 对每个第一位动作和末位动作检查三元 payoff tuple 与预期精确值；
- 检查末位唯一最佳回应分别为动作 1、2、1；
- 检查第一位收益表的唯一最优动作是 1；
- 检查在背景增量 `k+1` 后的最终值和最佳回应；
- 检查 `utility(2,k,(2,1,2))==1`、`utility(2,k+1,(2,1))==2` 及 `1 < 2*F(2,3)`。

主程序遍历 `k=1..100`、`1000`、`10**6`，合计 102 个正背景计数。它没有读取 JSON、canonical model、solver、探索 LP 或完整 61 客户 BAAF 策略。

## 证据边界与既有障碍的关系

运行结果是 finite Fraction regression evidence。它支持“给定硬编码三主题结构和列出的 102 个 k 值，收益表、最佳回应和比例断言没有触发断言”；它不能单独支持任意正整数 k 的一般定理、任意目录/客户宇宙的 incumbent bridge 失败、完整原模型反例或 Q-CAG-HALF 反例。

与已有 `实际前缀单主题比例中继的四人反例` 相比，该脚本是定义级局部公式核验，后者另有 61 客户完整策略、BAAF 路径和全历史真实/最小续局证据；两者不能合并成同一 source 或同一运行范围。与 `customer-attraction实际前缀Lipschitz失败证书` 旧 JSON 相比，脚本没有核验那个四人六主题 JSON，也没有导入其 `left/right`；本批三源中新的五人七主题 JSON 仍是独立有限记录。

与 `直接覆盖弱匹配LP诊断入口` 相比，本脚本不使用随机 LP、NumPy/SciPy 或 canonical solver，属于较窄的独立回归核；其通过不能证明弱匹配或平均支付桥。全部结果不迁移到 unrelated-machines。

## 接续

若要提高证据强度，需要把硬编码公式与对应动态-iid/local 或完整 direct-cover 源的量词、策略和背景定义逐项绑定，再给出有理解析证明或完整策略证书。当前保留脚本、stdout、执行 metadata 和源 comparison，不把有限通过写成一般 theorem。
