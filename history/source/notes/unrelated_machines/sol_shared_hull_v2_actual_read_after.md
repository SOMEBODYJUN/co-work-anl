# 共享 aggregate 直方图 Exact / Proof v2 的实际读后复核

来源 sol_true_hardness。root 已实际全文读完本人的 Exact-first 与 v1 作者读后记录，再明确提供以下三个 v2 / 勘误文件供读取。本次是 **v2 actual read-after**，不是全新 blind 重构，不能改写既有时间顺序。

## 1. 实际读取的版本与保持的历史

以下三文件本次均实际全文读取，SHA256 与 root 指定值一致：

| 文件 | 实际 SHA256 |
|---|---|
| sol_shared_hull_exact_v2.md | f839d92f3c5d69e9123e03b1ebbaf6624d4b15f6d3df5c85acc193fc4c146777 |
| sol_shared_hull_author_proof_v2.md | 915038cea01dd43bc7b2163b09f105754a8a275b33009e76e5fea6f9e8592541 |
| sol_shared_hull_v1_author_errata.md | 1a4de6d19c3f038685e822d471f0d3f388e6fb23bae780aec96e4802147b8a15 |

原记录与程序/输出没有改写。本轮重新 hash 确认：

- Exact-first 独立冻结记录仍为 `473e3da98481251e317fbeaf8aea3548bd159c54958d862a2948ca283a18e6fd`。
- v1 actual-read-after 记录仍为 `ee8279757a7aba4f74a51b5918ec52b3f628fae1615b58270d3f30730f4a282c`。
- 原作者 audit code 仍为 `2dfa7278cbc7677eb3c5927c11a51900cfd6c391a94ad41dc8f882bc08ece09f`。
- 本人原 targeted audit 输出仍为 `27cb65a6da68dc13fb73824ca2fee374d026374d790771f16b1cd61290c72fc5`。

未读取 new-PHP / fixed-k 层次草稿，未将 rank / matroid 附属结果作为本 Eq 的依赖。v2 专用 Proof 的实际全文 scope 是§1–6；不借它追认旧 full Proof 所有章节无 fatal。

## 2. 逐步 weak Ĥ 的对象现已明确，原错误并未被抹除

Exact v2 第3项明确写 Σ_i z^i∈Ĥ_(j−1)。Proof v2 §1 使用同一个递归对象，§2从任意最终 weak point 递归取 witness，§3逐前缀构造同一 weak 轨迹。两方向均不需要、也没有加入逐分支 z^i∈θ_iĤ_(j−1)。

Proof v2 §5明确说明 B 从 A 后的 weak Ĥ_5 继续；若要求 aggregate 属于 true H_5，则无合法 B branch。真实 H 只在四机例中作共同实际前缀的对照。该版本不存在“每一步 aggregate 都仍在 true common hull”的过强前提。

独立作者勘误明确承认 v1 full Proof 的 true-H 字面是错误，而非仅排版差异；保留原字节与原审查结论。此处修复与本人 v1 read-after 的具体反例一致，不能记录成旧 full Proof 原来已经正确。

## 3. 双向一般证明与全部整数边界复核

Proof v2 §2的 add / stay 行流，从 unit 初态经每层守恒到末层，按每机路径分解给容量≤K的带标签配置。逐 job add 总质量是 Σ_rθ_r=1，所以是完整 CONFIG，不只是某份 certificate 被接受。

§3的任意 CONFIG→weak 方向，v^+/v^- 是同一 row-configuration distribution 在每个前缀上的真实概率。own row 取 v^+；其他 rows 分摊 v^-；分母1−x_rℓ>0时行质量恰θ_i。x_rℓ=1时其他 x_iℓ全0、v^-全0，专门分段0正确；不存在除0。r∉E_ℓ时 x_rℓ=0且 v^+=0，缺失自己的 branch 不会遗漏质量。

非负前缀负载≤完整配置负载，保证 own capacity face。每个旧 job 的 inclusion marginal 保留，当前 job inclusion 总量恰1。全体 real probability points 都在这两方向内；算法返回 rational 点不将集合偷偷限制成 rational points。

边界也保持完整：

- j=0、n=0：每机唯一空配置与初态同一 histogram。
- K=0：所有有限端只能为0，仍有逐 job 的 selected-mass 覆盖约束；资格空就不可行。
- 零时间选入和跳过保持两个不同 arc 标签；不同 jobs 位于不同层，不按同负载合并。
- ∞无 selected arc / 无正 inclusion；E_j空则两系统同步不可行，以后每个前缀继续空。
- θ_i=0整份 z^i=0，θ_r=1分段正确；不依赖 OPT>0 或时间正下界。

本轮数学逐项复核后，没有发现上述全量词集合恒等式的新 fatal。

## 4. j=0 / K=0 / objective bits 的计算合同修复

Exact v2 与 Proof v2 §4现在均使用

    O(m(j+1)(K+1)+|E_[j]|(K+1))

的显式 variables / constraints bound。j=0 时 m(K+1) 个 y 坐标仍计入；K=0 时每层每机仍有一个 load node，不再把规模写成0。可直接以 y_(r,0)=1、其余0构造零步 LP。

每机是 layered unit-flow，各 job 再加跨机器 add 流质量1的 side equality。processing time a 只决定 arc endpoint；全部 LP 矩阵系数与 RHS 可取−1,0,1。Proof v2 明说 job coupling，并未利用 pure network TU 或声称积分性。

优化时间与输出位长现在额外计 L_obj。一般 feasible set 有界，有理目标取到最优；其最优 rational witness 与 infeasible Farkas certificate 的 bitlength 可按显式 LP 和目标长度控制。原 v1 所列 j=0/objective 编码问题已在新版本修复，但原冻结记录不改。

整数 K 只以 binary 输入时，K+1节点仍按数值展开，是 pseudo-poly。向下舍入时 q=δT/n，K=floor(n/δ)；固定 δ 时 K=O(n)，精确 rational arithmetic、LP构造/求解/certificate 都是原显式输入总位长多项式。δ 变输入时允许数值1/δ，不能把它换成只依 log(1/δ)。

sound cut 的方向仍只由真实 T 调度构造 Dirac 配置：每条 used edge通过 p≤T剪枝，每机 Σfloor(p/q)≤floor(T/q)=K。故 LP infeasible⇒OPT>T；LP feasible并不解码一个真实容量K调度。T=0另查零端，不产生 q；n=0另给空调度。

## 5. 四机例与 integer K=3 的精确对应、所有 job 轨迹

v2 Proof §5继续用 rational展示 p∈{1/3,2/3,1}、T=1。本轮明确将其与 integer theorem 对接：**全部时间及容量乘3**，得到 K=3，完整矩阵为

| 机器 | j1 | j2 | j3 | j4 | A | B |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 3 | ∞ | ∞ | 2 | 1 | ∞ |
| 2 | 2 | 3 | ∞ | ∞ | 1 | ∞ |
| 3 | ∞ | 3 | 2 | ∞ | ∞ | 1 |
| 4 | ∞ | ∞ | 3 | 2 | ∞ | 1 |

same job labels、finite资格、概率与branch质量均保留，load coordinate s只同步乘3。integer actual OPT=4、CONFIG threshold=3，除3即作者展示的4/3和1。这是精确坐标重标，不是新的数值运行。

四个 prefix jobs 的两个真实 full matchings：

- D：j1→1、j2→2、j3→3、j4→4，负载(3,3,2,2)。
- O：j1→2、j2→3、j3→4、j4→1，负载(2,2,3,3)。

每个 row 的 CONFIG 两配置（各概率1/2）仍为：机1 {j1}/{j4,A}；机2 {j2}/{j1,A}；机3 {j2}/{j3,B}；机4 {j3}/{j4,B}。每配置整数负载3；六件原 jobs 每件恰两次1/2覆盖，没有遗漏 aux 或把重复 jobs 合并。

记 δ_s 为 load s 的 Dirac，h_(s,t)=(δ_s+δ_t)/2。逐 job 的 row histogram 轨迹为：

| 已处理前缀 | 机1 | 机2 | 机3 | 机4 |
|---|---|---|---|---|
| ∅ | δ_0 | δ_0 | δ_0 | δ_0 |
| j1 | h_(0,3) | h_(0,2) | δ_0 | δ_0 |
| j1,j2 | h_(0,3) | h_(2,3) | h_(0,3) | δ_0 |
| j1,j2,j3 | h_(0,3) | h_(2,3) | h_(2,3) | h_(0,3) |
| j1,…,j4 | h_(2,3) | h_(2,3) | h_(2,3) | h_(2,3) |
| 再加A | δ_3 | δ_3 | h_(2,3) | h_(2,3) |
| 再加B | δ_3 | δ_3 | δ_3 | δ_3 |

前4步来自 D/O 各半的同一个真实共同前缀 law。A 的两个 weak branches各质量1/2：自己行取1/2的load2、另一候选行取1/2的load3，机3/4在每个branch各取1/4的load2与1/4的load3。shift后出现所列表第5步 ghost。

B 的branch3/4各质量1/2：自己行取1/2的load2，另一候选行取1/2的load3，机1/2各取1/2的load3；自己行平移+1后末层每行成为δ_3。所有 own faces要求 s≤2，选中 own load正为2，因此容量合格。

真实 H_5却由(3,2,3,3)、(2,3,3,3)的共同凸包给出；其机3/4固定load3，B 的两个own faces均空。因此把 B 接在 true H_5 后会失败，恰说明为什么必须递归 weak Ĥ。

任何实际 C<4时，两枚最小 prefix jobs之和2+2=4，前4件仍必须D/O。D使A的两端已有3，O使B的两端已有3，故六件不可能峰<4。反向选D、A→1、B→3，完整实际负载(4,3,3,2)，六件恰执行一次；所有零/∞/标签处理与上节一般证明相容。

专用 v2 本文还未把“×3→K=3”直接写入§5；这不妨碍上述精确 scaling 解释，但 canonical 若继续引用 integer theorem，建议加一句明确映射，避免读者把分数负载直接当作整数坐标。此项不是新反例或新的计算结果。

## 6. 精确版本比对、运行范围与最终状态

本轮只做文字 / 公式版本比对，没有无故重跑原 targeted 数值 audit：

- v1 full Proof 与 v2专用 Proof 的四机 Markdown矩阵按字节完全相同。
- CONFIG→weak 的三段 z 公式，经去空白、乘号点及“且/、”连接标点差异后完全相同；本轮逐项复核了各条件，没有把简单字符串比较充当数学审查。
- 数值、eligibilities、原 audit code 与本人已有 targeted 输出 hash全部未变；本轮新增的是 weak-H 文字纠正、计算合同修复、专用范围收束及本记录的人工 scaling / 全job轨迹说明，没有新增运行证据。

v2 Proof §6提及作者原 full audit 的115400 checks；本人本轮未读取该原 full JSON，也未执行 run()，因此不把该作者报告转记为本人新运行。本人的已运行范围仍严格是 v1 read-after 记载的 `shared_split_actual_counterexample()`，包括其内部四机穷举与 θ=1/zero/∞用例；一般 Eq 与 LP合同靠上述数学论证。

最终裁定：在本次实际读取的 v2 hashes 上，Exact 对象与专用 Proof §§1–6一致；recursive weak Ĥ 的关键定义、j0/K0显式规模、objective bits、完整integer/zero/∞边界、sound downward-rounding cut 及四机完整实际反例均通过。未发现新的 standing fatal。此为明确的作者读后，不是新的盲审，也不认证 fixed-k / rank / matroid / 新PHP 层次结果，更不升级 UM-TARGET-v1。

root可在实际全文读取本记录后，继续 final canonical 的指定准确范围审；不得覆盖历史 v1 records 或追认旧 full Proof true-H 字面正确。
