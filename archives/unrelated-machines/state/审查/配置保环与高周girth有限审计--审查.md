---
id: "unrelated-machines/configuration-preserving-cycle-cactus-20261030-review"
kind: "review"
type_tag: "审查"
title: "配置保环与高周 girth 有限审计"
status: "complete"
truth_status: "exact-finite-fraction-replay"
review_level: "full-json-read-no-full-schedule-enumeration-no-general-proof"
scope: "configuration-preserving single-cycle endpoints (two canonical runs) and cactus high-girth configuration gap; finite certificates only"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/configuration_preserving_single_cycle_endpoints_audit.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/configuration_preserving_single_cycle_endpoints_rational_parameter_audit.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/cactus_high_girth_configuration_gap_audit.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/configuration_preserving_single_cycle_endpoints_audit.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/configuration_preserving_single_cycle_endpoints_rational_parameter_audit.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/cactus_high_girth_configuration_gap_audit.json"
evidence_dir: "archives/unrelated-machines/tools/evidence/config-cycle-cactus-20261030"
---

# 1. 来源、对象与重读

本批完整读取三份冻结 JSON，并将原始字节与 manifest 保存到 `tools/evidence/config-cycle-cactus-20261030/`。两份 `configuration_preserving_single_cycle_endpoints` 的运行参数、脚本 SHA 和三组 (D,L) 完全相同，但 canonical SHA 不同；它们是同一有限参数族的两个冻结输出/编码版本，不能计作两份独立数学族。第三份 cactus 源是高周配置 gap 的六个有限 family。

全仓比较了现有《配置剥离与联合匹配有限审计》与其配置/标签地板段落。本批新增的是保环端点的具体 (D=3,5,7) 数据以及 cactus 的 (k=2,3,4)、girth 3/4/7、height 1/3 的精确数值；量词仍是 finite exact audits。

# 2. 配置保环 single-cycle endpoints

两个保环 JSON 都声明 `claim_id=UM-CONFIG-PRESERVING-CIRCUIT-TWO-SIGN-SUPPORT-LOSS-v1`、Fraction 算术、`all Fraction checks passed`，scope 为 `exact finite audits; no full scheduling enumeration or general proof claim`。三组运行如下：

| (D,L,N) | machines/jobs | finite edges | true optimal atoms | hard A/B counts | initial C edge | circuit support | connected degree-two graph | explicit configs | selected hard matching checks | global endpoint upper |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 3,5,15 | 60/62 | 160 | 15 | 6/6 | (2/5) | 60 | yes | 950 | 16 | (5/3) |
| 5,7,35 | 126/142 | 364 | 35 | 15/15 | (3/7) | 140 | yes | 2,100 | 64 | (9/5) |
| 7,9,63 | 216/254 | 648 | 63 | 28/28 | (4/9) | 252 | yes | 3,690 | 256 | (13/7) |

每组的 `max_box_steps` 都等于初始 C edge；config sample (	heta) 在 (-C/2,-C/4,0,C/4,C/2)（按具体分母写成源中的有理数）处逐点检查；`selected_label_all_export_subsets_enumerated=true`。前两组还报告若运行矩阵秩分别为 59（支持 60）和 139（支持 140），(D=7) 仅保留 `null`，不能用前两组模式填补。

这些字段支持的准确结论是：在给定 (D,L)、给定端点/标签导出规则和给定有限配置样本中，保环图为连通二度图，选定标签硬匹配及端点上界通过 Fraction 检查。它们没有枚举所有完整调度，`global_endpoint_upper` 不是统一近似比，也没有 general circuit theorem。两份 canonical 输出的差异只属于源版本证据，数学内容按三组参数合并记录。

# 3. 高周 cactus 配置 gap

cactus 源声明 `scope=exact finite evidence, not the all-k proof`，参数 (kin[2,256])，但实际明确列出的 family 只有六个：

| (k) | girth | height | machines/jobs | nonzero configurations | (T) | witness / claimed lower bound | exhaustive optimum | ratio to (T) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | 3 | 1 | 6/7 | 16 | (3/2) | (3/2) | (3/2) | 1 |
| 3 | 3 | 1 | 10/13 | 32 | (4/3) | (5/3) | (5/3) | (5/4) |
| 2 | 4 | 1 | 8/9 | 20 | (3/2) | (3/2) | (3/2) | 1 |
| 2 | 7 | 1 | 14/15 | 32 | (3/2) | (3/2) | (3/2) | 1 |
| 4 | 3 | 3 | 234/329 | 826 | (5/4) | (7/4) | (7/4) | (7/5) |
| 4 | 7 | 3 | 618/713 | 1,594 | (5/4) | (7/4) | (7/4) | (7/5) |

(k=3) 的 (5/4) 与 (k=4) 的 (7/5) 是相对给定 certificate threshold (T) 的有限 gap；`exhaustive_optimum` 与 witness 一致，说明这些小 family 的枚举没有只保存上界调度。另一方面，源的 `finite_formula_parameters` 只说明 (k_{min}=2,k_{max}=256) 的公式参数范围，并未为每个 (k) 提供完整配置/调度枚举。

因此可以保留“高周或 cactus 构造中，某些 (k=3,4) family 的精确配置最优值超过给定 (T)”这一条件结论；不能写成 all-(k) gap、near-two hardness 或统一近似下界。源 limitations 还明确指出：(T) 未声称为 exact configuration threshold，无 general near-two hardness/uniform approximation theorem。

# 4. 失败机制与关系

* 保环源的核心结构是 support 上的连通 degree-two circuit 与两个 hard label 计数；其端点上界来自有限配置检查。它与 cactus gap 的高 girth 约束不是同一个族：前者重点是配置保留与端点参数，后者重点是稀疏图 family 的 gap。
* 保环两份源都把 `selected_label_hard_matching_checks` 与 `selected_label_all_export_subsets_enumerated` 作为检查字段；这不等于所有 schedule 的全量枚举，也不等于存在一个 LP/配置 oracle。
* cactus (k=3) 和 (k=4) 的 witness 达到 exhaustive optimum，但只对表中六个 family 生效。height=3 的两组不能自动代表 height 或 girth 任意增长。
* 两类对象都属于 unrelated-machines，和 CAG 的共同目录、SPE、客户均分语义没有交集；不能把 endpoint upper 或 ratio 迁移到当前六人 CAG 目标。

# 5. 处置与接续

`ca97...` 与 `114...` 集成到本审查的保环有限证书段：保留同一三组 (D,L) 的两个 canonical hash，说明其互补版本而非重复数学族。`358...` 集成到 cactus 高周有限 gap 段，保留六个 family 的机器/任务规模、精确 witness、exhaustive optimum 与 ratio。

若后续要研究 general configuration-preserving theorem，应补齐 (D,L) 任意值的完整调度枚举或解析映射，并说明 endpoint upper 如何从配置到 makespan。若后续要主张 all-(k) cactus gap，需要为每个 (k) 给出可检查的配置/调度对象和阈值证明；本批没有做这些工作。正式等级是“有限 Fraction 证书与精确小 family gap”，不是一般证明、算法不可能性或 hardness 定理。
