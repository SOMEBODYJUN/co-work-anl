# round3 relay 第二次本人区保存交接

2026-10-23。一般 Q-CAG-HALF 仍 OPEN。本轮不扩样；本人不执行 git、不改共享或旧冻结。此页供 root 保存本人目录并向同行交接，不表示已远端保存。

## 可接续的全部输入关系

1. `review_optimal_exchange_kernels.md` 独立核 BER、HARM、随机配对与正 alpha 核，包括同槽 J、alpha↓0 和零客户边界；新增锚定查询核及 p0 私有块静态注入。
2. `optimal_exchange_potential_and_query_credit.md` 给固定 Beta/owner 势、原效用的 INSERT 分解、真正全深度最优前缀信用界，以及直接适用原实际-prefix matching 的 DIRECT-REPEAT：每个客户所有非owner查询信用之和至多 (a_x-1)/2。R、I 分账；没有将 I 重复误差塞入 R 预算。
3. `hall_owner_anchor_connection.md` 证明 Hall-B 的任意可行流都避开 owner-complete 角色；强制最优前缀的全部已锚定角色因此零入零出。这一同叶隔离已获 credible 收到陈述/证明后的独立重构，不称严格盲审。
4. `common_world_exponential_representation.md` 将已有 HYB/owner 势写为共用 Exp(1) 角色钟；逐样本 cap、期望 F_Q/INSERT 与原效用边际完全一致。root 独立重构通过；准确等级为既有势的等价表示，未增加动态付款。

相关 Fraction 审计及冻结 JSON 均由 README 指出；不修改旧运行记录。没有通过新增实例数量推断一般正确性。

## 现在真正未付的共同费用

主线对象以 credible 的 `../credible/owner_hybrid_transport.md` §5 和 root 的 `../GENERAL_PROOF_WORKING.md` 为准。固定最优 matching/owner，在原实际叶用一份 Hall-A 的 I 路由 f 将 G 取消为遗漏客户质量 gamma，令

    rho_x=1-gamma_x，    sum_R rho_x=OPT-W，
    eta_i=u_i(I)+gamma_i，    sum_i eta_i=W。

同一实际路由可同时保留局部指定取消 delta_i=min(b_i^G,|Q_i intersect R|)。只将 rho 接入原实际前缀真实查询的递增角色流，每个状态 (i,a) 具有全偏离收益 D_i(a)、实际吸收 A_(i,a)，最终只购买一份完整原 IC 系数

    w_(i,a)=A_(i,a)/D_i(a)，
    K_i=sum_a u_i A_(i,a)/D_i(a)=K_i^src+K_i^in。

零分母对应零吸收，系数取0。SOURCE-NET 已支付所有初始化 source 的当次吸收：K_i^src<=eta_i；根没有更早角色到达，故根行全部已付。

**尚未证明的是**：能否共同选择 matching、gamma/f 及合法真实捕获分流，使

    K_i^in<=eta_i-K_i^src  对全部 i，

或证明足够的较弱总费用关系

    sum_i(K_i^src+K_i^in)<=W。

前者只是一个充分的逐角色接口，不声称必要。一般 half 可由后一关系与完整原 IC 闭合，但这里没有其证明。不能让 K^in 重新领取一份 u_i，也不能把 A/B 两图或互斥叶的 I 容量当多份预算。

## 准确停界及下一承重点

原势 ROLL 的等价未付是跨真实 rollout 的联合信用与去槽势重置 sum_i(e_i^-+D_i)。最优前缀链必须用正文独立定义的 B^i=原 sigma 在完整最优前缀 T_pi1,...,T_pii 后的真实 rollout；它不同于 DIRECT-REPEAT 的原实际-prefix Y_i。形式去槽只是势计算，不是删祖先后的 SPE。

Exp 共用世界可使 cap 沿真实未来覆盖者单调传递，首次平均分流为真实 1/c；但后续查询和 IC 权依同一钟适应。缺少的是从这种适应选择回到无条件 whole-IC 的解耦、记忆性上界或别的共同付款，当前没有证明。任意合法叶的静态最优性容量也不能代替其内部 prescribed sigma 完成所需的 IC。

本分支本轮停止在这一精确未付关系。不再把势重表达、静态最大流、旧自由分数对偶、有限无反例或固定深度行补强计作一般 half 进展。后续若有新全输入 whole-IC 兼容关系，可直接从本页和 root/credible 当前对象接续。
