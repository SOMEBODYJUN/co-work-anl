# Uniform-cardinality first/pair 的显式稀疏设计

2026-10-18。仅据 root 给出的 Exact statement 独立重构，未读其作者 Proof。下述构造不调用 fixed-cardinality quadratic optimization 或隐式配置 separation。

## 1. 精确输出

输入整数 d>=1、0<=h<=d；复杂度按 d 的显式长度度量，不按 log d。令 D=1+d+binom(d,2)。确定性输出至多 D 个实际 h-subsets S_l subset [d] 及非负有理权 w_l，满足

    sum_l w_l=1,
    sum_(l:i in S_l) w_l=h/d,
    sum_(l:i,j in S_l) w_l=h(h-1)/(d(d-1))，i!=j.

d=1 不含最后一组等式；h=0,d 可立即输出唯一集合。总支持描述、权位长及运行时间均为 poly(d)。

## 2. 特征及闭合的标签交换

对 h-subset S 定义列向量

    phi(S)=(1,(1_(i in S))_i,(1_(i,j in S))_(i<j)) in {0,1}^D.

每个标签置换 tau 只置换 phi 的 singleton/pair 坐标，因此存在显式 D 维 permutation matrix A_tau，使 phi(tau S)=A_tau phi(S)。这使后续标签交换仅依赖当前 first/pair 向量，和当前支持的更高阶细节无关。

从 S0={1,...,h} 的单点 law 开始。依次对 i=d,d-1,...,2 做：独立均匀取 j in [i]，将所有标签作交换 (i,j)。这个有限 Fisher–Yates 过程给均匀随机标签置换，因而最终 h-subset 均匀。其正确性也可直接看成每个置换唯一分解成上述依次交换，总共 d! 个等概率序列。

我们不保留其全部分支。若当前 law 有至多 D 个有权实际集合，每一阶段只先显式列出至多 iD 个候选 tau_(i,j) S_l，权为 w_l/i；然后按下一节压到至多 D 个实际集合，同时精确保留 phi 均值。之后继续下一阶段。

因为每个后续阶段的期望作用是显式线性算子 i^(-1) sum_j A_tau，阶段压缩不改变最终 first/pair。最终特征均值恰等于完整 Fisher–Yates law 的特征均值，即第 1 节目标。

## 3. 只在显式候选上的有理压缩

给 N>D 个正权候选列 phi(S_l)，把全部权写为 a_l/Q，其中 a_l,Q 为非负整数、sum_l a_l=Q。寻找这些 0/1 列的一个非零整数线性依赖 u，满足

    sum_l u_l phi(S_l)=0.

这只需对至多 D+1 列作普通有理线性代数：按固定顺序选一个基本依赖，Cramer minors 给整数 u，支持至多 D+1，且

    log_2 max(1,|u_l|)=O(D log(D+1)).

常数坐标确保 sum_l u_l=0，所以 u 同时有正负坐标。确定性选

    k in argmin_(u_l>0) a_l/u_l,
    Q'=Q u_k,
    a'_l=a_l u_k-a_k u_l.

所有 a'_l>=0；至少 a'_k=0；sum_l a'_l=Q'；特征均值保持不变。删掉零权候选，重复到 N<=D。整个过程始终只使用已经显式列出的真实 h-subsets。

这也是对显式普通有理可行 LP 的 basic-support reduction：变量是该阶段已经列出的至多 iD 个候选权，等式仅为 phi 均值，无非显式列或 separation oracle。没有最大化一个任意 quadratic set objective。

## 4. 总位复杂度

每一阶段有至多 dD 个候选，每个集合 d bits，最多 d 阶段。每次压缩至少删一列；总消元次数 O(d^2 D)。基本整数依赖的每个系数有 O(D log(D+1)) bits，由 0/1 minors 的 Hadamard 界得到，和权重数值无关。

分支时共同分母只乘 i；每次消元共同分母只乘一个 |u_k|。因此所有阶段结束前

    log Q <= log(d!)+O(d^2 D^2 log(D+1))=poly(d).

由于所有权非负、和为一，0<=a_l<=Q；所有中间分子也有同样多项式位长。用标准精确有理/整数消元求上述基本依赖，和其余整数比较、乘加，均为确定性 poly(d) 时间。可将每轮共同分子分母约分，但正确性和多项式位界不需要约分。

最终输出至多 D 个 h-subsets，权编码总位长 poly(d)，并精确保留原均匀 h-subset law 的 first/pair。这完成 statement 要求，而非仅证明存在一个小支持。

## 5. 应用于行配置的准确身份

对七态行配置 law 中每个固定 (C,H) 类别分别取上述 h=H 的设计，给每个输出集合附上其类别质量；当 C=1 时加上那枚指定原 incoming job。所有集合仍是该类别的真实合法配置，总支持至多 6D，全部权精确可生成；可再在完整行 first/pair 特征上作同样压缩。

这只替代每行合法 CONFIG 分布的 first/pair 证书。共同 L 的次数六矩、所有全局 q2 检验仍使用原均匀 H-subset law 的高阶矩公式，不能以此稀疏 pair design 替换该真实 law 后冒称高阶矩不变。
