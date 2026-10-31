# Workspace metadata routing evidence

本证据包保存三份 workspace.json 的当前 clean 原字节，并把它们与对应工作区 README、现有正式对象和证据快照作了交叉核对。三份文件均为 schema 1 的索引元数据，字段只有 `save`、历史 `actor` 和 `instance`；它们不含客户表、策略、收益、IC 行、证明或实验结果。

| clean id | source | bytes | SHA-256 | 去向 |
|---|---|---:|---|---|
| `82bf513eb80edf079678` | R-275 workspace.json | 150 | `5f3ef1fcb42f0625a7b6343084b8c2f1036ce6df70effbae16f908b9a1bf47f6` | 保留索引字段并并入 R275 资源 |
| `07bd57dc0f2e89f6b8e9` | R-29 workspace.json | 150 | `8c13a2d811c350a0cbc865e18e4c82bcca8aa80e457c421fba87a7cfe189e4bd` | 保留索引字段并并入 R29 资源 |
| `2f8f17cb30bb679f82c3` | R-2d91 workspace.json | 150 | `7100f5130bd9248df5703b9f062bf64cb5e5c33215896267bb6a237c3b686b22` | 保留索引字段并并入 R2d91 资源 |

R-275 对照已保存的工作区 README 和 R275 的直接全局、树耦合、共同查询及安全证据；README 给出研究存档、历史发布身份和一般 Q-CAG-HALF 仍开放的导航，数学内容在各正式对象中。R-29 对照固定背景尾局、直接门槛资源和既有 R29 正式对象；README 的身份与目录信息不增加尾桥或 floor 结论。R-2d91 对照首次饱和版本路由、自然捕获资源、stationary 反例及安全证据；README/metadata 只承担工作区身份和恢复路由。

三源没有新的数学对象。证据副本只用于稳定 provenance；不得把 actor/instance 字段误读成数学作者、模型参数或证明结果。
