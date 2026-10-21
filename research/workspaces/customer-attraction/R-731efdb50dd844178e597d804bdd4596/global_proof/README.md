# 本轮全局证明研究备份

主目标Q-CAG-HALF保持OPEN。只在本人目录写入，未做git操作。

## 可接续成果

- `floor_only_protection_obstruction.md`及`audit_floor_only_protection.py`、`floor_only_protection_audit.json`：新的充分桥障碍。m个互不交36客户复制给OPT=21m，任意根动作都能被(10,12,12,21,…)的非可信菜单压低于OPT/(2m)=21/2；最后m−3位可配全部历史完整SPE。故任意固定长度理性尾部加其余后继收益floor仍不足保护当前人。不是目标反例。
- `repeated_prefix_independent_review.md`、`review_repeated_prefix_certificate.py`、`independent_repeated_prefix_audit.json`：独立审查terminal_geometry的18行正证书；原五人(C,C,C,A,B)与扩展(E,F,C,A,B), C⊆E∩F均通过原始逐会员审计。该结构性half不是一般half。

## 探索与失败，不作定理

- `menu_synthesis.py`、`prefix_menu_synthesis.py`：末两人G加在轨直接保底的数值必要条件合成；m5未闭合。m4浮点β≈1.9264902135尚无本文精确证书，不能当成熟结果；已向terminal_geometry共享避免重复。
- `individual_floor_search.py`：对六主题三人组策略锥的一次浮点逐人比率检查。弱逐人OPT/(2m−1)是历史已列OPEN，不是本轮新候选；已停止重复有限扫描。
- `safe_floor_milp.py`、`safe_floor_m3p6.json`：未成熟的非可信菜单MILP。该优化把t=1固定后最大化OPT；其value9不自动反驳t=OPT/(2m)，因为放大OPT会提高目标floor。可复用生成器，不将该输出当证明。

最初尝试高分数覆盖数与私有/共享客户质量互补；高τ不保证全局私有多（循环边型关联就是障碍）。尚无合法一般组合预算。下一步必须保留惩罚者自身真实最佳回复关系；仅延长已完全理性的末尾或只用后继收益floor都不够。
