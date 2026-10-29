# Boss30 六人研究去重与接续简报

日期：2026-10-27（本对话恢复后的状态）

## 固定目标

研究对象是 `research/current/customer_attraction/model.md` 的原模型：有限单位客户集 `N`、有限非空共同目录 `S ⊆ 2^N`、恰六名单位权提供者按固定顺序观察全部有序历史并选目录主题。允许重复、空主题、零客户和任意历史依赖平局。固定任意完整历史依赖纯 SPE `σ`，终局福利为覆盖客户数 `W`，最优六主题并集为 `OPT_6`。主 Claim Q-CAG-HALF-6 要求对每个实例、每个完整纯 SPE 都有 `2W ≥ OPT_6`。若主 Claim 为假，必须给出原模型中的严格反例、覆盖全部有序历史的完整策略、以及 Fraction/整数可复现的全历史偏离核验；辅助松弛、局部菜单和静态点都不够。

用户最新要求考察一般 n 的解析包络、递推与活跃极大集归约。最新接续入口为 [general_envelope_audit/architecture_audit.md](general_envelope_audit/architecture_audit.md)：该截短逐客户模板必须 tau≤2H_n−1，故不能覆盖 tau=n,n≥3；既有 all-big 族的 M=n、OPT/W=2−1/n 排除普适近边界常数秩说法，但不反驳仍未证明的严格最小反例归约。旧混合席位预算直接给 OPT_n≤(2−1/n)W+(1−1/n)D_shared；需在同一 W 中支付共享遗漏的剩余缺陷。

同步到 `8ca370ad` 后的范围纠正：六人现有分数覆盖条件证书已到 tau_C≤9/2，见 `SYNTHESIS.md`；本工作区旧 tau_inc≤149/50 的 half 范围已被较早的更强条件覆盖，其带核心定量式另有意义，不能继续当作范围突破。六人任意目录及一般人数仍 OPEN。

## 已可靠闭合或可直接引用的内容

1. 恰五人任意目录、全部有序历史、任意平局的 `2W ≥ OPT_5` 已有完整精确证书（见 `research/current/customer_attraction/five_player_half.md`）。它不是六人定理，也不能作为任意背景的五人利润定理。
2. 目录至多六个 inclusion-maximal coverage 的子类已有联合预算 half（见 `six_maxima_joint_bound.md`）。把最优六主题扩成极大主题或删去其它主题不会自动保留原 SPE 的离轨续局，因此不能把该子类外推到一般目录。
3. 六人若实际倒二主题 `A` 被前四主题中的固定两名逐集合包含，已有精确条件 half；若 `A` 内每个客户被前四至少三名覆盖，也有精确条件 half。两者都是结构特例，不覆盖 `A` 被前四包含 0/1 次的轨道。
4. 任意尾长的共同末位报价、隐藏回复投影、同菜单末回复互查、同源回复再查询等是真实 SPE 比较行，已经通过各自范围的有理核验；它们仍没有把早期、倒二、末位跨枝损失放入一份可支付的全局预算。
5. 四主题、六人、全部 15 种非空客户类型重数 `{0,1}` 的 32767 个实例已递推全部历史依赖纯 SPE，零个 half 违例，最坏 `W/OPT_6=6/7`；这是有限证据，不是主定理或反例。

## 已精确排除、不要重复投入的路线

- 逐位置 `M_i ≤ u_i`、逐人安全值、强/弱 iid 福利桥、固定实际缩放税、冻结前缀固定系数归纳；
- 把 SPE 当静态 Nash/CCE，或直接把五人零背景证书套进六人后五位；
- 七极大六人的逐席 `seat(t,j,k)` 行。已有完整 SPE 反例说明该行并非由 SPE 推出（但该实例本身仍满足 half），所以只能使用合法第 `r` 大席位或 aggregate/order-statistic 行；
- 旧 437/557/728 行松弛的调常数、uniform-`K` 补偿、把互斥分支的信用直接相加、局部菜单或 LP 可行点；
- 继续扩大有限无反例扫描。有限搜索只有在检验一个新精确候选、发现可复现目标反例、或识别新结构边界时才有价值。

## 当前真正开放的数学义务

1. **七极大六人 44 轨道的合法闭合：** 构造只使用真实 order-statistic/aggregate 关系的有理证书，尤其处理倒二被前四包含 0/1 次的轨道；不能假定七极大化保留原策略树。
2. **跨枝共同付款：** 从真实早期 IC、倒二 IC、末位改选/报价和共同 `K` 中得到一个不重复使用福利的 `Δ ≤ E`、`RM/UR-gap` 或等价全局关系。局部恒等式本身不够。
3. **全模型反例：** 若走反例路线，必须写出每个有序历史的行动和全部偏离收益，证明完整纯 SPE，并精确算出 `2W < OPT_6`。当前所有已知辅助坏点、LP 停界和静态反例都不满足这一标准。

补充已读到的正向边界：`research/workspaces/customer-attraction/R-d54cef1094414cc6a98575e671bd060e/dense_shared_seven_n6/dense_shared_seven_n6.md`（commit `fe99fcfe`，数学提交 `1ffe0346509c98828615b6f1c13f03300a83d3db`）已对恰七个 distinct inclusion-maximal sets、六人、且每个客户至少属于两个极大主题的 dense-incidence 子类给出 `U≤2W`。证书只用合法 `M_0..M_3`、六个真实末位 BR 和六个真实两人税，3840 个 literal 列的 Fraction 最小余量为 `15591089/238321440`。因此七极大缺口可进一步定位到含 singleton-incidence 客户的 mixed 子类；不能把 dense 结果与 singleton 块相减，也不能误报为一般七极大定理。

另一个可复用的表示工具是同覆盖标签商编译：`research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_4/README.md`。它把带重复覆盖标签的完整历史纯 SPE 依历史选择代表 lift 到真正集合目录，保持根覆盖序列、每位收益和 `OPT_m`；这有助于审查候选反例是否只是重复标签的伪区别，但不限制原模型为 count-policy，也不证明 half。

本轮代理已独立重构 `research/workspaces/customer-attraction/R-c499e3814bbe4743b298e230b37ddca1/research_d/incidence_tau/README.md`（checkpoint `e49fe7e3164fdcb38d32e77cc29534ba79af892f`）。Exact 条件是六人最大覆盖 incidence-LP 的 `tau_inc≤149/50`；后向归纳沿每个真实前缀的 forced-maximal/follower 分支给
`W ≥ c + (U-c) Σ_{r=1}^6 1/(6+(tau_inc-1)r)`，端点系数 `1006430343355/2012347307572 > 1/2`，Fraction 审计确认 `tau=3` 已不足半覆盖。它是一般 incidence 条件定理，保留全部历史和任意平局，但不覆盖 `tau_inc>149/50`，所以不是 Q-CAG-HALF-6 闭合；不得与七极大 dense/singleton 证书混称。

另有一个应停止重复的精确方法边界（commit `de15c9af`）：在六人、仅一固定早期主题包含倒二 `A`、且 `A` 客户前四负载至少二的指定结构中，把 common/逐前缀/逐异常 `K_i`、`L_A` 与已审 source-cut 行全部加入，七客户列的有理 Farkas 见证仍给目标 `-9/361`。这只否定该 enriched local cone；它不是结构类反例，也不说明真实跨枝预算不可能。若重试这类路线，必须加入本质新的跨源信用或改变表示。

七极大六人 source-(11) 的另一轮尝试也已精确收束（commit `68dd9d439424562c874d41e451114a7c3932c4ca`，入口 `notes/n6_seven_source11_failed.md`）：初报的正证书漏掉了末位份额中的 `q*f/|J|`，修正后在 130 个压缩状态上，合法 `M/L/T` 四参数族的统一余项最优值约为 `-0.0231282509`（Fraction 见脚本）。因此该行族不能闭合；初报正证书作废，这也不是目标反例。

## 给所有研究代理的共同交接

先读 `model.md`、`current/customer_attraction/README.md`、`customer_attraction/RESEARCH_STATE.md`、`FAILED_ROUTES.md` 和本文件；再按所选义务读取唯一原文。自由选择证明、反例、表示、条件引理或障碍，但每项工作都要明确：Exact statement、量词与定义域、它与上述已知资产的差异、证据等级（定理/条件定理/观察/障碍）、可复现输入与文件路径。阶段性成果写入个人 workspace 并用根 `work.py checkpoint`；只有回执 `status=pushed` 才算远端保存。

本简报只负责防止重复和保留真实边界，不把路线变成方法白名单。任何新路线若不依赖上述死桥，仍可直接推进。

