# root 第七轮解析重构与精确核查

- [源序重构](source_order_reconstruction.md)：先按陈述独立推导，再读作者对照；不假称完全盲题或新颖性。
- [共同列界、prefix 审查及反向 SD](reverse_sd_and_joint_review.md)：root独立重构与新一般反向核，coupling/global另行审核；方向和未闭项明确。
- [独立脚本](audit_joint_payments.py)、[冻结结果](joint_payments_independent.json)：原348单位客户完整策略，不导入 solver/作者审计，核原全部IC、非零共同运输及synthetic query投影。结果不得作一般福利证据。

Q-CAG-HALF仍OPEN。本目录只支持第七轮准确交接；外审与新颖性未认证。

- [坐标保留初始化](optimal_coordinate_initialization.md)：root最后新推导；global/coupling独立重构通过。一次wholeIC保存每个比较客户库存，未证future余额支付。
- [非零独立实现](audit_coordinate_initialization.py)和[冻结结果](coordinate_initialization_independent.json)：旧348完整策略上，固定最优比较组合触发10单位future源/3条SAFE正边，逐单位库存与质量守恒通过；不作一般容量证据。
