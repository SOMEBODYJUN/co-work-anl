# 范围、来源与冻结前审查

实际执行 agent：`/root/source1_lambda_complete`。独立解析审查 agent：`/root/source1_lambda_complete/root_lambda_review`。

四份最初指定正文已经首尾完整阅读：`all_source_minimal_cap_safe/proof.md`、`ordered_minimal_cap/proof.md`、`source2_lambda_anchor_complete/proof.md`、`later_sources_lambda_cells/proof.md`。另完整阅读共同目录完整历史模型。为做可复查的域、顶点、行系数身份，只读取固定旧局部包中的域、参数族、行目录和 exact_family 文件；所有12个实际读取来源由 `source_pins.json` 固定SHA256，生成器及独立检查器都在首末核对不变。

最初任务要求完整新raw矩阵；确认根λ域与旧根域完全相同后，Main明确缩小输出范围为完整映射与无新增行证书，并要求不物化900条重复raw。本包遵循该更新：`old_row_correspondence.json`只是900个原行／自由等式表示的来源记录，不是900×513重复矩阵。全部513列的符号身份仍完整保存。

数学推导从真实成本重建，依次证明零尾最小帽、全中间根锚、全32态、19面、连续ordered投影，再比较旧域。独立检查器不导入生成器或任何项目Python模块；以不同的逐份额成本实现和全五面交点枚举检查全部结论。独立解析审查另从32态分解及单面构造证明全部facet，无需优化器或顶点结论。

全程没有调用优化器，没有读取任何全局LP输入、数值候选或最优面文件，也没有修改Git、RUN、registry或其他目录。一次为了寻找空闲审查槽的 `list_agents` 元数据请求自动附带了另一已完成任务的摘要；该摘要并非本席请求的数学来源，已隔离，未复制其中数值、未访问对应文件、未用于推导或判断。本包“零全局文件读取”的声明不扩大解释为该工具从未展示过无关摘要。

本包可以准确声称：两域、全顶点、全部必要面和所有行身份已核验；它不能据此声称新增全局界、完整SPE实现、任意钱包最优性或half结论。限定结论是研究范围λ∈[0,25]下的准确重参数化闭合，新增不等式信息为零。
