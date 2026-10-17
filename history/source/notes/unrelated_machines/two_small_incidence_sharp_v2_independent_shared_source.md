# 每行两条小资格三半界：仅陈述后的独立重构

审查对象：`UM-TWO-SMALL-INCIDENCE-SHARP-APPROXIMATION-v2`。

仅实际读取精确陈述 `/workspace/scratch/038d9dcc4cac/two_small_incidence_sharp_approximation_v2_exact_statement.md`，SHA256 `051148816053f0c150ee70c9efa1b3f7cb76ecc46b999d793155b4070e3cd065`。未读作者证明、root slot proof、其它审查、root 提及但尚未传来的 PSM2018 prior。本稿来源为 Exact-first 独立算法与归约重构；此前曾研究本仓 Santa Claus/AFS/Haxell 桥，不把这种一般背景伪称隔离。root 在收到我已重构的容量表摘要后认可其方向，该回复未给新证明机制。

结论：给出的四项精确合同均独立重构成立；无 standing fatal。新颖性、独立论文价值和作者尚未提供的实现均不认证。本稿容量表是独立证明工具，不另立现行 Claim。

## 1. 先删去有零端的任务

每个有零资格的 job 固定到任意一条真实零端，记下全部这些原 job 的最终位置。删除这些 job 后，每行仍至多两条严格介于 0 与 b 的资格，且所有剩余 finite 值正。零 job 永不产生容量消耗，故这一步保存 OPT，之后可无条件回填。若没有剩余 job，则完整调度 OPT=0；包含 n=0。此举不把有零端但可能存在其它正端的 job 丢失。

## 2. T<b 的 exact flow

禁止所有 unit b 资格，也禁止值大于 T 的 small 资格。每行剩至多两个 eligible jobs。若两者的时间和不超过 T，该 machine 给 capacity 2；否则给 capacity 1。每个 job 到其所有剩余 finite 行连 capacity 1，源到 job 容量 1，machine 到汇点为上述容量。

整数满流当且仅当完整真实 C<=T 调度存在。关键是行容量 2 时仅有那两个真实任务，允许同时选择不会超载；行容量 1 时任一允许任务均不超过 T。反向每个真实调度显然给同一流。

OPT<b 时，某一最重行的负载属于显式集合 {0}、某条 small 值、某行两条 small 值之和；只保留小于 b 的候选。至多 1+3m 个数，精确排序逐一跑流可查明是否存在 OPT<b，并取第一成功者得到 exact OPT 调度。完全不按处理时间数值枚举。

## 3. T>=b 的独立局部容量包络

为简明统一算法分析，写 T=ell*b+a，ell=floor(T/b)>=1，0<=a<b。本段允许一般 ell，仅作为证明已给四项合同的工具；不新增现行 Claim。记该行的 unit jobs 集合为 U，选中的 unit 数为 u；至多两条 small 资格按 p<=q 排列，任务标为 x,y。每条 small 是资格，不是已分配量；原 job 可以在任意多个行有 small/unit 端。

以下都是普通整数容量约束，覆盖该行每一个真实负载<=T 的任务集合。每个被允许的集合真实负载<=T+b/2。

| 该行 small 型 | 采用的局部容量约束 |
|---|---|
| 无 small | u<=ell |
| 仅 p，p<=a | u<=ell；x 自由（仍至多一次） |
| 仅 p，p>a | u+1[x]<=ell |
| p+q<=a | u<=ell；x,y 各自由 |
| p+q>a 且 q<=a | u<=ell；u+1[x]+1[y]<=ell+1 |
| p<=a<q | u+1[y]<=ell；x 自由 |
| a<p 且 p+q<=b+a | u+1[y]<=ell；x 自由 |
| a<p 且 p+q>b+a | u+1[x]+1[y]<=ell |

证明逐项如下。

- 任一原可行集合的 u<=ell；当 u=ell 时 small 总和须<=a，当 u=ell-1 时 small 总和须<=b+a；u<=ell-2 时任意两个 small 都能保留，因为 p+q<2b。
- 前六型的容量描述是原真实可行族本身。尤其 p<=a<q 时，p+q<a+b，故 ell-1 个 unit 与两个 small 总可共存；q<=a 而 p+q>a 时，只需再限制总基数 ell+1。
- 第七型是唯一扩大。原 feasible 集合若含 y 至多有 ell-1 个 unit，故 u+1[y]<=ell。新增的最大负载为 ell*b+p，其相对 T 的超额 p-a。由 p<=q、p+q<=b+a 得 p-a<=(b-a)/2<=b/2。含两个 small 时至多 ell-1 个 unit，负载仍<=T。
- 最后一型，ell 个 unit 不能加任何 small，ell-1 个 unit 不能加两个 small；而 ell-1 个 unit 加任一个 small 的负载<ell*b<=T，ell-2 个 unit 加两个 small 的负载<ell*b<=T。因此总基数 ell 是 exact（ell=1 时不出现负单位数情形）。

注意第七型并不假定 small p<=b/2；只需要 p-a<=b/2。不能直接将所有 small 当作半单位任务。

这些容量约束可直接编译为普通 max-flow：

- `u<=ell` 用 unit 子节点到汇点 capacity ell；自由 small 各用自己的 capacity 1 节点。
- `u+1[y]<=ell` 让 U 和 y 共同进入 capacity ell 节点，自由 x 另走 capacity 1。
- 同时要求 u<=ell 和总基数<=ell+1 时，用 unit 子节点（到行节点 capacity ell），small 直接入行节点，行到汇点 capacity ell+1。
- 总基数<=ell 时所有任务直接入同一 capacity ell 行节点。

源到每个未删除 job capacity 1；该 job 到所有真实资格对应的局部节点 capacity 1。故整数满流输出每个原 job 的一个真实 finite 端。若原 C<=T 调度存在，它在上述包络中可行，必满流。任意满流的每行真实负载<=T+b/2，零任务回填后全机仍满足同界。FAIL 因而严格证明 OPT>T，没有调用 OPT 或 YES 见证 oracle。

对陈述第3项 ell=1，即所得 C<=3b/2+a；又 3b/2+a<=3(b+a)/2。

## 4. 全局三半近似，不漏 OPT>=2b 或松 b

对非零剩余任务数 N 构造候选集合：每行 small 子集和 s（空、单个或两个，共至多4项），对每个整数 k=0,...,N 加入 k*b+s，并保留 0<=k*b+s<=N*b。候选数 O(mN)，每个编码长度为输入位长多项式。

任何完整调度的最重行有若干 unit 加该行至多两个 small，因此 exact OPT 一定在候选中。合法输入总有某个调度，且每任务 finite<=b，故 OPT<=N*b。先用第2节判别是否 OPT<b，若有则直接输出 exact 最优解。

若没有，已知 OPT>=b。将 >=b 的候选递增扫描，在每个 T 上运行第3节流，取首次成功者。至迟到 T=OPT 必成功，故实际取的 T<=OPT。输出负载<=T+b/2<=OPT+b/2<=3OPT/2。

这一论证不需要成功/失败关于 T 单调；只要逐一扫描显式多项式候选。也不假设 OPT<2b，不假设存在实际时间恰为 b 的资格。b 极松时若 OPT<b 会走 exact 分支。若 b 并不极松而 OPT 很大，第3节的 ell 只是二进制容量，或截为 N；绝不循环至数值 T/b。所有原 job（包括所有 zero jobs）有明确输出位置。

## 5. Perfect3DM 锐困难性重构

源为非空平衡 3DM：三份不交集合 X,Y,Z 各 q>=1，显式 triples E subset X×Y×Z。若任一元素未在任何 triple 中出现，则源显然 NO，直接返回合法常量 NO 调度实例：一台机器、两件 unit 1 任务，OPT=2、b=1、small 行数0。其它退化的无 triple 源同样处理。q=0 的源不在指定非空源域；若另扩源域，该分支应送常量 YES，不能误送 NO。

令 M=|E|。每个 triple e=(x,y,z) 建一台机器 i_e。对每个 x 建一 job X_x，恰在包含 x 的 triple 机器上时间 1/2；对每个 y 建 Y_y，恰在包含 y 的机器上时间 1/2。对每个 z，建 deg(z)-1 个不同 unit jobs，皆恰在包含 z 的机器上时间 1。未说的资格全部无限。

每行严格只有两条 small 资格 X_x,Y_y；unit 资格可多。每 job 最多两种时间（实际上本构造每 job 仅一种时间）。所有 job 均有 finite 端，m=M>=1，n=2q+sum_z(deg(z)-1)=M+q，显式位规模多项式。所有 finite 值仅 1/2 或 1，无零资格。

YES：一个 perfect matching 中 q 台机器各接该 triple 的 X_x,Y_y，负载1；每个 z 剩余 deg(z)-1 台机器分别接其 unit jobs，负载1。全部原 job 恰一次。

反向 C<3/2：所有负载在半整数网格上，所以 C<=1。M-q 个 unit jobs 占不同机器，且 unit 行不能再接任何 small。剩 q 台机器需放完 2q 个 small jobs，每行最多两个，因此这 q 台全部恰好接 X_x,Y_y。每个 z 的 unit jobs 先占其机器组中 deg(z)-1 台，所以至多留下该组一台；全局恰留下 q 台即每 z 恰留一台。这 q 个 triples 同时精确覆盖全部 x,y,z，得到 perfect3DM。故源 NO 必 OPT>=3/2。

因此任何固定 rho<3/2 的保证算法在 YES 输出 C<=rho*OPT<=rho<3/2，而在 NO 一切合法调度 C>=3/2；可以直接解 NP-complete 3DM。若只允许 rho>=1 属通常近似因子；rho<1 本身更不可能，合同中“每 rho<3/2”没有反例。

## 6. 外部标准源与核验范围

亲自联网取得并视觉读取 Karp 1972 原文的2010重印：Richard M. Karp, Reducibility Among Combinatorial Problems, 原印 pp.94–95；重印 pp.232–233；PDF pages14–15（1-based）。原文主定理列出 complete problems，下一页 #17 是 U subset T×T×T、要求大小 |T| 且各坐标不重复的 3DM，等价于本稿三份不交坐标集的 perfect3DM。

主文原PDF重印：https://www.cs.umd.edu/~gasarch/BLOGPAPERS/Karp.pdf 。作者/伯克利目录另核书目信息：https://www2.eecs.berkeley.edu/Pubs/Faculty/karp.html 。首次找到的 GWU 原扫描10MB网页阅读失败，未假称该次成功；实际取得和读取的是 UMD 上原文授权重印。下载 PDF、局部渲染仅是审查 scratch，不登记文献资产。

本稿不涉及第三条 small 行推广；不否定一般 UM 离二改进或 reverse 主目标。有限 probe 只审计局部表、真实全 job 荷载及归约的小源，不代替上述一般证明。probe 自包含 max-flow 与独立全赋值 oracle，未导入作者代码。
