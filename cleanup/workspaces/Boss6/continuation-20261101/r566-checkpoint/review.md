# R5662 checkpoint三源完整复核

本次结论：三源均可按`retained`完成。现有正式资源没有遗漏三份原JSON的承重字段，也没有把历史复放、依赖封包检查或必要系统可行点升级为完整SPE。现回执的事实判断成立；本目录`receipts.json`把原来泛称“相关比较”的文字改为实际完成的逐项核验，不改变原来源、正式对象身份或数学状态。

## 实读范围与原件身份

先实读根`AGENTS.md`、`cleanup/OBJECTS.md`、现有三源回执及正式资源全文，再逐项读取manifest的全部174个(path,SHA256,bytes)、scope、snapshot_commit、note；verification的全部7项checks、curation_dependency_check、peer_author_replays及OPEN字段；potential replay的全部16个顶层字段、六项实际收益、十八项argmax和十八项倒二support slack。三源总字节46548B。

三份工作区冻结原件与正式`r566-checkpoint-metadata-primary/original/`原件均逐字节相同，SHA256/size全部符合`continuation-20261101/sources.json`；正式source-manifest的id/blob/mode/path/SHA/size/双冻结sources和preserved_path也全部准确。详细新检查见[verification.json](verification.json)，可复现入口为[verify_metadata.py](verify_metadata.py)。这个程序只核元数据、转写、既有输出同字段和小量标量代数。

|源ID|文件|字节|SHA256|
|---|---|---:|---|
|3913485fc9b9d5810df5|checkpoint_manifest.json|42960|492401cc235b536f42400195a3195a4dd9711bc0d3f89ce11eba2c58a1feedec|
|c6b117b9e8fd491d2d98|checkpoint_verification.json|2027|2b6dd05ab524e7994f80332bef3225db40e89605e2ebf52ae87662d46f250629|
|e68ceb56e0eb937c4162|potential_menu_replay.json|1561|80f886aa0aa4a7e8a7b610272ba7483a4056141c6accf2459d6684660f509f89|

## 174项逐版本结果

从`cleanup/inventory.jsonl`独立重建全部174条比较，而非信任既有comparison的结论。全部路径互异，声明总大小17810557B；172条在冻结inventory中有相同path/SHA256/size，2条同路径另版，0条路径完全缺失。独立重建的174条(path,manifest_sha256,manifest_bytes,frozen_matching_ids,other_frozen_ids)与正式`manifest-inventory-comparison.json`逐字段一致；正式资源174行表格的序号、相对路径和声明字节也与源全数同序一致。

manifest的snapshot为`b48a7563106808df5ff95bcc0160a8dd9b864ba1`。两份入口声明的旧版不在现冻结同路径字节中，不能用现冻结入口冒充该snapshot入口：

|入口|manifest旧版字节/SHA256|现冻结同路径source ID、字节/SHA256|
|---|---|---|
|FRONTIER.md|8086 / 228ae0b1edbf4b9f8f2c01aa4884ecb46d7ef1b6305bc1ea97f5a5b911f077ed|bbe87642e2efce14d63c；9820 / 6e89b1a05e7def262dae3612a6b5bfee17763a114acb2a7f52d22f48a08f53c7|
|README.md|3221 / d57fc596b071189c7e99c2acde812beafa303f5004b1d975753297c3d4279a37|2febc458086d3c08984e；3913 / e8b0dbe0aa9f95a5836777cf55eacf9edb37fe35a840960c534d9bf57c71e30b|

[manifest-versions.tsv](manifest-versions.tsv)保存全部174条声明及冻结版本的完整SHA/size/ID；`verification.json`进一步保各版本双冻结出处。这里没有取回b48旧树、没有读174个成员的全部内容，没有将172个字节身份匹配记成172份数学已清洗。manifest不列自己，四复制后续程序也不因一份replay被列入而获得代码认证。

## 正式数学和有限evidence比较

实读正式资源全文并机械核其两个JSON代码块：分别与verification和potential replay全字段相等。继续实读以下相关正文，比较承重范围：

* `整终局势与真倒二菜单联合停界--障碍.md`全文：普通点与private点分开；普通点只有19正压缩类型、物化114类型，十八主题势和指定末位/倒二菜单通过，并不能替代倒二改A6或Ri的真实续局。普通点不通过私有席位谱，不能把另一private点性质贴给本replay。
* `四复制与末回复研究的原运行及种子身份--审查.md`全文：18主题seed的原完整BI报告与本必要点严格分开，原实际路径不能保为SPE，不把后来浮点锥值或根terminal枚举拼成本源的SPE。
* `指定四菜单补价点与旧未闭点的审查时序--审查.md`全文及`六人冻结前沿的条件谱与共享回复接续账本--资源.md`全文：5692/4849、5112/1905和5277/2033是不同点/行集；5277已知后切，5692也未含全Z/PAIR closure。verification的passed只保其所列历史作者实现复放，不填为第二套矩阵重构。
* `极小可信续局首回复前移与严格间隙--引理.md`全文：15客户、四主题、4^5=1024完整两人尾策略和五个SPE的局部语义与1/5严格间隙一致；该局部背景没有给六人坏根完整SPE。
* `七极大至多两单例块半覆盖--定理.md`的“为什么OPT6=U”至“审计脚本及证据等级”对应段：两轨各3904列、两个正余项与peer_author_replays相同，只在至多两个singleton极大主题的条件类内。前沿账本保incidence端点与mixed-singleton条件，未从peer字段推任意目录half。

另全文读取既有`potential-menu-joint/replay/audit_normal.json`、`audit_potential_menu_joint.py`和`potential_menu_joint.json`。普通audit输出2184B/SHA`cf0adfcdd698eb91cadeab684da3734c49b884889cf9af7928e2080955201946`与manifest的对应报告同版；其与父方potential replay恰有13个共享顶层字段，全部精确相同，包括全部收益、argmax和十八条support slack。普通输入4966B/SHA`abb6ad00f9944d7502136ced5dab3eb447bea4c19587e381553e47255fe68d0c`也与manifest同版。其uncertified floating dual不被当作精确LP最优证书。

现保存审计脚本5937B/SHA`245483e74f526dccfb0e0bcf5346afb0fdabd2d91a09fa7592bea3dd83becdf3`与manifest一致，确实按正质量物化18主题、遍历势、多次精确末位报价，并对每个倒二行动取末位BR集合中对倒二最坏的收益。父方replay另报执行SHA`ff1536b0667244ca05a49ab1ea76a291dba50784524921e0dd5028c4b9364ec5`。13字段数值相同不能消除代码版本差异，也不能据此声称已找回该执行版本。

小量标量复核另确认：C(23,6)=100947；argmax为18分量、和6；六实际收益和W=1；最大势减W+C为0；18个倒二余量有5正、6零、7负，负索引恰5及12—17；8338358321338500等于56723525995500×60H6，其中60H6=147，低于有符号int64上界。这些不是新势枚举、新尾策略枚举或完整SPE核验。

## 去向、资源增补与关系边界

现有正式资源及原件包已完整容纳三源独有内容；本次无需创建新的福利命题或改数学真值。`resource-addendum.md`给出可选择合并的自足增补文字，补全两个入口的新旧完整版本三元组，并说明现finite audit的13字段对应；现文不合并也不会失去原源字段。若父方采用增补，可把`verification.json`或其中逐条结果另放正式evidence；本目录只是内部交付，不在这里自行移动或认定已推送。

关系仍是来源/版本定位、实现身份和有限检查：manifest→资源定位；verification→各有限行集历史复放；potential replay→总势必要系统障碍及真实倒二缺口。资源已解释这些关系，本次没有改图；不得造“174条清单→完整证明”或“passed/相同数值→一般SPE”推导边。

本次运行一次本目录元数据/转写/标量核验器；历史入口/import、LP/BI/100947势枚举、174成员内容重审、全矩阵第二实现、外审均0。Git/work.py start/sync/claim/done、凭据读取、外发、子代理启动均0。父方负责串行整合、推送和done。
