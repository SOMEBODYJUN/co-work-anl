# 完整可见最大标签联合必要系统 v6：4177×513，冻结准备完成

Boss1；RUN `six-boss1-20261111`；实际 agent ID `/root/visible_joint_v6_prepare`。

**已按Main指定顺序装配全部4177条原尺度必要不等式，独立检查PASS，0优化器。**
保留全部513个非负列、原覆盖目标及两个自由等式；未读候选点或最优面，未创建或消费LP release。
全局O取达到OPT6的最优六标签覆盖并；OPT6>0时按OPT6归一化，零OPT6实例直接处理。新增局部族对任意六查询并成立，在此特化到该最优O。

## 输入组成

| raw闭区间 | 来源 | 行数 | 数值除数 |
|---|---|---:|---|
| 0–3055 | 冻结v5全部原对象literal | 3056 | 旧3056字符串literal |
| 3056–3285 | 第二源λ窗口全部来源 | 230 | 25 |
| 3286–3445 | 第二源λ完整锚域全部来源 | 160 | 25 |
| 3446–3995 | 后部源λ全部闭窗口出现 | 550 | 25 |
| 3996–4175 | 第二源δ六切片全部端点 | 180 | 25 |
| 4176 | Main根严格C外部余项行 | 1 | 1 |

两份第二源λ来源都保留；没有按重复向量、凸生成关系、窗口重合或零型筛选。
δ独立helper的3条ordered ε行和150条仿射段不属于既定180个端点原行，未混入端点块。
父raw868保留，最后根行另加 `−ηc(1−o)`，其K系数不变。

## 数学和schema关键点

已全文实读三份λ证明、δ完整证明和原模型。λ包真实源IC权为 `λ+Στ`；δ包为 `25+τ4+τ5−s`；数值除数25不是该权。
λ的C-only加 `B E_C`，K=1；δ的C-only加 `(S−s/5)E_C`，K=s/5。
每个有符号等式及独立K列都另行检查。

列表源的第k项无损映到 `a[str(k)]`，字典源原键和原字符串保留。
原ID、源内索引、全部非系数metadata及原catalog条目全部保存；新λ/δ全局name采用 `package::原id`，解决两份第二源λ包的原名重合，未改动原id。
Main根行保持整个原对象literal。

## 独立核验

检查器只导入标准库，不导入builder或任何项目模块。它从真实个人份额、所有真实尾态及全部ordered重数重建来源列。

| 检查 | 准确数量 |
|---|---:|
| 原系统literal行 | 3056 |
| 新增合法来源列 | 575073 |
| 整个系统逐行完整列位置 | 2142801 |
| 新C有符号等式列 | 55917 |
| 根行与旧raw868完整差分列 | 513 |
| 独立真实尾成本 | 42824 |
| 独立条件最小值 | 4052 |
| 全部并列最小尾出现 | 5591 |
| 旧真实IC/K元数据行 | 2006 |
| 旧ordered客户列重建 | 162816 |
| 两个自由等式列 | 1026 |
| 覆盖目标列 | 513 |

全部30条rhs=−1保留。输出后诊断：恒零原行1条，
不同仿射向量（含零）3457个，
重复出现720次；这些统计不用于删行。
源文件的44个固定SHA在首尾和冻结前均一致。

一次checker接口失败是两份λ的ordered原catalog不含target；已按实际schema修正，并保留失败脚本和记录。
其他只读接口探针或被否决的辅助假设也完整记在failure_log中；未修改来源数学或冻结原包。
冻结前另补明全局最优O与局部任意查询并的语义，并保留更正前已成功的装配/检查记录；原系数对象未变。

## 工件和身份

- [完整原尺度输入](visible_maximum_joint_v6/exact_input.json)
- [行目录](visible_maximum_joint_v6/row_catalog.json)及[逐行来源](visible_maximum_joint_v6/provenance.json)
- [模型合同](visible_maximum_joint_v6/model_contract.json)、[来源核读](visible_maximum_joint_v6/source_review.md)及[全部列路由](visible_maximum_joint_v6/column_routing.json)
- [独立检查](visible_maximum_joint_v6/independent_check_result.json)及[全部raw行检查](visible_maximum_joint_v6/all_raw_row_checks.json)
- [来源pins](visible_maximum_joint_v6/source_pins.json)、[冻结manifest](visible_maximum_joint_v6/freeze_manifest.json)及[SHA256SUMS](visible_maximum_joint_v6/SHA256SUMS)

`exact_input.json` SHA256：

```text
8f953bca6b65a8093d5fcf0fdb5a432ba3603137fe1015cd06fc8f6324e68769
```

本包是普遍必要系统的完整输入准备，不是SPE实现证书，没有新优化值，六人half状态仍OPEN。
已冻结并停止写入；交Main对这份准确输入作完整复核。
