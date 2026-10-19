# 非负列总量约束下拟阵基的逐行加 B 舍入：独立重构

此稿于收到 root 精确陈述后独立构造；截至写成，未阅读 root 或其他研究者的证明。无 canonical/Git 修改。只给 upper-only 结论，不给 lower bounds 或 cost 保持。标准拟阵交换、二进制有理 LP 是已有工具；不声称全球新颖性。

## 精确 Claim 与显式输入合同

有限显式基集 E，A∈Q_(≥0)^(m×E)，B∈Q_(≥0)，且逐列 Σ_i A_ie≤B。给定 b∈Q^m，以及 x∈B(M)∩{Ax≤b} 的显式有理坐标，其中 M 是一个给定显式二分匹配所定义的 transversal matroid 的 parallel extension：每个 e∈E 的原元素 π(e) 显式给出，同一 π-class 至多能选一元素，原元素集独立当且仅当它可在给定二分图中被匹配。全部 parallel copies 显式列出、计入输入长度；未声称对二进制压缩且未展开的 copy universe 输出显式 base。

存在确定性总位多项式算法输出 M 的一份实际 base I，满足

`A 1_I ≤ b+B·1` 逐 row。

B=0、空基、loops 与重复 rows 均允许；x 与矩阵全按二进制有理数输入。没有配置 oracle、未知好基或 contraction 的 transversal presentation 作为额外输入。

下面的舍入论证实际上对任意可位多项式优化的拟阵成立；最后一节对本 Claim 的显式匹配输入给出多项式 LP，不免费调用泛化 oracle。

## 1. 紧拟阵行的计数引理

设 N 是 n 个剩余元素上的拟阵，rank 为整数 r，y∈B(N) 且每个 0<y_e<1。因此 0<r=Σ_e y_e<n。

记紧集族 `T={S⊆E:y(S)=r_N(S)}`。它含 ∅、E；由 rank 次模性与 y 模性，T 对并与交闭合。取 T 中一条不能再细化的 inclusion chain

`∅=S_0 ⊊ S_1 ⊊ ... ⊊ S_t=E`，块为 D_j=S_j\S_(j−1)。

每个块非空且 y(D_j)>0，又

`y(D_j)=r_N(S_j)−r_N(S_(j−1))`

为整数，所以 y(D_j)≥1，得 t≤r。

任意紧集 T 都是这些块的并：若某块 D_j 被 T 非平凡切开，则紧集

`S_(j−1) ∪ (T∩S_j)`

严格位于 S_(j−1)、S_j 之间，与不可细化性矛盾。故全部紧 rank inequalities 的法向量均在 t 个 block 指示向量的线性包络中，维数≤t≤r。基的总量等式由 E 紧集包含在内。非负坐标界在全分数点处不紧；上界 y_e≤1 属于 rank 约束，而且也不紧。

## 2. 必有一条可安全放弃的 upper row

考虑当前 residual polytope

`Q=B(N)∩{A' y≤b'}`，

其中 A' 只含尚未放弃的原 rows、尚未固定的原列，仍非负、逐列总量≤B。取 y 为 **Q 在原元素坐标中的一个投影顶点**，并假设所有坐标均严格分数。

一个 n 维坐标空间中的顶点，其全部紧约束法向量张成 n 维。第1节表明紧拟阵行至多贡献 r 维，故至少有 n−r 条不同紧 A' rows。记这些紧 rows 的集合为 H；|H|≥n−r≥1。

对 i∈H 定义残留全选亏缺

`F_i=Σ_e A'_ie(1−y_e) ≥0`。

列总量条件给

`Σ_(i∈H) F_i ≤ Σ_e B(1−y_e) = B(n−r)`。

因此至少一条紧 row i 满足 F_i≤B。删去此 upper row 安全：以后任何 0/1 residual 选择 z 都有

`A'_i z ≤ Σ_e A'_ie = A'_i y+F_i = b'_i+F_i ≤ b'_i+B`。

这个结论只使用 z_e≤1 与非负系数，不需要对未来方向、未来基或未来 LP 顶点作额外承诺。

## 3. 迭代算法与所有原 rows 的保证

维护已选固定集 F、已删元素 D、尚存 upper rows。初始 F=D=∅。保留当前 polytope 的可行性，反复执行：

1. 取当前 base-minor 与 upper rows 交的一个元素坐标投影顶点 y。
2. 若有 y_e=0，则删元素 e；若有 y_e=1，则选入 F 并收缩 e，同时对每个尚存 row 将 residual RHS 减去 A_ie。一次可只处理一个元素。
3. 若全部剩余坐标严格在(0,1)中，用第2节找 F_i≤B 的紧 upper row，删去这条 row。

固定 0 或 1 是当前非空可行 face，删 row 只扩大可行域；所以不发生中途无解。循环每步删一元素或一 row，至多 |E|+m 步。元素清空时，F 为原 M 的一份实际 base。

某原 row i 若从未被删，最终自然满足 A_i1_F≤b_i。若它在时刻 t 被删，当时已固定元素为 F_t、剩余元素为 R_t、分数点为 y_t，则

`A_i1_(F_t)+A_i y_t=b_i`，

`Σ_(e∈R_t) A_ie(1−y_te)≤B`。

以后最终 F 的新增元素只是 R_t 的某个子集，所以

`A_i1_F ≤ A_i1_(F_t)+Σ_(e∈R_t)A_ie ≤ b_i+B`。

删 row 后以后固定元素不需要继续维护此 row 的 LP；上式已经为所有未来补全给出同一份原 row 证书。这也说明不能据此声称 lower 或 cost 保证。

## 4. 显式 matching 与 parallel copies 的位多项式实现

设给定二分图左侧 L，右侧为原元素 V=π(E)，边集 G。原基 rank r_0 为该图最大匹配大小，可由单位容量整数流确定性求出。给变量 x_e≥0 及匹配边变量 z_(ℓv)≥0，约束

`Σ_(ℓ:(ℓ,v)∈G) z_(ℓv) = Σ_(e:π(e)=v) x_e`（每 v），

`Σ_(v:(ℓ,v)∈G) z_(ℓv) ≤1`（每 ℓ），

`Σ_(e:π(e)=v) x_e ≤1`（每 v），

`Σ_e x_e = r_0`。

它是标准整数容量 bipartite flow 加上各 parallel-class 容量1的多项式 LP；其 x 投影恰 B(M)。可直接看成匹配流从原元素 v 再分流至各 copy e：整数顶点选恰一 copy，全部大小 r_0 的匹配给出所有原基。所有 copies 显式，LP 变量与约束数是输入长度多项式。

在整个算法中保留这份**原** extended formulation，只对已固定坐标加 x_e=0 或 x_e=1；再加尚存 upper rows。投影即所需的 minor-face，不必假称 transversal matroid 在 contraction 下仍属于同一呈现类，更不必构造 contraction 的新 matching presentation。

为得到第2节所需的 x 投影顶点，不能仅任取 extended LP 顶点。可以对尚未固定的 x 坐标按编号逐一 lexicographically 最小化：每次用确定性二进制有理 LP，固定上一步的精确最优值，再优化下一个坐标。最后 x 在当前投影中唯一，因而是该投影的一个顶点。最后 z 是否唯一无关。

每个外循环至多 |E| 次 LP、至多 |E|+m 次外循环。全部 LP 均由同一份有理匹配网络、原 A、固定 0/1 及当前 lex 最优 faces 构成。lex 坐标都是当前原投影顶点的坐标，可由原多项式规模 extended polytope 的顶点取得；标准 Cramer determinant 位界给这些值的多项式位长。fixed-one RHS 的减法也只累加输入中至多 |E| 个有理数。因此循环数与中间位长均多项式，不按 1/B、系数倒数或分母数值迭代。

紧 row、F_i 与 0/1 坐标均以精确有理比较识别。证明中的 tight-set chain 无需被算法找到或枚举；它仅用于保证显式 rows 中必有可删的一条。B=0 时非负列总量迫 A=0，算法仍适用；也可直接输出任意最大匹配对应基。rank0 输出空基。

## 5. 常数 B 的渐近锐性

B>0 时取 rank1 uniform/transversal matroid（一个左 slot、m 个右元素均相邻），A=B·Id_m，x_e=1/m，b_i=B/m。每列总量恰 B，给定分数点可行；任一实际基都选一个元素，在对应 row 产生

`A_i1_I−b_i = B(1−1/m)`。

故不存在对全部这类输入将 +B 替换成统一 +cB、c<1 的结论。这个族不涉及 lower/cost，也不声称有限 m 必须正好达到 +B。

## 独立性与未检事项

本文件只独立证明所给 upper-only exact Claim；不提前查看 root 或其他证明。数学论证已闭合，软件 LP 舍入器未实现。若 root 的 parallel copies 实际指另一种 independence 规则，必须先按其精确定义重查；本稿明确使用同原元素各 copies 互相平行这一标准含义。
