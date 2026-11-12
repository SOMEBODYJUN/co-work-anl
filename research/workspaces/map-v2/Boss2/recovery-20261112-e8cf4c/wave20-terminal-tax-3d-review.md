# W20：固定完整策略终局税锥的只读 3D 预读

本报告为 Boss2 的只读实质数学预读，不是正式主覆盖，不是任务交付、正式边或收据。工作 clone 为 `/workspace/scratch/e8cf4ce833a5/co-work-anl-boss2`。没有认领或修改任务，没有操作 Git、registry、integration、coverage、正式边或收据；唯一主动写入为本报告。未访问 Library 或上传凭据。没有执行原科学入口、LP/MILP、全矩阵或全 SPE 审计。

**结论先行。** 当前核心 `M-2bfcda8cbda3409cad3c1a38f4eac783` 的成熟证据准确证明同一固定 259 动作策略锥的全非负客户重数税余量：

\[
W+\tau_{\rm full}-\operatorname{OPT}_4\ge T/35,
\qquad T=\sum_{M=1}^{63}x_M.
\]

这不是一般终局税付款，也不推出 ENT1。由它还能解析转换出该锥的锐福利界 \(\operatorname{OPT}_4\le7W/4\)，但当前 registry 已有覆盖同一后继策略、全部根动作的较大正深度锥的 \(7/4\) 福利结果。故本次福利推导应保留为**已有结论在完整根 IC 子域上的另一证明及显式证书转换**，不建议新增福利对象；不得将它硬塞为原税核心的 statement。子域包含关系已核，未证明包含严格。

## 1. 阅读快照、任务及 pins

开始读取、比较与去重使用的 registry 快照 SHA256 为 `2b066a396f3e3032544ab8a4c97cb74cbcb3c0852c92a65a5195fc714b824d02`。保存时 Root 的并行集成已使结束阅读快照变为 `2148b2fcbfd6788d1b109248ee8f067b7d7d1f738f5e0a3cee3f4f4fcc4a1d9c`；任务原文字节未变，核心在结束时另作只读 show，仍是 v2、pin `54fa95c791fce0b637a81fc0e7f05324fe6e66f5f20b4e5cb46649348f2aa1d2`、binding current。下表其它端点 pins 与 canonical 去重均指各自实际读取时的快照，不冒称对结束快照重做全图扫描。这是本 clone 的明确字节快照，不声称是远端实时任务状态；本次没有 Git 或同步动作。

已读根规则 `AGENTS.md`（SHA `20293db840f907c32f774b0d7f72450c56e6c0ad937720699d14f7c02e693cc9`）、`research/IMPLEMENTATION.md`（SHA `fb6613cd0c429f28b8bcfb1064076a629540cfbee8f7e3d670b0b39e78ff0d4b`）及 `prompts/03-map-worker.md`（SHA `6629f71923c54d994297d54c3737b285227b72c463641d318c3f61c9342d07b2`）。

任务原文为 `research/operations/map-v2/tasks/customer-attraction-3a-3a-518b9d3ca3cd7082.json`，SHA `394d7a8a6620f7ea2140bbece633f5445c5e7e850c83c529c52f2303fc41035c`。读取时本地原文为 `state=available, owner=null`，核心只有本税对象，`read_object_ids=[]`。核心 input pin 与当前 `research show` 一致。**definition 和 definition.context_plan 两处均没有 overlap_comparisons 字段，也没有 comparison_groups**；六个 deferred 候选只是发现提示，不能视为 in-packet、follow-up、已读依赖或已支付前提。

以下 pins 由只读 `research show` 返回，读取时均 `binding_status=current`。比较端点 pins 中前七项由支持子代理 `comparison_endpoints` 取得并回传；核心和最后两个 230 对象由本预读者亲自取得。

|对象|v|registration pin|
|---|---:|---|
|`M-2bfcda8cbda3409cad3c1a38f4eac783`|2|`54fa95c791fce0b637a81fc0e7f05324fe6e66f5f20b4e5cb46649348f2aa1d2`|
|`CA-STRATEGY-CONE`|7|`291bd4d94e33d40566453a33b5cf07b1c620b77362268417582efecb42b0c4bb`|
|`M-21b495b7e58840219b8452da00e263d2`|5|`b279eee54893fd85e3bd074375ea0cdd0d545cbd4778dbd4a618eb5caf9d4100`|
|`M-05b51399a0114768921338b101578273`（ENT1/SAIC 反例）|2|`168d3c72291a54640e4bb0d3779b0fb0efba031884ad88923c1d1957f8f7a1ae`|
|`customer-attraction/residual-payoff-tax-calculus`|1|`779995a2df37d219c501e728531e3ca4b83eaa87e7deff2653d5d66dcd5e89ba`|
|`CA-ROOT-TAX-NO`|3|`9ccf2e6812603affa30850cacbcb50b716f4ddfbebd1f38ab7243559c859c29a`|
|`CA-DISJOINT-MAXIMA-2M1`|5|`d0ea4ff60d59e858bed8625cf7bdb692e69a521ac0b1e4323bfa0243154d4d6f`|
|`Q-CAG-HALF`|2|`dccd5277f7b0c1bb4dcac17287010f1d012bb40c6244c51f24808c1519a4b5ea`|
|`customer-attraction/arbitrary-root-four-suffix-original-attack-and-entire-rational-records`|1|`f949a78ec9bbeb37285bcb772c6c81dfd6204cd63f3a3f23598e7bcc5f4dbf5e`|
|`customer-attraction/positive-depth-root-regret-cones-230-rational-certificates`|1|`1019a86335878664598e586625fdd0e8bee63d3863bf4fe946105da93701056d`|

## 2. 实际读取范围与证据归属

本预读者亲自完整读取：核心 Markdown、共同目录完整历史模型、原始 `tax_probe.py` 全 41 行、`audit_source_contract.py` 全 137 行、透明记录器 `run_original_once.py`、证据 README、manifest、execution-scope、execution、self-check；`exact-audit.json` 的全部顶层合同及全部 15 条精确记录，包含全部稀疏原始权重、非零乘子（原行号、历史、替代动作）及各 63 项余项。gzip 证据已实际解压并检查解压字节 SHA、结构、全部输入类型/seed、策略与矩阵尺寸、LP 记录和恢复字段；没有逐项重新审计 97902 个矩阵系数，也没有把解析/读入大 JSON 冒称新数学认证。

本预读者还完整读取 CA-STRATEGY-CONE 四定理、剩余收益税定义、全称终局税候选的两种搜索正文、ENT1/SAIC 同一性正文，以及后来发现的两个 230 对象的完整正文及各原攻击程序。CA-DISJOINT 本次亲读当前精确范围与锐性章节，没有声称复审其所有动态删除证明。根税反例全文、Q 全文与 ENT1 探针全文由支持子代理读取；本预读者亲自核对了根税登记合同、同输入身份与核心正文中的静态量。三个相关 canonical 边 JSON 已由本预读者全文读取。

成熟原运行的身份由原证据承担：未改原 main 一次、optimize 一次、terminal 216 次、LP 15 次，全部 success，约 6.952439421 秒；独立成熟标准库审计为另一既有事件，原 helper/LP/规范调用均零，重建 97902 个 Γ 系数、945 个成本系数，核 23310 条新原始点 IC、1554 条七客户点 IC、945 个对偶坐标。**这些是成熟证据原作者的工作，不是本次重跑。** 本次只作短 Fraction 代入和下述解析推导，并作两个保存动作表的精确身份比较；未导入或运行原探针、审计脚本、旧 LP 或 SPE 求解器。

核心六个登记引用的当前字节 SHA 均匹配：

|文件（均在 clone 内）|SHA256|
|---|---|
|`archives/customer-attraction/state/程序/完整策略客户锥的终局税探针--程序.md`|`eb2a26f26d4862ec891544404e5b722eccee24b764be9de8e03d564ab3cdac95`|
|`archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md`|`cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88`|
|`archives/customer-attraction/tools/evidence/terminal-tax-fixed-policy-probe/exact-audit.json`|`52ba6139d795a5b7ad8de0bd52e4dd20c1b4db1f47aef147129d9b4532e25b94`|
|同目录 `audit_source_contract.py`|`909894cda9b3d8836c89aa5aeb9b2c2fb7a3891e2592435ddd0e8e741513593f`|
|同目录 `replay/capture.json.gz`|`822bc77673cf4af08206acf04a91f588db7f10e4ea61bcf0ce8effbfc9d1eeae`|
|同目录 `original/tax_probe.py`|`8f72ad4dc8464ef17883bce8f273faefe55152dd31b35aeee136c8bcf3579e21`|

gzip 为 46106B，解压 3482470B，解压 SHA `53d1dcd0ab3ceb22baa75e1e2829c952f2d91496647ba1c799f7be13c41a3252`。成熟 manifest/self-check 内一些正文与共享定义 SHA 是当时打包版本，不能拿它们替换当前 registry 的引用；核心证据的当前绑定和旧事件身份须分别保留。本次未发现核心当前六引用缺失或 SHA 过时。

## 3. 固定策略、模型与真实 IC

模型为有限不同单位客户、六个共同**标签** 0…5（A…F）、四名单位提供者依次观察全部有序历史各选一次；每客户价值在全部终局覆盖者间均分。允许空主题、同覆盖异标签、重复选择、零客户与弱平局。非空兴趣型 M=1…63；无兴趣零掩码客户可以删去。

固定 seed 为 `{1:12,2:8,4:4,8:8,17:6,33:6,20:3,36:3,49:6,50:2,52:1,56:2}`，共 61 客户。它不是 RNG seed。\(\sigma(h)=0\) 对所有深度 0、1、2 历史成立；深度 3 动作按这个**固定旧 seed** 的精确末位收益最大化，平局偏大标签。动作图先固定，之后换重数 x 时不得重新算末位最佳回复或改平局。成熟审计使用的同一闭式身份为：深度不足 3 或 h 中 0 的个数不超过 1 时取 0；否则若 h 含 5 取 4，不含 5 取 5。

总动作数 \(1+6+36+216=259\)，43 个早期节点恒 A，216 个末位节点固定。root 叶固定为 AAAF。对任意 h 与替代 a，end(h,a) 是强制该动作后沿**同一个原策略在改变后的历史**完成的叶，不能冻结原尾，也不能把历史商成计数策略。

记每类型的终局覆盖次数 c_M，逐位置计重复行动。规定收益减真实偏离收益给

\[
\Gamma_{h,a;M}
=\frac{1_{\sigma(h)\in M}}{c_M(\operatorname{end}(h))}
-\frac{1_{a\in M}}{c_M(\operatorname{end}(h,a))}.
\]

零分子取 0，非零分子时当前行动确在对应叶中，分母至少 1。全部 1554=259×6 行中有 259 自身零行、1295 非自身行；63 列，97902 系数。各玩家每条路径只行动一次，因此全有序历史逐动作 IC 与完整纯 SPE 等价。CA-STRATEGY-CONE 给出的准确锥是 \(D_\sigma=\{x\ge0:\Gamma x\ge0\}\)。这是全重数锥，不是只检查原 61 客户或某个有限样本。

CA-STRATEGY-CONE 的完整量词为任意固定 m,p、任意形式完整 σ，构造有理锥、福利截面 \(W=1\) 的紧性和固定规模有限达到性，以及逐坐标对偶合同。它没有给本 σ 的具体 1/35，也没有给全部 σ 的税付款。当前探针优化使用 **T=总质量=1**，不是该一般定理中常用的 W=1 截面。对 T>0 可齐次转换；全兴趣型质量 1 为非空性见证。零质量单独为零，无需除 W 或 T。

## 4. 十五精确对偶怎样覆盖全部比较

定义 \(w_M=1_{c_M>0}\)、\(t_M=c_M/(c_M+1)\)、\(o_{J,M}=1_{M\cap J\ne\varnothing}\)。固定 J 的成本行

\[
q_J=w+t-o_J,
\quad \min\{q_Jx:x\ge0,\Gamma x\ge0,\mathbf1x=1\}.
\]

原 SciPy 约束为 −Γx≤0；其不等式边际 y≤0，故 λ=−y≥0，等式乘子 ν 的符号保原等式方向。成熟精确证书逐 63 坐标给

\[
q_J=\nu_J\mathbf1+\Gamma^\mathsf T\lambda_J+s_J,
\quad\lambda_J,s_J\ge0.
\]

于是所有归一化锥点有 \(q_Jx\ge\nu_J\)。匹配有理原始点又满足所有 IC、总质量 1、成本等于 ν，因此每个值是精确最优；float success、有限 no-hit 或单个正余量可行点都不能代替此对偶身份。

|四标签支持 J（零基）|ν_J|
|---|---:|
|0123|1/35|
|0124|3/32|
|0125|3/32|
|0134|3/32|
|0135|3/32|
|0145|3/32|
|0234|3/32|
|0235|3/32|
|0245|3/32|
|0345|3/32|
|1234|1/35|
|1235|1/35|
|1245|91/1030|
|1345|91/1030|
|2345|91/1030|

静态四槽比较允许重复、也允许不足四个不同标签。任意这样的元组的不同标签支持大小≤4；因目录有六个标签且覆盖质量非负，可将支持补到四个不同标签而不减覆盖。恰四不同标签又可作为合法四槽，因此 \(\operatorname{OPT}_4=\max_{|J|=4}o_Jx\)。这只对**静态覆盖**作支持扩张，不能去重实际行动的分母计数，也不能删偏离历史。

对全部 15 个 J 有 \(q_Jx\ge T/35\)，取覆盖最大 J 得核心结论，T=0 时直接为零。它量化所有非负实重数；整数点是不同单位客户，非零有理点可清分母。并未量化其它 σ、其它人数或其它目录规模。

本次短 Fraction 例核仅取第 0 份证书三个坐标，未复审全部身份：M=2 时成本−1，\(1/35-121/210-19/42=-1\)；M=49 时成本4/5，ν 加原正乘子对应的 1/4 收益差恰为4/5，s=0；M=63 时 Γ 坐标均0，\(1/35+27/35=4/5\)。这些短代入核对了符号与行的语义；全部 15×63 身份仍归成熟独立审计。

## 5. 七客户点、全历史资格与锐性

原 main 打印 `{2:1,4:1,8:1,49:4}`：B/C/D 各一单位客户，四客户喜欢 A/E/F，T=7。沿同一 σ 实际 AAAF，四人各从大块取得 1，W=4；大块负载 4，其余未盖，\(\tau=16/5\)。ABCD 覆盖全部七客户，故 OPT=7。

\[
W+\tau-\mathrm{OPT}=1/5,
\quad (W+\tau-\mathrm{OPT})/T=1/35,
\quad (W+\tau-\mathrm{OPT})/W=1/20.
\]

成熟独立审计已核全部1554 IC及15静态比较，minΓ=0。另可直接解析其完整资格：σ 在每个历史均选择 A/E/F 之一，它们在此点同覆盖。历史中已有 b 位选择大块，尚有 r 位含当前；按 σ 后来都选大块，当前得 \(4/(b+r)\ge1\)（b+r≤4）。改选另一大块标签同收益，改私有单例收益至多1。因此全部有序离轨历史 IC 均成立。此为本次短解析说明，不是新全树程序审计。

点达到质量归一化下界，故1/35对该 σ 全锥是锐值。它是正余量，既不是全税反例，也不是half反例；单点的W归一余量1/20不证明整个锥在W=1上的税余量锐值为1/20。大块4加三私有块属于已有 CA-DISJOINT 的 m=4 锐性族；同覆盖 A/E/F 标签仍须保原动作域。

## 6. 从税证书到 7/4：解析导出、显式转换及去重

令 O=OPT4。因为任何静态并集不超过全部非空型质量，O≤T；因实际负载≤4，逐客户有 \(\tau\le4W/5\)。核心给

\[
\frac{36}{35}O\le W+\tau\le\frac95W,
\qquad O\le\frac74W.
\]

W=0时，原正余量与非负量已迫T=O=0，不作比值。七客户点 T=O=7、τ=4W/5及税余量同时取等，因此这个固定完整策略锥的福利7/4也锐。

Root 提出的证书转换已由本预读者逐式核对。对固定 J 设

\[
a=W+\tau-o_Jx-T/35,
\quad b=4W/5-\tau,
\quad d=T-o_Jx.
\]

则

\[
\boxed{\frac74W-o_Jx=\frac{35}{36}a+\frac{35}{36}b+\frac1{36}d.}
\]

原15份税对偶可直接转换为全部15个福利比较的非负对偶：

\[
\frac74w-o_J=\Gamma^\mathsf T\lambda'_J+r'_J,
\quad\lambda'_J=\frac{35}{36}\lambda_J,
\]

\[
r'_J=\frac{35}{36}s_J
+\frac{35}{36}(\nu_J-1/35)\mathbf1
+\frac{35}{36}\left(\frac45w-t\right)
+\frac1{36}(\mathbf1-o_J)\ge0.
\]

最后两行逐类型非负：c=0时税容量余项0，1≤c≤4时 c/(c+1)≤4/5；o为0/1。该恒等式是**本次Root与预读者互核的解析转换**，不是成熟15税证书原本已经保存的福利目标，没有运行新对偶审计。

但已有对象已覆盖此福利结论：

1. `customer-attraction/arbitrary-root-four-suffix-original-attack-and-entire-rational-records`：FREE-ROOT，无根IC；只保四份指定后继策略的全部正深度真实IC。root_tax_failure族有90=6根×15支持记录，全部目标 O/W 上界≤7/4，且根0/4/5的若干比较达到7/4；这不是仅根A的结论。
2. `customer-attraction/positive-depth-root-regret-cones-230-rational-certificates`：同四份正深度后继，根改选的真实收益差另由非负Δ支配，目标O−3Δ，root_tax族90目标最大7/4。Δ为同一后继菜单的真实根regret上包，最优取真实δ；完整根IC下δ=0，可取Δ=0，所以也推出本完整σ锥福利界。

两个原程序均对actual_root逐0…5枚举，只改空历史动作；正深度Γ由全部非空h重建（不能从去重全Γ中简单删根行）。FREE不含Δ；paid的Δ列和−3Δ不可互删。两份230结果中的其它三个输入与本核心无关，不能把同数量或同第一族常数当全对象等价。

**策略同一性已精确核实，非凭文件名。** 当前税 gzip 保存259动作，与成熟证书 `archives/customer-attraction/tools/evidence/latest-net-and-owner-suffix-audit-primary/context/evidence/certificates/customer_attraction/root_tax_failure.json` 的259个 history→action 完全相同，全部258非空历史相同，空历史都取0。该策略文件 SHA为 `59fd58d85a3c3b989837467eb3523286d1f5ee529b0f119cd4d263bef6984111`；FREE对象的 `input-full-reading.txt` 明列所用同SHA，paid原报告/合同亦绑定同SHA。这里只比较保存动作，不重新算收益或矩阵。

因此本完整IC锥包含在FREE正深度锥的root0子域中；未证明包含严格。税导福利证书与已有FREE/paid福利证书是不同证明、不同归一和不同根条件下的关系，不能据此反推FREE锥的质量税余量1/35。现有福利对象已足，新增独立福利身份会重复结果。

## 7. 全称终局税、前缀根税与 ENT1 的实际逻辑

全称终局税对象 M21 的量词为任意m、任意有限标签目录、每份完整有序历史纯SPE：\(\mathrm{OPT}_m\le W+\tau_{\rm full}\)。它仍open。当前核心只覆盖m4/p6的一个固定σ全部重数，虽强于有限搜索，但没有支付其余σ或m/p。CA-STRATEGY-CONE 的固定规模有限枚举表述并不替代缺失的全体证书。

税定义区分实际前m−1槽的 \(\tau_0(c_{<m})\) 与全终局 \(\tau_0(c)\)。旧61客户同σ actual AAAF，W38/OPT61；前三槽税45/2，W+税=121/2<61。全税却为271/10，W+全税−OPT=41/10>0。前缀税失败不反全税；两个式子不能互借失败或成功。

ENT1令 \(J_T=\sum_{x\in T}1/(1+c_x)\)、\(R_0=\sum_{c_x>0}1/(1+c_x)\)、\(M_1=\max_TJ_T\)，且 \(\tau=W-R_0\)。ENT1为 \(mM_1\le W+R_0\)，与SAIC \(mM_1+\tau\le2W\) 逐式同一。静态覆盖给 \(\mathrm{OPT}\le mM_1+\tau\)，所以ENT1若成立足half；不能把这个上界倒推成对M1的预算。

成熟十三人同一完整SPE有W33、OPT36、R0=359/66、M1=3，ENT1超额37/66>0，故一般ENT1已假。该点全税余额却为 \(2W-R_0-\mathrm{OPT}=1621/66>0\)。这直接说明某点满足终局税付款也不蕴含该点ENT1；本固定锥正税余量更不可能支付全称ENT1。当前七客户点ENT1反而成立：J=(4/5,1,1,1,4/5,4/5)，R0=4/5，4M1−W−R0=−4/5；这只是一点。旧61点的同项为−129/10，也只是一点。两者不是整个固定锥的ENT1证书。

## 8. Canonical 去重与真实可写关系

只按当前 `registry.edge_files` 的2309个唯一路径读取/检索，未将盘上全glob当现役。支持子代理对canonical全文检索核心ID、核心中文标题及 `terminal-tax-fixed-policy-probe` 均零命中；`1/35` 唯一文字碰撞来自无关两人价反族的1/351。此结论只表示未发现现役同核心边，不能表述为数学结果新颖。后来本预读者按同一canonical清单查两份230对象端点，也没有命中现役边；registry对象本身却确已存在。

亲读的三条可复用现役边：

|canonical path|SHA256|实际范围|
|---|---|---|
|`map/edges/customer-attraction-3a-3a-d2d520d432eef77d/terminal-tax-load-cap.json`|`ec513beaaeb88b4b8883c8b7a25eff0d51623998a3e3ecb17b6692e6ff7a9d1d`|税定义→M21，accepted contribution，仅τ≤mW/(m+1)及付款若真后的因子；OPT付款仍未付。|
|`map/edges/customer-attraction-3a-3a-c986a138e6639b6f/thirteen-spe-implies-unscaled-ent1-saic.json`|`b7eb24be3bec39308944f17b088fa87cc378ca54b7e8fee1bf9f9fce1628606c`|十三人具体完整witness→M05，accepted whole_result，完整支付ENT1/SAIC反例及别名同一性。|
|`map/edges/customer-attraction-3a-3a-6d46bb1ce522a6d1/fixed-policy-matching-certificate-gives-nine-fifths.json`|`05443e58e018ace1c6c328b7514e2901d2bd864ab46b2270e59e134b22937633`|CA-CONE加指定五人七标签原始点/六乘子→固定(σ,J)9/5精确最优，whole_result；不是本σ、归一或常数。|

正式worker可选择的准确关系，不在本报告实际写边：

- **CA-CONE→本核心的承重贡献**：解释全有序真实IC锥与非负对偶付款，remaining明确15具体身份和七客户锐性由核心成熟证据承担。通用锥定理单独没有1/35。若要仿既有9/5边写整条specializes，必须将本固定输入、全部15匹配证书、静态支持完备性和七点完整资格都明确附证支付；只写“套锥定理”不能whole。保守贡献已足，不为linked强造整条。
- **本核心→M21 accepted contribution**：result精确为该m4/p6、原σ、全部63型x≥0且Γx≥0的 \(\mathrm{OPT}_4\le W+\tau-T/35\)。remaining为其它σ、其它m/p的全称付款。不是M21整条，也不是只有“有限支持”。
- **FREE230→本核心若写逻辑贡献，只定位七客户见证的OPT4=7子步骤**：核同一正深度动作身份及root0后，FREE界在已认证七客户点W=4给OPT4≤7，而ABCD覆盖七客户给OPT4≥7，故精确支付核心登记中该见证的OPT4=7。remaining为该点其余已登记量、完整IC资格、整个固定σ锥的税余量1/35及全部15税证书，均须由各自成熟证据另外承担。整个本σ锥的福利7/4不是当前税核心的登记结论，不将它写作FREE230→税核心的contribution.result；两份230与全锥7/4的比较可保留为另一证明的支持说明或语境，不强加逻辑边。
- **paid230→本核心若写逻辑贡献，也只定位同一七客户见证的OPT4=7子步骤**：该点完整根IC允许取Δ=0，paid界给OPT4≤(7/4)W=7，再配ABCD覆盖七客户得等式。remaining明确保留整个锥的税余量1/35、15税对偶及该见证其它量与资格的独立证据；不能由福利界反推税付款，也不能把−3Δ删去后授予FREE整域。整个本σ锥的福利7/4比较只作支持说明或语境，不作为该税核心的额外contribution.result，不另造福利身份。
- **本核心→Q的half贡献**可准确写固定σ子域的7/4保证；若与M21贡献重复，可只留在说明，不必再造边。
- **CA-ROOT→本核心**适合cites/sourced_from语境：同seed与同动作图来源，不是根税失败推出全税正界。**CA-DISJOINT与核心**可写七客户锐性族的语境或确切局部贡献；核心整个锥不满足不交假设，不能将两整条定理互推。**核心与ENT1**应说明预算不同并复用已存反例边，不画无根据的正向逻辑边。

## 9. 必要 read-add、原文SHA与未付范围

正式处理本核心时，优先追加两个新发现、与同σ福利去重直接有关的只读对象：

1. `customer-attraction/arbitrary-root-four-suffix-original-attack-and-entire-rational-records`；
2. `customer-attraction/positive-depth-root-regret-cones-230-rational-certificates`。

若写锥承重或税候选贡献，再加CA-STRATEGY-CONE、M21；若写Q贡献再加Q。税定义、CA-ROOT、CA-DISJOINT、M05按实际比较端点或必要语境加共享只读。deferred列表不是自动完成read-add，也没有替代正式worker的完整阅读责任。本报告没有调用read-add或修改任务。

比较原文当前SHA：

|原文|SHA256|
|---|---|
|`state/定理/固定完整策略的客户重数锥--定理.md`|`ae4bcfd424eca8d4e3d79965f72182c0b2c8eefb72e74b44c2521b519f7aad39`|
|`state/程序/终局负载税两种搜索的原始合同与有限阴性--程序.md`|`0581cfff731758cfa91954e94587c28e4f263dc2bc9dd04b81d5dd466c80dfa1`|
|`state/审查/实际终局插入预算与未缩放税桥的同一性--审查.md`|`a57391ef0955e4fac8a7b49ebde98deadbc7c7a668f804ca2b0090562d30fd9f`|
|`state/定义/固定背景剩余收益与税--定义.md`|`c752babf29ecf272b564fe9ff9883c77dcbf6d7fc5e3e501321fab8c5237b4ee`|
|`state/反例/四人实际根总税--反例.md`|`2efa02ba1a7186cf23fcc29e0f70f6cbeb36ce5db6614960091b3233e5b5aab4`|
|`state/定理/不交极大主题锐福利界--定理.md`|`73ee40ebc928e90365b86c776677e9acabd8445d5cb461c0675af50e77fdaac8`|
|`state/程序/任意指定根四后续策略锥的原攻击与全部有理记录--程序.md`|`939efd90923cc30640c3f69dfe86051570aafc702bc9506592e8c5336c0b7b9f`|
|`state/计算/正深度根遗憾锥的二百三十份有理证书--计算.md`|`e04c918a0319c4c1d7bf89d0109b978e46ac9fc38979f8ce7ce3b0ab841fb22d`|

表内相对路径均以 `archives/customer-attraction/` 为前缀。FREE成熟原报告SHA为 `df987b3c4bc28f6b074d77788c9ce901ab2ffa0f52682f216fcb382d1c6b0cf5`，原攻击码SHA为 `cb3b9878ba1a4d6192bb7583d76c913b95dcf9a0b303159729223288e43a159d`；paid原报告SHA为 `8440166fc55f8974f4e5c65e6dc6a960df6af4c0b4c9fb43fab171f2019cc732`，原攻击码SHA为 `5d055514b60fd8e3e92076c23e36142253bb3d62bbf2d82dcb983c7e1a56f7ef`。本次只定向读其原合同/保存输入和相应第一族结构，没有复审两套全部230份系数证书，不冒称新PASS。

未付范围保持明确：一般全终局税候选、所有完整σ、其它m/p、FREE的任意后继策略、一般ENT1或六人half都未由本次得到；本策略锥的ENT1上界也没有由15税对偶自动支付。成熟15税对偶归同一σ，不能移给调用者抽样的不同σ，即使它也出现1/35可行点。正式任务的认领、read-add、边绑定、coverage与交付均留Root按实时状态安排。本报告在保存后冻结，不是正式主覆盖。
