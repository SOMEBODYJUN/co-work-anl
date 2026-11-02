# 背景归纳研究备份

对象：一般 Q-CAG-HALF，研究任意合法固定背景的剩余利润、最优覆盖分配与递归不变量。
当前状态：探索中。已读取背景三/四人利润及一般税、逐期/前缀余额失败结果。
本目录不承诺主目标结论；精确脚本和失败候选会继续保留。

## 当前完成与失败状态

- `full_tree_independent_review.md`、`audit_full_tree_independent.py`、`full_tree_independent_audit.json`：独立审查全树收益图/SCC商锥，式(4)--(7)通过；另给真实完整策略的型空间额外lineality反例。普遍半覆盖未解。
- `search_background.py`：整数LCM缩放的全集 bitset 背景 SPE oracle；与规范 Fraction oracle 一个随机实例的全部终局集合对照一致。不是普遍定理证据。
- `search_invariants.py`：3000个随机背景有限实例未发现背景覆盖遗憾候选失败，不能升级为正面结论。
- `search_threshold.py`、`search_last_payoff.py`：若干阈值单调/逐人预算候选的探索反例，未作为成熟资产提升。
- `search_residual_union_lp.py`：两人五主题625个末回复锥的浮点LP筛查；`search_residual_cones.py`：三人六主题500棵随机完整策略锥筛查。均未找到 residual-union>W，但该加强桥已被另一研究目录六主题两人完整SPE精确否定，禁止据有限扫描复用。反例原文：`research/workspaces/customer-attraction/R-d51d7a410c12456aa5c44e84b78708d0/independent_attack/residual_cover_family.md`，q=2给W=13、残余OPT_2=14。
- `scc_attack.py`、`mapped_extra_lineality.json`：探索得到的SCC映射警告矩阵；已由不依赖LP的独立审查脚本精确复核。

下一步：按父代理要求，对两项已成熟的删客户/收益cap障碍做共享数学资产清洗入库；不据本目录有限扫描改变主目标OPEN。
