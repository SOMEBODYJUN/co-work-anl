# 真实单位请求容量核：未升级的自足探索稿

以下逐字保存实际作者稿，SHA256 `7b273faf03a36276ebd9ac22d398a07acac7cdcc72d76e67c067c2439d7907c0`。root 此后已全文读取并回算必要/充分性与显式规模；尚无陈述先行的独立完整攻击，保持 DRAFT，不进入 current 或可靠 Claim。真实 pins 是新增原任务，本文不能据此向原 half-root 模型增加强制义务；近二 actual 值不能替代 NP 源。

---

# 加权真实单位请求的共同闭包：精确容量条件与饱和近二值

内部 scratch 草稿，2026-10-19。不分配新的 canonical Claim 群，不修改已保存资产、metadata、frozen evidence 或 git。这里的请求由**新增的真实 singleton unit jobs** 表示；这是与原 half-root 模型分开的普通 UM 对象。显式接近二的实例只认证实际值，不是计算困难性，也没有证明任何源能强制这些 pins。

## 1. 完整普通 UM 对象

给有限 fee 顶点集 \(W\)。每 \(v\in W\) 有非空有限标签集 \(\Sigma_v\)，每 \((v,b)\) 有有限端口指标集 \(I_{v,b}\)，允许为空。给整数 \(D\ge2\)、\(\delta=1/D\)，及有理数 \(0<\beta<1\)（可写 \(\beta=1-\eta\)）。

对每端口 \(p=(v,b,i)\)，给正有理数 \(a_p>0\)，满足每 label 的完整预算

\[
\sum_{i\in I_{v,b}}a_{v,b,i}\le1.
\tag{1}
\]

给实际请求集合 \(Q\subseteq\{(v,b,i):i\in I_{v,b}\}\)。每个被请求端口有一件新的真实 pin job，只有该端口机器一个有限端，时间 1。没有外加但未执行的 preload，也没有把这些 pins 默认为原 half-root 已提供。

全部原 jobs、机器及有限时间如下；不同名字互异，未列边不可用：

| 原 job | 全部有限端与真实时间 |
| --- | --- |
| 每端口 guard \(z_{v,b,i}\) | \(H_{v,b,i}:\beta\)，\(A_{v,b}:a_{v,b,i}\) |
| 每 requested \(p=(v,b,i)\in Q\) 的真实 \(p_p\) | 仅 \(H_{v,b,i}:1\) |
| 每标签 \(w_{v,b}\) | \(A_{v,b}:1\)，\(B_{v,b}:1\) |
| 每 \((v,b,r)\)，\(r\in[D]\)，的 \(f_{v,b,r}\) | \(B_{v,b}:1/D\)，\(C_{v,r}:1\) |

pool 严格按 \(v\) 分隔，并保固定原编号 \(r\)：每个 \(f\) 只能用自己的 \(C_{v,r}\)。不同 labels 的同编号 \(f\) 共享该机器，没有重编号或跨顶点资格。未请求 guards、全部 labels 的 \(w\) 和全部 \(D\) 件 \(f\) 始终保留且必须执行。

定义真实请求质量

\[
m_{v,b}(Q)=\sum_{i:(v,b,i)\in Q}a_{v,b,i}.
\tag{2}
\]

由 (1) 有 \(0\le m_{v,b}\le1\)。这个归一化是以下充分性承重条件，不可删除。

如果 \(W=\varnothing\)，则端口与所有 jobs 都为空，补一台 dummy，OPT=0。以下默认 \(W\ne\varnothing\)，故至少有一件 unit \(w\)，任何实际峰值至少 1。

## 2. 全阈值精确可行性条件

对给定非负有理阈值 \(C\)：

* \(C<1\)：不存在完整可行调度，因为 unit \(w\) 无法执行。这里**不**把负数 \(\lfloor D(C-1)\rfloor\) 代入后续公式。
* \(C\ge1+\beta\)：总有完整实际调度。所有 \(z\) 留 \(H\)、所有 \(w\) 留 \(A\)、所有 \(f\) 留 \(B\)，pins 执行其唯一端；requested \(H\) 负载 \(1+\beta\)，其他机器至多 1。
* 对

\[
1\le C<1+\beta<2,
\tag{3}
\]

令

\[
k=\lfloor D(C-1)\rfloor,
\quad 0\le k\le D-1,
\quad h(C)=\left\lfloor\frac{D}{D-k}\right\rfloor,
\tag{4}
\]

以及

\[
n_v(C)=\#\{b\in\Sigma_v:m_{v,b}>C-1\}.
\tag{5}
\]

则完整实际可行的充要条件是

\[
\boxed{\forall v\in W,\qquad n_v(C)(D-k)\le D,}
\tag{6}
\]

等价于 \(n_v(C)\le h(C)\)。分母 \(D-k>0\) 来自 \(C<2\)，不是额外未述条件。质量等于 \(C-1\) 的 label 不计入 (5)，因为其 \(w\) 留 \(A\) 可以恰好达到 \(C\)。

## 3. 必要性：任意完整实际调度，允许非规范 jobs

给任意峰值不超过 (3) 的完整调度。

每 requested \(H_p\) 必执行其真实 singleton unit pin。如果该端口的 \(z_p\) 仍在 \(H_p\)，负载就是 \(1+\beta>C\)。因此全部 requested guards 都必须实际到其 \(A_{v,b}\)。未请求 guards 可以任意移动；它们的额外非负质量不削弱以下必要下界。

对一个满足 \(m_{v,b}>C-1\) 的 label，若 \(w_{v,b}\) 留 \(A\)，其负载至少 \(1+m_{v,b}>C\)。所以该 label 的 \(w\) 必须在自己的 \(B\)。

这台 \(B\) 已有 unit \(w\)，最多能留 \(k=\lfloor D(C-1)\rfloor\) 件 \(f\)。该 label 的至少 \(D-k\) 件 \(f\) 必须实际去自己的原 \(C_{v,r}\)。由于 \(C<2\)，每台 \(C\) 至多一件 unit。同一个 \(v\) 的所有这些 labels 合计至少外送 \(n_v(C)(D-k)\) 件 unit，只有 \(D\) 台原 \(C\)，故必须满足 (6)。

没有假设打开 label 后全部 \(f\) 都离开 \(B\)；允许留下的 \(k\) 件已经全额扣除。也没有假设未请求 \(z\) 留端口或未被强制的 \(w\) 留 \(A\)。

## 4. 充分性：一次共同安排所有 requests 与全部原 jobs

假设 (6)。对每 \(v\)，将集合

\[
S_v=\{b:m_{v,b}>C-1\}
\]

中的 labels 排任意固定顺序。在原编号 \([D]\) 内为每 \(b\in S_v\) 选一组大小恰 \(D-k\) 的编号 \(R_{v,b}\)，这些编号组两两不交；(6) 保证能取。只在各自原编号使用资格，未重编号。

实际执行：

1. 全部 pins 放唯一端 \(H\)；requested \(z\) 去对应 \(A\)，所有未请求 \(z\) 留原 \(H\)。
2. 对 \(b\in S_v\)，\(w\to B\)。恰当 \(r\in R_{v,b}\) 时，将原 \(f_{v,b,r}\to C_{v,r}\)；其余恰 \(k\) 件原 \(f\) 留 \(B\)。
3. 对其他 labels，\(w\) 留 \(A\)，全部 \(D\) 件 \(f\) 留 \(B\)。

逐机同时核验：

| 原机器 | 实际负载上界 |
| --- | --- |
| requested \(H\) | 只有真实 pin，1 |
| 未 requested \(H\) | 只有其 \(z\)，\(\beta<1\) |
| \(b\in S_v\) 的 \(A\) | \(m_{v,b}\le1\le C\)，使用完整预算 (1) |
| \(b\notin S_v\) 的 \(A\) | \(1+m_{v,b}\le C\) |
| \(b\in S_v\) 的 \(B\) | \(1+k/D\le C\) |
| \(b\notin S_v\) 的 \(B\) | \(D/D=1\) |
| 每台 \(C_{v,r}\) | 编号集合互不交，至多一个真实 unit \(f\)，负载至多 1 |

所有原 jobs 与新增 pins 恰执行一次，完整峰值不超过 \(C\)。该构造是一个共同选择，未独立叠加单个 label 的局部安排。扫描现有端口、jobs 和原编号便可在显式总位长多项式时间构造；没有把二进制 \(D\) 的展开输出当作 \(\operatorname{poly}(\log D)\)。\(\square\)

## 5. 任意实际低调度可提供的真实 source 质量列表

若本 kernel 来自更大的原 scheduling 实例，并从一份完整实际调度 \(\sigma\) 读出其实际接到 unit 查询的端口集合 \(Q(\sigma)\)，则可删除其他外部 jobs，将每个这些已实际执行的 unit 查询替换为同端口的 singleton pin。只保留原全部 \(z,w,f\) 的原实际位置。

若原 \(C<2\)，同一端口至多一件 unit，故这个 pin 集合合法；替换后各机负载不增加。于是对于 \(1\le C<1+\beta\)，从任意非规范原 \(\sigma\) 都得到真实列表

\[
L_v(\sigma,C)=\{b:m_{v,b}(Q(\sigma))>C-1\},
\]

并有完整的整数界

\[
|L_v|\le\left\lfloor
\frac{D}{D-\lfloor D(C-1)\rfloor}
\right\rfloor.
\tag{7}
\]

特别，若 \(C=2-\varepsilon\)、\(\beta=1-\eta\)、\(0<\eta<\varepsilon<1\)，那么

\[
L_v=\{b:m_{v,b}>1-\varepsilon\},\qquad
|L_v|\le\left\lfloor\frac{D}{\lceil D\varepsilon\rceil}\right\rfloor
\le 1/\varepsilon.
\tag{8}
\]

这界中 \(D\) 是实际展开的 pool/degree 参数，\(\varepsilon\) 是待考察负载余量，二者没有混作同一源参数。

(7)–(8) 只认证**近饱和质量 labels** 的 cost；没有认证全部被使用 labels 都在这些列表，也没有认证这些列表覆盖任何正比例源边。尤其原 half-root 可统一只外送左查询，真实请求列表在右侧为空，故本段并未补上 source 强制双端请求或覆盖比例的缺口。

## 6. 饱和请求的显式 actual 近二值

取任意整数 \(q\ge2\)，一个 fee 顶点，标签集 \([q]\)，令 \(D=q\)。每个 label 有 \(q\) 个端口，全部 guard 的 \(A\) 时间为 \(1/q\)，完整 label 质量正好 1。**所有** \(q^2\) 个端口都加入真实 singleton unit pin，所以每个 label 的请求质量 \(m_b=1\)。取

\[
1-1/q<\beta<1
\quad\text{（例如 }\beta=1-1/(2q)\text{）。}
\]

则这个完整普通 UM 实例满足

\[
\boxed{\operatorname{OPT}=2-1/q.}
\]

**达到。** 所有 requested guards 去各自 \(A\)，每个 \(A\) 负载 1；所有 \(w\) 去各自 \(B\)。label \(b\) 只把原 \(f_{b,b}\) 外送原 \(C_b\)，其余 \(q-1\) 件留 \(B_b\)。每 \(B_b\) 负载 \(1+(q-1)/q=2-1/q\)；每台 \(C_b\) 恰一件 unit，每个 \(H\) 只有其 unit pin，全部原 jobs 都已付清。

**任意低调度下界。** 若 \(C<2-1/q\)，unit \(w\) 先排除 \(C<1\)。剩余情形有 \(1\le C<2-1/q<1+\beta\)，全部 requested guards 被强制到 \(A\)。所有 \(m_b=1>C-1\)，故全部 \(q\) labels 的 \(w\) 都必须到 \(B\)。此时

\[
k=\lfloor q(C-1)\rfloor\le q-2,
\]

所以每 label 至少外送两件 unit \(f\)，至少 \(2q\) 件要进入仅有的 \(q\) 台 unit-capacity \(C\)，矛盾。这个下界适用于任意非规范完整实际调度。

全部显式规模为

\[
m=q^2+3q,\qquad n=3q^2+q,\qquad
\#\text{finite incidences}=5q^2+2q.
\]

如果同一个 internal kernel 只为一个 label 的全部 \(q\) 个端口加入 pins，其他 labels 不加 pins，则有完整 OPT=1：只打开该 label、其全部 \(f\) 到 pool，其他 labels 按未请求模式执行。两个输入的 internal jobs 相同，而 pins 的数量与集合不同。

此显式差异是请求模式造成的 actual 值，不是某个 NP 源的 YES/NO 归约；kernel 本身还有第2节的可判定条件。真正困难的 source 桥仍须强制 NO 生成多 label 的近饱和真实请求，同时在 YES 中以兼容方式请求少数 labels。本文未提供该桥。

## 7. 状态

完整对象、全阈值 iff、一次性所有 jobs 恢复、任意原实际请求的必要列表界与显式饱和值均有自足推导。root 已看过 iff 的口头陈述，本文件尚未接受 independent full-proof attack；无外审或全球新颖性声明。不将它升级为一般 hardness、原 half-root 的新义务或任何 source 强制性结论。
