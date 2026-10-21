# iid 福利桥状态的独立逻辑复核

2026-10-21。范围：只复核已有静态定理和已有八客户反例之间的逻辑闭包；没有发现新实例，没有重新认证全部 SPE 比较，也不改变一般半覆盖或真正聚合安全值桥的状态。

## 结论

`research/current/customer_attraction/iid_security_and_flow_barriers.md` §1、§5 仍称开放的普遍桥

\[
W(\sigma)\ge Z_n(w)
\]

已经被 `CA-WORST-CCE-WELFARE-8` 否定。这里无需求出该实例的静态分布 \(q^*\)。这项结论来自既有结果的严格蕴含，而不是新的有限搜索或平均流分离向量。

## 模型和量词逐项核对

`CA-IID-SECURITY-BENCHMARK` 的静态游戏与 `CAG-MODEL` 使用同一共同目录和同一终局均分收益。其定理允许非负质量，因此包含八个不同单位客户的整数类型实例；提供者数取 \(n=3\)，目录标签数取四。iid 表示各玩家独立按同一个目录分布抽样，并非顺序游戏的行为随机策略。

静态定理证明每个期望调和势最大者 \(q^*\) 都是该同时行动游戏的对称混合 Nash 分布；其乘积分布 \(\mu=(q^*)^{\otimes3}\) 的期望覆盖恰为 \(Z_3\)。混合 Nash 的每名玩家对每个固定纯行动均无盈利偏离，故 \(\mu\) 满足全部个体 CCE 约束。独立性、对称性是该分布的额外性质，未超出八客户定理允许的任意相关、任意不对称 CCE 类。因此

\[
Z_3=\mathbb E_{(q^*)^{\otimes3}}W
\ge\min_{\mu\in\mathrm{CCE}}\mathbb E_\mu W
=\frac{544}{87}>6=W(\sigma).
\]

`CA-WORST-CCE-WELFARE-8` 的反例 \(\sigma\) 定义于全部 \(1+4+16=21\) 个有序历史，84 项含自身行动比较已由两份不同的精确程序检查；其策略甚至只依赖前缀计数。因此它属于目标桥量化的完整历史依赖纯 SPE 类。一个允许类中的此类 SPE 就足以否定普遍桥，不需要所有 SPE 都违反它。主题重复和可信平局均由原完整证书涵盖。

静态定理还证明所有最大者的 \(Z_3\) 相同；即使不使用此唯一值结论，上述 CCE 下界也对每一个静态对称混合 Nash 分布分别成立，不能通过另选最大者逃开反例。

## 所依赖的已有合同

- `research/current/customer_attraction/eight_customer_cce_welfare_gap.md` §1–4：实例类型 \(\{2:4,4:1,8:1,13:2\}\)、完整纯策略、\(W=6\)、\(\mathrm{OPT}_3=8\)、任意静态 CCE 福利的下界及达到下界的分布。
- `research/reviews/customer_attraction/eight_customer_cce_welfare_gap.md`：独立单位客户展开、全部有序历史与静态有序终局检查，以及全部12项个体 CCE 约束。
- 两份已冻结报告 `evidence/runs/2026-10-21/customer_attraction_eight_cce.json` 和 `customer_attraction_eight_cce_independent.json`：均记录21历史/84比较、实际路径 \((0,1,1)\)、收益 \((2,2,2)\)、最低静态 CCE 福利 \(544/87\)。本复核阅读其结果，不导入或重跑其审计实现。
- `research/review_status.json`：`CA-IID-SECURITY-BENCHMARK` 与 `CA-WORST-CCE-WELFARE-8` 均记录完整证明和内部审查；未记录外部同行审查。`research/current/claims.md` 的 iid 行仍保留了应修正的“更强开放桥”字样。

## 不受影响的开放对象

八客户实例满足 \(2W=12>8=\mathrm{OPT}_3\)。真正静态安全值为 \(v_3=44/23\)，所以 \(W-3v_3=6/23>0\)。故此次闭包否定的是更强 iid 福利支配桥，未否定 \(W\ge n v_n\)，也未否定 `Q-CAG-HALF`。原完整树平均模板的非 SPE 分离向量仍只具有其原来的模板否定范围。

## 独立可选代数核对

这一步不用于上述蕴含证明。直接令 \(g_3(t)=1-t+t^2/3\)，取

\[
q=(0,1-2x,x,x),\qquad x=\frac{\sqrt{669}-23}{14}\in(0,1/2).
\]

四个纯查询收益为

\[
\alpha_0=2g_3(2x),\quad
\alpha_1=4g_3(1-2x),\quad
\alpha_2=\alpha_3=g_3(x)+2g_3(2x).
\]

\(\alpha_1=\alpha_2\) 恰等价于 \(7x^2+23x-5=0\)，且 \(\alpha_2-\alpha_0=g_3(x)>0\)。故支持上的行动收益相同，支持外行动0严格较差，直接满足静态 Nash 条件。由已证凹性，它确是 \(F_3\) 的最大者。因此

\[
Z_3=3\alpha_1=3\alpha_2
=\frac{4344-156\sqrt{669}}{49}
\approx6.307237698167356>\frac{544}{87}>6.
\]

本轮实际运行一次独立的 Python `Decimal` 50位数值代入，得到 \(x\approx0.204645308053937526\) 和上述 \(Z_3\)；精确结论由多项式等式和静态 Nash 条件给出，数值仅检查代数抄写。此处未导入其他研究者的 \(q^*\) 重构脚本。
