---
id: "unrelated-machines/seven-state-affine-boolean-owner-boundary-exact-v1-review"
kind: review
type_tag: 审查
title: "七态原星仿射 Boolean 所有者边界 Exact 与作者 Proof 版本审查"
status: integrated
truth_status: "exact-only-scope-closed; author-proof-and-finite-audit-kept-separate"
review_level: "full-read-5752-byte-exact-cross-read-author-proof-review"
scope: "UM-SEVEN-STATE-STAR-AFFINE-BOOLEAN-BOUNDARY-v1 Exact-only statement, author Proof, exact-first/read-after provenance, and global audit boundary"
summary: "01379ac… 的 Exact-only 源定义七态原星的实仿射 Boolean 分类、共同 M3 Gram-null 到真实支持的替换、同机 unit-owner 至多二结论和跨背景高物理入度边界。本文完整读取 Exact，并与既有 88eb… 作者 Proof 审查、exact-first/read-after provenance、七态全局二次审计和 raw-K2 对象对照；把 Exact 正式接入证据链，不重复作者证明，不升级为全局 owner degree、一般不可能性、调度算法或 hardness。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_seven_state_affine_boolean_owner_boundary_exact_v1.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_seven_state_affine_boolean_owner_boundary_exact_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_seven_state_affine_boolean_owner_boundary_author_proof_v1.md"
  - "source:88ebc1313d383dd51280:history/source/notes/unrelated_machines/sol_seven_state_affine_boolean_owner_boundary_author_proof_v1.md"
  - "source:02671c9d2026c3262451:history/source/notes/unrelated_machines/sol_seven_state_affine_boolean_owner_boundary_exact_first_review.md"
related_objects:
  - "七态原星仿射Boolean所有者边界作者证明审查--审查.md"
  - "七态星全局二次审计与root重放范围审查--审查.md"
  - "../计算/七态星全局二次审计与root重放边界--计算.md"
  - "鲁棒双端环与七态二次局部核双源审查--审查.md"
  - "身份耦合稀释raw-K2三源精读与锐二倍范围--审查.md"
evidence_paths:
  - "archives/unrelated-machines/tools/evidence/seven-state-affine-owner-boundary-v1-exact-20261031/original/sol_seven_state_affine_boolean_owner_boundary_exact_v1.md"
  - "archives/unrelated-machines/tools/evidence/seven-state-affine-owner-boundary-v1-exact-20261031/original/sol_seven_state_affine_boolean_owner_boundary_author_proof_v1.md"
source_sha256: "a38dfcf05158f38d93f1a26c54591944b8a662174018ece9f81388d499bef250"
source_size: 5752
---

# 1. Exact-only 来源身份与读取边界

本轮完整读取 01379acdbf1ccafd6d95 的 Exact-only 源，5752 字节，SHA-256 为 a38dfcf05158f38d93f1a26c54591944b8a662174018ece9f81388d499bef250。源标题是“七态原星的仿射 Boolean 端点与同机 unit owner 边界：Exact-only”，ClaimVersion 为 UM-SEVEN-STATE-STAR-AFFINE-BOOLEAN-BOUNDARY-v1，日期 2026-10-18。原文明确标记为 statement-only，不含证明，未登记 canonical，不声称一般不可能性。

既有 88ebc1313d383dd51280 作者 Proof 审查已经保存作者证明原字节（8086 字节，SHA-256 b887d569b134bebe1a99172d2332d670e60088705e41764db24d775d2da97259），并核对其与该 Exact 的 hash 绑定。作者 Proof 审查页此前因 Exact 未导出而只把 Exact 作为 related-source；本页补齐 Exact 原字节、Exact 的独有量词和版本身份，不重复作者 Proof 的逐步证明。

既有 02671c9d2026c3262451 的 exact-first review、七态全局二次审计/root replay 审查和计算页分别记录独立重构、最终 canonical/read-after 与有限软件字段。本页把这些资料作为 related provenance 和边界依据，不把历史读者的独立性倒写成本轮新的 blind review，也不把有限 PSD JSON 当作本 Exact 的分类程序证明。

# 2. 七态原星 Exact 的完整参数与正支持

参数是正偶数 d,s，满足 2<=s<=d/2；令 eta=s/d，h=s/2，p=eta^3/1000，u0=4p(1−eta)，e=4/5−p−u0。要求 d>=4，1<=h<=d/4；包括 h=1、h=d/4 的整数端点以及 d=4,s=2。所有七类概率和类别内的每个 H-subset 均严格为正。

基础 Boolean 坐标为 C,Y_1,...,Y_d，H=sum_i Y_i。Exact 的类别是：

| C | H | 概率 |
|---|---|---|
| 1 | d | p |
| 1 | 0 | 1/20 |
| 1 | h | 1/20 |
| 0 | 0 | 1/20 |
| 0 | h | 1/20 |
| 0 | d/2 | u0 |
| 0 | d | e |

每个类别内均匀选择对应 H-subset。记 S_h 为零向量、全一向量和全部 h-weight vectors 的并集，Omega0={0,1}×S_h。纯函数分类只需要 Omega0 的全部正质量点；额外 C=0,H=d/2 slice 是真实支持但不参与分类。

此处的“正支持”不是语法端点列表：后续从共同 M3 Gram-null 得到非负平方期望为零时，需要 Omega0 每一点有严格正真实质量。若条件化或改背景使支持缩小，分类和 owner 结论必须重新假设，不能自动继承。

# 3. 实仿射 Boolean 函数的完整分类

令 f(C,Y)=a+bC+sum_i c_iY_i，假设 f 在 P 的每个正支持点，或至少在 Omega0 的每一点，取值于 {0,1}。Exact 的分类是

0、1、C、1−C、Y_i、1−Y_i（某个 i）。

当比较 Y=0 的 C=0、1 两点时，a、a+b 属于 {0,1}，故 b 属于 {-1,0,1}。若 b=1 或 -1，比较同一 h-subset 在两个 C 值下的 Boolean 值，迫使每个 h-subset 的 sum c_i 为 0；交换两个索引得到 c_i 全相等，再用 h>=1 得 f=C 或 1−C。

余下 b=0。对常数取补可归约 a=0，于是 g(Y)=sum_i c_iY_i 在全部 h-subsets 和全一向量上 Boolean。

当 h=1，每个 singleton 给 c_i 属于 {0,1}，全一向量要求所有系数和属于 {0,1}，所以至多一个 c_i 为 1，得到 0 或 Y_i，再恢复常数补。

当 h>=2，交换一个索引得到 c_i−c_j 属于 {-1,0,1}。若所有系数相等，hc 和 dc 均 Boolean，因 d/h>=4，只能 c=0。若不全相等，系数只有最低层 c 与高层 c+1。若两层都至少两个索引，则 h-subset 中高层计数的可能区间宽度至少 2，与 Boolean 值矛盾；因此某一层只能有一个索引。

唯一高层给 g=Y_i。唯一低层给 g=H/h−Y_i，但全一向量值 d/h−1>=3，不是 Boolean，故被排除。这个排除在 h=d/4 边界仍成立；若擅自放宽到域外 h=d/2，H/h−Y_i 在零、h、d slice 上会成为额外 Boolean 非 literal，说明 d/h>=4 是必要边界。该分类是实系数分类，不依赖系数整数性或符号。

# 4. 共同 M3 Gram-null 的真实支持落地

Exact 允许有限原 jobs 的端点变量 X_e，并允许新 affine 候选 f_e(C,Y)。在共同线性泛函 Lhat 上，假设：

1. Lhat(1)=1，次数不超过 3 的 monomials 组成共同 M3 且 PSD；
2. 所有只含 C,Y、次数不超过 4 的多项式，其 Lhat 值等于真实 P 期望；
3. 原 endpoint 的 Boolean 与每 job one-hot 矩等式按总次数不超过 6 支付，特别包括次数四 Boolean；
4. 对 selected endpoint 集合 A，每个 e 有 Lhat[(X_e−f_e)^2]=0。

由 Gram-null，G=X_e−f_e 与所有次数至多 3 的 Q 正交。用 X^r−f^r=(X−f)Σ X^{r−1−j}f^j 及次数四的原 Boolean identity，r=1,2,3,4 时 Lhat(X^r)=Lhat(f^r)。于是

E_P[(f^2−f)^2]=Lhat(X^4−2X^3+X^2)=0。

被积函数逐点非负，而 Omega0 每点具有严格正 P 质量，所以 f 在整个真实支持上 Boolean，因而落入前一节六类清单。对两个 selected endpoints，分别用 Gram 正交乘以 X' 和 f，得到

Lhat(XX')=E_P(ff')，

且一阶矩也相等。这里依赖共同 M3 的 degree-three orthogonality、次数四 Boolean 等式和正支持；只有一阶边际、或只给 M2，不能自动替代这一步。Exact 不要求新 endpoints 先存在真实联合 assignment law，也不把 Gram-null 误写成真实分配。

# 5. 同机 unit-owner 的精确范围

固定物理机器 w，取 A_w subset A，其中每个 e 是不同原 job 在 w 的 unit-time endpoint，并假设这些 endpoints 的同行 pair moments 为零。若原 CONFIG(B) first/pair 与 Lhat 一致且 B<2，则这种 pair-zero 是必要条件。

在 A_w 中定义正 owner 为 Lhat(X_e)>0。Omega0 的四种 primitive pair patterns 全部正：C 与 Y_i 通过 C=0/1、零/全一 Y 获得，Y_i 与 Y_j 通过全零、全一及适当 h-subsets 获得。故两个非零 affine classified functions 的乘积期望为零，当且仅当它们是同一 primitive bit t 属于 {C,Y_i} 的互补 literals t、1−t。常数一与任何非零函数乘积严格正。

因此 A_w 中正 owners 至多两个；若恰有两个，它们必须是同一 t 的 t 与 1−t。若唯一正 owner 是常数一，其余 endpoints 的一阶质量必须为零。零一阶 endpoints 可以任意多个，不应把正 owner 数误称为原资格度。

该结论只计 A_w 内同时被 affine Gram 等式覆盖的 endpoints。要限制机器 w 的全部 unit owners，必须把该行全部 unit endpoints 纳入 A；不能忽略未覆盖的非仿射端点后再声称整行物理 degree 至多二。

# 6. 固定背景与跨背景高 degree

所有分类和 owner 结论可逐固定背景 beta 使用，但每个背景必须重新满足 Omega0 全支持、共同矩、affine Gram 和 pair-zero 假设。未条件化系统的 M3 不能免费赋予任意背景条件点；系数、endpoint 身份和互补 bit 都可以随背景变化。

Exact 给出任意 N>=1 的 scope 例：新增机器 w,u_1,...,u_N 及 N 个 unit jobs J_alpha，每个 J_alpha 只可在 w 与 u_alpha 处理，时间均为 1。令 beta 在 [N] 均匀且独立于七态 P，设

X_(J_alpha,w)=1_{beta=alpha} C，
X_(J_alpha,u_alpha)=1−X_(J_alpha,w)。

固定 beta 时，每个新增 endpoint 仿射依赖 C，每个背景的 w 只有一个可能正 owner。跨 beta 积分后，w 的 N 个 endpoint 全有正一阶，但不同 endpoint 的 pair 仍处处互斥、全为零；新增机器负载始终不超过 1，完整实例还有峰值 1 的 private-home 调度。

这个例子不违反 fiber owner 定理，却排除了“把逐背景正 owner 至多二直接相加为无条件物理 degree 至多二”的错误升级。它没有 near-two gap、hardness 或一般调度否定含义；跨背景路由必须显式纳入共同 law。

# 7. 与作者 Proof、既有七态审计和相邻对象的关系

作者 Proof 审查页已逐步核对上述 h=1/h>=2 分类、h=d/4 边界、Gram-null 到支持 Boolean 的替换、literal pair 互补性、B<2 owner 至多二和跨背景 N-job 反例。本 Exact 的独有贡献是把该 Proof 对应的 statement-only 参数、七类 law、Omega0、M3 degree/one-hot 量词和条件背景范围正式保存为原字节对象；不重新登记作者 Proof 的结论。

七态全局二次审计/root replay 计算页只认证有限参数组的 Fraction PSD、秩、assignment 字段及一次作者/root 输出字节一致。其 not_checked 明列 affine classification software、deep shared-owner law、AND extension、general scheduling 和 SDP finder。因此有限 audit 不能替代本 Exact 的任意 d,s 代数分类，也不能把任意参数程序证明写成已运行。

鲁棒双端环与七态二次局部核对象提供同一七态原星的实际 OPT=1、共同 M3、全局 degree-two physical-load localizer、逐行 CONFIG first/pair 和稀疏支持背景；raw-K2 对象与仿射线合并稿则展示跨行 higher-moment、条件支持和 global owner 接口的不同边界。它们共享 scope 警告，但不是本 Exact 的新 theorem，不能合并为一般 owner degree 或近二下界。

# 8. 已确认项、缺口与处置

在本 Exact 的明确范围内，已确认并归档：

- 七态 law 的所有类别与 Omega0 正支持条件；
- d/h>=4（即 h<=d/4）下全部实仿射 Boolean 函数六类分类；
- 共同 M3 Gram-null、次数四 Boolean identities 和正支持导致的真实支持 Boolean 落地；
- 被 Gram 覆盖的同机 unit endpoints 在 B<2 下正 owner 至多二，两个必为同一 primitive bit 的互补 literals；
- 固定背景条件量词；
- 跨背景任意 N 个正 owner、同行 pair-zero 但峰值 1 的完整 jobs scope 例。

未确认、不能外推：

- 任意条件化后自动保留 Omega0 全支持；
- 未被 Gram 覆盖的非仿射 endpoint 的 owner 数；
- 全局所有物理 owners 的 degree 上界；
- 深层 shared-owner、AND 或非仿射 extension；
- 任意 growing-depth 接线、一般 UM 调度算法、SDP finder、near-two gap、NP/UGC hardness 或新颖性。

处置为 integrated：Exact 原字节与作者 Proof 原字节已复制到 evidence；本页把 Exact-only 合同接入已有作者 Proof/审计 provenance，区分有限软件和解析分类，不创建第二份作者定理或一般不可能性结论。

