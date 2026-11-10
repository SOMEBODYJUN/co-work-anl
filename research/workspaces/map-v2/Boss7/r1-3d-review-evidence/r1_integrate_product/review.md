# r1-3d-product：四条已交付边的共享3D定向数学审读

## 结论与实际范围

四条指定边在当前端点版本下均可按现有文字保留，未发现需修订的数学错误。作用范围依次是 **whole / conditional step / whole / whole**；价格编译边的 `contribution` 必须保留，不能提升为该页全部结论、实际half反例或统一价格存在性。

这是已done成果的定向复核，不新建主覆盖、不再claim，也不改任何clone内文件、Git、队列、registry或integration。只读期间Boss在同clone推进了HEAD：起读为 `a8bc150911e24b59cd3cd4f5f71179c0a193867c`，本报告元数据绑定为 `8ec960078cd70aa2061293a09c6aa7b659d1dccb`。四边、五端点pin与必要正文SHA均在绑定时逐项复核无变化。未审本批其余边，未重跑科学程序、LP、完整树证书或有限扫描。

首先完整实读根 `AGENTS.md` 与 `research/IMPLEMENTATION.md`，依其中ALL前提、整条目标/局部贡献、已done定向处置、3D实质集成约束审读。完整实读共同目录模型、EXACT主文、PRODUCT账本主文、相邻换位主文、统一价格主文；正式关系审查只限四条指定边。旧review仅实读1、2、8、9四节；旧收据与读账本只用作精确版本和范围定位，不把旧worker读过的其余材料计为本次实读。

## 可直接接入3D正文的中文

> 完整历史终局递推给出两类可共用的可信拼接接口。不交客户、相同人数及行动次序、完整Cartesian目录下，组件完整孩子SPE的积仍是产品孩子SPE；不同联合行动即使共享部分组件动作，也属于不同有序孩子，可分别配置可信续局。因此给定目标的总当前收益达到各组件Θ之和就足以构造完整产品SPE，并只推出 `L_prod≤ΣL_k`、`Θ_prod≤ΣΘ_k`。一般产品SPE不能反向投影为组件SPE，门槛没有可加等号。
>
> 该接口支持精确有限价格不可行证书的保成本编译：有理非负Farkas权满足逐位置 `Σw(M_i−u_i)≤0`、`Σw(2W−OPT)<0` 时，清分母后以相同m的整数份单位客户组件构造全Cartesian产品，从末位向根保留递归已可信的目标孩子、逐联合旁枝贴组件极小完整尾，得到整棵有序树的纯SPE，且根W与m槽OPT均可加。限制价格域时须连同真实marked银行或保守proxy行计入 `B=2|I|+1`；没有免费域约束。这里仅完成条件编译环节，未给实际不可行组件/权、普遍有效价格或half闭合。
>
> 同一全集门槛在有序历史h的两层分别给出固定完整尾τ的精确条件：`AB,τ`可实现当且仅当 `α≥M_r(h)` 且 `β≥M_{r−1}(hA)`；整棵τ按后缀历史重标到相同负载的BA后，条件为 `β≥M_r(h)` 且 `α≥M_{r−1}(hB)`。它允许重新拼一份策略，不声称原σ在B孩子会执行搬来的尾。对原σ的强制T真实分支 `(T,C,τ)`，固定移植目标 `(C,T,τ)` 的最小第二节点后悔恰为 `(M_C−d_T)_+`；若 `c_T≥旧实际根收益α`，根与其余节点可保最优，仅该第二节点可能缺陷，并有 `δ≤(α−d_T)+(M_C−α)_+`。该叶来自强制T分支，不能自动保旧实际叶负载、更早祖先IC或多T共同付款。

## 一、EXACT作为四边共同语义基准

模型是有限单位客户、有限非空共同**标签**目录、单位提供者按1至m顺序各行动一次。标签覆盖允许相同、空覆盖和重复行动；策略定义在全部有序历史，弱平局保留。任意偏离必须使用同一完整策略在该有序偏离孩子后的真实后继。

在h的当前角色i固定后，强制动作a的集合R(h,a)只要求后续角色构成完整孩子SPE；当前i被强制，不预设该动作对i最优。定义 `ell_a=min_{z∈R(h,a)}u_i(z)`，`M=max_a ell_a`。这个min始终用同一当前角色i的终局收益，不改成下一位角色的收益或无祖先帽菜单。

有限性使所有孩子非空、极小值达到。必要性由所给完整SPE的每个真实孩子结果至少ell_a和当前IC得到；充分性在规定孩子保给定完整子SPE，在其余有序孩子各取达到ell_a的完整子SPE，再由目标收益≥M保证当前IC。不同有序孩子的后代互不相交。计数仅缓存同构子博弈的**可实现结果集合**，不强制相同计数历史使用同一策略。这也是下面所有“独立贴”成立的依据。

## 二、all-outcomes-to-cartesian-threshold-sufficient-closure

**端点和量词。** `CA-EXACT-PURE-SPE-ALL` v2 → `PRODUCT-TRANSFER-CLOSURE-v1` v2；任意有限个客户不交组件、同m/次序、任意共同深度有序产品前缀。各坐标选定动作a_k后，给定其完整可信孩子SPE与目标叶z_k。只须目标总当前收益满足 `Σ_k u_i(z_k)≥Σ_k Θ_k`，结论是存在一份完整产品SPE实现这些目标叶的产品。

**积的可信性。** 对固定联合孩子a，在每个未来有序产品节点，把第k坐标策略设为对应组件完整SPE在其投影历史的动作。客户不交给收益可加；任意联合偏离b后，每个坐标都按该组件策略的真实偏离后继继续。每坐标的当前收益差非负，故总差非负。这在全部未来节点成立，积是完整产品孩子SPE，而非仅在轨验证。

**共享动作分量不构成拼接冲突。** 对根的每个非规定联合动作b=(b_k)，逐坐标选择使当前i收益达到L_k(b_k)的完整组件尾，再取积。即使b与另一联合动作b'的某个坐标相同，也可以在两个产品孩子使用该坐标的不同续局；完整产品历史保留其余坐标，h·b与h·b'不同，后代互不相交。整棵根策略无需全局因子化为一套仅看投影历史的组件策略。若错误施加这一额外因子化限制，反而会无端丢掉合法SPE。

**根IC。** 每个非规定b的偏离收益为 `ΣL_k(b_k)≤ΣΘ_k`，目标总收益不低于此值；规定孩子也完整可信，故h处及以下全树为SPE。全Cartesian确保每个联合b合法，不能把目录并、受限纤维或耦合动作目录当作本结果。

**只能单向。** 对任意强制联合动作a，组件极小尾的积属于产品可信孩子集合，故 `L_prod(a)≤ΣL_k(a_k)`；再取max并用全Cartesian得到 `Θ_prod≤ΣΘ_k`。产品集合可能还有不能分解为组件SPE投影的补偿续局，故不能从产品SPE倒推各投影SPE，更不能反推等号或必要条件。当前边 `whole_result` 准确。

## 三、exact-product-thresholds-to-finite-price-compilation

**端点和实际贡献。** ALL(`EXACT` v2, `PRODUCT` v2) → 统一可信价格页v1；保 `relation_mode:conditional` 与 `contribution`。输入是同m有限组精确有理组件目标的真实 `M_i^t`、目标叶收益 `u_i^t`、根实际W_t及m槽OPT_t，令 `g_i^t=M_i^t−u_i^t`、`B_t=2W_t−OPT_t`。给定有理w_t≥0，满足每个位置i的 `Σw_t g_i^t≤0` 及 `Σw_t B_t<0`。w不全零；零权组件删除。

**Farkas方向。** 系统 `Gλ≥−B, λ≥0` 不可行的有限有理证书是 `w≥0, w^T G≤0, w·B<0`。若系统可行，则左乘w给 `wGλ≥−wB>0`，但 `wG≤0,λ≥0` 又给 `wGλ≤0`，矛盾。有限有理数据允许将负式正规化后取有理权并清分母；浮点不可行或近似M不承担这个结论。

**整数化的模型保真。** 取公分母D，n_t=Dw_t为非负整数。建立n_t份具有新客户身份的不交单位客户组件；玩家仍为相同m人，每位选择全部副本行动的元组，目录为全部这些目录的Cartesian积。没有分数客户、混合玩家或增添提供者。真实类型重数均为整数。

**核心不是把非可信组件目标直接作积。** 原组件目标后缀未必为SPE。因此从最后位置向根归纳：在目标产品前缀h_i，规定下一孩子已经在更深层构造成完整产品SPE；该孩子允许是非可分解的补偿产品策略。对每个非规定联合动作b，按每份组件在对应投影前缀/强制b_k后的当前角色极小完整尾取积，给当前偏离收益不超过 `Σn_t M_i^t`。规定目标叶收益为 `Σn_t u_i^t≥Σn_t M_i^t`，当前门通过。有限有序兄弟独立配置，既补在轨下方，也补每条离轨旁枝的整棵树。归纳到根得到完整纯SPE。末位BR目标是正文的标准输入；即使只从逐位置不等式看，末位自身无后继、M_m为最大原始收益，非负末位缺口的加权和≤0也会保证产品末位最优。

**福利与OPT。** 根实际覆盖逐不交组件相加。任意产品m元组的各坐标覆盖至多该坐标OPT；反之，各组件各自一份最优m元组逐位置对齐，在全Cartesian中可合法同时选择，故产品OPT恰为 `Σn_t OPT_t`。于是 `B_total=Σn_t B_t<0`。非零背景的剩余角色利润不等同根W；此处B是根覆盖量，未混用。

**真实银行成本不能删。** 若先限制λ∈K，须把定义该域的真实marked银行组件行或保守proxy `gbar=−1_I` 一并放入有限系统，且各自 `B=2|I|+1` 随Farkas权计入。真实银行g≤gbar逐坐标，λ≥0使真实行比proxy更强；用proxy得到 `Σw gbar≤0` 后改回真实g仍有 `Σw g≤0`。B保持同一正成本。proxy只给真M的上界，不冒充其精确值。正文还给全历史clean/cutoff与永久BI退出合同；本次实读这些解析条件，未重跑原程序。

**保留的未付范围。** 本边没有展示具体不可行G或具体w；因此没有实际half反例。统一价格存在性、上下域、BAL、ramp的独立结论不由这条边完成。上下域是普遍价格的必要筛选，域内某个候选也未因此自动普遍有效。

## 四、all-outcomes-to-adjacent-two-gates

**端点和量词。** `EXACT` v2 → 相邻门槛对象v2。任意有限合法输入、每个有序h、余r≥2、任何指定接在hAB后的完整r−2角色尾SPE τ。首两角色终局收益为α、β；M_r(h)、M_{r−1}(hA)、M_{r−1}(hB)均取无祖先承诺帽的全部真实可信孩子。

**AB必要性。** 若h处完整SPE规定ABτ，hA处也为完整SPE，分别由EXACT得到 `α≥M_r(h)`、`β≥M_{r−1}(hA)`。

**AB充分性。** 先在hA保指定Bτ，其余第二动作逐个贴当前第二角色极小完整尾；β门保证hA子SPE。再在h保该A孩子，其余第一动作贴当前首角色极小完整孩子；α门保证h处SPE。两步独立子树拼接，全部有序孩子都完整。

**BA双向。** hAB与hBA负载相同且剩余角色相同。将整棵τ以相同后缀标签序列逐节点重标：每条规定完成和每条真实偏离完成的终局负载保持，所有未来角色IC保持；首两角色主题交换使收益变为β、α。重复上述必要/充分论证，恰得 `β≥M_r(h)`、`α≥M_{r−1}(hB)`。r=2空尾、A=B、空题、别名与零收益均无需排除。

这里构造的是可重新补全的一份策略，不是将原σ在hB孩子的真实后继替换成想要的τ而仍声称“原策略真实偏离”。整条目标只登记这两个iff，边 `whole_result` 无过称。

## 五、adjacent-gates-to-fixed-target-minimum-regret

**端点和合同。** 相邻门槛对象v2 → `M-95339315b24743b1a55ef71f8b039ec6` v1。原完整SPE在h的**实际**当前收益为α。强制首动作T后使用原σ的真实第二动作C及其完整可信尾τ，首两收益(d_T,c_T)。根IC给d_T≤α。强制T分支可以离轨；不能把d_T当旧实际根收益。

交换前两题得到固定目标(C,T,τ)，相同于这条强制T分支的最终负载；新根规定收益c_T，第二角色规定收益d_T。在hC记 `ell_X` 为第二角色强制X后所有完整尾中的最低收益、`M_C=max_X ell_X`。对每个X≠T，任何可信尾都使偏离收益≥ell_X，所以固定目标的后悔至少 `max(0,max_{X≠T}ell_X−d_T)`。不同有序X孩子各取达到ell_X的完整尾可同时达到此下界。目标孩子本身可信且 `ell_T≤d_T`，因此是否把T纳入max不影响正部，最小后悔恰 `δ=(M_C−d_T)_+`，既非单纯上界，也未忽略保持目标叶的约束。

当c_T≥α，保原h根除C外全部真实孩子，它们给当前首角色的真实偏离收益≤α。新C孩子给c_T≥α，根仍最优；新C孩子各第二动作以下均为完整SPE，只有hC当前第二节点可能正regret。若δ>0，完整计划本身仍不是SPE；不能作为“只有根缺陷”的修复器输入。

由d_T≤α：若M_C≤α，则δ≤α−d_T；若M_C>α，则δ=(α−d_T)+(M_C−α)，得所列松弛分裂。移植叶只与**旧强制T叶**同负载，未必与旧h实际叶同负载，因此不能直接嵌回更早祖先并声称所有祖先IC保持。T等于原实际首动作时d_T=α，源松弛为零；也没有多T之间可重复领取同一松弛的证明。

## 六、仍开放且应在投影中显式保留

1. Cartesian充分阈值不提供一般门槛分解、等号、必要性或受限动作纤维迁移。
2. 有限价格编译不提供实际负种子，不决定普遍价格存在性；上下域/BAL/ramp须依原独立正文而非本边的contribution。
3. 两门槛未支付高阈值障碍；它只刻画固定真实尾可实现性。
4. δ接口没有一般第二节点修复、跨祖先保IC或多目标总付款预算；更没有据此解决六人half。

## 七、精确绑定与只读检查

下表是实际字节SHA，不是简写。全部四边的receipt asset SHA、端点registration pin、edge evidence SHA与review digest均重新计算一致。原生 `research edge-check` 四次均返回 `edge-structure-valid-not-a-mathematical-verdict`，proof_scope依次whole、step、whole、whole；这只核结构绑定，数学结论来自上文实质审读。

| 边文件（同目录 map/edges/customer-attraction-3a-3a-a0b2960851be4ccd/） | SHA256 | review_digest |
| --- | --- | --- |
| all-outcomes-to-cartesian-threshold-sufficient-closure.json | `8a59513ddbee25dd6a71db86841626933b5775e8ae137c5a96f38d5e8393dba7` | `6d9c7eed28538fb003d032166365a508cd3ef539f194eb50bce86c58390941b4` |
| exact-product-thresholds-to-finite-price-compilation.json | `5fc2c7c57bca2e395aca16d16e65fe11acf3045f2127f7549092ba38634cc5a5` | `a49bac57a220649066baf20a9cb69432acf0fe634a225e7644b3c7cf76695fd4` |
| all-outcomes-to-adjacent-two-gates.json | `e08d44fbe6a11cda65ce5fba4fccba45559cd106001653ff2cf0619878ecae25` | `32def26f94b715b2dc00a01d8061b62cbfc759dfe9a514ea3c11933dc842fd5c` |
| adjacent-gates-to-fixed-target-minimum-regret.json | `72a3fb58814ba6041f522f33f4b4563c2e55ba5e6ed8f2dc5f5c1330e56e6dd9` | `2c338cb24eb7bbd4faa430d9ef49add0f4ae4978b5f6176a466151404b9748a7` |

| 对象 | 版本 | registration_pin |
| --- | --- | --- |
| CA-EXACT-PURE-SPE-ALL | 2 | `aaa77e1f9a928bc25a315e66e18f424418e64643ec3fdb8717cbc3adc6310056` |
| PRODUCT-TRANSFER-CLOSURE-v1 | 2 | `66f336bb46a3d29d716b1819b9eb1a7ad72bf1d351e5a88f880293b57dc4129c` |
| customer-attraction/universal-credible-price-upper-lower-domain-and-exact-tests | 1 | `81a144578747283250d14af2a029a0ecfcac8c73c684726364ccca9472cdd407` |
| customer-attraction/credible-adjacent-transposition-and-fixed-count-extremal-form | 2 | `c4578f77fab30e7978a68a87a6091a4dd4e7b8b034712900b26a8ef4bb008c71` |
| M-95339315b24743b1a55ef71f8b039ec6 | 1 | `8fcacaf98d1339ac8ff9e8d3214aad1ee3ecf4278f8a7ac639e925943c2ac8e7` |

| 本次实读正文或关系证据 | SHA256 | 范围 |
| --- | --- | --- |
| archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md | `cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88` | full |
| archives/customer-attraction/state/算法/完整历史纯SPE终局全集--算法.md | `667d6f319b1f325bd32538f6b0e5a8e95c1942e2ec97cbc76d7cbaef06b36954` | full |
| archives/customer-attraction/state/资源/产品转移金融接口与阈值障碍的精确命题账本--资源.md | `994532710719c465d76c20aa0bcb7da4646ff5f9d08a009e3b76f151a7840588` | full; relation audit limited to PRODUCT-TRANSFER-CLOSURE-v1 |
| archives/customer-attraction/state/引理/可信相邻换位与固定计数坏点正常形--引理.md | `aaa8859eaa5951c82329b324465346657ddd29c5593aa4ae4898adbf5e7c15b2` | full; relation audit limited to two gates and fixed-target minimum regret |
| archives/customer-attraction/state/定理/统一可信价格的上下域与精确候选筛选--定理.md | `a8a58f3fef8ad4368eea1fb6b0fa845b7e74fcc0e3357eaf3d87bdac7f4f3f5e` | full; relation audit limited to finite compilation with true bank costs |
| map/edges/customer-attraction-3a-3a-a0b2960851be4ccd/review.md | `f9dff0cd0c3bb98c303aa4c149dd0626a180497471789b657c6d482fc14a1fd7` | exact sections 1,2,8,9 only |

机器可读详情见同目录 `verified-pins.json`，包括registry/receipt SHA、definition_pin、每条边全部endpoint_pins和evidence_pins。没有请求任何数学修订、替代任务或新正式follow-up；上述开放项是保持现有结论边界。
