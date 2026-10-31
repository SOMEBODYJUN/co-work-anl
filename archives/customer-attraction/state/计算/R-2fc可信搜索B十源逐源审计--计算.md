---
id: customer-attraction/r2fc-credible-search-b-ten-source-audit
kind: computation
type_tag: 计算
title: R-2fc credible_search B 十源逐源审计与有限证书分层
status: ten-source-read; exact-finite-certificates; timeout-separated
truth_status: fixed-strategy-full-history-certificates-only; no-universal-half-result
summary: 十个冻结 JSON 全文读取并逐项复核。十条候选均有完整有序历史 Fraction 证书，三条 MIP 报 optimal、七条 timeout/incumbent；所有点满足 2W-OPT>0，不能升级为普遍 half 定理或反例。
source_refs:
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/credible_search/m3p5_mid_J034.json
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/credible_search/m3p5_mid_J234.json
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/credible_search/m3p6_111000_a0_mixed.json
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/credible_search/m3p6_111000_a0_out.json
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/credible_search/m3p6_210000_a1_out.json
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/credible_search/m3p6_mid_J034.json
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/credible_search/m3p6_mid_J345.json
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/credible_search/m4p5_11110_a0.json
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/credible_search/m4p5_21100_a1.json
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/credible_search/m5p5_31100_a1.json
evidence_packet: ../../tools/evidence/R-2fc-credible-search-b-20261031/
related_objects:
- ../候选/R-2fc循环DAG有限完整证书--候选.md
- ../计算/R-2fc可信搜索DAG与循环候选审计--计算.md
- ../资源/可信全历史搜索与双支持校正的原稿证据--资源.md
---

# 读取方法与证据边界

十个源均先执行只读 `python3 work.py clean show <id>`。partial clone 的 promisor remote 无法连接 `browser-proxy:8889`，所以十次调用都以退出码 1 结束；每次 stdout/stderr 原样保存在证据包的 `clean-show/`。随后在冻结提交 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 的 GitHub blob 页面逐源读取完整只读文本区；页面文本长度与 inventory 相差一字节（末尾换行），原始 inventory size/blob/SHA-256 未改写，具体 URL、冻结提交、字节数和状态见 `source-manifest.json`，字段全量读数见 `browser-read/summaries.json`。

`run/independent_summary_validator.py` 是独立标准库 Fraction 校验器，不导入客户吸引实现、LP 或 MILP。对每条 JSON，它重算
\[
N_{m,p}=\sum_{d=0}^{m-1}p^d,\qquad C_{m,p}=N_{m,p}(p-1),
\]
并检查 `nodes=N`、`deviation_checks=C`、`OPT/u_target`、`2W-OPT` 与 `(2m-1)u_target-OPT`。十条均通过，结果保存在 `run/independent_summary_validator.json`。这只是对已给客户整数重数和已给完整策略的定义级核验。

# 十源逐项读数

| 源（m,p；root；target/portfolio） | MIP 状态与运行 | 完整历史 / 比较 | exact 候选（W, OPT, u） | 比值与处置 |
|---|---|---:|---|---|
| `m3p5_mid_J034`（3,5；111000；a=1，J=034） | optimal；5.473 s | 31 / 124 | (4, 5, 1) | OPT/u=5；完整有限证书；固定 DAG optimal 不作全类证明 |
| `m3p5_mid_J234`（3,5；111000；a=1，J=234） | optimal；7.903 s | 31 / 124 | (4, 5, 1) | OPT/u=5；完整有限证书；固定 DAG optimal 不作全类证明 |
| `m3p6_111000_a0_mixed`（3,6；111000；a=0，J=034） | timeout/incumbent；20.042 s | 43 / 215 | (4, 5, 1) | OPT/u=5；候选已完整核验，timeout 不是无解/最优性 |
| `m3p6_111000_a0_out`（3,6；111000；a=0，J=345） | timeout/incumbent；20.032 s | 43 / 215 | (3, 5, 1) | OPT/u=5；候选已完整核验，timeout 不是无解/最优性 |
| `m3p6_210000_a1_out`（3,6；210000；a=1，J=345） | timeout/incumbent；20.031 s | 43 / 215 | (3, 5, 1) | OPT/u=5；候选已完整核验，timeout 不是无解/最优性 |
| `m3p6_mid_J034`（3,6；111000；a=1，J=034） | timeout/incumbent；20.031 s | 43 / 215 | (3, 5, 1) | OPT/u=5；候选已完整核验，timeout 不是无解/最优性 |
| `m3p6_mid_J345`（3,6；111000；a=1，J=345） | optimal；12.988 s | 43 / 215 | (3, 5, 1) | OPT/u=5；完整有限证书；固定 DAG optimal 不作全类证明 |
| `m4p5_11110_a0`（4,5；11110；a=0，J=1234） | timeout/incumbent；12.030 s | 156 / 624 | (19, 19, 4) | OPT/u=19/4<7；完整有限证书 |
| `m4p5_21100_a1`（4,5；21100；a=1，J=1234） | timeout/incumbent；12.032 s | 156 / 624 | (5, 6, 1) | OPT/u=6<7；完整有限证书 |
| `m5p5_31100_a1`（5,5；31100；a=1，J=01234） | timeout/incumbent；12.096 s | 781 / 3124 | (1, 1, 1/5) | OPT/u=5<9；完整有限证书 |

对 m=3,p=5 的两条，`2W-OPT=3`；m=3,p=6 的四条分别为 3、1、1、1；m=3,p=6 `mid_J345` 为 1；m=4 两条为 19、4；m=5 一条为 1。故十条均没有 `OPT>2W`，不能形成 half 反例。弱逐人余量依次为 0、0、0、0、0、0、0、9、1、4/5；命中余量 0 只表示固定点达到弱桥门槛。

# 同模型交叉核对

全仓同模型对象按用途分开核对：`../候选/R-2fc循环DAG有限完整证书--候选.md` 汇总既有 12 个有限 Fraction 点；`../计算/R-2fc可信搜索DAG与循环候选审计--计算.md` 解释 DAG individual、循环根扩张和旧 963-incumbent 的量词边界；`../计算/R-2fc紧Markov与受限half尾段复核--计算.md` 记录 W=1 紧化、受限 half timeout 与 count-Markov 子类限制；`../审查/最大incumbent候选的根激励遗漏与错误认证--审查.md` 保留旧生成器跳过空根历史造成的五个根盈利偏离；`../资源/可信全历史搜索与双支持校正的原稿证据--资源.md` 载明同目录 README、末位支持、循环扩张和背景校正的条件。上述对象没有把本十源的 timeout 或固定锥证书提升为普遍结论。

# 语义分层

* **完整有限证明**：每条 `exact_candidate.certified=true`，策略键覆盖全部有序历史，Fraction 逐节点检查所有非自身动作；这认证给定客户目录与给定纯策略是 full-history SPE 候选，并给出该点的 W/OPT 与比值。
* **有限候选**：MIP `status=0` 只说明固定 DAG 的浮点搜索结束；`status=1` 只说明在时间预算内有 incumbent。两者都不优化所有纯策略或所有客户目录。
* **障碍**：本十源未产生新普遍障碍。timeout 的 `floating_bound_not_a_certificate=true` 明确阻止将浮点 bound 当成定理；固定根、target、portfolio、path 也不能扩张量词。
* **结论缺口**：没有一条源证明任意人数的 half 上界、六人完整纯 SPE 上界，或 `OPT>2W` 的反例。后续必须沿现有全历史定义和真实可实现策略继续推进，不能把 3/4/5 人有限点拼接成一般结论。
