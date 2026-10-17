# 双 small 资格行三半合同：作者证明与最近 primary 读后核对

## 来源层级与实际 SHA

本稿在独立 Exact-first 稿冻结后才读作者证明，不是本次候选的盲审。旧稿保持原字节：

`/workspace/scratch/038d9dcc4cac/two_small_incidence_sharp_approximation_v2_statement_first_review_literal.md`

SHA256 `ee6ce66d47247d16dac6cf2a71be92ea5894f8feccafbe0195e81ce989a57437`。

本次全文实读 root 冻结证明：

`/workspace/scratch/038d9dcc4cac/two_small_incidence_sharp_approximation_v2_root_frozen_proof.md`

实际 SHA256 `63da068c732421f76efa84cac37ad15d3e6fd24cc86af605403a344eadaf809a`，与给值匹配。绑定 Exact SHA `051148816053f0c150ee70c9efa1b3f7cb76ecc46b999d793155b4070e3cd065`。

本次另实际读取 Page–Solis-Oba–Maack 的 COCOA2018 accepted author PDF；不是在先行稿中已经知道其 flow plan，不能把本次读后 prior 反写成先前独立推导的来源。

## 数学结论

未发现 fatal objection。root 的 CONFIG／ordered-slot 算法、全 OPT 范围包装和 selector／leaf 形式的 3DM 归约均成立。它与本人独立稿的直接 machine-capacity flow 及 triple-job 形式 3DM 是两套不同的正确推导；无须靠两人同意来补证明。

最近 primary 已给相同的 flow、big-buffer、machine-plan 框架及每机全部资格≤3的三半界。此 common-unit 结构可以直接适配该框架；不能称为新的算法框架，亦不能因本文原输入资格数无界就忽略这个直接重叠。本文所保留的精确参数合同、位复杂度和显式困难性构造不自动成为新颖性认证。

## 1. root CONFIG 与槽证明逐项攻击

零资格预处理保持 OPT：移到零端只减原负载；后续实例所有 remaining finite 均正，row small 数不增。因而“每配置至多3jobs”确实合法，没有遗漏未移除的 zero jobs。

T<b 的整数 b-matching 正确：每行至多两个 eligible jobs，容量2只在两者和≤T时开；其它行容量1。负载候选 O(m)，精确决定是否有 OPT<b 并输出其最优 σ。失败的匹配／cut 证书给 OPT>T。

T=b+a<2b 时，每机配置为至多一枚原 unit job 与至多两 small 的子集；枚举至多 `4(1+|U_i|)` 个配置，确实得到普通精确 CONFIG(T)，不是仅 load-LP。一个 job 可在别机是 small，不改变此机的 job 身份或本机配置计数。精确覆盖及有限有理 LP 的 bit 长界成立。

有序槽中每机 unit 总边际≤1，且 unit 时间b先于全部 small，故 unit 只连第一槽；半开正交叠规则在恰整数端点不生成第二个 unit 槽。任意完整 matching 因此每机至多一个原 unit，不是合并 unit 身份后再猜回原 jobs。

Q_i>2 强迫一个正权的三 job 配置，只可能是 unit 加该行两 small p,q；故 p+q≤a。任意 matching 在此行至多该两 small 加一 unit，负载≤T。Q_i≤2 则最多两 matched jobs；unit 加 small p>b/2+a 的 big 集在任何合法配置中至多一个，所以总边际≤1，排序也使它们只连第一槽。两份 big 不能出现；余下 pair 至少一个 small≤b/2+a，另一份≤b，负载≤3b/2+a。作者另列两 light 的分段估计同样正确。

条件 Q_i>2 及 Q_i=2 的边界、a=0、a接近b、空行、零概率均处理正确。不要求实际存在 b 端；b作为 common 上界足够。

## 2. 全 OPT 包装与 σ 输出

[b,2b) 的 CONFIG 可行性只在本行 unit位0/1加至多两 small 子集和处改变，即 O(m) 个不同负载阈值；unit job 身份数影响 LP 变量数但不增加不同负载值。最小可行阈值 τ 若存在，满足 τ≤OPT：OPT<2b时由整数最优配置见证；OPT≥2b时因τ<2b≤OPT。

若全部失败，必有 OPT≥2b。作者设 τ=max(2b,L)，其中 load-LP 最优值L≤OPT，故τ≤OPT且τ≥2b。标准 ordered slots 的每个后继槽 matched 时间≤前一满槽积分，加第一槽≤b，得到每机≤τ+b≤1.5τ≤1.5OPT。无隐式 OPT oracle；输出取原 jobs 的真实 finite 端。

所有步骤都是有限精确有理 LP、排序、max-flow／matching 和实际回算；没有按 binary 数值作伪多项式循环。零、空、单机、单 finite 端及没有实际 unit 的输入范围均不破证明。数学算法完整，不表示已写生产实现或已跑有限审计。

## 3. root 的 selector／leaf 3DM 归约

各 a 的 unit selector 只在含 a 的 triple 根资格；若 a 无 triple，原源已 NO，可用一机两 unit 的合法常量 NO。只检查 A 的孤立也足够合法：B/C 在此是外机而不是需要 finite 资格的元素 job，孤立 B/C 只会让低 C 见证不存在。源无 triple、q≥1因此被处理。

每 triple 根恰两条不同 small leaf 资格；B、C 资源使用 tagged sides，故即使坐标原底集相同也不是同一机器。选中的 q 个根在 C<1.5 下都必须把两 leaves 外送；每外机至多一枚 unit，解码 B/C 各互异，和 selector 的 A 各一次共同得到 perfect3DM。YES 的全部未选 triple leaves 父置负载1，原 jobs 无遗漏。

所有 finite仅1/2或1、无 zero，每行 positive small≤2；资格可能多的 selector仍只具有 unit时间，满足精确类。下界不借 LP gap；对任意固定ρ<1.5实际比较输出C<1.5即可判源。

本人先行稿使用另一种正确构造（X/Y元素small jobs、每triple unit J_e可去根或Z资源），二者无需混合。Karp 的 source 域已在先行稿中按现有原文重印实际核对，不在本次重新冒称证明源 NP-completeness。

## 4. 最近 primary 的实际读取

题名：Daniel R. Page, Roberto Solis-Oba, Marten Maack, *Makespan Minimization on Unrelated Parallel Machines with Simple Job-Intersection Structure and Bounded Job Assignments*，COCOA2018 accepted author version。

- 原始 author URL：`https://drpage.pagewizardgames.com/COCOA2018_dpage_solis_maack_accepted.pdf`。
- 本地实际读到：`/workspace/scratch/038d9dcc4cac/project_sources/page_solis_oba_maack_2018_bounded_job_assignments_author.pdf`。
- 实际 SHA256：`a2fad69bcf3b1e6caed4ce4f29d559e1b0f394695d859f2ca0fd8f05f8296775`。
- 亲读摘要／对象域及 §6 的物理 PDF9–11（printed9–11）全文，Fig5 network/caption 与 Theorem2；§6 标题在前一页末。原文假定正整数时间，定义 bounded assignments 为**每机全部 eligible jobs** 的数量，不是仅 small 数。
- Theorem2 明确给全部 eligible≤2、3、4时的精确、3/2、5/3算法。Fig5 已用 big组容量1的 buffer、总 machine容量d、small直接流入的网络；§6 cases(b),(c) 按本机全部jobs能否一起放及≤3来选plan。

因此“不计 unit 资格数”的当前结构不字面等于原文定理的 |J_i|≤3 输入。但下面的直接适配证明确实保留其机制，不构成独立新框架。

## 5. common-unit 代理适配与重叠边界

固定 b≤T<2b。对每 machine，将所有真实 unit 资格仅在**本机 plan 分类**时视作一枚大小b的代理类型，和其至多两 small 类型合计≤3。实际流图仍保留每个原 job 节点及全部资格，所有真实 unit 资格共用一个容量1门；绝不是把全局原 unit jobs 合成一枚 job。

T<2b保证任何 T 调度在本机至多一个 unit。因此原文≤3型 plan 可直接用于此局部分类型：

- 若代理加全部 small 的总时间≤T，允许这些本机类型全部共存，同时继续给真实 unit组容量1。
- 否则限制总 assigned job数为本机类型数减1，且沿原文门限制所有 p>T/2 的资格（包括全部 units）至多一个。

原 T 调度嵌入这些限制：不能同时取完一份负载>T的全部类型，且不能有两个>T/2的 jobs。若原机器没有 unit资格，本来就只有至多两个 small，按原文≤2分支精确处理。真实 unit组的额外门在“全型能共存”情形也必须保留，避免把多个同型 unit错误当作多份代理。

所得满流若本机接完所有型，负载≤T；其余至多两份且至多一big，负载≤b+T/2（若两份均light则≤T）。由于 T=b+a，`max(T,b+T/2)≤3b/2+a`。所以当前阈值合同本身已由原文 machine-plan 的该显式 common-unit 适配覆盖；全输入包装、零资格预处理与 rational bit 编码补齐不能被写成新算法框架。

该适配是本次读后独立核出的直接推论，不把更宽“unlimited unit”输入合同假称为作者原文定理的逐字 statement，也不声称作者文中已明确写了此代理扩域。原文整数假设对 binary rational 可用有限精确比较／匹配实现；若用统一缩放，分母乘积的编码长也仅为各输入分母位长之和。零资格则由本合同第1步移除。

## Status

root proof全文读后攻击完成，实际 SHA 匹配，无fatal；新 primary 的最近算法框架重叠已明确。旧 Exact-first 稿不倒改。未认证新颖性／外审／独立成文价值，未新增生产实现或有限运行。一般 UM 的统一离二正反面保持 OPEN。
