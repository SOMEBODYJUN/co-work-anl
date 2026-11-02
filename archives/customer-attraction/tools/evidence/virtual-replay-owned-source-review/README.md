# 虚拟重放专项11源与两套原审计

11个原件共70214B，全部以Boss4本人现有in-progress源逐件`clean show ID --out`取得，逐字节核size/SHA。仅整理这11件，不继承根稿对其它导航的读取声明。两冻结提交`68fad804ec5946cb296f77dc5b336308a66abf12`和`aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`对本批每件内容相同，完整blob/size/sha256/来源定位在[sources.json](sources.json)。原件按完整原相对路径存入original/，不覆盖它们运行。

正式数学：[局部cap/谱预算/正背景精化](../../../state/引理/因果删位的最大主题误差与正背景精化--引理.md)、[Cartesian末位与G重置差](../../../state/障碍/笛卡尔保计划修复的末位边界与重置差--障碍.md)、[完整源审查和去重](../../../state/审查/虚拟重放专项原审计与候选去重--审查.md)。已有因果回放主引理和五客户最小首位嵌入反例分别继续复用原正式对象，没有重建第二份主定理/反例。

| 源ID | 原件 | 字节 |
|---|---|---:|
| 319a51070af88ef8f0e1 | [audit/README.md](original/research/workspaces/customer-attraction/R-4ffa8b85fa8847e09e45dcafc8e1326f/audit/README.md) | 1445 |
| 72aa0c5864f013cbb03e | [audit/audit_virtual_replay_independent.py](original/research/workspaces/customer-attraction/R-4ffa8b85fa8847e09e45dcafc8e1326f/audit/audit_virtual_replay_independent.py) | 6560 |
| b26b88f4fa369186bd21 | [audit/check_actual_insertion.py](original/research/workspaces/customer-attraction/R-4ffa8b85fa8847e09e45dcafc8e1326f/audit/check_actual_insertion.py) | 2334 |
| 440038e60ef2ce97de04 | [audit/minimum_spe_value_embedding_counterexample.md](original/research/workspaces/customer-attraction/R-4ffa8b85fa8847e09e45dcafc8e1326f/audit/minimum_spe_value_embedding_counterexample.md) | 2936 |
| cedc58eaa6a32798951e | [audit/virtual_replay_independent_exact.json](original/research/workspaces/customer-attraction/R-4ffa8b85fa8847e09e45dcafc8e1326f/audit/virtual_replay_independent_exact.json) | 24764 |
| f357042dedd0f3c96a68 | [audit/virtual_replay_independent_review.md](original/research/workspaces/customer-attraction/R-4ffa8b85fa8847e09e45dcafc8e1326f/audit/virtual_replay_independent_review.md) | 10066 |
| 59d7df32374cf7cca518 | [deletion/README.md](original/research/workspaces/customer-attraction/R-4ffa8b85fa8847e09e45dcafc8e1326f/deletion/README.md) | 1643 |
| 4ba06d7faddf010e16f1 | [deletion/audit_virtual_replay.py](original/research/workspaces/customer-attraction/R-4ffa8b85fa8847e09e45dcafc8e1326f/deletion/audit_virtual_replay.py) | 5913 |
| bb478c8b91eace29e2d3 | [deletion/cartesian_terminal_obstruction.md](original/research/workspaces/customer-attraction/R-4ffa8b85fa8847e09e45dcafc8e1326f/deletion/cartesian_terminal_obstruction.md) | 3787 |
| 1935d482c0d069739aa7 | [deletion/virtual_replay_audit.json](original/research/workspaces/customer-attraction/R-4ffa8b85fa8847e09e45dcafc8e1326f/deletion/virtual_replay_audit.json) | 1413 |
| 9e7c0fa9b487c2ed4e52 | [deletion/virtual_replay_regret.md](original/research/workspaces/customer-attraction/R-4ffa8b85fa8847e09e45dcafc8e1326f/deletion/virtual_replay_regret.md) | 9353 |

## 本次真实运行及字节对比

两套代码只依赖标准库Fraction/itertools/json/pathlib。分别复制到新的replay/author及replay/independent目录，各以普通Python3.12.14 `-I -B`运行一次；无-O，assert开启，exit0、stderr空。运行的源码副本与冻结源码SHA一致。author只打印JSON；independent会在脚本旁写JSON，所以隔离目录是必要保护。

[run-record.json](replay/run-record.json)保真实绝对cmd/cwd、耗时、Python、原码/报告SHA及运行次数。author [stdout](replay/author/stdout.json)1413B逐字节同冻结作者JSON；independent [输出](replay/independent/virtual_replay_independent_exact.json)24764B逐字节同冻结独立JSON，另保真实[stdout](replay/independent/stdout.json)与两份空stderr。独立stdout输出路径属于本次隔离目录，不冒称取得旧stdout。代码副本[author](replay/author/audit_virtual_replay.py)、[independent](replay/independent/audit_virtual_replay_independent.py)可直接用普通Python在新副本目录复现，不在original中运行。

作者7case的506/6086含self历史比较、独立6case的252/1968比较/984规定后缀/126删位集均按代码真实域解释；全部输出字段和删位行已实读。没有SPE oracle、LP或随机搜索参与两套原审计。正背景/空主题/零客户不在两套有限输入中，普遍式由正文证明承担。

2334B check_actual_insertion.py已全文理解原样保留，本次执行0。它的六查询浮点发现及有理打印既不是精确对偶，也没有assert拒绝负min_ic；候选已被旧完整SPE反驳，未追加阴性扩样或补造缺失的旧stdout。

## 版本与比较

独审记录被审稿SHA e8f17651f7630e7f8731539cba836de96ea3d60ee5c3b8ac4ee964e0abb26d88；冻结最终作者稿SHA 5bbf42627342b30cac93b5f87617faf92d721895afdd2b3852002f6ea30b8f6f，两者不混。最终稿已吸收q≥1锐性、q0端点、P_L cap较弱/冗余等澄清；旧快照字节未取得，未造编辑事件或最终版本盲审。

[related-materials.json](related-materials.json)保本批全文比较的14个现行正文路径及本次观察SHA，包括原主引理、R4ffa根账本、正背景守恒、单删界、缩尾、硬删信用、真实修复差、残余/额外查询反例及Cartesian边界。它记录现行正文比较，不冒认其原源再次完整清洗或其既有运行在本批重复发生。源审查分别解释每项数学用途和未付量。

本批仅写独立新对象及证据，不改共享既有正文、原源、清单或图，不进行Git写/认领/done。三个新对象的关系已作文字判断：精化依既有因果回放及退款IC；两原程序为有限实现检查；Cartesian G差说明从原回放重选时额外付款义务；已知反例复用现有稳定身份。第三阶段超图不得将这些来源/实现联系误作half推导。
