# R51分数根菜单审计器：源码合同与隔离重放

[正式审查](../../../state/审查/R51分数根菜单审计器--审查.md)补既有分数根菜单引理当批明确未读原code/JSON的范围，不重造引理。

三份冻结原件经 `work.py clean show`完整实读并原样导出；双冻结路由、blob及SHA见[source-manifest.json](source-manifest.json)。

| 角色与源ID | 原件 | 字节 |
|---|---|---:|
|主源 `1864478e226928da29a3`|[audit_fractional_root_menu.py](original/audit_fractional_root_menu.py)|3033|
|比较报告 `ffb62fe84028190eeb5c`|[fractional_root_menu_audit.json](original/fractional_root_menu_audit.json)|831|
|比较边界稿 `2b1766f3d4198f0abba8`|[fractional_root_menu_boundary.md](original/fractional_root_menu_boundary.md)|2397|

原审计器只用Python标准库，无网络或外部模型依赖。它会写到脚本相邻目录，故不能直接在冻结报告旁重跑。仓库根执行：

```bash
python3 archives/customer-attraction/tools/evidence/R51-fractional-root-menu-auditor/replay.py
```

[replay.py](replay.py)先校验三原件字节/哈希，将主程序原样复制到一次性临时目录，启用默认assert运行其原main，只将产物写回本目录 `replay/`。未修改客户、策略、常数或旧scope。

本次 [执行汇总](replay/replay-summary.json)记录Python版本、命令合同、exit0、stderr空以及两个字节比较。生成的 [JSON](replay/fractional_root_menu_audit.json)和 [stdout](replay/stdout.txt)均与831字节冻结报告完全相同，SHA256 `619560f7f2c91aad9ee82c911d8f9589468a161424c9685b8379e59100faad9c`；[stderr](replay/stderr.txt)为空。

程序实际重放43个有序决策历史、258项含自身行动比较（215项真正改选），核actual路径/收益、两真实尾列、中点六值及全六标签均匀点六值。其连续minmax、strict gap等输出含写定字段；一般实参数最优性和四标签/六标签全域结论必须同时援引既有凸对称证明，不能当成程序优化结果。

分数质量向量不是可执行SPE：真实策略已被全树核验，分数负载是独立静态对象。旧scope中的FF/extra OPEN已由另一个银行完整反族更新为假，原JSON仍原样保留。重复执行同源不是第二独立数学实现。配套报告的独立逐字段核验另见[计算对象](../../../state/计算/R51分数根菜单有限审计--计算.md)；本目录只对主代码源登记处置，不替比较来源办理done。
