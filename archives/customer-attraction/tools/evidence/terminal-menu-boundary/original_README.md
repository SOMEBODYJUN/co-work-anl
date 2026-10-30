# 真实末尾菜单：探索记录

对象始终是 Q-CAG-HALF 的共同目录、单位客户、任意全部有序历史纯 SPE。
这里是未正式入库的个人探索，不改变主目标 OPEN 状态。

- `bounded_suffix_security_obstruction.md`：完整真实固定尾深子博弈，加全部早期逐前缀最坏拥挤保底，仍不能推出半覆盖。解析参数族，不是真 SPE 反例。
- `audit_suffix_obstruction.py`：独立 Fraction 审计；不导入仓库求解器；验证通式、保底和两个小参数的全部尾部有序历史。
- `suffix_obstruction_audit.json`：实际审计输出。
- `terminal_projection_independent_review.md`、`audit_terminal_projection.py`、`terminal_projection_review_audit.json`：对 global_proof 无条件菜单投影及分数权扩展的独立解析重构；正文只保留发现者一份。
- `individual_deficit_candidate.md`：可直接蕴含主目标的新桥候选、与已有失败接口的区别、精确未闭合义务及当前限定计算。
- `probe_individual_deficit.py`、`probe_individual_deficit_sparse.py`：规范全集求解器的实例探针。
- `probe_deficit_cone.py`、`probe_deficit_cone_larger.py`：读取完整真实策略每个独立偏离的策略锥 LP 探针。
- `probe_fractional_deficit_cone.py`、`fractional_deficit_probe_report.json`：已知非PNE三人策略锥上的均匀分数查询探针。
- `probe_price_existing.py`、`existing_price_probe_report.json`：19个既有实例、207个真实SPE计数终局的完整价格LP探针。

当前继续方向：必须使用更早偏离后后继玩家自身的最优性；单靠非均匀组合早期粗保底与任意固定尾深的完整菜单不够。正在尝试把末两人菜单嵌入倒三真实偏离分支，而不是继续调原 few-exceptions 乘子。

与已有 `iid_security_and_flow_barriers.md` 区分：本记录删除早期真实偏离的收益，只保留其逐前缀稳健下界；已有 iid 流障碍则读取全树真实偏离后在每个节点内平均。两者是不同的弱化，不互相覆盖。
