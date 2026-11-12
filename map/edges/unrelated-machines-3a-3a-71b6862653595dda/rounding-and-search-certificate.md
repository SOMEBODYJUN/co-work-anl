# BLMRS 局部搜索：舍入收尾与证书、递归计数的精确审读

## 对象和阅读范围

核心是当前 v2 对象 `M-a3feff9f6a574834925528d0f9d9d658`：每固定正精度下，restricted resource-matroid Santa Claus 有一般值的 `(8+epsilon)` 近似和两值的 `(4+epsilon)` 近似。比较端是当前 v2 减最大项舍入 `M-737cbc9ea3b54c03b847026018cf5b19`，及当前 v2 两值近似双向归约 `M-e7c107d268344ca592782a71e1925647`。

实读冻结 PDF（SHA256 `fc907ac5159b3b20ae8498052c161f7aaf8d64114db84d7ef1947d6f1c6d4183`）的定义、Proposition 9、Section 3 的 Lemma 15、Appendix D 的 Lemma 16、Section 4 完整算法、Appendix E 的 Theorems 21/23 与 Lemma 22，以及 Appendix F 的 Lemmas 24--37 和运行时间段。本文页码以下统一用印刷页码；对应 PDF 页码加一。另完整读当前舍入端点的严格替代证据 `archives/unrelated-machines/tools/evidence/boss2-6405-blmrs-proof/rounding-slots-and-dual.md`，不复用冻结 v1 错误的相邻资源图作为舍入证明。

本次逻辑边只交付下一节的已给中间见证舍入贡献。随后给出的证书与递归计数修复是独立可审核的数学证明，明确列出从原局部搜索调用的结构不变量；不以它们冒称舍入定理单独推出整条局部搜索结果。

## 给定重轻中间见证后的完整舍入收尾

设原资源的公共非负有限有理值为 `v_j`，每项的合法分配是其归一化单调整数次模秩所定义 polymatroid 的整数基。固定 `V>0` 和 `alpha>=2`。设原项被分为互不相交的重项 `H` 和轻项 `L`，每项重资源值至少 `V/(2alpha)`，每项轻资源值小于 `V/(2alpha)`。

输入中间见证包括：原重项的合法整数独立向量，使玩家集合 `W` 的每个人至少收到一个重资源单位；未覆盖玩家 `U=E\W` 的原轻项合法分数独立向量，使每个 `i in U` 的轻项总值至少 `V/alpha`。这里不要求重资源覆盖者有轻值下界，也不要求规范子问题中的无穷值项满足有限最大值条件。

先逐项把重资源独立向量补成原整数基；非负值不减少 `W` 收益。对每个轻资源限制到地面集 `U`，其给定分数向量仍是合法独立向量。将其补成限制 polymatroid 的分数基，再调用减最大项舍入，得到 `U` 上的整数独立/基向量，每人值至少

`V/alpha - max_{j in L} v_j >= V/(2alpha)`。

将每个轻资源的该整数向量在原地面集上补成原整数基，`U` 的值不下降；重项的分配已固定，轻重项没有重复使用。每个 `i in W` 已从重项获得至少 `V/(2alpha)`，所以最终全体玩家均达到该值。`U` 为空时只需补基；`L` 为空而 `U` 非空时正阈值见证不存在，不伪造可行性。补基及 oracle 操作的位复杂度由当前严格舍入证据的逐坐标次模最小化构造保证。

两值实例另一个独立分支也确实用到舍入：若已给整体分数基见证、每人值至少 `V`，最大资源值为 `w<V/alpha`，则舍入给每人至少 `V-w>V(1-1/alpha)>=V/alpha`。最后一步恰使用 `alpha>=2`。这不能替代两值实例的小阈值/中阈值分支，更不能替代规范 `M/P` 子程序的失败证书。

因此，一旦规范算法、解码与阈值搜索已给上述见证，取其保证 `alpha=4+epsilon/2`，一般值收尾就是 `2alpha=8+epsilon`。两值 `4+epsilon` 需要 Lemma 22 的另一组分支。这里的任意精度参数应与下一节算法内部的小参数区分。

## 冻结 v1 的 C 定义冲突及最小改法

原算法在印刷页 15 列出 `A subset C subset I_M`，在印刷页 16 却将 `C` 印为

`B_0 union A union {i in I_M\A : f(i | 2b A)<2b}`。

后文又用 `E'=E\C`、`B_0'=B_0 union B`，并返回 `I_M=C union I_M''`。由于输入的 `B_0` 与 `I_M` 不交，上述印式会把 `B_0'` 排除在 `E'` 外，也不保证返回的 `C` 独立。Lemma 27 的证明、Lemma 29 的可行性证明和 Lemma 30 的递归输入均需要 `C subset I_M`。应改为

`C := A union {i in I_M\A : f(i | 2b A)<2b}`。

这删除错误的 `B_0 union`，保留全部原 addability 条件。本页下文均使用这个修正后的 `C`。它是原文内部可直接定位的公式冲突，不是否定主近似定理的反例。

## A 为空时的必要终止分支

还须显式处理 `A=empty`。原操作 2 的成功触发式是 `|A_I|>=e|A|`，此时变成 `0>=0`，但没有释放任何 matroid 元素，可能并未覆盖新的 `B_0` 元素。

准确的小例是 `E={a,b}`、`M=U_(1,2)`、`I_M={a}`、`I_P=empty`、`B_0={b}`、小项 polymatroid 的秩恒为零，阈值 `b=1`。两元素最初均非 loop，故该输入可以在外层先成功加入 `a` 后出现。此时 `r(B_0|I_M)=0`；无元素通过 `2b` 的 addability 测试，所以 `A=empty`、`C={a}`、`A_I=B=empty`。操作 2 会触发，却既没有移出 `a`、也不能把 `b` 加入 rank-one matroid，不能满足输出的正覆盖要求。

最小修正是在构造 `A,C` 后，若 `A=empty` 立即返回 failure；或给操作 2 添加 `A!=empty` 的条件，让操作 3 处理空阻塞集。该 failure 有下节 combined 证书 `Z_1=C,Z_2=empty`：`r(B_0 union C)<=|C|+2e|B_0|<|C|+3e|B_0|`，而对 `C` 的 `<2b` 边际条件正是其定义，空集合的好元素比例条件为空真。故该修正保留原 failure 合同，不是额外未经证实的拒绝。原 Lemma 33 的严格不等式只在非空阻塞阶段使用；空 `A,B` 的边界由本分支承担。

## 修复失败证书的 combined rank 合同

令 `0<e<1/12` 为局部搜索内部参数，`c=1/2-2e`。采用原 Lemmas 24--33 的已述结构不变量，特别是：`A subset C subset I_M`，`B subset I_P`，这些集合依输入保持相关的不交性；`2b A in P`；在已排除空 `A` 的非终止阶段，`|A_I|<e|A|`、`|B|>(1-2e)|A|`；`r(B_0|C)<=2e|B_0|`；`f(i|b(A union B-i))<b` 对所有 `i in (A union B)\A_I` 成立。递归秩是 `r'(X)=r(X|C)`，递归小项函数是 `f'(X)=f(X|b(A union B))`，`B_0'=B_0 union B`。

原 Definition 34 的两个分开的 rank 条件在 Lemma 37 中不能按印式直接传递：将递归的 `+e|B_0'|` 与 `2e|B_0'|` 相加，直接给 `3e(|B_0|+|B|)`，不是印式中的 `2e|B|+e|B_0|`。Lemma 36 还残留 `C_1/C_2` 标签和 `<2b`，不能仅改名称就认为全证书已修复。下面用一个更适合归纳的 combined rank 条件取代两条分离 rank 条件。

修复证书为 `Z_2 subset Z_1 subset E\B_0`，满足

1. `r(B_0 union Z_1) < |Z_1| - c|Z_2| + 3e|B_0|`；
2. 至少 `(1-e)` 比例的 `i in Z_2` 满足 `f(i|b(Z_2-i))<b`；
3. 每个 `i in Z_1\Z_2` 满足 `f(i|2b Z_2)<2b`。

以下证明独立支付其正确性、直接失败构造及递归传递；不再依赖原错误的 rank 展开。

### 证书排除更强可行解

令 `D subset Z_2` 为不满足小边际的例外集合，`|D|<=e|Z_2|`。由 Lemma 26，`f(Z_2\D)<=b|Z_2|`。对任一更强候选解 `I_M^*,I_P^*`，假设 `I_M^*` 是 matroid 独立集，`alpha b I_P^* in P`，且其并覆盖 `E\B_0`。

写 `W=I_P^* intersect (Z_1\D)`。单调性、次模性及 capped contraction 给

`alpha b|W| <= f(W) <= f(Z_2\D) + 2b|D| + sum_{i in I_P^* intersect (Z_1\Z_2)} f(i|2b Z_2)`

`<= (1+2e)b|Z_2| + 2b|W|`。

为明确中间的 capped contraction 使用：对互不相交的 `K,D,Y`，有 `f(Y|hK)<=h|D|+f(Y|h(K union D))`。将 `K union D` 上的坐标封顶为 `h`；其在 `K union D union Y` 的秩不小于限制到 `K union Y` 的秩，而增加 `D` 使被收缩秩至多增加 `h|D|`，相减即得。另 `f(Y|K)<=f(Y|hK)`，因为封顶收缩保留的资源更多。取 `K=Z_2\D`、`h=2b` 即得所用不等式。

故

`|I_P^* intersect Z_1| <= q|Z_2|,   q=(1+2e)/(alpha-2)+e`。

覆盖性给 `|I_M^* intersect Z_1|>=|Z_1|-q|Z_2|`。若 `q<=c`，则 combined rank 条件直接推出

`|I_M^* intersect B_0| <= r(B_0 union Z_1)-|I_M^* intersect Z_1| < 3e|B_0|`。

所以它排除原 framework 要排除的 `|I_M^* intersect B_0|>=3e|B_0|`。可取

`alpha >= 4 + 16e/(1-6e)`；特别在 `0<e<1/12` 时取 `alpha=4+32e` 足够。精确代入得 `c-q=8e(1-12e)/(2+32e)>0`。

### 直接失败时构造证书

当 `|B|<e|B_0|`，令 `Z_2=A union B`、`Z_1=C union B`。这些集合不含 `B_0`。因 `C` 独立，

`r(B_0 union Z_1) <= |C|+|B|+r(B_0|C) < |C|+3e|B_0|`。

又 `|B|>(1-2e)|A|` 蕴含 `|B|>=c(|A|+|B|)`，因此得所需 combined rank 条件。小边际条件直接来自 Lemma 31；例外仅 `A_I`，其数小于 `e|A|<=e|Z_2|`。最后，`Z_1\Z_2` 包含于 `C\A`，其 `2b` 边际界由 `C` 的定义及收缩单调性给出。这里使用的确是 Lemma 31 的 `<b`，不是原 Lemma 36 印出的较弱 `<2b`。

### 递归失败时传递证书

设递归返回 `Z_2' subset Z_1' subset E'\(B_0 union B)`。定义

`Z_1=Z_1' union C union B,   Z_2=Z_2' union A union B`。

`Z_1'` 与 `C,B` 不交，`Z_2'` 与 `A,B` 不交。故

`r(B_0 union Z_1)=|C|+r'(B_0 union B union Z_1')`

`< |C|+|Z_1'|-c|Z_2'|+3e(|B_0|+|B|)`。

这至多是 `|Z_1|-c|Z_2|+3e|B_0|`，因为

`(1-3e)|B| >= c(|A|+|B|)`。

最后不等式由 `|B|>(1-2e)|A|` 得到；其最坏比率的精确余量是

`(1-3e)(1-2e)/(2-2e) - (1/2-2e) = e^2/(1-e)>0`。

小边际方面：原 `A union B` 中仅 `A_I` 例外；递归 `Z_2'` 中至多 `e|Z_2'|` 例外。封顶到同一 `b` 后的连续收缩满足并集合成，且增加被收缩集合/封顶量只减少剩余边际（Lemma 24），故其余元素在原 `f` 和 `Z_2` 上仍有 `<b`。两个例外集总数小于等于 `e|Z_2|`。对 `Z_1'\Z_2`，将递归的 `b(A union B)` 收缩增加为 `2b(A union B)` 只减少边际，再用递归 `<2b`；对 `C\A` 用其定义的 `<2b`，即得最后一条证书性质。

为使这里用到的混合封顶也可独立核对，固定被收缩集合 `K` 及其逐坐标容量向量 `q`，对 `Y` 与 `K` 不交，定义

`A_q(Y)=min_{T subset K} [f(Y union T)+q(K\T)]`。

封顶后收缩的剩余秩恰为 `A_q(Y)-A_q(empty)`，这是 polymatroid 逐坐标封顶的标准秩公式。对不交集合连续封顶、收缩，嵌套最小值合并为对两集合并的同一个最小值，故相同容量的收缩严格可合成。若 `q<=q'`，取分别实现 `A_q(Y)` 和 `A_q'(empty)` 的 `T,U`；次模性及逐坐标容量比较给

`A_q(Y)+A_q'(empty) >= f(Y union T union U)+q'(K\(T union U)) + f(T intersect U)+q(K\(T intersect U))`

`>= A_q'(Y)+A_q(empty)`。

所以增加任一批被收缩坐标的封顶量只减少剩余秩；将其他坐标的封顶先固定，正好给上述从 `b(A union B)` 到 `2b(A union B)`、同时保留 `2bZ_2'` 的混合容量比较。这也说明这里没有把普通 contraction 与 capped contraction 混用。

因此 combined rank 证书在所有失败路径归纳成立，保留原 `3e` 的 failure 合同。

## 固定内部参数下的递归节点多项式界

此处仅调用 Lemma 32 的已证结构结论：若一次递归返回而父过程未立即终止，阻塞集从 `B` 变为其子集 `B'`，且 `|B'|<=(1-e^2)|B|`。在真正递归前又有 `|B|>=e|B_0|`。下述计数独立于冻结末页的 log 下标与过紧的分桶尺度。

对一个父节点写 `s=|B_0|`、`d=|B|`，每个孩子的输入阻塞底集大小是 `s+d`。同父下一孩子的 `d'` 满足 `d'<=(1-e^2)d`，所以

`(s+d')/(s+d) <= 1-e^3/(1+e) = 1/gamma`,

其中 `gamma=1/(1-e^3/(1+e))>1`。此外每个孩子的大小至少 `(1+e)s>=gamma s`（`0<e<=1`）。

按 `floor(log_gamma |B_0|)` 分桶，同父各孩子桶号互异，且严格大于父桶号。若总元素数为 `n`，令 `K=floor(log_gamma n)`，令 `T(k)` 是底集大小至少 `gamma^k` 时的最大递归节点数。则

`T(K)<=1,   T(k)<=1+sum_{j=k+1}^K T(j)`。

归纳给 `T(k)<=2^(K-k)`，故总节点数至多 `n^(log_gamma 2)`；每固定正 `e` 是多项式。每节点的集合构造至多逐元素处理，capped contraction/value-oracle 调用及次模最小化也在原访问合同下为多项式。外层逐个增加覆盖和将失败元素设为 matroid loop 的次数亦由有限地面集大小多项式控制。这里不声称精度参数本身的统一多项式依赖。

## 两值归约对端的比较闭合

Theorem 3 是两个完整算法类之间的双向归约，不是任一算法已经存在的证明；Theorem 4 提供其中 Santa Claus 侧的具体算法。联合使用时，在两值子域取 Santa Claus 比率 `4+eta`，给 job-matroid makespan 比率

`2-1/(4+eta)=7/4+eta/[4(4+eta)]`。

对任意目标 `delta>0`，取 `eta=16delta`，右端恰为 `7/4+delta/(1+4delta)<7/4+delta`。这就是源文 Corollary 5 的方向；没有把 `4+eta` 错译为其倒数，也没有把一般值 `8+eta` 送进仅两值的桥。当前任务没有承载该 job 算法数值结论的独立端点，因此记录这一准确比较，不将它冒写成对整条 Theorem 3 的蕴含，也不造自环。

## 有限复核的用途和限制

用精确有理 Python 算术另核：三元素、秩值不超二的全部 37 个规范化单调整数次模函数的补基集合恒等式；625 组含零、整数和非整数尾段的有序槽行的减最大值不等式；999 个小秩/不交集合组合的 capped contraction 合成及混合容量单调性；冻结原图反例的 floor/ceil 容量；上述 `alpha`、`q`、`c`、两值比率、combined rank 余量以及递归分桶不等式的边界。有限枚举只排查算术与小边界，普遍结论由本文与现有严格证据的符号证明承担。
