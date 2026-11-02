# 真实配对与末偏离标记的原审计资源

本包首次primary处置5个冻结源版本，共34680B：R-6bb relay的9315B八人代码、6665B八人报告、10488B七策略报告；R-7c relay的6860B标记代码与1352B报告。原主程序/原数据均完整读取，源字节与双冻结路径保在 `source-manifest.json`。所有写入和执行先在结果clone之外隔离树完成，没有Git/远端事务、凭据访问或新策略搜索。

正式对象：

- [真实重置配对审计的七旧策略与八人二次型合同](../../../state/程序/真实重置配对审计的七旧策略与八人二次型合同--程序.md)：七例全部摘要与305项H保原报告；八人局部负pair、路径总正余量、根精确二次型最大值及其完备性证明、QD失败与OCC数值。
- [末偏离标记审计的真实行双射与多源有理总账](../../../state/程序/末偏离标记审计的真实行双射与多源有理总账--程序.md)：输入动作表身份、全部计数和有理输出、1296/1295根叶例外、指定多源与根容量的不同合同。

既有中继定理和研究账本只增“本批后续补齐两原件”的明确更新；上批0run与12缺项的历史快照不倒改，其余10件不宣称已补齐。

## 源与实际运行

| 主源ID | 原件 | 本次动作 |
|---|---|---|
| 5432547156a3d5b2aef6 | `original/5432547156a3d5b2aef6--audit_two_block_pair.json` | 全部字段、64项H、16分解保全；生成JSON逐字节一致 |
| b466d91f6834c6cb1fea | `original/b466d91f6834c6cb1fea--audit_two_block_pair.py` | 原代码一次exit0，未改字节 |
| 9ee90437901f5c68c5b1 | `original/9ee90437901f5c68c5b1--pair_reset_checks.json` | 与协作批一次原入口生成物逐字段/逐字节相同，本站不重复run |
| 8f429e7f24738e3cf4f4 | `original/8f429e7f24738e3cf4f4--audit_marked_relay.py` | 原代码一次exit0，未改字节 |
| 663eec081e2f58ae5d76 | `original/663eec081e2f58ae5d76--marked_relay_audit.json` | 与原入口stdout逐字节一致 |

`runs/two-block/event.json` 保存真实argv、cwd、exit0、耗时、Python版本、stdout/stderr大小及生成/冻结报告SHA；同目录完整保stdout2629B、stderr0B与 `generated-report.json` 6665B。源程序会写同名JSON再打印删去H/分解的摘要，二者不要混同。

`runs/marked/event.json` 保存相同运行元数据；stdout1352B等于原报告、stderr0B。该源程序只打印而不保存JSON，输入证书始终只读。

七例重放由协作的一般重置清洗包一次执行，原事件/完整stdout分别在 [replay-record.json](../real-two-query-reset-relay-primary/replay-record.json)、[replay-pair-reset.stdout.json](../real-two-query-reset-relay-primary/replay-pair-reset.stdout.json)，10488B生成JSON在 [replay-pair-reset.json](../real-two-query-reset-relay-primary/replay-pair-reset.json)。该次原调用未另重定向独立stderr，工具合并输出未见报错，故不伪造stderr文件。本站只比较其输出，不重复执行；`pair-report-comparison.json` 保相等SHA及全部字段/305H同字节结论。

## 精确依赖及可重放布局

两入口不导入规范模型或数学求解器，只依赖Python标准库。原代码相对路径有承重含义，直接在 `original/` 内运行会找错输入；复现时将代码复制到隔离根下的**冻结原相对路径**：

- `research/workspaces/customer-attraction/R-6bb0323d87294932af2aa23b47b9d4ad/relay/audit_two_block_pair.py`
- `research/workspaces/customer-attraction/R-7c3db62487a34730a704a4f2eb401556/relay/audit_marked_relay.py`

八人代码读取隔离根下 `research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/counterexample/pure_menu_two_block_dag.json`。本次零网络复用结果仓已有[原DAG](../stationary-author-audit-and-route-status-five-primary/related-original/research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/counterexample/pure_menu_two_block_dag.json)，1443260B，冻结ID eb04fc1052e27bef301f，SHA `6190bc98dedda4fb22a1af6339702c03a6cb3b04cd8dfe6b18a577782e5d2f95`，复制后核哈希相同。

标记代码读取隔离根下 `research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/direct_cover/actual_root_B_certificate.json`。本次复用结果仓既有[原动作表](../R12bf-prefix-obstruction-20261031/original/actual_root_B_certificate.json)，27302B，冻结ID e83180295536835c44f4，SHA `2c0721c062d3da02e18884e412676ff07b23f27daa0ddac6d5ad26abeeac42a4`。

各运行目录 `inputs.json` 保本次实际复制来源及哈希；`related-source-manifest.json` 保这两依赖和root_tax模型的完整冻结元数据。这里引用已经入库的精确原件，不复制另一份同SHA的大DAG，亦不把依赖的related读取冒充额外primary done。

七例的14输入、字节指纹、原相对布局和完整性检查在协作包 [manifest.json](../real-two-query-reset-relay-primary/manifest.json)、[input-contract.json](../real-two-query-reset-relay-primary/input-contract.json)。本批标记代码硬编码ROWS与其中61客户模型逐行相同，但策略文件不同：通用root_tax证书SHA `59fd58d85a3c3b989837467eb3523286d1f5ee529b0f119cd4d263bef6984111` 与actual_root_B证书只有根动作不同，仍是不同完整策略。`marked-input-contract.json` 保259唯一历史/行动范围、实际叶及终局计数、两策略唯一差异这一独立数据核查。

## 全仓比较、量词与现态

先按五主源ID、文件名和SHA检索全仓inventory/正文/旧证据，再全文比较：根RESET正确税项引理、八人笛卡尔局部障碍、整数占用与自税引理、整数占用4095标量程序合同、保留占用根账本、平稳来源分层资源、末偏离定理、首次偏离研究账本资源、61客户实际前缀障碍。与三个当批relay MD（README/working及actual_marked_relay）读取对照，精确区别一般证明、旧有限声称和本批原CLI。

- 七旧策略通过aggregate pair，只覆盖这些固定完整策略；局部缺陷字段从0初始化且比较D交叉和，不能误记为真正最大值或2u余量。
- 八人局部pair被否，根全p二次型在本输入仍严格低于u，路径聚合也通过。不是一般全p真：后续银行已否普遍根封顶，紧最大元亦否普遍高G严格导数合同。
- 八人QD失败点G<u，只否更强全p定量导数；OCC/CURRENT-GAP仍正确，折扣尾V⁺不是actual尾福利。
- 标记审计给1295非根叶/非自身行双射，源样本总账精确却没有每位置单位容量；有限PASS不支付总净债。
- 同61客户实例有两完整策略、不同根路径及W，不互换。双singleton例复用旧实例说明主题守恒不能跨不同叶测度取消客户债。

本批无LP/MIP、无新策略搜索、无六人完整目标认证、无外审或新颖性结论。关系及共同前提见 `relation-evidence.json`；这里进行实际关系判断，正式三级超图留第三阶段。
