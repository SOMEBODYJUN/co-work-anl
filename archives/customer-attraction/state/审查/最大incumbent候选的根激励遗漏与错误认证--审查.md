---
id: customer-attraction/largest-incumbent-candidate-omitted-root-IC-and-false-verification
kind: review
type_tag: 审查
title: 最大incumbent候选的根激励遗漏与错误认证
status: 旧候选非SPE；Root新定义核验明确五个根严格偏离；旧冻结字节保留
source_refs:
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/credible_search/README.md
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/credible_search/audit_old_largest_incumbent.py
---

# 最大incumbent候选的根激励遗漏与错误认证

本审查处理已有正式页将R18三人六主题best JSON误称“完整SPE反例”的实质冲突。直接依据本批主源可信搜索README的后续纠错，Root又完整实读原5707B输入、5627B生成器、三篇旧正式页，另按单位客户定义独立一次核验。被质疑的已done原源不重done；本批处置的是明确后续审计主稿，原冻结输入和过去回执不改。

## 同一精确输入而非标签相近

源JSON SHA256为7dcd445bdfe275e7b0521945ad4242aea3f3401dc0df848fb01c5bcb2fcfcbbd。主题0…5，以下11兴趣类型重数展开为不同单位客户，共963：

| 类型 | 数量 |
|---|---:|
| 1 | 208 |
| 3 | 154 |
| 1,4 | 5 |
| 0,1,2,4 | 36 |
| 3,4 | 17 |
| 0,3,4 | 168 |
| 2,5 | 190 |
| 0,3,5 | 36 |
| 2,4,5 | 14 |
| 0,2,4,5 | 27 |
| 0,1,2,4,5 | 108 |

JSON确实保存43有序节点完整动作表，但**完整定义一份形式策略不等于完整SPE**。根规定0；按其原全部动作继续，强制根各主题得到：

| 根行动 | 同一原策略真实叶 | 根收益 | 相对原收益的严格增益 |
|---:|---|---:|---:|
| 0 | 0,2,3 | 375/2 | 0 |
| 1 | 1,3,5 | 303 | 231/2 |
| 2 | 2,3,1 | 303 | 231/2 |
| 3 | 3,1,5 | 357 | 339/2 |
| 4 | 4,3,2 | 190 | 5/2 |
| 5 | 5,3,1 | 303 | 231/2 |

每叶及收益可由11类型直接均分复算。五个根替代均严格更好，最小也赚5/2，故该形式策略不是SPE，不能反个体OPT/(2m−1)桥。实际023收益(375/2,579/2,273)、W750；最优963由123或135达到（各排列皆可），实际023并未覆盖全部963。旧页同时写“023覆盖全部”及W750是另一个错误，不能用OPT963冒实际覆盖。

形式策略上的算术OPT/u0=642/125>5及2W−OPT537保真，但缺SPE前提时不构成所称桥反例。一般个体桥后来由[真实银行族](../反例/笛卡尔银行完整根菜单的低值自洽分布失败--反例.md)独立否定，不因此回填本候选有效。该候选的half算术余量正，也不认证一般half。

## 生成器的准确失败机制

原5627B largest_incumbent_probe.py SHA24ef0170b318beb6411bbeec2f988c38bdf57443fc48a361edeac464f97a16b0：先允许原R[0]外目标进入根候选、将root floor设极低，再自行重建约束时明确`if not h: continue`，删去所有根IC，只留42个后继节点的真实比较并加“根主题最大大小”的容量行。

有理recover确会逐行核传入G，但G本来没有根行，所以它只能认证此松弛锥。`verify_canonical`虽被import，全文没有调用；proof字典直接硬编码`verified:True`。旧正式描述“调用verify_canonical”不能成立，JSON的字段不是定义级全树验证。没有把错误归因于LP浮点容差或某个标签映射；是认证义务被删。

本候选其余42历史的全部非自身比较确非负，而根五行负，恰吻合遗漏范围。最大主题/有理重构/全部孩子SPE都不能替代根最优性。生成器其它有限输出仍可保为松弛锥记录，但每一份若要称完整SPE必须另外按全有序定义核。

## 本次真实新验证及原历史分开

Root自写标准库Fraction入口，仅读上述同SHA原JSON，展开963不同单位客户和全部43策略键。一次运行核258含自身/215非自身真实比较，且枚举216终局覆盖；完整有理输出76161B，发现上述恰五根偏离，最大覆盖963、最优无序支持123/135。exit0、stderr空，0.293秒；[源码/完整输出/执行SHA](../../tools/evidence/cyclic-extension-terminal-support-and-root-audit-primary/new-root-definition-check/)保原捕获。不导入作者或规范validator、SPE solver、LP/MILP，不重跑原审计或过去成功有限搜索。

它是针对新发现实质矛盾的必要定义重构，不为了增加运行次数重复扫描妥善已处置来源。原可信搜索稿称audit_old_largest_incumbent及JSON已完成215非自身审计，是原历史内部声明；本次独立代码和它身份分开，无外审/新颖性认证。

本十源清洗再以 `run/old_largest_incumbent_recheck.py` 运行同一单位客户/Fraction 逻辑：exit=0、stderr 为空，重得五个且仅五个根盈利偏离，输入 SHA 与冻结值一致。该运行只复核已有归档 JSON，不把 `verified:true` 恢复为 SPE 认证。

三篇旧正式页的当前更正保原稳定ID/路径、原历史运行及冻结证据，只撤回错误SPE/桥认证并指向本审查；Root留完整before/proposed/after及精确SHA，不改旧progress ownership/disposition。可接续任务是用根行完整的固定策略锥或真实可实现菜单，不能让`verified:true`跨越缺失假设。
