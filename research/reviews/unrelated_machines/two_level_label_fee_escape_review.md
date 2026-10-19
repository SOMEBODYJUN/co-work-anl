# 两层标签收费的独立最优值重构与全任务审查

2026-10-19；实际内部数学审查，外审与全球新颖性均未认证。下列记录按真实顺序完整保留。记录中的 scratch 绝对路径是当时的读取路由，不是现行依赖；数学内容和反驳已一并收在本文，不声称那些临时路径会永久可读。正文、审计代码和冻结结果以仓库登记路径为准。

---

原记录 `two_layer_activation_independent_exact_first.md`；SHA256 `bd1fa284269b549b2259f458884616cd25c53b3f56cb478ac78079047ccd90cc`。

# 两层标签激活矩阵：陈述先行的独立重构与边界攻击

2026-10-19. Independent reviewer: source_gap_bridge. Internal scratch only; no shared ledger, git, or external communication.

Input read before deriving: only the pure Exact file
`/workspace/scratch/6bd6916818c5/hardness_decoder_new_notes/two_layer_label_activation_universal_exact.md`, SHA256 `b5e5034dc5ebd2fb4afffcfc7493f48cecb70b15704bb1588833d979fe346e1d`, and root's subsequent message stating the strict decoder and cyclic-shift family. No author proof or author code has been read at this freeze.

## The generic upper bound independently reconstructs

Write W=U union V for the full source vertex set, to distinguish a generic vertex from the named right side V. Let q0=floor(D/2). Given the stipulated edge choices a_e, define the endpoint label on each edge to be a_e on its left endpoint and pi_e(a_e) on its right endpoint. For b in Sigma_v let t_vb count the incidences of v carrying endpoint label b. Then

    sum_b t_vb=deg(v)<=D.

Put s_e at its prescribed R_(e,a_e), send the two selected query jobs to their actual H ends, and leave every unselected pair of queries at its own R. Selected R machines have load 1 and unselected R machines have load 1/2+1/2=1, including when several right queries share one H because pi_e is noninjective.

For every selected endpoint label on incidence (e,v), send that unique guard z_(e,v,b) to A_(v,b); leave every other guard at its H end. Each H therefore has either its one selected unit query or its guard of size 3/4. An H indexed by multiple preimages still receives at most one query, because only one original state of edge e is selected and all other queries stay at their own R.

At a vertex v there is at most one label b with t_vb>q0: two such labels would give sum t>=2(q0+1)>D, both for even and odd D. For every label with t_vb<=q0, put w at A, and leave all D f jobs at B. Their loads are 1+t_vb/D<=1+q0/D at A and 1 at B. If the unique exceptional label exists, put its w at B and export its first D-q0 f jobs to their same-index C_(v,r), leaving q0 at B. The exceptional A load is t_vb/D<=1 and its B load is 1+q0/D. Each C_(v,r) gets at most one unit f, because at most one exceptional label exports anything. No f is reindexed and no C belonging to another vertex is used.

This assigns every original job exactly once and gives the claimed 1+floor(D/2)/D<=3/2. The procedure uses no source assignment search and works for the exact fixed local pool eligibility.

All computations are explicit counts, source table lookups and assignments of existing jobs. In the actual-matrix input model D copies of f have already been listed. In source-generation mode choosing D=max(2,max deg) makes the expansion polynomial in the explicitly listed source/labels/projection tables. An empty full vertex set is handled separately by its idle dummy.

## A stronger independent exact value identity

For fixed edge choices let t_(2)(v) be the second-largest endpoint-label multiplicity at v, with zero if fewer than two labels have positive count. Let

    L(a)=max_v t_(2)(v),
    L*=min_(all edge choices a) L(a).

The empty max is zero. Always L(a)<=floor(D/2). For a nonempty full vertex set W, the matrix actually has

    OPT=1+L*/D.                                                (I)

This is an identity/interpretation, not a polynomial optimizer for L*.

Upper: at each vertex choose a label of largest t_vb (choose any legal label if all counts are zero), place just that label's w at B, export all its D f jobs to the same-index C pool, and put all other w at A with all other f at B. Its chosen A load is at most 1, chosen B and C loads are 1, and every other A load is at most 1+t_(2)(v)/D. Keep the earlier R/H/guard assignment. This proves the fixed-choice upper 1+L(a)/D, which may improve the requested schedule.

Lower: suppose there were a full actual assignment with C<1+L*/D<=3/2. Nonempty W has a unit w job, so C>=1. Every s_e selects an actual R_(e,a_e). Since C<3/2, neither size-1/2 query of that selected state can stay with s_e; both are at their actual H ends. The corresponding guard must be at A, since 1+3/4>C. Consequently A_(v,b) contains at least t_vb/D from the selected endpoint incidences.

Let m=floor(D(C-1)). Since C<1+L*/D, m<L*. At some vertex v for these actual a_e, at least two labels have t_vb>=m+1. For either label, w cannot be at A: its load would be at least 1+(m+1)/D>C. Thus both w jobs are at their B machines. Such a B can retain at most m of its D size-1/D f jobs, so each label exports at least D-m jobs. But m<L*<=floor(D/2), hence 2(D-m)>D. All those unit exports must enter the same D local C machines, and C<3/2<2 permits at most one per C. Contradiction. Extra unselected queries/guards can only add nonnegative load and do not remove the selected-incidence lower bound.

If L*=0, the lower OPT>=1 is provided by any w. This completes (I), including noninjective projections and isolated vertices.

## Strict and absolute decoder

For any actual assignment with

    C<1+1/D,

one has C<=(but in fact strictly below when D=2) 3/2. Therefore each selected root's two half-size queries are forced to H, and each corresponding guard is forced to A. If a label is activated by even one selected incidence, w at that label cannot be at A, since 1+1/D>C. Thus its w is at B. No f can remain beside that w, since again 1+1/D>C. All D same-index f jobs of that activated label must occupy all D C machines of its source vertex.

Two activated labels at the same vertex would put two unit jobs on each C_(v,r), contradicting C<2. Every nonisolated vertex therefore has one common endpoint label on all its selected incidences. Use that label; choose arbitrary legal labels at isolated vertices. The left/right selected endpoint relation was pi_e(a_e) by construction, so the resulting singleton assignment satisfies every original edge. The decoder scans actual job placements and source tables in polynomial time.

The same argument covers C<=1, because 1<1+1/D. Conversely any satisfying singleton source assignment gives the earlier fixed-choice schedule with L(a)=0 and peak<=1. For a nonempty full source vertex set, w forces OPT>=1; thus the source YES case has OPT=1. The stronger decoder is correctly strict at 1+1/D: the shift family below attains equality while its source is unsatisfiable.

D=2 has threshold 3/2, and the proof uses C<3/2 to force both queries off a selected root. At equality a root can contain s_e and one half-size query. There is no claim of decoding at that equality. The universal schedule at 3/2 is valid.

## Empty graph boundary: a notation issue to correct

The completely empty full vertex set W=U union V gives no original jobs and the optional idle dummy has OPT=0. If E is empty but W is nonempty, there are still w_(v,b) and f_(v,b,r) jobs, and OPT=1. In particular the statement "V=E=empty implies only dummy/no jobs and OPT=0" is false if V means the right bipartition side and U contains an isolated vertex. A concrete counterexample is U={u}, V=E=empty, Sigma_u={0}, D=2: w_(u,0) has processing time 1 on either A or B, hence OPT>=1, and the all-w-at-A/all-f-at-B assignment attains 1.

If the symbol V in that sentence was intended to mean the entire generic vertex set, this is merely a notation clarification; the upper/decoder conclusions themselves are unaffected. The final statement should use U union V=empty for the zero case.

## Cyclic shifts: exact actual OPT and genuine cheap-list NO

Take any odd integer q>=3 (primality is unnecessary), U={u}, V={v}, both alphabets Z_q, q parallel edge types t, pi_t(a)=a+t mod q, and D=q.

The source cannot have a satisfying singleton assignment: edges t=0 and t=1 would require simultaneously b=a and b=a+1 mod q. Hence the absolute decoder gives OPT>=1+1/q.

Choose the actual edge states a_t=0 for all t. At u only label 0 is activated, with multiplicity q; at v the q activated labels are all distinct and each has multiplicity one. Thus L(a)=1. The exact-value upper gives OPT<=1+1/q. More directly, activate u's label 0 with w at B and all its f in C; at v put every w at A and all f at B. Each v-side active A has load 1+1/q, u's active A has q*(1/q)=1, and every other original machine is at most 1. All unselected states' queries and every unselected guard are still scheduled. Therefore

    OPT=1+1/q.

For arbitrary two source lists A,B with |A|+|B|<=2g, the set of covered parallel edge types is B-A in Z_q. Every pair (a,b) certifies only the unique shift t=b-a; hence

    covered <= |A||B| <= ((|A|+|B|)/2)^2 <= g^2.

Thus covered/q<=g^2/q<rho whenever q>g^2/rho. This is an actual all-list partial-MinRep NO promise, despite actual UM OPT tending to 1. Empty lists and collisions of differences only decrease coverage. This is a finite explicit counterexample family, not a hard-source reduction or a proof of global near-two hardness.

The family even works for q=2 at OPT=3/2; the supplied odd-q domain is valid and avoids that upper-bound equality. No strengthening to strict singleton decoding at C=1+1/q is possible.

## Freeze status

Core universal upper, strict iff/absolute decoder, and cyclic-shift exact OPT reconstruct without a standing mathematical objection. The only identified issue is the empty-case notation if V denotes only the right source side. The stronger identity (I) is an independent deduction, unreviewed at this freeze. No author proof or author code has yet been read; finite tests, if subsequently run, are separate evidence.

---

原记录 `two_layer_activation_author_read_after.md`；SHA256 `3020363b58881a093892504f29b736862a29618a578011def0b1feb57a5b6680`。

# 两层标签激活：作者冻结稿及代码的实际读后记录

2026-10-19，source_gap_bridge；内部 scratch。此记录在独立 Exact-first 推导冻结和向 root 报告之后建立；不改原独立稿。

## 顺序与实际读取字节

1. 先只读纯 Exact `two_layer_label_activation_universal_exact.md`，SHA256 `b5e5034dc5ebd2fb4afffcfc7493f48cecb70b15704bb1588833d979fe346e1d`，并读 root 随后给的 strict/shift 补充陈述。
2. 冻结独立推导 `two_layer_activation_independent_exact_first.md`，SHA256 `bd1fa284269b549b2259f458884616cd25c53b3f56cb478ac78079047ccd90cc`，报告了上界、任意低调度 decoder、shift actual OPT、空图边界和独立第二次数恒等式。
3. 得到 root 明确准许后，实际全文读作者 `two_layer_label_activation_shift_counterexample.md`，SHA256 `6d573c0ab727d2aadbedd6d9bc5e723ced7eb734feb58891024b7b88f53257f7`；实际全文读作者 `two_layer_label_activation_audit.py`，SHA256 `89120e3a2070db70be51addb7b744d1e3b3e2375856642ef1891d7804e428936`。

## 数学读后

作者 §1–4、§6 的全部任务、端口共享、同编号 pool 及负载与独立重构一致。非单射右投影使多个未选 query 共享 H 资格，但完整上界把它们全留各自 R；任意低调度下界只使用真实选中 query 带来的非负负载下限，不需假定其他 query 规范化。

作者 shift 证书选择 a_t=t、右标签 2t。奇数 q 正好保证二倍映射可逆，因而所有 w 留 A、所有 f 留 B，每 A 恰负载 1+1/q。我的独立重构用 a_t=0 并在左端打开一个标签，同样合法；两份证书不同但实际值一致。

旧作者稿有两处边界文字，需与现行 canonical 区分：

- §2 的无条件“OPT=1 iff 源满足”漏完全空顶点图。完全空图的源满足而 OPT=0。应改成 OPT<=1 iff 源满足，非空全顶点集时 YES OPT=1。这已在最终 canonical 正文中修复。
- §5 的“在 C<2-epsilon 下，只有 k>(1-epsilon)D 才被迫激活”在整数等号处不准确。若 k=(1-epsilon)D 恰为整数，w 留 A 的负载等于 2-epsilon，也已大于实际 C，仍被迫激活。精确条件为 1+k/D>C；仅从 C<2-epsilon 得到的充分条件包含 k>=(1-epsilon)D。此处不影响 shift 反例或核心上界/decoder，最终 canonical 已不使用该不准确阈值句。

§7 的置换大字母表贪心也有效：处理一条边时，已用的左端标签和右端标签的逆像各至多 D-1，q>=2D-1 给未禁用的左标签。这是本 compiler 的额外易逃逸范围，不是一般源困难性。

## 代码读后和实际运行

作者代码逐项生成全部原 jobs；f 的外端恰是 C_(v,r)，无跨顶点共享、无重编号。构造与核验没有删未选 states。主程序只实现奇 q 的两顶点 shift/identity 源及特定 edge choices；它不测试一般非单射、孤立点或 D=2，也不枚举全部 actual schedules。这个有限范围与其 docstring 相符。

已经实际运行作者代码主程序一次，stdout 保存为本目录 `two_layer_author_code_replay.json`，SHA256 `a7e77ce8c6855a8d2d6859823ff089b2b76d938aad59fa403c258c651ede0812`。没有改作者代码或覆盖作者输出。

另外自写 generic builder 与真正 actual-option DFS（不导入作者程序）在 `two_layer_activation_independent_audit.py`，SHA256 `ccc22e938040d7883663be17bd9622c609202a7bdc4e517f6fbeb58877e98054`。已经运行；输出 `two_layer_activation_independent_audit.json` SHA256 `c649c1098e9c677279812c33f5c601a0ccad4377c7579c2fdeda88b3ca22e0a5`。该独立有限审计额外覆盖空全顶点集、只含左孤点、双孤点、非单射单边、D2 不满足的两平行边及 D3 同源。前六个小矩阵搜索全部可能改善当前明确上界的真实原 job 分配，使用非负负载作安全剪枝；分别核得 OPT 0,1,1,1,3/2,4/3。第七个非单射三平行边例只核8个 edge-state choices 的全部原 job 构造，不枚举所有 actual schedules。

结论：旧作者稿核心对象/证明无 standing fatal；上述两处边界用语不能按旧字节称“全域已准确”，应由现行修复稿承接。代码只给它实际运行的有限证据，不代一般定理、全原输入识别或未知最优值求解。

---

原记录 `two_layer_second_multiplicity_optimum_independent.md`；SHA256 `dd2c53d2118c73e3e502e9c2d53f27ad66ad41a941478a5d2b0d3d593c560e3c`。

# 两层标签激活编译器的第二大重数最优值：陈述先行独立攻击

内部冻结稿，2026-10-19。来源：root 只给出了待核 Exact；本文未读取 `source_gap_bridge` 的独立证明或记录。下述是本子研究者从该 Exact 自行重构的上下界与端点攻击。它不修改先前冻结稿或 evidence。

## 1. 完整对象与待核陈述

源为显式二部投影约束多重图 \(G=(U,V,E)\)，每顶点 \(v\) 的标签集 \(\Sigma_v\) 非空有限，每 \(e=(u,v)\) 有全定义投影 \(\pi_e:\Sigma_u\to\Sigma_v\)。允许非单射投影、平行边、孤立点及不同 alphabet。给 \(D\ge2\)，每顶点 \(\deg(v)\le D\)，取 \(\delta=1/D\)、\(\beta=3/4\)。下列机器的名称除明确共享者外互异；未列边不可用，全部原 jobs 都执行。

| 原 job | 全部有限端与处理时间 |
| --- | --- |
| \(s_e\) | \(R_{e,a}:1\)，对所有 \(a\in\Sigma_u\) |
| \(x^u_{e,a}\) | \(R_{e,a}:1/2\)，\(H_{e,u,a}:1\) |
| \(x^v_{e,a}\) | \(R_{e,a}:1/2\)，\(H_{e,v,\pi_e(a)}:1\) |
| \(z_{e,v,b}\)，每 incidence 与标签一件 | \(H_{e,v,b}:\beta\)，\(A_{v,b}:\delta\) |
| \(w_{v,b}\) | \(A_{v,b}:1\)，\(B_{v,b}:1\) |
| \(f_{v,b,r}\)，\(r\in[D]\) | \(B_{v,b}:\delta\)，\(C_{v,r}:1\) |

特别，\(C_{v,r}\) 的资格按顶点分隔、按 \(r\) 固定，不能跨顶点或重编号。若完全没有顶点，则没有原 jobs，加一个无任务 dummy 使普通 UM 的机器集非空。

给每边任意 state \(a_e\in\Sigma_u\)，将该边左、右标签分别记为 \(a_e,\pi_e(a_e)\)。令

\[
c_{v,b}=\#\{e\ni v:\text{该边在 }v\text{ 选择标签 }b\}.
\]

定义 \(s_2(v)\) 为有限多重集 \(\{c_{v,b}:b\in\Sigma_v\}\) 的第二大值；不足两项补零。顶点集非空时令

\[
\mu=\min_{(a_e)_{e\in E}}\max_{v\in U\cup V}s_2(v).
\]

空边集的 state 选择恰一个空选择，故非空顶点集、空边集时 \(\mu=0\)。完全空顶点集不对空 max 强行定义 \(\mu\)，另列结论。

**独立核验结论：** 顶点集非空时，真实全部原 jobs 的

\[
\boxed{\operatorname{OPT}=1+\mu/D,\qquad 0\le\mu\le\lfloor D/2\rfloor.}
\]

完全空顶点图的 \(\operatorname{OPT}=0\)。

## 2. 第二大重数的范围

对任意 state 选择和任意顶点，

\[
\sum_{b\in\Sigma_v}c_{v,b}=\deg(v)\le D.
\]

若至少两个正重数，则前两大之和至少 \(2s_2(v)\)，故 \(s_2(v)\le\lfloor D/2\rfloor\)。零、一标签时同样成立。因此其所有 state 选择的 max 与 min 都有该范围；\(\mu\) 为有限集合中的非负整数。

## 3. 上界：给任意 states 的完整实际构造

固定任意 state 选择，写 \(r=\max_v s_2(v)\)。每顶点选一枚达到最大 \(c_{v,b}\) 的标签 \(b_v\)；即使全为零也可选，因为标签集非空。

实际安排如下：

1. \(s_e\to R_{e,a_e}\)。选中 state 的两个 \(x\) 均去其 \(H\) 端；所有未选 state 的两个 \(x\) 均留各自 root。
2. 收到 \(x\) 的端口，其 \(z\) 去 \(A\)；所有其他 \(z\) 留 \(H\)。每端口按 incidence \(e,v\) 索引，因此即使投影非单射，每条边选一个 state 后也只向相应端口送一件 \(x\)。
3. 每个 \(w_{v,b_v}\to B_{v,b_v}\)，该标签全部 \(D\) 件 \(f\) 分别去其原资格 \(C_{v,r}\)。所有 \(b\ne b_v\) 的 \(w\) 留 \(A\)，其全部 \(f\) 留各自 \(B\)。

所有 selected roots、unselected roots 的负载均恰 1。每个被 query 占据的 \(H\) 负载 1，其余 \(H\) 负载 \(3/4\)。被打开的最大重数标签 \(A_{v,b_v}\) 负载 \(c_{v,b_v}/D\le1\)，对应 \(B\) 只有一件 \(w\)，负载 1。其他标签的 \(A\) 负载

\[
1+c_{v,b}/D\le1+s_2(v)/D\le1+r/D,
\]

相应 \(B\) 的 \(D\) 件 \(f\) 总量恰 1。每顶点只打开一个标签，因此每台固定编号 \(C_{v,r}\) 恰一件 unit，负载 1。全部原 jobs，包括未选 states、未选 ports 与孤立点的 jobs 都已明确安排。

得到 \(C_{\max}\le1+r/D\)。取达到 \(\mu\) 的 state 选择，给 \(\operatorname{OPT}\le1+\mu/D\)。此为存在式上界；若要构造，给定 states 后的恢复为位多项式。没有声称可多项式找到达到 \(\mu\) 的 states。

## 4. 下界：任意非规范完整实际调度

顶点集非空时至少一枚 \(w\) 必须实际在一个 unit 端执行，所以 \(\operatorname{OPT}\ge1\)。因此 \(\mu=0\) 的下界已经完成。

以下令 \(\mu>0\)，反设存在任意完整实际调度 \(\sigma\) 满足

\[
C:=C_{\max}(\sigma)<1+\mu/D\le3/2.
\tag{1}
\]

不移动或规范化 \(\sigma\) 的任何 job。对每边，直接读其 \(s_e\) 实际所在的 \(R_{e,a_e}\)，从而得到一组真实 edge states 与计数 \(c_{v,b}\)。

### 4.1 选中 queries 与 port guards 都被绝对阈值强制

选中 root 已有 unit \(s_e\)。若其中任何一件 \(x\) 留 root，负载至少 \(3/2>C\)，与 (1) 矛盾。因此选中 state 的两个原 \(x\) 都实际去各自 \(H\)。该端口已有 unit \(x\)，若其 \(z\) 仍留 \(H\)，负载至少 \(1+\beta=7/4>C\)，也矛盾。所以这两件对应 \(z\) 都实际到其 \(A\)。

故对所有 \((v,b)\)，无论额外未选 state jobs 如何调度，都有真实下界

\[
L_{A_{v,b}}(\sigma)\ge c_{v,b}/D
 +\boldsymbol 1[w_{v,b}\text{ 实际在 }A_{v,b}].
\tag{2}
\]

额外外送的 \(z\) 只增加负载，不会破坏下界；这里没有假设它们留 \(H\)。

### 4.2 严格低于三半时，同顶点至多一个打开标签

称 \(w_{v,b}\) 实际在 \(B_{v,b}\) 的标签为打开。设

\[
t=D(C-1)<\mu\le D/2.
\tag{3}
\]

因为 \(C\ge1\)，有 \(t\ge0\)。对一个打开标签，\(B\) 已有 unit \(w\)，所以留在此 \(B\) 的 \(f\) 件数最多为 \(\lfloor t\rfloor\)。至少

\[
D-\lfloor t\rfloor>D/2
\tag{4}
\]

件 \(f\) 必须实际在其 \(C_{v,r}\) unit 端执行。

如果同顶点有两个打开标签，则由 (4) 它们共向该顶点的 \(D\) 台 \(C\) 送出超过 \(D\) 件 unit jobs。由于 \(C<3/2<2\)，任意一台 \(C\) 至多接一件 unit，矛盾。固定编号资格甚至更强；本计数不要求它们可任意改投 pool。

因此每顶点至多一个打开标签。证明没有禁止某打开标签在 \(B\) 留下部分 \(f\)；恰恰是按其允许留下的 \(\lfloor t\rfloor\) 件做了全额扣除。

### 4.3 第二大重数必留下一个未打开高重数标签

由 \(\mu\) 的定义，当前从任意 \(\sigma\) 读出的 state 选择必有一个顶点 \(v\) 满足 \(s_2(v)\ge\mu\)。因为 \(\mu>0\)，该顶点存在两个不同标签 \(b_1,b_2\)，其 \(c\) 均至少 \(\mu\)。至多一个打开，故至少一个 \(w\) 仍实际在 \(A\)。由 (2)，该机负载至少

\[
1+\mu/D>C,
\]

矛盾。得到 \(\operatorname{OPT}\ge1+\mu/D\)。结合上界完成精确公式。\(\square\)

## 5. 端点与最小攻击

* **偶数 \(D\)、\(\mu=D/2\)：** 上下界给恰 \(3/2\)。下界只反设 \(C<3/2\)，从未声称 \(C=3/2\) 时每顶点至多一个打开标签。
* **恰 \(C=3/2\) 的双打开反例：** 一个孤立顶点、两个标签、偶数 \(D\)。将两枚 \(w\) 都放各自 \(B\)；第一个标签外送前 \(D/2\) 件 \(f\)，第二个外送后 \(D/2\) 件，其他 \(f\) 留各自 \(B\)。每台 \(B\) 负载 \(1+D/(2D)=3/2\)，每台固定编号 \(C\) 恰一件 unit。这是完整原 job 调度，说明不能把严格唯一性引理闭成非严格端点。该实例 \(\mu=0\)、真实 OPT 仍为 1，与精确公式不矛盾。
* **\(D=2\)：** \(\beta=3/4\ge\delta=1/2\)，根 \(3/2\) 阈值严格排除留 query，全部下界有效；可能的 \(\mu\) 仅 0 或 1。
* **奇数 \(D\)：** 最高值 \(1+\lfloor D/2\rfloor/D<3/2\)，故即使在最高实际最优阈值，同顶点仍至多一个打开标签。
* **\(\mu=0\)：** 上界给 1；非空顶点至少一枚 unit \(w\) 给下界 1。没有用不存在的 top-two 正标签。
* **非空孤立顶点集、\(E=\varnothing\)：** 唯一空 states 选择使 \(\mu=0\)，w/f 自身仍使 OPT 为 1。
* **完全空顶点集：** 没有所有类型的 jobs，dummy 机器负载 0，所以 OPT 为 0。

## 6. 限定身份与独立状态

这是该显式构造呈现的实际最优值恒等式；它不自动给求 \(\mu\) 的多项式程序，不给 raw UM 模板识别程序，不是一般调度三半算法或 near-two 困难性。现阶段这份 statement-first 独立推导无尚成立的反例；未读另一作者 proof，未调用外部源定理，也未用有限运行替代一般证明。原目标及其一般反面均保持 OPEN。

---

原记录 `two_level_label_fee_escape_canonical_read_after.md`；SHA256 `45b4218c474f29a8ae3ce728e034d80247feeb2826e6bb6c5966be7e64208414`。

# 两层标签收费终稿的实际全文读后审查

2026-10-19，内部 scratch。未修改 canonical、metadata、git 或先前冻结证据。

## 已实际阅读的版本

* canonical 全文：`/workspace/scratch/6bd6916818c5/co-work-anl-boss4/research/current/unrelated_machines/two_level_label_fee_escape.md`
* 本次全文读取 SHA-256：`27bf8a1e9a7e564d58f586e70fa409e8dc1f1766481c0ba36cfa6efe4d738164`
* 先行独立陈述重构：`two_layer_second_multiplicity_optimum_independent.md`，SHA-256 `dd2c53d2118c73e3e502e9c2d53f27ad66ad41a941478a5d2b0d3d593c560e3c`。
* 此前没有阅读 `source_gap_bridge` 的证明记录。本次在独立冻稿之后，按 root 指示实际通读上述 canonical §1–6。

## 数学审查结论

本文的对象、全源完整调度、第二大标签次数的精确最优值、strict decoder 与显式 shift 反例均通过本次实际读后攻击；没有尚成立的 fatal objection。

1. **全部原 jobs 与真实 pool：** 所有未选 state queries 留 root，未用 port guards 留 \(H\)，全标签 \(w,f\) 逐项支付。pool 严格按顶点分隔且 \(r\) 资格固定；每顶点唯一 heavy 或唯一最大 label 全部 \(D\) 件 \(f\) 去原 \(C_{v,r}\) 足够，无须全局 pool 或重编号。
2. **非单射投影：** 多个未选 states 可共享同一个 \(H\) 资格，但构造每边只选一个 state，且 \(H\) 按 edge incidence 索引，故一次构造不会因非单射而让两个 selected queries 占同一 \(H\)。
3. **精确公式的上界：** 每顶点仅打开最大重数标签，其他 labels 的实际 \(A\) 负载受第二大重数控制。只证明给 states 的恢复和最优值恒等式，未偷用 \(\mu\) 的优化 oracle。
4. **任意非规范下界：** 反设 \(C<1+\mu/D\le3/2\)，根上的 unit 排除任何半长 query 留家；端口 unit 加 \(3/4\) 排除 guard 留端口。于是所读 states 的全部计数都对应已实际到 \(A\) 的 guards。任意其他 jobs 的非规范外送只增加下界。
5. **允许 \(B\) 留部分 \(f\)：** \(k=\lfloor D(C-1)\rfloor<\mu\le\lfloor D/2\rfloor\) 已真实扣除可留的 \(k\) 件，每个被迫打开标签仍至少送 \(D-k\) 件 unit。两标签总数 \(2(D-k)>D\) 与原 pool 容量矛盾；没有错误要求打开就全送。
6. **偶数 \(D\) 的三半端点：** 唯一性只用于严格 \(C<3/2\)。恰 \(C=3/2\) 可让两个标签各留 \(D/2\) 件 \(f\)、外送互补编号；不影响严格反设下界。因此 canonical 没有错误闭合该端点。
7. **\(D=2\)：** \(\delta=1/2\)，根留 query 的负载恰 \(3/2\)，严格反设足以排除；\(\beta=3/4>\delta\)。未发生 \(D\ge3\) 才成立的隐含假设。
8. **\(\mu=0\) 与空图：** 非空顶点有至少一件 unit \(w\)，故最优至少 1；上界给 1。孤立点与空边集亦成立。完全空顶点集单列没有任何 jobs、OPT0，避免空 max 与错误只检测右侧为空。
9. **shift 源与外部条件：** 列表 NO 只由差集计数推出，没有把这个两顶点显式族声称为 NP-hard、指定 PCP hard image 或任何随机种子归约。\(q\) 奇数使 \(t\mapsto2t\) 可逆不需要 \(q\) 为素数；所有 \(A\) 恰一 query，实际 OPT \(1+1/q\) 的下界来自严格 decoder。
10. **构造复杂度：** 原 source 到展开矩阵用最大度多项式；另给巨大二进制 \(D\) 时，声明仅按已经显式展开矩阵位长计。没有将 \(D\) 次输出当作 \(\operatorname{poly}(\log D)\)。

## 一个非 fatal 表述建议

§6 选 \(D=\max(2,\max_v\deg(v))\) 时，完全空顶点图的内部 max 未定义。可改成

\[
D=\max\bigl(\{2\}\cup\{\deg(v):v\in U\cup V\}\bigr).
\]

这是 source 自动选 \(D\) 的空图写法；不影响已给定 \(D\ge2\) 的精确对象或任何数学结论。已原文报告 root，审查者没有修改正文。

## 核验边界

root 的 general audit 文件本次只核取路径与 hash，未执行；其读取时 hash 为 `1cf691dd2321cd988bf7fefed6fbce232a3c9cce6113571ce779a24af44f1de4`。实际统一运行与最终冻结按 root 的指示由 root 完成；本审查不声称已验证其代码或 evidence。先前子研究者 Fraction 审计仍保持原冻结字节，仅覆盖其明确列出的 shift/identity/预选 states 情形。一般证明由上述解析推导支撑。

---

原记录 `two_level_label_fee_escape_canonical_final_attack.md`；SHA256 `892cd1c01804ac9e6a97ff41a7c829ffc271509331ee0c9632c72df272d034c4`。

# 两层标签收费最终正文与 generic 审计：实际全文后置攻击

2026-10-19，source_gap_bridge；内部 scratch；不改正文、maps、证据冻结件或 git。

## 实际读取范围与 SHA256

本记录建立前已实际全文读取以下两份最终文件，未仅凭文件名或旧作者稿转记：

- `/workspace/scratch/6bd6916818c5/co-work-anl-boss4/research/current/unrelated_machines/two_level_label_fee_escape.md`，SHA256 `27bf8a1e9a7e564d58f586e70fa409e8dc1f1766481c0ba36cfa6efe4d738164`。
- `/workspace/scratch/6bd6916818c5/co-work-anl-boss4/tests/audits/unrelated_machines/two_level_label_fee_escape.py`，SHA256 `1cf691dd2321cd988bf7fefed6fbce232a3c9cce6113571ce779a24af44f1de4`。

独立陈述先行稿 SHA256 `bd1fa284269b549b2259f458884616cd25c53b3f56cb478ac78079047ccd90cc` 保留原字节。旧作者稿实际读后单独记于 `two_layer_activation_author_read_after.md`，不将其 reading scope 混成最终正文。

## 后置数学攻击

**全原任务域。** 表中所有 e,a 的两个 query 原任务均在。对固定边状态，只有该状态两枚 query 外送；其他每个 root 接两件 1/2 query，恰负载1。右投影非单射时多个原 query 虽可去同一 H，所给构造仍至多送其中一枚，因为一边只有一个所选 state。每个 incidence/label 的独立 z 也均有执行位置。

**局部 pool 与 all-f 导出。** §2 的简化将唯一重标签的全部 D 枚 f 外送，而不是只送 D-floor(D/2) 枚；这是合法且更简单的构造。该顶点最多一个重标签，故每个 r 的 C_(v,r) 仍只接这个标签的一枚原 f。没有重编号、任意 pool 资格或跨顶点共享。其 B 变成负载1，不影响其他类上界。§2.1 对任取最大次数标签导出全部 f 同理；即使所有次数为零，也可任取一个真实非空域标签打开，得到合法负载1。

**mu 的任意实际调度下界。** 非空全顶点集中的 unit w 排除 C<1。mu>0 的反设 C<1+mu/D 自动给 C<3/2，因此实际 selector 所在 root 的两件半长 query 都不能留根；C<1+3/4 又迫相关真实 guard 到 A。额外未选 query 或 guard 的移动只加非负负载，所用 c_vb/D 是真实 A 负载的下限，不是假设所有任务已规范化。k=floor(D(C-1)) 满足0<=k<mu<=floor(D/2)，实际状态向量某顶点的第二次数至少 mu，故两标签的 w 均被迫在 B，每个至少导出 D-k 枚原 f。它们受同一个本顶点 D 台 C 的 unit 容量约束，2(D-k)>D 矛盾。此论证不按 query 身份合并、没有遗漏未选状态，也不依赖输入给最优状态。

**strict decoder 与 D=2。** 当前写的是 C<1+1/D，正确。D2 时 C<3/2，正好排除 selected root 的 selector+一枚半长 query；不能把端点改成 <=。H guard 的3/4值更大，后续 w、f 的阈值也都保持严格。C=1+1/D 的 shift/no-source 调度是明确边界，正文没有误排该等号。

**空源。** 当前 top statement 和 §3 均写 OPT<=1 iff 源满足，并明确 U union V 非空时才将 YES 值升级为恰1；完全空顶点图保一个 idle 机、零任务、OPT0。E为空但有任何左或右孤点仍有单位 w，OPT1，当前正文的表和退化说明覆盖。源生成式 max_v deg(v) 在完全空顶点集上应按零理解（等价写 max({2} union {deg(v):v in U union V})）；当前已经单列该空模型，不造成核心对象未定义。

**shift 与 scope。** 奇数 q 下选 a_t=t、右标签2t各遍历一次，所有 w 留 A、所有 f 留 B，全部 pool 闲置，峰1+1/q。任意C<该值由真实 decoder 推出不可能的 singleton 全满足，给真正 actual OPT。列表差集/AM-GM 是对任意两侧列表的覆盖上界，不是只管规范调度。正文明确其非 PCP hard image，而全源三半上界本身不需要该反例来自 hard image。值恒等式未被说成能多项式优化 mu；一般UM、其他共享结构及主目标均保留 OPEN。

在上述准确范围中未发现 standing fatal。无外部 Paper Fact/PCP 前提需要为这份自足证明另作联网背书。

## 实际代码执行和未执行范围

已经逐行读 generic 审计，并实际运行其主程序一次，stdout 另存本目录 `two_level_canonical_code_replay.json`，SHA256 `b090c8c028dd37360f91a2d80ba3f14ba518edd676f924dde17d5f22294f2cc2`。运行报告内的 account/code SHA 恰等于本记录上列实际读取 SHA。

此次实际运行包含：q=3,5,7,11,25 五份完整 shift P（分别63,165,315,759,3825件 jobs）；每份另核三种边状态选择的 half/max 输出；六个明确 tiny source 的18个全部 edge-state choices，含空全顶点图、孤点、非单射投影和D2；q3/5/7共17472份两侧列表。所有程序断言通过。

generic audit 的 build 明确构造全部 z,w,f 和固定 C_(v,r) 资格，验证逐原 job 恰执行一次、合法目的地与所有 pool 行负载。mode=max 用所给状态下的 second count 检验其构造值；tiny_sources 另枚举 source singleton 标签，只用于独立检查 mu0 iff source satisfiable。它没有用 SAT oracle 来构造调度。

没有运行仓库全局 map/catalog 检查、没有重跑别的UM审计、没有枚举一般源或generic程序所列矩阵的全部 actual schedules，没有实现求最优mu的后端。generic代码自己的 unchecked 字段准确保留这个范围。另一个本人独立的 actual-option DFS 有限核验已运行并在作者读后记录列明，不能混作本 generic code 的能力。

本最终审查仅绑定上述两份文件的精确字节；若正文或代码随后改变，新增字节须另读后再登记。

---

原记录 `two_level_label_fee_escape_locked_final_delta_read.md`；SHA256 `5400ccf510dadedcd801f7109c1e1f1d3cd9c538ce5d0357e5d59a91800560ed`。

# 两层标签收费锁定版：最终 delta 全文实读与重跑

2026-10-19，source_gap_bridge；内部 scratch；不覆盖旧独立稿/读后稿/输出，不修改共享正文、maps 或 git。本记录只确认锁定字节与已有数学义务，不追加新 Claim。

## 实际最终读取

已在收到 root 的锁定通知后，再次实际全文读取正文及完整 generic code，实测 SHA256 为：

- 正文 `/workspace/scratch/6bd6916818c5/co-work-anl-boss4/research/current/unrelated_machines/two_level_label_fee_escape.md`：`260bec7f3ca19c3af7f48c7550150796aa9208d477ee97eff9c3568e7a2c4baa`。
- 代码 `/workspace/scratch/6bd6916818c5/co-work-anl-boss4/tests/audits/unrelated_machines/two_level_label_fee_escape.py`：`471ae6ff9bd819db11eae260fda53a1a38d20d77896e7b7f5af8ce0dfc22defb`。

确认正文 §6 已把源生成时的 D 写为 max({2} union {deg(v):v in U union V})，完全空顶点集不再需要未写出的 max-empty 约定。代码 build 新增左右边端集合不交验证；construct 新增 chosen 长度等于 edge 数以及 mode 属于 half/max/none 的验证；tiny_sources 的 str 格式调整等价，不改有理值或范围。

再次通读后，先前对全部原 jobs、非单射 H 资格共享、固定编号本顶点 pool、全部 f 导出简化、D2 严格阈值和 mu 任意实际调度下界的攻击结论保持。当前锁定版在这些准确量词与 Scope 中无 standing fatal。

## 已实际重跑锁定代码

已运行锁定代码主程序一次，stdout 另存：

`/workspace/scratch/6bd6916818c5/source_gap_bridge_notes/two_level_canonical_locked_code_replay.json`。

该新输出记录的 account/code SHA 与上列锁定字节一致；五份 shift、六个 tiny source／18个全部 edge-state choices、17472份列表全部通过。旧 `two_level_canonical_code_replay.json` 和其他冻结输出未覆盖。

未运行 maps/catalog/全仓审计，没有把这些有限输入变成一般源或实际调度的穷举定理。本 generic 程序本来也不枚举其所有 actual assignments；其 unchecked 字段保持准确。

## 可供 root 实读并入库的第二份独立 actual-option 审计

代码原件：

`/workspace/scratch/6bd6916818c5/source_gap_bridge_notes/two_layer_activation_independent_audit.py`

SHA256 `ccc22e938040d7883663be17bd9622c609202a7bdc4e517f6fbeb58877e98054`。

已实际运行的原 JSON：

`/workspace/scratch/6bd6916818c5/source_gap_bridge_notes/two_layer_activation_independent_audit.json`

SHA256 `c649c1098e9c677279812c33f5c601a0ccad4377c7579c2fdeda88b3ca22e0a5`。

此代码不导入作者或 root 的构造器。它独立生成完整实际矩阵、验证显式上界的全部原 job 目的地，再把所有处理时间乘 lcm(4,D) 化成整数，DFS 遍历每枚原 job 的真实有限选项。当前负载若已达到已验证上界或更小的当前 best，则由非负性安全剪枝；不是只搜索规范 query/guard 模式，也不调用 mu 优化或 source 满足性 oracle 来证明下界。初始上界有前面完整 σ 验证支持；发现更小完整实际分配才更新 best。

前六个明确小矩阵的 actual-option 搜索分别给：空全顶点集 OPT0（0 jobs），仅左孤点 OPT1（3 jobs），双孤点 OPT1（8 jobs），非单射单边 YES OPT1（17 jobs），D2 不满足两平行边 OPT3/2（21 jobs），D3 同源 OPT4/3（24 jobs）。搜索访问节点数为1,4,9,59,77,95；这些较小计数来自 unit/半长任务的容量剪枝，不是未生成其他原 jobs。第七个非单射三平行边例（43 jobs）只核8个边状态的完整构造，没有跑 actual-option DFS，JSON明确分开。

主程序默认拒绝覆盖原 JSON；入库时如改 CLI/路径，应保存本原件字节并对规范化程序另记 SHA。此处仅提供已发生的独立代码与运行，不预写 root 已读或已审结论。

---

## boss4 最终独立回算与代码规范化

root 实读全部作者与独立稿并独立证明 μ 恒等式：在 C<3/2 时任一打开标签必须导出严格多于 D/2 枚 f，故同顶点至多一个打开；第二大计数给任意完整调度下界。最终正文以 U∪V 判断零任务分支，显式源生成 D 的空最大值已修正。root 实读独立 DFS 全部源码并保留搜索数学不变，仅去掉向脚本旁固定文件写入的三行，改为 stdout，由统一冻结位置保存。新文件 tests/audits/unrelated_machines/two_level_label_fee_independent_search.py 的代码身份由对应新冻结结果记录；不将旧脚本 hash 冒称为新文件 hash。root 实际运行了构造审计及新路径独立 DFS；DFS 的剪枝只排除当前峰不可能严格改善已验证上界的部分分配，未把有限结果升级为一般证明。

## root 保存核验与结论

本次正文一般性证明与有限核验分层。root 实际重跑相关登记程序，冻结证据含命令、输入约定、代码及正文 hash。现有审查在明确域内没有尚成立的 fatal objection；不表示自动保证真值，更不升级 UM-TARGET-v1 或其反面。
