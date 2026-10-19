# Token-label bridge canonical v2：知情 final actual-read

2026-10-18，sol_true_hardness（6.1sol max）。本次是已读 Exact-first、作者 Proof 之后的知情 final-read，不是新 blind 来源。

实际文件：`home_unit_cycle_token_bridge_with_label_boundary_final_v2.md`。
完整 SHA256：`dd3a012c9e24eb64a6ddc4f8e953ccc787aa27cc8a6945a454af2357d5689fb8`。
本次读取时304行、28121bytes；实际全文读范围为第112–304行，即完整新增 §7、§7.1–7.7。

前13728bytes仅取 hash：`d8eeff7d6763b03172f57770021a250782ad796a10a44d1bb4ac62777e7556e9`。没有重新全文读或重签这个旧 prefix、旧 native-cycle 主张及其历史 evidence。完整文件 hash 也不代表本次全文重审旧 prefix。

结论：新增 §7 的数学范围准确，general M1、所给 aggregate M2/no-extension、全局 affine-context K 的整体 PSD 及其 SOS 通过本次实际读取。此前多 context 的 off-diagonal 歧义已在 canonical 明确排除。没有发现影响所写范围的 fatal。

## 与已冻结来源的对齐

此前实际来源保留原 hash：Exact `5a953ed6365e2be029ef31d3ee0184447d626971ad8af7369ee5190eac69a86d`；作者 Proof `88904ae073464b199a928516af9918422f684c606ff5efe67e075ba2e70a06a8`；独立 Exact-first `091585c4b21b13eb8487435d094fa6b0d8905655c88a7232faa4a39d32d1b9d0`；作者 actual-read `6836e703ef5084e67c8655aedae6397f5aad575df44ecfdb51961e553196187e`。本次均未改。

§7.1–7.2 的共同四阶方程、全 groups/context、k=1 的线性替换、r=0/k、home mixing 和类别 Laplacian，与已独立证明一致。没有把各行可行 projection 冒成共同 functional，也没有把真实 injection 的随机解释当成伪矩完全正性证明。

§7.3 的 beta 是 signed weights，两个 full-row laws 只指 anonymous cardinality-four 行与 Boolean Y 行；非 joint true law、非完整原作业 CONFIG+M2。扩大210点函数空间的 Schur 三个正值 `10729/10000,59/40,2687/160000` 正确，与独立 pair-basis Schur 并不混用。67 Gram rank55 有独立解析与 Fraction 依据。

这里另解析核 §7.3 所写46维原 M1 rank38，而不借未打开的软件：40个 head variables 的真 uniform labelled injection M1，连常数共41维，恰有四条 token-row 一热关系，故 rank37。确无其它线性关系：固定其它三行选择，任一行可在任意两列间替换，迫该行所有线性系数相同；只余四条一热关系。beta 与 nu 的 singleton 均2/5，所以 Y 在 M1 与各原 head 的 covariance 为零；`Y−delta` 的范数 `delta(1−delta)>0` 再加一秩。四个 home 变量全零，最终46维 rank38。

§7.4 的 formal Q²=−1/150、保持全部 aggregate≤4 矩的任意 extension 不存在两种证明均保留正确量词；没有由某一 uniform kernel 失败推所有延拓失败。§7.5 所列13机6job、48 finite ends 及全部 jobs 的 OPT1 见证均正确；本次只核其列明 ordinary 矩阵，不凭旧 prefix 未重审内容替它扩范围。该普通实例自身有 strong Dirac 点，坏 aggregate point 非原 native gap。

## 新 §7.6：完整全局 affine-context K 的独立度数核查

任一原 token a 的 head 类别 x_a,i 可为一个原端，也可为该任务一组互不交原端的和；不可用类为零，类别不必覆盖 home/其它端。原 one-hot/Boolean ideal 通过 degree four 使每类幂等、同 token 异类乘积为零。这些关系乘任意两个 affine expressions 的积仍总度≤4。

固定一个全局 affine context 列表 z_0=1,z_1,…,z_s，允许含本组某个原 label。任意系数方向给 `t_i=Σ_l c_i,l z_l`，令 `S_a=Σ_i x_a,i t_i` 与 `B=Σ_i X_i t_i=Σ_a S_a`。S_a、B、q_a=S_a−B/k 均至多二次。

原 ideal 正好给

`Σ_a L(S_a²)=Σ_i L(X_i t_i²)`。

所以

`cᵀKc=kΣ_a L(S_a²)−L(B²)=kΣ_a L(q_a²)≥0`。

等式只用次数四内的原方程，共同原 M2 对每个 degree-two q_a 的真实平方范数非负。即使 z 含个别原标签仍成立，无需标签对称化；若 z 不含个别标签且置换不变，才可进一步命名为 standard-label 表示块。canonical 对这两种情形已有正确区分。

X_i 不要求 Boolean；本证明没有把 `X_i²` 错约为 `X_i`。类别未覆盖全部 token ends 也不影响 `B=Σ_a S_a` 或平方恒等式。k=1 时 q_1 恒零，整个 K 由原 ideal 恒零。没有新引入第六阶矩、未知 conditional law 或数值 precision 假设。

整体指标确为 `(i,l)×(j,t)`；canonical 已明确禁止把任意异 contexts 的 cross-block 单独称 PSD。对角 principal blocks 与全局矩阵的 PSD 均是正确对象。

取已给 counterexample 的 context 基含1和Y、方向 `t_i=s_iY`，则 cᵀKc=−1/25，四个 q_a 平方期望和为−1/100，乘k=4恰对齐。它是给定 aggregate point 的不延拓证书，单独该必要 block 不充当完整匿名可延拓判据。

## 软件与主目标边界

§7.7 区分显式 k 原 jobs 的 M1 输出规模与仅二进制需求，四阶下降阶乘 bit 长度和给定 polynomial context 列表的 K 尺寸均正确。包含原标签的 contexts 在原 M2 内给冗余约束；若已抹身份，不能免费从更少匿名矩中恢复未知条目，canonical 没有作这个承诺。

本次未打开作者 code/audit 或目录改动版，不签其 SHA、运行事实、路径选择或 ROOT=Path.cwd() 修改。root 已报告实际代码全文读与新目录重放；该软件复核由 root 保持其独立记录。此次数学 actual-read 不代签它，也不新增运行。

本次没有证明一般 exact SDP finder、growing-depth 共同状态构造、一般 UM 算法、近2 hard source或弱调度 source decoder。repo 未改，Exact/Proof 原件未改，Work/Git/凭据未使用。
