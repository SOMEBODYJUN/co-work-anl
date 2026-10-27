# 整终局势候选的全混合元组收尾仍不足

2026-10-27。**主目标 Q-CAG-HALF-6 仍未解决。以下均是精确必要条件/候选收尾的障碍，不是完整 SPE，也不是半覆盖反例。**

## 新信息与用途

已有开放候选以实际六主题 `A_0,...,A_5` 的自复制税 `C` 为预算，要求所有六槽终局的调和势 `P_6 <= W+C`。本实验不攻击这个候选本身，而是检查：即使把全部混合实际/最优主题的势比较一起用上，是否能以纯组合计算推出 half？答案是否定的，而且把同类更强预算加入每个实际前缀也仍不足。

`mixed_potential_static.py` 生成两份精确有理可行点：

| 点 | 全部比较/合法行 | W | O |
| --- | --- | --- | --- |
| `mixed_potential_static_extra.json` | 根的全部 1292 个混合势比较、42 条真实路径安全偏离、29 条强末两位势比较，共 1363 行 | 1 | `475133789041/228181575630 > 2` |
| `mixed_potential_static_extra_suffix.json` | 再加入每个实际前缀余 3/4/5 人的同类**开放**势预算，共 2292 行 | 1 | `681135740229009527889/330411663283037526451 > 2` |

每个点的所有客户都恰属一个比较主题，因此六个比较主题覆盖全宇宙，`O=OPT_6`。但是给出的实际六主题序列没有被证明为某份完整 SPE 的路径；这些点只说明上表行族不足以闭合目标。

## 行与压缩的完整定义

目录有十二个合法主题：六个实际主题 `A_i` 和六个比较主题 `T_j`。对比较标签全对称化后，客户类型为 `(a,k)`：`a` 是六个实际会员位的 mask，`k` 是比较主题会员数。该类型的总质量 `w_(a,k)` 均匀分到 `binom(6,k)` 个比较会员子集。允许所有 447 个非空类型；最终点只有 `k=1`。

令 `p_i(a)` 为在位置 i 之前的实际覆盖数，`r_i=6-i`，`c(a)=popcount(a)`。

`W(a,k)=1_(a !=0)`，`O(a,k)=1_(k>0)`；实际第 i 位利润为 `1_(i in a)/c(a)`，零分子按零处理。自复制税为

`C(a,k)=sum_(i in a) [1/(p_i(a)+1)-1/(p_i(a)+r_i)]`。

根势候选行是：对任意由十二主题组成的六槽计数 q，

`sum_x H_(c_x(q)) <= W+C`。

实际标签计数保留顺序，比较标签计数只按整数分拆分类；因为客户质量在比较标签间对称，这覆盖**每一个**原始六槽多重集，而非抽样。按实际总槽数 d 分类，行数为 `sum_d binom(d+5,5) p(6-d)=1292`。

42 条真实路径安全偏离是每个 i 对六个 `A_j` 和一个对称 `T_j` 的

`u_i >= sum_(x in Q) 1/(p_i(x)+r_i)`。

29 条强末两位势比较是对任意两槽 `(Q,R)`：

`Phi_b(Q,R) <= u_4+u_5+sum_(x in A_4)1/((b_x+1)(b_x+2))`，

其中 `b=p_4`，`Phi_b(Q,R)=sum_x[H_(b_x+c_x(Q,R))-H_(b_x)]`。这是有效的两人强 PAIR：在现行两人税证明的非负恒等式中删去最后的 `g_b(Q,R)` 项即可得到，不是三人以上未证外推。比较两主题的对称分类是 21 个实际对、6 个实际/比较对、同一或不同的比较对，共 29。

后缀版本另对实际前缀 i=1,2,3 加入全部 r_i 槽混合势比较，右端为真实后缀玩家的最终利润和，加它们的实际有序自复制税；背景固定为实际 `p_i`。这些是更强的**开放候选**，没有标成合法 SPE 推论。i=4,5 的预算已经包含在强 PAIR 及末位 BR 中。

## 精确证书与单位客户恢复

JSON 的 `exact.support` 储存全部非零 `(a,k,mass)` 的 Fraction 字符串。程序先由数值 LP 发现支撑，再以标准库 Fraction 高斯消元重构，逐行验证所有整数系数不等式。每个原始系数统一乘 3600 后为整数；精确核验不依赖数值 LP 的容差。

将质量均分到比较会员子集，再乘所有有理分母的公倍数，就得到有限个不同单位客户。无需引入非单位提供者。客户全在 `O` 内，因而没有把遗漏 L 与净差 `OPT-W` 混用。

从仓库根精确重放（不调用 LP）：

```sh
python3 research/workspaces/customer-attraction/R-5ba0899f8e71460dafad1ae1ac8c0bcf/subagent_1/mixed_potential_static.py --verify research/workspaces/customer-attraction/R-5ba0899f8e71460dafad1ae1ac8c0bcf/subagent_1/mixed_potential_static_extra.json
python3 research/workspaces/customer-attraction/R-5ba0899f8e71460dafad1ae1ac8c0bcf/subagent_1/mixed_potential_static.py --verify research/workspaces/customer-attraction/R-5ba0899f8e71460dafad1ae1ac8c0bcf/subagent_1/mixed_potential_static_extra_suffix.json
```

两个点均通过，最小清分母松弛为零。程序的 `--extra --exact`、`--extra --suffix --exact` 重新运行发现 LP；数值最优性没有被提升为精确 LP 最优性。这里证明的是存在上述精确可行点，已足够否定各自纯组合收尾的充分性。
