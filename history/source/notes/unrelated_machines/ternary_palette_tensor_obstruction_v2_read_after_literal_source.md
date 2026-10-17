# 三叉调色板张量／收缩限制 v2：作者证明读后攻击

## 实读与独立程度

独立 v1 陈述先行稿 SHA `fb59cbb90a782f7e8b7452a6046e89f6b12689431ba0779014f8fead74016cc2`、v2 范围修正先行稿 SHA `950164f0ce3c2d9f32096bd3f80b58857243865761f51d70f94a81152b5c493a` 均已先冻结且不改。本次才全文读取作者 proof，不声称本次是盲审。

实读文件：`/workspace/scratch/038d9dcc4cac/ternary_palette_tensor_review/ternary_palette_tensor_obstruction_v2_frozen_proof.md`。

实际 SHA256：`b2b7afdcdd362c8b8b087d97f9ba90e5bcf657d592857a7bbf9308293bc65aaa`，与给值匹配。绑定 Exact SHA `11ead3e74a0d9309174d2ad3dee16a1b30b1691ee03b0493635656f7bd8940df`。

## 结论

v2 的四项核心数学及全部 P 等式均成立，无核心 fatal objection。作者证明与本人先行独立重构一致，明确修复 v1 的常量输出范围和 U 高度缺口。另发现 proof §7 一个**复杂度包含方向错误**，须在现行正文纠正；它不是 Exact 主结论的前提，故不影响 tensor 失败界。

## 1. 完整 P 与精确 OPT 恒等式

作者将 internal machines 与颜色 resources 明确分namespace，每job有限端合法，pin单端，其余原树边job不同、均为真实parent与唯一down端。H≥1、d≥2确保root internal存在。没有合并同色叶jobs。

给满r虹彩树时，活跃机unit+(d−r)/d、非活跃机全部d枚父置=1、资源≤1；每原边job都回填一次，得C≤2−r/d。给任意actual C<2时，root pin保证C≥1，资源最多1枚unit。每活跃机至少 `d−floor[d(C−1)]=ceil[d(2−C)]` 个原端真实下送，逐层抽取同一r得到真实rainbow子树。C≥2的下界自动，所以OPT恰2−q/d，不是只有上／下某一方向。

q=d、q=1、H=1、等号阈值和不可假定存在高效求最优q的范围均正确；给定σ提取、给定F回填按显式输入多项式。路径上界覆盖任意NO，不需要分数可行性或保留原谓词。

## 2. 张量与 G_k

逐坐标Cartesian孩子确使末父palette恰为各坐标palette集合的乘积，故≤2^k。F^[k]是真正满2^k、同深rooted树；叶颜色有序tuple相等逐坐标反推同一F叶，得到虹彩而不是仅本地无冲突。于是YES精确q=2^k，实际OPT=2−(2/3)^k。

作者取A=3^k、B=2^k写出的精确通分式

\[
 G_k-G_{k+1}
 =\frac{2A(B-2)+B}{(2A-B)(6A-2B)}
\]

正确。对所有k≥1，B≥2，分子严格正、分母正，因此全k严格递减，G1=5/4，极限1。它与本人先行稿的x=3^(−k)交乘证明等价。G1、G2、G3分别5/4、17/14、53/46也一致。作者称曾算k1..30只作为其排印sanity记录；本人没有读其脚本或重跑这30值，数学认证依赖上述一般恒等式。

G_k只是NO最强可能值相对YES的上包络，不声称某实际NO族达到它，也不声称tensor保留原NP谓词。作者明确这些限制，没有把(2/3)^h叶比例误当每层branch ratio。

## 3. 旧SAT构件、常量规范与纯收缩

作者对旧 canonical 实读SHA9314...及Rigid／Dead／Atom／AND／OR／Pad底层不变量的核法与本人一致：最底Rigid是(A,B,A)，Dead末星全同色，上层组合接高度≥1构件，因此不另建三色叶星。v2 protected色及每星独有dead色不改变palette≤2。

作者明确 v1 的“合法固定常量”本来未指定，不能倒称任意YES都满足；现采用(A,B,A) YES、(A,A,A) NO（A≠B）后的规范输出族正确。来源异议已按新Exact关闭，不改旧v1历史。

纯k层收缩的末macro父含3^(k−1)份原末星，总palette≤2·3^(k−1)；任何rainbow r宏子树在一个末macro父必须选r个不同色孩子，故q≤该数。k≥2给严格小于3^k−1，k|h使宏高≥1。作者还明确此后重新按P(U)生成任务，不声称原physical P的jobs原封保存；没有将结论扩到非等长尾层、padding或改色。

## 4. 输出位长与适用操作

Tensor每层节点数3^(kell)，总数 `(3^(k(h+1))−1)/(3^k−1)` 正确，≤原节点数的k次方。tuple有序、编码可自定界且无hash碰撞，time1/3^k位长O(k)。显式P任务／机器数由expanded树控制，dense编码仍为expanded规模多项式；不承诺按binary k输出规模多项式。

k=O(log n)、原树n^{O(1)}时输出至多n^{O(log n)}的规模估计正确，但无论允许多大展开，G_k仍≤5/4并下降。这是具体操作的数学失败，不是归约运行时太大的一条代用结论。纯收缩规模不超原树，原叶色保留。

作者明确不排重新设计跨副本约束、非对齐操作、padding、改变时间或其它状态；未升级为所有张量／所有虹彩树放大不可能，也非UM main正反面结论。

## 5. 需纠正的复杂度方向旁注

作者 proof §7 的句子“准多项式gap归约，加上假定多项式近似算法，才可导出NP包含QP”方向倒置。若从NP-complete源存在quasipolynomial-size/time gap归约，合成目标的polynomial-time近似算法，得到的是

\[
 \mathrm{NP}\subseteq\mathrm{QP},
\]

而不是NP⊇QP。相应可使用的排除假设应精确写NP⊄QP，中文用“NP不包含于QP”，不宜写含义相反的“NP不包含QP”。

本候选没有建立任何这样的gap归约，且G_k已在数学上不足near2，所以更强复杂性假设无法补上缺失gap的**本意正确**。该方向错误仅在讨论性旁注，不影响Exact四项，但不应原样进入最终正文。已向root报告，冻结原proof可保留并附读后更正，不倒改历史。

## Status

作者proof全文读后攻击完成；SHA匹配；四项核心结论无fatal；v1真实域异议已在v2关闭。复杂度包含方向旁注待上述准确修文；没有新增一般Claim、代码／有限实验认证、新颖性或外部复审。旧两份先行稿保持原字节。
