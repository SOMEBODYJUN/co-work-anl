# aff821168f7ae8b335a0 元数据清洗记录

## 冻结源

- source id: `aff821168f7ae8b335a0`
- frozen path: `research/workspaces/customer-attraction/R-373daba10913464c93771a808d88fce3/workspace.json`
- source SHA-256: `1125fdec81fef01d9321a7bf6539b8af88bde7c81183965d1755314da5b74701`
- exact payload size: 150 bytes; JSON schema 1

## 实际读取与语义

源文件只有四个元数据字段：`schema=1`、`save=customer-attraction`、`actor=R-373daba10913464c93771a808d88fce3`、`instance=79cefb89a2254f2cb010c1acd68f51bb`。它不包含收益、策略、客户目录、终局、证明、实验输出或参数。因此它不能单独支撑任何数学命题，也不能替代同一工作区中 `root_menu` 与 `root_review` 的实际源文件。

全仓比较显示该工作区下已有清洗对象与证据：根菜单有限探针、固定策略锥/桥审查、R-373d 安全/报告/credible2/coupling 等证据，且其数学源已由对应 source IDs 单独登记。当前源的唯一内容是把工作区绑定到 customer-attraction、记录历史 actor 与 instance UUID，便于溯源和重现上下文；不应复制成新的正式数学对象或把身份字段解释为结果。

## 建议处置

建议 `retained`：保留作为工作区 provenance 资源，目标放在 `archives/customer-attraction/tools/evidence/` 下的 R-373d provenance manifest（或在已有 R-373d 证据 manifest 中增加该 JSON 的 hash/path）。不建议 `integrated` 到 `state/`，因为没有数学承重内容；不建议 `duplicate`，因为这条源在冻结清单中是独立的元数据版本，不能与任何数学 JSON 合并替代。若协调者决定不保留工作区身份元数据，可退为 `retired`，理由必须明确“无数学内容且正式对象/证据已由同目录源独立保全”，不能写成未读。

## 接续边界

后续清洗应沿 `R-373d.../root_menu`、`root_review` 的实际 JSON/脚本继续，保持固定策略锥有限证书、审查和完整六人 Q-CAG-HALF 目标的量词分离；本元数据源不增加任何定理、反例或证据边。
