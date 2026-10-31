# LST affine-line uniform 菜单编译：独立 Exact-first 审查

对象：`lst2025_affine_line_source_uniform_menu_compilation_exact_v1.md`。

Exact SHA-256：`a1334a82f1acf7fd9562c2d44e6620b84b5a1acd37993ce3c7131b81a8e56472`，已实际全文读取并核验。

读取隔离：只读取该 Exact，未读作者 Proof、root 推导或其它 agent 推导。数学重构先独立完成，随后才实际核 primary v1。未写 repo、Work 或 Git；仅 scratch 记录。未实现软件、未做有限枚举。

**判定：Exact 的明确非空菜单域内，allocation (A)、完整 actual UM 上界 (B)、counts/bit complexity 与 scope 均通过，无 standing fatal。** 数学是 pair-overlap union bound 与 Hall 的直接应用，不是新 Hall 定理或新一般近似框架。

## 1. 独立几何核对：degree 与 intercept 都不可省

固定任意完整选择 s(g)∈A_g；不同 constraints 的 local tuples 可以完全不一致。对变量 x，每个包含 x 的 indexed constraint g 贡献一条

    E_xg={(x,z,s(g)(x)z+j_x(g)):z∈F_R}。

每条 line 恰 R 个不同资源，因为坐标 z 自身不同。变量 tag 不同的资源永远不合并。每 constraint 含 k 个不同变量，故每 selected state 恰 kR 个资源。

若 g≠h 都包含 x，则 j_x(g)≠j_x(h)，这是按 indexed constraint incidences 的注入，不按 allowed tuples 数量编号。即使两个 constraints 内容或 tuple 表完全相同，也不能给相同 incidence index。

- 若 selected slopes 相同，两条线相交会强迫 intercept 相同，矛盾，故交集为空。
- 若 slopes 不同，(s(g)(x)-s(h)(x))z=j_x(h)-j_x(g) 在 prime field 中恰一解，故交集恰一资源。

于是任意两条不同 selected incidence lines 在同一变量处交集≤1。仅仅不同 slopes 不足以处理同 slope 情形；intercept 注入确保没有相同 line。degree≤R 又保证编号 1,…,d_x 在 F_R 中确实注入，包括 d_x=R 时 R 代表 0。

## 2. 对全部 Hall 子集的量词证明

令 b=ceil(kR/2)。取**任意** H⊆G，不只取全部 G。对每变量令

    r_x=|H∩G(x)|，0≤r_x≤d_x≤R。

H 在 U_x 内选中了 r_x 条 line。由每条 R 点、两两交集≤1 的二阶容斥下界，

    |⋃_{g∈H:x∈X_g} E_xg|
      ≥r_x R-binomial(r_x,2)
      =r_x(2R-r_x+1)/2
      ≥r_x(R+1)/2。

多线共点不使这个下界失效：一点出现 q≥1 次，对二阶计数贡献 q-binomial(q,2)≤1，故二阶计数仍不超过真实 union 大小。r_x=0 时该式为 0。

不同 x 的资源带 tag，不相交；每个 g∈H 恰有 k 个不同变量，所以 Σ_x r_x=k|H|。因此选中 group-resource 图的邻域满足

    |N(H)|≥Σ_x r_x(R+1)/2=k|H|(R+1)/2≥b|H|。

最后 ceiling 精确成立：若 kR 偶数，b=kR/2；若 kR 奇数，b=(kR+1)/2≤(kR+k)/2，因为 k≥1。空 H 平凡满足 0≥0。这里得到每个 Hall 子集的条件，绝非以整个 pool 的总资源数代替局部条件。

## 3. 精确整数 allocation 与任意 local tuples

把每 group 复制成 b 个 unit demand clones，邻接同一 selected state 的 kR 个真实资源。任意 clone 子集 C 所触及的原 groups 为 H，则 N(C)=N(H)，且

    |N(C)|≥b|H|≥|C|。

普通 Hall matching 覆盖全部 clones，合并每 group 得两两不交 B_g，且每 |B_g|=b。等价可用 source→group capacity b、group→resource、resource→sink capacity 1 的整数 flow；资源 sink 容量保证一个真实资源至多一个 owner。

该推导没有要求 local labels 来自全局 CSP assignment，不利用 source YES/NO，也不要求 B_g 分解成每变量半条 line 或 Cartesian 子集。每组领取的是自由的全局 partial subset。所有 A_g 非空时任取每表第一 tuple 就能启动。

b≤kR，每组 clones 数≤kR。因 a=Σ|A_g|≥m=|G|，总 clone 数 mb≤mkR≤kRa=L，故此构造不会隐藏超出显式 incidence 总量的数值复制。

## 4. 所有原 jobs 的实际普通 UM 调度

P 每 state 有 kR 枚 private time 1/(kR) 的 distinct 原 incidence，总工作恰 1。把 J_g 放 selected M_g,s(g)，仅导出该 state 的 B_g 对应 jobs；所有其它原 incidence，包括每个 unselected state 的所有 jobs，留自己 private machine。

每个原 job 恰一次且在原有限端。资源机器至多一枚 unit，负载≤1；未选 private 负载精确 1；选中 private 负载

    1+(kR-b)/(kR)=2-b/(kR)≤3/2。

kR≥2，所以上式≥1，足以覆盖其它机器的 1。实际时间表可在选中 private 先排 selector、再逐枚排留下的 incidences；其余 private 串行、resource unit 从 0 开始。所有时刻都是整数/(kR)，全原任务的非抢占排程可显式输出。

因为 G 非空，selector 给 OPT≥1，故 absolute C≤3/2 也蕴含同一实例的 approximation ratio≤3/2。它只覆盖此精确 uniform compiler，不使 source set packing/CSP 本身变容易。

若另给真正满足全部 constraints 的全局 CSP assignment，其 local tuples 在每共享变量的 slope 相同、不同 indexed constraints 的 intercept 不同，selected lines 即平行不交；不同变量又有 tag。所以全部 selected states 两两不交，可全部导出，得 C=1，selectors 又给 OPT=1。但 near-perfect val≥1-ε 并不提供该 stronger witness。

## 5. 空 relation 与其它边界

- A_g=∅ 不在合同内：保留 J_g 而不给 state machine 会令它无合法端，P 不可行。source set packing 没有该 constraint 的 set，不等于这里可合法删除 selector 或免费加 dummy state。
- 删除空 constraint 会改变 source 归一化 value；加 state/改编码也可能改 soundness，均须另证。当前 Exact 没有掩盖该接口。
- k=1、R=2 合法，ceiling 及 Hall 链仍成立；合同不把 source hardness 的 k≥4 要求倒灌进纯组合 allocation 域。
- R odd、k odd 的 ceiling 已逐项处理，不能仅给 floor(kR/2)。
- 未使用变量、d_x=0 的 tagged资源池可为空参与集/机器闲置，不影响 sums 或完整调度；G 保持非空。
- 同 constraint 内变量重复会破坏 Σ r_x=k|H| 及 kR distinct resources；当前明确禁止。相同内容的不同 indexed constraints 则允许，依 intercept 注入仍合法。
- 若放弃 prime field、intercept injectivity、degree≤R、变量 tags 或 uniform 权，当前证明不自动延伸；不将该局部应用包装成任意源 compiler 的不可能性。

## 6. Primary PaperFact 的实际读取

实际打开：[arXiv:2409.17831v1 PDF](https://arxiv.org/pdf/2409.17831v1)。PDF 版本头为 v1，十四页；未下载 raw PDF，故不声称本地 raw 文件或 hash。实际读取 §2 Definition 2.1、§3 Theorem 3.1/Claim 3.3/完整 gadget 与匹配对应证明，以及 §4 Theorem 4.1 与正文。未依赖 abstract 作证。

核对结果：定义允许任意 relation；§3 用 prime R、R-degree bounded CSP、label 为 slope、constraint incidence 的一一编号为 intercept，并保留 kR-set matching 与满足约束数；时间按 R^k 计。§4 的声明确为 k≥4、充分大 prime R、YES≥1-ε、NO≤k(1+ε)/((k-3)R)，并保留 NP⊆BPP 的例外。没有从这些文字得到 perfect completeness、partial-subset hardness 或只需 P≠NP 的版本。

这段 PaperFact 是对 primary 中所述对象/定理/证明位置的核验，不是本审查重新认证整篇外部 hardness 证明。当前 Hall allocation 的数学推导本身不依赖 source hardness。

## 7. 完整矩阵规模与 binary complexity

v=|X|、m=|G|、a=Σ|A_g|。资源机器 vR²、private machines a、incidence jobs L=kRa、selectors m；每 incidence 两个 finite ends、selector finite ends 总和 a，所以 sparse finite entries 精确 2L+a。dense P 为 (vR²+a)(m+L)。未选 states 的 jobs 在 L 中全部计入，没有按 selected states 缩减原矩阵。

时间 1/(kR)、field 元素、variable/group/state/resource/job identifiers 均有二进制多项式位长。模域加乘只涉及 O(log R) 位整数；显式枚举 vR² resources、a 个 kR 支持及所有 m+L 原 jobs 的成本按已列完整 output length 收费。matching network 是其多项式大小，整数 flow 输出与有理开始时刻同样如此。

这不等于 polynomial in log R 的 succinct 编译，也不保证当 R 以二进制输入且任意增大时 source-to-explicit-P 在原 source 输入长度上多项式；Exact 已把固定 source k,R 情况与显式 output 计费分清。固定 k,R 时才直接是普通 source 输入大小的多项式编译。primary 的 poly(V,E,R^k) 也没有免费提供 succinct 生成。

## 8. 冻结结论

**Exact-only 通过，无 standing fatal。** 任意 selected local tuples、injective intercept、degree≤R、全部 Hall 子集、ceiling、所有原 jobs、空 relation 及 explicit binary counts 均闭合。作者 Proof 尚未披露给本审查；可在本记录冻结后再转 Proof 做 read-after。
