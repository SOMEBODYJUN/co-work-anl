# 正占用核的交互秩暴露面、锐截断预算与非闭锥补全

本稿把正负载多项式中不发生抵消的混合差分提取为独立的有限维表示工具。对象是 Boolean 输入上的向量响应表，不需要博弈、策略改善或均衡。原始机制来自 boss4 的局部成本展开；E1 新增任意交互阶数的暴露面、对任意有限次数统一的锐预算，以及无界次数锥的准确闭包。来源链见第七节。

## 一、输入、定义与三个精确接口

固定整数 n≥1、正实质量 w_1,…,w_n，N={1,…,n}。输入为 s∈{0,1}^n。对非空 S⊆N 和整数 k≥0，定义向量核

\[
 K_{S,k,i}(s)=
 \begin{cases}(\sum_{j\in S}w_js_j)^k,&i\in S,\ s_i=1,\\0,&\text{其他情形}.\end{cases}                         \tag{1}
\]

k=0 时第一分支恒为1，不使用 0^0。令 K_fin 为全部这些核的**有限非负线性组合**之锥；每个表示有自己的有限最高次数，不预设全锥共同次数界。零向量由空和给出。所有响应在本坐标未激活时为0。记 active 表 f_i(x)=C_i(1,x)，x∈{0,1}^{N\{i}}；其唯一多重线性展开的最大次数称交互秩，零表约定秩≤任意非负整数。令 V_r 为每个 active 表次数≤r 的线性空间。

对 T⊆N\{i}、R⊆N\(T∪{i})，定义真实输入混合差分

\[
 \Delta_T f_i(R)=\sum_{A\subseteq T}(-1)^{|T|-|A|}f_i(1_{R\cup A}). \tag{2}
\]

当 0≤r≤n−2，置 q=r+1，定义只在**顶端背景**取值的线性泛函

\[
 L_q(C)=\sum_{i\in N}\sum_{\substack{T\subseteq N\setminus\{i\}\\|T|=q}}
 \Delta_Tf_i(N\setminus(T\cup\{i\})).                         \tag{3}
\]

定义全激活状态质量 B(C)=Σ_i C_i(1_N)，特别

\[
 b_{S,k}=B(K_{S,k})=|S|W_S^k>0,\quad W_S=\sum_{j\in S}w_j.    \tag{4}
\]

B 是一个状态上各响应的和，**不是所有状态的总和**。以下归一化和锐常数均只用(4)。

| ID/version | Exact Statement / Quantifiers / Conclusion |
| --- | --- |
| PK-INTERACTION-RANK-FACE-v1 | 对每个上述 n,w、整数 r≥0 及每个 C∈K_fin，C∈V_r 当且仅当 C 的每个有限非负核表示中，每个正系数项都满足 min{k,|S|−1}≤r。因而等价于存在这样的表示。r≤n−2 时这个子锥恰为 K_fin∩ker L_(r+1)，是暴露面；r≥n−1 时为全锥。 |
| PK-SHARP-FORBIDDEN-MASS-v1 | 对每个 n≥2,w 和整数 0≤r≤n−2，令 q=r+1，γ 为(5)。对**任意**有限非负表示 C=Σa_(S,k)K_(S,k)，删掉所有 min{k,|S|−1}>r 的项得到 C_low∈K_fin∩V_r，有 Σ_bad a_(S,k)b_(S,k)≤L_q(C)/γ，及逐坐标 0≤C−C_low≤L_q(C)/γ。γ 是所有被删归一化单核 L_q(K)/b 的精确下确界，且达到；这里不声称最终距离界最优。 |
| PK-OCCUPANCY-CONE-CLOSURE-v1 | 对每个 n≥1,w，在完整有限维响应表空间的通常拓扑中，cl K_fin=cone({K_(S,k)}∪{U_S})，U_(S,i)(s)=1_(i∈S)∏_(j∈S)s_j。cone 仍指有限和。每个 n≥2 的 K_fin 均非闭；并且对每个 r≥0，cl K_fin∩V_r=cl(K_fin∩V_r)，r≤n−2 时也等于 cl K_fin∩ker L_(r+1)。 |

其中 e_q(w_S)=Σ_(T⊆S,|T|=q)∏_(j∈T)w_j，

\[
 \gamma=\min_{\substack{S\subseteq N\\|S|\ge q+1}}
 \frac{q!(|S|-q)e_q(w_S)}{|S|W_S^q}>0.                       \tag{5}
\]

**Objects / Domain / Assumptions / Scope：** 有限 n、固定正实质量、整数非负幂、有限非负混合、完整 Boolean 输入表和 active 交互秩；无符号抵消、无负质量、无改变输入标签的归约。闭包是有限维欧氏闭包，包含原有限表示锥之外的对象。r≥n−1 时无 forbidden 项，预算为空，(5)不定义且不调用。n=1 同属该退化情况。

**Dependencies：** 非负多项式展开、Boolean 多重线性表示、容斥、有限概率空间、有限维紧致及线性相关消元。下面全部重建；不导入外部均衡定理。三接口中秩面不依赖锐常数，锐预算依赖秩面；闭包的直接表示证明独立于预算，闭包切片再用预算。

**Status / Evidence / Objections：** 完整解析证明已写；独立重构与冻结攻击、实际 Fraction 审计范围以配套审查和冻结运行记录为准。外部同行评审及全球新颖性未认证。条件删除反例和一次实际复用见第五、六节。没有将有限计算当作实参数/任意次数证明。

## 二、正展开与秩面：为什么不能抵消

对 i∈S，将 (w_i+Σ_(j∈S\{i})w_jx_j)^k 作普通多项式展开，再用 x_j^a=x_j（a≥1）归约。每个多重线性系数非负；T⊆S\{i} 的系数恰在 |T|≤k 时严格正。确实，普通展开中该系数汇集所有恰使用 T 中变量、每个至少出现一次的单项式，wi 的余幂任意。若 |T|≤k，正权保证至少一项严格正；|T|>k 则无项。因此一个单核的 active 秩精确为 min{k,|S|−1}。

写一般 active 表为 f_i(x)=Σ_A m_i(A)∏_(j∈A)x_j。对 K_fin，m_i(A)≥0。容斥消去未含 T 的项，得到

\[
 \Delta_T f_i(R)=\sum_{A\supseteq T,\ A\setminus T\subseteq R}m_i(A)\ge0.
\]

在顶端背景，该差分正好为 Σ_(A⊇T)m_i(A)，所以

\[
 L_q(C)=\sum_i\sum_{A\subseteq N\setminus\{i\}}
             { |A|\choose q}m_i(A).                        \tag{6}
\]

它为0当且仅当所有 |A|≥q 的系数为0，即 C∈V_(q−1)。同时 L_q 在单核上严格为正当且仅当 |S|≥q+1 且 k≥q。有限正和为0迫使每个正项自身为0；由此得到“每个表示”的量词。非负泛函的零截面是面：若 C=D+E 且 D,E∈K_fin、L_q(C)=0，则 L_q(D)=L_q(E)=0。该同一泛函显式暴露此面。

r≥n−1 时每个 active 表最多有 n−1 个变量，全部结论退化为全锥，无需非零暴露泛函。

## 三、锐预算：无界次数也不能隐藏质量

固定 forbidden 单核 S,k，m=|S|≥q+1，k≥q。对 i∈S 和 T⊆S\{i}、|T|=q，在顶端背景所有 S\(T∪{i}) 都激活，因此

\[
 \frac{\Delta_T f_i(N\setminus(T\cup\{i\}))}{W_S^k}
 =\sum_{A\subseteq T}(-1)^{q-|A|}
 \left(1-\sum_{j\in T\setminus A}\frac{w_j}{W_S}\right)^k. \tag{7}
\]

令 k 次独立抽样分别以 w_j/W_S 的概率取颜色 j∈S。(7)按容斥恰为 T 中每个颜色至少出现一次的概率。随 k 增加该事件的概率不减。k=q 时它等于 q!∏_(j∈T)w_j/W_S^q，因为每种指定颜色必须恰出现一次。

若 i∉S 或 T⊈S\{i}，对应差分为0。对 i,T 求和并除 m，注意每个 q元 T⊆S 对恰 m−q 个 i 被计入，得到

\[
 \frac{L_q(K_{S,k})}{b_{S,k}}\ge
 \frac{q!(m-q)e_q(w_S)}{mW_S^q}.                            \tag{8}
\]

等号在 k=q 成立。S 的选择有限且每个候选严格正，(5)为精确最小，达到于某个 S 的 k=q 核。这证明的是**单核预算比**的锐性。

对任意表示，用 L_q 的线性性、low 项为0和(8)，得

\[
 L_q(C)\ge\gamma\sum_{bad}a_{S,k}b_{S,k}.
\]

每个核的每个坐标均位于 [0,b_(S,k)]，删除正项不会增大任何坐标，故逐坐标误差界成立。算法输入一个有限表示：逐项按 min{k,|S|−1}≤r 保留或删除；输出保持该核模型合法、秩≤r 的表示及可直接复核的预算。没有声称能从响应表多项式时间找回未知表示。

若 C∈K_fin 且任意目标 A∈V_r 满足 ||C−A||∞≤ε，则 L_q(A)=0，而(3)至多 n·binom(n−1,q) 个差分，每个用2^q个带符号值，所以

\[
 0\le L_q(C)\le n{n-1\choose q}2^q\varepsilon.               \tag{9}
\]

合并即得一个固定 n,w,r 的稳定投影界。独立审查进一步证明，(9)的常数其实正是 L_q 在 active 表坐标上的精确绝对系数和：固定 i，缺席集合大小 b≤q 的坐标系数为 (−1)^b·binom(n−1−b,q−b)，同一坐标贡献同号，求绝对值并用二项式计数即得该常数。这不等于声称组合后的最终距离界最优。它不要求 A 本身是非负核表，但要求完整表的绝对一致误差；抽样、相对误差或仅偏离比不满足本假设。

## 四、闭包的全部新增方向

令 P={K_(S,k)/b_(S,k)}。每个元素坐标非负、≤1，且 B=1。固定 S，当 k→∞，若 S 全部激活则非零用户坐标恒为1/|S|；若缺少任何 S 中元素，则正权给严格较小负载，归一化值趋于0。因此

\[
 K_{S,k}/b_{S,k}\longrightarrow U_S/|S|.                   \tag{10}
\]

S 只有有限种，任何核序列均能先固定 S，再取有界整数 k 的常数子列或 k→∞ 子列。故 cl P 正好是 P 加有限多个 U_S/|S|，是紧集。

有限维空间中紧集的凸包仍紧：任一凸组合若超过 D+1 个点，增广向量 (p,1) 线性相关；沿该关系减去最大可行倍数，保持总质量与向量并消去一项。反复得到≤D+1个点。紧集的有限次积与紧权重单纯形之连续像因此覆盖其凸包，证明紧致。

所有这些点满足 B=1。其生成锥闭：若 t_l p_l 有有限极限，p_l 属该紧凸包，则 t_l=B(t_l p_l) 有有限极限，取 p_l 收敛子列即可；t_l→0 时极限为0。由(10)及原核的包含关系，这个闭锥正是 cl K_fin，并给出接口中的有限和公式。

n≥2 时取任意两元素 S。U_S 在任一单独用户激活时为0，但在两用户都激活时正。若有有限正核表示，任何一正项 K_(T,k) 都给 T 中某坐标的单独激活状态严格正；这与 U_S 的所有单独激活状态都为0矛盾。故 U_S∉K_fin，却按(10)属于闭包，证明非闭。n=1 时锥只有单一非负射线，闭。

最后设 C_l∈K_fin 收敛到 C∈cl K_fin∩V_r，r≤n−2。L_q(C_l)→0。逐个删除 bad 项，由第三节得到 C_low,l→C，故 C∈cl(K_fin∩V_r)。反向包含由 V_r 闭性显然成立。在闭包中各 Möbius 系数仍非负，(6)继续保证 V_r 与 ker L_q 的截面相同。r≥n−1 时直接为全闭包。也可从闭包生成式看出低秩面只新增 |S|≤r+1 的 U_S 方向。

## 五、承重条件与失败回收

1. **允许负混合系数会失败。** n=2、w=(1,1)、S=N、r=0 时，K_(S,2)−3K_(S,1)+3K_(S,0)=K_(S,0)。右侧秩0，左侧有秩1的项；非负性的作用正是禁止消去。这不是对有符号模型的表示定理。
2. **允许零质量会失败。** S={1,2,3}、w=(1,0,0)、k=2，active 交互秩≤1，但 min{k,|S|−1}=2。名义支持不能代替严格正质量支持。
3. **只在零背景测差分，精确判别仍成立，稳定预算失败。** 对 n≥q+2，full-S 归一化 k次核在任一零背景 q差分中最大负载至多 w_i+Σ_(j∈T)w_j<W_N，故所有这些值趋0；但其极限 U_N/n 的 active 秩为 n−1≥q+1。原失败是测试遗漏高背景，不是计算误差。改用顶端背景正是第三节的修复。
4. **常数依赖质量。** q=2、n=3、w=(1,t,t)，(5)为 2(2t+t²)/[3(1+2t)²]，t↓0 时趋0。固定质量的锐预算不提供任意正质量统一误差常数，也不提供全类均衡倍率。
5. **低交互秩不等于全部小支持。** r=1 时所有任意大 S 的线性核都仍允许；原仿射全签名刚性恰落在这里。本稿增加的是“高次数且大支持”的联合排除，不推翻原刚性，也没有把任意完整 MODEL 成本锥误认成只用动作1的核锥。

## 六、实际复用：低阶共享负载响应的表示审计

一个非博弈实例：三个开关传感器质量 (1,2,3)。某共享元件 S 在传感器 i 激活且 i∈S 时产生响应 (Σ_(j∈S)w_js_j)^k，设备输出是这些元件的非负叠加。希望输出对每个传感器自己的激活条件下仅有对其他开关的仿射响应，即 r=1。

接口一立即给出精确模型字典：共享≥3传感器的元件只能常数/线性；两传感器元件可用任意次数；私人元件可用任意次数。此判断覆盖未知有限最高次数，不用枚举它。

取具体响应

\[
 C=K_{N,1}+\tfrac1{100}K_{N,2}+\tfrac1{1000}K_{\{1,2\},4}.
\]

唯一 forbidden 项是中间一项。q=2，γ=11/54，L_2(C)=11/50，bad 全激活质量=(1/100)·3·6²=27/25，且 L_2(C)/γ=27/25。此例达到的是单核质量预算；保留其余两项给出合法仿射 active 响应。所有输入状态、差分、删除和反算由标准库 Fraction 程序实际核验；高次两传感器项确实被保留，而不是简单“删掉全部高次数”。

回到原主题时，一个确切桥梁是：若 MODEL 表在每名玩家动作0下全成本为0，则任何正费用资源都不可能用于任何人的动作0，因为正权与非零非负多项式会给正成本。因此全部正资源定向为(1)，本稿逐状态适用；零费动作 marker 不影响它。若没有该零成本动作条件，资源可用动作0或两个动作，差分可能换号。本稿不提供该一般签名锥的均衡归约、selector 可行性或全类匹配上界。

## 七、不可变来源、提取变换与文献范围

原作者/发布者 **boss4**，源分支 **main**：

- `38cd5c7fb520e826f060f678aa6deb48d3163fe8`，`research/current/weighted_congestion/template_certificates/selector_local_moments.md`，SHA-256 `a6a89aab5a2c3ccf06a3fc89e84293ad253840c6aa105dac535185a80b3f71d7`，公屏 seq68；原 Claim `WC-DEGREE-LOCAL-COST-COMPRESSION-v1`，第2节的非负 Möbius 展开为本提取的局部机制。
- `211a7d26332aa6303c7cfde814805ab792ff4bb6`，同路径，SHA-256 `c8e1c746ccf5c1462b244faebe0c15ec0f3378f62d0e915c3c134aaa348454a5`，公屏 seq77；原 Claim `WC-AFFINE-FULL-SIGNATURE-RIGIDITY-v1`，零成本动作定向与正预算饱和提示了不能取消的承重假设。

E1 实际执行 `git show commit:path` 并按公屏 descriptor 核对这两个 hash。原两 Claim 身份保持完整；新 PK ID 不静默改动它们。提取变换依次为：去掉策略/均衡叙事→独立向量核；任意 r 的正差分检测→所有表示的联合次数/支持过滤；全激活归一化→抽样覆盖概率的锐预算；无界整数幂极限→有限个 unanimity 新方向。独立审查者先只读 exact statement 重构，后参与提出完整闭包，再攻击冻结正文；其具体贡献和 hash 在审查内记录。

2026-10-15 实际联网检索两组引擎及一手来源，查询包括 `nonnegative polynomial congestion game representation quadratic cost functions hypergraph Möbius coefficients`、`pseudo-Boolean higher-order positive derivatives`、`Möbius totally monotone belief functions nonnegative coefficients`。准确读到的范围：

- Foldes–Hammer，[*Submodularity, Supermodularity, and Higher-Order Monotonicities of Pseudo-Boolean Functions*](https://pubsonline.informs.org/doi/10.1287/moor.1040.0128)，2005，一手摘要。其研究高阶离散导数正负性和低阶多项式类；正混合差分作为一般工具不是本稿首创。未以仅读摘要声称其全文没有(5)。
- Erginbas–Kang–Polito–Ramchandran，[*Adaptive Sparse Möbius Transforms for Learning Polynomials*](https://arxiv.org/abs/2602.06246v1)，2026，一手摘要与版本页。它研究稀疏 AND 基学习及超图重建；本稿不导入其算法或复杂度定理。
- Del Pia–Khajavirad，[*The pseudo-Boolean polytope and polynomial-size extended formulations for binary polynomial optimization*](https://arxiv.org/abs/2309.08693v2)，2024修订，一手摘要及版本页，关于有符号超图和扩展表述；不能直接等同这里的正占用核锥。

**Truth：** 本稿精确接口由自足证明承担。**Value：** 可直接过滤非负共享负载字典，量化坏项质量，并避免混淆有限表示与闭包。**Novelty：** 有限检索未认证全球新颖性；通用 Möbius/高阶差分已知，特定预算与闭包在本仓首次登记，不称全球首次。**Mechanism：** 正展开、顶背景覆盖事件、紧归一化生成集。**Ambition：** 是独立工具，未改变 WC-TARGET OPEN。

## 八、可复现核验与尚缺桥梁

在仓库根运行：

```
python3 tests/audits/positive_kernels/verify_rank_faces.py
python3 tests/audits/positive_kernels/independent_rank_face.py
```

两程序均输出 JSON，不覆盖冻结记录。作者输入在 `examples/positive_kernels/rank_face_inputs.json`；冻结输出在 `evidence/runs/positive_kernels/rank_faces_author.json` 和 `rank_faces_independent.json`。独立审查位于 `research/reviews/positive_kernels/rank_face_review.md`。各记录给出实际 Python 版本、完整参数、无随机性/seed、Fraction 精度与零舍入误差、source/input SHA-256、命令和实测范围。有限网格只检验其覆盖的代数/边界，任意实质量和无界次数由以上证明承担。

仍缺的桥梁是：一般动作签名存在符号差分时如何建立可用正结构；只有抽样响应、相对误差或改变质量时如何取代(9)；是否能用秩面结构推进任意 selector 的 moment hull 与 resource polar 相交。这里未提出无证猜想，也未给出全类均衡保证。
