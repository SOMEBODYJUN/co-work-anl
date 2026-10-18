# 固定轮 assignment Sherali–Adams 的趋二间隙

本文给出一个参数化、完全符号化的局部松弛障碍。它说明：无论把 assignment/LST 线性规划提升到任何**固定轮**的 literal Sherali–Adams 层，仍不能从阈值证书 `T` 统一舍入出 `(2-ε)T`。该结果只限制固定层局部舍入，不是一般算法的复杂度下界；本族实例本身有显然的最优调度。

## 局部松弛的精确定义

固定整数 `r≥1`。给定阈值 `T` 的 unit-assignment feasibility LP 为

\[
\sum_i x_{ij}=1\quad(j\in J),
\qquad
\sum_j x_{ij}\le T\quad(i\in M),
\qquad 0\le x_{ij}\le1.
\]

本文采用如下轮次约定：`SA_r(T)` 包含原约束乘以任意至多 `r-1` 个 literal（`x_{ij}` 或 `1-x_{ij}`）后的线性化不等式。改变文献中的轮次编号只会把 `r` 平移 1。

## 命题卡

**ID/version：`UM-FIXED-SA-ASSIGNMENT-GAP-v1`。** 对每个 `m≥r`，取 `m` 台相同机器和 `n=m+1` 个 unit 任务，所有 `p_{ij}=1`，令

\[
T_{m,r}=1+\frac1{m-r+1}.
\]

则 `SA_r(T_{m,r})` 可行，而整数最优值恰为 `OPT=2`。因此

\[
\frac{OPT}{T_{m,r}}
=\frac{2(m-r+1)}{m-r+2}
=2-\frac2{m-r+2}.
\tag{1}
\]

对任意固定轮 `r` 和任意 `ε>0`，取 `m` 足够大就有 `OPT/T_{m,r}>2-ε`。所以任何“先求固定轮 `SA_r` 证书、再对所有证书作统一 `(2-ε)T` 舍入”的合同都不可能成立。
另一方面，任意 `SA_r(T)` 可行点投影为原 assignment/LST 可行点，经典有序槽舍入给出 `C_max≤2T`。因此在本文的阈值意义下，固定轮 literal-SA 的全类上确界间隙恰为 2；“恰为 2”仍只关于这个松弛，不是主问题的复杂度下界。

## 伪分布证明

对每个至多 `r` 个任务的 literal 事件 `Λ`，令 `Q` 为其中涉及的任务集合，`q=|Q|`。令

\[
A_\Lambda=\{\phi:Q\hookrightarrow[m]:\phi\text{ 满足 }\Lambda\}.
\]

定义 `y_Λ=|A_Λ|/(m)_q`；若没有满足事件的局部注入则置 `y_Λ=0`。注意两个不同任务被指定到同一机器在原调度模型中并不矛盾；这里只是本伪分布主动给这类局部事件权重 0，以便容量期望变成注入统计。对于同一任务的互相冲突 literal，`A_Λ` 自然为空。于是 `y_Λ` 是满足 `Λ` 的均匀注入

\[
\phi:Q\hookrightarrow [m]
\]

的概率。这里“注入”只是一种构造伪分布的局部统计；原调度允许同一机器接多个任务。所有 `y_Λ` 非负，且 `y_∅=1`。事件的可满足性由 `A_Λ` 的定义决定，不能仅凭文字上没有冲突就假设有注入见证。

对任意 `|Λ|≤r-1` 和未在 `Q` 中的任务 `j`，每个满足 `Λ` 的注入都有恰 `m-q` 个把 `j` 加入注入的扩展，故

\[
\sum_i y_{\Lambda\wedge(x_{ij})}=y_\Lambda.
\]

若 `j∈Q`，这是逐个注入上的恒等式。因此所有 assignment 等式及其 literal 乘式都成立；同一任务的互补、上下界和空事件也由同一局部分布直接满足。

现在核对容量乘式。固定一个 `Λ` 且 `y_Λ>0`，在满足 `Λ` 的均匀注入上取条件期望。对机器 `i`，已查询的 `q` 个任务至多有一个占据 `i`；每个未查询任务在 `i` 空闲时以概率 `1/(m-q)` 被加入。于是

\[
\begin{aligned}
\mathbb E\left[\sum_j x_{ij}\mid Λ\right]
&=\mathbb E_\phi\left[\mathbf1_{i\in\operatorname{im}\phi}
 +(m+1-q)\frac{\mathbf1_{i\notin\operatorname{im}\phi}}{m-q}\right]\\
&\le \max\left\{1,\frac{m+1-q}{m-q}\right\}
=1+\frac1{m-q}\\
&\le 1+\frac1{m-r+1}=T_{m,r}.
\end{aligned}
\tag{2}
\]

故 `y_Λ(T_{m,r}-\sum_j x_{ij})≥0`，即每个容量不等式及其所有允许的 literal 乘式均满足。若 `y_Λ=0`，线性化乘式按同一局部事件概率定义为 0。由此得到完整的 `SA_r(T_{m,r})` 可行伪解，而不只是原 assignment LP 可行点。

## 整数值、位复杂度和范围

`m+1` 个 unit 任务放在 `m` 台机器上时，鸽巢原理给 `C_max≥2`；把两任务放在一台、其它各放一台达到 2，所以 `OPT=2`。式 (1) 随 `m→∞` 趋近 2。所有输入时间都是整数 1，阈值分母为 `m-r+1`，其二进制位长为 `O(log m)`；这里没有枚举、伪多项式循环或数值近似。

这个实例的 configuration-LP 在任何 `T<2` 时立即不可行，因此本命题不声称配置层也有同样间隙；它只说明固定 literal 局部化不能替代跨机器完整配置。它也不限制随 `m` 增长的层数、Lasserre/SOS、配置型联立约束，或直接利用原矩阵构造调度的算法。由于本族调度显然可直接求出，命题不是 `P≠NP` 意义的困难性证明。

**Status：** 固定层局部松弛的完整参数化证明，未用有限枚举；主目标 `UM-TARGET-v1` 仍 OPEN。任何真正的统一改善必须使用固定层之外的全局信息，或证明一个不同于 literal-SA 的可计算结构。
