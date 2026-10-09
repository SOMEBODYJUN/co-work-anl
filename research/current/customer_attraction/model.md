# CAG-MODEL：依次选主题、固定均分的客户吸引博弈

本分支的客户不进行第二阶段优化；这是 Deng 等的 customer attraction game，
与仓库既有 `research/current/model.md` 的主动原子客户设施模型不同。

## 对象、定义与量词

有限客户集为 $N$，有限非空共同主题目录为 $\mathcal S\subseteq2^N$。
每个客户价值为一，每位提供者权重为一。提供者数 $m\ge1$，行动顺序固定为
$1,\ldots,m$，每位提供者观察全部有序历史并且选择一个目录主题，允许重复选择。
空主题允许存在；不可被任何主题覆盖的客户可以删除，且不改变所有收益或最优覆盖。

有序终局 $s=(S_1,\ldots,S_m)$ 中

$$
c_x(s)=|\{i:x\in S_i\}|,\qquad
u_i(s)=\sum_{x\in S_i}\frac1{c_x(s)},\qquad
W(s)=\left|\bigcup_i S_i\right|=\sum_i u_i(s).
$$

纯策略为每个有序历史上的主题选择：
$\sigma_i:\mathcal S^{i-1}\to\mathcal S$。
记 $\alpha(h,\sigma_i,\ldots,\sigma_m)$ 为固定前缀 $h$ 后所得完整终局。
纯 SPE 的要求为：对每个 $i$、每个 $h\in\mathcal S^{i-1}$、每个 $T\in\mathcal S$，

$$
u_i(\alpha(h,\sigma_i,\ldots,\sigma_m))
\ge u_i(\alpha((h,T),\sigma_{i+1},\ldots,\sigma_m)).
$$

这量化全部离轨历史。相同主题计数的两个历史可以选择不同的续局；没有固定、
匿名或对在轨有利的平局规则。SPE 存在由有限树上的逆向归纳直接得到。

最优覆盖为

$$
\operatorname{OPT}_m=\max_{(T_1,\ldots,T_m)\in\mathcal S^m}
\left|\bigcup_{i=1}^mT_i\right|.
$$

用少于 $m$ 个主题获得的覆盖可通过重复某个主题补齐。因此“至多 $m$”与
“恰 $m$”的最优覆盖相同。全零实例直接满足目标不等式，不定义 $0/0$ 的效率比。

## 精确压缩输入

一个客户类型记录其感兴趣的主题标签集合，以及非负整数重数。
重数 $r$ 代表 $r$ 个不同的单位价值客户，不引入非单位权提供者。
对终局主题计数 $q$，选择标签 $a$ 的任一提供者收益为

$$
U_a(q)=\sum_{B\ni a}\frac{r_B}{\sum_{b\in B}q_b}.
$$

仅在 $q_a>0$ 时需要这个表达式，因此每个所用分母正。
计数压缩保存终局收益和覆盖，不能直接把所有纯策略限制为只依赖计数的策略。
集合值逆向归纳的正确性须另证其恢复的是全部有序历史续局，而不是一个规范选择器。

## 来源与状态

Paper Fact：Deng 等，*Equilibrium Analysis of Customer Attraction Games*，
[arXiv:2307.07174v2](https://arxiv.org/html/2307.07174v2)，§2、§5 Definition 4。
本页重新固定本轮 exact input class；没有把论文其他非对称模型并入本分支。
