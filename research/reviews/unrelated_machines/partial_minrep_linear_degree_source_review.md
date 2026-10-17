# 部分 Min-Rep 线性度数源的独立重构与读后攻击

对象：[现行正文](../../current/unrelated_machines/partial_minrep_linear_degree_source_and_fee_bridge.md)，精确身份 `UM-PARTIAL-MINREP-SPARSIFICATION-BRIDGE-v2`。本记录区分自足删边证明、外部 PCP Paper Fact、条件 UM 费用桥和未认证新颖性。

## 实际审查顺序

作者先冻结 Exact-only，SHA256 `067ebfea168a2047d4b9a533c17430afdfefff78a14c0cb473f61a401b83c906`；原字节见 [Exact 来源](../../../history/source/notes/unrelated_machines/partial_minrep_linear_degree_exact_source.md)。相应原证明另冻为 SHA256 `0f9b8241108e69d242d140b2228adb0aa4dbaadbb96878224680c5e6cd8ef3eb`，root 已参与交流并亲自重算，不冒称 root 盲审。

第一位审查者只读指定 Exact，未读作者证明、其他审查或父 agent 的证明讨论，独立重构原图列表界、计数、rare upper tail、trimming、位复杂度、degree 必要性、两个 value-preserving 正规化与费用代数。完整原稿 SHA256 `c04b2797441c761c7f452ceb86c05d3647a832975dd4ab3861dc4457922d4840`，见 [独立原稿](../../../history/source/notes/unrelated_machines/partial_minrep_linear_degree_exact_only_independent_source.md)。其自身参数取覆盖阈值ρH₀/8并用 size-biased binomial tail 控 trimming，独立得到成功概率>0.97，不是复述作者常数。外部 PCP 原文未读，明确保留其适用前提。

该稿冻结后，第一位审查者才读上述冻结证明，读后攻击另冻 SHA256 `8d18098504d29946148c9e8b65fa65723b97bd91dbd6822ac657693e76f8e7d8`。确认作者更简短的条件 Markov trimming 也给总失败概率<0.018，无 standing fatal。其指出 degree 必要性只能阻止“无证明设F=1”，不能排除另一个 c 很小且有充分证明的编译器实现F=1；现行正文已准确限定。

第二位审查者此前收到过旧 O(g log g) 结果及新γ/可能 O(g) 的参数预告，但没有读新证明。实际只读 Exact 后独立重构，故记为 **Exact-first，事先有参数预告**，不称完全未见候选。其原稿 SHA256 `b01269e878b076f74bade4699134b176d404bdfd3c04ea4d4b45d583f8f580bf`，见 [第二独立原稿](../../../history/source/notes/unrelated_machines/partial_minrep_linear_degree_statement_first_row_source.md)。它独立得到更强的原 cheap coverage 界和采样常数。该稿冻结后才全文读作者 proof，另冻 SHA256 `2a576ea4c59f9436dee7cbfde6c0c8b4e52117231dd2ef38ab2cd8028a9104e7`，无 fatal；后来收到另一审查者的结论在两份冻结之后，未把它算作自己的推导。

root 自写现行正文 SHA256 `00540e9eb336807cd23b290fdb32876d7e9aaacf0a92310db88d5a3d22c1ce4f`。两位审查者随后均实际核 SHA 并全文读取，回执确认量词、参数、正规化、随机归约假设和费用边界的誊写无 fatal。第一位另核了“每seed”的两项与“同一≥0.9好事件”的同时列表量词，确认没有将单list概率冒充统一 soundness；外部原文仍未由其亲读认证。两份原独立稿保持冻结。

## root 与外部原文的实际核查

root 实读 Moshkovitz 官方最终 PDF 印223–224的 Label-Cover/完美完备定义、Theorem2.1/2.3；取固定误差起点即可，无 PGC。实读 Dinur–Steurer 作者 PDF Theorem1.1（印3）及 Theorem6.2（印24）；主证明只用前者与显式直积，未自动从后者导入 regularity。raw PDF 的字节/SHA/页数在 [manifest](../../unrelated_machines/literature_manifest.json)。

root 与作者实读 Manurangsi arXiv 原 PDF §3完整证明、Lemma7及讨论：其采样/高 degree trimming 是已有框架；其同时性分析控制 unsatisfied 边的常数下尾。本稿的数学增量在更低原覆盖和 rare covered 上尾，与全图只一次总边数事件结合。不能把它说成首创整个稀疏化框架。

作者实际读 ECCC TR24-027 原版 §7.4 和2026修订 §7.4/Lemma7.12/Theorem7.13；root 又实际打开2026修订 primary PDF，核对同段显示定理的 O(g log g) 度数及 O(g^{2+ε′}) 字母表。最初比较稿冻结时只有 web 阅读，稍后实际取得原字节；2026修订1,526,039bytes/106pages、SHA256 `13b8eb55f86cfe28ac8b283fe83612889b335e14b7a87d64d479451693c7dff4`，root 核 header、hash、页数并重读对应两页，原件见 manifest。初始 web-only 冻结记录保留，不倒改成当时已下载。没有审计其整个应用证明；现有较粗多项式字母表不保证改善其连通性应用。有限定向检索没有定位同结论，不等于新颖性认证。作者的实际来源比较原稿见 [来源边界](../../../history/source/notes/unrelated_machines/partial_minrep_linear_degree_primary_comparison_source.md)。

## 已实际攻击的承重点

- 原图正规性用于 heavy incidence 上界；输出不要求正规。平行约束逐条独立采样，不能误用简单图邻居计数。
- 列表可空；总预算 gN 不是逐点 g。生成函数处理 gN>NQ，无额外 logN。
- rare 上尾的 ln g 是节省来源；共同总边数事件只能 union 一次。不得把普通常数尾界直接换成 O(g) 度数。
- trimming 使用中间图 degree 一次性标记；每条已抽中边的条件期望仍包括该边本身。删除边可双计上界，不需高 degree 事件独立。
- NO 的非空与严格 coverage<ρ在同一好事件上；YES 和最大度数是每个种子成立。空输出不能混入好 NO。
- μ 极大时走原图返回；只采样支路才使用 s=O(logD)。分析的列表枚举不出现在算法中。
- value-preserving clone blowup 是全 copy-pairs；不能随便独立重接。公共字母表 padding 保持全投影及 value，不擅自用随机图 regularization。
- 固定参数 PCP 和显式游戏删边的统一 binary 复杂度分开。随机 soundness 对确定性判别器只推出 NP⊆BPP，未声称 P≠NP 足够。
- degree 必要性中 (g−1/2)N 是整数，ceil(ρM) 才给严格下界；非空、平衡、全投影不可略。
- 费用代数需 F>0、c≥0、g≥2、正确源边身份和逐 job 无重复计账。O(g) 源只把一个**足够** F 降成固定常数，未提供该实际收费器件。

## 状态

自足数学证明完成，实际陈述先行重构及读后内审无 standing fatal；root 已核外部来源的实际适用条件。没有生产实现或有限实验完成声明。外部同行审查、全球新颖性和独立成文价值未认证；实际 UM compiler、源一致性和 weak 调度解码仍 OPEN，UM-TARGET-v1 正反面不升级。


## v3 正规、简单与固定高围长的实际独立审查

另审精确身份 `UM-PARTIAL-MINREP-REGULAR-HIGH-GIRTH-SOURCE-v3`，保留 v2 原算法及域。root 提出参数和证明，不能称自身盲审。Exact-only 原稿 SHA `0e2b614ae0a0af12c592d3b57558e2c3baf13cf4377b90b26769fc6e5d24cc61`，证明另冻 SHA `f43e32fa61899de87121c161e3ca51ac76dbaa47daccef5fce7a02ba8609e646`，原字节见 [Exact](../../../history/source/notes/unrelated_machines/partial_minrep_regular_high_girth_v3_exact_source.md) 与 [冻结证明](../../../history/source/notes/unrelated_machines/partial_minrep_regular_high_girth_v3_frozen_proof_source.md)。

两位实际审查者只收到 Exact 后分别重构，未读新作者证明或互传本次证明。二者都已知道旧 v2 的 cheap-list 截长和 rare-tail 思路，此先验如实披露；不是宣称对整个方向零背景。row 独立稿 SHA `7493f719723990b2aa4416b151bef1c84e947eaa71392cd378c0195c9b26fc3d`，pcsp 独立稿 SHA `f9c965c6a8b608ba088e135444c4cc8f19c7ed36798b5259c397b84b09b26396`。两稿自行把 covered 模板子图二部着色，抽一个每份 permutation 暴露≤ceil(t/2) slots 的半数 witness，再以≤4p_e 的逐边条件概率控制全部 copy lists；与作者后来的 e^(2k) 点态密度证明不同。两稿也分别闭合 cycle 期望、same-type/layer repair、统一2B误差和固定G位复杂度。

两稿冻结后，才给予上述作者证明。row [读后稿](../../../history/source/notes/unrelated_machines/partial_minrep_regular_high_girth_v3_read_after_row_source.md) SHA `a012d2d0b32b4691d76e839ac0e87a97b68fd722ff9583ee75c80a60c6613c3e`；pcsp [读后稿](../../../history/source/notes/unrelated_machines/partial_minrep_regular_high_girth_v3_read_after_pcsp_source.md) SHA `8db3a1405825c243a21c57b7e603b72bcbcba43c48c78732cda8424366474fc0`。二者实际核读后均接受作者 factorial-moment、参照独立 samples、真实相关 permutations 的密度比较、实数 Chernoff 阈值和全 lists 同时性；末端 slot 及其 template mate fresh 的短环证明也无 standing fatal。root 亲读两份独立推导与作者全文，核这些承重点及全部参数代数。

两处诚实勘误保留旧字节：作者冻结稿保守多计为2dN份 permutations，真实为dN，故其 samplingFAIL≤.001仍有效；现行正文写实际dN及≤1/2000。pcsp 原独立稿写 z>GB+4U+1，应为 z≥GB+4U+1>GB+4U，仍足保证可选f；其读后稿已明确更正。cycle枚举的安全多项式界按显式顶点和边身份计 O((N′+M′)^G) 即可，不借错误的精细计时声明。

root 另实际打开 Kun v2 原PDF、读取 Theorem1 与 Theorem9/交换证明（物理页1–2、6–7），并核本地12页原字节；打开 Dinitz–Kortsarz–Raz final 原PDF §3（物理页8–9）Lemma3.1、Theorem3.2–3.4。Kun 已有换纤维置换修围长；DKR 以采样/删短环保gap。二者只用于准确比较，不是 v3 自足概率/repair 证明的隐藏前提。DKR final 下载403，未虚构本地原件；manifest如实记web读取。v3仍无生产实现、有限运行或全球新颖性认证，无外部审查及实际UM费用/弱调度解码。主目标正反面均OPEN。


v3现行誊写后，pcsp又实际核SHA并全文读同专题canonical（cd68fd767ed68c15ad3b6b58c5826513cfc7059852bf67ea9c22df30fe8afa96），确认v2/v3域、实际draw数及费用N′M′转写无standingfatal。其新Kun/DKR原文未亲读，因此此回执不认证新增外部比较；root实际读取责任仍如上单独列明。
