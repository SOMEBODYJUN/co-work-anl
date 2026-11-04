# CAGN-LP-PROJECTION 覆盖说明

本组复用现有审查页和定义/引理；没有把有限 LP、浮点分离或局部关系升级为整数客户、完整历史纯 SPE 或 HALF 定理。变量域沿用《共同目录、均分价值与完整历史纯SPE》：单位客户类型的非负整数重数/直方图质量，以及由真实前缀单步偏离引理产生的必要 IC/BR 行。投影中的质量变量可以是连续松弛，不能自动实现一个有限整数客户实例；所有离轨后继必须沿给定策略恢复后才能成为 SPE 证书。

## R-3e17a9 父方首位回复与 1269 行系统

复用正式页：

- `archives/customer-attraction/state/审查/R-3e17a9父方首次回复独立审计与1269停界--审查.md`（输入 SHA `b0e4e63965eaa4afd5e36e346f6be1f931ed8dd7dc80f8d9050ca78ec495e6f1`）。
- 共同模型 `archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md`（SHA `cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88`）。

父审计枚举 1024 个 membership coefficient states、256 个 projections；旧必要行 1143 条、新增首位推广行 88 条、条件质量界 38 条，总计 1269 条。指定冻结必要点的共同福利为

\[
W\approx0.4963200234724811,
\]

且 \(1-2W>0\)。同页给出指定 3889-row point 的 exact 负 slack，归一化约为 \(-0.0435021\)（原页保留完整分数）。这只严格分离一个固定必要系统点；它没有整数客户重数、完整有序历史动作、每个偏离的真实后继或 SPE 收益，因此不能成为 HALF 反例。新 88 行与旧 1143 行的最小 slack 可为零；“可行 necessary point”也不等于策略可实现。

## R-428 五人根续接尾部 LP 与根列生成

复用正式页 `archives/customer-attraction/state/审查/R-428五人根续接与尾部LP停界--审查.md`（输入 SHA `54e4ad8d9de43b7d3628a5ffba59c12eb45524023c3bdfaa9611031c4b04f1f2`）。模型固定 14 个主题和四条真实路径 `ABCDE, EFGHI, AEUVW, ABEXY`；尾部 LP 在 16,384 个客户 membership 类型、222 条必要行上得到目标

\[
2.209867046461754,
\]

最小浮点 slack 仅为舍入量级的零。根列生成含 720 条根扩展行、1,890 列，dual beta 轨迹最终约 `2.0166955106`，最后定价值仍为负，列生成未闭合。尾部变量和根列都是必要不等式松弛；没有精确 primal/dual 恢复、整数客户实现、根分支完整 IC/BR 或全历史 SPE，所以数值超过 2 不能推出可行反例，也不证明五人/六人 HALF 失败。

## R-275 背景交换投影续审计

复用正式页 `archives/customer-attraction/state/审查/R275背景交换投影续审计--审查.md`（输入 SHA `dd42df8741ee7a8794f2ff8c60ffbccd0f41f6977e9277cdaf80569a8d3a7f8c`）。

- `overlap_consistency_projection_m5`：\(m=5\)，4095 个连续变量、942 行，HiGHS 目标 `2.084593514818204`，加入 true-reply overlap 后仍标注 `NOT SPE`。
- `strengthened_global_projection`：1350 行、exchange coefficient `14.80952380952381`，目标 `2.2227917306871228`；该复算依赖缺失的外部 `actual_ap_projection.py`，故不能称独立重放。
- `two_remaining_projection`/`middle_floor_projection`：\(m=3\ldots9\) 共 14 个有限 retained-tax 状态；例如 \(m=3\) coefficient 4、\(K=2,v=1\)，\(m=4\) 两模式 coefficient \(8.63636\ldots\)、\(K=3.72727\ldots\)、\(v=1.18181\ldots\)。这些只证明有限投影可行，未恢复早期分支、真实动作映射或 SPE continuation。

所有投影都可作为证明路线的障碍或待加强入口，不能把聚合原子质量当作同一客户类型在全部历史的整数实现。

## 五人 44/60 行局部关系

复用正式页 `archives/customer-attraction/state/审查/五人局部关系来源与未复跑边界--审查.md`（输入 SHA `e73c2b30b333d5e71ba132a376573bfe9a16a6c5be2f056c4f223320451f06e4`）。44 行来源给出 \(a_k=8(k-1)+k^2\)、

\[
a_k u-(a_k-2)s-2F\ge0,\qquad
8(k-1)u+kK-(a_k-2)s-2F\ge0,
\]

其中 \(w=1/(b+k)\)、\(s=\sum_Cw\)、\(F=\sum_{C\cap D}w+\sum_{D\setminus C}1/(b+1)\)。60 行同源再查询关系的逐行权重为

\[
2,\;3/2,\;1/2,\;1/4,\;5/12,\;1/12,\;1,
\]

局部预算为 \(\tfrac72r+\tfrac23u_m+K/12\)。完整 44/60 行系数包、逐行变量域与可执行核验器没有作为当前输入交付；因此这些是可复用的局部代数关系和 provenance 边界，不是新的完整证书，也不覆盖六人目标。

## 统一缺口与下一步

要把任一松弛结果升级为可复用的 SPE 数学成果，仍需：

1. 明确每个连续质量变量对应的有限整数客户类型和重数；
2. 对每个真实有序历史给出策略动作和所有单方偏离后的实际 continuation；
3. 逐行恢复精确 IC/BR 不等式、终局负载和福利，再检查平局、空主题、重复标签和零客户边界；
4. 对未闭合列生成补齐列/对偶或保留“未解入口”状态。

本覆盖说明是组内工作记录；正式数学采用上述四个审查页及共同模型/真实前缀引理的原字节，未删除或改写任何原件。
