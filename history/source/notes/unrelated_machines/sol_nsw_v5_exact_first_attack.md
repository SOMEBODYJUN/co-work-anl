# v5 Exact-first 独立数学攻击记录（冻结前记录）

日期：2026-10-18。任务：仅据指定 statement-only Exact，从零重构分数 benchmark 匹配、显式 XOS 后端及 C–E 后果；独立记录先于作者 Proof 阅读冻结。

## 0. 阅读边界、实核哈希及裁定范围

**本轮裁定：在此文件记录的假设和有限显式输入范围内，A、B1–B6、C–E 的承重数学链可以独立重构；未找到站得住的 fatal。** 这是数学与位复杂度接口的独立 PASS，不是后端软件实现/测试证明，不是一般 subadditive 后端 PASS，不是 weighted NSW 结论，也不是全 UM 主命题、外部硬度、普适近二障碍或新颖性认证。

实际读取与哈希：

1. 首次实质文件读取且先完整阅读的是 `/workspace/scratch/038d9dcc4cac/fractional_rematching_extension_statement_only_v5.md`，31,269 bytes，实际 SHA256：`3160d7f7dc3265c7753ba558bb6cd21fe58fc5e2ea84562d2558ee852701154e`，与任务指定值一致。工具完整显示全文，未截断。
2. 唯一另读的数学材料是指定 primary DLRV v1 的本地 text：`/workspace/scratch/038d9dcc4cac/dlrv_2023_subadditive_nash_social_welfare_v1.txt`，88,992 bytes，1,414 行，实际 SHA256：`10fb320d3a7aaccb3baf579b657b3bcfecd931c45133df3f14337ce1e94829fb`，与任务指定值一致。完整文件字节为计算哈希而载入；全文仅扫描了指定关键词以定位段落。实际逐行显示并阅读的范围为 **229–768、1212–1346**。一次大范围输出有中间截断，随后以未截断的小范围完整补读了上述并集。前一区间包括 §2.1–§2.5；后一区间包括 Appendix B，以及为消除第一次输出范围歧义而读到的 Appendix C 开头。没有依赖其 generic-subadditive 数值尾界；本记录另行证明 B15。
3. 没有读取 PDF 本体，故不把任务给定 PDF 哈希称为本轮实核结果。
4. 没有读取任何其他 agent 的新推导、作者 proof、review、coauthor_validation、v1–v4 过程文件或新 canonical；没有仓库/Git/Work/推送/外部通信操作，没有接触 token。下文也不以这些被排除材料为隐含引理。

DLRV 的实际作用只限于核对 inherited 模板和 source rematching 条件：初始匹配必须在**所有原始物品**上真最大化正 singleton product，比较匹配只需是到 H 的任意双射，残余单点尺度 ν 来自 B。其发布的 actual-integral-OPT theorem 没有被当作 fractional log-CONFIG 结论调用。下面给出本次自己的推导，尤其补全零值、循环分解、全部 fractional 量词和位复杂度。

## 1. A：从任意正分数 benchmark 到 H 上匹配

写 `f_ih=V_i+v_i({h})`。先构造一个带有原配置标签的分数双射。

对每个正概率 `(i,S)`：若 `S∩H` 非空，选其中 singleton value 最大的 `h(i,S)`，把其 y 质量送至边 `(i,h)`。每行当前质量至多 1，每列至多 1，因为 h 是原配置中的真实物品而非新坐标。行缺口正好是该行 `S∩H=∅` 的总质量。若 i 不在 A，则 `v_i(B)=0`，正价值配置不可能完全落在 B，所以这些缺口行都在 A。将行缺口和列缺口用完全二分图上的非负运输填满，即得 doubly stochastic q。也可以把每个 H-empty 配置的质量进一步拆分以保留 `(S,h)` 耦合。

q 的正边都有正 f：A 内有 V_i>0；A 外的代表 h 必有正 singleton value，否则 subadditivity 与 `v_i(B)=0` 将给出 `v_i(S)=0`。故填补不会引入零分母。

对每个耦合项，令 `T=S∩B`，`k=|S∩H|`。若 i∈A，monotonicity 与 subadditivity 给出

\[
\frac{v_i(S)}{f_{ih}}
\le \frac{v_i(T)}{V_i}+k.
\]

当 k>0 时，h 取最大 singleton，故 `v_i(S∩H)≤k v_i({h})`；当 k=0 时只用 `f≥V`。若 i∉A，则 k>0，且同理 ratio 至多 k。

把 y 投影到 B，并只保留 A 的行，得到 A2 意义下的一个**分数配置族**：行和仍是 1，原始物品列仍至多 1。故所有耦合项的 residual ratio 总和至多 cn，而 H-cardinality 总和至多 n。对总质量 n 的这些正 ratio 应用 Jensen：

\[
\sum_{i,S,h}\widetilde y_{i,S,h}
 \ln\frac{v_i(S)}{f_{ih}}
\le n\ln\left(\frac{cn+n}{n}\right)=n\ln(c+1).
\]

因此

\[
\sum_{i,S}y_{i,S}\ln v_i(S)
\le \sum_{i,h}q_{ih}\ln f_{ih}+n\ln(c+1).
\]

q 的 positive-edge graph 满足 Hall：任意行集 I 的质量 |I| 只能流向 N(I)，其列容量和为 |N(I)|。所以有正边 perfect matching。减去该 matching 上最小正 q 值并递归，或直接用 assignment-polytope integrality，可把 q 分解成有限 permutation mixture。因此至少一个 permutation 的 log product 不小于 `∑q ln f`，给出 A4，且其全部 factors 为正。

此推导不需要 H 来自最优 singleton matching；H 只需有 n 个不同的真实物品。A2 的**全部 feasible fractional families** 量词是必要的，不能偷偷替换成 integral-allocation 上界。A empty、B empty、重复配置条目均不影响运输、Jensen 或 Hall。A empty 时事实上还可得到比 c+1 更强的界，但无需使用。

算法只须最大化 H 上的有理数正 factors product；它不需要 y、A2 的验证或 benchmark 的实数值作为比较过程输入。第 8 节给出 true maximum-product 的有限位长实现，因此 A3 的 exact/approximate 算法声明均得到支持。

## 2. B1：无正 singleton matching 的总分支

显式非负 XOS 的任意正值集合必包含某个正 singleton。若正 singleton 图没有覆盖全部 agents 的 matching，Hall 给出 agent 集 I，满足 `|N(I)|<|I|`。

若存在正 actual allocation，则每个 i∈I 的正 bundle 可取一个正 singleton，且 actual bundles disjoint，立即产生覆盖 I 的匹配，矛盾。

若存在 A1 的 finite positive fractional benchmark，则 I 的每行正支持配置都至少包含 N(I) 中一个物品，所以 N(I) 中的总预期物品使用量至少 |I|；容量又使其至多 |N(I)|，矛盾。故此分支 optimal NSW=0，且不存在所声称排除的 positive fractional benchmark。m=0、n>m、全零或某 agent 全零均包含在此论证中。

正分支的 τ 必须在全部原始 U 上取得 true maximum positive singleton product。这一精确条件将在 rematching 中使用；只在 H 上最优并不足够。

## 3. B2：lift、全分数量词、终止与位长

### 3.1 归一化及 lift 覆盖所有分数配置

`W_i=v_i(B)>0` 可由显式 clauses 最大化有理数和计算。每个 residual clause total≤W_i，至少一个恰等 W_i；所以除以 W_i 后 clause total≤1 且有一个=1。对 binary rationals 作有限次和、比较和一次除法只增加多项式位长，没有按 `1/W_i` 数值展开。

给任意 feasible fractional residual configuration family，给每个正条目选择一个 attaining original indexed clause s。令 λ_(i,s) 是送往 s 的配置质量，z_(i,s,j) 是其中包含 j 的质量。则 B2 的全部约束成立，其 utility 恰等该 fractional family's actual normalized expectation。**这一步证明任意 fractional family 的 utility vector 在 R 中；不是仅证明 integral allocations 在 R 中。**

反方向，对 B2 的任意 lift，条件于 λ_(i,s)>0，把 marginals z/λ 按阈值排序。用至多 |B|+1 个 nested subsets 可精确实现这些 marginals，外加 λ 混合。其 assigned-clause expectation 等于 lift utility，而 actual XOS expectation 至少等于 assigned-clause expectation。这里不要求 assigned clause 对恢复后的每个 subset 都 attaining；B6 再评价 actual valuation 正是为此。

每个 R coordinate 在 [0,1]。选择一个 total-one clause，令其 λ=1、该 clause 的所有 item marginals=1/a，可得 b_i=1/a 的 feasible lift，各物品总 marginal 正好 1。

### 3.2 显式终止界

令 `F(x)=∑_i ln x_i`，仅作分析，算法不计算它。R′ 中每个 coordinate≥ell=1/(4a)，且≤1。x=b∈R′。每次 LP 输出 w∈R，故 y=b/4+3w/4∈R′；convex update 保持 R′。

若 M>2a，写 D=y−x，则

\[
\nabla F(x)\cdot D
=\tfrac14\sum_i b_i/x_i+\tfrac34 M-a>a/2.
\]

整条更新线段 coordinate≥ell，`∑D_i²≤a`，故 Taylor 下界为

\[
F(x+hD)-F(x)
\ge h\nabla F(x)\cdot D-
 \frac{h^2}{2\ell^2}\sum_iD_i^2
>\frac{\ell^2a}{8}=\frac1{128a},
\]

这里 h=ell²/2=1/(32a²)。起点 F(b)=−a ln a，而全过程 F≤0。因此更新数小于 `128a² ln a<128a³`（a≥2）。a=1 时起点 x=1，而 M≤1，立即停止。给定的 `128a³` 上限是安全的。

### 3.3 不发生 objective-dependent 位长递归

LP 的 feasible lift polytope 始终同一个有界 λ/z 多面体；约束 coefficients 为 0、±1，RHS 为 0、1。设其显式维数为 D，任何 basic vertex 的分子分母位数有 `O(D log D)` 类型的 determinant/Hadamard 上界，**不含当前 objective 1/x 的位长**。有理 LP 可确定性地取一个 basic optimal vertex；在最优 face 内用确定性 tie-breaking 取 vertex 也满足此固定 polytope 的 vertex bound。

可以把每次 lift 保存在共同分母形式，或保存 polynomially many basic vertices 的 convex combination。每次乘 h、1−h、1/4、3/4 并加入一个有上述固定 vertex bound 的新点，只向共同分母位数添加 polynomially many bits。T 次迭代后，分母可界为固定小 rational factors 的 T 次积乘 T 个 basic-vertex denominators，其 binary length 是 T 的多项式，而非反复调用一个依赖 objective 位长的宽泛 LP-output 上界。normalized utility map 的 coefficients 有固定多项式位长，也可先取其共同分母。因此 x、1/x、每轮 LP 以及最终 lift 的位长和运行时间均为 total-bit polynomial。

### 3.4 终点保证是 B7 的全部 fractional 量词

终点 M≤2a。恢复 threshold configurations 后的 actual normalized targets 满足 `Vhat_i≥x_i≥1/(4a)`，又因为所有 subsets⊆B，`Vhat_i≤1`。它们确有行和 1、物品列≤1、polynomial support 和 rational bit length。

给任意 feasible fractional residual family z，3.1 将其 actual normalized utility vector u^z 映入 R。于是

\[
\sum_{i,T}z_{i,T}\frac{v_i(T)}{V_i}
=\sum_i\frac{u_i^z}{\widehat V_i}
\le\sum_i\frac{u_i^z}{x_i}\le M\le2a.
\]

这给出 B7，而非只对 recovered family 或 integral allocations 的界。A empty 时所有 residual values 为零，V=0 直接分支即可；B empty 不可能留下 positive residual agents。

## 4. B3：独立抽样的 1/2 福利界及实际支持

设当前 agent 数为 q，期望 actual values U_i>0。对每一原 support configuration 预先固定 attaining clause。令 b_ij 为随机 bid。对物品 j 与任意 positive threshold t，写 `p_i(t)=Pr(b_ij≥t)`。由于 positive bid 必要求该配置包含 j，feasibility 给出 `s(t)=∑_i p_i(t)≤1`。

各 agents 独立，所以

\[
\Pr(\max_i b_{ij}\ge t)
=1-\prod_i(1-p_i(t))
\ge s(t)-s(t)^2/2\ge s(t)/2.
\]

对有限 bid levels 积分/求和，得到 `E max_i b_ij≥(1/2)∑_i E b_ij`。再对 j 求和：attaining clause 在每个 T 上的总 bid 是 v_i(T)/U_i，因此总期望 bid 为 q，proxy expectation≥q/2。

逐 agent 固定 support configuration，枚举正概率候选并选择条件期望最大的一个。当前条件期望是这些候选条件期望的概率加权平均，所以总 proxy 不下降。每个 item's maximum 的条件分布可由剩余 agents 的 ordered bid CDF products 精确计算；不同物品的 bids 相关不妨碍对 proxy 求和。所有运算只含 polynomially many rational sums/products，不枚举全部联合抽样结果。

固定完以后只把物品给 positive maximum-bid claimant。对每个 agent，其所获 bundle 都属于其选定 support configuration；该 chosen clause 在 bundle 上的 additive value 至少承载其 proxy 贡献，而 actual XOS value 更大。因此 `∑v_i(A_i)/U_i≥q/2`。零 bids 物品不分配不会破坏 support 声明。这正是 B8 的 deterministic、actual、support-respecting 保证。

## 5. B4：分裂、质量归一化及先固定候选

对 i∈A′′，ν_i>0，因为非负 XOS 在 B 上正值必有正 singleton。又 V_i≥6ν_i，故 `alpha_i=V_i/3−ν_i≥V_i/6>0`。

高值配置 T 的 attaining-clause weights 各≤ν_i，总和等于 v_i(T)。令 k=floor(3v_i(T)/V_i)。已有 `v_i(T)≥kV_i/3`。每次累加剩余 weights，直到至少 alpha_i；最后一项最多 ν_i，故拿出的 weight≤V_i/3。如此取 k−1 份后，剩余 weight≥V_i/3。由原 clause，所有份的 actual values≥alpha_i。

当某份 actual value>V_i 时删物品。subadditivity 给出单次 actual value 损失≤ν_i；第一次跌至≤V_i 时仍>V_i−ν_i≥alpha_i。所以最终每份满足 B9，并仍是原 T 的子集，且同一原配置内各份 disjoint。

规模无数值爆炸：`v_i(T)≤|T|ν_i`，故 `k≤3|T|ν_i/V_i≤|T|/2`。因此每个 support configuration 只生成 polynomially many parts，而不是按 1/V 或 tiny coefficient 展开。

行归一化也不会放大 item marginals。原先被丢弃的低值配置贡献至多 V_i/3，所以高值部分的 expected value≥2V_i/3。对 `r=3v_i(T)/V_i≥1` 有 floor(r)≥r/2，故该 agent 的 total inherited mass

\[
M_i=\sum_{T\text{ high}}k_Tx_{i,T}
\ge \frac3{2V_i}\sum_{T\text{ high}}x_{i,T}v_i(T)\ge1.
\]

每个原 item 从同一原配置最多继承一次，之后除以 M_i≥1。因此 modified family 是 feasible，且 `V_i/6≤V′_i≤V_i`。

当前 q 个 agents 的 B3 输出 normalized values `b_i=v_i(S_i)/V′_i` 在 [0,6] 内，总和≥q/2≥q/d。令 satisfied 为 b_i≥δ，其中 d=5/2、δ=1/(7d)=2/35。若 satisfied 少于 δq，则总和<7δq=q/d，矛盾。所以每轮至少 ceil(δq) 个离开，特别是至少一个，L≤a_0。

关键独立性：这整个选择过程中没有 item labels；某 agent 的 S_i、attaining clause、t_i 都在 mask 前固定。每轮 S_i 之间 disjoint。不同轮可能重用 item，但正式 mask 给每个原 item 唯一一个全局 label，因此跨轮最终 T_i 不能冲突；同轮也因 S_i disjoint 不能冲突。不是给每个 agent/item incidence 单独抽一个标签。

若把 agents 按离开先后编号 k=1,…,a_0，则其所在轮 t 之前仍至少有 `a_0−k+1` 个 agents，而 current count≤`a_0(1−δ)^(t−1)`。所以

\[
p_{t_i}=\delta(1-\delta)^{t_i-1}
\ge\delta\frac{a_0-k+1}{a_0}.
\]

B10 的 0 label 接收截断尾概率，故 finite distribution 总和正好 1；0,…,L 每个 label 都有正概率。其 rational bit size 是 O(L) 级（固定 δ），没有按 tiny probability 的倒数展开。

## 6. B5：局部 relative floor、逆矩及确定性 DP

### 6.1 floor 的正确损失单位

候选的 attaining clause 给出原始 w≥0，`∑w=v_i(S_i)≥δV_i/6`，每项≤ν_i。除以同一 agent 的 V_i 后才 floor：Q=210m_B，每项损失<1/Q，总损失<`m_B/Q=1/210=δ/12`。于是

\[
\sum_j a_{ij}\ge\delta/6-\delta/12=\delta/12,
\quad \sum_j a_{ij}\le1,
\quad a_{ij}\le\beta_i=\nu_i/V_i.
\]

这里 β_i∈(0,1/6]，可以任意 tiny；它作为 binary rational 存储。原始 table、job coefficients、states 均未被 floor。对实际 mask 后 bundle，原 attaining clause 仍给出 `v_i(T_i)≥∑_{j∈T_i}w_ij≥V_i A_i(r)`。

### 6.2 不引用作者工具证明的 B15 重构

设 β>0，Y=∑(a_j/β)X_j，μ=M/β>0。对 0≤t≤1、0≤a_j/β≤1，由 concavity 的 tangent bound，

\[
t^{a_j/\beta}\le1-(a_j/\beta)(1-t).
\]

独立性给出

\[
\mathbb E[t^Y]
=\prod_j(1-p_j+p_jt^{a_j/\beta})
\le e^{-\mu(1-t)}.
\]

因此

\[
\mathbb E\frac1{\beta+\sum a_jX_j}
=\frac1\beta\int_0^1\mathbb E[t^Y]dt
\le\frac{1-e^{-\mu}}{M}<\frac1M.
\]

对 log 使用 Jensen，即得 `E ln(1/(β+∑aX))≤ln(1/M)`，甚至有严格富余。此论证只用 independent Bernoulli 和 additive weights≤β；没有 generic-subadditive concentration，也不把跨 agent 的 masks 当成独立。每个固定 agent 所需的是其候选内不同原 items 的 labels 独立，这由 B10 满足。

### 6.3 finite-grid DP 可以独立实现 B16

所有 Q a_ij 都是非负整数，且总和≤Q。对每个 agent，在任意固定前缀 labels 后，已固定贡献为一个整数 offset；未固定 candidates 中每个 item 独立地以 p_(t_i) 加上 Q a_ij，否则加零。常规长度 Q+1 的 convolution DP 精确给出 `Pr(QA_i=k)`。每个 rational probability 的分母 bit size 仅随 polynomially many input probabilities 的 bit sizes 相加；不按其数值倒数展开。不同 agents 的 distributions 不必联合存储，因为 potential 是一项一项求和。

一个具体 error budget：每步对每个 candidate label 的 total conditional potential 计算至 absolute error≤`ξ=1/(2m_B)`。每个 agent 的每个 log 值只须误差≤`ξ/a_0`，因为该 agent 的 DP probabilities 和为 1。选择近似值最小的 label，使真实 conditional potential 至多上升 2ξ；m_B 步后的总上升≤1。当前 potential 是各 candidate-label conditionals 的正概率平均，故 min≤当前值。这给出 B16，无须把近似比较视为 exact transcendental comparison。

log argument 是正 rational `β_i+k/Q`，可能在 k=0 时 tiny，但其 binary length 是 polynomial。将正 rational 缩放到 [1,2)，用 `ln z=2∑_{r≥0}t^(2r+1)/(2r+1)`、`t=(z−1)/(z+1)∈[0,1/3]`，加上整数倍 ln 2，可用 polynomially many rational terms 与显式 geometric tail bound 得到上述精度。tiny β 只增加所需 binary precision。复杂度对 Q=210m_B、L≤n 以及所有实际 rational representations 均为 polynomial。

### 6.4 B18 数字重算

令 a=a_0>0。由 B15、局部 weight 总量≥δ/12，以及第 5 节的 rank bound，

\[
\mathbb E\Phi
\le\sum_{k=1}^a\ln\frac{12a}{\delta^2(a-k+1)}
=a\ln\frac{12}{\delta^2}+a\ln a-\ln(a!)
\le a\left(\ln\frac{12}{\delta^2}+1\right).
\]

最后一步用 `ln(a!)≥a ln a−a`。DP 的总 error≤1 后，

\[
\left(\prod_i\frac1{\beta_i+A_i(r)}\right)^{1/a}
\le\frac{12}{\delta^2}e^{1+1/a}
\le\frac{12e^2}{\delta^2}
<\frac{200}{\delta^2}
=9800d^2<10000d^2.
\]

再用 `ν_i+v_i(T_i)≥V_i(β_i+A_i)` 得 B18。严格符号来自明确的 `12e²<200` 和 `9800<10000`，不是来自一次 random success，也不是把 numerical precision 留白。A′′ empty 时不调用 DP、所有 T_i empty。

## 7. B6：任意 π 的 rematching，含路径/循环及零值

这里独立重构 source lemma 的适用版本。记 singleton value `a_ih=v_i({h})`，τ 是 U 上 true maximum positive-product matching，π 是 H 上任意双射，ν_i=max_(j∈B)a_ij，W_i≥0。

要证存在 ρ 到 H，使

\[
\prod_i\max\{W_i,a_{i\rho(i)}\}
\ge\prod_i\max\{W_i,a_{i\pi(i)},\nu_i\}.
\]

若右侧 product=0，τ 本身给出正左侧，声明立即成立。以下令右侧各 factor 都正。定义

\[
E=\{i:W_i<\max(a_{i\pi(i)},\nu_i)\},\qquad
N=\{i\in E:\nu_i>a_{i\pi(i)}\}.
\]

在 E 上画 successor `i→τ^{-1}(π(i))`，只保留 successor 仍在 E 的边。每个 vertex 的 indegree/outdegree≤1，所以组件是 paths/cycles。令 Eτ 为其 forward path 可到达 N 的 vertices（包括 N）；余下为 Eπ。给 Eτ 用 τ，给 Eπ 用 π，其他 agents 任意补齐 H。

此 partial assignment 无冲突：若 i∈Eπ 的 π-item 等于 k∈Eτ 的 τ-item，则 i→k，i 也能到 N，矛盾。其余未赋值 agents 与未使用 H items 数量相等，可任意完成。

为了证明 product bound，在 Eτ 的图中删掉每个 N vertex 的 outgoing edge。即使原组件是含多个 N 的 cycle，此操作也将它切成互不相交、每条恰终止于一个 N vertex s 的 paths。这是避免不正确的“循环天然是唯一终点路径”推断的关键。

对一条 path P，前驱的 π-item 是后继的 τ-item。尝试把 P 内除终点 s 外的 agents 改用 π，把 s 改用一个 attaining ν_s 的 residual item j∈B；其他 agents 保持 τ。所有使用 items 不同，因此是 U 上另一完整 matching。ν_s>0，非 N 的 path vertices 有 positive π value。τ 的 true maximum-product 性给出

\[
\prod_{i\in P}a_{i\tau(i)}
\ge\nu_s\prod_{i\in P\setminus\{s\}}a_{i\pi(i)}.
\]

对 disjoint paths 相乘，即得 Eτ 所需的 ν/π targets。不同终点可能由同一个 residual item attaining ν；这**不构成冲突**，因为每条 path 只用于分别构造一个反事实 alternative matching，之后乘上已独立成立的数值不等式，而不是同时给全部终点分配那个 item。Eπ 的 target 为 π value；E 外 target 为 W。这证明所需 rematching inequality。

将 W_i=v_i(T_i) 代入。最终 actual matching σ 的每个 factor≥`max(v_i(T_i),a_iσ)`，且最大化 actual product，因此至少达到上述 ρ 给出的 product。σ 的 positive perfect matching 一定存在，因为 τ 每条 singleton 已正，monotonicity 使 `v_i(T_i∪{τ(i)})>0`。

现独立核算 B19。固定任意 π；若 `∏(V_i+a_iπ)=0` 则比较保证 vacuous，输出仍正。否则所有以下 ratio 分母都正。写 `b_i=v_i(T_i)`，`D_i=b_i+ν_i+a_iπ`。

对 i∈A′′，b_i≤V_i 且 ν_i≤V_i/6，所以 `b_i+ν_i≤2V_i`，并有

\[
\frac{V_i+a_i\pi}{D_i}
\le\frac{2V_i}{b_i+\nu_i}.
\]

对 i∉A′′，b_i=0；若 i∈A 则 V_i<6ν_i，ratio≤6；若 i∉A 则 V_i=ν_i=0，正比较强制 a_iπ>0，ratio=1。因此 B18 给出

\[
\prod_i\frac{V_i+a_i\pi}{D_i}
\le(20000d^2)^{|A''|}6^{n-|A''|}
\le(20000d^2)^n.
\]

另一方面 rematching 后 actual product≥`∏max(b_i,a_iπ,ν_i)≥3^{-n}∏D_i`。综合得到 B19 中的 `1/(60000d²)`。若 A′′ empty，上一式仍由 outside-factor≤6 推出，不需引用空乘积的 1/|A′′| 次方。

由 B7，A2 可用 c=2（2a≤2n）。A4 再损失 c+1=3。因此

\[
60000\cdot3\cdot(5/2)^2=1,125,000,
\]

即 B20 的第一界；第二界 2,250,000 是显式放宽，不是遗漏精度或随机成功事件。

## 8. exact positive product matching 的位复杂度

这个论证同时覆盖 A 的 matching、B1 的 τ、B6 的 σ。先删去 zero edges，做普通 bipartite feasibility；正分支有 perfect matching。设所有正 rational factors 的整数分子分母均≤2^L。n 条 factor 的任意 matching product P=A/B 可令 A,B≤2^(nL)。不同 product P>Q=C/D 满足

\[
\ln P-\ln Q
=\ln\frac{AD}{BC}
\ge\ln(1+2^{-2nL})\ge2^{-2nL-1}=:G.
\]

把每个 edge log 计算为 rational，absolute error≤G/(4n)。每个 matching sum error≤G/4，所以任意不同 products 的 order 严格保留。用这些有理权运行 exact max-weight matching，必得 true maximum product；相等 products 的任意 tie 都可。所需 log precision 只有 O(nL+log n) binary bits。第 6.3 节的 rational-series 算法足以提供带显式误差的 logs，故不用 exact symbolic/transcendental comparison。

L 是 actual rational factors 的 bit size；这些 factors 是有限显式 table 的 sums/max 和 polynomial-bit intermediate rationals，因此整体 polynomial。n² singleton evaluation、最终 table evaluation 及 rectangular τ matching 也都在显式规模的 polynomial 内。A5 是 exact 版本的直接弱化；无须依赖未知 benchmark 的实数近似。

## 9. C：unit-FSLP、NSW 常数、严格计数和量词

对任意原 state s，正 support P_(g,s) 上该 clause 的 value=1，所有 clauses 在任意 subset 上≤1，所以 actual XOS value 也恰为 1。取 feasible λ 的这些 supports 为 configurations，合并相同 subsets，即得 positive benchmark，B_v(y)=1；列约束恰是 C1 的 positive-support indicators。

所有 original utilities≤1，所以所有 finite positive log-CONFIG terms≤0；上述 witness 值为 0，故 optimum=0。对 item-equality 版本，可逐 item 把未满 column 的缺口加到尚未包含该 item 的配置质量上。若当前 column use 为 c≤1，所有 rows 中尚未包含该 item 的总质量为 n−c≥1−c，足够填满。必要时拆分有限条目；monotonicity 与 utility≤1 使 value 仍为 1。逐项填满不改变已处理 item 的 memberships。因而 equality 版本也有 0-value witness；并未提供一般 exponential log-CONFIG 的求解方法。

显式 XOS 的 value/attaining clause 直接枚举 clauses。对 rational prices r_j，demand 也可按每个 clause 计算 `∑max(p_sj−r_j,0)`，然后取最大 clause 和正收益 items；`max_T max_s` 可交换。全程原始 coefficients 未变；最后原 state 应以 unfloored table 重新 attaining。

由 B20，C 可实际使用 ≥1/1,125,000（或保留 reserve 的 ≥1/2,250,000），因此声明的

\[
\mathrm{NSW}\ge1/3,000,000>2^{-24}=1/\rho
\]

安全。FSLP feasible 时其正 fractional witness 也保证 B1 不会走无匹配分支。

令 K=ceil(1/eta)，q=rho^(−K)。若 k 个 output utilities<q 且 k≥eta n，其余 utilities≤1，则

\[
\prod_g v_g(T_g)<q^k=\rho^{-Kk}\le\rho^{-n},
\]

与 NSW>1/rho 矛盾。因此 k<eta n。`v≤c_eta=q/2` 严格蕴含 v<q，故第二计数也严格小于 eta n；不把 equality boundary 模糊带过。n 与 eta n 无需为同一整除尺度，这一实数比较同样成立。固定 eta 时 K、q、c 都是固定 rational constants；eta 可变时 threshold 的 denominator 有 O(K) bits，poly(K,input) 正是声明范围，而不是 poly(log(1/eta))。

C6 的矛盾使用同一 n menu groups：若每个 actual allocation 至少 γn 个 values≤δ≤c_eta，而 γ>eta，则 C 的输出直接违背它。它没有给全部 groups 的 constant minimum quality，也不能转换成 machine/job 数上的比例。

F1 也成立：对 C 输出，若至少 γn 项≤δ∈(0,1)，其余≤1，则 `(1/n)∑ln v≤γ lnδ`；与 NSW≥1/rho 比较得 `γ ln(1/δ)≤lnrho`。这仅禁止给定的小阈值区间，不禁止所有固定 positive γ、δ，更不推出 core fraction 随 source input size 趋零。

## 10. D：同组 shared singleton REPAIR 与 LP promise decider

D1：保留原 allocation 中 quality-one 的 groups，剩余至多 D 个（D≥n 时全部至多 n≤D）。给这些剩余 groups 各选不同 repair resource 及其 singleton alternative，即全体 unit allocation。D=0 即原 unit allocation。

D2：任取 augmented allocation，把所有 repair items 去掉并只在原 U 上评价，得到 Q 的一个 actual disjoint allocation。原 premise 使至少 γn groups 的该质量≤δ。至多 D 个 groups 收到任意 repair item；剩下至少 γn−D 个 bad groups 未收 repair，其 augmented XOS quality 与原 restricted quality 相同。repair resource 不会被多组复用。若把 allocation 表示为 selected states，也可以在原 restricted bundles 上取原 attaining state来应用 premise，得到同样 count。

D3 YES：D1 的 augmented actual unit allocation 中，每组选到某个 total-one state，并拿到其全部 positive support（少一个正 coefficient 就达不到 1）。这些 supports disjoint，故把对应 λ 设成 1 即为 augmented FSLP witness。

D3 NO：若 augmented FSLP feasible，C 给出少于 eta n 个 groups quality≤c_eta。但 D2 对每个 augmented allocation 要求至少

\[
\gamma n-D\ge(\gamma-a)n>\eta n
\]

个 groups quality≤δ≤c_eta，矛盾。因此 LP infeasible。这里 eta<gamma−a 的固定 slack 和同一 n 都确实使用，不能省略。δ=0 仍没有问题，因 C output 全正；δ 在允许的闭区间上均可。

显式 feasibility LP 只有 rational 0/1 incidence constraints，确定性 bit-polynomial 可判；不用算 integral NSW optimum，也不用执行 NSW finder。D≤a n 时新增 nD states 是 polynomial size；promise 外任意返回不影响 decider。由一个 NP-complete language 的 Karp reduction 推 P=NP 是此明确 fixed-constant promise gap 下的条件后果；没有据此声称 source reduction 已存在。

## 11. E：所有原始 jobs 的完整 schedule

固定每组恢复出的一个 original indexed state s_g。其 selector 在该 state 的 private root 上执行，load 为 1。对 allocated bundle，只将该 state 在所分配 original positive resources 上的 incidence jobs 放到对应 original resource machines；其他该 state jobs 留在其 root。每个 unselected state 的所有 incidence jobs 留在自己的原 root。显式 zero incidences 也保留，root processing time 0，不会漏 job。

原 state clause total 为 1。所迁到 resources 的 private weights 总和就是该 selected state 在 bundle 上的质量 r_g。因此 selected-root load 恰为 `1+(1−r_g)=2−r_g`；unselected-root load 恰为 1。资源分配全局 disjoint，每个 resource 最多承接一个 unit incidence job，load≤1。每个 selector/每个 incidence identity 恰执行一次，没有改物理 processing time、换成 slot 或删掉 unselected jobs。

故 whole-matrix makespan≤2；selected root 超过 2−q_eta 当且仅当 r_g<q_eta，数量<eta n。没有因此得到 all-machine makespan≤2−c_eta。

若 actual unit allocation 存在，选择其 attaining original state 后 selected roots 为 1，其他 roots 仍为 1，resources≤1；所有原 jobs 仍完整，所以 makespan≤1。任意 selector 的 finite processing time 都是 1，且 n≥1，因此普通 OPT≥1，从而 OPT=1。D1 的 augmented YES 同样包括所有新增 repair roots/jobs 及原来的 jobs。

S 个 indexed states 对应 S 个不同 roots，m 个 resources 对应 m 个不同 resource machines；jobs 是 n 个原 selectors 加 I 个原 incidences。augmentation 加 nD roots、D resource machines、nD positive singleton incidence jobs、nD selector endpoints，selector identities 仍为 n。若另有显式 zero incidences，照计并保留。没有把新增 states 当作新增 groups。

## 12. 最终攻击结论与冻结约束

本轮针对以下潜在断点给出了独立推导：

- A 的 fractional quantifier 与正边 Hall/Birkhoff，而非把 published integral OPT 偷换为 fractional benchmark；
- residual lift 覆盖全部 fractional configuration utility、actual recovery≥lift utility，以及固定 basic-vertex 位长；
- log-potential 的显式 progress 和 polynomial 更新次数；
- independent finite-support welfare proxy 的 1/2 下界及每个实际 bundle 的 support containment；
- splitting 后 inherited mass≥1，防止 normalization 放大列；
- 候选在 labels 前固定、同一 original item 唯一全局标签；
- local relative floor 的 δ/12 loss 与 tiny β 的纯位精度成本；
- B15 的独立 inverse-moment 证明、DP 的 total error≤1 和 B18 常数；
- 任意比较 π 的 rematching，包括含多个 ν vertices 的 cycles、重复 residual maximizers 和零 comparison edges；
- c、d、δ、NSW denominator、rho、eta/K、gamma−a slack 与 equality thresholds 的数字反算；
- empty/zero branches 和普通矩阵全部 selector/incidence jobs 的完整身份。

**裁定：上述 Exact v5 的 A 与 explicit-XOS B，以及在 original total-one normalization 下的 C–E，可以在本记录范围内 PASS。未发现 fatal。** 此 PASS 不延伸到旧 generic-SA 数值路线、weighted agents、输入未显式给出 clauses 的 oracle-only backend、其他 dummy constructions、general UM configuration LP、source hardness 或全 UM 主命题。算法存在性和 total-bit-polynomial 证明不等于已有可执行实现。

本文件写出并计算冻结哈希后，不再把后续作者 Proof 或其他 reviewer 材料融入此独立记录；若随后发生 read-after，只能另立文件并声明阅读次序。冻结哈希应由外部回报记录，避免自哈希循环。
