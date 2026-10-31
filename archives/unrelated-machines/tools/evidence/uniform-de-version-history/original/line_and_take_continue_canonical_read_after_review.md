# D/E canonical：实际全文 read-after 审查

对象：`co-work-anl-boss11/research/current/unrelated_machines/line_set_packing_and_take_continue_compilation_obstructions.md`。

本次实际全文读取并核验的 SHA-256：`c50fb9792f101967a996913f2c6ac4269035143fe2a137b831dfdbdcd6c40eee`。

**数学结论：§1–3 的 D 仿射线 uniform compiler 与 §4–5 的 E take/continue 常数反例均通过，未发现主数学 fatal。** 下述两处 scope/provenance 措辞仍需精确化：D 的 tuple-as-group 不变量应表为“不再自动保证”；E 的 root 独立 actual checks 按本次任务说明仍在进行，不计为本审查已见的完成证据。解析证明不依赖这两项运行或措辞。

## 1. D 的读取次序与记录保真

本审查先仅读取 D Exact，SHA `a1334a82f1acf7fd9562c2d44e6620b84b5a1acd37993ce3c7131b81a8e56472`，独立闭合全部 Hall 子集，再实际核在线 arXiv v1 的 §2–4，冻结独立记录，SHA `3576492af3ca5e319a888cca805897a850472ad3dca00cc80d1e647bddff6ffd`。

随后才读作者 Proof，SHA `e9ca11c2975bc8509681619857e772bb0086a489dc9c56a8cb9b1833a08c1e3b`，另冻 read-after，SHA `f6c5e7034c6239504efc0b1e2267ae28ad2c9906d7fa972f2cd9fe7ff5ce2c1c`。本次再次核验这两份审查记录原 hash 未变。

root 后来的 raw primary 下载及 SHA 为 root 的实际操作；本审查实际读的是在线同版原文，不冒认下载/亲核 root 本地 raw 字节。canonical 对这一归属的表述正确。

## 2. §1–3：D 的正式数学核对

**对象不变。** group 仍是一项 indexed constraint，state 是其 allowed tuple；每组 k 个不同变量、变量 constraint-degree≤R、j_x 注入、变量 tag 分离、prime R、非空显式菜单，全部承重条件保持。所有 indexed states 的 kR incidence jobs 保留，只有其 private 1/(kR) 或唯一 resource1 两个有限端，selector 仅本组 private，未添其它 jobs/逻辑。

**全部 Hall 子集。** 对任意 local state 选择和任意 F⊆G，r_x≤R；同变量 selected lines 因 intercept 注入不重合，pairwise overlap≤1。二阶容斥给 union≥r_xR-binomial(r_x,2)≥r_x(R+1)/2；tag 分离及 k distinct variables 给 Σ_x r_x=k|F|。于是 |N(F)|≥k(R+1)|F|/2≥ceil(kR/2)|F|，包括 kR odd、k=1、R=2、空 F。不是只核整个 pool。

**整数 allocation 与 actual jobs。** b-slot Hall/flow 给每 group 恰 b 枚不交真实 resources，不要求 source labels 一致，不要求按变量半条 line或 product 领取。只有 selected state 的 B_g jobs 导出，其余全部原 incidence 留原 private；selected load=2-b/(kR)、unselected=1、resource≤1。因此 all-jobs C≤3/2，非空 G 的 selector 下界又给该精确结构类 ratio≤3/2。

**source scope。** 真正全满足 assignment 的 same-slope/different-intercept 平行性给 OPT=1，但 primary near-perfect YES≥1-ε 不自动提供它；NP⊆BPP 例外、full-set matching 与 partial bundles 之别均正确。不是一般 source compiler 不可能性。

**空关系与位复杂度。** 空 A_g 保 selector 会无端，当前明确排除，删除/加 dummy 须另证 promise。vR²+a machines、m+kRa jobs、2kRa+a finite entries 与 dense product均保持；按真实显式长度收费，不偷称 polynomial in logR，固定 k,R 时才直接得到普通 source-polynomial compiler。

**一处 scope 措辞建议。** §3 说 tuple-as-group 加 dummy “会破坏 r_x≤R 与同 intercept风险”。严格说这种更改**不再自动保证**本证明的不变量，而非每个实例必然破坏：每 relation 只有一个 tuple 时并不因此增加 group incidence 数。此措辞应弱化；核心结论已明确“不排那个不同 compiler”，所以不是 D 的主命题 fatal，也绝不能据此对该不同 compiler 宣布 3/2。

## 3. E 的 proper statement-first 与另一审查路线区分

旧名含 Exact 的 source 本身含完整证明。canonical/root 明示另一审查者 general 早期先读该 source，原“Exact-only”标签因此不能代表 blind reconstruction；其路由错误后来以另冻 scope correction 撤回盲审身份，旧字节与实际 Fraction 核验保留。这是另一人的证据路线，本审查没有采用其证明或认领其软件运行。

本人的真正路线是：首次仅读新 statement-only，SHA `c78b878296d50e7d84ee1389e0eeb7e3796e1ee7b3c1242b54dd5d4cd3d1e41c`，独立给 V/OPT 及 literal 30-job 时间表，冻结记录 SHA `8c5980dbbf6234cf34d2900d98359fc51c50318a932bfb184b6676ee2ab6ba46`；经 root 读后授权才首次读旧含证明 source，SHA `27d2926563eeb34591ca44a75cf09ca623719827a67eedff485edf78e22053ac`，另冻 source-proof read-after SHA `fcad85bc9d4142f883a515dae08e72e3a421a9ab244f3c98c8c32c122e236d77`。

本次再次核验本人的两个 E 记录 hash 未变。不能把旧 misnamed Exact 当 statement-only，也不能把另一人的 proof-aware check 混记为本人的盲重构。

## 4. §4–5：E 的正式数学核对

**完整矩阵不变。** 每 a 的 r_take1、m_off/take2、l_off/accept 及 weights 都与 statement-only 一致；两源 items 仍 global resources。全局 private15、resource11=26 machines，selector9、incidence21=30 jobs。新增 finite-count 57 正确：selectors 每 a 有1+2+2=5 finite ends，共15；incidences21各2 ends，共42；合57。

**精确值。** 三源 agents 只有两不可拆 items，故 SC max-min=0。目标逐 a 取 r{x_a}、m_take2{y_a}、l_accept{z_a} 得质量2/5、3/5、1，九束不交；min>2/5 又会迫三个 r 都领取唯一 u1，故 V=2/5。

**全部30 jobs actual certificate。** 9 selectors 落上述 states，9 own/accept incidences 导出，其余12 incidence 留原 private，包括全部 unselected off-state jobs。每 a 五 private loads=8/5,1,7/5,1,1，九辅助资源各1、两原资源idle，C=8/5。与独立记录的30-row exact start/finish表相合，原 job 一次、原 finite endpoint、无丢 job。

**任意调度 lower。** 假设 C<8/5，r 的唯一 selector private 强迫三枚 r,u1 incidence 全去同 R(u1)，其工作3>C，矛盾；其它 state choices、unselected exports 或排序均未被限制。故不是仅给定模式 lower。

**decoder scope。** δ=2/5 target 正值证书不能变出三个源 agents 全正值的合法 item allocation；任意统一 c>0 的 all-agents cδ 合同连存在性都失败，重排全部原 items也无济于事。不排所有 DAG、existing normalized leaf selector-tree、其它守卫/activation、不同矩阵或更强输入 promise。

## 5. E 的 root actual checks：本快照尚待证据落定

本次任务说明 root 正在独立回算 E 完整原矩阵/30 jobs，完成后将补 checks 出处。因此本记录只认证解析 proof 与作者/独立证书一致，**不预先认证 root 尚未交付的实际有限运行**。

canonical 当前句子已写 root“另从原矩阵精确回算”；在实际运行和出处冻结前，应理解为待完成计划或将文字标 pending。完成后可补独立 output/hash 作 read-after 范围延续；有限 checks不能取代这里任意调度下界或一般 decoder 矛盾。

本审查未读取另一人的 scope-correction 文件、Fraction 输出或 root未来回算 JSON，故只按 root提供且canonical明示的路线记录其归属，不冒称亲核这些未读文件的字节。

## 6. 冻结结论

**指定 c50fb9…快照：D §1–3、E §4–5 主数学通过；scope/provenance 的两处精确化如上。** 旧来源与 proper 独立记录未改。仅 scratch 写本记录；未写 repo/Work/Git、未运行软件或枚举。此认证不涵盖未读的其它 compiler 或尚未落证的 root checks。
