---
id: "customer-attraction/direct-cover-incumbent-lipschitz-failure-v2"
kind: counterexample
type_tag: 反例
title: "直接覆盖 incumbent Lipschitz 失败的新有限证书"
status: "finite-obstruction-retained"
truth_status: "machine-readable-finite-obstruction; no-complete-SPE-certificate"
review_level: "full-2407-byte-read; related-direct-cover-comparison"
scope: "R-12bf direct_cover; five players, seven topics, one finite dynamic-iid-local record"
summary: "该 JSON 在 prefix=[0,0], T=6, A=0, r=3 记录 left=12<right=16；它是指定 incumbent proportional relay bridge 的有限障碍输入，不是完整 SPE 反例或六人半覆盖结论。"
source_refs:
  - "clean:ed65ba81661d52d8aaea:research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/direct_cover/incumbent_lipschitz_failure.json"
  - "local:archives/customer-attraction/tools/evidence/direct-cover-incumbent-lipschitz-20261031/original/incumbent_lipschitz_failure.json"
  - "local:archives/customer-attraction/state/审查/customer-attraction直接覆盖分支README、义务分层与前缀障碍路由--审查.md"
  - "local:archives/customer-attraction/state/反例/customer-attraction实际前缀Lipschitz失败证书--反例.md"
source_identity:
  inventory_blob: "f6214e5140aaca3194b0e8d17c3bb03b9da24167"
  source_sha256: "b9939dc192a3aab429ae037737e2e2364796fed29fadec41943ff53d219b7a16"
  source_size_bytes: 2407
  frozen_commits:
    - "68fad804ec5946cb296f77dc5b336308a66abf12"
    - "aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c"
evidence_paths:
  - "archives/customer-attraction/tools/evidence/direct-cover-incumbent-lipschitz-20261031/original/incumbent_lipschitz_failure.json"
  - "archives/customer-attraction/tools/evidence/direct-cover-incumbent-lipschitz-20261031/comparisons/comparison-notes.md"
related_objects:
  - "archives/customer-attraction/state/审查/customer-attraction直接覆盖分支README、义务分层与前缀障碍路由--审查.md"
  - "archives/customer-attraction/state/反例/customer-attraction实际前缀Lipschitz失败证书--反例.md"
  - "archives/customer-attraction/state/反例/实际前缀单主题比例中继的四人反例--反例.md"
---

# 直接覆盖 incumbent Lipschitz 失败的新有限证书

## 身份与处置

本源是 `R-12bf6a96d24c48eca828620d6642e203/direct_cover` 下的 machine-readable JSON。clean source ID 为 `ed65ba81661d52d8aaea`，大小 2407 字节，SHA-256 为 `b9939dc192a3aab429ae037737e2e2364796fed29fadec41943ff53d219b7a16`，inventory blob 为 `f6214e5140aaca3194b0e8d17c3bb03b9da24167`。原字节保存在 [JSON evidence](../../tools/evidence/direct-cover-incumbent-lipschitz-20261031/original/incumbent_lipschitz_failure.json)。

处置为 `integrated` 的有限障碍对象。它不是完整策略证书、不是 SPE 证明、不是随机搜索输出，也不是 Q-CAG-HALF 的一般反例。JSON 的 `source` 字段写为 `dynamic_iid_local.json`，因此要把左右值解释为某个 incumbent 函数的确切收益，还需读取 direct-cover README 和其兄弟推导/验证来源。

## JSON 逐字段内容

顶层字段记录：

- `prefix=[0,0]`：两个前缀动作均为主题索引 0；
- `T=6`：比较主题索引 6，即 `P`；
- `A=0`；
- `r=3`；
- `left="12"`、`right="16"`；
- `instance.players=5`，主题依次为 `X0,X1,X2,Y0,Y1,Y2,P`。

客户类型共有 19 个非空支持项。前三组是九个 `Xi,Yj` 二元类型，各重数 1；中间九个类型是两个 X 与两个 Y 的四元支持，各重数 3；最后是 `P` 单例，重数 24。总客户重数为 60。JSON 只保存输入和比较数值，没有列出每个历史动作、完整 SPE 续局或偏离后的全部收益表。

## 有限障碍的准确含义

结合 direct-cover README 的 incumbent bridge 语境，该记录给出指定前缀、背景和尾长下的 `left < right`，即该按人数比例传递单一 incumbent 标量的桥在这份有限输入上失败。它和已有 61 客户四人 BAAF 的 `V_1(A)=9 < (3/4)V_2(A)=39/4` 是不同记录：旧对象有完整 61 客户策略和真实路径/全部末位回应证据；本对象是五人七主题的 dynamic-iid-local JSON，参数和源身份均不同。

因此本对象只支持“该候选 bridge 需要跨主题信用或其他状态”的有限诊断。它不否定：

- 弱匹配、弱平均或旧强平均接口；
- 真正的跨主题菜单支付或 root-only slack；
- 六人/一般 Q-CAG-HALF；
- 已证明的五人半覆盖定理；
- unrelated-machines 的任何模型或结论。

不能从 `left=12,right=16` 反推全部背景、所有玩家数、所有目录或完整 SPE 都失败。若后续要把它升级为数学反例，需要补充源动态记录、完整策略/均衡证明、偏离收益定义及有理推导，并与既有 direct-cover 障碍去重。

## 接续与证据边界

该证书适合成为 direct-cover finite-obstruction 的输入或回归夹具；后续可检查 dynamic-iid-local 的真实前缀、跨主题信用和更弱 matching/average 条件。当前本批未执行 JSON 生成器或 LP 搜索，也没有把此记录迁移到 unrelated-machines。有限 machine-readable 值只作障碍证据，不承担一般 theorem、hardness 或半覆盖结论。
