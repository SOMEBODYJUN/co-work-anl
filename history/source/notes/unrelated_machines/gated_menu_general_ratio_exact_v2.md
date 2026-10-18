# 任意归一化加权门控菜单的未知最优值 13/8 近似：v2 先冻结 Exact

日期：2026-10-18。v2 是独立加强文件，不改 v1 Exact 或 v1 作者证明。本文只陈述对象、算法合同与结论，不含完整作者 Proof；供先读 Exact 的独立重构。福利配置舍入/按最大 attaining coefficient 争资源是既有 DNS/Feige 机制，非本页原创。新用途仅为这一 ordinary gated 矩阵的完整桥梁、任意权未知 OPT 的结构近似及 robust 参数纠错。

## 1. 完整对象域

G 非空有限，n=|G|≥1；U 有限，m=|U|≥1。每组 g 有非空有限显式 indexed state 表 A_g，总 state 数 S。每 state s 列一个资源集合 U_gs⊆U（同 state 不重复标识）及 p_gsu∈Q_≥0，二进制显式，Σ_{u∈U_gs}p_gsu=1。全部 incidence 数 I；正系数 incidence 数 I_+≤I。可有显式零、unused resources、重复 indexed states、任意 menus 大小和资源重数；未列系数在效用公式中作零。

v_g(B)=max_sΣ_{u∈B∩U_gs}p_gsu∈[0,1]。allocation 为全部 n 个真实不交原资源 bundles B_g；资源可未分配。W*=max_allocationΣ_gv_g(B_g)。所有 max 在有限对象中取得；不是调用未知优化 oracle。

定义 balanced 值

  β*=max( {0} ∪ { min(|H|/n,min_{g∈H}v_g(B_g)) : ∅≠H⊆G，(B_g)_{g∈H} 两两不交 } )。

所有原有限表、p 和各输出 state 身份保持；不以 implicit/exponential states 代输入。

## 2. 显式普通 UM 矩阵及双向完整合同

机器为根 R、一组一个 gate X_g、一 state 一个 private M_gs、一资源一个 Q_u，四类互异，共 1+n+S+m 台。

完整 jobs 恰为：pin J0 仅 R 时间1；connector C_g 在 R 时间1/n、X_g 时间1；selector T_g 在 X_g 及本组全部 M_gs 时间1；每列 incidence 一件 I_gsu，在 M_gs 时间p_gsu、Q_u时间1。其余全部∞。总 jobs=1+2n+I；有限资格=1+3n+S+2I。含全部未选 states、零 incidence jobs；所有 job 必执行一次、不可拆、无抢占，无其他约束。

记此矩阵 P_gate。

**Exact GATE-IDENTITY。** 对每个完整域输入，不要求 unit-FSLP 可行，OPT(P_gate)=2−β*∈[1,2]。给任意 C<2 的完整实际调度可确定性总位多项式提取 |H|/n≥2−C、全部选中原质量≥2−C 的不交原 bundles；给任意 β≥0 的对应见证可构造全部 jobs 峰≤2−β 调度，β=0 用完整峰二基线。C≥2 分支不假设资源 unit 独占。

## 3. 多项式福利 LP 与确定性输出

变量 z_gs≥0（全部 states）及 x_gsu≥0（仅正 incidence），约束

  Σ_sz_gs=1（每组）；0≤x_gsu≤z_gs（每正 incidence）；
  Σ_{g,s:(g,s,u)正}x_gsu≤1（每资源）。

目标 L=maxΣ_{positive incidences}p_gsu x_gsu。零 incidence 的 x 固定零但其物理 job 不删除。变量数 S+I_+、归一化等式数 n、x≤z 链接数 I_+、资源容量数 m，均明确；LP 非指数配置 oracle。

**Exact WELFARE-LP。** 该 LP 总可行，0≤W*≤L≤n。有确定性总位多项式舍入算法，输入一个合法有理最优 LP 解，输出原 states 与真实不交原 bundles，取原 attaining state 后总质量 W 满足

  W≥(1−1/e)L，且 L>0 时 W>(5/8)L。

算法精确有理，先逐组固定一个 z>0 的原 state，后逐 incidence 固定其 conditional Bernoulli 决策；每项只经有限条件期望。概念分布为先独立每组按 z 抽 state s，再对该 state 每个正 incidence 独立以 x_gsu/z_gs 提议资源；每 resource 只交给提议者中原系数最大者。z=0 ⇒ x=0，不计算 0/0，不选零概率 state；实际代码不用随机位。输出每 resource 至多一组；可把剩余资源留未分配。精确条件期望通过所有不同原权重的 tail 水平与概率乘积计算，算法不比较无理数 e。

这是对标准福利配置舍入的显式 rational specialization，不主张原舍入、1−1/e 常数或条件期望方法新颖。只有该具体多项式 LP、显式输入和实际后续门控合同是本页研究范围。

## 4. 排序平衡化与真正未知 OPT 近似

取上节原质量 r_g=v_g(B_g)，非增排列 r_(1)≥⋯≥r_(n)，定义

  β_hat=max( {0} ∪ { min(k/n,r_(k)):1≤k≤n } )。

扫描 n 个有理候选，选 attaining k，以其前 k 个原 groups/bundles 构成 H（若 β_hat=0 可选空集），然后调用完整 gate 构造。算法不输入 OPT、β*、最佳H、源YES证书或 unit-FSLP witness。

**Exact BALANCED-WELFARE。** 对任意原 allocation（不要求是舍入输出）及 w=W/n，均有 β_hat≥1−sqrt(1−w)。原最优值满足 W*≥n(β*)²。这两条是分析不等式；算法只比较上述真实有理候选，不做无理阈值判定。

**Exact GENERAL-RATIO。** 上述有理 LP、state+incidence 条件期望、排序与完整作业构造组成一个确定性总位多项式算法，对本页每个 P_gate 输出完整合法 σ，且

  C_max(σ)≤(13/8)OPT(P_gate)。

不附 unit-FSLP 可行假设，故是整个明确 gated 类的未知 OPT 结构近似。更精细的分析合同可记录为

  C_max(σ)≤1+sqrt(1−(5/8)(β*)²)，OPT=2−β*。

本页不声称 13/8 锐、最优常数或全球新颖性；不把该结构近似推广到 all-group flat、任意原 UM、多层 private tree 或一般 Santa Claus。

## 5. 与源困难性及 v1 的关系

v1 的 unit-FSLP 是更强的 feasibility 证书：Σ_sλ_gs=1，Σ_{g,s:u∈positive support}λ_gs≤1。令 z=λ、x_gsu=λ_gs（全部正 incidence）给福利 LP 的值 n。因此 v1 的真实绝对峰≤13/8 与其 rational LP promise decider 原样保留；v2 不修改 v1 Exact/Proof 的已冻字节，也不回填审查。

对源 robust NO，“每个allocation high_≥δ组数<γ_hi n”互补为“每个allocation low_<δ组数>(1−γ_hi)n”。旧正文中 γ_bad 与 γ_hi 不能直接用同一符号比较。v1 已精确列出其 rational LP promise decider；v2 的全类近似进一步限制本 ordinary gated 编译器，但没有提供一般 near-two hardness，也没有把配置间隙作复杂度困难性。

若声称一个 hard 源编译到本文 gated 类且 YES/NO 实际 OPT 比趋近二，则它与本页全类 13/8 算法冲突（依实际 deterministic/randomized 归约合同分别导出相应复杂度后果）。若源图不满足显式norm1菜单、门控矩阵、真实全部jobs或源NO全allocation量词，则不在此否定范围。

## 6. 证据边界

本文件先冻结 Exact；完整新 Proof、独立攻击、Fraction 双向实际作业审计及通用有理 LP solver 的生产实现分别管理。当前不登记未发生的独立审查、有限运行或外审。不给单次运行数学真值升级。所有工作在 clone 外；不改共同登记，不做 git 写入或 push。
