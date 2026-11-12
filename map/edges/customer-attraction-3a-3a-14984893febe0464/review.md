# 同时纯Nash、五人全0完整策略及静态删位平均的比较

本包实际得到两条数学关系。第一，对指定九兴趣型单位输入及其全0实际叶，直接算出的末位最佳回应与同主题根覆盖界给出 OPT₅≤1800，而五标签 {0,1,2,4,5} 的明确覆盖给出 OPT₅≥1800，因而支付该有限点的精确最优覆盖步骤。第二，任意静态纯Nash终局的逐角色静态IC支付最优主题索引的冻结平均 Q≤W；配合对任意确定叶成立的 Q≥OPTₘ−(1−1/m)W，完整推出该模型的静态纯Nash半覆盖，实际得到更锐的 OPTₘ≤(2−1/m)W。

第一条只作指定有限构造的一项局部贡献；第二条支付静态定理的整条全称结论。两条独立证明不互作前提，不把共同模型定义画成逻辑hub。一般顺序SPE的IC不能支付第二条的静态上界。

## 当前任务、对象与实读边界

身份 Boss2。任务 `customer-attraction-3a-3a-14984893febe0464` 当前为 claimed，owner Boss2；本次最终实读的 request_id 为 `5e7217a660ec4e3087831032c0fe40e8`，definition 的规范JSON SHA256 为 `fea698351b9e547b3d1a034176d7aa03dc39d5559cf96aa1811b2c918bcadc9e`。九个 input_pins 均按 `tools/research_runtime.py` 的 pin 算法从当前 registry 对象独立核对一致。

| 对象 | 版本 | registration_pin |
|---|---:|---|
| M-5d3e3db90ead48339c63f8f5debbd4e3 | 1 | 66d8d7da2b147439298a42e13155d5b4b9173e3ca27187da4a108d9c52792f8b |
| M-3a55169b86b64a7a99a13e612a389688 | 2 | c890e5d906328f6a25dab6fe69c85ef056482e2bce48c12e5373d0dc7a6ed3a9 |
| CAG-MODEL | 1 | 3216d1db43ff83e0e0c9cf2479e79611277c9d9291a68e7f9b85ec4bb299dc5c |
| customer-attraction/residual-payoff-tax-calculus | 1 | 779995a2df37d219c501e728531e3ca4b83eaa87e7deff2653d5d66dcd5e89ba |
| CA-SPE-NON-PNE | 3 | f4af450f2a468bb54f1aacb63fa9cab54d95f2daf47af5989c4bdf137083ff0d |
| customer-attraction/unanimous-terminal-root-bound | 1 | a60d79577f6645764740e39f549c7cd0759061aa99b4ff2d2a543a1a89c0759b |
| CA-STRATEGY-CONE | 7 | 291bd4d94e33d40566453a33b5cf07b1c620b77362268417582efecb42b0c4bb |
| B2-STRICT-UNIQUE-SPE-STATIC-GAP-v1 | 4 | 0a7ab130d597bf3224aeb28f74d44c76b1b875dfde1b35d1f548a6032ef7f193 |
| customer-attraction/static-allowance-original-notes-and-finite-search-contract | 1 | 30389930f5358e6b3928bb6a4fe3726e5c7da2e6f1c5690ec6c2d82d2d7c48b5 |

已全文实读两个核心正文、完整历史模型、固定背景税定义、同主题根界、固定完整策略锥的四定理、三客户非PNE正文、严格唯一DAA正文、静态删位原笔记合同及其关联新标签策略资源；另全文读单主题局部余项引理，核对同主题锐界的独立证明。静态核心的绑定唯一标题“静态同时行动的完整证明”完整读取，所在资源其余章节亦已读，未将后面的二分关联模板结论混入该静态定理。

原 m5k7 JSON 的全部字段及2801动作记录已完整解析，下面给出无损动作规则；实读其保存的 `replay/verify_certified.py` 和 `verify_certified.stdout`，但未运行它。静态删位3168B原笔记 `static_allowance_notes.md` 已全文实读，其旧OPEN只表示原稿当时状态；当前正式资源已明确一般SA被十三人反例否定。本轮只使用不依赖均衡的恒等式与平均下界，不继承旧OPEN或有限阴性资格。

没有运行原数学入口、LP/MILP、BI、完整IC审计、全支持/全矩阵扫描或优化器。新执行仅为JSON与字节/类型字段解析、完整动作表覆盖性核对及少量 Fraction 算术。保存的2801历史/16806真偏离成功是原成熟验证事件，不是本轮新审计。

## 指定九型证书：完整规则及有限点

原证书 SHA256 为 `9265ba4df39bde36bfac210f27532fe89fba817df74a4a61853b09c6191afb66`。输入为五名单位提供者、七个标签 T0,…,T6，九个非零兴趣型如下；重数表示互异的单位客户。

| 兴趣标签 | 重数 |
|---|---:|
| {0} | 5 |
| {1} | 200 |
| {2} | 200 |
| {3} | 1 |
| {0,3} | 995 |
| {4} | 200 |
| {5} | 1 |
| {6} | 1 |
| {5,6} | 199 |

总客户数1802，各主题大小为 (1000,200,200,996,200,200,200)。每个标签都有至少一个独占私客，所以七个覆盖两两不同且互不包含，全部是包含极大覆盖；“极大”不表示同为最大大小。

全部动作表恰覆盖有序历史 ⋃_{t=0}⁴{0,…,6}ᵗ，各层条目数为1、7、49、343、2401，总2801；history不重复、无缺失、无越界，所有 action 都为0。这不是从metadata推定的策略压缩，而是全部原动作记录的无损总结：σ(h)≡0。声明 terminal_counts 为 (5,0,0,0,0,0,0)，与该规则的根实际叶 00000 一致。

这份策略还有短的统一全历史解析证明。任给长度t的有序历史，令n_j为此前标签j的次数，r=5−t为含当前玩家的剩余人数。遵从并沿同策略完成，当前收益为

U0=5/(n0+r)+995/(n0+n3+r)≥1000/5=200。

两个分母均在1到5之间。若当前改选3，未来依原策略仍全选0，共享995客的分母不变，故

U0−U3=5/(n0+r)−1/(n3+1)≥1−1=0。

改选1、2、4时收益为200/(n_j+1)≤200；改选5或6时收益为1/(n_j+1)+199/(n5+n6+1)≤200。于是全部有序历史的全部合法动作都无改进，包括离轨、重复与平局。这是从已完整解析规则直接重建的解析理由；没有再次执行16806项审计，也没有给原浮点搜索补全局资格。

根实际全0，五人收益各200，W=1000。更局部地，在实际末位历史0000，留0得1000/5=200；改3得1+995/5=200，改1、2、4、5、6都得200。因此实际末位最佳回应是直接由客户表支付的事实，不以目标对象的“OPT1800”或“完整SPE已证”反作前提。对任意玩家冻结另四人0时面对同一收益表，所以该实际叶同时也是PNE；全部35项含自身静态比较均为平局。这仅是本指定叶的准确资格。

## 局部逻辑边：同主题根界支付有限点的OPT等式

同主题根定理的合同是：任意m≥1、空背景、实际Aᵐ，且只需真实末位在A^{m−1}选择A为最佳回应，即有 OPTₘ≤(2−1/m)|A|。不需要整策略恒A，也不需要先把SPE转换成PNE。

本证书的直接输入事实是 m=5、A=T0、实际A⁵、|A|=1000，以及上节已经逐标签算明的实际末位IC。代入给出

OPT₅≤(2−1/5)1000=1800。

反向选 {0,1,2,4,5} 五个标签：0覆盖自己的5私客及995共享客，1、2、4各覆盖200，5覆盖1私客及199共享客；这些客户块彼此不重叠，合计1800。因此 OPT₅≥1800，得到精确等式。这一证明没有把证书中声明的 optimum 字段当作数学输入。

另一个独立的有限上界核对是：至多五个不同标签必漏至少两个标签，各漏标签至少损失自己的一个私客，故覆盖至多1802−2=1800；重复行动不增加并集。该核对说明指定覆盖数一致，但逻辑边选择同主题定理作为可复用上界来源，不并发制造两条等价应用边。

本边 contribution.result 只为该九型指定点的最优覆盖等式及 OPT₅≤1800 这一步。完整2801节点SPE资格仍由原成熟证书及其原验证合同承担；上节解析重建是比较中的独立说明，不把它冒作同主题定理单独推出的结果。原另一浮点候选的有理恢复 W3/OPT3 是不同端点，本边不支付该恢复、浮点搜索、辅助anchor族或全五人策略的全局上界。第一核心整体已经是 proved，不因本边为局部贡献而降格；remaining描述本边没有承担的其余部分。

## 静态核心：冻结索引平均给出完整另一证明

静态目标的原合同是任意m≥1、任意有限单位客户、有限非空共同标签目录、单位提供者同时选择一次，对每个静态纯Nash终局a有 OPTₘ≤2W(a)。偏离固定另外m−1个动作。主题可空、覆盖可别名、动作与比较主题可重复，平局保留。共同目录和均分收益与删位identity使用的是同一公式；这里无需一份顺序策略，更不需要把静态终局补成顺序SPE。

原核心的直接证明已核：取最优比较主题T_i及终局负载c_x，有 u_i(a)≥u_i(T_i,a_{−i})≥Σ_{x∈T_i}1/(c_x+1)，求和后逐客户以覆盖指标支付OPT。这条原证明有效，不需取全局势最大。新增边给出另一条完整证明，并得到更锐中间界。

源identity对任意确定叶s定义 D_T(s)=Σ_i u_i(T,s_{−i})。对x∈T且c_x>0，c_x名原覆盖者被替换时各得1/c_x，其余m−c_x名各得1/(c_x+1)，合计(m+1)/(c_x+1)；c_x=0时m名各得1。故

D_T=Σ_{x∈T∩C}(m+1)/(c_x+1)+m|T∖C|。

这一步是任意确定profile的代数，无均衡假设。固定任意m索引比较主题T₁,…,T_m（允许重复），均匀排列索引分给角色的冻结收益总和期望为

Q=(1/m)Σ_j D_{T_j}。

每个角色分到每个索引的边际概率为1/m；重复标签仍保留各自索引槽，故公式没有漏重数。令比较并集O、比较重数d_x。O∖C每客对Q贡献d_x≥1；O∩C每客贡献 d_x(m+1)/[m(c_x+1)]≥1/m，因为1≤c_x≤m。因此

Q≥|O∖C|+|O∩C|/m≥|O|−(1−1/m)W。

现在使用目标自身的静态PNE假设。对每个角色i和每个比较索引j，固定另外动作的同一静态IC给

u_i(a)≥u_i(T_j,a_{−i})。

对j均匀平均，再对i相加，得到

W=Σ_i u_i(a)≥(1/m)Σ_jΣ_i u_i(T_j,a_{−i})=Q。

取达到OPTₘ的比较元组，有限非空目录保证最优达到；不足m个不同主题可重复补齐。于是

OPTₘ≤Q+(1−1/m)W≤(2−1/m)W≤2W。

这覆盖目标整条全称结论。m=1时系数为1，实际唯一角色最优故OPT₁=W；上式本身也成立。W=0时同样推出OPTₘ=0，不定义0/0。零客户、空主题、重复动作、覆盖别名及弱平局都不影响逐客户公式或静态IC。源没有需要补付的SPE资格、SA全称不等式、浮点搜索或十三人证书前提。

这里没有反用“每T有D_T≤W”来认定未对称化确定profile为PNE。我们只作从目标已有的每角色静态PNE不等式到总D及Q的正向求和。源中D_T≤W的对称CCE等价解释与这一步相容，但本边不需要CCE转换。全人数SPE的SA已经被否，不影响任意叶恒等式；一般SPE不能用真实偏离IC来代替本节的每角色静态IC。

## 两均衡概念的准确比较与失败迁移

顺序SPE只比较 u_i(a) 与 u_i(a_{<i},T,continuation_σ(a_{<i},T))；静态PNE比较 u_i(T,a_{−i})。若对每个实际前缀、角色i与偏离T，真实分支后缀等于原实际后缀，则两者相等，SPE蕴含该叶PNE。更弱的充分条件是每个真实偏离收益不小于冻结偏离收益，配合SPE的实际收益上界即可。条件的方向不能反写。全树各角色常值是强充分条件，本有限全0策略满足它；一般SPE没有该条件。

另一个特殊接口是空根实际Aᵐ。真实末位IC已经等于该角色的静态比较；共同目录、单位权和匿名均分使每个角色面对同一其余A^{m−1}，所以该叶为静态PNE，不要求离轨整策略恒A。本包的锐同主题边更直接，不借静态half的较弱常数2000。

CA-SPE-NON-PNE的三客户完整表已实读：A={a}、B={a,b}、C={b,c}；根C，第二位在A/B/C后为C/B/A，末位在AA/AB/AC/BA/BB/BC/CA/CB/CC后为C/C/B/C/C/C/C/B/B。全部13节点给完整SPE，实际CAC利润均1且W=OPT=3。中间玩家冻结另两位C时A→B得4/3>1；真实CB后末位按原策略选B，得5/6<1。它精确否定一般SPE叶必为PNE及等收益强化，不否定静态PNE定理。

严格唯一DAA正文给另一更强障碍：三人四标签12客户，全部21有序历史的非自身IC严格、最小余量1/6，反向归纳唯一完整SPE为DAA，利润(4,7/2,7/2)，W11。静态PNE恰ABC六排列、W=OPT12。根D冻结AA改C得13/3>4，真实选C后按原策略得到7/2<4。该完整表对同计数历史恰取同一严格最优动作，故严格、唯一、计数Markov均不足补后缀冻结桥。1215客户满支持与扰动稳健版本按当前正文的成熟证明范围保留，本包不重跑其程序或认证原发现最小性。

两个核心不能整条互推：单个五人完整SPE存在性不推出每m每静态PNE的福利界；静态全称half本身不构造这个1802客户输入、全0策略或W1000/精确OPT1800。新第二边来自任意确定叶的静态删位identity加目标自身PNE假设，而不是把第一核心的有限结果提升为全称。税定义中的非零背景剩余利润R_b不等于根覆盖；税桥反例也不是本静态定理的反例。

## 仅保说明的额外推论：本全0固定策略锥的全J精确9/5

固定本JSON的同一形式完整σ₀(h)≡0、m5/p7，让全部127个非空兴趣型r_B任意非负，并保全部真实有序IC定义的D_{σ₀}。整数点表示单位客户；实点只作齐次优化。每个锥点的actual标签路径始终00000，其实际末位0000的IC是锥约束的一部分，同主题定理因此给所有比较五元组的覆盖≤(9/5)W。原九型整数点已证明可行且达到1800/1000，所以归一截面W1上 max OPT₅=9/5；这不是只固定一个比较J的目标。

实质量的上界可以直接逐型线性写明。任取五个比较标签T₁,…,T₅，允许重复，令b=1_{0∈B}、d=Σ_j1_{T_j∈B}、o=1_{d>0}。令Γ_j为真实末位0000的“遵0减改T_j”单位客户行（T_j=0时为0，重复索引重复取该行）。则

(9/5)b−o=Σ_jΓ_j+ρ_B，

其中 b0/d0时ρ=0，b0/d>0时ρ=d−1，b1/d0时ρ=4/5，b1/d>0时ρ=(d−1)/5，全部非负。与任意非负r内积，Γ_j r≥0就给比较覆盖≤(9/5)W，因此不需把任意实点假称为有限单位客户实例。

W0时直接得全部比较覆盖为0；非空类型各被某标签查询，可知r=0，不形成比值。W>0时除以W保齐次锥与全部覆盖比；有理归一点清有限公分母给互异单位客户，irrational点只保优化域意义。给出的原整数点已支付达到性，不依赖实点近似。每标签正私客还使本点满足七个不同包含极大覆盖，故该受限子域同样达到9/5，但允许任意σ的五人七标签全局问题没有因此解决。

本推论超出第一核心“只断言保存点可行”的陈述，保在support中；没有硬塞其whole_result或contribution，也没有创建新独立对象或为同值制造follow-up。

## canonical去重、重叠及交付范围

仅沿当前 registry.edge_files 的2309条现役清单逐一解析检索端点与精确证书名，没有glob全盘边。新read-add后再次查静态删位源和静态目标端点，只有该源与十三人固定D向量共同推出固定最优计数极值的现役ALL边；没有支付本静态核心的现役同关系。没有现役边以两个本核心为端点。

已完整读以下相关canonical边，精确区分用途，不借他人support充本包资产：

| 现役边 | 精确作用及本包处置 |
|---|---|
| cag-unanimous-terminal-residual-pays-sharp-root-bound | 单主题显式余项推出普遍同主题锐界，SHA c8ccabce90842be03801febf5de4338ec691c9c28b473ca6d6143b785a3e7e6a；本包仅将已证锐界应用于新指定有限点，不重发其普遍证明。 |
| cag-boss4-2fcb-equal-profit-spe-does-not-freeze-cp-successors | CAC纠正共同价格路线的等收益冻结捷径，SHA ff7df8c75f1694b70f0032330fb53ae7fec7c4c9bf431ce3279e1c8aaaf5358b；本包不复制同一价格纠错边，不把静态定理当refutes目标。 |
| cag-fixed-policy-cone-and-matching-certificate-give-exact-nine-fifths | 另一selected_exact完整σ，actual00055、固定J01234的六乘子9/5最优，SHA05443e58e018ace1c6c328b7514e2901d2bd864ab46b2270e59e134b22937633；不能混成本全0策略或扩为旧锥全J。原2801动作和127型对偶未在本轮重新打开，旧边仅供身份去重。 |
| ca-13-frozen-deletion-vector-and-average-identity-to-optimal-extrema | 十三人特定D向量与索引平均identity的ALL应用，得到2002最优计数的固定极值；其目标和本全称静态PNE定理不同，不冲突也不重复。 |

definition.overlap_comparisons 与 definition.context_plan.overlap_comparisons 两处均不存在；comparison_groups为两个singleton，没有已指派follow-up对象对。本包的具体比较已由两条边和本support解决，无需伪造closed_overlaps或另发旧00055全J研究任务。未发现本范围内已付模型映射的跨存档迁移，不为共同SPE/势/因子二名词造边。

最终只交本人两条边、此support及覆盖receipt。Git、edge-bind、edge-check、checkpoint、队列done和共享registry/coverage/integration均交Root串行处理。本worker没有修改原文、原证书、任务定义或他人资产。

## 实际引用文件的字节指纹

| 路径（均为仓库内） | SHA256 |
|---|---|
| archives/customer-attraction/state/障碍/R-3b6b辅助锚点提升与m5k7有限证书边界--障碍.md | b9a8fbed171f2384d990cfb6554ef878d220c796177db2047ca92e08ef01a80d |
| archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md | cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88 |
| archives/customer-attraction/state/定义/固定背景剩余收益与税--定义.md | c752babf29ecf272b564fe9ff9883c77dcbf6d7fc5e3e501321fab8c5237b4ee |
| archives/customer-attraction/tools/evidence/R-3b6b-counterexample-20261031/source/certified_m5k7_maximal.json | 9265ba4df39bde36bfac210f27532fe89fba817df74a4a61853b09c6191afb66 |
| archives/customer-attraction/tools/evidence/R-3b6b-counterexample-20261031/replay/verify_certified.py | 01c5e5b2c15979b3e5b1a4bb95995e20edc556a6139c5c5bfb0f4a1035170644 |
| archives/customer-attraction/tools/evidence/R-3b6b-counterexample-20261031/replay/verify_certified.stdout | 13a1a5fd6b32e908e62264190c79b45f799cf71e22556338e60e3f90e0c33f37 |
| archives/customer-attraction/tools/evidence/R-3b6b-counterexample-20261031/source-manifest.json | 144b4d837873eaf6a8ba44c861dd5845707bcca8612d187c1e34af2f3a2f744a |
| archives/customer-attraction/state/资源/静态势半覆盖与二分关联预算的原稿边界--资源.md | 09c1b1b776374c71f0360d5acecdfbedd5d4adccc9d4eec6d99b41374a289000 |
| archives/customer-attraction/state/反例/顺序SPE终局不必为同时PNE--反例.md | 0879e6843689c4978c3c44a51fe779714ca3b6290cb4778a9243126295203a99 |
| archives/customer-attraction/state/反例/全部历史严格唯一均衡与静态PNE福利的分离--反例.md | 66490ad8e7f940462fb56fd7093921df5844be6539384b76c7a54a3262794d44 |
| archives/customer-attraction/state/定理/同主题终局根覆盖界--定理.md | a52a47cf2b31f3e15124a2146406b5317e33f93a1372f75571619295a2697036 |
| archives/customer-attraction/state/定理/固定完整策略的客户重数锥--定理.md | ae4bcfd424eca8d4e3d79965f72182c0b2c8eefb72e74b44c2521b519f7aad39 |
| archives/customer-attraction/state/引理/单主题实际终局的显式局部半覆盖余项--引理.md | 92bd65b374e1a1138a0c097b9b296f4838c6866a0d0ca88e8b388147ccc97fa2 |
| archives/customer-attraction/state/资源/静态删位宽限原笔记与有限搜索的准确合同--资源.md | 5b4a03208b79bcb8791d8d03da7192cbbf4d10287afacea17f5191e97c75c686 |
| archives/customer-attraction/state/资源/静态删位宽限的新标签策略锥与单纪录--资源.md | 6c0e61041a0886dd38c7b0f6df4ef9356674d04883e53ea91ee9b19037aff988 |
| archives/customer-attraction/tools/evidence/static-allowance-original-notes-and-independent-review-primary/source-root/research/workspaces/customer-attraction/R-d51d7a410c12456aa5c44e84b78708d0/global_proof/static_allowance_notes.md | ea23fdaea943eccfe19dc0d9ecf7159f9c048fb05ee23736b35df7bc8a601500 |
