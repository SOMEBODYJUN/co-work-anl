---
id: "customer-attraction/R-171-coupling-pair-route-review"
kind: review
type_tag: 审查
title: "R-171 共同客户根路径支付与 pair 预算开放边界"
status: "integrated-route-review-with-finite-pair-audit"
truth_status: "route-and-quantifier-review; Q-CAG-HALF-remains-open"
review_level: "full-1621-byte-read-related-R-171-materials-and-replay-cross-check"
scope: "R-171 coupling README; fixed-population pair-error route, interval-rent route, omission and early-incentive boundaries"
summary: "README 将固定人数 r>s pair-circuit 误差压到 (r-s)(r-1) 倍宽二 ghost rent，并宣称对每个前缀 r+s=m-j 可接一次根路径预算；本页保留该路线的量词、有限审计和缺口：它没有给出实际全树 SPE 运输，也没有关闭 skip-premium、早期激励或共同根支付。"
source_refs:
  - "clean:af416d25b1181a69b019:research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/coupling/README.md"
  - "local:archives/customer-attraction/tools/evidence/R-171-coupling-pair-20261031/original/README.md"
  - "local:archives/customer-attraction/tools/evidence/R-171-coupling-pair-20261031/original/audit_fixed_population_pair_error.py"
  - "local:archives/customer-attraction/tools/evidence/R-171-coupling-pair-20261031/original/fixed_population_pair_error_audit.json"
  - "local:archives/customer-attraction/state/审查/R-171接续工作区主张边界与开放义务--审查.md"
  - "local:archives/customer-attraction/state/引理/R-171稀疏槽clock租金与skip-premium分解--引理.md"
  - "local:archives/customer-attraction/state/反例/R-171完整SPE稀疏槽租金障碍--反例.md"
  - "local:archives/customer-attraction/tools/evidence/R-171-coupling-pair-20261031/comparisons/comparison-notes.md"
source_identity:
  inventory_blob: "c2e3a909a6edf1d768934408f11f1cde9680f35c"
  source_sha256: "c30072054fd1b49b6030f6449953fb1e4e9dc1701a25be261bc9ad955e2674a9"
  source_size_bytes: 1621
  frozen_commits:
    - "68fad804ec5946cb296f77dc5b336308a66abf12"
    - "aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c"
evidence_paths:
  - "archives/customer-attraction/tools/evidence/R-171-coupling-pair-20261031/original/README.md"
  - "archives/customer-attraction/tools/evidence/R-171-coupling-pair-20261031/original/audit_fixed_population_pair_error.py"
  - "archives/customer-attraction/tools/evidence/R-171-coupling-pair-20261031/original/fixed_population_pair_error_audit.json"
  - "archives/customer-attraction/tools/evidence/R-171-coupling-pair-20261031/replay/audit_fixed_population_pair_error.stdout.json"
  - "archives/customer-attraction/tools/evidence/R-171-coupling-pair-20261031/comparisons/comparison-notes.md"
---

# R-171 共同客户根路径支付与 pair 预算开放边界

## 1. README 的实际范围

冻结 README 共 1,621 B，SHA-256 `c30072054fd1b49b6030f6449953fb1e4e9dc1701a25be261bc9ad955e2674a9`，稳定 ID `af416d25b1181a69b019`，blob `c2e3a909a6edf1d768934408f11f1cde9680f35c`。它明确把原目标写成：共同有限目录、任意人数、每个完整有序历史纯 SPE 的 Q-CAG-HALF（`2W\ge OPT`）仍 OPEN。README 是 coupling 子目录的导航和量词边界，不是 `fixed_population_pair_error_budget.md` 正文；该正文在清单中存在但没有随本批导出，因此本页不把导航摘要冒充完整证明。

README 指向三条相互关联的路线：

1. **连续窗口 ghost-rent。** 对任意实际路径，若每个前缀收费的未来槽位是连续窗口，可用宽二、reserve 一、前缀权 (1/j) 的槽位拥塞支付至多 (W)；不需要 SPE，但尚未把该条件运输到一棵满足所有离轨激励的全树。允许任意稀疏单槽后，`R-171完整SPE稀疏槽租金障碍` 已给出调和发散，所以“路径来自 SPE”本身不能替代连续性。
2. **固定人口 pair-circuit。** 对 (r>s\ge1) 的局部两主题电路，README 声称误差由 ((r-s)(r-1)) 倍宽二 ghost rent 逐客户支配。对每个前缀 (jle m-3) 选择 (r_j+s_j=m-j)，并以实际相邻主题 (S_{j+1},S_{j+2}) 作 (A,B)，归一化误差的总和可接到一次根路径预算。当前三源的 Fraction 审计重核了该代数接口的定义级有限域；它没有构造真实后继策略或 SPE 运输。
3. **下一步义务。** 需要真正不同的前置查询族和早期激励，或把全树误差嵌入连续窗口拥塞。旧 clique 菜单 (A_r) 的根支付仍缺；同一 (T_i) 查询族的 clique 被 README 标为冗余，不能当作新桥。

README 还列出最优遗漏独立审查及其 71 客户二人反例/ (k\ge3) 族：它们只否定“总能选一个有利最优组合并支付遗漏”的加强桥，原 half 余量仍为正。故 pair-circuit 路线与 omission 路线都不是 Q-CAG-HALF 反例。

## 2. 与已归档 R-171 对象的对照

`R-171稀疏槽clock租金与skip-premium分解--引理` 已将 reset 费用拆成可按真实 hit 时钟支付的部分和非负 skip-premium；连续窗口使 premium 为零，而两客户完整 SPE 族的发散全部来自 premium。当前 README 的 pair 预算只说明一个**局部 pair 误差可由宽二 ghost 项控制**，没有支付 skip-premium，也没有证明真实离轨路径满足窗口条件。

`R-171完整SPE稀疏槽租金障碍--反例` 的模型是两个单位客户、两个互斥单例主题、(m=2q) 的完整纯 SPE 族；其 welfare 和 OPT 都为 2，因此不反驳 half，却说明稀疏收费桥可无界。当前 pair 误差审计不改变该障碍，也没有产生新的福利反例。

`R-171接续工作区主张边界与开放义务--审查` 已把 B5-FIXED-POPULATION-PAIR-ERROR-v1 归类为局部接口：短 pair 终局的 (f_H(B)) 不是任意真实续局的激励值。当前 README 和审计输出应沿用这个边界，不能把“主要 pair 终局恰 (m) 玩家”改写成完整任意历史 SPE 结论。

## 3. 处置

本 README 作为 integrated 的路线审查页保存。其独有内容是把连续窗口、固定人口 pair、遗漏桥和早期激励义务放在同一入口，并明确它们的开放连接；有限脚本和 JSON 的精确结果在相邻计算页另行保留。任何后续引用都必须同时说明：

- pair 误差公式的全量词来自未导出的正文主张，当前本批只独立重核定义级有限域；
- ghost-rent 的根支付需要连续窗口或另一个真实运输构造；
- 完整 SPE 的离轨激励、skip-premium 和早期中继缺口仍未关闭；
- 没有新的 `2W<OPT`、一般算法、hardness 或 unrelated-machines 结论。
