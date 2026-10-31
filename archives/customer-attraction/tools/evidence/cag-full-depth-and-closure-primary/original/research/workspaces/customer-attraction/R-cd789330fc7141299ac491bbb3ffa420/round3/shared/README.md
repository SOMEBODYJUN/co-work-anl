# round3/shared：全输入共享遗漏与最优交换

2026-10-23。已读最新 AGENTS，只攻任意人数、任意有限共同目录、全部有序历史纯 SPE 的一般 Q-CAG-HALF；目标仍 OPEN。不扩受限客户归属、私有谱或固定规模正面定理。不执行 git。

本轮主资产是[最优元组随机替槽的调和预算](optimal_exchange_harmonic_budget.md)：一次 Bernoulli 替槽控制 N\\O 的全客户势，保留最优及真实元组全部 incidence，允许空和重复主题。root 独立重构、补全随机匹配及锚定版本并精确核验，见[本轮一般工作稿](../GENERAL_PROOF_WORKING.md) §3、§5。这里静态关系已证明，真实 IC 同核差额及跨子树收费未闭，不提升为 half 或 SPE 性质。

下一精确义务：对实际 C 和任意最优 O，使真实偏离捕获的遗漏信用、比较重复信用及 I 同时收费一次，推出 |O\\C|≤|O∩C|+2|C\\O|。Bernoulli/Beta 与原单位效用积分可共用覆盖次数变量，但原 IC 只在整个积分后非负，禁止任意重加权被积式。N\\O 在离轨叶的新支持不能被叫成实际 G。

后续得到[全局最优交换势及互核](review_global_exchange_potential.md)：shared 与 relay 独立找到同一有限全局势，具有 0≤单位边际ℓ_i≤原单位收益，误差只在 O 内；同一实际叶的总误差≤I、O外边际利润总和恰G。shared 又独立重构 relay 的逐步真实 OPT 前缀查询误差，每客户≤H_(a−1)≤a−1。两条信用的对象不同，尚无跨真实 rollout 的共同支付；合稿与审计由 relay/root 汇总。

当前新的主组件是[owner 分块全局势](owner_exchange_potential.md)，由 shared 提出并经 root/relay 盲重构通过。Q_i⊆T_i 只薄化静态比较基线；每个 hybrid 都被合法 T/B hybrid 逐槽支配，不把 Q 当玩家动作。常数从Σ1/a变为OPT，边际仍满足UNIT；实际同叶得到精确一次预算Σe=I−κ、Σℓ=G+κ。first-owner 合法最优前缀查询的重复信用加强为H_a−1。它保留所有真实动作客户兴趣，适用于全输入；跨真实rollout的去槽差/客户流收费仍OPEN。

已对 credible 两项[同叶 owner maxflow 运输作独立解析核查](review_owner_hybrid_transport.md)，A/B 均通过；过程为读到完整稿后的独立重构，非盲审。全部J的harmonic hybrid与出割端点均无缺口，[独立 Fraction 审计](audit_owner_transport_independent.json)通过。两张图不能共用库存各付一次，也未解决与递增R流共用whole-IC系数。

新增[锚定最优查询后的残余运输与共同资金](anchored_owner_transport.md)，经 credible 解析核对通过：若B在K槽固定T_i，可将outsideO普通利润完全通过O\\∪_K T_i的资源运走，因此与锚定查询上的捕获利润互不重用，逐role资金之和≤原完整单位利润。任意K只是静态资金；K为完整OPT前缀时，所有active角色均为原σ真实后继，才可合法购买共同whole-IC。未将这些新系数θ当成旧actual-prefix R流的固定w。

附带单次诊断 [diagnose_direct_floor.py](diagnose_direct_floor.py)、[输出](diagnose_direct_floor.json) 只检验精确一般候选 u_i≥OPT_m/(2m)：用已存 X/Y 完整策略的一次固定 IC 锥、一个比较元组，浮点 LP 提案后用 Fraction 验全部 258 行。未分离；输出点 root=1、W=3、OPT=4。不构成该候选的正面证据，不扩样，不计新一般机制。按 root 指示主线回到交换核与真实 IC。
