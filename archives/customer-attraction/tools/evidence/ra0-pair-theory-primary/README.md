# Ra0 pair_theory 十三主源证据入口

十三主源均在 `R-a0bb57fa24044a8794bc7991918a19c6/security_aggregate/pair_theory/`，共 **157146B**、五程序八JSON。父方claim已pushed `83ecdd25e46c0b454349c7e73880a391d4fba49d`。全部原件在导出后完整读，包括三份大JSON的全部825条计数动作；没有按文件名verified、Gram、success或gap判断数学。

[source-manifest.json](source-manifest.json) 保每源原id、完整双冻结commit/path、blob、size/SHA及本包原件路径；原字节在 `original/<ID>/<basename>`，父方导出记录原样在 `export-metadata/`。这里的pushed是认领状态，正文checkpoint/done由父方另行办理。

## 正式对象与结论

- [41客户坏最优查询及完整最优面](../../../state/反例/四十一客户的坏安全最优查询与最优面费用区间--反例.md)：两primary，复用已保3516B原41包。三人五题完整31节点策略actual044，W29/OPT37/v3=19/2；P*精确为p0=0、0≤p1,p2,p3≤1/5、s≥13/34、p4=1−s，费用区间[57/2,446/15]。坏p只反ALL，good及整个面最低值说明该例EXISTS成立。
- [固定策略与对称目录的删除费用锥](../../../state/程序/固定策略与对称目录的安全最优删除费用锥--程序.md)：八primary。保CCE鞍点发现iteration0，初始13向量读取后未用；循环三报告2000计数及825动作；双组g4n4全历史策略。均查某个安全最优p，未排整个最优面。四个对称保存点都精确是一名共客户，任何完整策略都是SPE，W=R=1解析等号，不能推广全部浮点锥。
- [成对成本极限的两个冻结版本](../../../state/程序/成对成本极限的两个冻结版本与有限记录--程序.md)：三primary。当前源Mq−n diag、两报告Mq−diag；两常对角矩阵的IC不变但excess相差112、1376。保全部矩阵/概率/状态和源字面，不修改代码伪造复产，不授有限客户CAG证书。

[relations.json](relations.json) 登记阶段三承重关系及边界。[related-material.json](related-material.json) 绑定实际完整读的十二正式对象，包括父方刚发布的31客户SSR真反例与两个已更新入口、旧13客户CCE完整策略、R31bbb隔离屏和辅助二次模型边界。read_sha只是实际比较版本，不是要求这些活入口以后永不更新的运行依赖。

当前一般SSR及包含空背景的普遍背景SSR已由另个31客户完整SPE否定；本包41只反ALL，不与31混同。二者都不否真正安全聚合或当前六人half。

## 原程序必要闭包与副作用

[reused-dependencies.json](reused-dependencies.json) 指向实际读过且核SHA的三份已保存原件：41原输入、13客户example及其完整certificate。后两者是CCE程序根路径读取的实际文件；原13向量虽不影响该main初轮，仍保其真实读入。其完整动作图与41输入相同，但客户谱不同。

41核验器只需标准库，必须与41原JSON相邻；main会**覆盖相邻verified JSON**。本次没有在原件旁执行。CCE程序用 `ROOT=parents[6]`，模块导入即读原证书/构数组，main另读example并覆盖相邻results；不能从按ID散置副本直接假定项目根导入正确。其余三程序无本地文件依赖，都是标准库+NumPy/SciPy/HiGHS；历史库版本未保存，不能补造。

原四优化main、41核验main、LP/MILP、BI运行、随机新样本、旧成熟审计重放，本批均为 **0**。41完整SPE/静态值/费用由正文的七类背景表及精确解析论证承担；共客户SPE也是全历史恒等证明。结构字段检查不当数学证明。

## 唯一新结构绑定事件

[check_preserved_policy_structure.py](check_preserved_policy_structure.py) 只读三份循环原报告，核全部计数键、无重复、动作合法、全兴趣唯一非零字面质量，并沿保存动作表读根路径。它不计算效用、IC、BI、LP或随机数。唯一执行一次，exit0/stderr0，命令、UTC、Python、脚本SHA及范围在 [execution-boundary.json](execution-boundary.json)。

[完整结果](policy-structure-report.json) 与 [stdout](structure-check.stdout.json) 给：

| k,m | count记录 | 读出的有序路径 | 声明终局计数 |
|---|---:|---|---|
| 6,5 | 210 | 5,0,4,1,3 | 110111 |
| 7,4 | 120 | 4,6,1,2 | 0110101 |
| 8,5 | 495 | 1,3,5,7,2 | 01110101 |

完整原825动作另有 [可逆逐条阅读投影](cyclic-all-policy-reading-projection.txt)：每条固定k位单数字counts后跟action，原记录顺序保留；所有字段均已印出且原JSON保全。它不是抽样、摘要或策略总数统计。[all-report-read-ledger.json](all-report-read-ledger.json) 只是八JSON读域索引，不代替原文。

如独立复查结构，可以把下面作为**新**运行，输出必须不存在；不是本包的额外执行记录：

```sh
python archives/customer-attraction/tools/evidence/ra0-pair-theory-primary/check_preserved_policy_structure.py \
  --evidence-dir archives/customer-attraction/tools/evidence/ra0-pair-theory-primary \
  --output NEW_STRUCTURE_OUTPUT.json
```

## 旧页增量路由与交付

[suggested-r31bbb-route-append.json](suggested-r31bbb-route-append.json) 给旧R31bbb屏幕页的精确追加文本和目标路径，本代理**未应用**，供父方串行增量整合。它保旧1500/smoke时态，新增41精确完整SPE与31的EXISTS反例入口，不整树覆盖旧历史。

十三逐源语义回执在 `cleanup/workspaces/Boss2/receipts-ra0-pair-theory-complete-20261102.json`。完整新增文件/字节/SHA最终清单由独立stage外delivery给出；本包没有Git/work.py、claim/done或认证操作。
