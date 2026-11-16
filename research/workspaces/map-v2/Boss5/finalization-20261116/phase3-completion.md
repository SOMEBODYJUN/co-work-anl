# 第三阶段数学超边：完成记录

Boss5 · 2026-11-16。第三阶段当前已知构图任务均已处置，最后两批正式交付已纳入统一图。原题和候选的开放数学义务按其精确量词保留；任务完成不表示所有原题已证明。

## 最终状态

| 项目 | 数量或状态 |
| --- | --- |
| 已登记数学对象 | 3,821 |
| 当前登记关系记录 | 2,673 |
| accepted 关系 | 2,667：其中逻辑关系 2,208，语境/计算/来源等关系 459 |
| proposed / rejected | 5 / 1，均保原实际范围和理由 |
| 核心 coverage | 2,656 linked；1,165 isolated-after-review |
| 未登记 / 待处理材料 | 0 / 0 |
| 任务历史记录 | 1,050：935 done，115 withdrawn |
| 有效交付及已整合交付 | 680 / 680 |
| 当前未完成任务、待整合批、未处置整合标记 | 全部为 0 |
| 最终投影 | 21：全仓 1，存档/子档 20 |
| 最终门禁 | research check --final、research build --final 均通过 |

935 是历史 done 记录数；680 是按当前替代关系计算的有效交付数，二者不应重复相加。withdrawn 记录保留队列历史。coverage 中的孤立对象已经实读比较，收据说明未建边的数学原因；不是遗漏。

工具原始回执为 [check-final.json](check-final.json) 和 [build-final.json](build-final.json)。它们明确将结构验收与数学判定区分；build 的 local-not-pushed 是生成时的原始回执。最终文件随本轮 checkpoint 发布到 rebuild/research-v2，任务及发布状态同步 wcg/board-map-v2。精确文件 SHA 和数量见 [final-manifest.json](final-manifest.json)。

## 两条最后接入的数学关系

### 1. 原正编译族每份完整 SPE 的共同预算

[all-spe-summin-budget.json](../../../../../map/edges/boss5-summin-all-spe-3b-7383c8bf44f753cc/all-spe-summin-budget.json) 是一条 accepted、unconditional 的 ALL **contribution**。两个共同前提是 CA-AGGREGATE-LAST-FLOOR-NO 与 CA-MOBIUS-FULL-HISTORY-EMBED；终点仍是开放的一般 SUMmin-full。

对每个 n≥3，固定原两组势、原整数反演及 K=6M+4 输入。M2 的严格比较余量 K/2−2M=M+2>0 付清较大 K 的参数桥，并覆盖全部有序历史、重复离轨历史及每份完整原纯 SPE。任意 actual n 标签因而互异。令 C=2^(2n)−2^n、β_n=(2^(2n)−2^(n−1))/(n+1)，则任意 actual 集合 Z 都满足

$$
W\ge KC+n-1,\qquad
\max_a Q_a(z)=K\beta_n-F(Z),\qquad F(Z)\in\{0,1\}.
$$

每行先固定 actual 动作，沿同一 σ 重现 z；对同一个任意合法查询分布 p，

$$
\sum_iR_i(p)\le n\mathbb E_pQ_T(z)
\le n[K\beta_n-F(Z)]\le nK\beta_n<W.
$$

统一余量至少 K(C−nβ_n)+n−1>0。未用查询使用 Boolean 势差，已用查询保留重复计数并用 signed 误差界；不能把展示路径的福利等式套给任意 σ。两份独立证明与主笔比较报告都随边绑定。旧 Boss3 指定策略贡献、36 客户贡献及其资产保持原样。

这支付的是**同一明确输入族的全部策略量词**。一般输入、其它 F/K、36 客户任意其它 SPE、一般 SUMmin 与无条件六人 half 都没有由此获得证明。

### 2. 均匀时间预算与 SUMmin 的完整候选等价

[uniform-summin-equivalence.json](../../../../../map/edges/boss3-uniform-summin-identity-3b-3313f41b4a46c9dc/uniform-summin-equivalence.json) 为 accepted、conditional 的 **whole equivalent_to**。固定同一原输入、完整 σ、actual 前缀、真实完整 m 槽和同一合法 p，对每个先固定的 A 交换有限和，再在同一标签目录取 min，得到 R_i(p)=ψ_i(p)。双向保持全部 m≥1、原目录、重复动作、零客户、同覆盖异标签及全部有序历史量词。

两候选的完整全称预算因此相同，两个端点均继续 open。它们重名的 L 不同：旧槽到完整槽折扣含查询边际 q，同菜单重选收益是另一量，协方差自税不含该 q。准确桥是 κ+删槽折扣=Cov+自税。

既有末两位贡献保留为局部步骤。用 G_i 表示重选收益、H_i=C_i^full−u_i，六人尚须在全部原实例/完整 σ/同一 p 上证明

$$
H_1+H_2+H_3+H_4
\le e_5+L_{BR}+V+Q+e_6+V_6+\sum_{i=1}^6G_i.
$$

末行 actual 折扣与平均列储备只能按对应最大值或完整菜单的更好选择使用，不能相加重复支付。PF 的全行 Jensen 余量也不能直接替代 ΣG_i。

## 本轮复核和入口修订

- **θ 的背景槽数：** 已反驳的是 m−1 背景槽的 W≥mθ_m。现役 M-8f66f1abb0374762883f01d13235901c 是 m 背景槽的 W≥mθ_(m+1)，仍 open。原定义、609ace 收据和边一致；这里只把 integration 的缩写补精确。36 客户例的两者分别为 θ_3=12、θ_4=15/2，不能混读。对原 K=6M+4 正编译族，已付的同一 actual 列还直接给 θ_(n+1)≤Kβ_n−F(Z)≤Kβ_n<W/n；这说明该族不反驳完整额外槽候选，没有支付一般输入的动态命题。
- **Cartesian 与正规形：** 保留任意 full-vector 选态、全部原 jobs 和 V=1−2^(−t)、OPT=1+2^(−t)。源值与正规形共同使用时只支付目标审查的明确部分。free+quota 的 ALL whole 已否定同菜单统一正常数保值的逐坐标修复，已补入 UM 入口。
- **NSW 到 UM：** 已付域是显式非负二进制有理、无权 XOS；同一输出对全部正分数 benchmark 的保证已付。原 norm1 且正 support unit-FSLP 可行时，准确 REPAIR 合同和全部原 jobs 的 makespan≤2 已付。一般 UM 的全机统一 2−ε 改善及更广输入接口仍待证。
- **补集迁移：** bridge 给成本/收益和势差对应；Shapley 同色定理与 bridge 的两源 ALL 完整推出目标同动作静态 PNE 的全局势最小性。十三客户例精确否定同一完整序贯 SPE 的直接保持；窄静态路线已闭合。
- **版本与收据：** 01720 以正式后继修正 b77 的冗余旧 pin，保留五项原 SHA 资产和数学。历史 reading SHA 按历史解释，当前登记、边及回执按现役版本使用。

本轮还继承并保留 Binary、R105、DEEP-CAP2 等已经完成的精确审读；相应一般最优元组付款、早期共同预算或全称命题仍按原对象和 integration 的 open_math 保留。

## 后续研究从哪里进入

先锁定同一个原题，再给三组分配互补责任。以下入口提供完整前提、数学方向、精确证据和真正未付步骤：

| 入口 | 适用目的 |
| --- | --- |
| [CA：原题、SUMmin 与完整历史编译](../../Boss7/final-review-20261116/ca-research-entry.md) | 原题/定义/反例独立组；SUMmin 与静态充分链成果组；完整历史编译与已付输入族成果组。 |
| [UM：两条成果线与独立障碍线](../../Boss7/final-review-20261116/um-research-entry.md) | 同一一般 UM 原题下，明确两组可复用成果与保原机器身份的障碍责任；含 Main/三 Solver 阅读表。 |
| [WC：静态补集联合迁移](../../Boss7/final-review-20261116/wc-research-entry.md) | 复用已闭合的精确迁移，辨别静态结论与完整序贯边界。 |

全仓机器入口：[graph-v2.json](../../../../../map/graph-v2.json)；[coverage.json](../../../../../map/coverage.json)；[integration.json](../../../../../map/integration.json)；[registry.json](../../../../registry.json)。每个存档/子档的局部投影路径列在 build-final.json。

## 消费语义已验证

[final-consumer-validation.json](final-consumer-validation.json) 对新关系及真实相邻路线作了定向消费检查：全 SPE 局部边只进入 research_leads，两个 ALL 前提及 remaining 同时返回；U⇔SUMmin 两个方向都保留 open unpaid_premises；六人条件链继续保留 SUMmin 开放前提。所有选定承重绑定 current，unavailable_edge_files=0。等价环不会自行生成证明，末两位局部步骤不会被升级为整个候选。

本轮完成的是研究依据与关系图交付。一般 SUMmin、无条件六人 half、一般 UM 统一改善等开放命题，继续由后续研究在其原量词下推进。
