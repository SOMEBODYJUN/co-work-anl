---
id: "unrelated-machines/fractional-rematching-explicit-xos-v4-v5-increment-review"
kind: "mathematical-object"
type_tag: "审查"
title: "分数重匹配显式 XOS 的 v4–v5 增量与协作验证边界"
status: "reviewed-in-explicit-source-domain; implementation-unverified"
truth_status: "v4/v5 are statement-only contracts; later v5 author proof and independent mathematical review separately identified; no backend execution"
review_level: "Boss7 informed source comparison, not a new independent Exact-first review"
summary: "保全 v4 的数值 Q 收费格点 XOS 合同、v5 的残余精确归一化与固定候选相对格点替换，以及两份明确非独立的 coauthor 记录；核对五版 A 逐字相同，区分当时待审与后续 v5 Proof/PASS，并保留高低质量比例互补勘误。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/fractional_rematching_extension_statement_only_v4.md.gz#all"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/fractional_rematching_extension_statement_only_v5.md.gz#all"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/fractional_rematching_extension_v4_coauthor_validation_and_provenance.md#all"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/fractional_rematching_extension_v5_coauthor_validation_and_provenance.md#all"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/fractional_rematching_extension_author_proof_v5.md#all"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_nsw_v5_exact_first_attack.md#all"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_nsw_v5_author_read_after.md#all"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_nsw_v5_canonical_full_review.md#all"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/nsw_gamma_complement_correction_actual_read_after_review.md#all"
related_objects:
  - "unrelated-machines/fractional-rematching-normalized-xos-robust-gap"
  - "unrelated-machines/fractional-rematching-version-audit"
  - "unrelated-machines/weighted-bernoulli-shifted-inverse-moment-xos-log"
  - "unrelated-machines/finite-grid-label-mask-log-potential-derandomization"
evidence_manifest: "../../tools/evidence/Boss7-fractional-restored/manifest.json"
---

# 【数学审查】

## 1. 材料身份、实际阅读和本次结论

本对象完整读取四份冻结来源，按数学内容比较 v1–v3 statement、rank v3 异议、作者 Proof v5、后续 v5 Exact-first/Proof-read-after/canonical-review，以及高低组比例勘误。四份主源的压缩原件、解压正文、完整 v4/v5 差分和可复核字节记录见[证据目录](../../tools/evidence/Boss7-fractional-restored/README.md)。冻结提交 `68fad804ec5946cb296f77dc5b336308a66abf12` 与 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 的同路径字节合并为同一来源，不重复计为独立证据。

| clean ID | 主源角色 | 完整正文规模 | 本次去向 |
|---|---|---:|---|
| `93808197dd001b8ac118` | statement-only Exact v4；原件为 gzip | 解压 28,800 bytes，350 行 | 格点域、数值 Q 收费、确定性替换及归一化应用 |
| `b50f2d64238493b723a0` | statement-only Exact v5；原件为 gzip | 解压 31,269 bytes，383 行 | 任意显式二进制有理 XOS、精确残余归一化、候选局部格点 |
| `dc1a1b0e22af277523e9` | v4 coauthor validation/provenance | 8,494 bytes，64 行 | 合作者已知策略、所读工具、来源角色、位长及常数检查 |
| `8e013b1a8d17a54eba9a` | v5 coauthor normalization/local-grid freeze | 7,013 bytes，50 行 | 两个新替换的量纲、终止、位长、原价值支配及冻结身份 |

**四份主源自身的准确状态是：两份精确陈述、两份知情协作验证，没有在其中交付完整 NSW 作者证明或新的独立 Exact-first 审查。** 两份 coauthor 的“未发现 fatal”不能计为独立盲审票；它们事先接收 root 的算法提议及证明提纲，并读过工具证明和旧异议。本轮先读这些材料再进行比较，也不是重新开展盲审。

后续材料则确实另有 v5 作者全文证明和独立数学重构，不能因四源写着“待审”就忽略：作者 Proof v5 为 `0becaa69222f60a39778`，SHA-256 `2989351ca6ab45779fecb3c4a4ccefbae2044cdcce7ad3f3fab0d0e2ce55a1af`，71,631 bytes、1,052 行，本轮全文读取；独立 Exact-first、该作者证明的 read-after、最终 canonical 的 read-after 分别为 `ed33bb167491de41a491`、`04dae13e7eb821aeaa1e`、`f52fb32efeeba91da30a`，亦全文读取。三份记录可在[后续 v5 证据目录](../../tools/evidence/retired-nsw-v5-20261031/manifest.json)定位。它们对明示显式无权 XOS 域给出数学/总位复杂度 PASS；后两份是同一审者的后置读后审，不增加两张盲审票。没有 backend 可执行实现、执行测试或外部 referee/全球新颖性认证。

本次未发现四源在其明示域中的新致命反例。下文复述已有推导并显化版本差异；不将 coauthor 声明独立当作证明，也不以“没有代码”否定已经另立的数学证明。v4 当时无独立审查、无完整 v4 作者证明这一历史事实不被后续 v5 证明追溯改写。

## 2. 承重位置审查表

| 原文位置 | 所需依据与本次核对 | 准确裁定 |
|---|---|---|
| A2 | 对所有残余可行分数配置族的语义预算；不能改为仅整数分配 | 五版相同；A 不负责验证该全局前件或寻找 targets |
| v4 B1/B2/B5 | 系数为 1/Q 格点、每 clause 总量≤1；DP 和迭代按 Q 数值收费 | 只给该域的多项式，不是对任意二进制 Q 位多项式 |
| v5 B2 | 除以精确正数 W_i 后至少一 clause 总量一；固定 lift 基本顶点位长独立于当前目标 | 除法是有理表示，不按 1/W_i 展开；128a³ 次更新有显式势进展证明 |
| B3/B4 | 福利 rounding 保持某个原支持配置的子集；分裂后 inherited mass≥1 | 这是保持容量和每轮值上界所需条件，不能只引用数值福利比 |
| v5 B5 | 候选先固定；相对 floor 后总量≥δ_mask/12；正 shift；每 row 原物品标签独立 | 与独立逆矩工具和格点 DP 接口匹配；跨 agent 不要求独立 |
| B6 | 初始 τ 在全部 U 上真最大乘积；对每个比较 π 的路径重匹配；同一最终输出 | 后续作者证明/独立重构闭合，不使用未知 OPT 或 benchmark 作算法输入 |
| C/D/F | 原 clause 总量一、所有质量≤1、同一 n 组；严格阈值及 γ_lo−a_rep 的 slack | 低端定理和 F1 成立；与高端 NO 比较必须作集合互补 |
| E | 原 indexed states、selectors、所有正/显式零 incidence、未选状态作业均保留 | 只给全矩阵≤2 与所述 selected-root 计数，不给全机器统一 2−ε |

旧 rank v3 的异议仍约束旧一般次可加 backend：其 μ 代回漏因子三，任意 Bernoulli 参数不能无证套 reciprocal-sampling 引理，移位 f=v+ν 不满足所引 Theorem 20 的原 singleton 前件。v4/v5 选择显式 XOS 支持 clause、加性逆矩与确定性有限 DP，是更换证明路线；它们没有修正已经冻结的旧一般次可加陈述，也没有证明一般次可加 backend。

还有两项已核实的表述/适用问题，应与证明 fatal 区分：后续 Exact-first §6.2 把 `t^d≤1−d+dt` 称作 concavity/tangent，术语不准确；正确理由是固定 `0<t<1` 时 `d↦t^d` 凸且在 `[0,1]` 上位于端点弦线下方。作者 Proof §6.2 与 read-after 已正确表述，公式方向没有因此错误。后续旧 canonical §F 则出现实质的高低比例混用，须按第 8 节勘误；不能引用旧 PASS 覆盖该已撤回外推。

# 【修改建议】

1. 引用算法结论时同时注明版本与输入域。引用 v4 必须写“显式格点、按 Q 数值收费”；引用 v5 才能写“任意显式非负二进制有理 clause、按总位长收费”。不能只因两版最终数值相同就抹去输入域强化。
2. 用 `δ_mask=2/35` 表示固定标签参数，用 `δ_q` 表示可变质量阈值，用 `γ_lo`/`γ_hi` 区分低端下限和高端上限，用 `a_rep` 表示 repair 比例。它们不是一个参数。
3. v4 的全局 floor 是内部辅助 valuation；v5 的 floor 只作用于已经固定候选的相对 clause 权重。两者都不能代入原作业处理时间。v5 C 不再需要全菜单 floor 或 3/4 benchmark 损失。
4. 精确状态分三层记录：四源生成时仅陈述/协作核对；后来另立作者证明及独立数学审查；软件实现和执行审计仍不存在。不要把后置读后审计作另一张 independent Exact-first 票。
5. 使用 robust NO 前先逐字写出计数集合和严格符号，再作互补。后续旧 §F 的“γ≤δ 不覆盖”只能在 γ 确为低端比例时作条件比较；它不能用于同名高端比例。具体 source 是否满足 norm1、显式菜单、unit-FSLP 等全部前提仍需另审。

# 【论文版本】

## 3. 不变核心 A：一般次可加的分数 benchmark 重匹配

设 `n≥1`，U 有限，`H⊆U` 恰含 n 个不同原物品，`B=U\H`。每个 `v_i:2^U→Q_{≥0}` 有限、单调、次可加，且空集值零。给定非负有理 `V_i` 和 `c≥1`，令 `A={i:V_i>0}`，并要求 `i∉A` 时 `v_i(B)=0`。有限有理配置族 y 满足行和一、原物品列和至多一，正质量配置均有正值。令

\[
\mathcal B(y)=\exp\left(\frac1n\sum_{i,S}y_{i,S}\ln v_i(S)\right)>0.
\]

若对 A 在 B 上的**每个**可行分数配置族 z（行和一、列和至多一）均有

\[
\sum_{i\in A,T\subseteq B}z_{i,T}\frac{v_i(T)}{V_i}\le cn,
\tag{1}
\]

则存在双射 `π:[n]→H`，使

\[
\left(\prod_i[V_i+v_i(\{\pi(i)\})]\right)^{1/n}
\ge\frac{\mathcal B(y)}{c+1}.
\tag{2}
\]

式 (1) 不是算法要从 value queries 自动检验的性质。A 也不构造 V_i；这些须由后端另行保证。H 在 A 中不必是最优匹配的像；此额外最优性仅在 B 的最终重匹配使用。

证明依后续已交付推导：将每个与 H 相交的配置质量送到其中 singleton 值最大的真实物品。每列至多一；H-empty 配置只出现在 V_i>0 的行，因而可以运输补齐行列缺口且所有使用因子 `f_ih=V_i+v_i({h})` 都正。对耦合配置 `T=S∩B`、`k=|S∩H|`，次可加性给

\[
\frac{v_i(S)}{f_{ih}}\le
\begin{cases}
v_i(T)/V_i+k,&i\in A,\\
k,&i\notin A.
\end{cases}
\]

不活动行没有除以零的表达式。将 y 投影到 B 是式 (1) 真正允许的分数族，残余比值总和≤cn；H 的列容量使期望 k 总和≤n。总质量 n 上用对数 Jensen，得到总 log benchmark 至多双随机矩阵的 `Σq_ih ln f_ih+n ln(c+1)`。正边 Hall/Birkhoff 分解选出不劣于该平均的置换，即 (2)。原物品不复制；重复配置条目不成为新资源。

真最大乘积匹配有有限位实现。若每条正有理因子的分子分母≤`2^L`，n 条乘积的分子分母≤`2^{nL}`；不等乘积的 log 差至少 `G=2^{−2nL−1}`。把每条 edge log 用有理数逼近到 `G/(4n)`，有理最大权匹配便保留不同乘积的顺序。正有理数二进制缩放到 `[1,2)` 后，`z=(x−1)/(x+1)≤1/3` 的对数级数给所需多项式精度。不要求 exact transcendental comparison，也不计算一般无理 benchmark。零因子边删除；`A=∅`、`B=∅`、零 singleton、零 V_i 均由上述正性论证处理。

本次直接比较了 v1–v5 的完整 A 段：均为 **3,565 UTF-8 bytes**，SHA-256 均为 `1c1250fb4e62c641d2bdc1d688d967cc5334e999ad61862a2641c1e3bd0f4828`。这项字节核验只说明相同，不单独证明数学。

## 4. v4 到 v5 的全部实质差异

两版均用有限非负显式 XOS

\[
v_i(T)=\max_s\sum_{j\in T}p_{i,s,j},
\]

菜单非空且有索引，允许零系数、重复 clause、未使用物品及零总量 clause；目标始终为无权 NSW。两版均不依赖 benchmark y 或实际最优分配作为输入。

| 接口 | v4 | v5 |
|---|---|---|
| 原输入域 | `p∈(1/Q)Z_{≥0}`，每 clause 总和≤1 | 任意显式非负二进制有理 p；总量可不等、可超过一、可为零 |
| 复杂度 | poly(显式位长,n,m,Q 数值) | poly(总显式位长,n,m,clause 数) |
| 无正 singleton 覆盖匹配 | 报告无匹配；后续限正分支 | 返回全空；同时证明实际最优 NSW=0、无正分数 benchmark，包含 m=0 |
| 残余基线 | `b_i=v_i(B)/a`，格点使正值≥1/Q | 精确除以 `W_i=v_i(B)` 后 `b_i=1/a` |
| 坐标地板/步长 | `ℓ=1/(4Qa)`，`h=1/(32Q²a²)` | `ℓ=1/(4a)`，`h=1/(32a²)` |
| 更新次数 | 至多 `128Q³a³` | 至多 `128a³` |
| mask 权重 | 原格点支持 clause 权重 | 已固定候选上 `a_ij=floor(Qw_ij/V_i)/Q`，`Q=210\|B\|` |
| 势与 shift | `Σln[V_i/(ν_i+W_i(r))]` | `Σln[1/(β_i+A_i(r))]`，`β_i=ν_i/V_i` |
| 归一化 C 的路径 | 全菜单内部 `Q=4m` floor；同一支持 benchmark≥3/4 | 直接原 table，benchmark=1；只需 B 的局部辅助 floor |
| 下游数值 | B 至少 benchmark/1,125,000，放宽到/2,250,000；C≥1/3,000,000 | 相同保守陈述；C 的 3/4 损失已不再需要 |
| E 原作业约束 | 不用全局 floor 替代物理处理时间 | 不用 residual 归一化或局部辅助 floor 替代物理处理时间 |
| 历史状态 | 新协作陈述，未在该文件给完整 proof | 强化后的新协作陈述，等待另立审查；不追溯升级 v4 |

完整 315 行 unified diff 已保存。B3、B4 的支持内福利舍入及先固定候选的数学内容不变；B6 只调整编号和“同一原显式对象”的比较域；C1/C3/C4、D 的 repair 组合条件、E 的作业/机器计数、F1 的低端量词均保留。其余 header、B7、F 的改动明确新域、来源与排除项，不能当作额外定理。

v4 的全菜单 floor 满足每个原 normalized clause 总量≥3/4，且辅助价值不超过原价值。因此 reserve 后的 `((3/4)/2,250,000)=1/3,000,000` 有依据。v5 C 直接用原 table，仍保守写 1/3,000,000，不意味着算法还执行已取消的全局 floor。

## 5. v5 残余归一化为何消除数值尺度收费

先在全部原物品 U 上求真最大乘积正 singleton 匹配 τ，令 `H=τ([n])`、`B=U\H`、`A={i:v_i(B)>0}`、`a=|A|`。A 为空则所有 targets 为零，不运行求解器。否则对活动行作精确有理归一化

\[
W_i=v_i(B)>0,\qquad \widehat p_{i,s,j}=p_{i,s,j}/W_i.
\]

每条 residual clause 总量≤1，每行至少一条总量恰一。二进制有理除法只增加表示位长，不产生与 `1/W_i` 数值相等的循环或副本。固定 lift 为

\[
\lambda_{i,s}\ge0,\quad\sum_s\lambda_{i,s}=1,\quad
0\le z_{i,s,j}\le\lambda_{i,s},\quad
\sum_{i\in A,s}z_{i,s,j}\le1.
\tag{3}
\]

其归一化 utility 像为

\[
R=\left\{u:\ u_i=\sum_{s,j\in B}\widehat p_{i,s,j}z_{i,s,j},\ (\lambda,z)\text{ 满足 (3)}\right\}\subseteq[0,1]^a.
\]

R 包含**每个** residual 分数配置族的实际期望 utility：给每份配置选 attaining clause，按 clause 聚合概率和物品边际即可。反向，将 `z/λ` 按边际排序，用至多 `|B|+1` 个嵌套阈值集合恢复每条正 λ 的分布；其指定 clause 期望等于 lift utility，实际 XOS 期望只会更大。这一不等号方向不能反写成相等。

取 `b_i=1/a`、`R′=b/4+3R/4`、`ℓ=1/(4a)`、`h=ℓ²/2`。基线 b 的 lift 用每行一条总量一 clause、每项边际 1/a 构造。每轮在固定 (3) 上求基本最优点 w，使 `M=max_{w∈R}Σw_i/x_i`。若 `M≤2a` 则停；否则按 `x←(1−h)x+h(b/4+3w/4)` 更新完整 lift。

算法只用有理运算。分析势 `F(x)=Σln x_i` 不实际计算；`M>2a` 时梯度内积大于 a/2，整段坐标≥ℓ、平方方向和≤a，故每次 `ΔF>ℓ²a/8=1/(128a)`。起点 `−a ln a`、上界零，a≥2 时更新少于 `128a² ln a<128a³`；a=1 时起点即停。v4 同理用格点下界，得到其含 Q 的保守次数。

位长理由是固定 (3) 的矩阵只有 `0,±1`、右端 `0,1`。基本顶点的 Cramer/Hadamard 位界只依显式维数，不依当轮目标 `1/x`；多次更新共同分母的位数按轮数相加。不能用“LP 总是多项式”略过一个目标位长递归，但本构造已给出固定顶点界。

恢复配置后取实际 `\widehat V_i≥x_i≥1/(4a)`、`V_i=W_i\widehat V_i`。任意可行分数族 z 的实际归一化 utility `u^z∈R`，因此

\[
\sum_{i,T}z_{i,T}\frac{v_i(T)}{V_i}
=\sum_i\frac{u_i^z}{\widehat V_i}
\le\sum_i\frac{u_i^z}{x_i}\le M\le2a\le2n.
\tag{4}
\]

故 A 的 c=2 前件真正量化到全部 residual 分数族，既非仅输出 witness，也非仅整数分配。

## 6. 固定候选、局部相对格点与误差预算

令 `ν_i=max_{j∈B}v_i({j})`，空集最大值为零；只对 `A″={i∈A:V_i≥6ν_i}` 生成 residual 候选，其余 `T_i=∅`。活动 XOS 行 ν_i>0。原配置 T 的 attaining clause 权重均≤ν_i；丢掉 `v_i(T)<V_i/3` 的配置，其余取 `k=floor(3v_i(T)/V_i)` 个不交 parts，经贪心提取与删项使每份实际值在 `[V_i/3−ν_i,V_i]`。`k≤|T|/2` 排除按 tiny utility 展开。

继承原配置质量的总量 `M_i≥(3/(2V_i))·(2V_i/3)≥1`；每原项从同一配置至多继承一次，再除以 `M_i≥1` 不会放大列容量。得到可行 x′，实际期望 `V_i/6≤V′_i≤V_i`。

福利舍入先独立选各 agent 的有限支持配置，并用 attaining-clause bid `p_ij/U_i`。每物品超过任意正阈值的概率和≤1，跨 agent 独立使最大 bid 的期望至少总 bid 期望的一半。按有限 bid 层级的严格 CDF 乘积，以精确有理条件期望依次固定配置，再给正最大 bid 的 claimant。实际 bundle 是其选定原支持配置的子集，归一化总福利≥当前人数/2。

以保守 `d=5/2`、`δ_mask=1/(7d)=2/35` 逐轮留下满足 `v_i(S_i)≥δ_mask V′_i` 的 agents。支持内性质给归一化值≤6，故每轮至少 `ceil(δ_mask·当前人数)` 人离开，最多 `L=|A″|` 轮。**所有 S_i、round t_i、attaining clauses 都先于标签固定。** 同轮 S_i 不交；不同轮可重叠。

每个原 residual 物品用一个全局独立标签，概率

\[
\Pr(r_j=t)=\delta_{\rm mask}(1-\delta_{\rm mask})^{t-1}
\ (1\le t\le L),\qquad
\Pr(r_j=0)=(1-\delta_{\rm mask})^L.
\]

这只是去随机分析分布，最终算法不抽随机位。v5 对固定候选的 attaining weights w_ij 取

\[
Q=210|B|,\quad a_{ij}=\frac1Q\left\lfloor\frac{Qw_{ij}}{V_i}\right\rfloor,
\quad\beta_i=\nu_i/V_i>0.
\tag{5}
\]

候选原 relative total≥δ_mask/6，floor 总损失≤`|B|/Q=1/210=δ_mask/12`，从而

\[
\delta_{\rm mask}/12\le\sum_j a_{ij}\le1,
\qquad0\le a_{ij}\le\beta_i.
\tag{6}
\]

仅这些辅助权重进入 DP；原 clause、原 V、原分配和处理时间都不改。

所用逆矩为：`β>0`、`0≤a_j≤β`、独立 Bernoulli X_j、`M=Σa_jPr(X_j=1)>0` 时，

\[
\mathbb E\ln\frac1{\beta+\sum a_jX_j}\le\ln\frac1M.
\tag{7}
\]

令 `d_j=a_j/β∈[0,1]`，用凸弦 `t^{d_j}≤1−d_j+d_jt`、独立乘积及积分 `1/(1+Y)=∫_0^1t^Ydt` 得 `E[1/(β+ΣaX)]≤(1−e^{−M/β})/M<1/M`，再用 log Jensen。式 (7) 对单候选中的原物品独立性成立，不需跨 agents 独立；不能推广相关 mask 或一般次可加价值。

mask 势为 `Φ(r)=Σ_{i∈A″}−ln(β_i+A_i(r))`，其中 `A_i(r)=Σ_j a_ij 1[r_j=t_i]`。每行 `Qa_ij` 总量≤Q，故准确有理卷积 DP 只需整数状态 `0,…,Q`。若一项概率为 P/D，共同分母递推 `N′_k=(D−P)N_k+PN_{k−h}`；位长随真实概率分母位数相加，不按倒数数值展开。

取每个 log 表值绝对误差 `1/(2|A″||B|)`，每个 label child 的总势误差≤`1/(2|B|)`。近似最小 child 每步真实误差≤`1/|B|`，全部原物品累计≤1，得到 `Φ(r)≤EΦ+1`。tiny β 只增加 log argument 位数，不增 DP 状态数。空活动集、空 A″ 直接跳过，避免除以零规模。

按离开顺序 k，目标标签概率至少 `δ_mask(|A″|−k+1)/|A″|`。结合 (6)–(7)、阶乘下界及总势误差一，得

\[
\left(\prod_{i\in A″}\frac1{\beta_i+A_i(r)}\right)^{1/|A″|}
\le\frac{12e^{1+1/|A″|}}{\delta_{\rm mask}^2}
<\frac{200}{\delta_{\rm mask}^2}<10000d^2.
\tag{8}
\]

`T_i={j∈S_i:r_j=t_i}` 在所有 agents 间不交：同一原物品只有一个标签，同轮候选又不交。原 clause 给 `v_i(T_i)/V_i≥A_i(r)`，因此式 (8)控制原单位的 `GM[V_i/(ν_i+v_i(T_i))]`。v4 没有 relative floor，平均势上界的 12 对应为 6；两版都放宽到同一 200。全链的误差一已实际支付，不藏入后面的 factor-two reserve。

## 7. 任意比较重匹配、normalized 后果及所有原作业

初始 τ 在全部 U 上真最优是承重前件。对 H 上任意比较双射 π 和非负 W_i，后续证明用 `τ^{-1}∘π` 的有向路径/循环分解，得到一个 H 上双射 ρ 满足

\[
\prod_i\max\{W_i,v_i(\rho(i))\}
\ge\prod_i\max\{W_i,v_i(\pi(i)),\nu_i\}.
\tag{9}
\]

将需要 ν 的每个顶点出边切开，含多个此类顶点的环也变成终止于这些顶点的路径。每条路径分别构造用一个 B 中最大 singleton 替换终点的反事实全 U 匹配，τ 的最优性给该路径的乘积界；不同路径的反事实可能用同一 B 物品，但不是同时进行的实际分配。补全 H 中的余项无冲突。零右乘积直接用正 τ 处理。

取 `W_i=v_i(T_i)`，最后对原值 `v_i(T_i∪{h})` 在 H 上求真最大乘积 σ。其正性由 τ 仍可用保证，输出原 bundle 全局不交。对 A″ 行使用式 (8)和 ratio≤`2V_i/(v_i(T_i)+ν_i)`；对 `A\A″` 使用 `V_i<6ν_i`；不活动行正比较时 ratio=1。式 (9)的 max-to-sum 损失三得到

\[
\operatorname{NSW}_{\rm out}\ge\frac1{60000d^2}
\left(\prod_i[V_i+v_i(\pi(i))]\right)^{1/n}.
\tag{10}
\]

这是一个确定性输出对**每个** π 同时成立的分析。结合 (2)、(4)的 c=2、d=5/2，对每个同一原对象的正有限分数 benchmark y 有

\[
\operatorname{NSW}_{\rm out}\ge\mathcal B_v(y)/1125000
\ge\mathcal B_v(y)/2250000.
\tag{11}
\]

该输出不依赖 y；后一个不等式是显式放宽，无抽样成功事件。关键常数精确为 `200/δ_mask²=61,250=9,800d²<62,500=10,000d²`、`60,000·3·d²=1,125,000`。

现在另加 C 的原 normalized 条件：每 indexed state 的原 clause 总量恰一，n≥1、m≥1。令正支持 `P_gs={u:p_gsu>0}`；unit-FSLP 的行和一、列约束使用 **正支持指标** `Σ_{g,s:u∈P_gs}λ_gs≤1`。若可行，每份正支持实际值恰一，故给 benchmark 一；所有原价值≤1，使 log-CONFIG 的 item-inequality optimum 为零。逐项将未含该物品的配置质量填入列缺口，可得 item-equality 的零值 witness，行和、其他列不变；这是分数 witness，不是整数 unit 分配，也不是一般指数 LP 求解器。

v5 直接对原 table 用 (11)，安全写出

\[
\operatorname{NSW}_v\ge1/3000000>\rho^{-1},\quad\rho=2^{24}.
\]

对任意固定有理 `0<η<1`，`K=ceil(1/η)`、`q_η=ρ^{-K}`、`c_η=q_η/2`，同一输出满足

\[
\#\{g:r_g<q_\eta\}<\eta n,\qquad
\#\{g:r_g\le c_\eta\}<\eta n.
\tag{12}
\]

证明是若 k≥ηn 项低于 q，其余≤1，则总乘积小于 `ρ^{−Kk}≤ρ^{−n}`，与严格 NSW 下界矛盾。≤c 严格包含在 <q 中，涵盖等号阈值；ηn 不必为整数。可变 η 时阈值本身需 O(K) bits，复杂度只承诺 poly(K,input)，不承诺 poly(log(1/η))。

指定 REPAIR 仅增加 D 个全局共享 singleton 资源和每组 D 个替代 state，不加 agents。原来至少 n−D 组达 unit 时，用不同 repairs 补全；任意增强分配删掉 repairs 后回到原分配，至多 D 组获救。因此固定 `0≤a_rep<γ_lo≤1`、`D≤a_rep n`、`0<η<γ_lo−a_rep`、`0≤δ_q≤c_η` 时，YES（原有 n−D 个 unit）与 NO（每个原分配至少 γ_lo n 个≤δ_q）由增强 unit-FSLP 可行/不可行分离。算法只测显式有理 LP，其 soundness 使用上述存在性定理；不必运行 NSW finder。没有断言存在相应 NP-hard source reduction。

原 ordinary flat-UM 矩阵保持每个 indexed state 的不同 private root、每资源一 machine、每组一单位 selector、每个正/显式零 incidence 的独立 job。为输出 Z_g 用原 table 重取 attaining state s_g：selector 在该 root；仅其分配正资源的 incidence jobs 外移到原 resource；该状态其他 incidence 及所有未选状态 incidence 留各自原 root，包括 time-zero jobs。所有原身份恰执行一次。若原质量 r_g，选中 root 负载 `2−r_g`，未选 root 为一，resource≤一。因此全矩阵 makespan≤2；仅 selected roots 中超过 `2−q_η` 的数量<ηn。全 unit 时同一完整调度 makespan 一，selector 给 OPT≥1，故 OPT=1。

若 S 为原 state 数、I 为全部显式 incidence 数，矩阵有 S+m machines、n+I jobs。repair 精确增加 nD roots、D resource machines、nD 正 singleton incidences 和 nD selector endpoints；selector 身份仍 n 个。如额外显式列出 Z_new 个零 incidences，总 job 增量为 `nD+Z_new`，这些同样保留。所有计数后果始终以同一 n 原组为分母。

## 8. 后续实质勘误：γ_hi 和 γ_lo 不能同名代换

四源 F1 的低端命题为：若每个 actual allocation 至少 γ_lo n 组质量≤δ_q，且 `0<δ_q<1`，则 NSW 正下界给必要式

\[
\gamma_{\rm lo}\ln(1/\delta_q)\le\ln\rho.
\tag{13}
\]

这本身正确，并不排除所有正参数对。然而后续旧 canonical 与其最终审查曾将某高端 NO 的 γ_hi 当成这里 γ_lo，并据 `γ_hi≤δ_q` 宣称“不覆盖”。[实际勘误来源](../../tools/evidence/retired-nsw-flat-followup-20261031/nsw_gamma_complement_correction_actual_read_after_review.md)（`2635332457d793f7982c`，SHA-256 `fc0f0432c6a676f73696ac1aa845c323592bbda34068fa32452e0bc5da892644`）明确撤回这一实质错误；本轮全文核对该来源以及[现有勘误对象](NSW比例勘误与flat菜单证明读后--审查.md)。它不是四源原来已经包含的发现。

准确互补如下：

| 高端 NO | 等价低端条件 |
|---|---|
| `#{r≥δ_q}<γ_hi n` | `#{r<δ_q}>(1−γ_hi)n` |
| `#{r≥δ_q}≤γ_hi n` | `#{r<δ_q}≥(1−γ_hi)n` |
| `#{r>δ_q}<γ_hi n` | `#{r≤δ_q}>(1−γ_hi)n` |
| `#{r>δ_q}≤γ_hi n` | `#{r≤δ_q}≥(1−γ_hi)n` |

由 (12)第一项，若 `δ_q≤q_η` 且 `γ_hi≤1−η`，输出有 `#{r≥δ_q}>(1−η)n≥γ_hi n`，反驳第一行高端 NO。两个等号可以同时成立，不需额外 strict slack。因此例如 η=1/2、`0<δ_q≤2^{−48}`、`0≤γ_hi≤δ_q` 的小常数域确实被排除。不能沿用“不覆盖所有 γ≤δ_q regime”的旧外推。

若高端集合改为 `r>δ_q`，仅引用 (12)第一项时需 `δ_q<q_η` 才能直接包含低端≤δ_q。另由严格 NSW 下界可加强得 `#{r≤q_η}<ηn`，但应另给乘积证明，不能假装原文 `<q_η` 已写成 `≤q_η`。此勘误不反驳 A/B、原低端 C/D、完整 jobs 的 E；也不自动构造 source reduction，或证明任何具体 source 的 normalization、显式性、unit-FSLP、同组身份全都保持。

## 9. 证据时序、归档关系与接续

| 材料 | 知识/时序边界 | 可支持的证据 |
|---|---|---|
| v4 coauthor | 事先收到 root 策略；读 v3/rank v3 和两个工具的 Exact、独审、Proof、read-after | 当时的协作一致性、来源披露；非独立审查、非完整 NSW Proof |
| v5 coauthor | 事先收到 normalization/local-floor 提议；沿用已知 v4/tool 阅读 | 两个新替换的协作核验；非独立审查、非完整 NSW Proof |
| 后续 v5 Exact-first | 先全文读精确 v5，仅另读指定 primary 范围；在作者 Proof 前冻结 | 独立重构数学链；其自身完整记录保留，不混入后见材料 |
| 后续作者 Proof v5 | 读 Exact、已冻结 Exact-first 与两个工具 Proof 后写作 | 知情作者重构的完整推导，不是新盲审 |
| Proof/canonical read-after | 同一 Exact-first 审者在解封后另立记录 | 后置一致性检查；旧 canonical §F 外推后来被勘误撤回 |
| 本轮 Boss7 | 先读四源及相关对象，再读 Proof、后续审查和纠错 | 清洗、版本比较和知情数学核对；不新增独立盲审票 |

本对象对已有[版本审查](分数重匹配版本审查--审查.md)和[核心对象](../定理/分数重匹配与归一化XOS稳健缺口边界--定理.md)增加的是 v4/v5 的原精确域、数值收费变化、两份 coauthor 的知识先验及后续状态定位，不新建第二个 NSW 算法身份。旧对象中“backend 尚待独立 read-after”的描述属于其七源阅读边界；本批实际找到的后续 v5 数学审查应单独引用，不能把没有执行实现等同于没有数学证明。

与[加权 Bernoulli 移位逆矩](../定理/加权Bernoulli移位逆矩与XOS对数期望--定理.md)的关系是满足权重上界和行内独立性的局部引理依赖；它本身不证明全 backend。与[有限格点标签势去随机](../证明/有限格点标签掩码对数势去随机--证明.md)的关系是表示保持的工具调用：v4 按 Q 数值收费，v5 用 `Q=210|B|` 才转为总输入位多项式，且同标签候选不交另有 B4 保证。与[比例勘误](NSW比例勘误与flat菜单证明读后--审查.md)是对旧后续应用外推的反驳/修订关系，不是对 A/B 的反例。以上是逐条数学关系判断，阶段三再建立对应超边；此处不复制旧图。

接续时可使用明示域内的数学证明/审查合同；若要交付软件，仍须另行实现固定 lift、精确匹配、CDF、DP/log 误差和所有零分支并执行验证。任何一般次可加 backend、weighted NSW、非显式 oracle 输入、其他 dummy/SC、一般 UM 近二结论、all-group max-min、source hardness 或六人 SPE 结论均不由本批产生。

本次四条 receipt 只作为**本地待父 Boss 推送并提交**的完整语义记录保存；没有执行 clean done，也不称远端清洗完成。
