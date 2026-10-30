# Bare binary Cartesian reverse amplification：canonical 实际全文读后审查

审查者：rank_deficiency_fee，2026-10-18。此记录另冻，不改作者 Exact/Proof、先行独立 Exact-first 记录或先行作者读后记录。没有修改仓库。

## 读取对象与认证范围

实际全文读取对象：

`/workspace/scratch/038d9dcc4cac/co-work-anl-boss11/research/current/unrelated_machines/cartesian_menu_recoupling_and_coordinate_consistency.md`

读取时 whole-file SHA256：

`50d41b240871e19d82c6cdb82165f13cdfb9087097e7c0162fef3cb45075592a`。

**本记录正式认证仅限该字节版本的 §1–5 数学陈述、证明、完整实际 P 与范围。§6–8 虽已实际全文阅读，只作为 context；不在本次数学认证范围。** 特别不借本记录认证 §6–7 的受限配额或 §8 软件与有限输出。有限软件由 root 另核。

重新实际读取并核 SHA 的冻结源：

* `normalized_flat_cartesian_tensor_reverse_amplification_exact_v1.md`：`60299e46c9677b6fbfc94ac866bfe317151c83154c1fe7c14510eedc84050bac`。
* `normalized_flat_cartesian_tensor_reverse_amplification_proof_v1.md`：`958aba5d1ab5d2aff945df752a80d87bb99a61f64dcfc9cf439db74717338702`。
* 先行独立 Exact-first 记录：`normalized_flat_cartesian_tensor_independent_exact_first_review.md`，`a04fa4b474fc605ccc32f32728779f02dcec7c0be91e8c01ab031cf99a9f943e`。
* 先行作者 Proof 读后记录：`normalized_flat_cartesian_tensor_author_proof_read_after.md`，`0d4594479dba2d3f3019db1b14621ba373264b07b36ebdd3853f9c50cc3b2dbb`。

为核 §5 的关联范围，实际读取链接中的完整三态正规形/路径降度合同与旧 palette 张量限制所在段落：

* `research/current/unrelated_machines/degree_three_weighted_menu_cube_embedding.md`，whole SHA `5e3f12dff54e770ff4afeae4201ef7f5c21536f0243858708fc24e3449439b41`；此次只用于核对 §5 引用的保值后果，不另行重新认证其中全部结果。
* `research/current/unrelated_machines/ternary_rainbow_subtree_exact_hardness.md`，whole SHA `3f3075ec56543f2e2b1f909614c853762b66232c0081d311e9c3d1f58d8b1903`；此次核 `UM-TERNARY-PALETTE-TENSOR-AMPLIFICATION-OBSTRUCTION-v2` 的域与机制，不认证全文的 SAT 困难性。

## §1–5 的数学核查

1. **域和完整矩阵。** t≥1，D=2^t；每 group 有全部 D 个 indexed states，每 state 有 D 枚 distinct resources、各 private 时间 1/D，总质量1。每 incidence 有且只有自己的 private 与其真实共享 resource 两个有限端，selector 只在本组 private 机 time1。全部 D^3 原 incidence jobs 均实际存在，未选 states 没有被删除。资源没有被 incidence 私有化。t=0 明确排除；t=1 的基例和循环自依赖有效。

2. **V 的任意 partial 上界。** 对任何一对补 groups g 与 g+1，任意已选 states 的共同资源恰有一枚。两组不可能都领取完整支持，因此至少一组整数领取数≤D−1。此论证覆盖优化中的任意整体 state 函数及任意非 Cartesian partial subsets；不假设标签只看自身坐标。

3. **V 的达界。** 循环标签 ℓ_i(g)=g_(i+1)，领取全部 a≠1^t 对应资源。若两组领取同一资源，δ_(i+1)=a_iδ_i，至少一枚零 a_i 沿整个环强迫全部 δ=0。因此每组 D−1 枚资源共同不交，精确 V=1−1/D。t=1 时保留 a=0 这一枚，仍成立。

4. **Actual 全 jobs 上界。** 每 selector 在自己的 selected state；该 state D−1 件 incidence 外送，剩余一件留 private；每个未选 state 的全部 D 件 incidence 都留它自己的 private。selected private 负载1+1/D，unselected private 负载1，每 resource≤1。每件原 job 恰一次，得到完整原矩阵实际峰1+1/D。

5. **Actual 任意调度下界及 C=2。** 对 C<2，每 resource 至多接一件 unit incidence。取 selectors 实际所在的补组 states，共同资源对应两件不同原 jobs，至少一件必须留在自己的 selected private，那里已有 selector，给峰≥1+1/D。未选 state 的额外外送不能消除此下界。对 C≥2，因 t≥1，2≥1+1/D，故下界自动成立；不漏 C=2 等号。因此任意完整实际调度受限，精确 OPT=1+1/D=2−V，而非只分析一类正规调度。

6. **规模和位长。** Groups D；private 与 resource 各 D²；jobs D³+D；finite 条目2D³+D²；dense 条目(D³+D)·2D²。标签与1/D的二进制编码 O(t)，逐项生成与完整见证核算按显式总编码长多项式。不承诺 poly(t) 输出8^t原 jobs；不按分母数值复制。

7. **正规形组合。** 本族是 normalized flat 源，可接已链接的真实三态/degree3正规形。该合同给 actual OPT 精确相等，包括2端点，并保 V；所以目标仍有已下降的 OPT=1+1/D。即使把大资源跨组度 D 和大菜单 D 降为3，也不能恢复裸 product 没有保住的 NO gap。此是保值合同的直接后果，不是额外源困难性或新的 gap 放大。

8. **旧 palette 的区别。** 旧对象是末层三叶至多两色的三叉树，按有序元组相等的对齐张量把分叉 d 变3^k，YES 的最大虹彩分叉被终端 palette 卡在2^k，实际 YES OPT=2−(2/3)^k 上升，完备性目标丢失。本页对象是二态 normalized flat Cartesian 菜单，所有 product states 均为真正 Cartesian，但允许每个完整 group 重新选择标签；循环标签给 NO 侧 V 从1/2上升至1−1/D、actual OPT反降至1+1/D。两者失败方向和对象不同；仅可称区别于已链接的旧机制，未作全球文献新颖性认证。

## 结论与边界

在上述精确 whole-file SHA 下，canonical §1–5 与冻结 Exact/Proof、先行独立重构一致；本次未发现 standing fatal objection。域、任意 partial、全部原 jobs、C=2、显式位复杂度与否定范围均闭合。

认证只及这一个明示裸 binary Cartesian 操作，及 §5 的已知保值后果。它不证明所有 products/tensors 失败，不给实际 coordinate-coherence gadget、normalized tiny-NO 源、一般 UM 算法或主目标反面。§6–8 仅 context，不能由本次认证扩域。
