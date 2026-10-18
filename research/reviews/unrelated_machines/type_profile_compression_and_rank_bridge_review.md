# 分块类型配置与真实匹配后端的实际审查记录

本记录保留已发生的独立重构和读后攻击；原始来源论文的全部主定理、全球新颖性和一般UM算法不在审查范围。作者冻结整合稿SHA256为 e0e87f81608320da6e65b8f82365d37b7938efb5ef3d5cb11e91533c3de6d957。canonical版本仅修导航、改临时稿口吻并附运行链接；数学陈述未变，主研究者重新逐行核查。

# 分块类型配置压缩的逐支核对与精确有限审计

核对对象：`literature_frontier_type_matching_profiles_final.md` §1–3，最终 SHA256 `e0e87f81608320da6e65b8f82365d37b7938efb5ef3d5cb11e91533c3de6d957`。Claim：`UM-SC-BLOCK-TYPE-PROFILE-RECONSTRUCTION-v1`。

## 身份与结论

本核对者是该 block-count 重构的提出者，不能再计为它的第二名独立证明审查者。独立性准确地是：收到 Exact 后先独立给出算法和承重不等式，再读 BLMRS Appendix B 核来源字样；随后写成自足冻结稿，并在整合后读作者最终文字。本软件审计另用独立的全 count oracle 与实际分配枚举校验实现，但不是外部审查。

接受最终 §1–3 的陈述和证明，未发现声明范围内 fatal。最终稿将原全局 YES 结论强化为“每玩家每个原值至少1的实际子集都包含一个输出 profile”，强化成立：cap、取值落在[1,2)的子集、删tiny、几何舍下和分块舍count全部可在给定的该子集内执行。

范围保持：固定正有理 ε、显式有理输入、m≥1、partial allocation 允许资源闲置。算法只生成舍下矩阵和列表，不输入最优分配、不求共同 profile、不判定原阈值。新颖性、全球优先权和外审未认证。

## 关键量词及边界核对

1. n=0 输出 t=0 及空菜单，OPT=0；该支从不计算 δ/(t a_k)。m=0 不在声明域。
2. tiny cutoff 为 δ/n，删除最多 n 件的加性损失≤δ。等于cutoff的值保留；grid延伸到最小 a_K≤cutoff，不能假定舍下后的最小正值仍不低于cutoff。
3. 任意达到1的实际子集 cap 后仍达到1；首次达到1的 capped 前缀总值严格小于2。该前缀仅用于存在性证明，不由输入算法索取。
4. b_k=1 的 count 舍下无损；b_k≥2 时单type损失<b_ka_k≤δ/t。每块价值≥δ/(2t) 在 u=δ/(t a_k)<2、u≥2 两支均成立，u=2无遗漏。
5. 因舍count后的总值仍<2，Σh<4t/δ≤H，全部见证进入有共同预算的 weak-composition 枚举。
6. 最终值≥(1−δ)/(1+δ)−δ≥1−3δ>1/(1+ε)，对全部正 ε 成立。
7. record数 binom(H+t,t)=exp(O_ε(t)) 是多项式；没有将各type菜单的无约束直积误作多项式。
8. grid以固定有理数 s/r 的整数幂计算，共同分母 s^K 的位长 O_ε(log(n+1))；floor、ceil和阈值比较均可精确完成。复杂度可以强依赖固定 ε，不声称对 bit(ε) 统一多项式。
9. 输出子集只删资源，保全局不交与 exact type counts；不再放回闲置资源。最终 Exact 已显式写出 counts 为非负整数。

## 实际有限审计

代码：`migration_packages_santa_block_profile_audit.py`。
输出：`migration_packages_santa_block_profile_audit.json`。
代码 SHA256：`548f54024eadb0b6a2f18909a6070ac67692a783177b0ef938cc2d0dadd3ea22`。
独立重构冻结稿 SHA256：`c6fd16ab33015979e4a53efb1e14ea7629632ab7cdca7b30a5c3d8d68b8886ac`。

使用 Fraction，无浮点。Seed=824731。106个列出矩阵与 ε∈{1/8,1/2,2,7} 合成424个参数—矩阵检查，m≤3、n≤6，含零资源、零值、cap>1、不可同时满足的 n<m 和长分母端。

- 7612个累计输出 profiles：按block递归生成的完整列表，与独立“先枚举全部可用整数counts、再检查整除及H”的列表完全相同。
- 288个原阈值YES参数—矩阵例：先对所有完整资源分配求真实OPT，再在所有partial allocations构成的搜索空间中直接找完整profile分配，找到一份即停；全部成功。此处并未逐个检查所有可行分配，也不调用证明中的cap子集构造。
- 19620个累计原值≥1的实际行子集：逐一验证至少一个已输出profile的counts被该子集的正type counts逐坐标支配，直接核最终稿的局部强化。
- 4个cutoff精确相等/刚低于cutoff例：相等保留、低者置零，grid bottom按实际区间核查。
- 8个更大局部count向量：n∈{1024,4096}与上述4个ε；全有 b_k≥2 且正count舍弃损失，精确核总损失≤δ、count≤n、Σh≤H。只检查局部count lemma，未穷举这些大例的全局分配或全部profiles。
- 旧cutoff字面删除断言的额外小反例：一玩家、n=10、9件值9/100和1件值19/100，η=1/10。原总值1；旧cutoff1/11会删去前9件，仅剩19/100<10/11。这与文献研究者使用的n=101反例相独立，不改原PDF字节。

这些有限检查验证列出的代码行为和边界，不替代一般证明、共同选择算法或复杂度证明。Exact B 的归一化类型匹配恒等式及其非次模反例不属于本份审计的独立核验范围。


# 类型 profile 匹配后端的独立陈述先行与读后攻击（内部 scratch）

审查对象：`UM-NORMALIZED-TYPE-MATCHING-RANK-VALUE-IDENTITY-v1`。
本记录不登记 canonical、不写 Git、不认证新颖性或外部评审。

## 实际审查顺序

1. 先只收到 root 的 Exact 陈述：显式非空 profile 族、非负有理类型、整数 counts、正归一化分母；每 profile 一个 home、每 player 一个 unit selector、匹配资源端 unit。
2. 未读作者稿时独立推出双向构造和 `OPT=2-V`，并编写独立 Fraction 枚举器。首跑7个固定+54个生成 fixture，656个完整 actual 分配，其中166个严格次二态全部成功解码。
3. 随后读 `/workspace/scratch/1c5ec79ebe2a/literature_frontier_blmrs_profile_reconstruction.md` §5及§6，再读最终冻结稿 `/workspace/scratch/1c5ec79ebe2a/literature_frontier_type_matching_profiles_final.md` §4–6。后者SHA256为 `045dd24754ff04be9201151ddec1d68edd9098f662a82bf6a01fc39b0ce527dc`。
4. 读后追加 indexed duplicate profiles、零 type 保留/省略两个编译版本和完整4资源非次模菜单枚举。最终有限范围见下节。
5. 作者随后在§6新增直接组合界(9)与空菜单 fixed-OPT2 分支。本审查者再次实际读取最终稿§4–6，并回看 Exact A 的输入/空资源入口。此轮审查冻结hash为 `e0e87f81608320da6e65b8f82365d37b7938efb5ef3d5cb11e91533c3de6d957`；§4–5后端没有改变，上述较早hash保留真实审查顺序。

## 独立重构的承重证明

令选中的 profile 为 c_i，归一化 home 权为 `w_iv=v/W(c_i)`。
它的全部 home jobs 总权恰1。若给定实际 UM 调度峰 C<2，每个资源机至多接一枚
unit job。定义 B_i 为**仅所选 profile**实际外送 jobs 所占的资源集合，忽略未选 profile
的外送资源。全局资源独占使 B_i 两两不交。

对每正类型 v，外送的 distinct jobs 数 t_iv<=c_i(v)，并且恰等于
`|B_i intersect E_iv|`，因为不同类型的 E_iv 两两不交。因而

`f_i,c_i(B_i)=sum_v w_iv t_iv=E_i`。

该 private 机只接自己的保留 tokens 及自己的 selector，所以实际负载**恰**
`1+(1-E_i)=2-E_i<=C`。故每 F_i(B_i)>=2-C。C>=2时直接给空 bundles，
不使用资源独占推论。此分支覆盖 OPT2/V0 端点。

反向给任意不交 B_i，逐 player 显式计算全部 profiles 并选 argmax。
每类型从 B_i 取 min(c(v),可用资源数) 枚不同资源，和等量 distinct tokens 任意一一匹配。
类型互斥、玩家 bundles 不交，保证没有实际资源重复使用。未外送 tokens 留原 home；
**所有未选 profiles 的全部 tokens**也留其原 home。selector 放选中 home。
选中 home 峰为 `2-F_i(B_i)`，未选 home 为1，资源负载至多1；F_i<=1且玩家非空，
故全局峰恰 `2-min_i F_i(B_i)`。有限分配最大最小值均被达到，得精确最优值恒等式。

## 主动攻击的边界及结果

- `m=0` 若被纳入，空 UM 的值0不满足右端2−V>=1；最终 Exact B 已显式要求非空玩家，故不是当前缺陷。
- 空 profile 族使 selector 无合法端，`W(c)=0` 使归一化无定义；最终稿显式排除，不使用0/0约定。
- `c(v)=0` 不造 token；`v=0` 在最终稿不造 token。若按 root 初始字面保留零 home jobs，同一证明仍成立，但代码分开审计两种编译。
- indexed 重复 profiles 必须产生不同 home 及不同 token 身份；本证明与枚举都不合并身份。
- 任意 actual 可以外送很多未选 profiles 的 jobs，不能假设它来自前向规范构造。反向只读 selector 所选 profile，所以不会错误重复资源。
- 正向必须放置未选 profile 全部 jobs；最终稿完整保留它们，未发现删 job 换模型。
- count 用二进制并不导致数值复制：最终域每 profile 正 count 总数<=n；显式菜单有多少 profile 就支付多少输入长度。
- 有理分母、类型相等、归一化 v/W(c) 均可用精确有理运算，总位长按整份显式输入收费。
- `c(v)<=availability` 用于 f_ic(R)=1；核心值恒等式在更宽的 count<=n、允许不存在类型的域仍成立，但不能在宽域沿用 f_ic(R)=1。审计含这个宽域 fixture，只作为额外攻击，不混同作者合同。

未发现当前 Exact B 的 fatal objection。这个结论是自足双向证明的内部复核，
不等于得到 shared-resource profile 的全局算法或一般 UM 的低于2近似。

## 新组合界(9)与空菜单分支的读后攻击

此段**使用 Exact A 已证陈述为前提**，不假称本审查者独立重证 A。
若全部 menus 非空且每 profile W(c)>=gamma>0，则对每个 i、每个实际 B，

`f_ic(B) <= v'_i(B)/W(c) <= v'_i(B)/gamma <= v_i(B)/gamma`。

故 `F_i(B)<=v_i(B)/gamma`。对一份共同不交分配先取 player min，再取所有分配 max，
严格得到 `V<=OPT_SC(v)/gamma`；没有把不同玩家/不同配置的 argmax 私自拼成资源分配。
若原 SCOPT>=1，有限原资源分配达到最优，所以可取同一份不交 B_i 且原值各>=1。
A 的逐实际子集性质给 B_i 内一个完整 profile 的资源副本，使 F_i(B_i)=1。
不同玩家仍使用原来不交的 B_i，故 V=1。这证明(9)的两条量词。

若某 C_i 为空，A 的逐子集 completeness 的逆否推论排除该原输入属于 YES。
在一个另行已证的 YES OPT_SC>=1 / NO OPT_SC<=zeta 承诺源上，该分支只可能来自 NO
（非承诺输入无需声称 gap），故输出一台机器两枚 time1 jobs 的合法普通 UM，OPT恰2。
对 zeta>=0、gamma>0，有 `2>=2-zeta/gamma`，满足所列 NO 下界。
这里没有定义空-menu V，没有把该分支代入(8)/(9)，也没有错误输出“原输入一定NO”而不带承诺。
Exact A 已显式处理 n=0 为全部空 menus，故其空资源输入也由这个 fixed-OPT2 分支合法接住。
源玩家数仍>=1；无玩家输入不属于此域。

未发现该新组合推论或完整编译退化分支的错误。它只传递外部给定的源 gap；
没有产生 zeta 可任意小的 SC 困难性，也不把 max-profile 当次模。

## 真实有限审计

脚本：`/workspace/scratch/1c5ec79ebe2a/global_algorithm_profile_bridge_audit.py`。
输出：`/workspace/scratch/1c5ec79ebe2a/global_algorithm_profile_bridge_audit.json`。

最终：8个固定 fixture、54个生成 fixture，每个分别保留/省略零 tokens，共124个版本；
完全枚举1260个 actual 完整分配，331个严格次二态全部验证反向；
每份 fixture 全部资源 owner 分配均跑前向构造并逐机精确回算，且枚举 OPT=2−V。
覆盖 V=0、1、1/2，缺失 type、零 type、零 count、重复 profile 与257bit分母；
拒绝5种不合法边界。有限计算不替代一般证明，也没有调用 UM/SC 优化 oracle。

脚本SHA256：`1c0ac2c662838795bfd8a616cd7cf88f135b29d7a8e6948b0abc70071c9c1ffc`。
输出SHA256：`f38f93614edf8d3e1b17444c8252581b5928f1b7c9ba0c53d22e2a7e9fbc29ae`。

非次模例独立枚举全部计数 profile 后得到
`F({a,b})=F({a,c})=3/5, F({a,b,c})=1, F({a})=1/4`，
确有 `6/5<5/4`。它否定通用 max-profile 的次模性，没有证明 Exact A 每个固定参数生成
的特定菜单都呈现同一反例。没有复核 Exact A 前端或 BLMRS 整篇主定理；本审查只承担 B 后端与所列非次模边界。


## 主研究者最终核对

root独立核了分块预算、弱composition计数、全部子集completeness、big分子分母、真实全部任务双向构造和空菜单分支；对规范位置重跑两份Fraction审计。分块审计仅把文稿定位和输出改为仓库相对定位/标准输出，未改数学核心。规范proof为 `research/current/unrelated_machines/type_profile_compression_and_matching_rank_bridge.md`；代码为 `tests/audits/unrelated_machines/santa_block_type_profiles.py` 与 `type_matching_rank_bridge.py`。精确冻结hash及实际输出见 `evidence/runs/unrelated_machines/type_profile_compression_and_rank_bridge_audit.json`。A的独立重构者同时是其代码作者，不将其自检伪称另一名独立审查；A另经literature_frontier读后攻击和root重新推导。B由global_algorithm先只读Exact重构，再读完整证明；未发现standing fatal。
