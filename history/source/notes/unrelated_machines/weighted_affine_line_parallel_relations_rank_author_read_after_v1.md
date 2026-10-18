# Weighted affine并行关系：rank实际作者Proof读后 v1

审查者：rank_deficiency_fee，2026-10-18。先行Exact-first记录865ed899…已冻结且root实际通读，本次获准后才全文读取作者Proof。另冻本记录，不改raw Exact/Proof或独立记录，不写repo/Work/Git。Bulk候选不纳入本审查。

## 1. 精确读取对象与顺序

实际全文读取：

`/workspace/scratch/038d9dcc4cac/weighted_affine_line_parallel_relations_half_escape_proof_v1.md`

wholeSHA256：`17bfce4c624b6c72566940329328f9765541e65db6a5156a4b6a2912761da6de`。

对应Exact：`weighted_affine_line_parallel_relations_half_escape_exact_v1.md`，SHA `780454f7a404d2fd17edf2adbf2e8e2fdd8318f98686478547a3be58d4433c7e`。

先行独立记录：`weighted_affine_line_parallel_relations_rank_exact_first_review_v1.md`，SHA `865ed89990239c36dabefe8250d72c7cfb2a4ea5f4f10ee4b609b2beea368be4`，本次重新核hash未变。

先行重构时仅读取指定Exact，未读取作者口头策略/Proof或其它agent新推导。Root先见作者口头策略、再实际核本候选，故root不记作盲审；该路由与本记录一致。作者Proof前言写作时reviewer仍持Exact，是历史状态，不倒填后续事件。

## 2. 与独立重构逐项一致性

**条件分布。** 作者以(c,d)→(c,cj+d)的C×D与C×A_j双射，先条件于完整selected state a，再取c_i均匀边际。与独立记录完全相同，正确允许w任意依赖整个state。k≥2是R^(k−2)纤维计数所需；不误假定各c_i或各j的states彼此独立。

**相交结构。** 固定c,d，tagi中y=d_i z+j(c_i z+1)。c_i0时所有线平行不交；非零时共同点P_i=(x_i,−1/c_i,−d_i/c_i)，除该点不同j绝不交。各P_i因tag分离而不同，且属于全部groups的selected supports。与独立记录的K(c,d)相同。

**总损失。** 固定state条件下每非零z成为共点的概率1/R，零z永不成为共点；所以每组条件期望loss≤1/R、总期望≤1。作者未用权的共同item属性、对称性或最大单项界；式(12)对任意state-dependent非负权有效。

**唯一例外。** 找到总loss≤1后，最多一组loss>1/2；所有共点可一起给该组，令其质量1、其它质量≥1/2。无例外时共点可不用。等号1/2、不同比重和零系数均正确，不拆分物品。与独立整数分配相同。

**确定性位多项式。** 枚举R^(2k−2)≤(R^k)²候选，每个候选只读最多kR个输入权并精确比较总loss≤1；有限平均保证找到。完整state/weight表显式，所以此枚举对总输入位长多项式，k/R不必固定；不能误称poly(k,logR)的succinct算法。模域运算、求逆与有理权相加位长都多项式，无分母数值复制。

**完整actual。** 每selector选态，B_j对应原incidences导出，其余全部原incidences留自身private，含所有unselected states和零私时job。Selected private≤3/2、unselected private=1、资源≤1，全原jobs同一assignment一次；counts R^k private、kR² resource、kR^(k+1) incidences、R selectors、finite2kR^(k+1)+R^k和dense乘积均一致。

**Singleton与k1。** A'_j唯一(j,0,…,0)的第一tag共点(x₁,−1,0)放权1，给V0；全部private峰2，任何C<2强迫R件共点unit一起外送而矛盾，所以actualOPT2。R2时−1=1仍有效。k1主关系本身正是singleton，不得扩域；主k≥2/R≥2无退化。

## 3. 范围与结论

作者Proof与先行独立重构在全部关键步骤、构造、边界和scope一致，未发现standing fatal objection。可以认证正式ID `UM-WEIGHTED-AFFINE-LINE-PARALLEL-RELATIONS-HALF-ESCAPE-v1` 对指定完整all-tuples sum关系、任意state-dependent norm1权的det-bit-poly半值逃逸及全原UM≤3/2。

仅否定对包含本显式value1/R族的整个NO域、保持groups/states/resources/eligibilities而只改incidence权时一概V<1/2的接口。不排避开本族的hard image、任意relations、额外gadget或一般source编译。Singleton与主族皆非困难性源，没有新软件/有限实验或全球新颖性认证。等待canonical实际范围审查，原raw保持不变。
