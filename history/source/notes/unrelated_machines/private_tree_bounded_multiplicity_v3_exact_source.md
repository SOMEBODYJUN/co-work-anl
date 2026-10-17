# 有界叶资源重数私有树：全配置阈值的常数离二界（仅陈述）

读取目的：供尚未读作者证明的独立研究者按精确陈述重构。本文不含证明。

Candidate identity：`UM-Q-PRIVATE-TREE-BOUNDED-MULTIPLICITY-CONFIGURATION-FLOOR-v3`。v3 为相对注入状态 v2 的新对象／新量词，不倒改 v1/v2 冻结字节。未登记 canonical，未认证新颖性。

## Objects / Domain / Quantifiers / Assumptions

任意整数 d,h,μ≥1。μ 允许作为二进制输入，不预设固定；“统一常数离二”仅在 μ 固定时解释为与其它输入无关的常数。有限非空 root 集 U，每 u 有非空有限显式状态菜单 S_u；共享有限外机集合 Z。

每 (u,s) 是完全私有的满 d 叉高 h 树，深 0,…,h−1 为内部机器，叶地址为 [d]^h；不同状态内部机器也不共享。完整普通调度输入 P：每 u 一枚 unit selector，其全部合法端恰为各状态根；每内部 edge job 父端时间 1/d、子端时间 1；每 leaf job 父端时间 1/d、唯一外机端时间 1，其外机由显式 f_us:[d]^h→Z 给出。其它端∞，没有额外 jobs、预载或其它有限时间。

全部状态、机器、jobs 和 leaf 资格都显式列出。**不要求 f_us 单射**，而要求每个完整状态的每个资源实际重数均有同一个上界：

\[
 |f_{us}^{-1}(z)|\le\mu\qquad(\forall u,s,z).
\]

不同状态／root 间可任意共享资源；μ 不限制跨状态总重数。

CONFIG(T) 是完整原 P 的通常配置 LP，配置负载≤T，每机器权重和 1，每原 job 覆盖恰 1；向下封闭下与至少覆盖版等价。非空 U 的 selector 保证 OPT,T_conf≥1。空 U 仅作单独空任务情形，不套该下界。

## Definitions

一个真实 state 中的满 r 叉高 h 子树称为 **rainbow**，当且仅当其 r^h 个叶映到 r^h 个互不相同的实际外机。选出子树必须包含该 state 的原根并在每一活跃内部节点恰选 r 个原 children，不能逐路径更换 state。

对任意满 a 叉高 h 抽象树的叶子集 A，q(A) 为 A 中所含满 r 叉高 h 根子树的最大整数 r∈[1,a]；若不存在则 q(A)=0。这个辅助定义仅用于精确解释下列局部陈述。

## Exact Statements

### L. 局部有界重数 rainbow 与资源 blocker 下界

任意整数 a,h,μ≥1，给满 a 叉高 h 树任意叶资源映射 f，每资源在该整树出现至多 μ 次。

1. 存在满 `ceil(a/μ)` 叉高 h 的 rainbow 子树。特别地，μ=2、a=3 时，对任意 h≥1 均存在 binary rainbow 子树。
2. 对任何整数 r∈[1,a] 且 μ(r−1)<a，任意资源集合 X 若命中该树中**所有 rainbow 满 r 叉高 h 子树**的资源像，则

\[
 |f^{-1}(X)|\ge [a-\mu(r-1)]^h.
\]

第二项仅声称下界，不声称对所有 a,r,h,μ 都达到等号。计数对象是原叶逆像的 multiplicity，不是把一个资源直接当作一个叶。

### A. 共同 full-state 分数点的实际离二存在性

给共同非负有理 λ_us，满足

\[
 \sum_{s\in S_u}\lambda_{us}=1\quad(\forall u),
 \qquad
 \sum_{u,s}\lambda_{us}|f_{us}^{-1}(z)|\le1\quad(\forall z).
\]

所有资源行必须来自同一份 λ，按实际 multiplicity 计。则对每个整数 r∈[1,d]，若

\[
 \mu(r-1)<d,
 \qquad[d-\mu(r-1)]^h\ge2r^h-1,
\]

存在对每 root 选一个真实状态及其中一个 rainbow 满 r 叉高 h 子树，使全部选中叶资源在所有 root 间也互不相交。完整原 P 存在实际合法 σ，满足

\[
 C_{\max}(\sigma)\le2-r/d.
\]

所有未选 state、未选分枝和零 λ state 的原 jobs 均在该 σ 内。

### B. 全部 CONFIG(T) 阈值与配置整数间隙

对任意有理 T∈[1,2)，若完整原 P 的 CONFIG(T) 可行，设

\[
 s=\lfloor d(T-1)\rfloor,\qquad a=d-s\in[1,d].
\]

对任何整数 r∈[1,a]，若

\[
 \mu(r-1)<a,
 \qquad[a-\mu(r-1)]^h\ge2r^h-1,
\]

则完整原 P 存在真实状态／rainbow 满 r 子树的全 root 不交选择，及实际合法 σ 满足 Cmax≤2−r/d。

特别取

\[
 r=\left\lceil\frac{a}{\mu+2}\right\rceil,
 \qquad\alpha_\mu=2-\frac1{\mu+2},
\]

对所有这些参数均满足上述数值前提，且

\[
 \operatorname{OPT}(P)
 \le2-r/d
 \le\alpha_\mu(1+s/d)
 \le\alpha_\mu T.
\]

T≥2 时有完整实际 C≤2 的直接调度，补齐全部配置阈值。因此此有界**每完整 state 叶资源重数**结构类的配置整数间隙至多 α_μ；μ=1 恢复 v2 的五三上界，μ=2 给七四上界。α_μ 是已证候选上界，不声称锐利。

## Dependencies / Evidence / Scope / Status

- 已有 v2 的小型精确 CONFIG 边际系统和 CONFIG(T) 向每 root 同一真实 state 的 a 叉树分布支配桥，本身不需要单状态 leafmap 注入；此事实必须按原证明条件使用，不把所有原 LP 当作全局整数调度分布。
- 已登记／审查的单树 q 子可加性、精确 raw 叶 blocker 数、Haxell 有限二部超图匹配条件可能作为外部或前置依赖；本 v3 的 rainbow 限定、multiplicity 加权和完整原 P 回填须重新证明，不能把 raw r 子树直接当成 rainbow 候选。
- 本文给实际 σ 的**存在性**；不声称在任意变参 d,h,μ 下已实现或已证明总位多项式输出 σ。配置 LP 的小型系统和确定性位多项式可行性属于 v2 已审结论，不能替代 σ 构造。
- μ 固定时 α_μ<2，但结构域仍远小于一般 UM；μ 随输入无界时不产生统一离二常数。共享内部机器、异构树、非均匀 processing times、多单位叶端、额外 jobs 与预载不在范围。
- 这可限制始终产生本结构及共同 CONFIG(1) 的近二困难性编译，不证明 UM-TARGET-v1 的正面或反面。
- 状态：新 Exact-only 候选；作者已独立推导，证明另冻；尚无本 v3 的陈述先行独立重构、全文读后审查或有限生产实现；新颖性未认证。
