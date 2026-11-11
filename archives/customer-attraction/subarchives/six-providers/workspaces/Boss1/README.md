# Boss1：恰六人半覆盖

# Stage17：真实内部源共同付款、源权端点与完整下一输入

Boss1；RUN `six-boss1-20261111`；分支 `rebuild/research-v2`；存档 customer-attraction，子存档 six-providers。研究 clone 是 `/workspace/scratch/b0fef5ec503f/co-work-anl-boss1`。原命题对任意有限单位客户、有限非空共同标签目录、任意完整有序历史纯 SPE 证明 `2W >= OPT6`，仍为 **OPEN**。空覆盖、重复行动、同覆盖别名和任意弱平局均保留。

## 恢复入口与当前边界

最后完整数学发布是 Stage16c，提交 `4f247f0a3ea65db6b4b74ff65306d964ebc6a2b9`。随后正规 mapper 任务 `six-boss1-source-requery-map3b` 的回执已推到 `33663ce220e55fa6f52e44297c0bdf3684df1fd9`，done 状态已推到 `434b525fca184b302de2688c63c72f04b71f460c`。本次十四条关系已通过正规 assemble 接回 canonical，包含此前漏索引的十三条，实际边文件总数为 2127。随后 Main 写了准确的局部整合审读，保留旧 pending 与同期未审变化；三派生文件及本批审读已确认推到 `3d2b34b8e72754f31e13e9e2c15c8f89fe090e32`。全仓 final check 仍报告 18 个未纳入当前冻结基线的新正式路径，本批不声称全仓终验完成；三个旧 Boss1 3A 任务保持原状。研究 clone 随后仅 fast-forward 这些已确认推送且与数学工作区不相交的 tracked 路径，没有再 stash/reset/清理新工作。

本页所列 Stage17 新数学在本轮 checkpoint 确认 `pushed` 之前只在本地。实际可恢复上限看 `checkpoints/` 真实回执，不能把本地 HEAD 或已生成文件当成远端保存。新 clone 先运行 `restore_frozen_text.py` 恢复两份精确压缩保全的历史文本，再打开本页、`spec.json`、下列实际输入和证明，最后 `research resume six-boss1-20261111`。同 Boss、分支、存档及子存档 `start --resume`。

## 当前 Main 已核的普遍福利下界

`visible_maximum_joint_v2/` 保留全 512 客户型 `(a1,...,a6,x,o,c)` 和独立 K 列、1003 原行及两质量式。其唯一一次 LP 已消费并精确恢复：

\[
W\ge\alpha_{1003}\,\mathrm{OPT}_6,\qquad
\alpha_{1003}=
\frac{112508769242601005698939086121271608650179}
{255504218184559114703526217520973415950853}
\approx0.44034016362630934.
\]

输入 SHA `0d80f56ac0b1f82350ae5e307370d9860b21382c7059b688904230a3b80f20a4`；`visible_maximum_joint_v2_solve/exact_certificate.json` SHA `b9c1d5339b21823b5f448f8c8242bf8b1394b181c099c2bf7d87c68d3f227aea`；求解包 manifest `110e6b873a0d7d61f552b8c2c97a28a1dc571a7b130137a5926a36496f6713ce`。

Main 亲读完整证明，并在 `main_visible_c_v2_certificate_check.py/json` 独立核全部 1003 原行、513 对偶列、两等式、非负性、互补性及原对偶目标。完整最优面仍有 21 个可非零列、秩 14、七自由参数，保全部 1003 面限制，未缩成求解返回点的正支持。

该整个最优面不能实现为原模型 SPE。正权 NS5 的完整局部零态使同一真实第二源强制最大 C 分支的源份额为 `|C|/5`，源 IC 等号因此要求 `u2=K/5`；而完整面上的准确固定差是

\[
u_2-K/5=
\frac{2090367050511169183056222233334689252587}
{30660506182147093764423146102516809914102360}>0.
\]

此结论由完整 513 列有符号面身份支持，不仅代入一个点。原 P25-C 行在这个新面上不再取等，不能复用 1002 面的旧等号推导。半覆盖仍未证明，也没有完整 SPE 反例。

## 将等号障碍改成普遍的端点付款

同一真实第二源历史 `(A1)` 强制目录最大 C 后，保留真实 R3、R4、R5、R6。逐客户 `p=1_A1,c=1_C,o=1_O`；O 是任意六合法标签的覆盖并，不当作合法行动。定义

\[
B=\sum\frac c{p+5},\quad M=\sum\frac o{6(p+4c+1)},\quad
N_j=\sum\frac o{6[p+(j-2)c+7-j]},\quad j=3,4,5.
\]

原 Main 行 `300u2+K >= 288B+12M+5N5` 已独立审计。完整新包 `source2_joint_internal_safe/` 证明如下四参数族，Main 提出扩张并直接核过，实际代理独立重建：

\[
(25+\Theta-s)u_2+\frac s5K
\ge24B+M+\theta_3N_3+\theta_4N_4+\theta_5N_5,
\qquad \Theta=\theta_3+\theta_4+\theta_5.
\]

指定仿射最小值的完整参数域为

\[
\theta\ge0,\quad
\theta_5\le5/12,\quad
\theta_4+\theta_5/36\le5/12,\quad
\theta_3+\theta_4/72+\theta_5/36\le5/12,\quad 0\le s\le9.
\]

全部 16 顶点、2048 隐藏态与 8208 全列系数已核，所有源 IC 权至少 16。三个内部 SAFE 的收益始终是同一强制 C 分支的真实收益，取完四尾 minimum 后才使用 `|C|=K`。没有冻结偏离后继或共享虚构的分支边际。原固定源权 25 的钱包位于 `s=Theta` 截面，因此 16 端点保留更多限制。

简洁端点 `theta=(0,0,5/12),s=9` 给

\[
985u_2+108K\ge1440B+60M+25N_5.
\]

其真实付款先直接证明，再作准确身份 `row985=5*NS5-515*(u2-K/5)`。不能通过相减不等式证明它。它在整个旧 1003 面的值严格负；全三权饱和的 `s=9` 端点在共同末 BR 权 1 尺度下也严格负。

族文件 SHA `a38144bb000e8585d520a731ed4159269a7245e0616d020ca12550d55df3719e`；证明 SHA `e4ba6dd0e4cde35a9c899d35e85c53a98a042b257e6bb14a01078726138210e4`；manifest `ec51f3eff143d0f555d2601deb1954a06f249aecbd4eabcfab3398d2c45d7b25`。`main_source2_reweighted_seed/` 保 Main 原始 2048 状态推导。

## 跨实际源与后续范围

`all_source_nested_safe_family/` 已证任意 actual 源 i=1,...,4、任意合法强制 T 的 P25 加真实第五源 SAFE。令 n=6-i、D=p+n+1，正确份额是 `H=t/min(D,5)`。不能用 `t/D` 代替：全部八个相应错误状态给余项 `-1/72`。完整 416 隐藏态、40 minimum、36 条全 513 列均核过。

四条 outerOmean 已被旧 P25 双 mean 的 30 异索引行逐客户支配，保留失败说明而不添加；C2 与原 NS5 模 C 质量等式等价。其余 31 纯标签行保留真实付款，不声称条条独立。Main `main_joint_cross_family_check.py/json` 又独立核了两个族全部 26676 个系数及隐藏态；旧 1003 点除七个端点负值外，纯标签负行仍是第二源 T=A4。

`visible_maximum_joint_v3/` 已按原合同冻结 1050 原行：完整原 1003，加 16 端点，再加 31 纯跨源行；513 列、两质量式不变。它明确保留 `NO_SOLVE_INTERMEDIATE_INPUT`，输入 SHA `c5ddba49b71303083b07b96f90888d56f11b291d7c307f0c3e8280b7385d280e`，manifest `f7cf345480b2d0c328a12a3485b0ad9d66c260f611b6c6e5253a16b361c857f9`。

`all_source_joint_reweighted_safe/` 已完成全部内部 SAFE 与源 IC 权的普遍推广，四源参数域分别有 39、16、8、4 个顶点，31 个真面；原源权为 `a=25+Theta-s`，一般 T 的大小项完全保留。第一源额外范围为 `s<=15+5theta_j`，最大 s 为 `1070/63`、最小 a 为 `605/63`，均唯一在四个 theta=`25/63`。Main 独立重新求交所有顶点、核全部 8064 余项、444 minimum 与 536×513=274968 系数，及 source2,C 的 8208 列模质量等式身份，全部 PASS。完整 family SHA `c8a40df9458e2add557ef14b8282880a1d14b05d55238ecf0715f63968907c18`，proof `1a72e75cbcfa36d215c5030d1b86426746d068c1afc806894272b5c9aca60f70`，manifest `3f08170af4b678688317bdebfd8468a8c62e8a801923b3e86f7612a8873825eb`。

下一输入 `visible_maximum_joint_v4/` 正准备在完整 1050 上追加这 536 行，总 1586 raw、513 非负列及两等式。新增数值除数全为 25，K 原列保持 c_i，所有旧行、重复和零型保留。`visible_maximum_joint_v4_solve/` 只准备下一求解骨架，必须等 Main 精确输入释放，当前没有优化授权。

`actual_source2_fixed_C_lift/` 已冻结无点绑定的固定 C 真实分支模板。其合同是 734 条隐藏行及 17 条显式可见前置路由；全 512 可见型各 16 真尾，共 8192 状态。旧外层 q 的两个矩约束在固定 C 中不合法，必须删除；内部 C30 的六查询矩仍合法并保留。当前不绑定已排除的 1002/1003 点，不消耗 phase-I。Main 全文实读完整推导并独立核当前 21 条 checksum；有效新冻结 manifest 为 `10012e13e443042a6be1150277207c67bfd222c7e0967e9b3818fd4a49c54f61`。首次两份收尾清单因 Main 同步与写入竞态缺失，已保存原 SHA 和事件，仅重新生成元数据；不声称原清单逐字恢复，没有数学输入或求解重跑。1050 首次 checker 的同一竞态失败亦保留，输入未变，仅重放确定性 checker。详见 `stage17_sync_recovery/`。

## 实际代理与下一问

- `/root/early_shared_x_source_audit`：已闭合 NS5、16 端点及一般源 536 行。下一义务 `all_source_ordered_joint_menu/`：外层强制 Q_k，内层对同菜单 l!=k 的五查询平均，保准确重数 d 后再取全尾 minimum，检查是否能改进已失败的独立 outermean；0 优化。
- `/root/visible_maximum_joint`：已闭合跨源第五 SAFE 及 1050 未求解中间输入；准备完整 1586 输入，0 优化。新输入逐项获 Main 复核前不释放求解。
- `/root/visible_maximum_joint_solve`：已闭合 1003 唯一 LP、全原对偶与整面排除及 734 固定 C 无点模板；只准备 1586 求解骨架，等待 Main 输入 SHA 与一次明确释放，0 新优化。
- `/root`：亲自推导源权扩张、复核全部新客户列，串行保存与推送，当前正规 mapper 集成已 pushed；随后审核更强完整输入并释放唯一求解。只有新精确候选通过廉价必要式检查后才考虑绑定 734 模板。

唯一云请求仍为 `C-six-boss1-common-x-joint-23676-01`，GitHub run `43096304349`，源提交 `b96dbcdfe0dec963bbaf91f3a9a2f0ed597467ad`。check11 为 queued，jobs/artifacts 空；未重发、取消或绕过本地大型求解守卫。固定 16hist 松弛值与上述全型普遍下界严格分开。

每次 checkpoint 只确认实际回执覆盖的文件。新成果继续回流正式正文及受影响边；当前正式计算对象 v13 只回流到此前 CAP4 阶段，不能把随后工作包当已正式登记。原题开放，Main 持续推导、核验、派工和接回。
