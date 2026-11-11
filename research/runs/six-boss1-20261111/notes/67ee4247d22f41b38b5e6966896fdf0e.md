# 5692 行加三包 24 个不同切面的必要 LP 重算

运行：`six-boss1-20261111`；内部计算代理：`/root/augmented_lp`。

## 正在承担的数学义务

在原固定 16hist、4849 列的 5692 行必要系统中，加入三包 27 条历史记录对应的 24 个不同有理系数向量，重新最小化归一化福利 W。回答新系统是否仍有严格低于 1/2 的精确可行点，以及新最优值是否严格高于旧点的 W。若新可行点较旧点高，只有额外核验精确对偶下界后才声称严格提高；浮点最优状态和新可行点自身均不足以单独作该断言。

模型仍是六人共同目录完整历史纯 SPE 的必要投影，只固定现有 16 个 hist。任何新可行点不是 SPE 或博弈反例；即使该支持域达到 half，也不证明全模型。

## 已实读与输入身份

已实读根 `AGENTS.md`、`共同目录完整历史模型--定义.md`、`实际末主题分支分离器与四菜单补价原点核验--计算.md`、`同源再查询与容量报价的三份冻结切面包--计算.md`，及原构造器、材料化器和独立切面重建的定义代码。

原点：`archives/customer-attraction/tools/evidence/b-family-menu-prices-boss3/original/research_2/all_menu_prices_exact.json`；SHA-256 `46e52c1cec4a5cac3e6d7fe3bbe8d227cd663e428ca7f4e955182343eedb418e`。旧 W 为

`1905769909616898376137238949200623274593168205/3898693540058852735821709960049703833207552519`。

切面输入：`archives/customer-attraction/tools/evidence/requery-capacity-cut-packs-boss3/runs/all-sparse-row-coefficients.json`。27 条记录均仅使用前 1905 坐标，其余 2944 坐标补精确零；按完整有理稀疏向量去重，目标为 24 条。

## 材料化 schema 问题与适配

确实先执行了封包 `b-family-menu-prices-boss3/materialize_runtime.py`，目标为本人子目录的 `augmented_lp/runtime`。基材料化器完成 47 份文件的大小/SHA 校验和复制；外层随即在 `rec['stored_path']` 抛出 `KeyError: 'stored_path'`，退出 1。

当前 `source-manifest.json` 实际是 8 条：使用 `local_original` 或 `local_replay`，目的路径使用 `path` 或 `basename`，与该脚本预期字段不同，也与正文所称覆盖 9 条不一致。本人没有修改封包。局部 `augmented_lp/prepare_runtime.py` 先复核已复制的全部 47 条，再逐条核实际 8 条的 SHA/size，将它们映射至已知 `research_2` 运行路径。适配执行成功，记录见 `augmented_lp/materialization.json`。运行树是完全可重建的中间产物，不需要整树推送。

## 当前执行与恢复入口

`augmented_lp/solve_augmented.py` 已启动，stdout/stderr 写在同目录。它将调用未经修改的 `B_menu_prices_master.build(all_families=True)`；核原点全部 4849 个非 weight 描述符；调用封包 `audit_cut_packs.independent_row` 的字面后继实现重新构造全部 27 条，并逐系数比对；然后建立 5716 行稀疏矩阵并求 LP。

程序会在任何有理恢复前先保存 `augmented_lp_float.json` 和完整求解器数组。之后以原 `exact_solve`、原 `exact_point` 的支持/活跃阈值恢复有理点，省略全零方程但不删除任何待核不等式；全部 5716 行及非负/归一化都用 Fraction 回代。最后尝试恢复精确对偶并逐列核非负剩余系数，以认证有限系统的最优性。任一步失败将保存准确 traceback 和浮点候选，不把失败称为严格界。

主要输出将包括：`inputs.json`、`cut_records.json`、`old_point_audit.json`、`exact_matrix.json.gz`、`augmented_lp_float.json`、`augmented_lp_exact.json`、`primal_exact_audit.json`、`exact_dual_certificate.json`、`status.json`、`stdout.txt`、`stderr.txt`、`progress.jsonl`。当前数学结果尚待本次进程完成；本笔记的初始状态不预先宣称可行或最优。

恢复命令（仓库根）：

```bash
python3 -B research/workspaces/six-boss1-20261111/augmented_lp/solve_augmented.py
```

正常已有运行时不要重复启动；先查 `status.json`/`progress.jsonl` 与活动进程。给后续同源及跨枝代理的优先接口是两个完整 4849 列新点 JSON。
