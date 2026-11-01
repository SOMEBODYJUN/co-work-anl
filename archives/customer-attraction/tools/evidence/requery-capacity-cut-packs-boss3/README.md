# 同源再查询与容量报价三份冻结切面包

主源为三JSON：6165B all_queries、3013B pending、5134B capacity_master。三份共27条历史记录，在共同1905列上恰24个不同系数向量；每条原负slack均从绑定输入精确复现。数学定义、完整参数表、重复原因及5692上的两个不同负切面见[正文](../../../state/计算/同源再查询与容量报价的三份冻结切面包--计算.md)。

## 输入和实际读取

`source-manifest.json` 保存双冻结来源、blob、SHA、字节数、角色和原路径。所有三主源全文实读。关联的requery/portfolio源码全文读；旧query模块只读PAT/GS/groups；两个点仅为指定切面输入，不冒全矩阵重新认证。requery源码属于另一认领，不在本批done。所有所需冻结原字节均保在original/。

## 重现

Python标准库即可，无网络、凭据或求解器。第一条从字面索引对及后继位重构所有27行，并与AST提取的作者纯函数逐系数核；第二条只用已核系数解决pending五条在5692上的具体接续缺口。

```bash
python audit_cut_packs.py
python compare_pending_with_new_point.py
```

两个命令从证据包目录运行。第二条默认读取仓库中既有 `b-family-menu-prices-boss3/original/research_2/all_menu_prices_exact.json`，或用 `--new-point` 显式传入同SHA原件；SHA在脚本与结果中固定。该原点已经在另一批完整核5692行，本批不重复。

## 保存证据

- `runs/exact-cut-audit.json`：27记录、52,075系数比较、全部参数及精确slack、11次13→16补零比较。
- `runs/all-sparse-row-coefficients.json`：全部行的长度和非零系数；未列系数均严格零，含完整行SHA。
- `runs/pending-at-5692-and-record-identities.json`：共同1905描述符一致、其它系数零、27记录24向量、五条新点余量。portfolio符号+−+，requery两条同一负值。
- `runs/audit.stdout.txt`及`runs/execution-record.json`：实际已观察的执行信息。报告mtime明确为文件生成时间，不冒进程起止时间。

首次独立切面审计约1.0434秒，exit0；本批没有运行原CLI、历史384个发现LP或任何整个保存矩阵的重放。精确点低于half不是完整SPE；有效切面负只排保其所用坐标的补全。没有修改原JSON、原代码或来源归属，也没有删掉重复历史记录。
