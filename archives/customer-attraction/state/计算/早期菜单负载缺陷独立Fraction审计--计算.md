---
id: "customer-attraction/early-menu-load-defect-independent-fraction-audit"
kind: "computation"
type_tag: "计算"
title: "早期菜单负载缺陷独立 Fraction 审计"
status: "finite-exact-audit-passed"
truth_status: "finite-identities-and-fixed-SPE-checks; global-payment-bridge-open"
review_level: "full-12347-byte-read-and-exit0-replay"
scope: "B5-EARLY-MENU-LOAD-DEFECT-v1 scalar identities, range bounds, two fixed complete SPEs"
source_refs:
  - "clean:1e795f8ce6ca04b7be77:research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/independent/audit_early_price_review.py"
  - "clean:2cfff9951e701660a06d:research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/independent/early_price_review.md"
  - "local:archives/customer-attraction/state/审查/早期真实菜单负载缺陷引理独立审查--审查.md"
  - "local:archives/customer-attraction/state/审查/R-171接续工作区主张边界与开放义务--审查.md"
  - "local:archives/customer-attraction/state/引理/原策略菜单的固定过去负载与静态折扣分解--引理.md"
source_identity:
  inventory_blob: "90ac518202a67fdf87ae8d01b3a973ae53a7a4cc"
  source_sha256: "51773b4a0a76b4bee8fcdb5c50de06c59fd9c3ee98288c13c97105a69b3f15dc"
  source_size_bytes: 12347
evidence_paths:
  - "archives/customer-attraction/tools/evidence/early-menu-price-independent-20261031/original/audit_early_price_review.py"
  - "archives/customer-attraction/tools/evidence/early-menu-price-independent-20261031/original/early_price_review.md"
  - "archives/customer-attraction/tools/evidence/early-menu-price-independent-20261031/replay/audit_early_price_review.stdout"
  - "archives/customer-attraction/tools/evidence/early-menu-price-independent-20261031/replay/execution.json"
  - "archives/customer-attraction/tools/evidence/early-menu-price-independent-20261031/related/manifest.json"
  - "archives/customer-attraction/tools/evidence/early-menu-price-independent-20261031/comparisons/1e795f8ce6ca04b7be77.md"

# 早期菜单负载缺陷独立 Fraction 审计

## 程序身份和可复现执行

完整实读 12,347 字节 Python 源，SHA-256 为 `51773b4a0a76b4bee8fcdb5c50de06c59fd9c3ee98288c13c97105a69b3f15dc`，blob 为 `90ac518202a67fdf87ae8d01b3a973ae53a7a4cc`。程序不导入作者审计、游戏求解器或规范实现，只用 `Fraction`、笛卡尔积、JSON 和原始客户/策略 JSON。

由于源代码按旧仓库层级以 `Path(__file__).parents[5]` 定位输入，本次将程序复制到临时 synthetic source-root，并以 inventory SHA 精确复制两个例子和两个证书输入后执行。原始来源和相关输入均未修改。实际 exit 0，stdout 报告 `status=passed`，重放输出位于 evidence `replay/audit_early_price_review.stdout`，执行计数和依赖指纹位于 `replay/execution.json` 与 `related/manifest.json`。

## 检查范围和计数

程序的 `scalar_audit` 逐项重算三点混合分布、客户缺陷 `epsilon`、参考/真实份额与 `V` 差异，核对
\[
 S_0-S=-\tau E[sf_T(r)],\qquad
 (V_0-V)/\tau=\tau E[rf_T(s)]-\tau eE[f_T(s)],
\]
以及 `epsilon - defect_delta = v_real/tau^2`。它还核对 `Gamma` 包络、`q=0,1` 端点、`eta\ge0` 余项角点和 `tau<1` 的精确缩放。

实际计数如下：

| 检查 | 次数 |
|---|---:|
| scalar identities | 43,776 |
| range bounds | 14,592 |
| remainder bounds | 10,944 |
| tau scalings | 648 |
| fixed-SPE rows | 288 |
| real menus | 71 |
| real inequalities | 852 |
| relay payment bounds | 256 |
| root-envelope points | 60 |
| zero-defect menus | 3,256 |

`real_audit` 对两个固定完整 SPE 证书直接按所有有序历史重算当前行动与每个替代主题的真实终局收益；未把同计数历史合并，也未只检查实际路径。额外对 71 个真实菜单和 852 组 `eta/qmode` 参数检查余项上界、`v+sum Gamma` 价格上界和 `delta` 版本。

## 数学边界

这份程序支持审查稿中的有限实现事实：`epsilon` 的符号恒等式、`delta` 与 `V/tau^2` 的关系、`Gamma` 逐客户包络、`tau<1` 归一化、根包络点和两个固定 SPE 的 288 项真实比较。它不单独提供任意目录/任意人数的普遍证明；审查稿中的一般端点和逐点分类推导承担普遍量词。

尤其要保留以下条件：式 (6) 的 `3/8` 卸载支付只在所有中继负载确实可卸载时成立；式 (9) 需要存在非末位的全体最低收益者；式 (10) 的零缺陷条件需要逐查询的负载序关系。程序没有证明这些条件由任意完整 SPE 自动满足，也没有把 `epsilon_*` 变成可由真实中继福利支付的全局预算。

对象处置为 integrated 的有限精确计算记录。它支持早期菜单缺陷引理的独立内部检查，补强 existing R-171 route/审查页的证据链；不构成 Q-CAG-HALF、一般 SPE 付款、弱 CCE 桥或 unrelated-machines 结论。
