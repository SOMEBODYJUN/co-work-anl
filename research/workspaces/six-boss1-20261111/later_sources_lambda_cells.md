# 后部源λ全窗口：24个完整域与550条完整行

Boss1；研究标识 `six-boss1-20261111`。源3、4、5；`q₀∈{1/6,1/5}`；`λ∈[0,25]`。**0优化器、0全局LP数据或候选点读取**，未加入3056计划。

## 承重结果

- Main的三个低段猜想全部成立：第三源[0,9]每个q₀恰5facet、5顶点；第四源[0,4]恰3facet、3顶点；第五源[0,1]恰2端点。
- 全部24个闭窗口域共96facet、110次顶点窗口出现，带来源与q₀去重后74组参数。372真实ρ原态、440原约束、322比例组全部保留。
- 全部550条raw、每条513列：440条八目标通用行、55条C-only、55条ordered。精确重复、零列、旧参数和边界重复均保留；364个不同向量仅作审计计数。
- 第五源低λ不能套W>Z；从真成本所得严格凹二次仍证明d=1是整个连续域唯一最弱正重数。
- 六个[16,25]域与旧族经`s=25−λ`具有准确面、顶点及列身份。本窗口190条raw，加相邻窗口λ16重复70条，共260次旧参数出现的133380列身份全为零差；不重复认领旧族。

## 核验与文件

两种独立几何算法一致；独立字面checker不导入生成器或项目Python。5252张物理最小表、27144真实尾成本、6591弱平局达到态、77568实际内五均值和全部282150行列系数均PASS。

主证明见 [proof.md](later_sources_lambda_cells/proof.md)；全部几何见 [geometry.md](later_sources_lambda_cells/geometry.md) 与 [endpoint_table.md](later_sources_lambda_cells/endpoint_table.md)。完整输入、原态、完整行与检查结果分别为 [inputs.json](later_sources_lambda_cells/inputs.json)、[state_halfspaces.json](later_sources_lambda_cells/state_halfspaces.json)、[exact_family.json](later_sources_lambda_cells/exact_family.json)、[literal_checker_output.json](later_sources_lambda_cells/literal_checker_output.json)。冻结身份见 `later_sources_lambda_cells/freeze_manifest.json` 与 `later_sources_lambda_cells/SHA256SUMS`。

适用原共同有限标签目录、全部有序历史纯SPE，允许空覆盖、重复与别名、所有弱平局及零客户。只完成指定真实锚族；未给出新全局最优值或SPE实现，六人half问题仍为OPEN。
