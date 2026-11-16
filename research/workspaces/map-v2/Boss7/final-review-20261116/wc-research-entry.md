# Boss7：补覆盖到同动作全局 Rosenthal 势的研究入口

快照：2026-11-16 17:01 UTC，当前克隆 `e92ab4c379a44694fb33abc8b2a6f20d0b979596`。本记录实读当前登记、现役边及下列正文，另用精确分数重算两人十三客户小例；未重跑历史搜索。`research/registry.json` SHA256 为 `202c608164e5e7f706c6178d16a0f13089c01abf7b7fdc3cc5b091370fb1f4a8`，`map/integration.json` 为 `135bdadeca23e9346a77097d2818dd9c005e68f7d906af6b4eae587977b141fb`。

**本窄路线已支付完整目标。** 三个数学端点当前均为 v1、`proved`；修订后的单源缺口边与两源 ALL 完整迁移边均已进入当前 registry/integration。没有本路线尚缺的不等式或必须另开的比较任务。旧复核页所说“尚未整合”是其较早快照状态，不能沿用到本快照。

## 1. 从这三个实际对象进入

下文以 S、B、T 为阅读简记，不是新增对象。

| 简记与稳定 ID | 精确正文路径 | 在本路线中的作用 |
| --- | --- | --- |
| S：`customer-attraction/submodular-shapley-monochromatic-static-pne-global-potential` | `archives/customer-attraction/state/定理/固定背景下单色静态Shapley均衡的全局势最大性--定理.md` | 独立的同色静态 Shapley 定量势差上界；覆盖专门化包括任意固定实背景。 |
| B：`weighted-congestion/static-customer-coverage-complement-harmonic-transfer` | `archives/weighted-congestion/state/定理/客户均分到非负多项式拥塞的静态补集转移--定理.md` | 覆盖动作逐客户取补集；精确保持固定对手偏离差、反转势差，并构造合法多项式费用。 |
| T：`weighted-congestion/harmonic-complement-monochromatic-pne-global-minimum` | `archives/weighted-congestion/state/定理/调和补集拥塞的同动作精确均衡是全局势最小点--定理.md` | 完整目标：同动作精确静态 PNE 的全状态 Rosenthal 势最小性及其定量下界。 |

S 的同一势/收益积分可上溯至 `M-c81148ab9bca4553bd1b73e97b080e81`，正文 `archives/customer-attraction/state/定理/共同删除势的全域效率与单调次模提升--定理.md` 的“全域构造和收益积分”。现役边 `ca-r33-shapley-bernoulli-fixed-background-monochromatic`（文件 `map/edges/phase3-math-round33-shapley-3a-821d1061aedde9ad/shapley-bernoulli-fixed-background-monochromatic.json`）是 `accepted / unconditional / whole_result`：带身份 Bernoulli 抽样识别同一 Shapley 势与真实收益，再逐参数使用次模性，完整推出 S。无需把一般抽象次模价值误认成非负客户覆盖。

## 2. 当前两条承重边：单步与整条不可混读

| edge_id 与现役文件 | source → target、状态及实际交付 |
| --- | --- |
| `wc-static-complement-transports-same-action-deficit`；`map/edges/wc-boss4-deficit-repair-repair-3be320ec40a8e3a3/static-complement-transports-same-action-deficit.json` | B → T；`accepted / conditional / contribution`。交付补集解码、PNE 变号与双方缺口恒等式；`remaining` 是源定量势差上界，已由下一条 ALL 边支付。单源边本身不能无条件推出 T。 |
| `ca-wc-shapley-and-complement-transfer-global-minimum`；`map/edges/ca-wc-static-complement-transfer-3c-ccaee520d97ff0de/shapley-and-complement-transfer-global-minimum.json` | **ALL {S, B} → T**；`accepted / unconditional / whole_result`。S 给符号，B 给变量/偏离/势的精确对应及合法费用，联合完整推出 T。`unconditional` 表示列明的模型假设下没有待证数学前提。 |

当前 `map/integration.json` 已含任务 `wc-boss4-deficit-repair-repair-3be320ec40a8e3a3` 和 `ca-wc-static-complement-transfer-3c-ccaee520d97ff0de` 的收据 pin。旧路径 `map/edges/wc-harmonic-complement-recovery-3a-94bcf27212441a7a/static-complement-transports-same-action-deficit.json` 已被替代，未列于当前 `registry.edge_files`；应读表中的修订路径。

## 3. 完整模型、恒等式与方向

有限资源/客户集 X，共同有限非空动作目录，m≥1 名**单位权**活动玩家；每个 x 的质量 v_x>0，外生参数为任意固定实数 b_x≥0。源覆盖动作 S_i 映为目标资源子集 X∖S_i，目标费用为非负系数多项式，并且在全部实际可访问正负载节点满足

\[
p_x(j)=\frac{v_x}{b_x+m+1-j},\qquad 1\le j\le m.
\]

取目标同动作精确静态 PNE s=(B_0,…,B_0)，其补集源剖面记为 s̄；任意完整目标剖面 t 解码为 t̄。允许空动作、弱平局及同覆盖异标签；取商后把起点统一提升到同一个源标签即可，逐玩家提升比较剖面不改收益或势。

固定其他玩家于同一个 s_{−i}，其源覆盖数 c_x^{−i} 固定。目标玩家使用 x 时目标负载为 m−c_x^{−i}，故

\[
C_i(A_i,s_{-i})=K_i(s̄_{-i})-u_i(X\setminus A_i,s̄_{-i}),\quad
K_i=\sum_x\frac{v_x}{b_x+1+c_x^{-i}}.
\]

于是 δ_i^C:=C_i(t_i,s_{−i})−C_i(s)=−δ_i^u，其中 δ_i^u:=u_i(t̄_i,s̄_{−i})−u_i(s̄)。精确静态 PNE 双向保持，给 δ_i^C≥0 和 δ_i^u≤0。若源总活动覆盖数为 c_x，目标负载恰为 m−c_x；置 H_b(c)=Σ_{ℓ=1}^c1/(b+ℓ)，有

\[
\Psi=\sum_xv_xH_{b_x}(m)-\Phi,\qquad
\Phi=\sum_xv_xH_{b_x}(c_x).
\]

因此双方共同缺口精确满足

\[
\underbrace{\Psi(t)-\Psi(s)-\sum_i\delta_i^C}_{\text{目标缺口}}
=\underbrace{\sum_i\delta_i^u-[\Phi(t̄)-\Phi(s̄)]}_{\text{源缺口}}.
\]

**恒等式不提供缺口的符号。** S 的独立同色不等式给 Φ(t̄)−Φ(s̄)≤Σ_iδ_i^u≤0。与 B 联合，双重变号得到对每个 t∈目录^m 的完整目标

\[
\boxed{\Psi(t)-\Psi(s)\ge
\sum_i[C_i(t_i,s_{-i})-C_i(s)]\ge0.}
\]

方向是**源势差上界 → 目标势差下界**；源全局最大点变为目标全局最小点。ALL 保留两源，是这条跨档证明的联合前提，不意味着 T 只能依靠这一证明。右端是固定同一起点对手的静态偏离之和，不是共同转到 t 后的联合成本差。

## 4. 实背景与合法费用均已支付

任意实 b_x≥0 的证明没有把它拆成整数背景玩家。S 对每个 p∈(0,1) 取归零单调次模函数 C_p(U)=Σ_{x∈∪U}v_x(1−p)^{b_x}。j≥1 位活动覆盖者的每人积分边际为

\[
v_x\int_0^1(1-p)^{b_x+j-1}\,dp=\frac{v_x}{b_x+j},
\]

相应势积分为 v_xH_{b_x}(j)。逐参数的次模比较仍适用，故所需实背景定量不等式完整成立。

B 的“正系数插值与有理位长”已给出共同次数 O(m²) 的精确节点费用：m=1 用常数；m≥2 令 A=b_x+m+1≥M=m+1、D+1=9mM，以截断几何级数加 Lagrange 余项修正，低次系数扰动严格小于 mM36^{m−1}(m/M)^{9mM}<1，故系数保持正。实输入得到合法实系数存在性；有理输入另有多项式构造时间和位长保证。无需约束 p_x(0) 等于调和公式。

T 正文还给独立的目标证明：同动作起点 B_0 中某资源移去 r_x 人，势损失至多 r_xp_x(m)；B_0 外加入 r_x 人，势增加至少 r_xp_x(1)。相加恰给框中右端。这一证明适用于单位权非减费用，说明该目标已闭合；跨档 ALL 边仍只声明其明列的调和补集节点费用子类。

## 5. 十三客户只否定同一完整 SPE 的直接保持

两名单位提供者，三个标签 A、B、C；不同单位客户兴趣类型 AB、C、BC、ABC 的人数依次为 4、2、3、4，b=0。末位在根 A、B、C 后选择 A、B、C 的源收益分别是 (4,7,7)、(4,11/2,11/2)、(6,15/2,9/2)。完整末位回复取 (C,B,B)，各分支均为最佳回复。首位源收益为 (6,11/2,11/2)，故根严格取 A，这是一份完整纯 SPE。

用补集费用 p_x(z)=z/2，末位相同回复仍各自最优，但首位目标成本变为 (5/2,2,2)，根 A 严格失败。本轮用分数重算这些行及 27 个固定对手单方差，后者全部仍满足成本差与收益差变号。失败来自根偏离改变真实后继，对手常数 K_i 随根分支为 (17/2,15/2,15/2)，不再抵消。

故被反驳的精确命题是“对完整历史策略逐动作取补集，会保持**同一份完整序贯 SPE**”。它没有反驳静态 PNE 迁移、上式全局势保证，也没有断言目标不存在其他 SPE。真实终局 (A,C) 本身不是所需同色静态 PNE。社会总成本、乘法近似率、一般异权及换前缀后的真实续局比较都不由本路线自动取得；本记录不把这些不同命题虚构为本路线未付义务。

## 6. 复用时的字节核对

| 已实读承重资产 | 本快照 SHA256 |
| --- | --- |
| S 正文 | `bb44ea464f60d7da0fc13551dafca11f08d9f86b69a77e17d4cac4aaeab01e57` |
| B 正文 | `e6b18c3998549abe895e26851e05645168eaee8ac0ddd2b8afecabff53ff80ed` |
| T 正文 | `278f3b3307126edc820681ccfefbc917d657893119e0bef28c148dc3c3f50f13` |
| 修订后单源 deficit 边 | `0a86ccca43f52a3a83e6d58b8dc337762d3585cf2eafb57ef0f99e86c2dc6f04` |
| 两源 ALL 完整迁移边 | `93a39650c48eae6516dcbece24f408c77318f26dc1276712903f2aa64fb68c82` |

最短复用顺序：读 T 的目标与假设 → 读现役 ALL 边的完整联合前提 → 回 S 的“从单方收益到全部活动配置”“任意外生负载的覆盖专门化”和 B 的“静态偏离与势的精确对应”。需重建多项式实例再读 B 的插值节；需涉及真实序贯策略先读 B 的“序贯边界”和 `archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md` 的全部有序历史量词。
