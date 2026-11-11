# Boss2：恰六人半覆盖

- RUN：`six-boss2-20261111-cross`
- 分支：`rebuild/research-v2`；存档：`customer-attraction`；子存档：`six-providers`。
- 当前clone：`/workspace/scratch/0ecc5caed424/co-work-anl-boss2`。
- 实际工作文件：`research/workspaces/six-boss2-20261111-cross/`；主笔记`main.md`；输入`spec.json`。
- 事件与证据包：`research/runs/six-boss2-20261111-cross/`。
- 原题仍开放：对任意有限单位客户、有限非空共同标签目录、每份完整有序历史纯SPE，证明`2W >= OPT_6`或给全离轨IC精确反例。
- 首个义务：沿已被两条不同真行排除的5692点，加入已认证同源/容量切面并重优化；推导仍缺的真实跨枝约束及其覆盖预算。

## 恢复

用同Boss/分支/存档/子存档执行start --resume；打开本README及主笔记、各solver笔记和计算产物，再执行`python work.py research resume six-boss2-20261111-cross`。

当前为新RUN：start --resume返回本Boss六人工作区created=true；起始远端fee00e0b8f6ec7509fa178975e24769547aab8e9。仅以checkpoint实际pushed回执判定后续可恢复。

## 当前可接续成果

1. `master_cuts/merged_5716_exact.json`与`dual_exact.json`给5716有限图精确最优0.4900905644294647…；对应精确矩阵已保。
2. `joint_requery/selected_cuts_5716.json`的5条强PAIR跨枝切面、`coverage_bridge/new5716_joint_discounted.json`的6条折扣重查询切面均已Main独立精确核通过；它们排除该5716点。
3. 当前未完：5727增强图重优化/双证、四状态前一主题重查询与更早源的联合PAIR分离。
4. 16hist全d=1，纯静态OPT多槽交换在此支持上冗余；不要再次走该路线。

已确认远端入口（首轮）`2fd3f0e33ab2df27df598fea0d205edfaef479c2`；后续以checkpoint回执为准。
