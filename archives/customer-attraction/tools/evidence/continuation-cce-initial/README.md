# 初次静态CCE策略锥分离：保全与精确重构

[数学对象](../../../state/计算/静态CCE福利分离的初次策略锥证据--计算.md)给出全部单位客户、完整策略、静态对偶和35列证书。这里不执行浮点发现LP，不导入作者或规范模型。

- `original/alternating_cone_result.json`：本批源2e9cd770fef4e67ed7b5完整原字节；初次五主题严格分离和四标签策略两轮零差。
- `original/README.md`：本批源45dfb652f8f558701583完整原字节；十三客户正式成果及发现文件清单。
- `original/later_thirteen_certificate.json`：已完成源625c2e102057a2ad1c50的原字节比较依赖，仅用于核对完整31动作相同；本批没有再次完成该源。
- `source-manifest.json`：上述文件的完整冻结commit、路径、源ID、字节数和SHA-256。
- `audit_initial.py`：本轮标准库Fraction实现；读取初次JSON，穷尽每份策略的有序历史和静态有序终局，直接个体偏离与逐客户对偶恒等式双算；同时清分母、求该有限实例OPT并比较后续策略。
- `replay.json`：上述程序完整输出，含各节点全部候选收益和全部计数对偶列；不是作者浮点发现过程的重跑，也不是新增外审。

从仓库根执行：

```sh
python3 archives/customer-attraction/tools/evidence/continuation-cce-initial/audit_initial.py
```

严格分离的归一化W为1，CCE下界3011/2950；放大31575倍后有43426名单位客户，W31575、OPT42100、CCE下界3802893/118。此下界没有匹配原始分布，不称锐最优值。负面两轮只验证那份固定四标签策略的记录。
