---
id: "customer-attraction/r105-research-desk-metadata-boundaries"
kind: "review"
type_tag: "审查"
title: "R105 研究桌面元资料与方法边界"
status: "source-curation-complete; earlier-claim-boundary-kept-as-history"
truth_status: "source-specific metadata and method-boundary synthesis; Q-CAG-HALF remains open"
review_level: "five frozen sources reread in full; current owner claim checked separately; mathematical scope compared with later results"
summary: "五份 R105 研究桌面元资料分别给出精确 claim 清单、失败接口、一般工作稿、恢复导航和研究状态。它们共同确认 Q-CAG-HALF 的模型与量词不变，保存 DR/ASD/VR、静态排列反例、根可达性必要条件及若干未闭合桥的边界；没有新增一般 half 证明或目标反例。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/CLAIMS.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/CLAIMS.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/FAILED_ROUTES.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/FAILED_ROUTES.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/GENERAL_WORKING.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/GENERAL_WORKING.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/README.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/README.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/RESEARCH_STATE.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/RESEARCH_STATE.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/CLAIMS.md"
legacy_ids:
  - "B16-R105-RESEARCH-DESK-METADATA-v1"
evidence_manifest: "../../tools/evidence/R105-meta-20261031/manifest.json"
---

## 读取范围与版本身份

五个文件均通过 `clean show` 导出并完整读取；legacy-cleanup 与 main 的同路径字节按一个冻结源版本计数。`CLAIMS.md` 是对象与量词账本，`FAILED_ROUTES.md` 是接口失败与可回收信息，`GENERAL_WORKING.md` 是父方推导和停止线，`README.md` 是恢复导航，`RESEARCH_STATE.md` 是当前前沿交接。它们是研究桌面元资料，不应被误当作新的 canonical 定理。

本页先前整理时曾记录 clean claim 被自动审核层拒绝（理由是对未验证 github.com 的网络写入风险），当时未将五源计作正式 done。这是保留的旧操作边界，不是数学反证，也不是当前写端点状态。后续 Boss4 KR 批再次完整实读五份冻结原件、比较后续正文，并按实际新回执核验五源归属；正文 checkpoint 与逐源 done 仍分开确认，精确回执保存在本批工作区。旧拒绝记录原字节保全，不改写为当时已成功。

## 共同模型与主问题

五页共同冻结：有限单位客户、有限非空共同目录、任意玩家人数、六人目标作为特例、每份完整有序历史纯 SPE、空主题/重复/零客户/任意平局均保留。主命题是 `Q-CAG-HALF: 2W>=OPT_m`，状态仍 OPEN。文件明确区分内部证明、内审、外审与新颖性；元资料没有新增外部文献或一般复杂度结论。

## 已承重的可复用组件

- `B16-DELETION-REGRET-ENVELOPE`（DR）对任意背景删除给出原实际节点 regret 的目录敏感包络 `ΣR_j<=ΣK_j-E_d`。依赖原 IC、删除收益差和单调分母；它没有把 `ΣK_j` 变成同一实际利润可支付预算。
- `B16-AVERAGED-SUFFIX-DELETION`（ASD）给出 `ΣR_ij+D/2<=Σ min{u_j,K_ij}` 及 `ΣR_ij<=((m−1)W−D)/2`。该式只控制原实际节点；较早虚拟回放（VR）和离轨叶退款仍需另证，不能直接调用精确 SPE 归纳。
- 静态最优排列桥在三人、1953 客户的精确完整策略中失败：`W=1735`、`OPT=1740`，全部最优支持排列的静态支付至少 1736。该例只否定静态辅助桥，`2W-OPT=1730>0`，不是 half 反例。
- 根可达性 incidence 条件若 `B>I/a` 且 `qB>β+floor(I/α)+r+1`，则某合法前缀不能成为完整根 SPE 的实际前缀。它排除特定同背景/同剩余人数实现，不排除离轨 child 或新编码。

## 失败接口与严谨边界

失败表明确拒绝：把单插入返还池支付全部删除误差；把平均删位误差直接当作精确 SPE 归纳；用驻留终局的一阶矩支付收益；将遗漏 `H` 独立交给 `W`；以及旧 route5a 的算术推论（`W>=(OPT-W)/2` 只给 `3W>=OPT`）。正确门槛可写成 `B>=OPT-W` 的条件桥，但一般成立未证。

对任意完整计划的全历史 regret 稳定性反族有 `B=H_(m-1)-1`、`W=q+2`、`OPT=q+m`，说明无人数无关的 `OPT<=2W+CB` 桥可直接替代精确 SPE 结构；它不是删位 SPE 反例。固定背景零 regret 的 18 客户例中，保留策略投影福利 17，而删后全部精确 SPE 福利 16，说明“实际 regret=0”不足以无损修复；背景不必是原根实际前缀，因此仍不否定主命题。

鲁棒前缀乘积式本身有效，但五人零 regret 时因子仍为 `15625/6049>2`；因子 2 的额外结构仍是开放义务。真实最优菜单账需要共同支付 `ΣQ_i<=W+ΣL_i`，该指定恒等式并未由本桌面稿付款。原稿称完整根菜单 Mfull 未闭合只保历史时点；后续完整银行族已反驳一般 Mfull，见下节，不能把它继续列成当前待证充分桥。下一步必须在真实分支切换时同时支付主题重选和新叶退款，或绕开删位直接证明 `OPT-W` 的共同付款；局部失败、低人数例、代数等价和多人赞同都不足以改变状态。

## 处置与接续

本页把五份元资料合并为一个资源审查对象，保留稳定 ID、冻结指纹、失败路线和下一义务；不新造 theorem/hardness/half 节点。KR 批保存五主源34105B及当前全文比较、逐源语义回执；原运行或旧审计一律不重复计作本批新运行。只有本批实际 checkpoint 与 done 回执才能分别证明新正文推送及五源处置登记。

## KR批的定义级复核：删除退款如何合法，但尚不能修复完整SPE

本批再次从定义给出DR的精确证明，避免把身份账本当作证明。固定原背景b+d中的完整SPE及其实际尾叶q，c为q的客户负载。删d后保留同一完整策略，原实际角色j改T后的后继仍按这个策略真实响应。设原实际收益u_j^old、原偏离收益v_j^old(T)，删除带来的收益增量分别为δ_j和Δ_j(T)。原IC给v_j^old(T)≤u_j^old，故

$$v_j^{new}(T)-u_j^{new}≤Δ_j(T)-δ_j.$$

若当前T覆盖客户x，其删后终局总负载l_x至少b_x+p_j(x)+1；逐客户增量为d_x/[l_x(l_x+d_x)]，随l_x不增。因此

$$Δ_j(T)≤\sum_{x∈T}\frac{d_x}{(b_x+p_j(x)+1)(b_x+p_j(x)+d_x+1)}≤K_j.$$

最大偏离包括规定行动，R_j≥0，而该规定行动自身也说明K_j≥δ_j。因此不需要从可能负的上界错误地取正，便有R_j≤K_j−δ_j。实际同叶

$$δ_j=\sum_{x∈S_j}\frac{d_x}{(b_x+c_x)(b_x+d_x+c_x)}.$$

这里x∈S_j保证c_x≥1，所以全分母正；d_x0只给零。按j求和，每个客户出现c_x次，恰得

$$\sum_jR_j≤\sum_jK_j-\sum_{x:c_x>0}\frac{d_xc_x}{(b_x+c_x)(b_x+d_x+c_x)}=\sum_jK_j-E_d.$$

没有冻结偏离后的真实后继；K_j只使用客户负载的安全下界。它也没有证明各K_j可共同由同一W支付。

对删除实际位置i的单一主题，后续j>i的实际前缀b_j已含该主题，所以K_ij=Σ_(x∈S_i)1/[b_j(x)(b_j(x)+1)]。同叶退款A_ij=Σ_(x∈S_i∩S_j)1/[c_x(c_x−1)]。偏离的删除增益还至多其旧收益，再由原IC至多u_j，故R_ij≤min(u_j,K_ij)−A_ij。实际覆盖次数c≥2的客户恰有c(c−1)/2个i<j对，退款合计1/2；各客户相加给D/2。这完整解释CLAIMS中的共同退款，较早虚拟角色改变与各离轨叶重置仍有独立义务。

[现自足ASD/VR正文](../引理/实际单删后缀的共同退款与全回放界--引理.md)另保所有有向删位退款D、较早角色递归重选及完整回放界；本页只对这五份入口实际引用的组件核定义，不把它们变成精确SPE修复。十八客户零实际后悔例的[全部可信菜单复核](零实际后悔修复障碍的父方独立复核--审查.md)显示实际节点R0仍可能必须从投影福利17降至16；任意整数复制排绝对零误差修复费，但A仅合法离轨背景，未否实际原根受限接口。

## 后续真值对照，不将旧OPEN整体抄成当前状态

| 桌面原记录 | 当前准确去向 |
|---|---|
| 全人数Q-CAG-HALF未解决、五人产品式因子15625/6049>2 | 产品式对任意完整计划仍是较弱已证关系；另路[五人半覆盖](../定理/五人半覆盖--定理.md)已证明真正五人目标。一般人数和恰六人未由这五源解决，不能把旧压力测试当五人当前开放。 |
| 全历史regret的任意计划、因子2近似计划和真正删位计划 | 三个定义域不同。花瓣反族只排无结构任意计划的常数稳定桥；因子2只给C≥1必要条件；来源为SPE删除的额外结构仍须单独利用。 |
| 原1953客户静态最优排列失败 | 仍是真完整SPE的辅助桥反例。43历史×6行动=258比较包含自身；不与另处排自身的215行混数。真实偏离重选与冻结终局排列不同。 |
| 原Mfull/全p封顶候选未闭 | [完整银行根菜单](../反例/笛卡尔银行完整根菜单的低值自洽分布失败--反例.md)已反驳Mfull、低值对称NE及全p-WP。四人根u4/3，而任意列混合最大查询≥19/14；完整菜单精确值59/36，所有对称NE同值。银行族对所有m≥4含六人有效，但仍过half。原在1953客户上的低浮点菜单值只说明那个固定输入没有给反例，不抵消另银行真反例。 |
| 因果单客户五人松弛24/125 | [锐包络](../引理/因果吸引亏空的单客户锐包络--引理.md)给完整全参数和端点证明；这是任意条件尾负载松弛，未证明一个目录/完整SPE可同时实现所有客户极值。 |
| 真实菜单净差、FTA或其它较弱共同支付 | 只按各自实际定义判断；本批不从Mfull否定自动推这些接口均假，也不从旧桌面OPEN认定它们已真。 |

五份来源分别保九项B16身份、失败适用域、原叶共同池缺口、父方未保存的三单位置/联合Mfull数值试验、研究桌面导航及精确接续义务。三单位置约426.619、426.629、436.604与联合415.970仅GENERAL_WORKING原文字报告，原scratch未作为正式资产保存，本批未补造向量、dual或运行日志。既有正文和原源已全读后进行上述比较，不继承历史盲审身份，无外审/新颖性认证。
