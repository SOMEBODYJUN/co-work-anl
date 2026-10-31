# 作者完整实读及后置自攻：shared-UD tiny state potential

2026-10-18，/root/sol_general_repair。作者自核，**不是独立审票**。不给正在 Exact-first 的 NSW；仅先给 root。冻结原 Exact/Proof 字节不改。

## 1. 实际读取范围

本轮实际完整读取以下两个文件，工具无截断：

- Exact：`sol_general_repair_shared_ud_tiny_state_potential_19_10_exact_v1.md`，3867 bytes，SHA256 `80fd4ff5b6aab2993e42b995ea369e9441543e754cf3642800c84a784c63cf1d`。
- Proof：`sol_general_repair_shared_ud_tiny_state_potential_19_10_author_proof_v1.md`，13302 bytes，SHA256 `409ce88433cd698d477862098023f7e064dbe7a75426117f3c617e70aad7f435`，完整 §1–9。

没有打开 fresh reviewer 的独立稿；没有把其尚未产生的意见当支持。未新开 canonical 或改变原 k^4 tiny19/10 的审查身份。

## 2. 最承重的交换耦合

固定 λ>0、profile S 和其中任意 λ-optimal fractional utility W。叶匹配的 vacancy matroid M 是满秩 transversal matroid N 的 dual：S⊂B 独立 iff B\S 含 N 的一个 basis，也就是能完整匹配所有叶。每个资源的 helper-incidence copies 与零 dummy 是 M 的 parallel extension；loops、rank0、空 B 都不影响此定义。

Proof §4 的单元素最优敏感性可以不用泛称 greedy，直接由 symmetric basis exchange 付款。若 B 是最大权 basis、e∈B 被删除，令 C 是删除后最大权 basis；存在 f∈C\B 使 B−e+f 与 C−f+e 都为 basis。后者在原 ground、前者在删除后 ground，故

    wt(C) ≤ wt(B)−wt(e)+wt(f) ≤ wt(C),

两边相等。所以只换一元素足以保持最优。dummy copies 保证删除 helper candidate 不降 rank。插入一元素同理：若新 optimum 使用 e，和原 optimum 做 symmetric exchange，即得到原 basis 中只换一个元素的最优新 basis。可用 fundamental circuit 的最小权元素实现。

删完旧 helper j 的 copies 后，其他 helper 的 weighted utility 只增，总增 G≤旧 j 的 weighted utility A。加完新 copies 后其他 helper 只减，总损 L≤新 j 的 weighted utility B。A,B≤λ_owner w_j。即使同一 outer 还有其他 helpers，owner 坐标仍为

    B−A+g_owner−l_owner ∈ [−A,B].

其他坐标在 [−B,A]，跨 outer 的 L1 至多 A+B+|A−B|=2 max(A,B)。这同时支付 L∞、L1。它允许叶 matching 整体变更，并不假定 matching 路径只改常数边。

给定 fractional W，只在证明中使用 integral network optimal face 的凸分解。每个分量在 λ 上也 optimal，helper claims 可补零 dummy 为 basis；逐分量执行耦合后取平均。算法不求此分解，也不把它作 oracle。两条范数界在平均后仍保留。

## 3. 势近似与位长

精确 P(S) 仅用于数学比较。QP 改写中的严格凸性只作用于 deficits，足够得到

    P(S)−Φ(W_hat) ≥ ||d(W_hat)−d*||².

不需要 W* 本身唯一。可实现后端是固定 profile 的资源分配/完整叶 matching 线性优化。若 a_u 是 λ 加权 helper candidates 在 u 上的最大权，则优化值等于 Σa_u 减去一个以 a_u 为边代价的最小费用完整叶 matching；未被叶使用的每个资源交给 argmax helper（或零 dummy）。这不枚举 helper 的 joint profiles。

Frank–Wolfe 的 γ_t=2/(t+2)，从 t=0 计，第 t≥1 个 iterate 的 vertex 权重正是 2(r+1)/(t(t+1))，r=0,…,t−1。原 integral payoff 坐标来自输入 w_j p_jsu 的和；取这些输入乘积的一个公共分母 D_1，其 log 长度至多输入分母位长的多项式。故 W 的分母可取 D_1 t(t+1)，flow 只需 t(t+1)。gradient 和 matching costs 再相乘仅增加多项式位长，没有逐迭代分母递归倍增。固定次数 ceil(4k/ξ)、固定初始 matching 与 tie 规则给每 profile 确定的 P_hat。

Φ 具有 gradient Lipschitz2、域 diameter²≤k，初始 gap≤θ+kc²≤2k；Proof 的 gap≤4k/(t+2) 与 iteration count 因而相容。

## 4. 常数与 FAIL 的真实语义

本轮用 Fraction 实际反算：ε²=225/256；k≥2 的 summed profile-gain 下界在 Dsum=9/80 为 293/81920；k=1 分支为 177/8192=885/40960；最终 prefix-flow 后下界为 799/4096。

若近似 W_hat 某坐标小于25/128，deficit 稳定性保证精确 P 的最优 deficit sum 大于9/80。实际 V≥15/16 则给一个共同真实 target profile O，但它只在反证中出现；submodular exchange 和曲率界强制至少一个可枚举单 helper 替换增 P≥ρ/H。新旧近似差至少ρ/H−ξ>τ。因此无增益 FAIL 证明的是 actual V<15/16，**没有把某个必要 LP/λ 点失败误当 actual 不可行**。

实际 V<15/16 时仍可成功或继续；势有界以及每次 P_hat 增τ保证所有输入多项式停止。初始叶图无完整 matching 时也由 exact threshold-UD iff 直接推出 actual V<15/16。

## 5. 独立形式的有限枚举，不是新审票或算法软件

作者新写并实际执行 `sol_general_repair_shared_ud_potential_exchange_small_network_audit_v1.py`。它直接枚举原资源的 helper ownership 和剩余叶 matching，不使用 matroid exchange 算法或 Proof 的 coupling 构造。对每个旧 integral optimal outer-vector，要求新 optimum 中实际存在同时满足 weighted L∞、L1 以及 exact welfare difference 的向量。

240 例均通过，共26674个可行原资源 ownership、242个全部旧最优 outer-vectors；160例异质 λ，160例变更 helper 还具有同 outer 的其他 helper。资源数4/5、helpers3、叶1/2；不能满足新 Exact 的 tiny 限制，但所审的交换 lemma 本来不依赖 tiny。所有计算使用 Fraction。stdout 原样冻结在对应 `_run_v1.json`。

此只检验有限 integral exchange coupling，**没有执行完整 Φ/FW/profile 搜索、tiny 输入、最终 prefix-flow 或全部 UM jobs**。没有端到端软件认证，也不声称 root 已打开或执行此新 code。

## 6. 结论与边界

本轮完整作者实读及定点攻击未发现 fatal。保留待 Exact-first 独立重构的身份；不把本自核当 fresh independent review。single-state outers、全 homes 独占、B-only threshold-UD extras、k^4 tiny 都仍承重。一般 UM-TARGET-v1 继续 OPEN。
