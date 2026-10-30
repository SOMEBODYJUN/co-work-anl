# 研究员4：一般人数尝试的真实结论与停止界

**没有证明一般 Q-CAG-HALF，也没有得到其 SPE 反例。** 本轮没有将五人零背景定理用于有背景后缀。完整推导在 [general_proof.md](general_proof.md)。

## 已完成且可复核

- 新尾二容量桥及其**任意剩余人数 k 的闭式推论**已独立重构。任真节点尚余 k≥2、规定收益 v、前缀 b，任合法 T,Q，有 `v+K≥Σ_x[t/(b+k−1)+q/(b+k−1+t)]`。强制 T 后将最后真实回复 R 与 T 配对，中间 k−2 主题合计 z；精确恒等式为 `v+K−f_(b+z)(T)−U_(b+z)(Q,T)=源IC+末位IC+(K−|R|)+Σ_R(b+z)/(b+z+1)`。先非负，再用 z≤k−2 及分母单调性。k=2 正是 six_stress 新容量桥。它等价于通用投影参数 alpha全0、beta仅末位1、mu1，隐藏位最小值在中间全1、末位0取得。
- 容量桥还可写成更强菜单容量版本 `v+F_b≥f_b(T)+U_b(Q,T)`，其中 `F_b=max_H f_b(H)`；其证明没有逐客户余项。`F_b≤K` 给新桥，`F_b≤u_D+g_b(C,C)` 给原保留重叠 PAIR，因此新增的是同一右端的一个容量预算端点。自足全k推导与精确核验均在 [verify_tail_capacity_bridge.py](general_work/verify_tail_capacity_bridge.py)，默认测试k=2..25、b=0..50的所有计数/会员位，并独立检查b=0..1000的尾二恒等式。解析式对全部k成立，有限扫描不冒称无限计算证明。
- 任意 m 的“实际末主题 E 的所有早期复制分支”可用独立隐藏位 epigraph 精确编译；共同实际收益 u_i 和共同 K 统一记账。代码：[copy_cone.py](general_work/copy_cone.py)。
- 保留重叠尾二引理给任意 m≥2 的合法并集行 `(m/2)H≥Σ_x 1_{x∈O}/(b_x+1)`，由全部比较索引对求和后逐客户下界导出。
- 六人对应408条必要行系统存在精确有理分离点：W=1，O=93445653738551/37969467558408≈2.46107358748。独立 Fraction 语义核验所有408行非负以及全部共同边缘一致性通过。

精确源：[cone6_exact_obstruction.json](general_work/cone6_exact_obstruction.json)、[cone6_semantic_report.json](general_work/cone6_semantic_report.json)；直接复核：

```sh
python research/workspaces/customer-attraction/R-07e871289a6b4c1fb07244c97eb4aac8/general_from_half5/general_work/verify_semantic_obstruction.py 6
```

此点把比较元组压成并集位 O，没有完整 SPE，也没有六个显式比较主题。它只否定所列必要行系统的二系数闭合，不否定主目标，不否定五人索引证书，不否定六人新菜单/自由投影。

## 精确停止界

1. `u_m≤W/m` 已有两个单点目录完整 SPE 反例，不再尝试。
2. 令ℓ为实际前m−1位负载、P=Σ_{实际覆盖}1/(ℓ+1)。合法 `OPT≤m u_m+W−P` 不能借 `m u_m≤W+P` 闭合：仓库旧四主题五人完整 SPE 路径00001有 W39、u5=53/5、P=67/5，反向差3/5。本轮独立重放341历史1364比较通过。原始精确源：`research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/terminal_balance/refined_failure.json`；复核：[verify_terminal_tax_bridge_failure.py](general_work/verify_terminal_tax_bridge_failure.py)。
3. 上述六人408行固定锥的任意新乘子都不能闭合二；停止继续扩其阴性计算。新增比较索引菜单、跨索引真末回复、再一层真偏离或其它投影后，可重新检验。

## 可接续而尚未证明的义务

新增容量桥提供此前固定锥没有的合法端点，可接入六人新菜单系统。本轮没有从它加 MAXROOT 结构找到一般人数的可行共同乘子。单个尾二并集行需要乘m/2，而容量K若仅由根K≤m u_1支付，开销随人数增长；所以这项闭式本身不是人数无关的福利闭合。

五人机制的全m推广需要真正支付 `OPT−W` 的跨枝共同信用。当前 O-only 复制系统已经明确丢掉最优索引相关性；六人新菜单/自由投影应优先尝试切掉现有分离点。

另一个仅供未来验证的背景五人候选：对任意固定外负载 B_x，将容量权重改为 κ_x=5/(B_x+5)，共同 K_B=max_QΣκ_x 1_Q，所有原始份额改为1/(B+c)，目标改为同背景剩余利润 `2Σc/(B+c)−Σd/(B+d)`。这会保留合法根界 `u_first≥K_B/5`，但每个组件、MAXROOT和所有客户 B≥0 的余项均必须重新证明；当前没有验证，不能用作一般归纳。
