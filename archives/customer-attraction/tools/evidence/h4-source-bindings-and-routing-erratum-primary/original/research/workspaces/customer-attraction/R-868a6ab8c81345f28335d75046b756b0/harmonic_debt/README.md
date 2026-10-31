# 调和端点债务：独立重构与精确量词边界

2026-10-24。本分支只研究一般 Q-CAG-HALF；主目标仍 OPEN。

- `h4_quantifiers_and_owner_thinning.md`：独立重构 H4；写清全部真实后继、最优元组与排列的存在量词、owner 薄化和真正剩余义务。未给一般支付证明。
- `audit_packet13_h4.py`、`packet13_h4_exact.json`：从既有十三人闭合 DAG 独立复核全部 27243 节点、112050 项含自身 IC，再计算局部错误候选、同查询预算及存在最优元组 H4 的精确边界。复用旧实例，不声称新反例或一般证明。
- `attack_h4_cone.py`、`attack_endpoint_max.py`、`attack_same_query_debt.py`、`attack_local_debt.py`、`attack_local_random.py`：探索脚本。既有策略锥中的浮点阴性提案与随机精确 BI 阴性都没有普遍数学意义。局部候选及端点最大查询桥已由旧十三人完整 SPE 否定，已撤回，不能再据阴性重提。
- `product_transfer_independent_review.md`：独审相邻 dynamic_matching 的一般全续局转移闭包、L严格非可加见证及放大充分条件；审查范围内通过。
- `review_product_transfer.py`、`product_transfer_independent_audit.json`：不导入构造器或规范求解器，独立重放全部91有序历史/819项IC及16个末回复叶对，确认 `L_prod(BB)=5/2<3=2L(B)`。

当前判断：本分支没有新增接通一般证明的正向关系。保留的价值是 H4 与薄化/直接覆盖预算的强弱关系、精确定位已知局部失败，以及对另一分支一般机制的独立验证；不把这些账本整理称为主线突破。全续局L的普遍可加假设确被合法单位客户见证否定；固定坐标产品策略的实际收益可加性不受影响。
