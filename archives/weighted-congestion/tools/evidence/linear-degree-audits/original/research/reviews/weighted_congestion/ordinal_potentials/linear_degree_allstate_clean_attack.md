# 线性次数全状态无均衡族的先重构后冻结独立攻击

本轮结论：对下面绑定版本，逐式检查未发现尚成立的 fatal objection。正文中的一般参数论证闭合了基体闭环、全部前沿覆盖、非法状态修复、原次数预算和否定量词；有限计算只核对本文件明确列出的恒等式与一个起点。此结论是内部独立数学审查，不代表外部同行评审、全球优先权或最优常数认证。

## 1. 审查对象、冻结身份与独立性

对象为 [一般证明正文](../../../current/weighted_congestion/linear_degree_allstate_lower_bound.md) 的四个身份：

- `WC-HEALTHY-LINEAR-SWEEP-v1`；
- `WC-HEALTHY-FRONT-COVERAGE-v1`；
- `WC-LINEAR-DEGREE-ALLSTATE-NONEXISTENCE-v1`；
- `WC-MATCHING-LOG-UPPER-NEGATIVE-v1`。

精确主张是：对每个整数 $p\ge2^{20}$，存在有限非空玩家/资源、正有理权、每人恰两个非空不交资源子集动作、全部费用为正有理系数乘 $x^p$ 的游戏，每个纯状态均有真实单人严格 $p/10$ 改善。由此对每个实 $C\ge1$ 与整数 $d_0\ge2$，存在 $d\ge d_0$ 的 MODEL 游戏没有 $(Cd/\ln d)$-PNE。

审查过程先只读根 AGENTS、分支 AGENTS、[MODEL](../../../weighted_congestion_frontier/MODEL.md)、ACCEPTANCE 和现行相关 README，自主重建必要条件；起始工作树 HEAD 为 `d5492a5deb217e85f438a38a4809057d8ece1f6e`。随后才收到候选正文。没有阅读其他 review 的结论，没有将其他审查或有限实验当作本证明的前提；本轮不进行 Git 写入或公屏操作。

| 版本 | SHA256 | 实际核查 |
| --- | --- | --- |
| 首次完整合并候选 | `c1f846520baa918b5506013e7a2704fb059e64f1f03c6699c0183b799ee0029c` | 全文逐式攻击；从 literal 资源关联重建关键端点 |
| 首次规范正文修订 | `def2b498fca93bfb68e5c9096b0cde127e6165c5ca84daa144de74cff6f0ebca` | 与首稿逐行 diff；补 W 定义、删除未定义 B_actual、调整状态/文献/配套链接 |
| 本审查绑定最终正文 | `04181c4d5c09fb85ac84270e06743571e156a8334611943aa5f6b865f9409c33` | 实际重算 hash；确认显式线性顺序与 clean 代码/证据链接；再次确认数学公式未变 |

首稿首次使用 W 时未定义，已要求补写 $W=(1+1/p)^p$。最终稿已修正。首稿“至多一次相邻变化”由相位定义和首位论证已可解释为线性顺序；最终稿进一步显式写明 `0,...,N−1`，消除了措辞歧义。这两项均未留下尚成立的数学反驳。

## 2. 未读证明前自主重建的必要条件

这些必要条件独立于候选路线；没有把“未击中”解释为证明成立。

### 2.1 资源支持与玩家数必须增长

记 $M_s=\max_e|\{i:e\in S_i^0\cup S_i^1\}|$。对任意非减费用，未乘权社会成本 $\sum_iC_i$ 是 $M_s$-近似势：离开资源的社会成本降幅至少为该玩家的旧费用；加入资源的社会成本增幅至多为加入后人数乘新费用，因而至多 $M_s$ 倍该玩家的新费用。共有资源的负载不变。取全局最小点得到 $M_s$-PNE。

所以本主张必须有 $M_s>p/10$，并有 $n>p/10$。固定玩家数或固定资源支持的大倍率反例均会被此条件否定。

候选有 $n=mN$；邻接资源支持为 $Q+1$，返回资源支持为 $N+1$，clock 支持为3；故最大支持是 $N+1\gg p/10$，不冲突。这里 $m$ 是正文的类数，不能误当总玩家数。

### 2.2 每次动作改变的资源数不能一致有界

对正单项式，取全部资源费用降序排序向量的字典序最小纯状态。若某偏离满足“旧离开资源的最大费用严格大于新加入资源的最大费用”，则最高改变层至少有一个资源因减载严格下降，加入后的全部改变费用都更低，矛盾。

因此这个状态是 $R_s$-PNE，其中

\[
R_s=\max_i\max\{|S_i^0\setminus S_i^1|,
                     |S_i^1\setminus S_i^0|,1\}.
\]

证明最后一步是 `sum ≤ R_s·max`，共有资源费用再加回。故必须 $R_s>p/10$。相同关联签名的资源可先合并系数，不能仅靠复制相同资源逃避此检查。

候选加入 clock 后，非锚点类0玩家每个动作已有 $2+(N-2)=N$ 个资源；末类锚点为 $L_c+N+Q$。动作规模足够大，不冲突。

### 2.3 高次近精确势迫使极小共占份额

记

\[
\theta=\min_{e,i:e\in S_i^0\cup S_i^1}
\frac{w_i}{\sum_{j:e\in S_j^0\cup S_j^1}w_j},\qquad
\delta=1-(1-\theta)^p.
\]

对势 $\Phi=\sum_ea_ex_e^p$，离开资源的势降幅至少为旧费用的 $\delta$ 倍，加入资源的势增幅至多为新费用。势最小点因而为 $\delta^{-1}$-PNE。无 $p/10$-PNE 必须有

\[
\theta<1-(1-10/p)^{1/p}
<-\frac{\ln(1-10/p)}p
\le\frac{10}{p(p-10)}.
\]

候选邻接最小潜在份额为 $1/(2Q)$，返回末类份额为

\[
\frac{\varepsilon}{1+1/p}=\frac1{(p+1)N},
\]

clock 为 $1/3$。故全局最小份额是返回末类份额，足够小以避开上述存在保证。全同权、固定非退化权谱等简单反驳不适用。

## 3. 从 literal 关联重建的关键端点

没有先采用正文的成本表作为输入。将 light 相位归零，取 forward mover 为 index0。它参与的窗口中心为 $h_k=-k\bmod N$，$k=0,...,K-1$。直接按动作位 xor 关联相位统计：当前同侧 light 人数为 $K-k$，翻位后目标侧包含自身的 light 人数为 $k+1$。

返回 orientation 为+，因此 mover 在中心 $h_0=0$ 的关联为1，在其余 $h_k=N-k$ 的关联为0。令 heavy 相对相位为 r，得

\[
e_k(r)=1[B_r(h_k)=1[k=0]],
\]

\[
O(r)=\sum_{k=0}^{N-1}((N-k)\varepsilon+e_k(r))^p,
\quad
Q(r)=\sum_{k=0}^{N-1}((k+1)\varepsilon+1-e_k(r))^p.
\]

这包括偏离者自身重量，没有把全部 front 当成一个玩家。

- 偶奇累计为偶数时 $r=-T\bmod2N$。当 $T=0$，仅 $e_0=0$；当 $1\le T<N$，恰 $e_0,...,e_T=0$，其余为1。
- 累计为奇数时选择 backward。它是上一 forward 边的反边；扭转归一化后的相对相位是 **r+1**。代入 $r=N-T$，在 $r+1=N-T+1$ 处恰有 T 个 e 为1；T=0 时全0。

故两种选向都从有利全同基准 $(U,V)$ 损失至多 $(\alpha+1)(T+1)W$。每个缺陷对旧、新费用的改变量分别至多 W，给出的是真实逐资源成本比较。

邻接 heavy forward 由同一关联直接得到

\[
n(r)=Q-\min(r,Q)\;(0\le r\le N),\qquad
n(r)=\min(r-N,Q)\;(N\le r<2N).
\]

其成本为 $A_a(1+n/Q)^p,A_a(2-n/Q)^p$，backward 为 r+1 表的反向。任意 front 的 light 两方向成本均不超过 $A_aX$，因为旧 light 计数枚举 Q,...,1，新计数枚举1,...,Q，heavy 指示逐项至多1。

共同扭转确实使每类相位加1。窗口集平移不变；线性先后指示改变为旧指示 xor 两端 wrap 标志。light 动作 wrap 与自身关联 wrap 抵消，只余 heavy wrap 引起的资源对换侧；两侧费用相同。因此当前与单人翻位后成本均保持。没有把其他类归零。

## 4. 全部一般参数义务的逐式核查

| 义务 | 独立核查内容 |
| --- | --- |
| 参数合法性 | $m-1=\lceil\log_2p^2\rceil$，$N=p^{4m-5}$ 为整数；p≥20 时 m≥3、m≤p、N≥p⁷>Q。所有权与系数正有理；每对资源两动作恰各用一侧。 |
| 真实双扫环 | 按全局 pos 单人翻位，邻接 heavy 为 $(A_a2^p,A_a)$、light 为 $(A_aY,A_aX)$；返回 heavy 为 $(A_R,A_RW)$、light 为 $(A_RU,A_RV)$。第二轮是资源侧互补，成本重复。 |
| 标量与幅度闭环 | 右 Riemann 和上下界给 $4/Q\le H/L\le40/Q$；$Y\le2^{-p}X$，$Z\ge0.9N$，$0<J<3\alpha$。代入幅度得 $A_RZ/(A_{m-2}L)>3\,2^{m-1}/p^2\ge3$。 |
| 环余量 | 类0恰 H/2；中间类为 $A_{a-1}L>H/2$；末类 $>HZ/(3J)>H/(p^2\varepsilon)>H/2$。所以环最小值恰 H/2，不是仅证一个较弱下界。 |
| 全部基体状态 cap | 邻接潜在总重为 $2w_a$，单个 light 参与 Q 窗口；返回总重 $1+1/p$，末类参与 N 窗口。按任意状态最大可能负载得 $B_*=mQ^{m-1}2^p$，没有使用只在 sweep/front 成立的计数。 |
| 邻接出口 | 短区间外选到 margin $A_aH$ 的 heavy 方向。中间类扣至多 $\alpha A_{a-1}X$ 后 $>H/2$；类0扣返回新费后为 $H(J-1)/(2J)>H/3$，因 J>3。 |
| 剩余全部 front | 若所有邻接差在两短区间，累积为 kN+T，$0\le T\le(m-1)Q<N$。第3节的 literal 返回端点覆盖 k 的两种奇偶。 |
| 前沿统一余量 | $D_0\le(3/5)p^6\le Z/30$ 用 p≥20、N≥p⁷。再用 $A_RZ>3A_{m-2}L$、$\alpha X\le2L$，末类 margin $>(29/10-2)A_{m-2}L>H/2$。故每个 front 有保 front 出口，统一可取 $\eta_0=H/4$。 |
| 非 front 修复 | 全部 anchored triples 不触发当且仅当线性类位串至多一次变化。非法类取最早异位 i；有某后位 j 回到首位，故旧费至少 M。翻回首位后，i 作中位时与锚点相同，作末位时更早中位与锚点相同；所有参与 clock 均不触发。 |
| 完整单人偏离 | front 的旧、新状态都不触发，损失至多 $\alpha L_cM(2/3)^p\le\eta_0/2$。非法修复的完整 margin 至少 $M-\alpha B_*-\eta_0/2\ge\eta_0/2$。M仅依赖基体 cap，不存在循环预算。 |
| 原次数预算 | $4\alpha^2B_*L_c/\eta_0\le(8/45)mp^{12m-12}\le mp^{12m-12}$。由 $m-1\le5\ln p$、$\ln(3/2)\ge1/3$ 得 $D_*\le180\ln^2p+3\ln p+1\le184\sqrt p\le p$，后两步在 p≥2²⁰ 成立。实际资源直接采用整数次数 p。 |
| 原题全部量词 | 取整数 $k\ge\max\{20,\lceil20C\rceil,\lceil\log_2d_0\rceil\}$，d=p=2ᵏ，则 $\ln p>k/2\ge10C$。严格 p/10 改善直接给目标倍率的严格改善。 |

所有玩家两个动作非空且资源系数为正，所以当前与偏离成本实际均正。即便只使用非负成本，最后的严格 margin 论证也没有除零或 0/0。资源集合相互独立、权不随资源改变，没有玩家特定资源费用、负系数、同时移动或费用次数的偷换。原题允许的空策略与零费用不必加入此反例子类。

## 5. 外部定理与不能外推的范围

核对了 Caragiannis–Fanelli 的 [ICALP 2019 原文](https://drops.dagstuhl.de/storage/00lipics/lipics-vol132-icalp2019/LIPIcs.ICALP.2019.133/LIPIcs.ICALP.2019.133.pdf) Theorem 3：全类次数 p 有 p-近似势与 p-PNE。p/10<p，不矛盾。该定理不是反例证明前提。

另核对 Christodoulou–Gairing–Giannakopoulos–Poças–Waldmann 的 [2022 原文](https://arxiv.org/pdf/2002.07466) 模型定义及 Theorem 4：未乘权成本约定一致，一般非减费用 n 玩家有 n-PNE。候选 n=mN 足够大，不矛盾；第2.1节另自行重建了更局部的支持数版本。

“每人两动作”不等于 singleton 或 matroid 策略族；不能套用那些 exact-PNE 定理。此轮仅排查上述具体冲突，没有完成全球文献与优先权审查。

## 6. 独立代码、实际命令与证据范围

[独立脚本](../../../../tests/audits/weighted_congestion/cyclic_clone/clean_attack_linear_degree.py) 不导入研究模块或其他审计，构建实际资源对、各玩家两资源集动作，以 Fraction 重新汇总真实负载与费用。保存规范资产时查看了旧审计的运行布局和 replay 包装器；没有把旧审计结论作为本轮数学或代码断言的依据。

实际执行命令（仓库根目录）：

```bash
python3 tests/audits/weighted_congestion/cyclic_clone/clean_attack_linear_degree.py --output evidence/runs/weighted_congestion/cyclic_clone/linear_degree_clean_attack.json
```

CPython 3.12.14，确定性，无随机数/seed；只用整数和 `fractions.Fraction`，无浮点、Decimal、舍入或误差容限。输出采用独占创建，拒绝覆盖已有文件；不带 `--output` 时仅输出 stdout。实际运行 exit code 为0。[冻结 JSON](../../../../evidence/runs/weighted_congestion/cyclic_clone/linear_degree_clean_attack.json) 记录完整输入、命令、解释器、运行时 HEAD 与代码 hash。

| 输入与覆盖 | 实际结果 |
| --- | --- |
| 辅助 literal 测试 $(N,K,p)=(3,3,3),(5,2,3),(7,3,3)$；邻接权比1/K，返回权比1/$pN$ | 120条双扫边、60条 heavy 双向端点、60条邻接 light 双向端点、120个 light 成本上界、60条返回 light 双向端点均通过 |
| 同一辅助输入的相位缺陷与扭转 | 30个缺陷模式、30个缺陷 margin 下界、5312次当前/偏离后扭转费用比较通过 |
| 单类 clock，N=3,...,7，次数3，权2/5、幅度7/3 | 穷尽248个位串，2808个资源触发恒等式、198次非法修复、100条保 front 边通过 |
| 实际起点 p=2²⁰ | m=41；直接整数交叉乘检验 CLOCK 通过，左/右整数 bit length 分别为2106762与2710538；未使用对数近似或巨大有理数的浮点计算 |

实际起点检验清除分母后是

\[
40p^2mQ^{m-1}L_c2^{2p}
\le(250\,2^p-25p)3^p.
\]

小参数是检验关联恒等式的辅助游戏，不是声称 p=3 达到一般定理起点。单个实际起点计算不能证明其上全部次数；全参数预算由第4节核对的分析链承担。代码没有、也不声称穷尽巨大 $G_p$ 的全部纯状态。

| 资产 | SHA256 |
| --- | --- |
| 独立脚本 | `98f61e99f5516424e33faa411397255b2d37eba90c5a24e9997d26e1a0bb43b5` |
| 冻结 JSON | `a495370776bdcd922b2983ecc50de6211a87995b6db3fb03b3396da90d00071c` |

## 7. 审查结论与交接边界

从精确 statement 自主重建的三类必要条件没有否定本构造。之后对绑定冻结正文的 literal 关联、各一般不等式和穷尽分支逐项攻击，未留下尚成立的 fatal objection。W 定义和线性顺序表述已经在最终版本修正；这些修订与证据层级已分别记录，未倒写成首稿原有内容。

本文件的数学判断来自一般论证，不来自 confidence、有限实验成功、其他审查赞同或入库位置。全类否定、内部审查通过与有限实现回归是分别记录的层级。仓库图、账本、最终提交/推送及外部评审不属于本轮写入范围，交由父任务单独核验。
