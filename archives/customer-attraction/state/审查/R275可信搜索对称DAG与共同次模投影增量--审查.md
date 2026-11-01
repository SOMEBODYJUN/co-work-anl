---
id: customer-attraction/r275-credible-search-symmetric-submodular-review
kind: review
category: 审查
title: R-275 可信搜索、对称 DAG 与共同次模投影增量
status: integrated-finite-witnesses-and-projections
truth_status: exact-finite-SPE-audits; necessary-projection-only; broader-class-only; no-Q-CAG-HALF-result
source_refs:
  - clean:8db1a2a5000b71f8b0d7
  - clean:cc5b25ed41995a64490b
  - clean:e3ecc10a13a38b92f417
  - clean:65fe51df1a3e78d8406d
  - clean:8d0734cffee299d6fc93
  - clean:8adfa0f761bfd561e87d
  - clean:baedd574d2f97e628a27
  - clean:c2b50b070dd097fa7a94
  - clean:633b64cbcf0233d0f667
  - clean:eb29376c023b5cd9726a
  - clean:c73e6eab5543a604ee48
  - clean:19aa5c10645c08cf8efe
  - clean:fcf5b34776da46287050
  - clean:b3f1a7f89ebcadcc70ab
  - clean:d2f2f8ffd2da9dee688d
  - clean:339d6de697e137702a2a
  - clean:57a3d41b4bdd023c48a6
  - clean:289d45c5d46219c922ff
  - clean:a4691452782e3989d996
  - clean:f292807346b79669d918
---

本批读取 R-275 credible_search 的二十个冻结源，覆盖 acyclic/certificate 回放、对称输入类的 MILP 候选、整数锥精确恢复、indexed actual-customer projection，以及共同单调次模 Shapley 扩展。材料同时包含浮点候选与 Fraction/完整历史核验；正文把它们分开，不把“必要投影可行”写成客户吸引 SPE，也不把 broader class 的结果写回当前模型。

## 1. 已有对称候选的完整历史核验

`certificate_audit.json` 与独立 `audit_stdout.txt` 都用 standard-library continuation audit，不导入 canonical solver。12 条记录全部 `valid_complete_pure_SPE=true`，每个五人七主题候选有 2801 个有序历史和 16806 个非自身偏离，最小 slack 均为 0。代表性 exact ratios 为：1 客户例 $W=OPT=1$；33 客户例 $W=20,OPT=33$、$OPT/W=33/20$；9 客户例 $W=5,OPT=9$、$9/5$；按同一 symmetric family 放大的两例为 $W=4000,OPT=7164,OPT/W=1791/1000$ 与 $W=2500,OPT=4485,OPT/W=897/500$；warm-start smoke 为 5 客户、3 主题、13 历史、26 比较、$W=3,OPT=5$。这些都是完整策略的有限证书，所有 ratio 都小于 2，不能形成 half 反例。

`acyclic_review_stdout.txt` 另外独立复核四行 witness：52 客户、4 人、6 主题、259 历史、1295 非自身偏离，实际支付均为 $47/4$，$W=47,OPT=52$，$OPT/W=52/47$，最小 slack 0，26 个平局。它确认一个 acyclic/static matching 输入上的完整 SPE 证书和四条预算行，但不是当前六人主目标的证明。

## 2. 对称 DAG 的 MILP/精确分层

`symmetric_dag.py` 将后 $p-d$ 个主题视为输入中的交换标签，但不强加纯策略的 equivariance；浮点 MILP 只负责候选生成，抽取的策略必须进入整数固定锥并做定义级核验。

五个单/最大/热启动 JSON 的 exact candidates 均 `canonical_definition_verified=true`。有些 MILP 运行 status 0/7，另一些 status 13 (`kTimeLimit`)；这只影响候选搜索是否闭合，不影响随后已写入 JSON 的 exact candidate 证书。q23/q32 的候选分别达到 $W=5,OPT=9$（$9/5$）；q221 的两个放大 exact symmetric candidates 是 $1791/1000$ 与 $897/500$；浮点 objective 1.8、1.7169 或 time-limit 结果都不能被写成 universal optimum。每个 JSON 明确 `universal_claim_proved=false`。

## 3. indexed actual-customer projection：超过二的必要点没有成为 SPE

`indexed_projection_instance.json` 记录五人、十主题、60 个具体客户类型。`indexed_projection_completion.json` 的目标列被归一为巨大的有理尺度 `target_W`，对应 comparison/OPT 为约 2.0614 倍目标列；但 `target_reachable=false`，完整 BI 只留下一个 root outcome，`minimum_SPE_W=OPT` 且 `OPT_over_minimum_SPE_W=1`。四个 `actual_order_ABCDE_obstructions` 记录具体前缀处目标支付与 credible floor 的冲突，其中前三个还没有进入选定子树。它因此是“一个显式 actual-unit-customer projection 的必要点与不可达障碍”，不是完整 SPE 的 `OPT>2W` 反例。

`indexed_projection.py` 在 materialized evidence 原路径运行时因相对依赖缺少 `customer_attraction/model.py` 首次真实失败；失败 stdout/stderr 已保存。静态 `py_compile` 通过。没有用别的模型包重写运行结果。

## 4. broader common-submodular Shapley 类只作外部压力测试

`submodular_joint_m5p7_q32.json` 与 `..._genuine.json` 明确把输入扩大为 common monotone-submodular truncated moments，而非客户类型重数；均保留 full ordered-history pure SPE witness。前者检查 1470 个 coefficient rows，exact candidate value/dual bound 为 2；后者加 root marginal floor 0.1，MILP status 13 的有限候选后仍有 exact value `88/57`，independent uniform-order audit 为 2801 histories、16806 deviations、$W=1,OPT=88/57$。两个 JSON 都写 `customer_attraction_half_status=OPEN`，故只能作为 broader-class pressure test/necessary obstruction。

`submodular_path_m5p7.json` 有 30 条 path necessary cuts，全部 `certified=true` 且 dual optimal；best path `[0,0,0,1,1]`、portfolio `[2,3,4,5,6]` 的 value 为 `17/8`。但 `best_exact_point_credible_completion` 的 root target reachable 为 false，root threshold `17/40`，三处 on-path obstructions 明确记录目标 payoff 低于 credible floor。因此 path projection 超过 2 仍不是可实现完整 SPE。

## 5. 与主线接续的明确边界

这些源的独有内容是：在 $m=5,p=7$ 对称输入上，用完整历史证书确认若干 $9/5$ 或更低的有限候选；用 indexed projection 展示 necessary point 可达性失败；用 common-submodular Shapley 扩展测试 1470 行 moment/IC 约束；用 path LP 给出 30 个 dual-optimal necessary cuts。它们不证明六人 Q-CAG-HALF，也不构成当前客户吸引模型的反例。

后续若接续，必须恢复每个 projection 的真实客户目录、全部有序离轨 continuation、均分福利和任意平局；对 broader class 还必须先证明从 Shapley moments 回到单位客户类型的保真映射。保留空主题、重复标签、零客户和离轨历史，不以对称 orbit 压缩替代完整策略树。

证据、原始 materialized source、运行失败边界、manifest 与比较记录见 [R-275 credible evidence](../../tools/evidence/R275-credible-search-20261031/README.md)。
