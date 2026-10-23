# 带 actual\\OPT 负信用的调和终局预算

2026-10-23，Boss10子任务个人工作稿。模型、全历史纯SPE与单位客户量词严格采用
`research/current/customer_attraction/model.md`。**一般桥仍为候选，未证明、未反驳；
一般 Q-CAG-HALF 保持 OPEN。** 没有外部结果或文献归属声明。

## 定义级归约

固定完整SPE的实际客户负载c，实际覆盖C、福利W=|C|。
比较元组T=(T_1,...,T_m)达到OPT_m，允许重复；其并集O，客户重数d。
令H_0=0，H_j=Σ_(l=1)^j 1/l，定义

\[
B(c,d)=\sum_x(H_{c_x+d_x}-H_{c_x}),\qquad
D(c,d)=\sum_x\frac{d_x}{c_x+1}.
\]

本任务攻击的桥为：**至少存在一个最优元组T使B(c,d)≤W+|C\\O|。**
更强版本把B替换为D。因为逐项H_(c+d)-H_c≤d/(c+1)，D桥推出B桥。
两桥都足够half，严格理由如下。

令M=|O\\C|、A=|C\\O|、I=|O∩C|。c=0,d≥1的客户对B至少贡献一，
所以M≤B≤W+A=I+2A，从而OPT=M+I≤2I+2A=2W。
空客户、空主题、重复比较主题都不影响这一论证；证明只依赖最优性保证|O|=OPT。

更精确地

\[
B=M+E_B,\qquad
E_B=\sum_{x\in O\cap C}(H_{c_x+d_x}-H_{c_x})
 +\sum_{x\in O\setminus C}(H_{d_x}-1)\ge0.
\]

因此B桥**等价于**2W−OPT≥E_B，而不是与half等价；它要求额外支付E_B。
D桥同样要求2W−OPT≥E_D，其中
E_D=Σ_(O∩C) d/(c+1)+Σ_(O\\C)(d−1)≥E_B。
这些都是一般终局的精确恒等式，完全不需要SPE。

还可弱化为S=Σ_(x∈O)1/(c_x+1)≤W+|C\\O|，依然足够half。
若C⊆O且最优主题把O分割（d∈{0,1}），则S=B=D，桥恰好是
OPT≤W+Σ_(x∈C)c/(c+1)。这正是`two_remaining_tax.md`末段所区分的
**全终局负载税候选**；不能与已反驳的前m−1步税混同。

## 已知完整SPE族的解析攻击

这里只沿现行正文已经证明为完整SPE的指定策略，检查预算；没有把有限回归当成其
完整策略存在性或一般量词的证明。

| 完整SPE族与比较元组 | B | D | 预算余额 |
| --- | --- | --- | --- |
| 文献锐下界：m个客户的大主题A，m−1个单例；实际A^m，比较A加所有单例 | m−1/(m+1) | 同B | W−B=1/(m+1) |
| 无拥挤3/2族：m=k+1，实际C_1,...,C_k,D，比较A_1,...,A_k,D | 2k+1 | 同B | W−B=1 |
| 负前缀族m≥4：实际AB^(m−1)，比较全部m叶 | W−(m−1)/2−2/(m+1) | 同B | W−B=(m−1)/2+2/(m+1) |
| 实际分数负载失败族：实际B^(m−1)A，比较A^(m−1)Q | mH_m | m(m+1)/2 | W=m²，均满足预算 |

以上比较均覆盖全部客户，A=|C\\O|=0。前两行说明不能仅因当前所有已知族通过，
就期待一个与m无关的正余量：文献族余额趋零，无拥挤族余额相对W趋零。

第四行的直接核算：A及AD共m客户有c=1,d=m−1，贡献m(H_m−1)；Q的私有
客户有c=0,d=1，贡献1；共同大块m(m−1)客户有c=m−1,d=1，贡献m−1。
总数mH_m。D则为m(m−1)/2+1+(m−1)=m(m+1)/2。H_m≤m足够B预算。

来源正文：`collision_free_three_halves_family.md`、`prefix_balance_family.md`、
`fractional_actual_load_counterexample.md`与精确目标页的文献族。
`audit_families.py`对2≤m≤30从兴趣类型精确重算上述公式；它不是扩大SPE扫描。

## 旧唯一最优反例及定向证据

`audit_known.py`读取十份既有实例及其完整策略，用规范定义级验证器逐有序历史核验。
随后独立以Fraction计算预算、枚举全部最优支持及补齐元组的极点。

固定一个非空最优支持S，整数q_a≥1、Σq=m形成单纯形；B关于q凹，D关于q线性，
而outside对该支持固定。因此二者的最小值都能在“全部备用副本放到同一标签”处取得。
枚举所有最优支持与这些极点，确实覆盖存在性量词所需的精确最小值。
报告中的`largest_extreme_B`只指这些极点的最大值，不声称凹函数的全域最大值。

- 四人七主题旧唯一最优末查询反例：实际(E,G,A,C)，OPT=1562，W=1559，
  outside=89；唯一最优支持(B,C,D,F)给B=56547/56、D=24441/20，预算1648。
  全400个历史、2400个真正偏离均通过SPE核验。
- 两人五主题旧唯一最优匹配反例：W=44，outside=41，B=D=87/2，预算85。
- 其余八份旧证书也没有反例；精确最优最小值在`known_witness_audit.json`。

进一步的`attack_known_cones.py`没有随机生成新策略，而是在上述两棵旧策略及
负前缀/root-tax旧策略的**固定完整策略锥**中重选全部非负兴趣类型重数，
强制各自原比较支持以1e−6归一化差距成为唯一最优支持，并分别最大化B、D的违反。
八次浮点LP最优目标都严格为负，记录于`known_cone_attack.json`。
这只说明这些指定LP探索没有提出反例；未保存有理对偶，所以不能提升为精确锥定理，
更不能提升一般桥。脚本若出现正目标，必须继续有理化、完整历史精确重放和全部
最优支持枚举，才会标记为精确反例；本次没有触发这一步。

## 当前卡点与下一步

桥有严格的half归约，并通过最相关已知完整SPE族与两个唯一最优旧反例攻击。
尚缺的是从原策略的跨真实离轨分支推导B或更弱S的共同预算。
只有末位节点可直接上界D≤m u_m−Σ_x d_x 1_(x∈S_m)/[c_x(c_x+1)]；
把m u_m支付给W+outside仍无一般证明，不能冻结早期偏离后的后继。

建议下一次判别行动攻击一个明确的一般跨分支收费规则或另一个有完整策略的可变人数族，
而不是扩大随机有限扫描。当前没有合法反例，因此没有新增待宣称的完整反例策略。

运行：

```sh
python3 research/workspaces/customer-attraction/R-75bfd8f0f91740408bf08f0c9f5e2aa1/signed_harmonic/audit_known.py
python3 research/workspaces/customer-attraction/R-75bfd8f0f91740408bf08f0c9f5e2aa1/signed_harmonic/audit_families.py
python3 research/workspaces/customer-attraction/R-75bfd8f0f91740408bf08f0c9f5e2aa1/signed_harmonic/attack_known_cones.py
```
