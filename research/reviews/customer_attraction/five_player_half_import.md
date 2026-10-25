# 五人半覆盖证明包：入库、数学审查与精确复跑

审查对象为用户本轮上传的 `Q-CAG-HALF-5-proof.zip`，不是历史聊天中的不可读路径。原包证书 SHA-256 为 `395e056b218d237abe8b85db894f0b1c37d2e14d55c74b1dca723abeceb6a44e`。

## 结论

接受 `CA-FIVE-HALF-EXACT-v1` 为**完整精确计算机辅助证明、内部独立审查通过、未记录外审**。准确对象见[现行定理入口](../../current/customer_attraction/five_player_half.md)。一般人数仍 OPEN，没有获得六人或任意背景五人定理。用户明确批准本次入库；审查按实际完成范围记录，不把批准本身作为数学证据。

## 实际完成的检查

| 检查 | 实际覆盖及结果 |
| --- | --- |
| 原始来源 | [ZIP 原档](../../../history/source/notes/customer_attraction/half5_exact_upload.zip)全部解压文件与 MANIFEST 的哈希、字节数一致；规范包保留原字节。 |
| 局部数学 | [独立局部审查](five_player_half_local.md)实际读取原局部正文、MAXROOT、核验器及全部输入；核对 IC 符号、强制节点、真后继、共同 K 和向外取整；未见致命漏洞。 |
| 主证书数学 | [独立主证书审查](five_player_half_global.md)读取主正文、全部活跃行、主核验器及输入；重构强末两人式、直方图对称性、共享 d、族分离、菜单四角及整数判号。 |
| 主方重新运行 | [局部报告](../../../evidence/customer_attraction/half5_exact_v1/local_components_rerun.json)验证 36 组件、47,872 系数状态；[完整主域报告](../../../evidence/customer_attraction/half5_exact_v1/complete_domain_rerun.json)验证 6,144 条件，最小余项 0，K 余项 2,264,870，均精确通过。 |
| 另一研究员复跑 | [主域记录](../../../evidence/customer_attraction/half5_exact_v1/global_recheck.json)与主方一致；这重跑同一主程序，不冒称第二独立主实现。 |
| 字面语义交叉核对 | [审查程序](../../../tests/audits/customer_attraction_half5_semantics.py)另按字面索引构造活跃行，再与原程序比较；[结果](../../../evidence/customer_attraction/half5_exact_v1/literal_semantics.json)通过。它导入被测程序及其投影表，只是行语义交叉检查，明确不是独立完整证明器。 |
| 终式 K 列 | 主方额外从 `active_k_columns.json` 与整数权重直接相乘，得加权 K 列 −2,264,870，乘 120 后为 −271,784,400，反算一致。 |

## 必须保留的边界

1. 原包只有一个可运行主域核验器和一个局部核验器。随包 `primary_full_domain.json` 为历史日志；未交付其对应主程序，本轮不声称复跑两份独立主实现。
2. 局部核验器发现一个未来输入的语义加固点：PC2 的 TAX 解析分支未排除被强制的第四位。当前所有 PC2 数据均没有 TAX 行，所以当前证明不受影响。原包冻结不改；未来扩展输入前须单独加固。
3. 计算所穷举的是覆盖所有任意规模实例的系数类型域，完整性有正文和独立审查支撑。它与“有限实例未找到反例”有本质不同。
4. 五人零背景结论不能直接作为五人有背景新增覆盖或剩余利润定理。任意人数推广需重新定义并证明相应行、表与总预算；不能仅换代码人数。

## 来源与新颖性

证明由用户作为已完成资产提交。本轮贡献是原档保存、复跑、独立审查、正式导航和推广义务提取，不认领上传证明的发现或全球新颖性。外审、论文接收和锐性均未认证。
