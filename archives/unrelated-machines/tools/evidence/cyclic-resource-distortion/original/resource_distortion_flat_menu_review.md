# 逐资源畸变完整菜单的实际审查与有限核验

本页只审 `UM-RESOURCE-DISTORTION-FLAT-MENU-APPROX-v1`。接受已发表 restricted Santa 算法定理；未重证外部全文，未实现其生产后端。一般 UM 正反面保持 OPEN。

## 实际顺序与冻结范围

`negation_logic` 只收到精确域与 α>6 陈述，先独立重构 baseline/state-dummy/全部原jobs 输出并冻结，之后才读初始作者稿；该稿当时仅有陈述，没有证明，不能把这次读取追记为全文读后。原记录 SHA256 `ea0619f9244d6e4a6e5fe97bdfc799bd1101fb533ba4af60fc7de09a57a01155`，原字节见 history/source/notes/unrelated_machines/resource_distortion_flat_menu_statement_first_review.md。

另行直接读取 Cheng–Mao 原PDF定义、定理1、Build/Collapse、Lemma18及AppendixA，独立付清确定性、位运算和未知目标接口，再冻结 α>4 后端记录 SHA256 `9509ab6f189202fa618a8963718d15ee7019eaf3a2a31f444127f3de78678791`，原字节见 history/source/notes/unrelated_machines/resource_distortion_flat_menu_backend_scope_review.md。两版只有导入后端常数不同，不把 DRZ 旧错误4+η当依据。

root在读取该独立重构后，自行完整撰写 canonical，不称 root blind。作者采用 bonus 增广，root/独立重构采用直接 baseline；两者保 OPT，但 V 的定义须分别注明。最终正文明确采用含 baseline 的式(3)，没有在 W<1 时偷用旧无 baseline V。

## 根审查与边界

已重构 1≤OPT≤2、baseline 版 OPT=2−V、V/κ≤V_−≤V、dummy-free 实际解码以及所有机器共同负载。κ仅按全部正项计算，非 witness 子菜单；全零、unused 资源没有0/0。非空 groups、各 private 及 resource 机器互异、全部未选/零jobs、每 state 同资源不重复列出是本文域。

原文导入限定为实际 allocation，不把配置 LP 指数 oracle 视作已实现。实现措辞曾需补清：若再做几何搜索，内部常数须更强并支付网格比；正文现明确直接导入完整a近似，另写清分母整数目标的单向FAIL及不要求成功单调的二分。该修补不改变式(2)的域或结论。

反面推论仅排所有输出在此域且κ统一有界的精确 YES≤1、NO≥2−ε、ε<1/(ακ₀) 归约。κ可随固定目标ε变化时需逐参数比较，不能说‘它总是某个常数’就排全部归约。

## 实际软件范围

root全读并运行两套不同的审计。主程序945份小对象枚举普通矩阵及辅助ownership，含 seed210721、巨大分母、全零、bonus和重复states；独立程序1301输入，枚举1328275份原完整调度和20798份正资格辅助allocation。对α=41/10、7各10770份合格辅助近似allocation逐原job回填全部通过。规范独立代码只移除写同目录JSON的两行，root重新运行，规范结果记录自己的代码hash，不冒用原脚本hash。

重跑命令及准确未检查范围在两个 evidence JSON 中。没有实现 CM/DRZ 后端，没有测试全部有理矩阵，没有软件结果构成一般证明或困难性。外审/新颖性未认证。最终实际全文读后记录将沿下面的附记保存，不倒填读前记录。

## 实际冻结读后原记录：resource_distortion_flat_menu_independent_final_read.md

# 逐资源畸变完整菜单定理：首次完整作者证明实读审查

## 1. 对象、顺序与证据身份

审查人：`negation_logic`。本次实际全文读取的 canonical 是

`research/current/unrelated_machines/resource_distortion_flat_menu_rounding.md`

所读版本 SHA256：`3a863222725d5493f49691d5743425ecc1513c1e2d547bb161a0cd614409dbc7`。

这是我**首次读取作者的完整证明**。此前读过的 `source_promise_decoder_draft.md` 在当时仅有域、S1/S2 陈述与 PaperFact，没有作者证明，不能计为完整读后。更早的读前独立重构已冻结为 `resource_distortion_review_before_proof.md`，SHA256 `ea0619f9244d6e4a6e5fe97bdfc799bd1101fb533ba4af60fc7de09a57a01155`；root 明确在读过该重构后才写 canonical，故 canonical 不是与这份重构相互盲写。

后续我另核原始 Cheng–Mao α>4 后端，并冻结 `resource_distortion_backend_scope_review.md`，SHA256 `9509ab6f189202fa618a8963718d15ee7019eaf3a2a31f444127f3de78678791`。该文件不修改读前记录，也没有追认外部论文已被完整重新证明。

## 2. 审查结论

对 canonical 声明的精确完整 flat 域，没有发现 standing fatal。接受 Cheng–Mao 已发表 restricted Santa Claus Theorem 1 后，式 (2) 的确定性总位多项式实际分配结论可由正文所写转换成立。主目标 `UM-TARGET-v1` 的正反面状态仍 OPEN。

以下具体承重项已逐段实查。

### 2.1 域与零边界

G 非空、各 S_g 非空已写明；每组 selector 给 OPT≥1。全部 M_x 和 R_u 两两不同，消除了 private/resource 合并后的负载干扰。原 incidence 集可空，p=0 和 unused/all-zero resources 都合法；κ 的定义含 1，不作 0/0。空组集被明确排除在两段不等式链之外，空任务另返回零分配，正确。

### 2.2 baseline 版 V 与实际 OPT

正文式 (3) 使用的是 \(b_x+\sum p_{xu}\)，不是 W<1 时旧的无 baseline 菜单效用。由于 b_x+W_x=1，各 f_g 的值均在 [0,1]，有限菜单保证 maxima 达到。

正向给定两两不交 B_g，逐组选一个达到 f_g 的实际 state；其 private 负载恰 2−f_g，其余 private≤1，资源至多一枚 unit。即使导出某些零 p incidence，B_g 的不交性仍给资源峰≤1，因此全 jobs 调度合法。

反向仅在 C<2 下读 resource 独占，正确避免在 C=2 时把两件 unit 误当不可能。选中 private 给同一负载恒等式，推出 V≥2−C。OPT=2、V>0 时正向会给峰<2，矛盾，故 (4) 在 V=0 也闭合。没有额外输入最优调度或免费选择 V 见证。

### 2.3 restricted Santa 的两侧值界

每个原资源只建一件 real item，值 q_u=min positive p；并未按 incidence 克隆资源。每个 baseline 只被其原 state 感兴趣；每组 |S_g|−1 件 unit dummy 只被本组 state 感兴趣。这三类物品都严格是每件物品有固有值、玩家只决定零/非零资格的 restricted 域。

式 (5) 左侧：选中玩家的 baseline 与真实资源值向下比较损失至多 κ，其他玩家各拿一枚 dummy。κ≥1 支付 baseline 的比较，所有 auxiliary allocation 真实不交。

式 (5) 右侧：每组至少一名玩家没有本组 dummy；它的正效用至多 b_x+Σq≤b_x+Σp≤1。按组取这样的玩家，保留其正资格 real items，原 p≥q，因此得到 baseline 菜单分配，其最小值不低于当前 Santa allocation 的最小值。对最优 Santa allocation 应用即可得 V≥V_−。零价值或外组 dummy 不增加效用，忽略即可。

### 2.4 全部原任务的实际回译

§4 只导出选中玩家收到且有正价值的 real items 对应原 incidence；这些 items 全局不交，所以所有 resource 峰≤1。所有未导出的 incidence，包括未选 states 的全部 jobs 和 zero jobs，仍在原 private，各执行一次。baseline 没分给所选玩家也不造成缺口，因为可用上界是 a_x≤b_x+Σ收到的q，而非假定它必收到 baseline。式 (5) 还保证后端实际最小值 t≤V_−≤1，所以 2−t 同时覆盖资源和未选 private 的峰1。

第二段不等式差为 \(2(1-c)(O-1)\ge0\)，由 c∈(0,1)、O≥1 得到。若去掉非空 G，这段会失效；当前域已修正。

### 2.5 ≥ 型 NO 承诺及严格 ε

§6 的判别阈值为 τ=2−1/(ακ0)。YES 有 O≤1，而 selector 强制 O≥1，故实际输出峰≤τ。NO 有 O≥2−ε 且 ε<1/(ακ0)，于是任何实际调度峰≥O≥2−ε>τ。因此“输出峰≤τ”可靠地区分 ≥ 型 NO。

严格 ε 不可删除；在等号 ε=1/(ακ0) 时，NO 可能恰有 OPT=τ，会与 YES 允许的输出阈值接触。正文没有误用这一边界。随机归约也没有被升级成仅 P≠NP 的反证。

## 3. 位复杂度与外部 import：接受的准确读法

已直接核读 Cheng–Mao arXiv:1905.06084v1 原 PDF 的 restricted 定义、Theorem 1（物理第 2 页）、其后的未知目标搜索说明、§3 Build/Collapse、§4.3 Lemma 18 与 Appendix A 路径算法。原文给实际 4+δ 近似，固定 δ 时组合迭代为多项式；不是从积分间隙自行推导一个 finder，也不是沿用 DRZ 旧版错误的 4+ε。

组合状态只存实际资源子集、matching、层与路径。值比较是原输入值的有限子集和、固定有理参数倍和整数计数，确定性顺序足够；没有随迭代把分母相乘增长的新权值。正文有理清分母与辅助表大小说明正确，κ 只用于分析而不按数值循环。

正文 §4 的 `t≥V_−/a` 应按**直接导入完整的 Cheng–Mao Theorem 1 的 a 近似算法**理解；这个算法合同本身已经包含未知目标。该读法下 §4 的数值完整成立。

§5 又给了两种实现说明：单向成功目标例程或几何网格。若实际选择第二种，需把常数分层写清：先取固定 \(4<\beta<a<\alpha\)，选固定网格比 g>1 满足 βg≤a，以 β 后端输出 V_−/a；若还有近似配置误差，再在 β、a 之间支付。仅有 a<α 可以支付最终式 (2)，但若几何损失后仍逐字保留 `t≥V_−/a`，则应另选内部 β。这是实现文字的精化，不是当前直接 import 读法下的 fatal。

还有一种完全不损比率的标准补法，已在 `resource_distortion_backend_scope_review.md` 详细写出：清分母后真实 Santa 最优值 V_int 为整数；给整数目标 z 的组合算法加固定参数多项式时钟，精确验证实际输出。真实 V_int≥z 必成功，失败只能在 V_int<z。用 lo=0、hi=全部礼物值之和+1，成功增 lo、失败减 hi。只维护 hi>V_int，最后 lo=hi−1≥V_int，保留的实际输出给 V_int/a 保证；成功标签无需单调。这样不需要精确配置 oracle，也不会因错误目标而无限运行。

我已把上述精化通过 parent message 发给 root，未改 canonical。若 canonical 修改了搜索段，需另记录新全文 hash；本报告当前完整读取身份仅对应所列 `3a863...` 字节版本。

## 4. 独立有限审计的范围

我实际执行的 `resource_distortion_independent_audit.py` 不导入 canonical 或作者脚本。它独立枚举 1296 份二组/各二 states/二资源、p∈{0,1/2,1}、W≤1 的完整矩阵，并加 5 份零值/空资源/异分母边界，总计1301份。

共枚举1,328,275份原完整调度求真实OPT，20,798份辅助实际 allocation，并逐个回填原全部 jobs。α=41/10与7分别有10,770份满足近似前提的allocation，全部满足本接口；观察最大比率3/2。巨大分母样本也通过。脚本与JSON的SHA256已在后端scope文件登记。

这些有限数据只检查值比较、dummy-free读出和原job负载；没有实现 Cheng–Mao/DRZ 后端，没有证明外部算法、一般数学结论、全球新颖性或近二复杂度困难性。canonical 在§7保持了这些层次的分离。

## 5. 最终状态

**限定数学转换：** 实读后无 standing fatal。**外部算法：** 接受已发表 restricted Santa 定理，适用域和固定参数位复杂度接口已核，未独立重证全文。**实现：** 只有独立 finite audit，无完整后端。**复杂度推论：** 仅为固定κ完整flat像类的源筛选，P≠NP等假设按归约种类保留。**主目标、新颖性、外审：** 均未升级。

## 6. 实际重读实现措辞修补后的版本

root 修补 §5 后，我实际重读了 §4、§5 全段、§6 promise 段及相邻上下文。修补后 canonical 的 SHA256 为

`0da64ce52e3d85666aed7c3a156f68c09a699418e584512d851d82a02c3b05c5`。

两段变化已核：其一明确 §4 使用完整 a 近似算法合同，不再额外损失；若改用几何网格，先选内部 a0<a，再令 a0·g≤a。其二完整写出清分母后的整数目标、固定多项式时钟、失败方向、lo/hi 不变式、无需标签单调及 O(log U) 调用数。与本审查第 3 节的精化一致，没有留下 standing 实现措辞异议。

这次修改是实现合同说明的修补，不改变主定理、输入域、α>4 后端来源或 promise 分离阈值。第 1 节的 `3a863...` 对应首次全文实读，第 6 节的 `0da64...` 对应本次明确增量重读；不把两者混成同一版本。

另据 root 报告，独立 audit 复制到规范 tests 后删去了把 JSON 写在脚本同目录的两行，其余保留，并由 root 全文实读及 fresh run。该复制版代码的新 hash 由 root 单独登记；我未将本工作区原脚本 `7f90a...` 的 hash 冒充规范复制文件的 hash，也没有在本次只读审查中自行核读那份复制文件。


## 实际冻结读后原记录：resource_distortion_flat_menu_author_final_read.md

# 逐资源畸变菜单规范正文的作者全文读后审查

审查对象：`research/current/unrelated_machines/resource_distortion_flat_menu_rounding.md`，实际全文读取1–7节；冻结SHA256：`0da64ce52e3d85666aed7c3a156f68c09a699418e584512d851d82a02c3b05c5`。本记录的审查者已写过完整bonus增广版本、读过源定理并与root交换过Exact，因此这是**实际全文read-after**，不是blind/statement-first审查；不替代另一审查者的独立Exact重构。

## 结论

所读版本未发现仍成立的数学fatal objection。正式后端来自Cheng–Mao 2019 Theorem1，而非DRZ旧4结论。规范正文把作者草稿中真实bonus增广改为直接baseline item，保留同一实际OPT和κ比较，而且不需要新增调度jobs；该变化正确。

一项非fatal形式细节已发给root：正文允许每固定**实**α>4，§6却写直接检查峰值是否不超过`2−1/(ακ0)`。若α或κ0为任意固定非有理实数，这不是默认可精确计算的有理阈值。应在YES上界与NO下界之间硬编码一个固定有理separator，或将这项算法描述的常数限定有理。固定参数存在性、隔开的promise和定理(2)均不受影响。此记录不提前声称root已修改。

## 直接baseline与bonus稿的逐项对照

1. 规范V的效用是`b_x+received original p`，其中`b_x=1−W_x`，不是旧未归一化的无baseline V。状态总质量0时V1、actualOPT1正好匹配。作者bonus稿的V则是增广对象V；两个值相等，但规范稿更直接。
2. 每个baseline item只对其state player有正值，不与任何其它player竞争，固有值b_x满足restricted合同。将它加到真实allocation效用中，不是给原调度机器虚加负载或免费释放原任务。
3. 到lower restricted实例时，real值取同资源的最小**正**private值，零incidence保持零/不想要。baseline和dummy都可保原值：κ≥1使它们也满足比较下包络。源标签/状态数无须有界。
4. 从任意lower allocation找dummy-free state时，不需要该state实际收到own baseline。它实际效用t始终至多`b_x+收到real的q`；由p≥q得原调度private负载≤2−t。这个不等式方向已逐项重算。
5. 全部未选states的原incidence留private，负载W_x≤1。原zero jobs也留private，不会凭辅助SC的零值选项给任务增加资格。resource只外送真实收到且有正值的原incidence，对应real items跨players不可拆分，所以原resource峰≤1。
6. dummy-free player的效用≤b_x+Σq≤b_x+W_x=1，故t≤1。这一事实共同控制未选private及resource≤1，不能漏掉它而只报selected-state负载。

## 边界与量词攻击

- 同resource出现正/零混合：仅正值参与κ；零support不被改成正值，restricted eligibility仍逐state正确。
- all-zero/unused resource：不建有正值real item，无0/0；原jobs仍在P，私端0可完整安排。
- 空state或W0：baseline1给该state真实价值1，对应selector加零jobs的原private负载1。
- K_g=1：本组没有dummy，唯一player自动dummy-free，不需要额外pigeonhole前提。
- V0/OPT2：算法可输出t0与all-private2；反向资源独占只在C<2使用，正文没有在C2端点偷用unit容量1。
- κ可增长：算法只取最小正值，不按κ循环；κ的bit长由正值分子/分母位长支付。因子改善可能趋零，未升级为一般UM统一常数算法。
- α固定实数：先固定有理a∈(4,α)后调用R4完全合法。若α作为输入给出，本正文并未承诺统一次数。
- 实际近似比：以O=OPT∈[1,2]、c=1/(ακ)，重新展开差值确为`2(1−c)(O−1)>=0`。
- 源排除：固定κ0与ε严格小于1/(ακ0)时，YES实际上界和NO实际下界有固定正间隔；这只排这个完整flat像类。κ随ε发散仍被允许，不能从中推出标准LabelCover/MinRep可解。

## 来源与总位复杂度

已亲自下载并读取CM原PDF：`history/source/literature/unrelated_machines/cheng_mao_2019_restricted_max_min_allocation_v1.pdf`，28页，768864 bytes，SHA256 `ea99b29b0b05694d16fcf18b63fddcd9dc798aa6ef476ac0b78033c8eaf90e7a`，URL <https://arxiv.org/pdf/1905.06084v1>。实际读restricted定义、Theorem1/印2及其后无需目标oracle的说明、§2.2–2.4、§3.1 Build/Collapse、Claim16末有理参数和Lemmas17–18运行界。没有独立复证全部local-search不变量。

对规范§5的二进制接口，已独立核以下事项：清分母乘积只增加多项式位长；组合最优目标为整数，lo/hi截停二分在`hi>OPT`不变量下不需成功标签单调；target<=OPT时CONFIG可行保证不误失败，其它target若成功只使实际分配更好；0目标为空质量分配。local search所用物品集合、匹配/整数流、固定有理倍target比较不展开数值权。

若需要明确固定参数，令d=min(1,a−4)，γ=d/100、β=γ²、μ=γ³。Claim16末所需式等价于`d > 10γ+4γ²+(15+3d)γ³−γ⁴`；右侧≤0.100418d，故均为可硬编码有理数。signature里的log仅用于分析。该补充不替代外部定理正确性。

另下载核DRZ当前v4：`history/source/literature/unrelated_machines/davies_rothvoss_zhang_2026_santa_hypergraphs_matroids_v4.pdf`，17页，186948 bytes，SHA256 `a95a66ce64fbaf6c49086f6891a19909d271df2fd784e0da530424afd9c91081`，固定URL <https://arxiv.org/pdf/1807.07189v4>；§4/物理15页明确改旧4为6。规范正文只用它纠错，不作为第二个后端。

## 核验与证据层

本次没有实现/执行R4后端，没有重跑root所述945个Fraction小例，也没有把其执行归为本人独立测试。本文审查的是规范正文的所有定义、一般转换、原job合法性、边界和Paper Fact适用性。有限审计的真实数量/代码hash由root自己的冻结输出承担。外审、全球新颖性与独立论文价值未认证。一般UM目标的正反面保持OPEN。


## 最终形式修补的实际复读追加

再次实际读取规范正文§6的完整段落，最终canonical SHA256：`983480e2db1676add57db68cbfd0f7eed4521cddc9c3152ef1de9fe6a283615b`。前序全文审查hash `0da64ce52e3d85666aed7c3a156f68c09a699418e584512d851d82a02c3b05c5` 及其当时意见保留，不倒改为已经修复的记录。

§6现明确取固定有理separator θ，使 `2−1/(ακ0)<θ<2−ε`，只对实际有理makespan与硬编码有理θ比较，并明确不对可能非有理的α、κ0作精确实数比较。我已按修后文字核：ε的严格间隔保证这样的有理θ存在；YES输出峰不超过左端、故严格小于θ；NO所有实际峰不低于右端、故严格大于θ。固定参数下硬编码θ是合法的位多项式判别算法，毋需从任意实数oracle求出θ。

因此前序记录中的唯一非fatal形式建议已实际修复，当前没有standing objection。此追加仅针对该小修补的实际read-after，不新增blind/独立审查身份，不更改原证明或有限测试的证据归属。


## 最后实现细节复核

另一读后者指出实常数阈值不能直接作为精确比较输入；正文§6已改为严格间隙内固定有理separator并由两人实际复读。最终正文SHA256 `983480e2db1676add57db68cbfd0f7eed4521cddc9c3152ef1de9fe6a283615b`。独立读后原记录追加保留此前两次hash和真实来源，未回填先发现身份。无standing fatal；修改只落实原有严格gap的可计算判别。
