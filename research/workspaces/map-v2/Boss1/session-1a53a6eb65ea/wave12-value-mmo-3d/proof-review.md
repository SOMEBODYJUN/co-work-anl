# VALUE-MMO2：两组独立 3D 数学复核

审读身份：Boss1，fresh 独立子审读 `wave12_value_mmo_3d`。共享 clone `/workspace/scratch/1a53a6eb65ea/co-work-anl-boss1` 全程只读；本次没有 Git、native work/队列命令、共享写入、凭据访问、认领、spawn 或科研计算重跑。文件 SHA 与 JSON pins 仅作精确身份核对。

结论：两个最近 done 包各自的整个 core coverage 均可采用。Svensson 包必须按 **accepted / conditional / whole** 消费；MMO 包按 **accepted / unconditional / whole** 消费。没有发现需要修改当前两个 canonical 文件的数学问题。两组没有共同的承重数学问题，本复核不在它们之间造关系。

## 本次范围及精确身份

本次完整实读仓库 `AGENTS.md`、`research/IMPLEMENTATION.md`、`prompts/03-map-worker.md`；两最近包的当前 definition 与 receipt；四指定端点的全部登记字段；两个现役 canonical JSON；两份当前资源正文全文；MMO 本包 `partition-path-transfer-review.md` 全文。另读取当前 registry 的相关 canonical 条目、integration 的相关 pins、两个 core 的 coverage，以及 canonical owner 的相关任务/替代资产元数据。

本次对冻结 Svensson PDF 只定向实读印页 **1–4、11、20**，并渲染目视印页 **11**；对冻结 Asahiro PDF 只定向实读印页 **1–3、12–15**，并渲染目视印页 **14–15**。Svensson 其余局部搜索证明复用当前全文资源和 e562 receipt 的成熟全 22 页审读；Asahiro 其余内容复用当前全文资源及本包成熟全 21 页审读记录。原作者报告的全 PDF 阅读数量没有计作本次新阅读。两份 PDF 的外引参考文献均未因此成为本次独立付清的证明。

| 最近 done 包 | 核心与只读端 | 当前 definition pin | 当前 receipt 原始字节 SHA-256 |
| --- | --- | --- | --- |
| `unrelated-machines-3a-3a-e5622a5b3226206f` | `M-28ae04c28f0e43369c5ec1bb68e63bf2` v2；`M-6e6de497c2034ca99d68b4ff3d548a0d` v2 | `61f01a49844cb34448a90baebb297c52cf2b95a80ab1f70f97f1bbb533fade2e` | `bd5aeb6d89d3430f7507e05fc8b1dc5ef88ddd479d690c74603ca0bd624a6869` |
| `unrelated-machines-3a-3a-eba225f7871d217b` | `M-dcc092193be04e8b9b143a1ed5ba1d4d` v4；`M-91ba949b418b4026aa3c2dc2e5a62834` v4 | `59a0446fd4d190533c4e5a379f2deca39dd830d8d6f382915ce4e01277c5e0aa` | `8ef59fe8d33758ba7e7b1a38f222f46520391a935fca60b14d58f70b0fba9201` |

两最近包的本地当前状态均为 `done`、owner `Boss2`；独立 receipt 与任务嵌入 receipt 逐结构相同。四端的完整合同、版本、registration pins、全部文件 SHA、两边 native edge pins 和两个 receipt pins 见 `refs.json`。JSON pin 使用仓库 `pin` 的纯散列定义重算，未调用 native 命令；重算结果与 definition 的输入 pins、edge endpoint pins 和 integration 中相应 pins 全部匹配。两个 receipt 的每个资产也均按当前原始字节核 SHA 成功。

## 第一组：配置 LP 间隙到多项式数值估计

现役 canonical 是：

`map/edges/unrelated-machines-3a-3a-46f9088da65c727f/gap-and-approximate-threshold-yield-estimation.json`

edge ID `um-46f9088d-gap-and-approximate-threshold-yield-estimation`，SHA-256 `6c73a9bbe9ec6ff01bbe1891a836a0dce99cb70e9b2f94f012bcf9f817fe4210`；当前 registry 确列此路径。canonical 原任务 `unrelated-machines-3a-3a-46f9088da65c727f` 为 done、owner Boss2，最近 e562 包按原字节复用它。

源模型是有限公共尺寸受限指派：每个作业有同一非负有理尺寸 `p_j`，机器仅通过资格集 `Γ(j)` 区别。它不是一般有限 `p_ij`。每作业资格集非空时，最优调度存在且最优值有限。配置族向下封闭，整数调度在每机器对应配置上放一个单位权，给

\[
T_{\rm conf}\le\mathrm{OPT}.
\]

源 v2 间隙合同和 PDF Theorem 4.1 给

\[
\mathrm{OPT}\le \frac{33}{17}T_{\rm conf}.
\]

本次 PDF 印页 11 确认定理与 `R=16/17`、每机器至多一件 big 的额外不变量；当前资源保存了 Claim 4.7 的对偶可行性、Claim 4.8 的相邻配对摊还及 Lemma 4.9 的有限终止证明。此处复用成熟源定理，不声称本次重新逐页重证全部一般尺寸局部搜索。

边的额外后端合同是实质前提：对每固定有理 `ε>0`，在有理输入位长的多项式时间返回一个有理数 `T̂`，满足

\[
T_{\rm conf}\le\widehat T\le(1+\varepsilon)T_{\rm conf}.
\]

给每固定 `η>0`，取固定有理 `0<ε≤17η/33`，输出

\[
E=\frac{33}{17}\widehat T.
\]

逐向检查得到

\[
\mathrm{OPT}\le\frac{33}{17}T_{\rm conf}\le E
\le\frac{33}{17}(1+\varepsilon)T_{\rm conf}
\le\left(\frac{33}{17}+\eta\right)\mathrm{OPT}.
\]

第一条输出不等式用到 `T̂≥T_conf`，最后一条同时用到 `T_conf≤OPT` 和 `ε≤17η/33`。近似误差方向不能省略。固定精度后端输出长度受其运行时间控制，再做一次固定有理乘法，足付整个数值算法的位时间。这里只声称每固定 η 的算法族，未声称对输入中的 η 或 `1/η` 统一多项式。

空任务及可行全零尺寸实例先返回 0；有作业没有合法端时先报告不可行，不套有限 OPT 乘法保证。对正最优值再使用归一化与相对误差，因此没有除零缺口。

本次实读 PDF 印页 2–4 和 11：作者确把近似配置 LP 求解/二分外引到 Bansal–Sviridenko，印页 4 的逐机器背包描述和“尺寸舍入”并未独立付清所需后端。现有边把上述双侧后端及其多项式复杂度明确保留为条件，这是准确的。不能仅根据有限签名或“可近似求 LP”一句去掉条件。本次未补该外引算法。

本次实读印页 20 确认：至多 `3|M|` blocker、每项有限取值与字典序下降只给有限终止，没有签名总数量的多项式上界。`E` 是真实 OPT 的数值估计；它虽是某个可行调度的存在上界，算法却不输出 assignment。不能由此升级成多项式 `33/17` 实际调度。

- **whole：成立。** 在所列后端条件下，目标每固定 η 的完整数值估值合同已经得到。
- **contribution：无需降级。** 这不是仅仅“间隙有助估值”的局部贡献；全部条件到完整输出不等式的论证已闭合。
- **remaining：** 对本 conditional whole 没有缺步。若要求当前证据中独立无条件重导估值，须另支付固定精度配置阈值后端的精确输出方向、求解/二分/舍入及位复杂度；实际调度的多项式构造是另一义务。
- **整个 core coverage：可采用。** 必须同时保留 accepted/conditional、公共尺寸域、固定精度及数值输出边界。登记核心的 proved 文献身份不把本条关系自动升级为 unconditional。

## 第二组：平行 MMO 到简单系列并行 MMO

现役 canonical 是：

`map/edges/boss5-asahiro-sha-current-repair-16bd7e5e49c5be05/parallel-mmo-to-simple-series-parallel-mmo.json`

edge ID `um-35169397-parallel-mmo-to-simple-series-parallel-mmo`，SHA-256 `7bbf1422afaaf991a1849fab6e543f64eca868d759148d92b3941ea61b0ec4fa`；当前 registry 确列此路径。它的现行 repair 任务 `boss5-asahiro-sha-current-repair-16bd7e5e49c5be05` 是 done、**owner Boss1**，边的 reviewed_by 也是 Boss1。最近 eba225 包 owner Boss2 复用的正是此路径和此 SHA，复用收据有效。

历史被替代的是 Boss5 原包 `unrelated-machines-3a-3a-35169397311361c0` 下的同名边，旧 SHA 为 `8b5812e7d5ba76a7e6eef4f8784f51dd3ac5969307b18976ca13ce0e5e2737a9`。repair 收据将该历史路径标为 replaced，并指向上述 `7bbf1422...` 现行路径。**本次没有发现现行 `7bbf1422...` 文件再次被替代或 eba225 收据失效。**

MMO 在本组中按每条边同一正整数权计入尾端，无节点初载。源 v4 合同提供两个点 `s,t` 间的独立平行正整数权边，权为 `w_i`，总和 `2B`。对每条边选尾端就是选半分子集；两端负载和固定为 `2B`，两端各不超过 B 当且仅当都等于 B。平行边必须逐条保留。源图允许平行边，确为多重外平面族。本次印页 13–14 和 Fig.4 对应上述源困难性。

对每条源边建独立路径 `s-u_i-v_i-t`，权依次为 `(w_i,B,w_i)`，其中 `B>0`，全部内点仅属于该路径。这条桥已经在当前 edge explanation 自足证明，不存在必须额外造一个桥节点才能使 ALL 成立的要求。真正使用的联合前提是源困难性以及此双向桥、图类与编码核验；当前 `source_ids` 只有源 M-91，桥留在关系证明中是充分的。

前向若源在 B 可行，每个 `w_i≤B` 自动成立。沿源边方向取向整条路径，端点负载逐点保持；两个内点分别付 B 和 `w_i`，均不超 B。

反向不假设整路同向。若中边 `u_i→v_i`，u_i 已付 B，正的外边权迫使 `s→u_i`；解码原边为 `s→t`。若中边反向，则同理迫使 `t→v_i`，解码原边为 `t→s`。每条原边只选择一个尾端，其费用已经出现在对应 H_B 端点负载中。另一外边可能也从另一端点指出，但解码丢弃该额外费用，故源两端各自负载只会降低。由总权 `2B` 再推出源两端恰为 B。此证明还直接给任意正阈值 B 下两点实例与 H_B 的同阈值 YES/NO 等价。本次印页 15/Fig.5 的实际权值和两向论证与之相符。

此桥使用外边严格正权作强制，中边 B 也必须符合正整数权模型。合法非空偶和输入给 `B>0`。奇和输出固定简单 NO（权 2 的单边，阈值 1）；非法/非正编码按源语言给固定 NO；空表若属源语言则输出固定 YES（权 1 单边、阈值 1），否则固定 NO。B=0 的空输入不进入路径公式，因此不引入零权中边。大于 B 的元素无需排除：它同时使源及替换图不可行。

输出恰有 `2n+2` 点、`3n` 边，无自环或重边。各路径先串联，再在 s,t 间并联，给简单二端点系列并行构造。显式树分解以 `{s,t}` 为根，每路挂 `{s,t,u_i}` 再挂 `{t,u_i,v_i}`：每条边有袋覆盖，所有顶点出现袋连通，最大袋大小 3，故 width≤2；复制根袋可二叉化，仍 O(n) 袋。求 B、复制两次元素权并写 n 次 B 都是二进制位长多项式，未按权值展开单位边。

当 n≥3，取三路并分别收缩中边即得 K2,3 minor，因此不能把结论改成简单 outerplanar 困难性。H_B 的权依 B 构造，只保此同一阈值的可行性；例如一条源边权 1、B=3 时，源最优为 1，而 H_B 最优为 3，所以也没有固定图全最优值保留。

弱标签使用当前正文 §3 已支付的安全 DP。对给定宽 τ、O(N+M) 袋的二叉分解，简单图单坐标负载≤k(N−1)，状态数≤`(kN+1)^(τ+1)`。显式枚举两个子状态和本袋边方向，父袋共享负载相加；父袋外顶点不能跨两个子树而不出现在父袋，故旧子表最大值已支付全部被遗忘顶点，合并双向精确。安全界是

\[
O\!\left(2^{O(\tau^2)}(kN+1)^{2\tau+2}(N+M)\right)
\]

次整数算术/比较，另付 `O(log(kM+1))` 位长的整数操作费用；τ≤2 时给安全的六次幂伪多项式界。构造族已显式给出分解。其对数值 k 的依赖与对二进制位长的依赖不能混淆。源多重图不能沿用简单图 N−1 度界；两点族也可用子集和 DP 支付伪多项式性。

本次印页 12–13 确认原文两子向量最小化公式及其直接按单表大小计时的跳步。当前安全 DP 显式支付配对，足够支持本次弱标签；原印 Theorem 10 快速指数不作为前提。NP 困难性的归约与此伪多项式上界是分别支付的；没有因源叫弱 NP-hard 就直接宣称目标不会强 NP-hard。

- **whole：成立。** 两点半和困难族经三边路同阈值双向迁移、合法简单系列并行输出及位长核验，加安全伪多项式算法，完整支持目标弱 NP 困难性。
- **contribution：无需降级。** 不是仅有某一路强制方向的局部观察；源到目标的归约合同已经闭合。
- **remaining：** 本核心目标没有未付步骤。更快 join、简单外平面复杂度、任意异端点权或机器相关时间、固定图全最优值保留均未由此得到，亦非当前核心剩余证明。
- **整个 core coverage：可采用。** 保留当前 accepted/transfers/unconditional/ALL/whole、正整数权、同阈值及 multi/simple 边界；沿现行 Boss1 repair 路径按精确 SHA 共享复用。

## 冻结决定

两最近包均已有可采用的完整核心比较，没有新边、新节点或本复核必须另派的数学缺口。e562 的后端条件保持开放前提但不损害已完成条件蕴含；eba225 的核心归约没有条件欠款。两包没有 formal follow-up 对象对，当前空 `closed_overlaps` 与 `follow_up_tasks` 不掩盖本范围未处理的指定比较。

`refs.json` 记录本地读取快照的精确 definition/receipt/asset SHA、原生等价 pins、canonical 当前有效 owner、historical replacement、四端完整合同及本次真实阅读范围。owner/state 仅是本次本地共享 clone 快照所见；本复核没有查询实时远端或宣称重新完成发布检查。证据身份与数学结论在上述范围内闭合。
