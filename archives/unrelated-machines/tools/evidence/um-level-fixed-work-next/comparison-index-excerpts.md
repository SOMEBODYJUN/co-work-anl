## source:68fad804ec5946cb296f77dc5b336308a66abf12:research/unrelated_machines/FAILED_ROUTES.md lines 90–95

## 固定阈值中任务配置与固定势均不能替代共同动作

新失败边界 `UM-MEDIUM-CONFIG-TINY-BARRIER-v1`：对任意固定有理 \(0<\alpha<1/5\)，经典两树族的 \(k=4,T=5/4\) 已使全部有限边 \(1/4>\alpha T\)，配置 LP 在 \(T\) 可行而 \(\operatorname{OPT}/T=7/5>1+\alpha\)。因此“配置 LP 加一次独立 tiny-ST 收费 \(\alpha T\)”在此阈值下完全退化为配置间隙；列数可枚举不等于 LP 到共同整数选择已有积分提升。它不排更强跨机器约束、改变分类或直接联合舍入。

`UM-FIXED-WORK-CONVEX-POTENTIAL-BARRIER-v1` 进一步给出固定松弛的参数化边界：\(h\) 个核心、每核心 \(q\) 个 home/tiny 私有叶、一个全核心时间1的大任务，\(t=(h-1)/(hq)\)，OPT=1。最小总工作量支撑及其标准槽匹配值为 \(2-1/h\)；取 \(q=h^2\) 时任何固定 \(W\le\rho h\) 仍有 \(C_{\max}\ge2-1/h-(\rho-1)ht/(1-t)\)。对固定有限非减凸 \(f\)，若 \(q>(1-1/h)(f(3)-f(2))/(f(1)-f(0))\)，\(\sum_i f(L_i)\) 的每个全局最小解也保留近二坏态。失败只针对固定正支撑/工作量/分离势；重开昂贵叶边、自适应 hinge、机器加权、非可加势与临时增载仍可重试。完整定义和 Fraction 小参数核验见[问题正文](../questions/unrelated_machines/fixed_work_and_medium_config_barriers.md)。


## source:68fad804ec5946cb296f77dc5b336308a66abf12:research/unrelated_machines/CLAIMS.md lines 1717–1740

## UM-MEDIUM-CONFIG-TINY-BARRIER-v1：固定阈值中任务配置分解的近二边界

- Exact Statement / Quantifiers：对每个固定有理 (0<\alpha<1/5)，存在合法 (P,T) 使全部有限 (p_{ij}>\alpha T)、配置 LP 在 (T) 可行而 (\operatorname{OPT}/T=7/5>1+\alpha)。因此“仅凭配置 LP(T)可行性，再把 (p\le\alpha T) 的 tiny 末步独立支付 (\alpha T)”的合同在该范围不可能给统一小于2。
- Objects / Domain / Definitions：取经典两树族 (k=4)，(T=5/4)，有限时间仅 (1/4,1)，整数最优值 (7/4)。
- Assumptions / Scope：只否定固定阈值、配置 LP 与独立 tiny-ST 加性收费的接口；不排跨机器强化、直接联合舍入、改变阈值或 (\alpha\ge1/5)。
- Conclusion / Mechanism：tiny 集合为空，接口退化为配置间隙；配置列在固定 (alpha) 下可枚举不改变 LP 到共同整数选择的积分缺口。
- Dependencies：UM-CONF-GAP-v1 与 `model_and_classical_barriers.md` 的 (k=4) 证书；本页 Fraction 反算 (1/4>\alpha(5/4))、(7/5>1+\alpha)。
- Evidence：参数化直接证明；独立 Python Fraction 计算覆盖 (alpha=1/6,1/10,1/100) 的严格不等式。有限算术核对不替代配置族证明。
- Counterevidence / Objections：若外层能识别更强的共同容量状态或允许重开配置边，该反例不适用；(\alpha=1/5) 时严格 tiny 排除条件失效。
- Status：failed-route boundary; not a hardness result; external review and novelty unverified。
- Related Files：`research/questions/unrelated_machines/fixed_work_and_medium_config_barriers.md`；`research/current/unrelated_machines/model_and_classical_barriers.md`；`research/unrelated_machines/FAILED_ROUTES.md`。

## UM-FIXED-WORK-CONVEX-POTENTIAL-BARRIER-v1：固定工作量与分离凸势锁定近二

- Exact Statement / Quantifiers：对任意整数 (h\ge2,q\ge1)，令 (t=(h-1)/(hq))，用 (h) 个核心、(hq) 个私有叶、一个核心全可用的大任务 (B) 与每个 tiny 的 home/私有叶两条边 (t,1) 构造实例。则 OPT=1；给定 (T=1) 的最小总工作量分数支撑的任一 ST 槽匹配值为 (2-1/h)。对任意有限、非减、凸 (f:[0,3]\to\mathbb R)，若 (Delta=f(1)-f(0)>0)、(D=f(3)-f(2)) 且 (q>(1-1/h)D/\Delta)，则每个 (\sum_i f(L_i)) 全局最小调度仍有值至少 (2-1/h)。取 (q=h^2) 时任意固定相对工作量预算 (W\le\rho h) 的调度满足 (C_{\max}\ge2-1/h-(\rho-1)ht/(1-t))（\(\rho\ge1\)）。
- Objects / Domain / Definitions：(P_{C_i,B}=1)、(P_{C_i,S_{i,r}}=t)、(P_{L_{i,r},S_{i,r}}=1)，其余边不可用；(m=h(1+q))、(n=1+hq)。
- Assumptions / Scope：只排固定正支撑、固定总工作量放松和固定非减凸分离势；不排输入自适应 hinge/机器权重/非可加势/允许暂时增载的批量迁移。(f) 仅需在 ([0,3]) 有限。
- Conclusion / Mechanism：最小工作量支撑把 tiny 叶边质量置零；迁出 (B)-核心 tiny 的叶增量 (f(1)-f(0)) 大于核心节省，故任一固定势全局最小解保留近二坏态；真正 OPT 通过重开边并非不可达。
- Dependencies：本页 `fixed_work_and_medium_config_barriers.md` 的参数化证明；UM-OPTIMAL-CONVEX-ST-SLOT-GAP-v1 只作相邻背景，不替代本族证明。
- Evidence：独立 Fraction 全枚举 ((h,q)=(2,1),(2,2),(3,1),(3,2)) 核验 OPT、(W_{\min}) 与槽值；((2,4), f(L)=L^2) 全状态枚举的最小势值为 (3/2)。
- Counterevidence / Objections：昂贵叶边本身可被配置方法识别；hinge/自适应势可逐件迁移，因此不能升级为一般困难性或主目标反证。
- Status：failed-route boundary; not a hardness result; external review and novelty unverified。
- Related Files：`research/questions/unrelated_machines/fixed_work_and_medium_config_barriers.md`；`research/unrelated_machines/FAILED_ROUTES.md`；`research/current/unrelated_machines/optimal_convex_fixed_slot_gap.md`。


## source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/README.md lines 72–75

下一义务已被半单位扩展修正：固定δ<1/2的(Aδ)承诺搜索在P≠NP下均不可能；应转向实际槽损失或可分离/可舍入的条件块强化，仍无统一新算法。文件入口完整路径为research/current/unrelated_machines/joint_matching_completion_and_block_cuts.md、research/reviews/unrelated_machines/joint_matching_completion_review.md、tests/audits/unrelated_machines/{joint_matching_completion,unique_small_matching_audit,joint_matching_completion_independent}.py及evidence/runs/unrelated_machines/joint_matching_completion_audit.json；新候选必须同时攻击共享z、长链与一般多小端输入。

新增失败路线见[固定工作量与中任务配置分解边界](../../questions/unrelated_machines/fixed_work_and_medium_config_barriers.md)：固定阈值的“配置 LP 加 tiny 槽损失”在 α<1/5 时退化为经典配置间隙；固定总工作量和固定非减凸分离势也会被私有昂贵叶族锁在近二。该页只排除所列合同，重开边与自适应共同势仍是开放方向。


## source:68fad804ec5946cb296f77dc5b336308a66abf12:research/CATALOG.md lines 625–625

| [固定工作量与中任务配置分解的统一近二边界](<questions/unrelated_machines/fixed_work_and_medium_config_barriers.md>) | `research/questions/unrelated_machines/fixed_work_and_medium_config_barriers.md` | 记录固定阈值配置加 tiny 槽损失、固定工作量和固定分离凸势的精确失败范围，避免把这些局部合同误当一般共同容量算法；重开边与自适应势的后续义务从此页进入。 | 方法障碍；否定范围以正文为准；精确范围见本页正文 |

## source:68fad804ec5946cb296f77dc5b336308a66abf12:research/CATALOG.md lines 635–638

| [固定层共同容量不能修复parity资源束乘积的候选](<questions/unrelated_machines/bounded_level_tensor_capacity_escape.md>) | `research/questions/unrelated_machines/bounded_level_tensor_capacity_escape.md` | 固定L共同容量下整数源逃逸，数学独立重构/全文攻击；仍无actual UM转移或通用poly构造。；配套 [强化资源束乘积的16边真实整数核验](<../tests/audits/unrelated_machines/bounded_level_tensor_escape.py>)；配套 [二层共同上容量的冻结整数候选证书](<../evidence/runs/unrelated_machines/bounded_level_tensor_escape_candidate.json>)；配套 [需求树私有组合的无放大恒等式与共享复制的保真断点](<current/unrelated_machines/private_graft_and_resource_repetition.md>)；配套 [固定层共同容量候选的先陈述重构与冻结全文攻击](<reviews/unrelated_machines/bounded_level_tensor_capacity_candidate_review.md>) | 候选或未闭合义务；保存不升级状态；关联 `UM-RESOURCE-REPETITION-SOUNDNESS-NO-v1`，[命题合同](assets.json) |
| [强化资源束乘积的16边真实整数核验](<../tests/audits/unrelated_machines/bounded_level_tensor_escape.py>) | `tests/audits/unrelated_machines/bounded_level_tensor_escape.py` | 核同一L2,t4匹配的322类joint guards和912个不重复资源clones，不求LP/OPT。；配套 [固定层共同容量不能修复parity资源束乘积的候选](<questions/unrelated_machines/bounded_level_tensor_capacity_escape.md>) | 有限计算核验；不代替一般证明 |
| [二层共同上容量的冻结整数候选证书](<../evidence/runs/unrelated_machines/bounded_level_tensor_escape_candidate.json>) | `evidence/runs/unrelated_machines/bounded_level_tensor_escape_candidate.json` | 只审一个显式B/16条真实匹配边；不以有限证据证明一般L，不含调度实现。；配套 [固定层共同容量不能修复parity资源束乘积的候选](<questions/unrelated_machines/bounded_level_tensor_capacity_escape.md>) | 冻结输入、证书或结果；不原位覆盖 |
| [固定层共同容量候选的先陈述重构与冻结全文攻击](<reviews/unrelated_machines/bounded_level_tensor_capacity_candidate_review.md>) | `research/reviews/unrelated_machines/bounded_level_tensor_capacity_candidate_review.md` | 核共轭概率/坏对/任意多轴guard/明确t6L，区分有限16边核验与一般证明；非UM困难性。；配套 [固定层共同容量不能修复parity资源束乘积的候选](<questions/unrelated_machines/bounded_level_tensor_capacity_escape.md>) | 实际审查记录；只覆盖所列版本与义务 |
