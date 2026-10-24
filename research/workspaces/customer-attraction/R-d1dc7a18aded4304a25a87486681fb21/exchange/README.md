# 一般最优元组交换：本轮恢复点

2026-10-24，general_exchange。原问题是任意人数、一般共同有限目录、每个完整历史纯 SPE 的 Q-CAG-HALF；仍 OPEN。未得到新一般半覆盖证明、真正反例或新动态共同付款。

- `bernoulli_optimal_exchange.md`：旧最优索引 E1/E2 对全部子列表的 Bernoulli 生成表示；保留分支负载 c 与最优重数 d，积分为外部 `c/(c+1)` 税核。root 和 aggregate_security 已分别独立重构基本(B)/(I)。锚点(BH)由保留最优比较前缀后同一论证直接得到。它不增加全部原 E2 子列表约束的可行性限制，不能称新的不等式机制或 half 进展；真正价值取决于尚未实现的真实枝接入。
- `audit_bernoulli_exchange.py`：不调用 solver/LP 的精确组合恒等式实现核验；m<=12 共 24570 个生成式参数点和 4095 个 Beta 系数全部通过。有限核验不承担一般量词。
- `actual_extra_candidate_probe.py`、`actual_extra_candidate_failure.json`：对唯一精确候选 `m max_T sum_(x in T)1/(1+c_actual)<=W` 用旧canonical实例定向检验，并在已有十一客户 `coverage_opportunity_failure` 的完整 AAB SPE 首次检出即停止。W=8、额外查询T=3、3M-W=1，31历史/124非自身偏离全过。仅重放旧例，不声称新反例、新发现或改变 Mpath 状态。
- `omission_factor_correction.md`：独立发现旧route5a §4把W>=L/2误推half。root 后获悉远端并发组也已纠正，且更精确保留 W 外最优客户差额；本记录只作独立重构。局部共享修改由 root 统一合并，未git提交。

## 正面尝试的真实瓶颈

锚定某个最优主题 T_j 后，真实尾部在 O 外的利润是外部新客户并集 E；积分核只支付 L_out=sum c/(c+1)。剩余返还池 R_out=sum_(c>0)1/(c+1) 满足 E=L_out+R_out。部分继承 `u_tail-u_root<=outside T_j actual shares` 使用实际分母，换成额外查询分母时这份R_out不能消失。即使逐枝补出它，各互斥强制 T_j 子树仍没有一份共同的原路径W可无重复使用。

下一步若继续，应当使用真实后继 IC 同时控制 R_out 与锚点残余(d,c)谱，或找新的跨枝合账。不得把静态最优交换积分、无反例、或本轮纠错当成该动态义务已经解决。
