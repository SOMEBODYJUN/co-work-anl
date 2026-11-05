# 数学关系图：registry 到可读取超边

第三阶段只读取2.5第三步已经推送并通过登记验收的`research/registry.json`。旧`graph.json`、旧Markdown manifest和`maps.py`原型不作为新阶段输入。图是研究导航和按需取上下文的入口，不是数学真值来源。

## 写入边界

每个Boss先领取一个`map/tasks/<task-id>.json`，任务定义固定对象ID、版本pin和写入路径。对象范围或写入范围重叠时不能同时claim。Boss只写自己的`map/edges/`和`map/receipts/`，不直接改canonical registry或全仓graph。

```sh
python work.py map plan --record-file map/planned-tasks.json
python work.py map list
python work.py map claim <task-id>
python work.py research edge-check map/edges/<edge-id>.json
python work.py checkpoint map/edges/<edge-id>.json map/receipts/<task-id>.json -m 'Publish explained hyperedge and coverage'
python work.py map done <task-id> --receipt-file map/receipts/<task-id>.json
python work.py map status
```

`map plan`会先把任务板checkpoint并尝试推送；只有远端确认`pushed`，其他Boss才应claim。claim、done、handoff使用远端快照和稳定request_id，丢回执时先读远端，不重复创建请求。认证失败保留本地草稿，不反复消耗同一失效凭据。

## 超边契约

联合前提必须保留为一条`premises_mode: all`超边。端点、条件、解释和证据都要写清，目录相邻、同名、共有输入或引用关系不能自动变成推导。

- `source_ids`、`target_ids`：registry中的稳定对象ID。
- `kind`：逻辑关系为`implies/refutes/specializes/transfers/equivalent_to`；语境关系为`motivates/cites/sourced_from/implements/checks/corrects/supersedes`。
- `relation_mode`：逻辑关系使用`unconditional`或`conditional`；语境关系使用`context`。
- `roles`：每个端点在这条关系中的数学作用。
- `conditions`、`explanation`、`scope`：共同前提、推理范围和适用域。
- `evidence`：正文、证明、反例或有数学owner的计算证据。
- `accepted`边还必须有`reviewed_by`、`review_note`以及当前`endpoint_pins`、`evidence_pins`、`review_digest`。

`research edge-check`在canonical `registry.edge_files`仍为空时也能验证交付边；`map done`会再次验证任务回执中的边，并把本批已交付边临时纳入coverage检查。因此3A/3B/3C处理者无需提前修改registry，3D集成人才把已接受边加入canonical表。

## 分层与收尾

3A处理同一对象族，3B处理同一存档的跨批关系，3C只处理有明确模型映射和条件保真的跨档关系，3D由一位集成人生成`map/coverage.json`、`map/integration.json`和派生`graph-v2.json`。没有关系的对象可以保持`isolated-after-review`，不为增加连通性硬造边；`needs-decision`不能进入最终闭合。

边、coverage和回执先推送，再`done`。最终运行：

```sh
python work.py research check --final
python work.py research build --final
```

最终图只表示已比较的范围。研究Main使用`research search/show/context`按需读取正文和完整超边；图中没有某条路线不代表数学上不可能。
