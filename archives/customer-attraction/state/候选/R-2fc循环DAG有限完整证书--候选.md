---
id: customer-attraction/r2fc-cyclic-dag-finite-certificate-pool
kind: candidate
type_tag: 候选
title: R-2fc 循环与 DAG 的有限完整证书池
status: exact-finite-points-retained; no-half-counterexample
truth_status: twelve-fixed-input-complete-pure-SPE-certificates; no-universal-bound
summary: 三组独立 Fraction 审计 JSON 共给出 12 个固定客户目录/完整有序策略证书；所有点有正 half 余量，且 individual probe 点低于其弱桥阈值。
source_refs:
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/credible_search/individual_candidate_audit.json
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/credible_search/extra_candidate_audit.json
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/credible_search/cyclic_candidate_audit.json
evidence_packet: ../../tools/evidence/R-2fc-credible-search-a-20261031/
related_objects:
- ../计算/R-2fc可信搜索DAG与循环候选审计--计算.md
- ../引理/循环对称目录的任意后缀均衡根扩张--引理.md
- ../审查/最大incumbent候选的根激励遗漏与错误认证--审查.md
---

# 证书池的语义

这里的“完整”只表示：对一份已经给出的客户整数重数和一份已经给出的纯策略，动作域是所有有序历史，且每个历史的所有非自身动作都被用精确分数重算。它不表示在所有客户目录、所有策略或所有人数上优化，也不把生成器的 MILP status 当作证明。

| 审计输出 | 固定点数 | 规模 | 实际路径/收益 | W, OPT | `2W-OPT` | individual 余量 |
|---|---:|---|---|---:|---:|---:|
| `individual_candidate_audit.json` | 3 | m4,p5: 19 客户；m4,p5: 6 客户；m5,p5: 1 客户 | (1,0,2,3): (16/3,4,16/3,13/3); (2,1,0,0): (4/3,1,4/3,4/3); (1,0,0,2,0): 五人各1/5 | (19,19); (5,6); (1,1) | 19; 4; 1 | 9; 1; 4/5 |
| `extra_candidate_audit.json` | 7 | m3,p6 三点；m3,p5 两点；m3,p6 mid 两点，均5单位客户 | 路径分别 (0,2,1)、(1,0,0)、(0,2,1)、(0,1,2)、(0,1,2)、(0,1,2)、(0,1,2) | (3,5); (3,5); (4,5); (4,5); (4,5); (3,5); (3,5) | 1; 1; 3; 3; 3; 1; 1 | 全部 0 |
| `cyclic_candidate_audit.json` | 2 | m3,p7: 14 客户；m5,p7: 7 客户 | (0,5,2): (3,4,4); (0,4,1,3,6): 五人各7/5 | (11,13); (7,7) | 9; 7 | 2; 28/5 |

三份 JSON 的源 SHA、完整历史数和非自身比较数保存在证据包。独立 `Fraction` 重核 12 条记录：历史数分别按 `Σp^d` 为 31/43/57/156/781/2801，比较数为历史数乘 `p−1`；所有记录 `violations=[]`、最小 slack 为 0。

# 为什么它们仍是候选/有限证书

循环 m=3 点给出 `OPT/u_0=13/3<5=2m−1`；m=5 循环点给出 `OPT/W=1`。DAG individual 三点的 exact ratios 为 19/4、6、5，对应阈值 7、7、9。额外七点的最小实际收益足以使 `(2m−1)min_i u_i−OPT=0`，但没有超过阈值；其福利分别 3 或 4、OPT=5。所有点都保留为可复核固定实例，不能拼接不同 m 或不同客户目录来形成六人结论。

`cyclic_construct.py` 只搜索 p=7 循环轨道中的 19 个有限种子，`dag_individual_probe.py` 只在给定 q、a、J 的 outcome-witness DAG 中找候选；二者的 search scope 与后续 exact audit 是不同量词。`dag_restricted_half.py` 还额外限制每个客户的未使用根主题支持数，不能用其 timeout 解释一般域无解。

本候选池没有 `OPT>2W` 的条目，因而没有 half 反例；也没有任何条目提供“每份六人完整纯 SPE”的上界。后续若复用，必须保留完整动作表、客户类型重数、静态 OPT 和所有离轨历史比较，不得把 ratio、浮点 bound 或有限未发现升级成普遍命题。
