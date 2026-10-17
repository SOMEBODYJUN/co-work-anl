# 私有树配置间隙随叶资源重数的一阶锐渐近（仅陈述）

读取目的：供独立研究者在未读本命题证明前重构。本文不含 λ 证书、最优负载证明或渐近证明。

Candidate ID：`UM-PRIVATE-TREE-MULTIPLICITY-GAP-ASYMPTOTIC-v1`。

## Objects / Domain / Definitions

对整数 μ≥2，令 C_μ 为下列所有有限显式调度输入 P 的类：

- 整数 d,h≥1，非空有限 root 集 U，每 u 有非空有限显式 state 菜单 S_u。
- 每 state 为完全私有的满 d 叉高 h 树，内部机器深 0,…,h−1；不同 states 内部机器也互异。共享有限外机集合 Z。
- 每 u 一枚 unit selector，合法端恰为该 u 的全部 state 根；每内部 edge job 父端时间1/d、子端时间1；每 leaf job 父端时间1/d、唯一外机端时间1，外机由显式 f_us:[d]^h→Z 指定；其它端∞。没有其它 jobs、预载或时间。
- 每个**完整 state** 的每个资源实际重数不超过 μ：`|f_us^{-1}(z)|≤μ`。不同 states／roots 间可任意共享外资源。
- 全部状态、机器、jobs 和叶资格显式给出，不能用 binary d,h 代替巨大树展开。

CONFIG(T) 为完整原 P 的普通配置 LP（每机器权重和1，每 job 恰覆盖1，配置负载≤T），T_conf(P) 为其最小可行阈值／可行阈值下确界。非空 selector 使 T_conf(P)≥1，故下面比值良定义。

定义参数类的最坏配置整数间隙上确界

\[
 G(\mu)=\sup_{P\in C_\mu}
 \frac{\operatorname{OPT}(P)}{T_{\mathrm{conf}}(P)}.
\]

上确界同时遍历 d,h、root 数、菜单、外机集合、全部映射及所有有限显式输入长度；μ 仅约束每个完整 state 内的重数，不要求其它参数固定。不声称上确界对每个 μ 都达到。

## Exact Statement / Quantifiers / Conclusion

对每个整数 μ≥2，

\[
 2-\frac1\mu\ \le\ G(\mu)\ \le\ 2-\frac1{\mu+2}.
\]

因而，沿整数 μ→∞，

\[
 \lim_{\mu\to\infty}\mu\,[2-G(\mu)]=1.
\]

等价的误差界为

\[
 0\le G(\mu)-\left(2-\frac1\mu\right)
 \le\frac{2}{\mu(\mu+2)}.
\]

这是叶资源重数参数的一阶锐渐近，不给每个固定 μ 的精确 G(μ)，也不声称各固定 μ 上界 `2−1/(μ+2)` 锐利。

## 显式下界族的对象参数

对每个 μ≥2，取 d=μ、h=1、U={u}，该 root 恰有 μ 个 states s=1,…,μ。外机为 μ 个不同资源 z_1,…,z_μ。state s 的全部 μ 个 leaf jobs 都映到 z_s。内部机器仅为 μ 个 state 根，selector 一枚；每枚叶在其 state 根时间1/μ、在 z_s 时间1。没有其它 jobs 或端。

该族在 C_μ 中，具有精确比值 `OPT/T_conf=2−1/μ`，给上面的下界。这里只陈述该族和准确结论，不附分数证书或实际最优调度证明。

## Dependencies / Scope / Status / Related Files

- 上界依赖新 `UM-Q-PRIVATE-TREE-BOUNDED-MULTIPLICITY-CONFIGURATION-FLOOR-v3` 的全 CONFIG(T) 上界；该一般证明、独立审查状态须独立登记，本命题不靠有限 μ 试算证明。
- 下界是上述显式平星族的精确分数／整数分析，不是 NP-hardness、搜索困难性或 UM-TARGET-v1 的反面。
- 没有产生一般位多项式输出 σ 算法。此处比值是有限显式 P 的配置整数间隙，不能混作算法近似比。
- 状态：作者推导完成，Exact-only 新冻结；尚待本项独立陈述先行重构和全文读后攻击；没有新代码或有限运行证据，新颖性未认证。
- 相关冻结文件：`private_tree_bounded_multiplicity_floor_v3_exact_statement.md` 及另冻 proof。旧 v3 Exact／proof 原字节不动；拟在同一现行正文中保存，避免复制资产树。
