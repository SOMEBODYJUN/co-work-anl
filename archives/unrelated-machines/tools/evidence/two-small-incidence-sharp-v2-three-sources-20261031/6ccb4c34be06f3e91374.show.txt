# 每机两条正 small 资格的三半算法：独立 Exact-first 重构

## 读取与隔离记录

仅先读新 Exact：

`/workspace/scratch/038d9dcc4cac/two_small_incidence_sharp_approximation_v2_exact_statement.md`

实际 SHA256：`051148816053f0c150ee70c9efa1b3f7cb76ecc46b999d793155b4070e3cd065`。

绑定 ID：`UM-TWO-SMALL-INCIDENCE-SHARP-APPROXIMATION-v2`。冻结本稿前未读作者／其它 agent 的证明或此候选新增正文，未询问构造思路。本人按 Exact 独立推导下述实际流网络、全输入算法和 3DM 归约。已有常识包括普通二部匹配、整数最大流、有理 LP 与有序槽舍入；有序槽负载界在本稿重新证明。

下界 primary 来源已实际核读现有 Karp1972 的2010原文重印 PDF 中原印94、95页，不以作者新候选证明为来源；详细范围见第6节。

## 结论

四项均可独立闭合，未发现 fatal objection。阈值程序可用整数流直接构造实际 σ，不需要 YES witness 或 OPT oracle；全类三半算法还需覆盖 OPT≥2b 的情况，本稿用独立重述的 L+b 槽舍入补齐。3DM 归约在每行恰至多两条 small、所有 finite 仅1/2或1的类内给匹配的三半下界。

没有认证生产实现、新有限运行或新颖性；不升级一般 UM。

## 1. 零值预处理

将每个存在 zero 资格的 job 固定到一个指定 zero 端并从后续正时间子问题移除。它们贡献0负载，也不占正资格行容量。任意原调度中的这些 jobs 都可移到 zero 端而不增加负载，因此残余实例与原实例 OPT 完全相同，残余每 job 的所有 finite 端均正，且每 machine 仍至多两条 positive small 资格。

残余空时立即输出全部 zero 分配，C=OPT=0；包括 n=0。以下假定残余非空。最后所有输出均回填这些原 zero jobs。

## 2. T<b 的精确实际判定与精确最优值

给 0≤T<b，所有 unit 资格 p=b 不可用。删去所有 p>T 的资格。每 machine 剩至多两条 small 资格。

- 若两条都在，且两处理时间之和≤T，则为该机器建立两个分别只连对应 job 的独立槽。
- 其它情况该机器仅给一个容量1槽，连其全部剩余 eligible jobs；无 eligible 时不必给槽。

残余 jobs 到这些槽的二部图有覆盖全部 jobs 的匹配，当且仅当存在 C≤T 的实际分配。必要性：任何 T 可行调度只有在 pair sum≤T 时才会把两个 jobs 放同机，按其各自槽映射；否则每机至多一枚。充分性：各槽的物理机分组正好只允许合法单枚或合法 pair。

最大匹配失败可输出通常 alternating reachability 的 Hall deficiency 集作为无可行性证据，保证 OPT>T；成功输出具体 matched 机器端，负载逐机≤T。T=0 的非空正实例自然失败。

若 OPT<b，最优实际调度每机至多两枚 small，且最大负载取自显式候选集

\[
 \{0\}\cup\{p_{ij}:0<p_{ij}<b\}\cup
 \{p_{ij_1}+p_{ij_2}<b:\text{同机两条 small}\}.
\]

共 O(m) 个候选，按精确有理比较排序；在其上作匹配判定找最小可行值，就可判断是否存在 OPT<b，并在存在时输出精确 OPT 及原完整 σ。无可行候选便保证 OPT≥b；不需要对 b 附近作无限或逐数值步进搜索。

## 3. T=b+a<2b 的实际阈值流网络

固定有理 0≤a<b，令

\[
 c=b/2+a,\qquad D=b+c=3b/2+a.
\]

每 machine i 的残余 positive-small 资格集记 S_i，|S_i|≤2，small 时间总和 A_i=Σ_{j∈S_i}p_ij。单位资格总量不限，job 可在不同机器具有任意多种 small/unit 选择。

若 A_i≤c，称该机器为 easy：单位资格共享容量1；全部 small 资格独立可用，机器总容量 K_i=1+|S_i|。该处 small 均≤c。

若 A_i>c，机器总 job 容量设 K_i=2；把全部 unit 资格及满足 p_ij>c 的 small 资格放入同一个 big 资格组，共享容量1；其余 small 是 light 资格，不经过 big 容量门。

这形成显式整数流网络：source→每 job 容量1；每 job 按其原 eligible 资格连对应机器，big 资格经该 machine 的容量1门、light 资格直接入该 machine；machine→sink 容量 K_i。easy 处 big 门仅含 units。所有容量为 1、2 或3，source 流总值要求为残余 job 数。

### 任何 OPT≤T 的真实调度都嵌入流

因为 T<2b，每机至多一枚 unit。easy 的容量显然容下至多一 unit 与其全部 small。hard 若有三枚 assigned jobs，只能是一 unit加全部两 small，负载 b+A_i>b+c>T，因此 T 调度在 hard 机器至多两枚 jobs。

hard 机器不能同时接受两个 big 资格：两 units 的和2b>T；unit 加 heavy small 的和>b+c>T；两个 heavy small 的和>2c=b+2a≥b+a=T。因此每组容量1也被任何 T 调度满足。

所以若 OPT≤T，整数满流必存在；无满流时可以返回 FAIL 和容量小于 job 数的 min-cut，保证 OPT>T。这里不先给 YES witness，只是用其存在性证明网络不会失败。

### 任意整数满流都给 D 负载调度

easy 机器至多一 unit，所有 assigned small 总负载≤A_i≤c，所以负载≤b+c=D。

hard 机器至多两枚 assigned jobs，且至少其中一枚为 light（除非仅一枚）。light 时间≤c，任何 finite 时间≤b，所以两枚合计≤b+c；一枚≤b。无非原资格，每 job 一单位 source 流确保恰分一次。

最大流积分性给实际 σ，成功始终 C≤D，而 D≤(3/2)(b+a)，因为 a≥0。成功不保证 OPT≤T，FAIL 仅保证 OPT>T，正好匹配 Exact 项3。

## 4. 覆盖全输入的实际三半算法

先执行第1、2节；若 OPT<b，返回其精确最优 σ。否则 OPT≥b。

### 4.1 O(m) 个候选补齐 b≤OPT<2b

每机至多两条 residual small 资格，记其所有子集为 A⊆S_i。形成候选集

\[
 \{b\}\cup
 \left\{k b+\sum_{j\in A}p_{ij}:\ i\in M,
 k\in\{0,1\}, A\subseteq S_i\right\}\cap[b,2b).
\]

共 O(m) 个有理值；即使某候选来自该机不存在的 unit 资格，也只增加无害的尝试。对各候选运行第3节，保留所有成功的实际 σ。

若 b≤OPT<2b，最优调度每机至多一 unit、至多两 small，所以某台达到最大负载的机器给出上述候选 OPT；在 T=OPT 的程序保证成功，且其 σ 的实际 C≤(3/2)OPT。

### 4.2 L+b 槽舍入补齐 OPT≥2b

独立构造：解通常 fractional assignment LP，Σ_i x_ij=1、x≥0、每机 Σ_j p_ij x_ij≤L，最小化有理 L。每 job 至少一个 finite 端保证可行，L≤OPT。

对每机按 p_ij 降序把其 fractional job 质量依次铺成总长度 Σ_jx_ij 的区间，切成单位质量槽，最后一槽可不足1。将 job 连到它在该机铺设质量相交的所有槽。该二部图有覆盖 jobs 的 fractional matching，故有整数覆盖匹配，可用普通最大匹配找出。每份 machine-job 质量区间长度≤1，故在该 machine 至多跨两槽；全图规模按显式资格数多项式。

在任一机器，首槽 matched job 的时间≤b。每个后继槽 matched job 的时间不大于前一满槽的平均处理时间（降序排列）；把这些不等式相加，后继 slots 的总 assigned 时间≤原机器 fractional load≤L。因此完整实际 C≤L+b。

当 OPT≥2b 时，L+b≤OPT+b≤(3/2)OPT。算法同时算出此调度及第4.1节所有成功调度，按实际回算负载取最小者，故无需知道 OPT 属于哪一段，也不调用 OPT oracle。

## 5. 确定性与总位复杂度

所有算术仅用输入有理数、至多两项小时间之和、与 b 或 b/2+a 的比较；候选 O(m)，网络规模按显式 P 多项式，整数最大流／匹配均多项式。无按处理时间数值、分母倒数或 b 的数值循环。

global fractional LP 是通常有限有理 LP，标准确定性位多项式算法可取精确有理可行最优点；排序铺槽及所有 overlap 也用有理精确比较。L+b 界不要求实际存在时间恰 b 的资格，b 只作为所有 finite 时间的上界。输入 b 与实际处理尺度相差极大时，精确 <b 分支仍覆盖小 OPT。

单机、仅一个 finite 端、没有 unit 资格、OPT=0、n=0、部分零 jobs、a=0 和 a 接近 b 都在以上分支中。没有使用任何随机、平均／期望、固定机器数或 fixed-precision 算法。

## 6. 三半困难性的独立 3DM 实际归约

### primary 源和读取边界

已亲视原始研究论文的现有未改写2010重印：

`/workspace/scratch/038d9dcc4cac/co-work-anl-boss11/history/source/literature/unrelated_machines/karp_1972_reprinted_2010_reducibility.pdf`

SHA256 `ae57cf641ae4f1924bdc4d7ef865edb2411c44e3040e8e546d01f1545e288e89`。其物理 PDF14／原印94页 Main Theorem 列明以下问题 complete；物理 PDF15／原印95页第17项定义 3-DIMENSIONAL MATCHING：给 U⊆T×T×T，问有无大小|T|且无坐标重复的子集。这里以三份 tagged copies X,Y,Z of T 形成 balanced perfect3DM，完全吻合。

本人实际读的是该原文重印的相关扫描页，不冒称重新证明 Karp 的 NP 完全性归约，也不声称这份重印是1972首次印行的原字节。非空域可由添加一枚只出现于新强制 triple 的 fresh 坐标同时增大三侧来确保，不影响 NP-hardness。

### 完整调度构造

给 |X|=|Y|=|Z|=q≥1、显式 triples E⊆X×Y×Z，令 b=1。若任一元素无 incident triple，源为 NO，输出合法常量 NO：一 machine、两 unit jobs，各唯一端时间1，OPT=2，small 行数0。无可用 triple 同样处理。

其余情况，对每 triple e=(x,y,z) 建 machine M_e，给它恰两条 small 资格：元素 job X_x 的时间1/2、元素 job Y_y 的时间1/2。另建该 triple 的 job J_e，合法端只有 M_e 和外部 machine Z_z，两处时间均1。每 z 建一 machine Z_z，除这些 unit jobs 外无资格。没有其它 jobs、端或 zero。

元素 jobs X_x、Y_y 因预检均有 finite 端；每 J_e 有两个 finite 端。M_e 每行恰两条 positive small，Z_z 每行零条。所有 finite 仅1/2或1，unit 资格数不限，某个 job可有多个small资格。机器、jobs与所有 finite/∞端的完整编码按源规模多项式。

### YES 与任意 C<3/2 的 source decoder

若有 perfect3DM，取其 q 枚 triples。选中每个 M_e 接其 X_x、Y_y 两 small，总负载1；其 J_e 放 Z_z，各 z 恰一枚unit。其它所有 J_e 留自己 M_e，负载1。全部 jobs 覆盖，C≤1。

反向取任意实际 C<3/2。每个 Z_z 至多接一 J_e，因此至多 q 个 triple jobs 离开自己的 M_e，称其 M_e 为 opened。未 opened 的 M_e 已有 J_e unit，不能再放任何1/2元素 job，否则负载达到3/2。全部2q元素 jobs 必到 opened machines；每 opened M_e 只可接自己的两枚 distinct 元素 jobs，容量最多2，所以 opened 数≥q。于是恰q个，且每个均接两枚元素 jobs；X、Y元素各恰一次。其 q 个 J_e 还分别在 q 个不同 Z_z，故第三坐标也各恰一次，opened triples构成 perfect3DM。

因此源 NO 保证任意实际 σ 的 C≥3/2。若存在任意固定 ρ<3/2 的确定性位多项式近似算法，YES 上输出<3/2，NO 上任何合法输出≥3/2，精确比较即可判定 perfect3DM，故推出 P=NP。下界真实针对实际σ，不是配置 LP gap。

## Status / Scope

Exact-first 独立一般证明完成；四项无 fatal；未读候选作者 proof；primary 3DM 域已按上述页实际核对。无生产实现、有限审计、新颖性或独立成文价值认证。每行第三条 small 或其它 finite>b 的扩展未审；一般 UM 正反面仍 OPEN。
