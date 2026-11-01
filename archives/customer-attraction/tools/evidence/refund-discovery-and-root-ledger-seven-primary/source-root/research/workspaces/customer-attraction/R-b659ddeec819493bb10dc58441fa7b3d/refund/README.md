# 共同退款：准确成果和接续

2026-10-24。只研究一般Q-CAG-HALF及适用于其全部输入的组件；原目标仍OPEN。

- [唯一最优逐角色退款反例](unique_optimum_refund_floor_counterexample.md)：本轮精确合同`ONCE-REFUND-FLOOR`的179客户完整SPE反例；连存在最优O、真实倒二位置也失败。根研究员的另一研究员已独立从原始数据复核；无外审/新颖性声明。由已有71客户机制派生，不是half反例。
- [共同退款的投影后悔预算](shared_refund_projection.md)：全历史`PROJ-IC`及实际路径`PATH-REFUND`，给单份E信用的真实后悔界；没有覆盖接入定理。允许跨角色的`SHARED?`仍未决。
- [冻结179客户输入与完整动作](prefixed_refund_counterexample.json)、[字面输入独立实现审计](audit_unique_refund.py)、[精确输出](unique_refund_audit.json)。179版冻结后不原位改变。
- `probe_prefixed_refund.py`是此明确反例的集合值BI发现程序；审计不导入它。默认只打印；如需写入新候选用`--output`指定不存在的新文件，禁止覆盖冻结证书。最初只有阴性信息的固定锥LP脚本未保留为研究资产。

仅写本目录，不git提交或push，不外发。下一步是真实跨角色共同付款，不能把任意互斥叶各自的外部信用相加成原路径E，也不能因本地逐期合同失败而宣布一般目标不可证。
