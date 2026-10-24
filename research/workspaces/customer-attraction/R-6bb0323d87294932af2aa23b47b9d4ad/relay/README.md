# Relay 工作检查点

对象：一般 Q-CAG-HALF，任意 m、任意有限共同目录、每个完整有序历史纯 SPE，单位客户与提供者，空主题/重复/平局保留。一般目标 OPEN。

当前材料：

- `working.md`：真实二查询 signed reset、共同税、当前 slack 与同分布对角税的精确分解；明确这些是等价账而非新福利下界。一般未决义务是用真正 successor IC 一次支付跨位置重置。
- `audit_pair_reset.py` / `pair_reset_checks.json`：七个既有 SPE 的定义级有理公式检查，不是一般定理。
- `audit_two_block_pair.py` / `audit_two_block_pair.json`：独立核验旧八人全策略 DAG，精确否定逐节点 cross-pair 充分条件；同一根的全 simplex 同分布二次型仍低于 root u，aggregate pair 亦未失败。

关键有限结果：根 pair(3,7) 的 `2u−K_AT−K_TA=−9/10`；但 root `max_p pᵀKp=1717/560<13/4`。不能混同局部 pair、局部同分布二次型、aggregate pair、自由菜单和 half。

补充一般组件 OCC：真实后继边际 q=Pp 满足 `n qᵀKp=E tail-extra-profit+I`，I 由整数尾负载的逐客户乘积给出且非负。它不使用 SPE，尚未给 derivative/half 支付。父方 quantitative derivative 候选在旧八人源精确失败，但更弱 `G>u => derivative>0` 仍未决；见 working.md §8。

§9 新增已给正分解的一般不等式 `I>=G−D`，故 `G+tail-extra-profit<=D+nqᵀKp<=u+nqᵀKp`。它使用单位整数尾负载；最后一步使用真实当前 IC。真正 successor IC 对另一混合项 `pᵀKq` 的支付仍缺。

未获新的全输入正向承重不等式。没有提交或同步；由 parent 汇总。
