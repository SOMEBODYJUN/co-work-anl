# DEEP 包含方向：定向替代数学审阅

任务 `boss6-deep-inclusion-receipt-repair-repair-7c94343cc7f181df`，Boss6 当前 claim `ef36405646ce48a4927ada4c2af45a1a`，definition pin `334c1f94b6f44be498f820cd1a7d63eedd3412f6f05c53206e76d11ec0173a0d`。

本次是旧任务 `customer-attraction-3a-3a-756cb80a6af99d8e` 的 receipt-only 定向替代。唯一数学文字修复为旧 coverage.reason 中“B不能包含A”改成“B不能包含于A（即B⊄A）”。原对象正文、登记陈述、26 输入合同、10 canonical 边及它们的全部绑定均有效；保留 12 linked、6 isolated-after-review，没有新增边或改变已有 whole/contribution/conditional 范围。原 source、旧 receipt 和已 done 任务没有被本 worker 改写。

## 本轮依据与继承范围

本 worker 新读了 18 个核心和 8 个 read 端点的精确模型、陈述、量词、条件、范围、异议和 body 定位；读完十条边的完整语义 payload 及旧 coverage 的每条理由。另读 15 份完整数学正文和 8 份文件的指定完整承重节，逐项范围在 reading-ledger.json 中列明。当前 26 input pins 均与 definition 精确相符，10 canonical 的原 SHA、endpoint_pins、evidence_pins、review_digest 均通过本轮原生只读核验。90 个去重 path/section 引用、74 个文件的字节校验全部成功；这 74 个文件不等于本轮全篇数学实读。

Root 成熟十边审阅及独立整合报告作为已经完成的审阅输入使用。阅读账分别列出其报告 SHA、实际读过的字段，以及所继承的数学判断。下面在当前合同上重核必要推导；前任源码、冻结数组、全历史证书的阅读和历史运行不倒填为本轮操作。没有运行旧 LP、IC/SPE/BI、随机搜索、科学审计或数组重放。原生结构/字节检查不作证明。

## DEEP 的独立同叶重建

固定原 m 人、原有限带标签共同目录和同一完整有序历史纯 SPE σ。合法节点 h 当前规定收益 u<t，且 h 的每个 proper 有序后代节点的规定行动者最终收益均至少 t；这个条件覆盖全部偏离子树，不能只检查 actual 尾。强制当前任意合法 A，再沿同一 σ 完成 z_A。令当前角色在此叶的收益为 d_A，由原节点 IC 有 d_A≤u<t。

任取该叶的一名未来角色，其规定行动 B 所在节点是 h 的 proper 后代，所以它在同一 z_A 的收益 v_B≥t。令 k_x 为这个完整原 m 人终局负载，含 h 的旧背景；对于 A 或 B 中客户，分母均为正。同一客户在 A∩B 上给两人的份额恰同为 1/k_x，因此

\[
v_B-d_A=
\sum_{x\in B\setminus A}\frac1{k_x}
-\sum_{x\in A\setminus B}\frac1{k_x}.
\]

移项并代入两个收益界，逐个未来角色得到

\[
\sum_{x\in B\setminus A}\frac1{k_x}
\ge t-d_A+\sum_{x\in A\setminus B}\frac1{k_x}
\ge t-u+\sum_{x\in A\setminus B}\frac1{k_x}>0.
\]

所以 B∖A 非空，精确包含结论是 **B⊄A**，中文为“B不能包含于A”。原句“B不能包含A”表示反方向的包含关系，不由这条式子得到。这里不声称 A⊆B 不可能。余一人 r=1 时没有未来角色，后继结论为空量词；A 空时当前收益为 0，右侧至少 t，同式仍有效。覆盖相同而标签不同、交叠主题和重复动作都受相同分母处理。

这个结论是逐 A 枝、逐未来 B 角色的限制。不同 B 可共享同一批 B∖A 客户，不同 A 处于互斥子树，故它不提供不同枝共同 actual 钱包、客户去重或统一 IC 系数预算。Hall-B 的 ∀B∃f_B 同叶预留不交换成跨叶共同流；latest-NET 的 13/12 几何例没有完整 SPE 或 DEEP 认证；两 H 合同也没有满足全 proper 后代阈值的保证。因此修正包含方向后，原 isolated-after-review 及其开放共同付款义务保持准确。

精确正文为 `archives/customer-attraction/state/引理/最深低阈值节点的逐后继查询外利润--引理.md`，SHA `42bca128951c583ad938570f289ed39abaaffd8a21a4b05cb56559edf022261b`，本轮全文读；其“同一真实终局的交集消去”已经正确写“B不能包含于A”。共同完整历史模型 SHA `cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88` 亦全文读。修复无 source/object/edge 变更。

## 十条保留关系与实际未付处

1. **last-two-relocation-obstruction，whole / unconditional / ALL。** 同一输入的真实末两人各≥θ_n。若尾部出现任一全局最低者，包括平局，则全部角色≥θ_n、W≥nθ_n。故 W₀<nθ_n 时，任何 W≤W₀ 的完整 SPE 全部 minimum 位置都早于尾部，整份策略替换也至少增加 nθ_n−W₀。证明不冻结后继、不只重排旧终局。n=2 和零覆盖没有严格前提；不否定允许正福利代价的变换或 half。已读末两人逐客户差值证明及障碍全文。

2. **36-exact-relocation-cost，whole / unconditional / ALL。** 只取同一 18 兴趣类型、36 客户、六主题输入，不拿一般 n 族代替。真实末位对重复背景最佳 15、不同背景最佳 12，θ₃=12；034 完整策略给 (10,12,12)、W34，012 达到全 12、W36。任意第二人可同组新题保 12，排重复；同组前两题迫末位补第三，跨组低福利的 minority 只能第一位。成熟精确分类为全部福利 {34,36}、48 个有序可实现终局，其中 12 个含尾 minimum，故精确代价 2、倍率 18/17。48 不是完整策略数，v₃=10 不混 θ₃=12。本轮在障碍的自足推导和已成熟独立审阅上复核，旧 py/冻结 JSON 数组仅核字节，没有重新执行或冒称新完整阅读。

3. **clock-real-ic-weighting-counterexample，whole / unconditional / specializes。** 共用 Exp 钟表示在两人三标签九客户的完整 SPE 实例化，未否定表示定理本身。末位各前缀的三行动值为 (2,13/2,0)、(5/2,4,0)、(4,8,0)，根真实偏离值 (5/2,4,0)。X=5(Y₀−Y₁)₊−Y₀ 的均值 3/2，而负区 Y₀<5Y₁/4 的指标重权积分为 −1/4−1/36=−5/18。固定确定原 IC 的非负权可先平均；对随机收益表示作乘积需辅助权独立收益钟。均未付逐角色平均行权和≤1。钟定理和负区引理本轮均全文读；没有积分 checker 或 12 行程序重跑。

4. **hall-b-trim-and-reserve，whole / unconditional / ALL。** 两源保持完全相同 B/T/O/owner。全部调和割给可送满 bᴴ 的 Hall-B 流，去循环、分解路径后裁至普通 bᴳ，容量不增。守恒及 missing-owner 入流上界给 roleout+sink=bᴳ+in≤bᴳ+eᴱ≤u−ell(O)，预留全部 O modified 边际与 owner 在场误差；已覆盖 E 终端均分 1/[c(c+1)] 加误差正好 1/c。只是一叶一钱包；A/B 不能合领，跨叶共同流和 actual IC 付款仍未证。Hall-B 页全文及运输的 HHYB/全部 B 割承重节本轮已读。

5. **three-maxima-certificate-specialization，contribution / unconditional / ALL。** 固定真实三极大 a，S=max{Σa,n+max a,3n/2}≤2n。下界直接由三私有、互补一对及三对和给出；在 [a_j,S−n] 填到总和 S 达到。三极大核心外非私有 incidence 只能是一对，所以这个更强的全 pair 解付全部真实客户，U−c≤Sν；接目标已经独立证明的 W−c≥nν 得精确三极大推论。ν=0 不除法。remaining 保任意 s≥2 的充分条件及全历史 superset 保底，不提供任意 s 的 2n 解或 SPE 锐性。静态证书全文已读；未重跑 292824 模式/规范化极值程序。

6. **mobius-embed-all-n-aggregate，contribution / unconditional / ALL。** M1 的唯一 signed 反演和 M2 的全部重复子树扩展须共同使用。两组势给非根收益 1、根 0 的辅助 fresh 完整策略，取 K=6M+4 正化；fresh−old 偏置差≥1/2 控制所有重复历史。最坏末位背景另由重复拆分偏置差≥1/3 证明 θ_n=Kb+1，W=nθ_n−1 且 2W>OPT。这里支付每个 n≥3 的一般反族，remaining 保额外独立 36 例，不把赤字 1/2 混算，也不将 signed 小 n 回归当合法全树证书。两编译定理与一般反族本轮均全文读，无数组或 signed 回归执行。

7. **rep-independent-cones，whole / unconditional / ALL。** 有限可信孩子极值达到给 REP；每个前缀独立局部见证首利≥Θ，分别选达到者给 TB 与全族见证预算等价，嵌套见证不必 glue。固定动作表后全部真实有序 IC 和负目标为有理齐次条件；严格实负点在同有理面保平局/零与正支持有理化，统一整数化即可。新见证只需继续 SPE，T 只需继续合法。省且仅省 actual IC 对应 ANY，不能反 actual-TB。动态多锥全文和 REP/独立前缀相关节已读；无统一有限架构上界或 TB 真值新增结论。

8. **any-cones-null-pop，whole / conditional / ALL。** 唯一 conditional 边的额外前提仍是所有有限 ANY 锥均无严格负预算，即普遍 TB-ANY。非零目录添加空标签后所有局部 SPE 都不会规定收益 0 的空动作；补齐新空孩子子树和限制回旧树双向保局部收益集合。全空合法路径 W0 得同目录不同人数动态首值之和≥OPT；此路径不须为 SPE，故不能将 ANY 偷换 actual。四客户 Θ₂=2、静态 v₂=3/2 继续区分。正文和候选相关节已读；没有证明 POP 或该全族前提。

9. **full-cone-individual-normalization，whole / unconditional / ALL。** 全有序真实 IC 锥精确筛形式 σ。每个非零可行点的每位实际角色可以偏离到最大 K 主题，无论真实后继如何至少 K/m，因此 u_i>0，齐次切片 u_i=1 无损。所有 |J|=min(m,k) 覆盖行的有限最大值精确为 OPT/u_i；同实际标签可只测一次。切片总质量≤km 且全兴趣质量 m 使其非空。当前锥定理和探针归一化/组合目标节已读。浮点 union 过滤、123 次 LP 或 448 点不成为全锥普遍上界，没移用 W=1 数值。

10. **reset-swap-two-projection-separation，contribution / unconditional / ALL。** 双信号按同 (b,A) 极小尾重置，反向归纳用 uτ≥dτ(A)≥ell(b,A) 保整棵旧零信号树及实际 u/W/OPT/K。余三人的两个真正交换末回复有共同 b=p+t+q，末 BR 等值给 E0、各自极小性给 JQ/JT≥0，只许全客户常数乘子。两源只付 81 行中 tie 与 minimumB/minimumT 三行；remaining 保其余 78 行及两个不同数据域的投影。目标正文的固定 s 隐藏 k 取 min，以及粗 hist 质量/ell 矩仿射 minorant 已在本轮相关节读清：精确 credit>B 才排局部完成。无 positive score、默认可见点、全局菜单或完整 SPE 新证书。重置全文及分离器前四个完整数学节已读，没有 geometry/LP/score 重跑。

十边中 7 whole、3 contribution；唯一 conditional 是第 8 项。所有 premises_mode 继续为 all，旧字节及 reviewed_by/review_digest 原样保留，新 receipt 精确复用路径和 SHA。

## 其余五项 isolated 的合法继承

梯度页全文给逐客户平方和、凹 log 势全环及同早背景自回复排他；等号只迫客户负载同，不迫主题计数同。有限旧 −3/13 两行、新 −8/13 三支持身份仅反相应抽象表，不生成完整客户 SPE 或一般付款。有限审计与解析定理的角色保留。

latest-NET 页全文给角色 8 两 context 密度 1+1/12，同时总质量仍 1，严格增载 3→4→5。它反纯几何结构聚合密度，未认证完整 SPE、不反同叶 Hall-B 或实际角色金额容量。

重复互惠三路径页全文给必要 a≤(3−t)x/[2(t+1)]，第三路径最后玩家的偏离增益 (t−1)x/[2(t+1)]+(t−2)a/(2t)>0 于 t≥2，直接排该指定合同。两 H 合同采用另一目录/负载：实际 D 尾的 BR 迫 |F|/L≥5p/2，拟定枝末 H 改 D 得 |F|/(L−1)−p>0，E 同叶相消。两者不能没有参数桥而互否全部复制/控制器；两 H 仅完整读其指定“草案的真实动机与未付处”及子节，不读成整页五人诊断。

四真实叶 SQ 的两个指定承重节已读：同一 σ、同深 g/actual 前缀产生 v,D,w,u，e=u−D≥0、ell=v−w≥0，故 (v−D)−(w−u)=e+ell≥0。这只给 off-history v≥w，不给 v 上界、多 g 共用 actual u 的合计容量或逐客户重权 IC。历史后续反例状态按成熟记录保留，不冒新执行。

上述各自没有在本任务比较范围内新增已付逻辑迁移，故连同 DEEP 保六项 isolated。一般开放共同容量、改变惩罚路径或补完整 SPE 是数学边界，不凭相近术语虚造新边或空的后续任务。

## 当前与历史 overlap 处置

当前 successor definition 的 context_plan 没有声明 overlap_comparisons。因此新 receipt.closed_overlaps=[]、follow_up_tasks=[]；没有将旧九对冒充本轮声明并新关闭的对象对。以下九项仅保存旧已 done 包的完成比较与理由，和其十边/coverage 共同继承：

1. `M-94bfb2bc835a4b29ba5ed87ef2e48585` / `M-7f014258b58d49fc9fd0fef19700ec26`：REP的达到性与独立量词现由本包rep-independent-cones完整承重边闭合；固定锥实负点整数化/actual与ANY双域已完整推导，不需另发3B。

2. `customer-attraction/program-reset-swap-visible-and-histogram-projection` / `M-854d5b60283949ce907a8b12c03b1709`：已在本包reset-swap-two-projection-separation保此重置/最坏平局端点ALL，精确提供minimumB/minimumT/tie三行合法性及同一原u/W/OPT/K预算接口。其余78行和两个投影代数在目标正文另已证明，边用contribution明确该remaining；minimum仅辅助信号树，不加给任意原σ。该指定承重比较已解决，不需另发3B。

3. `customer-attraction/program-reset-swap-visible-and-histogram-projection` / `M-c7ce265d763d49989603ff32f23fdc79`：已在本包reset-swap-two-projection-separation保此重置/最坏平局端点ALL，精确提供minimumB/minimumT/tie三行合法性及同一原u/W/OPT/K预算接口。其余78行和两个投影代数在目标正文另已证明，边用contribution明确该remaining；minimum仅辅助信号树，不加给任意原σ。该指定承重比较已解决，不需另发3B。

4. `B3-TAIL-MIN-NORMALIZATION-NO-v1` / `customer-attraction/tail-minimum-normalization-rejected-candidate-and-exact-relocation-cost`：review对端是unassessed审查记录，全文已与两核心同一θ门槛/36输入/43节点/48终局精确核齐；其中一般障碍和恰2成本由本包两条数学边承接，审查导航不另充证明前提，无未付定向比较。

5. `B3-TAIL-MIN-RELOCATION-GAP-36-v1` / `customer-attraction/tail-minimum-normalization-rejected-candidate-and-exact-relocation-cost`：review对端是unassessed审查记录，全文已与两核心同一θ门槛/36输入/43节点/48终局精确核齐；其中一般障碍和恰2成本由本包两条数学边承接，审查导航不另充证明前提，无未付定向比较。

6. `CA-AGGREGATE-LAST-FLOOR-NO` / `CA-MOBIUS-BOOLEAN`：本包mobius-embed-all-n-aggregate保两编译端点ALL，完整核两组F、正偏置、全部重复历史和重复末位背景拆分。对目标一般n部分用精确contribution，独立36例remaining另保；该承重比较已闭合。

7. `CA-AGGREGATE-LAST-FLOOR-NO` / `CA-MOBIUS-FULL-HISTORY-EMBED`：本包mobius-embed-all-n-aggregate保两编译端点ALL，完整核两组F、正偏置、全部重复历史和重复末位背景拆分。对目标一般n部分用精确contribution，独立36例remaining另保；该承重比较已闭合。

8. `M-ccbf3d5d9ff148d2ba833ecca9eeaee9` / `CA-STRATEGY-CONE`：本包full-cone-individual-normalization完整证明从全部有序IC锥到任一实际u_i>0、u_i1归一化与所有min(m,k)组合LP目标；有限浮点/448点没有被升级，比较已闭合。

9. `customer-attraction/background-query-gradient-square-positivity-and-self-reply-boundary` / `customer-attraction/two-topic-pivot-and-cross-background-gradient-original-exact-audit`：两正文实读后明确有限审计与普遍解析性质的作用不同：有限域PASS不是平方/全环普遍证明，旧两行−3/13和新三支持−8/13只排具体抽象表。现有解析页已经自足证明并准确记有限证据，此处没有未付模型映射或需要另发的具体比较，不造仅因检查相近而成的蕴含边。

## 资产处置及哈希图

旧 receipt 的十个 asset 每条 retained，原路径/SHA 精确列于新 receipt.supersession；没有 replaced 或 retired。新增加的 review、reading-ledger、manifest 仅为本次替代的支持元数据，不是正式数学边，JSON 元数据没有顶层 edge_id。manifest 只绑定 review、ledger 和旧 canonical 资产，不绑定新 receipt 或自己；新 receipt 绑定 manifest、review、ledger 和旧十边，故无文件哈希环。旧 receipt 作为历史输入由 ledger 绑定，未改写。
