# 真实节点交换与 signed 尾部时钟

Q-CAG-HALF 一般目标仍 OPEN。本目录只研究真实历史上的交换与误差抵消，不冻结尾部，不把同计数历史强制合并。

- [主推导](signed_history_exchange.md)：任意人数下，交换残差精确等于两条真实分支的尾部 clock 之差；标记 incidence 守恒才授权 signed 抵消。真实终局算出之后可合法合并 terminal debt。
- [完整 SPE 反例](attack/real_node_swap_obstruction.md)：三不交主题大小2、2、1，实际 BAC，真实交换为 ABA，旧群体总收益4降为3；两真实互惠节点与末位同值不消去续局差。
- `audit_signed_history_exchange.py`：独立重建全树、分支clock、标量守恒不足及终局层合并；`signed_history_exchange_audit.json`为本轮运行记录。
- `attack/audit_real_node_swap.py`及`attack/real_node_swap_audit.json`：反例的全部历史精确重放。

当前缺口是从同一完整 SPE 的真实 BR 行构造满足标记/终局债支付的同一组非负全行权。代数 circulation 不自动给出合法的反向 BR 行，也未证明旧 reset premium 与本次交换残差自动相消。下一次直接检查具体一般真实行构造产生的 d_z，不再尝试匿名冻结尾部。
