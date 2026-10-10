# 七极大目录的来源证明 checkpoint：范围与现行重构状态

2026-10-10。`CA-SEVEN-MAXIMA-N7-PLUS` 的**完整来源证明及独立审查**已经保存：
恰七个不同包含极大覆盖、任意n≥7、任意内部子主题、每个完整历史依赖纯SPE满足U≤2W。
此时OPT_n=U。现行本页是依赖和资产说明，**没有重写来源的全部系数分支**；登记分别保留
“来源完整”和“现行依赖概述”两轴，不把来源已有完整证明误称为只有候选。

## 数学依赖及证明范围

唯一模型是 [CAG-MODEL](model.md)。末位行动必为满极大覆盖：在固定真实前缀下，严格
超集保留原客户每份收益并新增严格正收益，且没有后继反应。早期子主题不作此假定。

来源以 [CA-DYNAMIC-MAXIMA-MIXED](dynamic_maxima_bound.md) 的完整历史混合保底、
真实末位相对七极大主题的BR及 [CA-TWO-REMAINING-TAX](two_remaining_tax.md) 的恰两人税
为联合前提，保留每客户的极大关联和真实行动会员。n=7,8为完整literal列的有理恒等式；
n=9,…,12为988个完整压缩列；n≥13由保底解析下界和全部余项case的符号论证完成。
审查独立重建所有合法slack及解析尾部，不能将有限n扫描当成无穷证明。

完整论证见[原始来源全文](../../../history/source/notes/customer_attraction/seven_maxima_checkpoint_2026-10-10/seven_plus_source.md)，
其中“审查待完成”是保存原文的历史状态；[后续独立审查](../../../evidence/runs/2026-10-10/customer_attraction_seven_checkpoint_review.md)
已通过，确认24,384个literal列、988个压缩列及n≥13完整解析分支。
无外部同行评审及全球新颖性认证。这里没有调用已否定的根总税或逐人安全桥。

## 小人数不能补齐的范围

一般n≤4已有半覆盖；至多六极大任意人数已有完整现行证明。
**恰七极大n=5,6仍未由这批来源闭合**：n5现有347/363个route/比较组合轨道，缺16；
n6现有833/877，缺44。已完成部分共2,059,186项客户不等式经过独立精确重放。
它们不能替代缺失轨道，也不证明继续搜索必然成功。

## 冻结资产及复验

[压缩checkpoint](../../../evidence/certificates/customer_attraction/seven_maxima_partial_checkpoint.tar.gz)
保留347棵n5完整席位树、n6直接证书清单及唯一完成树、来源全文、作者审计和两份独立审计。
[清单及SHA256](../../../evidence/runs/2026-10-10/customer_attraction_seven_checkpoint_manifest.json)
逐文件记录原始内容。[小人数缺口与全部已有重放](../../../evidence/runs/2026-10-10/customer_attraction_seven_partial_seats.json)
单独保存，避免将缺失项算成通过。

在新的空目录解压后，原相对目录保持一致，可运行

```sh
python3 general_joint_analytic/seven_tail_audit.py
python3 seven_checkpoint_review/independent_seven_plus.py
python3 seven_checkpoint_review/independent_seat_assets.py
```

后两脚本是保留原字节的来源审计，会在解压目录写报告；它们不是规范实现。
不要直接在冻结仓库证据目录重跑覆盖原文件。

该checkpoint不影响[两个一般目录攻坚任务](../../questions/customer_attraction_general_handoff.md)：
任意极大主题数、任意人数的一般猜想和聚合安全值桥仍开放。
