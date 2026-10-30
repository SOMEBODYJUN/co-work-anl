---
id: unrelated-machines/three-dimensional-and-high-dimensional-quota-obstruction-review
kind: review
type_tag: 审查
title: 三维匹配与高维配额部分障碍双源审查
status: complete-source-read-integrated
truth_status: exact partial-quota identities and conditional robust-bundle contract; no general UM hardness
review_level: full-source-read-proof-comparison-boundary-audit
scope: "three-dimensional matching demand floors, high-dimensional matching quota layers, low-quota label escape, robust bundle promise, and the remaining decoder obligation"
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/three_dimensional_matching_demand_floor_obstruction.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/three_dimensional_matching_demand_floor_obstruction.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/kdm_high_dimensional_quota_obstruction.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/kdm_high_dimensional_quota_obstruction.md
source_ids:
  - df7e9b9a6958e6b6712f
  - 91e3e78a4390c625b4b7
inventory_sha256:
  df7e9b9a6958e6b6712f: 1ab438c16b72d33a3913d88623a835143239c92b392802fc3d73b3a395f128bf
  91e3e78a4390c625b4b7: 78e53254e63022dbd3f8f2a5259176cd4827df28fc43c561e6574d1b320f1243
---

# 阅读范围与对象身份

本批完整读取 `three_dimensional_matching_demand_floor_obstruction.md` 与 `kdm_high_dimensional_quota_obstruction.md` 的冻结正文，并以两个冻结来源版本（`legacy-cleanup` 提交 `68fad804ec5946cb296f77dc5b336308a66abf12` 与 `main` 提交 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`）的相同路径为来源锚点。第一源的稳定源 ID 为 `df7e9b9a6958e6b6712f`，SHA-256 为 `1ab438c16b72d33a3913d88623a835143239c92b392802fc3d73b3a395f128bf`；第二源的稳定源 ID 为 `91e3e78a4390c625b4b7`，SHA-256 为 `78e53254e63022dbd3f8f2a5259176cd4827df28fc43c561e6574d1b320f1243`。

两源属于同一条反面归约线，但数学对象不同。三维匹配源给出一个带三元组点需求的精确闭式，说明把三维匹配直接编译成需求树时，二分投影层会遮蔽完整三维匹配层。高维匹配源先核对 Lee--Svensson--Thiery 高维匹配事实，再把一般 K-均匀超图的所有部分配额层写成精确恒等式；它进一步给出低配额双标签逃逸、资源重数至二仍无效的构造，以及一个可以真正接到需求树桥梁的 robust bundle matching 条件合同。两源都没有给出一般 `R||C_max` 困难性，也没有关闭 `UM-TARGET-v1`。

这里的 `b^*` 始终是需求树桥梁中的根树评分，实际调度翻译只在既有 `UM-DAG-DEGREE-TOKEN-IDENTITY-v1` 的输入合同内使用 `OPT=2-b^*`。三维匹配值、高维匹配值和六人 SPE 覆盖值不得互换。

# 一、三维匹配需求树的精确地板

## 1. 定义域

令三维匹配实例为
\[
A=(X,Y,Z,E),\qquad |X|=|Y|=|Z|=q,
\]
允许 `q=0`。令 `nu(A)` 为最大三维匹配大小。令 `mu(A)` 为二分图 `X`--`(Y union Z)` 的最大匹配大小：`x` 与 `y` 相邻当且仅当存在 `z` 使 `(x,y,z)` 属于 `E`，对 `z` 同理。对整数 `K>=2`，需求 DAG `D_K(A)` 的根需求为 `q`；每个 `x` 需求为 1；每个三元组点 `e=(x,y,z)` 需求为 `K`；每个 `y,z` 终端需求为 0。边只有
\[
r\mathbin{\to}x,\qquad x\mathbin{\to}e,\qquad e\mathbin{\to}y,e\mathbin{\to}z.
\]

沿根树桥梁定义
\[
b(H)=\min\bigl(\{1\}\cup\{\deg_H^+(v)/k_v:k_v>0\}\bigr),
\qquad b^*(D)=\max_H b(H).
\]
当 `q=0` 时，正文约定两边值为 0，避免把空根误算成正常正比例。

## 2. 恒等式与双层证明

三维匹配源的自足结论是
\[
\boxed{
 b^*(D_K(A))=
 \max\left\{
   \min\left(\frac{\mu(A)}q,\frac1K\right),
   \min\left(\frac{\nu(A)}q,\frac2K\right)
 \right\}
}\tag{1}
\]
对 `q=0` 使用上述空分支。

下界分成两种树。取 `X`--`(Y union Z)` 最大匹配，并为每条匹配边选择一个见证三元组；在三元组点保留匹配指向的一个终端，得到评分至少为第一项。再取最大三维匹配，并在每个对应三元组点保留两个终端，得到评分至少为第二项。

上界从任意正评分根树读取选中 `X` 点数 `s`。每个选中的 `x` 至少选一个三元组点，且不同 `x` 的父三元组点不同。若评分 `b<=1/K`，从每个已选三元组点任选一个子终端；树的单父条件使得到的 `X`--`(Y union Z)` 边互不冲突，于是 `s<=mu(A)`，从而 `b<=min(mu/q,1/K)`。若 `b>1/K`，每个选中的需求 `K` 三元组点必须有至少两个子终端；它恰好只有 `y,z` 两个子，因此这些三元组两两不共享 `X,Y,Z`，有 `s<=nu(A)` 且 `b<=2/K`。两个情况合并即得式 (1)。这是真实树结构证明，不是把有限枚举当作一般证明。

调用既有桥梁只得到受限实例的翻译
\[
\operatorname{OPT}(P(D_K(A)))=2-b^*(D_K(A)).
\tag{2}
\]
它不增加三维匹配之外的全局一致性。

## 3. 反面含义和锐边界

若 `A` 有完美三维匹配，`mu(A)=nu(A)=q`，式 (1) 给出 `b^*=2/K`。因此把三元组点需求提高到 `K` 会把 YES 的值一起压到 `O(1/K)`，调度值反而趋近 2，不能形成 YES 近 1、NO 近 2 的目标间隙。固定 `K=2` 才可能有 YES 的 `b^*=1`，但此时 `mu` 第一项仍可能遮蔽三维匹配 gap。

例如取 `A_q={(x_i,y_0,z_i):1<=i<=q}`，有 `nu(A_q)=1`、`mu(A_q)=q`，故 `b^*=1/2`，桥梁调度值为 `3/2`；即使三维匹配比例趋于 0，也会被一终端逃逸遮蔽。当 `mu(A)<q/2` 时，式 (1) 的第一项可由普通二分图最大匹配直接识别。因此 `D_2` 不能直接充当近二困难性归约；必须强制同时消费两类终端资源。

正文还给出公共终端目标样板 `Q_{q,K}`。根选 `r` 个变量时，`r` 个中间点必须从同一组 `K` 个资源中取互不相交子集，精确值为
\[
b^*(Q_{q,K})=
\max_{1\le r\le\min(q,K)}
\min\left(\frac rq,\frac{\lfloor K/r\rfloor}{K}\right).
\tag{3}
\]
这说明共享资源 Hall 碰撞可以给出小值，但它本身没有源语言编码；随机低交叠资源集也不会自动产生同样的 gap。

三维源的精确核验脚本使用 `Fraction`：对 `q<=2` 的所有边集、`K=2,...,6` 全枚举正评分根树；对 `q=3` 的空图、满图和固定种子随机边集，在 `K` 的指定集合逐项核对式 (1)，并核对完美匹配族 `b^*=2/K`。这些运行支持实现和边界，不能替代一般性结构证明，也不能证明复杂度困难性。

# 二、高维匹配来源事实与全部配额层恒等式

## 4. 论文事实的准确层次

高维源核对的 Paper Fact 是：Lee、Svensson、Thiery 的工作给固定 CSP arity `k0>=4`、足够大的素数 `R` 的 CSP gap，并在 `NP not subset BPP` 假设下给出近完美/低值区分；其确定性编译把 `R`-degree bounded 的 `k0`-partite CSP 转成 `k0 R`-Dimensional Matching，最大匹配大小等于最大满足约束数；稀疏化带来随机多项式时间，因此假设是 `NP not subset BPP`。这只是高维匹配/集合打包事实，未给 `R||C_max` 编译。

正文明确把 Paper Fact 与本地需求树推导分开；本审查不把文献定理改写成新的调度定理，也不以此宣称无条件 `P!=NP`。

## 5. K-均匀超图的全层公式

给 K-均匀超图 `H=(V,E)`，令 `q=|E|`。需求 DAG 的根需求为 `q`，每条超边对应需求 `K` 的中间点，并连接到其 K 个资源顶点；资源需求为 0。令 `nu_t(H)` 为最多能选多少条超边，使每条被选超边各取 `t` 个资源，且所有资源互不相交，`1<=t<=K`。则
\[
\boxed{
 b^*(H)=
 \max_{1\le t\le K}
 \min\left\{\frac{\nu_t(H)}q,\frac tK\right\}.
}\tag{4}
\]
任意评分 `b>0` 的树选了至少 `bq` 条超边，每个中间点至少送出 `Kb` 个资源；取 `t=ceil(Kb)` 个子资源，单父性给出不交的 `t`-束，因此 `nu_t/q>=b`。反向取达到 `nu_t` 的不交束族直接构造树，三类比例为 `nu_t/q`、1、`t/K`。这就是式 (4) 的完整证明。

当边的资源集大小可小于 K 时，第一源的推广只把 `t` 的范围截到 `1<=t<=min(k,K)`；同样的证明给出所有部分资源层。第二源的单层接口显式保留 `t=0`，公式为
\[
b^*(Q(A;q,K))=
\max_{0\le t\le K}
\min\left\{1,\frac{\nu_t(A)}q,\frac tK\right\},
\tag{5}
\]
其中 `nu_0=|X|` 处理空邻域和 `b^*=0` 边界。

## 6. 直接归约为什么失效

完整 K-匹配只控制 `t=K` 层。若某个中间层 `t` 仍有 `nu_t/q` 很大，式 (4) 或 (5) 就会给出正常数地板。固定 `t_0=floor(K delta)+1` 时，若 YES 有完整 K-匹配，则可截成 `t_0`-匹配；若 NO 要求 `b^*<=delta`，则必须同时压低 `nu_{t_0}/q`。把候选 `t_0`-束看成大小 `t_0+1` 的超边，任意极大匹配满足
\[
|M|\ge \frac{\nu_{t_0}}{t_0+1},
\tag{6}
\]
在 `delta<1/(t_0+1)` 的固定参数范围形成一个多项式复杂度筛选。该筛选只约束此直接束接口，不是一般 UM 算法或 hardness。

一个参数化逃逸族更直接：固定 `1<=t<K`，令每条超边资源集为同一个公共集 `C`（大小 `K-t`）与该边自己的私有集 `P_i`（大小 `t`），并取 `q>=ceil(K(K-t)/t)`。则 `nu_K=1`、`nu_t=q`，而所有私有集给出 `b^*>=t/K`。若评分严格大于 `t/K`，每个选中超边必须再取公共资源，公共集容量又限制根至多选 `K-t` 条，故此族精确为 `b^*=t/K`。完整 K 层可以任意低，而部分层保持指定常数。

## 7. 双标签逃逸与低重数边界

两标签资源集 `A,B` 各大小 K，若 `t<=K/2`，总能取不交的 `t`-子集 `A'`、`B'`。若差集各至少 t，直接取差集；否则差集大小相同，交集大小为 `K-a`，而 `2(t-a)<=K-a` 保证交集还能支付两边。因而仅用两份大小 K 的共享/私有资源集，不能在 `b>=delta` 且 `t=ceil(delta K)<=K/2` 时强制唯一选标签。

资源最大重数限制为二也不够。取偶数 `s`、`K=s^2`，每组 `s+1` 个标签；组内每对标签共享一资源，单标签另有 `K-s` 个私有资源。完整 K-束匹配在每组至多取一条，比例至多 `1/(s+1)`；定向完全图使所有标签同时拿到 `K-s/2` 个互不冲突资源，故 `b^*>=1-1/(2s)`。令 `s` 增大，完整层趋零而需求树值趋一。这个构造把“二重资源/成对冲突足够”的猜测排除为错误。

# 三、可接主目标的 robust bundle matching 合同

## 8. 精确 promise 与需求树编译

给变量集 `X`、`|X|=q`；每个 `x` 有若干标签超边 `e`，每条标签资源束 `S_e` 大小为 K。定义 `(K,delta,gamma)`-robust bundle matching promise：

* YES：存在每个 `x` 的一条标签 `e_x`，且全部 `S_{e_x}` 两两不交；
* NO：对任何 `X'` 且 `|X'|>=gamma q`，任取每个 `x` 的一条标签，再任取 `B_x` 满足 `B_x subset S_{e_x}`、`|B_x|>=delta K`，这些 `B_x` 不可能两两不交。

把它编译成根需求 q、变量点需求 1、标签点需求 K、资源点需求 0 的 DAG，边为 `r->x->e->u`。若 YES，直接选每个变量的完整不交束，得到 `b^*=1`、`OPT=1`。若 NO 中存在 `b>=delta` 的树，根至少选 `delta q` 个变量；每个变量点至少有一个被选标签；每个标签点至少送出 `delta K` 个资源；单父性使这些资源子集两两不交，违反 NO。因此
\[
\text{YES: } b^*=1\Longrightarrow OPT=1,
\qquad
\text{NO: } b^*<\delta\Longrightarrow OPT>2-\delta.
\tag{7}
\]
编译规模是显式标签边与资源束总大小；二进制需求只占对数位长，不按 K 展开虚假输入。这个合同是本批唯一真正把“全层一致性义务”写成可接桥梁的条件结论。

## 9. 当前缺口、旧段落修正和逻辑边界

高维源的 §4--5 旧式反面段落不能不加条件地回填为定理。其原 `NO` 条件若没有 `gamma<=delta`，只能推出 `b^*<max(delta,gamma)`；例如十组共享同一五资源束的参数可满足旧式 NO 描述，却仍有五组各取一资源，得到 `b^*=1/5`。因此必须加入 `gamma<=delta` 才能恢复相应步骤。

此外，“一个固定 epsilon 即否定 `UM-TARGET-v1`”需要对每个固定改善量给出足够近二的 gap，并比较可计算的绝对阈值 `beta`，而不能把未知 `OPT` 当作 decoder 输入。源中的范围更新已把这些段落标成条件反面和待复审内容；本审查保留修正后的 robust bundle 合同，明确不把旧无条件表述升级为主结论。

要从高维匹配 gap 推出主目标的条件 hardness，至少还需：YES 保持 `b^*=1`；对每个固定 `delta` 控制所有 `t>K delta` 部分层；任意 `b>=delta` 的实际树能在位多项式时间解码源见证；随机归约的成功概率可放大。LST 的完整 KDM 匹配值只给完整层，尚未给 robust NO。

# 四、证据、比较、用途与接续

三维源的有限审计覆盖小 `q,K` 的全枚举与固定种子实例；高维源的核验脚本使用 `Fraction` 检查公共资源加私有资源族的 `nu_t` 公式、式 (4) 的小规模树值、双标签同时支付和边界。它们是有限实验与实现核对，不能替代式 (1)、(4)、(5) 的结构证明，也不能证明文献新颖性或复杂度结论。

与已归档的 `k均匀束与单层配额超图双源审查` 比较：本批把三维投影 `mu`、完整三维匹配 `nu` 的两项闭式和高维 KDM 的文献 gap 接到同一全层公式；前一审查的 `t=0`、固定层极大匹配地板和单层接口在这里作为直接比较对象，而本批独有的是三维一终端逃逸、双标签 Hall 逃逸、二重资源仍失败的正则构造以及 robust bundle promise。与 `标签碰撞低重数地板与全层配额近二双源审查` 比较：共同核心+私有族的显式 near-two 整数实例说明全层损失可以精确实现，但本批进一步说明怎样把源问题的“全变量、全标签、全层”条件写成可解码的 NO 合同。与 `有向需求桥与共同拥塞流三源有限审查` 比较：两批都复用 `OPT=2-b^*`，但本批不提供一般支撑搜索或流算法；其用途是给后续 gadget 设计列出必须逐层满足的数学义务。

完整结论包括式 (1)、(4)、(5) 的精确恒等、三维匹配的 `mu`/`nu` 反面机制、KDM 部分层参数化逃逸、低配额双标签 Hall 恒等、资源重数二仍趋一的构造，以及 robust bundle promise 到需求树的条件编译。未成熟内容包括 LST gap 到 robust NO 的构造、跨层一致性 gadget、真实低负载调度解码、固定 epsilon 的位复杂度、文献外部评审和一般 `UM-TARGET-v1` hardness。所有空主题、零客户、离轨历史等六人 SPE 语义与本对象无关；六人 SPE 覆盖目标仍保持独立开放。

# 处置与接续

两源均按 `integrated` 处置。三维源独有的 `mu`/`nu` 双层恒等式、一终端逃逸和 `K=2` 解码边界已写入第一、二节；高维源独有的 LST Paper Fact、全层 `nu_t` 恒等式、低配额双标签与低重数正则构造、robust bundle 条件合同和旧段落修正已写入第二、三节。后续研究应优先尝试证明 robust bundle matching 的全层 soundness 或构造跨层一致性 gadget；在此之前不得把完整 KDM gap、有限审计或显式 near-two 族写成一般不可近似性。
