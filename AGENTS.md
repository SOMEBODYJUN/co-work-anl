# 仓库工作规则

本树只服务当前数学研究。旧 2.5.3、第三阶段批次、公屏、清点台账、阶段身份和派生验收已删除；不得重新创建这些路由，也不得把它们当作研究前置条件。

## 研究入口

- `work.py start` 绑定明确的 Boss 身份和研究存档。
- `research studio` 保存 Main、独立障碍线、idea 和执行线的 RUN、journal、反馈、冻结和回流记录。
- `research search/show/context/frontier` 读取现有对象、完整超边、替代路线和未付义务。
- `research check/build` 做当前 registry、证据和超边的结构核对与投影构建。
- `checkpoint` 保存指定研究资产；任何成熟结果都要在准确版本上复核后再回流。

研究结果必须说明模型、定义域、量词、假设、证据、实际得到的结论和剩余义务。联合超边的全部前提必须共同满足；独立证明保留为替代分支；开放等价、局部贡献和有限计算不能自动升级为一般定理。

Main 看超边和简短回执，负责路线选择、派工和发布。idea 子代理提方案。执行与复核子代理实读正文和证据、完成证明与计算。接近上下文上限时，先保存精确断点，再派 fresh 子代理按原引用接续。

## 论文评价（用户要求时执行）

先运行 `python work.py research evaluate --paper <稿件路径>`，按生成的 TASK 做完证据审查，再用 `--run <ID> --report <完成的评审JSON>` 出报告。需要时传 `--include` 和 `--target-file`。详细用法见 [论文评价](tools/PAPER_EVALUATION.md)。评审草稿留在本地；评价不改变研究 RUN 或数学登记。

## 文件边界

正式数学在 `archives/`；必要复现输入、程序和证书在 `tools/evidence/` 或 `tools/evidence/canonical/`；唯一当前登记是 `research/registry.json`；正式超边在 `map/edges/`。阶段证据迁移后只能引用新的 canonical 路径，不能保留旧阶段路径或悬空 SHA。

个人未完成研究可以保存到 `archives/<问题>/workspaces/<Boss>/`，连续 RUN 状态在 `research/runs/`。失败和开放问题照实保存，不为填表制造节点、边或公屏消息。
