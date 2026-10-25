# 研究员4：一般人数尝试的真实结论与停止界

**没有证明一般 Q-CAG-HALF，也没有得到其 SPE 反例。** 本轮没有将五人零背景定理用于有背景后缀。完整推导在 [general_proof.md](general_proof.md)。

## 已完成且可复核

- 任意 m 的“实际末主题 E 的所有早期复制分支”可用独立隐藏位 epigraph 精确编译；共同实际收益 u_i 和共同 K 统一记账。代码：[copy_cone.py](general_work/copy_cone.py)。
- 保留重叠尾二引理给任意 m≥2 的合法并集行 `(m/2)H≥Σ_x 1_{x∈O}/(b_x+1)`，由全部比较索引对求和后逐客户下界导出。
- 六人对应408条必要行系统存在精确有理分离点：W=1，O=93445653738551/37969467558408≈2.46107358748。独立 Fraction 语义核验所有408行非负以及全部共同边缘一致性通过。

精确源：[cone6_exact_obstruction.json](general_work/cone6_exact_obstruction.json)、[cone6_semantic_report.json](general_work/cone6_semantic_report.json)；直接复核：

```sh
python team/general_work/verify_semantic_obstruction.py 6
```

此点把比较元组压成并集位 O，没有完整 SPE，也没有六个显式比较主题。它只否定所列必要行系统的二系数闭合，不否定主目标，不否定五人索引证书，不否定六人新菜单/自由投影。

## 精确停止界

1. `u_m≤W/m` 已有两个单点目录完整 SPE 反例，不再尝试。
2. 令ℓ为实际前m−1位负载、P=Σ_{实际覆盖}1/(ℓ+1)。合法 `OPT≤m u_m+W−P` 不能借 `m u_m≤W+P` 闭合：仓库旧四主题五人完整 SPE 路径00001有 W39、u5=53/5、P=67/5，反向差3/5。本轮独立重放341历史1364比较通过。原始精确源：`co-work-anl/research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/terminal_balance/refined_failure.json`；复核：[verify_terminal_tax_bridge_failure.py](general_work/verify_terminal_tax_bridge_failure.py)。
3. 上述六人408行固定锥的任意新乘子都不能闭合二；停止继续扩其阴性计算。新增比较索引菜单、跨索引真末回复、再一层真偏离或其它投影后，可重新检验。

## 可接续而尚未证明的义务

五人机制的全m推广需要真正支付 `OPT−W` 的跨枝共同信用。当前 O-only 复制系统已经明确丢掉最优索引相关性；六人新菜单/自由投影应优先尝试切掉现有分离点。

另一个仅供未来验证的背景五人候选：对任意固定外负载 B_x，将容量权重改为 κ_x=5/(B_x+5)，共同 K_B=max_QΣκ_x 1_Q，所有原始份额改为1/(B+c)，目标改为同背景剩余利润 `2Σc/(B+c)−Σd/(B+d)`。这会保留合法根界 `u_first≥K_B/5`，但每个组件、MAXROOT和所有客户 B≥0 的余项均必须重新证明；当前没有验证，不能用作一般归纳。
