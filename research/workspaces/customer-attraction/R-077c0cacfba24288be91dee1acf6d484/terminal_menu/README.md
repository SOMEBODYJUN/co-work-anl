# 真实末尾菜单：探索记录

对象始终是 Q-CAG-HALF 的共同目录、单位客户、任意全部有序历史纯 SPE。
这里是未正式入库的个人探索，不改变主目标 OPEN 状态。

- `bounded_suffix_security_obstruction.md`：完整真实固定尾深子博弈，加全部早期逐前缀最坏拥挤保底，仍不能推出半覆盖。解析参数族，不是真 SPE 反例。
- `audit_suffix_obstruction.py`：独立 Fraction 审计；不导入仓库求解器；验证通式、保底和两个小参数的全部尾部有序历史。
- `suffix_obstruction_audit.json`：实际审计输出。

当前继续方向：必须使用更早偏离后后继玩家自身的最优性；单靠非均匀组合早期粗保底与任意固定尾深的完整菜单不够。正在尝试把末两人菜单嵌入倒三真实偏离分支，而不是继续调原 few-exceptions 乘子。

与已有 `iid_security_and_flow_barriers.md` 区分：本记录删除早期真实偏离的收益，只保留其逐前缀稳健下界；已有 iid 流障碍则读取全树真实偏离后在每个节点内平均。两者是不同的弱化，不互相覆盖。
