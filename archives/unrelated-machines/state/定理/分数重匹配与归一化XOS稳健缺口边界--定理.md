---
id: "unrelated-machines/fractional-rematching-normalized-xos-robust-gap"
kind: "mathematical-object"
type_tag: "定理"
title: "分数重匹配、归一化 XOS 与稳健小质量缺口"
status: "standalone-core-proved; backend-conditional"
summary: "独立分数 benchmark 重匹配引理及其在显式归一化 XOS/unit-FSLP 中的条件后果。A 的匹配结论和有限位最大乘积算法有完整证明与两份独立审查支持；残余 backend、rounding、1/1125000（预留安全因子后 1/2250000）和 rho=2^24 只在作者证明的显式 XOS 路线下作为待独立复核的条件合同。"
truth_status: "A proved under stated semantic hypotheses; B-C candidate conditional contract; D-E deductions conditional on C"
review_level: "A independently reconstructed in v1/v3 reviews; Boss1 full read-after of author Proof v5; no executable backend audit"
scope: "finite disjoint allocations, fractional residual configuration families, maximum-product singleton rematching, normalized explicit XOS, unit-FSLP, shared singleton REPAIR, flat unrelated-machines schedule"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/fractional_rematching_extension_author_proof_v5.md#all"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/fractional_rematching_extension_rank_exact_first_review_v1.md#all"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/fractional_rematching_extension_rank_exact_review_v2.md#all"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/fractional_rematching_extension_rank_exact_first_review_v3.md#all"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/fractional_rematching_extension_statement_only_v1.md#all"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/fractional_rematching_extension_statement_only_v2.md#all"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/fractional_rematching_extension_statement_only_v3.md#all"
legacy_ids:
  - "fractional-rematching-extension-v1"
  - "fractional-rematching-extension-v2"
  - "fractional-rematching-extension-v3"
  - "fractional-rematching-author-proof-v5"
---

# 1. 对象和版本边界

对象的核心是一个有限单位客户/物品分配接口。原始物品集为有限 \(U\)，给定 \(n\ge1\) 个有序代理和恰含 \(n\) 个不同物品的 \(H\subseteq U\)，令 \(B=U\setminus H\)。代理 \(i\) 的价值 \(v_i:2^U\to\mathbb Q_{\ge0}\) 单调、次可加且 \(v_i(\varnothing)=0\)。配置族 \(y=(y_{i,S})\) 的行质量为一、物品列质量至多一；只允许正质量配置满足 \(v_i(S)>0\)。给定非负有理 \(V_i\) 和 \(c\ge1\)，活动行 \(A=\{i:V_i>0\}\) 要求所有 \(B\) 上可行**分数**配置族 \(z\) 都满足

\[
 \sum_{i\in A,T\subseteq B}z_{i,T}\frac{v_i(T)}{V_i}\le cn. \tag{A2}
\]

该量词是语义假设，不能以一个整数分配福利界或未知最优分配替代。定义正 benchmark
\[
 \mathcal B(y)=\exp\!\left(\frac1n\sum_{i,S}y_{i,S}\ln v_i(S)\right)>0.
\]

本档合并七个冻结源的稳定内容：三个 statement-only 版本、两份 rank 独立审查、v3 增量审查以及作者 Proof v5。statement-only 文件本身没有证明；A 的证明由 v1/v3 审查独立重构，作者 Proof v5 给出更长的实现化证明。本轮 Boss1 已对作者 Proof v5 做完整 read-after；v1/v2/v3 与作者 Proof 的数值合同仍不能视为同一个成熟定理，且 backend 尚无执行审计。

# 2. A：分数 benchmark 重匹配引理（完整结论）

## 2.1 结论

在上述假设下，存在 \(H\) 上的双射 \(\pi:[n]\to H\)，使

\[
 \left(\prod_i[V_i+v_i(\{\pi(i)\})]\right)^{1/n}
 \ge \frac{\mathcal B(y)}{c+1}. \tag{A4}
\]

它可由 \(V_i\) 和 \(H\) 上的 \(n^2\) 个 singleton 值确定性求出真正的最大乘积正边完美匹配；零边先删除，若前提成立则正边图必有完美匹配。运行时间按有理输入总位长计为多项式，不需要精确表示一般无理数 \(\mathcal B(y)\) 或枚举全部 \(2^U\)。允许 \(B=\varnothing\)、\(A=\varnothing\)、重复配置条目和零 singleton；每个分母为零的情况均按分支处理。

## 2.2 推导

对正质量配置，写 \(T=S\cap B\)、\(k=|S\cap H|\)，并选取 \(h\in S\cap H\) 使 \(v_i(\{h\})\) 最大；若配置不含 \(H\) 则以后由缺口补全。设
\[
 m_i(S)=\max\bigl(V_i,\max_{h\in S\cap H}v_i(\{h\})\bigr),
 \qquad w_i(S)=v_i(T)/V_i+k
\]
（\(V_i=0\) 的行将残余比值定义为零）。次可加性给出
\[
 v_i(S)\le m_i(S)w_i(S).
\]
把 \(y\) 投影到 \(B\) 得到满足 A2 的分数族，因此残余项质量总和至多 \(cn\)；原 \(H\) 的列容量给 \(\sum yk\le n\)。加权 Jensen 得
\[
 \sum y\ln v_i(S)\le\sum y\ln m_i(S)+n\ln(c+1). \tag{A3'}
\]

把每个配置质量送到其最大 singleton 的 \(H\)-边，得到行、列均至多一的部分矩阵。行缺口只可能出现在 \(V_i>0\) 的活动行：不活动行若没有正 \(H\)-singleton，次可加性会使原配置值为零。将行缺口与列缺口按运输矩阵补齐，得到正边双随机矩阵 \(q\)。Birkhoff 分解（或 Hall 加逐次减最小正质量）给出若干支持内置换矩阵，其中一个的 \(\sum\ln(V_i+v_i(\{\pi(i)\}))\) 不小于 \(q\) 的加权和，合并上式即 A4。该论证用真实物品身份；不复制配置坐标，也不把一个物品在不同配置中重复使用。

## 2.3 有限位最大乘积算法

令正边因子 \(a_{ih}=V_i+v_i(\{h\})=A_{ih}/B_{ih}\)。任意完美匹配乘积的分子、分母位长均由输入位长多项式界定；两个不同乘积的对数间隔至少 \(2^{-O(nL)}\)。用
\[
 \ln x=2\sum_{k\ge0}\frac{z^{2k+1}}{2k+1},\quad z=(x-1)/(x+1)\in[0,1/3]
\]
在二进制缩放后求有理近似，精度取对数间隔的四分之一除以 \(n\)。在该有限精度下运行有理最大权完美匹配即可保证得到真正最大乘积解。无需近似或比较一般无理 benchmark。

# 3. B：外部 backend 与作者 Proof v5 的条件合同

B 不是原论文逐字定理。它把 A 与一个显式有限 XOS backend 接口组合起来；对任意一般次可加 value-oracle 输入不能自动推出。

## 3.1 E1：活动 residual 与全分数界

作者 Proof v5 在显式 XOS 表上构造固定 lift：对 \(i\in A\)，先令 \(W_i=v_i(B)>0\)，用原 clause 在 \(B\) 上归一化；lift 变量 \(\lambda,z\) 满足行和、\(z\le\lambda\) 及物品容量。其像 \(R\) 包含每个可行分数 residual 配置族的归一化 utility 向量，也能由嵌套前缀分布把任意 lift 点还原为多项式支撑配置族。以 \(b_i=1/|A|\) 为初点，在 \(R\) 上反复求
\[
 M=\max_{u\in R}\sum_i u_i/x_i
\]
并以固定步长更新 \(x\leftarrow(1-h)x+h(b/4+3u/4)\)。有限位凸势分析保证终点 \(M\le2|A|\)，从而所有 residual 分数族都满足 A2（\(c=2\)），且恢复的 \(V_i\) 有多项式支撑与有理编码。此路线的关键是“所有分数族”的 inclusion，而非只恢复一个 witness。

这是作者稿中的候选实现；本轮 read-after 逐节核对了证明接口，但没有运行记录或独立 backend 实现。后续若采用它，必须审计 LP 基本解位长、嵌套前缀回收、空活动集和数值预算。

## 3.2 E2：显式 XOS rounding、mask 与 rematching

作者稿的候选路线先在正 residual 配置上做 support-respecting welfare rounding：独立抽各代理配置，按每个物品的 bid 以有限 CDF 逐次固定，保证归一化总福利至少当前人数的一半，并取 \(d=5/2\) 的松弛。对 \(V_i\ge6\nu_i\) 的行（\(\nu_i\) 为 residual 最大 singleton）做 split，每份价值落在 \([V_i/3-\nu_i,V_i]\)，继承质量至少一；逐轮固定候选，给原物品有限标签。对每个候选使用 candidate-local floor \(Q=210|B|\)，在权重上加移位 \(\beta_i=\nu_i/V_i\)，以 Bernoulli shifted inverse moment 和有理卷积 DP 做确定性标签选择；不复制物品、不把标签当新物品。

最终按真实原价值对 \(H\) 做最大乘积重匹配。作者稿给出对每个比较双射同时成立的
\[
 \operatorname{NSW}(S)\ge\frac1{60000d^2}
 \left(\prod_i[V_i+v_i(\{\pi(i)\})]\right)^{1/n}.
\]
A 与 \(c=2,d=5/2\) 组合得 benchmark 除以 \(1{,}125{,}000\)，另预留固定实现安全因子二后写成 \(1/2{,}250{,}000\)。这些是作者 Proof v5 的候选常数，不是独立审查对该稿的无条件通过。

早期 rank 审查指出若直接沿用原文一般次可加 tail 链，\(\mu=(1/3)\delta^2t_iV_i\) 代回漏乘三，且把任意 Bernoulli 参数或移位 \(f=v+\nu\) 直接套原 Theorem 20 不充分；因此旧 v3 的 60000/1,125,000 不能单凭旧链认证。作者稿改为显式 XOS support rounding 和 candidate-local shift，但其有限位、采样成功率和所有 LP/DP 位长仍需独立复核。

## 3.3 E3：有限位、floor 与成功事件范围

公开的 v2/v3 contract 对内部 floor 给
\[
 \widetilde p_{i,s,j}=\frac1{4|U|}\lfloor4|U|p_{i,s,j}\rfloor,
\]
每 clause 总量至少 \(3/4\)，故 unit-FSLP benchmark 的内部值至少 \(3/4\)。作者稿的 local floor 采用 \(Q=210|B|\) 只作用于候选权重，不改原菜单或物理处理时间。任何最终 bundle 都要按原菜单重新选 indexed clause。E3 仍是条件：必须展示采样 cutoff、候选支撑、DP/log 近似的总位长，以及同一成功事件同时覆盖全部 comparison matching；“每个固定 \(\pi\) 各有概率”不足以直接推出所需量词。

# 4. C：归一化 XOS / unit-FSLP 的条件后果

设 \(m=|U|\ge1\)，每个原 clause 的系数总和为一，菜单显式、可有零坐标、未使用资源和重复 indexed clause。正支持 \(P_{g,s}=\{u:p_{g,s,u}>0\}\)。unit-FSLP 为
\[
 \lambda_{g,s}\ge0,\quad\sum_s\lambda_{g,s}=1,\quad
 \sum_{g,s:u\in P_{g,s}}\lambda_{g,s}\le1.
\]
可行证书把每个正支持作为 value=1 的分数配置，因此 \(\mathcal B_v(y)=1\)，item-inequality 的 log-CONFIG optimum 为零；逐项把质量填到缺口可得 item-equality 版本也为零。此证书使用正支持指标，不使用 private processing weights。

若 E1–E3 经独立验证，内部 floor 的 utility benchmark 至少 \(3/4\)；在 \(c=2,d=5/2\) 且另留二倍安全因子时，作者/contract 给出原菜单实际 NSW 至少 \(1/3{,}000{,}000>2^{-24}\)。因此可固定 \(\rho=2^{24}\)。成功输出对任意固定 \(0<\eta<1\)，令 \(K=\lceil1/\eta\rceil\)、\(q_\eta=\rho^{-K}\)、\(c_\eta=q_\eta/2\)，满足
\[
 \#\{g:v_g(T_g)<q_\eta\}<\eta n,\qquad
 \#\{g:v_g(T_g)\le c_\eta\}<\eta n.
\]
这只是固定 fraction 的低质量排除，不给所有组的常数最小值，也不把辅助机器/作业数当成组数。

# 5. D：共享 singleton REPAIR 的组合推论

给同一 \(n\) 个组增加 \(D\) 个全局共享新资源；每个组增加 \(D\) 个单资源、值一的 indexed repair state，同时保留全部原 state/resource。若原实例有至少 \(n-D\) 个组可达 value 1，则给其余组不同 repair resource 得到增强实例全 unit。任意增强实例分配去掉 repair resource 后仍是原分配，至多 \(D\) 个组被修复，所以原来至少 \(\gamma n\) 个质量至多 \(\delta\) 的组，增强后仍至少 \(\gamma n-D\) 个。

固定 \(0\le a<\gamma\le1\)、\(D\le an\)、\(0<\eta<\gamma-a\)、\(0\le\delta\le c_\eta\)。在 YES（原实例至少 \(n-D\) 个 unit）/NO（每个原分配至少 \(\gamma n\) 个质量至多 \(\delta\)）承诺下，增强 unit-FSLP 可行当且仅当 YES：YES 用完整 unit 分配给每组择一达到值一的原/repair state；NO 若增强 FSLP 可行则由 C 产生少于 \(\eta n\) 个低组，与 \( (\gamma-a)n>\eta n \) 矛盾。该结论是显式有理 LP 的 promise-gap 判定，依赖 C 的条件 backend；D=0 时也只给同一承诺差距。

# 6. E：完整普通 flat-UM 调度接口

每个 indexed state 用独立 private root，每个资源用独立 resource machine，每个组一个 selector；每个 state-resource incidence 是带原始系数时间的 job，在资源机上时间一，其余端点回到自身 root。选定原状态 \(s_g\) 与原 bundle \(Z_g\) 后，选择状态 selector 在 root；选定状态中分配到资源的 incidence jobs 外移到各资源机，其余 incidence 保留在 root；未选状态全部 incidence 保留在各自 root；包括显式零 incidence，不能静默丢弃或改物理时间。

若 \(r_g=v_g(Z_g)\)，选定 root 负载为 \(2-r_g\)，未选 root 为一，资源机负载至多一。因此完整矩阵有 makespan 至多二；仅有少于 \(\eta n\) 个选定 root 可超过 \(2-q_\eta\)。若增强/原实例有全 unit 分配，同一构造给 makespan 一，且 selector 的单位处理时间给 \(\operatorname{OPT}=1\)。这不是所有机器的 \(2-\varepsilon\) 界或一般 UM 算法。

# 7. F：量词、用途与已知缺口

在同一 \(n\) 个组上，若每个分配都有至少 \(\gamma n\) 个质量至多 \(\delta\)（\(0<\delta<1\)），则 C 的正 NSW 给
\[
 \gamma\ln(1/\delta)\le\ln\rho,\qquad\rho=2^{24}.
\]
对固定 \(\eta\) 的 \(c_\eta\) 结论只排除 \(\gamma>\eta\) 且 \(\delta\le c_\eta\)；不能推出 \(\gamma\to0\)（除非另给随规模变化的 \(\delta(n)\)），不能推出所有组都有常数质量，也不能把辅助对象数量代入人口分母。

本对象尚未解决一般 Q-CAG-HALF，也没有把它转成六人 SPE 或客户覆盖结论；不同客户/调度模型保持独立。

# 8. 来源比较、用途和接续

- statement-only v1/v2/v3 逐字保留版本演进：A 相同；v2/v3 改用保守 60000、内部 floor 及共享 REPAIR；旧 20000、1/375000 等数字只作为历史候选，不当最终结论。
- v1 审查完整重构 A、unit-FSLP 证书、matching finite-bit 过程和低 utility 计数；v2 审查核对 60000 的 factor-three 算术和 \(3/4\) floor，但明确未审 backend 全链；v3 审查指出旧一般次可加 tail 的具体缺口，并给出更保守替代链（例如 \(400000d^2\) 或 \(\rho=2^{30}\)），不把该替代链与作者 v5 的显式 XOS 证明混为一谈。
- 作者 Proof v5 自称给出显式 XOS 的 residual lift、welfare CDF rounding、split、shifted inverse-moment、finite mask DP、任意 comparison rematching 和完整 flat-UM schedule；本档及本轮增量审查已全文读取并把接口和常数写入，但没有执行程序、独立 backend 复核或新颖性认证。未来仍应逐项检查 LP 基本解位长、采样 cutoff、相同成功事件和每个 DP/log 误差预算。

该对象可被第三阶段作为多个关系节点使用：A 是一般分数配置到 singleton matching 的证明节点；B/C 是带精确外部前件的条件推导节点；D 是 C 的 promise-gap 组合，E 是 C 输出到普通 UM 全作业调度的实现迁移。与当前六人客户 SPE 主问题没有已知直接同构边，暂不造边。
