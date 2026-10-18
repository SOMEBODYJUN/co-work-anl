# v5 Author Proof 实际全文读后审（另立冻结记录）

日期：2026-10-18。角色：此前 Exact-first 独立攻击者的 author-read-after 审查。此刻已经公开作者策略；本记录不是新的 blind review，也不把它计作一张新的独立盲审票。

## 0. 裁定与冻结边界

**裁定：实际阅读全文后，未发现可以成立的 fatal；作者 Proof 在 Exact v5 的既定范围内自给地支撑 A、explicit-unweighted-XOS B、original-total-one C、指定 REPAIR D、完整 ordinary-matrix E 及 F 的限定量词。** 固定 LP 顶点位长、真最大乘积匹配、item-equality 填满、DP 全部误差、局部 floor 常数和完整 jobs/zeros 都已核查。作者没有把我先前的 PASS 当作证明的替代。

原先 `/workspace/scratch/038d9dcc4cac/sol_nsw_v5_exact_first_attack.md` 保持不动。此次重新读取其字节仅作 hash/mode 检查，得到原 SHA256 `a900867a462b030db5cb2556f68f992b89efce28936a5c2658b13aeb03d7d306`，权限仍为 `0444`。此前冻结时间为 `2026-10-18T13:06:38.617949+00:00`。本记录不会回写、修订或把后见材料混入该 Exact-first 文件。

本读后审不承诺后端已有实现、不认证软件执行、不覆盖一般 subadditive 或 weighted backend、不证明 source hardness、不证明全 UM 主命题，也不认证全球新颖性。

## 1. 此次实际新增阅读范围与实核身份

唯一新增读取的数学正文：

- `/workspace/scratch/038d9dcc4cac/fractional_rematching_extension_author_proof_v5.md`
- 实际 byte count：71,631。
- 实际行数：1,052。
- 实核 SHA256：`2989351ca6ab45779fecb3c4a4ccefbae2044cdcce7ad3f3fab0d0e2ce55a1af`，与 root 释放值相同。
- 四次未截断显示，逐行实际阅读全文：**1–270、271–540、541–810、811–1052（EOF）**。没有把只作 hash 而载入的未显示正文计作阅读。

此轮没有读取作者列出的独立工具 proofs 或其他 agent 的新 reviews；作者 Proof 中对其阅读的披露，仅作为作者的已披露来源信息，而非我也读过那些文件的证据。没有读 canonical，没有 Git/Work/推送/外部通信，没有接触 token。

旧 primary 的内容阅读沿用原 Exact-first 记录；本轮只重新核了指定 text 的 hash、行分隔计数，未新增显示任何 source 正文。该 text 仍为 SHA256 `10fb320d3a7aaccb3baf579b657b3bcfecd931c45133df3f14337ce1e94829fb`。其有 **1,391 个 newline 和 23 个 form-feed**，故 Python `splitlines()` 得到 1,414 行。作者在 provenance 中称 physical lines 1–1391，与这个 newline 计数一致；我旧记录里的 229–768、1212–1346 是当时工具按 Python `splitlines()` 的索引，二者不可直接对齐成“漏读了 23 行”的指控。没有 PDF 阅读或 PDF hash 实核声明。

Exact v5 身份仍使用原先全文实核的 SHA256 `3160d7f7dc3265c7753ba558bb6cd21fe58fc5e2ea84562d2558ee852701154e`。作者 Proof 的 target 披露与它一致。

## 2. 作者是否借旧 PASS 代替 Proof

作者 §0 明确披露先读 Exact、再读我的冻结攻击记录及两个工具 author proofs；所以这是一份 informed author reconstruction，而不是声称独立重做的盲审。此披露与本次 read-after 的角色匹配。

关键是检查其数学依赖而不是检查它有没有提到我的文件。实际的承重依赖如下：

| 结论 | 作者正文中的实质推导 | 是否需要先前 PASS 才成立 |
|---|---|---|
| A fractional benchmark matching | §2.1–2.3：真实 item 代表、缺口运输、全部 fractional 投影、Jensen、正边 Hall/permutation decomposition | 否 |
| B2 full fractional residual bound | §3.2–3.5：lift 双向关系、显式 progress、固定 vertices、actual recovery≥lift | 否 |
| B3 支持内 welfare rounding | §4.1–4.2：independent-agent tail bound、finite CDF 条件期望、chosen-clause actual lower bound | 否 |
| B4 split/round candidates | §5.1–5.3：weight extraction、删项损失、mass≥1、每轮离开比例、labels 前固定 | 否 |
| B15/B16/B18 | §6.2–6.5：convex chord inverse moment、完整 rational DP、显式总误差一、factorial 常数 | 否 |
| B19 任意 π rematching | §7.1–7.3：cycles 切路径、逐路径反事实匹配、零值分支、ratio 常数 | 否 |
| C–F | §8–11：unit witness、填满、product count、repair 投影、完整 schedule、量词 | 否 |

所用标准计算原语为有理 LP、bipartite matching、整数/有理运算；需另行证明的 logarithm approximation 和 product separation 已在 §1.1–1.2 明写。没有用 source 的 integral-OPT theorem 给新 fractional-log benchmark 签 constant。

## 3. logarithm 和真 maximum-product matching

§1.1 的 reduction `x=2^e y, 1≤y<2` 保证 `|e|` 受输入 bit length 控制。`z=(y−1)/(y+1)≤1/3` 的 odd-power series 及 tail bound 足以用 polynomially many rational terms 获得任意指定 absolute precision；计算 cost 依赖 precision 的 bit 数，不依赖 x 的倒数数值。ln 2 本身也用同一 series，故没有隐蔽的 exact-real oracle。

§1.2 的 gap 可直接复算：若每条正 factor 的整数 numerator/denominator≤2^L，则 n 条 matching product 的 numerator/denominator≤2^(nL)。不同 P=A/B>Q=C/D 满足 AD−BC≥1，故

\[
\ln P-\ln Q\ge\ln(1+2^{-2nL})\ge2^{-2nL-1}=G.
\]

edge log error≤G/(4n)，每个 matching sum error≤G/4，两个不同 products 的次序仍严格保留。用 rational approximate weights 做 exact maximum-weight matching，确实输出 true maximum-product matching，而不是只得到一个未计损失的近似。所需 precision 为 O(nL+log n) bits。

零 factors 先删，普通 matching 先测可行；矩形 U 端允许多于 n 个 items。A 的正 perfect matching 来自其证明；B 的 τ 在原始全部 U 上取最大，σ 因 τ 仍给 positive actual factors 而可行。对 final values 仍直接用原 table，有理 bit sizes 是输入和各 polynomial-bit intermediates 的多项式。

**核查结果：PASS。** 特别不是在 real log 权重上无条件调用“精确比较”。

## 4. 固定 LP polytope、归一化和全分数量词

作者 §3.2 归一化仅把 residual utility coefficients 除以 W_i，不改固定 λ/z feasible polytope P：其 constraints 仍是 0/±1、RHS 0/1。这个 P 的可行性矩阵与 W_i、当前 x 和之后的 floor 无关。原始状态表、原资源与后续 physical processing matrix 也没有被改写。

任意 feasible fractional family 的 actual normalized utility vector 在 R 中：给每个 configuration 选择 actual attaining clause，再按 clause 聚合其 probability 和 item marginals 即可。这确实证明了“全部 fractional”而非“全部 integral”。

反方向 threshold recovery 的 `q_0=1,q_(b+1)=0`、nested-set probabilities `q_k−q_(k+1)` 正确实现 marginals。assigned-clause expectation 等于 lift utility；actual XOS expectation 可以更大。因此 final Vhat≥x 正是所需方向，不能把二者误写为必相等。作者 §3.5 随后用

\[
\sum_{i,T}z_{i,T}v_i(T)/V_i
=\sum_i u_i^z/\widehat V_i
\le\sum_i u_i^z/x_i\le M\le2a
\]

对任意 z 证明 B7，完整付了 A2 的量词义务。

终止部分：R′ 使 x_i≥ell=1/(4a)，coordinate≤1。M>2a 时梯度内积>a/2；沿线 Hessian lower bound 与 `∑D_i²≤a` 给每次 potential progress>1/(128a)。由起点 −a ln a、上界 0，更新数<128a² ln a<128a³；a=1 起点即停。算法未计算这个 logarithmic potential。

位长部分：P vertex 可由 D_P 个 independent active equations 决定。Cramer/Hadamard 的 numerator/common determinant bound 为 O(D_P log(D_P+2)) bits，完全独立于 objective 1/x。返回 basic optimum，或在 optimal face 内逐 coordinate 优化至 lexicographic vertex，都得到原 P 的 vertex。后者的额外 LP calls 为 polynomial；face restrictions 不会把最后得到的 vertex 改成“另一个任意新多面体的巨大 vertex”。

维护 lift 的 common denominator 时，每轮只乘入一个固定-bound basic denominator 和 h、1−h、1/4、3/4、a 的 polynomial-bit factors。因此 bit length 按轮数相加；不是把 objective-dependent output bound 递归代回自己。normalized utility map 可取固定 polynomial-bit common denominator；x、1/x、LP objective bits 都随之 polynomial。

**核查结果：PASS。** 没有 inverse-scale 数值展开、未知 utility floor 或 objective 位长递归漏洞。

## 5. welfare、support split 与候选独立性

§4 的独立性在 agent configuration draws 之间。单个 item 的 threshold exceedance probabilities 总和≤1，故 union probability≥s−s²/2≥s/2。对有限 bid levels 求和得 expected proxy≥q/2。不同 items 的相关性不影响这一求和。

作者给出 strict CDF `Pr(b<t_l)` 的有限层公式，ties/zeros 得到正确处理。依次选 exact conditional expectation 最大的 positive-probability configuration，使 proxy 不下降。每个 positive winning bid 来自该 agent 的已固定 support configuration，item 给其 claimant 后 actual XOS≥该 chosen clause 的 additive contribution。因此 bundle 为原支持集子集，而不仅是无支撑的福利数值。

§5 对 A′′ 的 ν>0、alpha=V/3−ν≥V/6 均有理由。attaining-clause weights≤ν，greedy 抽 k−1 个 weight 处于 [alpha,V/3] 的 parts，余下 part weight≥V/3；删项直到 actual≤V 的最后一次 value loss≤ν，保住下界。

规模界 `k≤3v(T)/V≤|T|/2` 排除了按 reciprocal target 分裂。高值 expected contribution≥2V/3，加上 floor(r)≥r/2，给 inherited mass M_i≥1；按行除以它只减小 item marginals。作者没有把“质量归一化总会保持 item capacities”当作无证明事实。

当前 normalized actual utilities≤6，sum≥q/d；δ_mask=1/(7d) 迫使每轮至少 ceil(δ_mask q) 个 satisfied。S_i、t_i、attaining clauses 全部先固定，再考察 labels，没有让候选自适应地窥视 future mask。

同轮 S_i disjoint；跨轮 item 只有同一个 global label。因此若 item 同时进两 T_i，两个 round labels 必相等，回到同轮 disjoint 矛盾。zero auxiliary weight 的 items 即使被保留，也受相同论证保护。

**核查结果：PASS。** 这些是 actual bundles、原 item 的全局 disjointness，不是按配置坐标或按 agent incidence 独立复制物品。

## 6. 局部 relative grid、逆矩和 DP 精度

为清楚区分符号，本审把 B 的固定标签参数写为 `δ_mask=2/35`；后文 robust-small-quality 中可变阈值另写 `δ_quality`。它们没有被设成同一参数。

候选 clause weight 的 relative total≥δ_mask/6，floor 总损失<|S_i|/Q≤1/210=δ_mask/12，故 auxiliary total≥δ_mask/12，且总量≤1、每项≤β_i。Q=210|B| 只控制固定候选的内部 DP，不是用 floor 替换原 valuation、state 或 physical time。

§6.2 的 inequality 方向正确：固定 0<t<1 时，d↦t^d convex，其端点 chord 给 `t^d≤1−d+dt`。独立 Bernoulli 后

\[
\mathbb E[t^Y]\le e^{-\mu(1-t)},\qquad
\mathbb E\frac1{\beta+\sum a_jX_j}
\le\frac{1-e^{-\mu}}M<\frac1M.
\]

再对 positive inverse variable 用 log Jensen 得 B15。这里仅逐 row 要求不同原 items 的 labels 独立；不同 agents 因共享 item 而相关并不被错误排除。

§6.3 的 DP 没有未明的精度债：

- 每 row 在 indices 0,…,Q 维护 rational distribution；fixed prefix 是 offset。
- 每个 Bernoulli 的 numerator update 和 common denominator multiplication 明写在 (6.11)。非负 numerators 的和等于 denominator，故 bit length≤输入 probability denominators 长度之和。
- table 中每个 log absolute error≤alpha=1/(2a_0 m_B)。row expectation error≤alpha，sum score error≤a_0 alpha。
- 选择近似最小 label 的真实 conditional potential 至多超过真实最小 child `2a_0 alpha=1/m_B`；parent 是 child 的正概率平均。
- m_B 步总上升≤1；无需除以 tiny prefix probability，无需 exact transcendental comparison。

tiny β_i 仅使 log argument 的 binary length 改变。原 labels 的 probability denominators bit length 是 O(L)，不是 O(1/p_t) 个 DP states。就算每个 item/label candidate 从零重算所有 rows 的 DP，运算数仍 polynomial。

**核查结果：PASS。** B16 的全局 error=1 已在后续常数中实际支付，未被藏进 factor-two reserve。

## 7. 任意 π rematching 和 source 条件

§7.1 的 τ 必须是在所有 U 上 true maximum positive singleton product；作者的 §3.1 确实这样构造。H 上任意 π 允许有 zero singleton edges。

将 agents 分成 E、N 后，`τ^{-1}∘π` 的 restricted graph indegree/outdegree≤1。Eτ 的各个 N outgoing edges 被删除后，原来含多个 N 的 cycles 也切成 disjoint paths。每条 path 恰终止于一个 positive ν_s；其非终点 π values 为正。

每条 path 单独把前驱改到后继的 τ-item、终点改到 B 中 attaining ν_s 的物品，得到全部 U 上的有效反事实 singleton matching。因此 τ 的最优性给该 path 的 product inequality。不同终点可能用同一个 residual maximizer，但这些是**分别比较的 alternative matchings**，并非一次同时分配；相乘数值不等式没有物品冲突。这是一个容易误审的承重处，作者已明确处理。

Eτ 用 τ、Eπ 用 π 不冲突；剩余 agents 任意补齐 H，并由 W_i>0 保护其 factor。right product=0 时用 τ 直接处理。将 W_i=v_i(T_i) 代入，再由 monotonicity 与 final actual-product matching 最优性，得到任意比较 π 的不等式。

ratio 计数分别处理 A′′、A\A′′、outside A：前者损失≤2V/(b+ν)，中者≤6，后者在 positive comparison 下 ratio=1。sum-to-max 的 factor 3 被保留；A′′ empty 时没有调用空集几何均值。

**核查结果：PASS。** 没有把 source actual OPT matching extension 偷换为新 fractional theorem；A 的新部分另有 §2 的完整证明。

## 8. 全部数值重新核算

本轮用 exact rational arithmetic 独立复算了下表；这只是常数核算，不是 backend implementation 或 algorithm test。

| 量 | 复算结果 |
|---|---:|
| d | 5/2 |
| δ_mask=1/(7d) | 2/35 |
| δ_mask/6−1/210 | 1/210=δ_mask/12 |
| 200/δ_mask² | 61,250=9,800d² |
| 10,000d² | 62,500 |
| B19 denominator 60,000d² | 375,000 |
| B20 denominator 60,000·3d² | 1,125,000 |
| 明确 reserve 后 denominator | 2,250,000 |
| C3 弱化 denominator | 3,000,000 |
| ρ=2²⁴ | 16,777,216>3,000,000 |

B18 的 analytic factor 为 `12e^(1+1/a)≤12e²<108<200`，其 strict margin 不依赖随机成功事件。B18 到 B19 的 2、outside factor 6、sum-to-max 的 3、A 中 c+1=3 均已逐项出现。factor-two reserve 之后还足够推出 C3。`ell² a/8=1/(128a)`、DP 的 `m_B·2a_0 alpha=1` 也一致。

**核查结果：PASS。** 没有发现 source 数值导入、丢 factor 3 或 precision 未付账。

## 9. C 的 unit benchmark 与 item-equality 填满

原 normalized clause total=1，故每个 positive support 的 original actual value 恰为 1，且所有 original utilities≤1。FSLP coefficients 正是 positive-support indicators。feasible λ 给 finite positive y，benchmark=1；不是以 private p weights 或 zero incidences 代替 capacity indicators。

所有 log-CONFIG terms≤0，unit witness 达到 0。作者的 item-equality 填满步骤也是有效的：当前 item u 的 column mass c≤1，全部 rows 尚未含 u 的质量为 n−c≥1−c，足够选择 deficit 1−c；只给这些配置加 u，row sums 不变，其他 columns membership 不变。monotonicity 与 original utility≤1 保持每个配置 value=1。整条目替换不增加支持数，每 item 至多一次 partial split，所以 witness 有限，事实上支持数也可保持 polynomial。

这一步在数学上不把“填满”理解为 actual disjoint integral allocation；它只构造 fractional equality witness，正是所需对象。亦不改变原状态身份或 processing times。作者未据此宣称求解一般 exponential log-CONFIG。

value、attaining-clause、demand 的公式都在 original explicit table 上；final state 重新以 unfloored coefficients attaining。内部 residual normalization 和 local grid 并未成为输出 state 的系数表。

**核查结果：PASS。** C 确实只额外使用 original total-one normalization 取得 bounded utility 和 unit witness；这没有倒灌为 B 的输入限制。

## 10. η、γ、δ_quality 的量词和 D 的 promise LP

C 的 single deterministic allocation 同时有 original utilities r_g∈(0,1]，NSW>1/ρ。对固定 rational η∈(0,1)，K=ceil(1/η)、q_eta=ρ^(−K)、c_eta=q_eta/2。若 k≥ηn 项严格小于 q_eta，则 `∏r_g<q_eta^k≤ρ^(−n)`，与 NSW>1/ρ 矛盾。这个 strict inequality 在 k≥ηn>0 时有效，无需 ηn 为整数。

`r_g≤c_eta` 严格蕴含 r_g<q_eta，故 equality boundary 也被覆盖。η 可变时 thresholds 本身有 O(K) bits，作者只主张 polynomial(K,input)，没有主张 polynomial(log(1/η))。

robust 阈值 δ_quality 与 δ_mask 分属不同结论。C 的排除量词是：固定 η 后，只在 γ>η 且 0≤δ_quality≤c_eta 的区间排除“每个 actual allocation 至少 γn 个 low-quality groups”。并不排除所有 positive γ、δ_quality，更没有强制 γ 随 source size 趋零。

D1 给未达原 quality one 的至多 D 组分配各不相同的 repair items。D2 对 augmented allocation 删除 repairs 得原 allocation，最多 D 个 groups 收到任意 repair resource，所以至少 γn−D 个原 bad groups 保持 bad。全部计数一直是同一 n groups。

D3 里 `D≤a n` 和 `η<γ−a` 给 `(γ−a)n>ηn`。YES 经 D1 得 augmented unit allocation，每组 attaining total-one state 的全部 positive support 都在其 bundle 内，所以 integral λ 是 FSLP witness。NO 若 FSLP feasible，C 输出与 D2 的 lower count 矛盾；因此 infeasible。δ_quality=0 也由 output 全正处理。

这就给显式 rational FSLP 的确定性 promise-gap test，无需调用 allocation finder，无需数值判定未知 integral NSW optimum。固定正 slack γ−a 确实使用；没有把 root/resource/job/state-agent counts 混入 n。若存在所述 Karp reduction，则 P=NP 是条件推论，作者没有构造或断言那个 reduction。

F1 的对数推导同样正确：output 中 k≥γn 项≤δ_quality∈(0,1)，其余≤1，故 `ln NSW≤γ lnδ_quality`；合并 lower bound 得 `γ ln(1/δ_quality)≤lnρ`。作者明确了固定 target 参数与 source input size 的区别。

**核查结果：PASS。** 这里没有一个隐藏的“对所有固定 δ_quality 都排除”的过强量词。

## 11. C–E 的同组身份、所有 original jobs 与 zeros

作者 §10 对每 indexed state 建一个独立 root，即使 duplicate clauses 也不合并 root/job identity。每组仍只有一个原 selector，其 eligible endpoints 为该组全部 roots；每个显式 incidence 都是独立 job，root time 为原 p，resource time 为 1，其余为 infinity。

给 final original bundle Z_g 选 original attaining state s_g，记 original quality r_g。只把这个 selected state 在 Z_g 中的 positive incidences 移到原 resource machines；其余 selected-state incidences 留 root。全部 unselected-state incidence jobs 留各自原 roots。显式 zero incidences 也留 root，time=0，不删除、不迁到 slot。

各 incidence/selector identity 恰执行一次。selected-root load 为 `1+(1−r_g)=2−r_g`；unselected-root load 为 1。每个 resource 最多收到一个 unit job，因为 actual Z_g 全局 disjoint。故 whole-matrix makespan≤2；只有 selected group roots 的 `<ηn` 例外计数获得 `2−q_eta` 阈值，不能扩展为所有 machines 都≤2−c_eta。

unit allocation 时同一完整 construction makespan≤1，而至少一个 selector 在任意完整 schedule 中必须有 unit processing time，所以 ordinary OPT=1。Q⁺ 的 repair states/roots/incidences 也是该 augmented object 的实际新 jobs/machines；没有在 YES case 漏掉原 states 或新 states 的 jobs。

为防总数表述被误解，可将每个对应对象的显式 incidence count 记为 I_Q、I_Q⁺。则 Q 有 S+m machines、n+I_Q jobs；augmentation 精确新增 nD roots、D resource machines、nD selector endpoints，selector identities 仍为 n。它新增 **nD 个 positive singleton incidences**。若 dense/specified representation 还新增 Z_new 个显式 zero incidences，则

\[
I_{Q^+}=I_Q+nD+Z_{\mathrm{new}},\qquad
\#\mathrm{jobs}(Q^+)=n+I_{Q^+}.
\]

这些 zero incidences 也必须输出执行端点。作者已经明言保留并计入所有显式 zeros；其 nD 是 positive incidence 的精确增加量，而不是声称所有表示下 total job increase 只能是 nD。本审未发现删除 zeros 或 unselected states 的隐藏简化。dense output 仍是显式 augmented input 大小的多项式。

**核查结果：PASS。** C–D 的 population n 与 E 的 machines/jobs 大小不能互换，作者也没有互换。

## 12. 非 fatal 的表述澄清与最终范围

此次没有需先修补才能成立的数学 fatal。以下澄清用于保持后续表述准确，不是追加定理：

1. 标签参数用 δ_mask、robust-quality 阈值用 δ_quality，可避免跨节同字母造成量词误读。
2. 增广 count 应区分 nD positive incidences 与可能额外显式列出的 zero incidences；每个实际对象的总 I 包括后者。
3. source 的 1,391 newline physical-line count 与 Python splitlines 的 1,414 count 相差 23 form-feeds，不是本轮发现的 source-reading 缺口。
4. 作者读过先前独立攻击及工具 proofs，且已披露；本轮是其后实际全文 read-after，不能重新包装成作者/审者彼此不可见的 blind test。
5. root 在本记录冻结前另提醒一个应用范围问题：若某拟用 source/解码仅保证 `γ≤δ_quality`，本结论不覆盖该 regime。此处只核对这个**条件数值关系**的后果；本轮没有新增读取或审计任何需求树、解码或 source hardness 材料，故不把“某具体 source 确有该关系”列为已验证事实。

第 5 点可直接证明。由 K=ceil(1/η) 有 η≥1/K，而

\[
c_\eta=\frac1{2\rho^K}
\le\frac1{2(K+1)}<\frac1K\le\eta
\]

（因为 ρ≥2、2^K≥K+1）。C/D 的排除域因此要求

\[
\delta_{\mathrm{quality}}\le c_\eta<\eta<\gamma,
\]

它与 `γ≤δ_quality` 不相容；D 中更强的 η<γ−a 同样蕴含 η<γ。对 0<δ_quality<1，若 γ≤δ_quality，则

\[
\gamma\ln(1/\delta_{\mathrm{quality}})
\le\delta_{\mathrm{quality}}\ln(1/\delta_{\mathrm{quality}})
\le1/e<\ln\rho.
\]

所以 F1 在该条件 regime 内自动满足，并不产生 source obstruction。δ_quality=0 且 γ≤δ_quality 也不可能满足 γ>η>0。此澄清不修改 Exact v5 或 Author Proof 的量词，只排除一种 scope 外推：不能把本次 PASS 叙述成“所有实际 near-two robust 源都被挡住了”，也不能据此解决所提醒的主目标 source regime。

**最终结论：在冻结 Exact v5 的明确输入、语义和量词范围内，Author Proof 的承重链可以通过此次 read-after 审查；未找到 fatal。** A 仍为一般 monotone-subadditive 的 semantic matching interface；B 只覆盖有限显式、非负 binary-rational、unweighted XOS；C 另需 original clauses total one；D 仅覆盖给定 shared singleton REPAIR；E 只给完整 ordinary matrix 的 makespan≤2 与所述 selected-group-root count，unit case 给 OPT=1。

此后若再读 canonical、其他 reviewer 文件或有新作者修订，不能回改原 Exact-first 或本冻结读后审，须另记新身份与阅读次序。

**Algorithm 仅为数学规格及复杂度证明，无 backend 实现或执行测试；全球新颖性未认证。**
