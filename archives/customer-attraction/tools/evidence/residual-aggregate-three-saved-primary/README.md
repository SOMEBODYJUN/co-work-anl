# 合法背景残余全集探针、三保存点与根锥导入版本

五主源共12712B，逐文件核size/SHA256后全文实读。原件在original/，完整冻结定位见[source-manifest.json](source-manifest.json)。两冻结提交同字节，不计双运行。本包不含凭据，不执行Git或work.py写事务。

正式数学去向：

- [合法背景残余总利润的全集筛查与三个重复终局点](../../../state/程序/合法背景残余总利润的全集筛查与三个重复终局点--程序.md)：4708B探针及945/1552/1555B三JSON，全部终局集合、最小剩余利润、输出版本差、三个精确取等点和新完整策略。
- [两步安全链根锥程序的依赖导入版本](../../../state/资源/两步安全链根锥程序的依赖导入版本--资源.md)：3952B R642版，与已充分整理4040B R-d51后继只有一条sys.path插入差，数学按既有正文去重。

## 一次新数学事件

[audit_three_saved_points.py](audit_three_saved_points.py)只用标准库和三个原JSON，从定义重建整数收益、集合值递推、完整有序策略及全部真实IC，再以Fraction核315个静态背景的纯查询下界/纯对手上界。原main/import/随机/LP调用均0；一次成功运行exit0，见[事件登记](execution-register.json)与[stdout](audit.stdout)。没有为补日志再次执行。

[精确总报告](exact-three-saved-point-audit.json)含全部非零客户类型、原字段列表、源SHA、状态/终局数、标签别名、新策略SHA、全IC数量和精确安全证书。三份完整动作表和静态矩阵如下，动作表明确是本批新恢复，不伪称原文件曾保存：

| r | 新完整策略 | 全静态收益矩阵 | 精确v / P |
|---:|---|---|---|
|3|[43节点](new-complete-policy-r3.json)|[21行](exact-static-matrix-r3.json)|63/10 / 189/10|
|4|[400节点](new-complete-policy-r4.json)|[84行](exact-static-matrix-r4.json)|32/3 / 128/3|
|5|[2801节点](new-complete-policy-r5.json)|[210行](exact-static-matrix-r5.json)|53/6 / 265/6|

三者均P−rv=0、根终局计数唯一；额外严格纯鞍点条件证明完整恒动作SPE唯一，非单凭根集合数。r3的同覆盖标签2/3保全。它们是总人数六的**非空合法前缀子博弈**；未给过去玩家激励、完整六人根策略或六人half结论。

## 同SHA复用、版本比较与关系

[依赖及复用绑定](dependency-and-reuse-bindings.json)逐项核既有已保存helper22102B、patterns6608B及压缩策略库552002B的SHA和size。本批完整重读前两源码，库数学和全策略字面阅读复用既有充分处理的同SHA证据，不再调用Space/full_policy/共同Q/扫描。4708B probe在旧PAIR包的related副本亦逐字同SHA；旧包的related-only身份不冒成此源先前完成。

[根锥唯一导入diff](root-cone-import-only.diff)保3952→4040B的唯一差。后继1900记录不属于本源；本批无3952B成功导入或原LP结果的新声称。源码、候选、输入库与运行报告分别绑定。

[只读比较及关系记录](comparison-and-relations.md)由内部辅助Solver在新审计前给出，核原字段版本、别名、全部D_j有理值、已有纯鞍点式(6)—(8)去重及PAIR/DR/原六人目标边界；是知情只读检查，不称盲审或外审。正式对象内解释关系，第三阶段不提前造图。

逐源receipt草稿在本批staging根receipts.json；只有父Boss串行checkpoint并确认pushed后才能done。本包的存在或静态检查不表示已推送、已勾选或全仓结束。
