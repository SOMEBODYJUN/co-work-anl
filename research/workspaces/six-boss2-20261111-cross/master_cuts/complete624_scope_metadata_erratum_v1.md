# 完整624输出继承构造scope的说明

受影响文件为 `complete624_actual4_R00_solve_v1_*`、`complete624_actual4_R00_opt_v2_*` 中含 `scope` 的数值/原始/对偶/验证JSON。它们的scope来自已审输入矩阵 `../joint_requery/complete624_actual4_R00_v1_matrix.json.gz`，原文中有 “Prepared … No optimization”。这句话准确描述**矩阵制备时**未优化，但不再描述随后求解阶段的执行状态。

不改任何已冻结字节。准确执行状态如下：

- `solve_v1` 已作一次HiGHS数值发现并恢复全行精确可行点；其首轮对偶失败，如实保存诊断。
- `opt_v2` 已作一次更严IPM/crossover发现，另存新精确可行点；516项非负有理对偶与其同值，完整12666行/12631列精确核验PASS。
- Main独立 `main_verify_complete624_opt_v2.json` 已复核整矩阵原始/对偶PASS，准确最优为 `formal_complete624_12666_gap_v1.md` 中的W*。
- 原始文件 `exact_optimum_claim:false` 的范围是该文件单独只给可行原始；全局有限LP最优性由同值对偶和最终验证共同给出。

此处是阶段性文本字段的澄清，不改变矩阵、任何分数、列/行身份、SHA或数学适用域；也不把固定必要系统升级为完整SPE充分条件或一般half证明。
