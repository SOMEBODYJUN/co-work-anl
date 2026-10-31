---
id: "unrelated-machines/identity-coupling-raw-k2-sa3-final-sections-read"
kind: "review"
type_tag: "审查"
title: "Identity-coupling raw K2/SA3 final §13–14 实读增量"
status: "retained-incremental-read-with-scope-boundary"
truth_status: "exact-for-the-specified-final-text-and-read-scope"
review_level: "full-source-read-for-sections-375-702-with-prefix-hash-and-cross-object-comparison"
summary: "对 d38bc86e1cf24e270a1a 的 final actual-read 记录逐字核对：§13 给出十八台机器、十七作业、三十四端点的同一三位 signed functional、完整 raw M2、全部 raw-affine load localizers、逐机 full membership law、实际 OPT=1 调度和跨三机 canonical 负三重矩；§14 给出在同一点 raw-SA3→canonical-SA1 合同下的次数账、质量恒等式、LP 位长与严格边界。该增量保留 source 身份、prefix374 只作 hash 核对、未读软件/linked review/unknown history 的边界；不把局部接口升级为一般 SA1、全局调度、近二 gap 或算法结论。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_identity_coupling_raw_k2_sa3_combined_final_actual_read.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_identity_coupling_raw_k2_sa3_combined_final_actual_read.md"
  - "clean:047a735b371f47f78a00703716f39956c95f0852"
related_objects:
  - "unrelated-machines/sol-general-repair-k2-local-law-canonical-pullback-v1"
  - "unrelated-machines/raw-k2-local-law-canonical-pullback-obstruction"
  - "unrelated-machines/raw-s3-to-canonical-sa1-same-point"
  - "unrelated-machines/raw-k2-sh3-conditional-flow-two-source-review"
legacy_ids:
  - "d38bc86e1cf24e270a1a"
  - "sol_identity_coupling_raw_k2_sa3_combined_final_actual_read"
---

# 1. 来源身份、阅读范围和版本边界

本页只清洗 `d38bc86e1cf24e270a1a`，即
`history/source/notes/unrelated_machines/sol_identity_coupling_raw_k2_sa3_combined_final_actual_read.md`，完整源 SHA-256 为
`069bcb27133cb3d43bd18d57cce77230e93e9489793c6d76cd979c85f1385578`。源作者为 `/root/sol_identity_coupling`，记录日期为 2026-10-18，并明确称自己是知情 final actual-read，不把本次 §13 审查称 Exact-first。

文件报告完整大小 48,840 bytes、702 行。此次实际完整阅读第 375–540、541–702 行，覆盖新增 §13、§14 和末尾 review link。前 374 行没有再次逐字阅读，只核对其独立字节 hash `8c5fcf273f9cd99a7b31b6b082a0880fc7ce186a0771cf600241eb07cc86e221`（25,741 bytes）与 root 指定旧正文一致；因此本页不重新认证前缀中的两算法或旧软件。

§14 的 Exact 独立重构在源中冻结为 SHA `5ee6c219ebde7bd459ba1f5afa24442cb8111de21d3bbfd1fea9bbcdc664746e`，作者 Proof 在 root 读后释放后另冻为 SHA `173148aa4baeac7d9fb66c6e4bad76c935999a9599d85473b56c9e0c9bcaa8b3`；本页把它们作为与 d38 交叉比较的既有来源，不把 d38 的知情阅读改写成独立 Exact-first。源正文指向的 linked review 以及 §13.6 所述 Fraction audit/root replay 程序没有在本次读取中执行或认证。

# 2. §13：十八机 raw K2 的完整合同

§13 的 ordinary flat instance 有一个二态 outer、四个二态 singleton helpers，共十个 indexed states；由普通 flat compiler 得十个 state-private roots 和八个物理资源，共十八台机器。五个 selector jobs 与十二个 incidence jobs 共十七个原 jobs；每个原 job 的两个有限端点都保留，共三十四个 raw variables/endpoints。原 state weights 是 (c,1-c,1)，并在 (0<c<1) 内均正；不删除 inactive job、不把 presence 当成新 job、不附加逻辑模式，也不遗漏原端。

三位 Boolean 形式变量为 (b_1,b_2,b_3)。三位 cube 的 signed weights 是：000 及三个 singleton 各 (35/160)，三个 doubleton 各 (7/160)，111 为 (-1/160)。所以

\[
\ell(b_i)=48/160=3/10,\qquad
\ell(b_ib_j)=6/160=3/80,\qquad
\ell(b_1b_2b_3)=-1/160.
\]

所有端点替换为 (0,1,b_i,1-b_i)，每个 selector 两端互补，每个 incidence 的 private/resource 两端互补。由此全部 Boolean identity、原 job one-hot/exclusivity 及允许的乘子在 degree 4 内为零；共同 (L) 是完整 raw degree-four 表，不是按机器分别拼的矩。

## 2.1 全局 M2

任意 raw degree (le2) polynomial 经替换落在

\[
1,b_1,b_2,b_3,b_1b_2,b_1b_3,b_2b_3
\]

的七维空间，覆盖原始 596 个 square-free degree-(le2) monomials 的 Gram 拉回。正文给出 signed-cube 的统一 PSD 证明：任意 Boolean degree-(le2) 的 (q) 满足三阶差分

\[
q_{111}=q_{110}+q_{101}+q_{011}-q_{100}-q_{010}-q_{001}+q_{000}.
\]

正权七点平方和记为 (S)。weighted Cauchy 系数为

\[
4(160/35)+3(160/7)=608/7,
\]

故

\[
\ell(q^2)\ge\left(1-\frac{608}{1120}\right)S
 =\frac{16}{35}S\ge0.
\]

因此 (L) 对全部 raw quadratic squares 非负；列出的七个正 pivots 只是附加证据，不把未读代码的输出当本页认证。三阶单项为负与 M2 不冲突，因为它不是 degree-(le2) square。

## 2.2 全部 raw-affine localizers 和逐机 law

两条 outer private load/slack 为

\[
\operatorname{load}_0=b_1+c(1-b_2),\quad
T-\operatorname{load}_0=(1-b_1)+cb_2,
\]
\[
\operatorname{load}_1=(1-b_1)+cb_3,\quad
T-\operatorname{load}_1=b_1+c(1-b_3),
\]

其中 (T=1+c)。其余 private roots、四个 home resources 和 fallback loads 均为常数或 literal 的非负系数组合（fallback 代表性 loads 为 (b_2,1,1,1-b_3)）。对任一原全局 affine (q)，literal (lq) 的次数不超过二，且

\[
L(lq^2)=L((lq)^2)\ge0.
\]

因此两条 outer slack、常数 slack 以及 (c+(1-l)) 型 slack 都有针对**全部 raw affine (q)** 的 localizer PSD。

正文还给出完整 local CONFIG：任意两位边际的 (00,10,01,11) 权重依次为 (35,21,21,3) 除以 80，单点一概率为 (3/10)。每台机器的 endpoint variables 最多依赖两位；M0/M1 两张 CONFIG 表逐模式匹配，非空配置分别为 (P_u)、(S,P_u)、(S) 与 (S')、(S',P_s)、(P_s)，最高 load 为 (T)。其余机器是 complementary unit pair、single literal 或 constant，load 至多一。故每一行的全部 membership moments 与该行同一真实两位边际一致，然而这些逐行 laws 没有被拼成 global schedule law。

## 2.3 实际调度与跨行负式

选择 M0、Hu1、Hv1、Hr0、Hs0；每个选中 incidence 到相应 unit resource，未选 incidence 留在 private roots。十七个 jobs 均执行一次，所有 loads 至多一，而 unit selector 给下界一，所以真实 (operatorname{OPT}=1)。

指定 canonical pullback 为 (Z_{M0u}=b_1b_2)、(A_{Hs0}=b_3)。于是 box/claim 行乘 canonical primitive 给出

\[
L(Z_{M0u}A_{Hs0})=-1/160<0.
\]

相应 canonical quality slack 是 (h'=cb_1b_2)，所以

\[
L(h'A_{Hs0})=-c/160<0.
\]

更强地，取真正 raw-affine (q=b_3)，则 (h'q^2=h'b_3^2=h'b_3) 的物理总次数至多四，仍有

\[
L(h'q^2)=-c/160<0.
\]

三个因子来自三台不同物理机器；因此负式不是某一机器遗漏 local triple 的伪影，而是跨行 global triple。它只击破该同一点、指定 direct canonical pullback 的 plain common-SA1/activation-quality 非负性；不击破实际可行性、一般 M2、其它 extraction、另一个 feasible point 或全局 triple-positivity 以外的合同。

# 3. §14：raw SA3 到 canonical SA1 的条件性边界

§14 保留所有 normalized-flat indexed states、zero incidences、duplicate states、unused resources、原 private/resource 端和 selectors；给定 (1\le T<2) 及同一点指定 pullback (A_s=a_s, Z_e=a_{s(e)}E_e)。在完整 S3 合同下，原 boxes/physical slack/unit-cap 行允许最多三个 raw-literal 乘子，Boolean/cover 等式乘子次数受控。

关键次数与恒等式全部保留：

* (1-aE=(1-a)+a(1-E)) 使 primitive/complement pullback 每项至多两个 raw literals；
* ((aE)^2-aE=(a^2-a)E^2+a(E^2-E)) 以 Boolean multipliers 支付；group one-hot 乘目标 (W) 只需原次数至多二，job-cover 乘子至多三；
* canonical resource slack 分解为
  (1-sum aE=(1-sum E)+sum(1-a)E)，由 cap1 lifts 与 literal cylinders 支付；
* quality 关系
  \[
  q_s-a_sh_s=(a_s^2-a_s)+\sum_{e\in s}p_ea_s(D_e+E_e-1)
  \]
  （其中 (h_s=T-a_s-sum p_e b_e)，(q_s=sum p_ea_sE_e-(2-T)a_s)）把 canonical quality 乘 (W) 化为 Boolean/cover 等式及 raw physical slack。即使 (W=Z_f) 或 (1-Z_f)，(h_sa_sW) 也只达到三 raw literals，正好是 S3 合同的边界。

因此，给定完整 S3 functional 时，canonical plain-SA1 rows、resource/gate/quality rows 可同点提取；同一点另有 raw M2 时，canonical affine square 的 pullback degree (le2) 给可选 M1。固定次数 rational LP 的 monomial 数、literal multipliers 数、系数 bitlength 和 vertex/Cramer/Hadamard 输出位长均为多项式；FAIL 只单向排除真实 threshold-(T) schedule。S3 并不由 raw K2、CONFIG 或实际 schedule 自动产生。

## 3.1 与 §13 失败的关键层次界线

§13 的 raw M2 和 raw-affine localizers 只能验证物理 slack 乘 raw-affine (q^2)。canonical (h'=a_sh_s) 含 selector 与 raw slack 的乘积；任意 canonical-affine square 可能需要六阶 raw moments。故 §13 的 (q=b_3) 反例是仍在 degree 4 内的真实负 localizer，而不能被包装成“raw K2 自动失败所有 canonical affine squares”。

若另加**所有** global triple literal 的非负要求，(ell(b_1b_2b_3)<0) 会排除该点；“任意一个 triple 非负都排除”是错误量词。相关 v2 定向补记只澄清这句量词，不改变 §13/§14 矩阵、负式、S3 合同或算法。

# 4. 与已归档对象的比较、独有内容和处置

已读并比较的相关正式对象包括：`sol-general-repair-k2-local-law-canonical-pullback-v1`（十八机全参数族、full row law 与 direct pullback 障碍）、`raw-k2-local-law-canonical-pullback-obstruction`（旧固定/有限 audit 证据）、`raw-s3-to-canonical-sa1-same-point`（S3 条件性同点提取）及 `raw-k2-sh3-conditional-flow-two-source-review`（K2/SH3 层次和 decoder 未解边界）。这些对象已经保存十八机数学主线；d38 不重复伪造新 theorem，而补充以下独有 provenance/边界：

1. §13–14 的 source 是 identity-coupling 作者的 final actual-read，§13 明确不是 Exact-first；§14 只在已有 Exact/Proof 后知情一致性复核。
2. d38 记录 prefix 374 的精确 hash 和全文 702 行、48,840 bytes 身份，明确前缀与新增 §13–14 的阅读分界。
3. d38 明确给出 (h'=cb_1b_2) 与 raw-affine (q=b_3) 的 degree-four 负 localizer，并把它与可能需要 degree-six 的任意 canonical-affine square 分开。
4. d38 明确声明未读 linked review、未运行 Fraction audit/root replay、未把软件执行、未知历史 review 或 prefix 旧算法升级为认证。

因此该增量拟归档到 `archives/unrelated-machines/state/审查/identity-coupling-raw-k2-sa3-final-sections--审查.md`，并与上述既有对象建立“来源—增量复核”和“同点边界比较”关系；不建立“全局调度失败”“SA1 不可能”“一般 UM gap/complexity”关系。所有源正文、旧 evidence 和 Git 内容保持不变。
