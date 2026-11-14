# 支持说明：共同 Q 条件如何给出 security-cone dual 证书

固定人数 `n`、标签目录、完整形式策略 `sigma`，写 `Gamma = G/L`，其中 `L=lcm(1,...,n)`。令 `b_{B,a,T}` 是竞争背景 `B` 对纯查询 `a` 的单查询系数。生成器的精确验收条件是：存在一个与 `a` 无关的 `Q`，以及每个 `a` 的非负 `lambda_a,r_a`，满足

`c/n - E_Q b_{B,a} = Gamma^T lambda_a + r_a`。

对任意有理查询分布 `p`，乘以 `p_a` 求和并乘以 `n`，得到

`c - n E_Q beta_B(p) = Gamma^T (n sum_a p_a lambda_a) + n sum_a p_a r_a`。

这正是 `CA-SECURITY-CONE-DUAL` 的 `(T)` 证书，且同一个 `Q` 对所有 `p` 都可用。对任意 `w in K_sigma` 内积，`Gamma w >= 0`、`w >= 0` 给出

`W_sigma(w) = c dot w >= n E_Q beta_B(p) dot w >= n min_B beta_B(p) dot w`。

因该不等式对全部 `p` 成立，再取 `max_p` 可得 `W_sigma(w) >= n v_n(w)`。因此迁移的精确结论是：

- **结果**：若生成器候选经有理、全类型、全历史的 exact 验收，便得到固定 `sigma` 客户锥上强于单个 `p` 的共同-Q证书，并推出该锥的总福利静态安全下界。
- **边界**：`CA-SECURITY-CONE-DUAL` 的充要定理允许 `Q=Q_p` 依赖 `p`，所以它不能反向产生生成器所需的单一共同 `Q`。
- **开放项**：有限候选不等于 `forall sigma,p` 证书存在；五人保存候选尚无精确可行证书；一般聚合桥、逐人保证和 `OPT_n>2W` 的 half 判据都未由此边闭合。

四人证据提供一个具体成功实例：重构后的 `Q=(3/4,1/4)`、19 个活跃乘子行，378 个类型恒等式全部通过；它仅认证一个固定完整策略锥。五人证据保留一个 6 点 `Q` 数值候选，原概率和及 378 项余数均未精确通过，不能写成反例。完整 DAG 与 `verify_common_reports.py` 的标准库检查验证了固定种子的有序历史节点、真实后继和 `Gamma` 行来源，不能替代普遍数学量词。
