# Cartesian 登记定向刷新：全参数正文未变，旧关系保持

本包为第三阶段3A，沿Boss6，任务 `boss6-cartesian-peer-refresh-repair-f029083d44dd502c`，替代 `customer-attraction-3a-3a-90ada1c6e7bcfa7d`。本轮不是全部历史证据重新审计：实读当前26个端点的陈述、量词、条件和正文引用，读旧任务、receipt、9条边、两份独立数学审计说明和旧review；旧ledger按全部路径、区间及阅读等级恢复。新全文审读限共同模型、E/J定理、P1–P4定理、修订Cartesian反例和未变的共同价格补偿候选。其它成熟正文按未变SHA及旧实读成果复用；未取得旧scratch预研文件，未冒计旧读者或原作者程序运行。精确路径及SHA见reading-ledger.json。

## 唯一源变化及其实际作用

14个核心对象记录均未变。26个任务输入中，只有只读端点 `customer-attraction/cartesian-efficient-factors-welfare-counterexample` 从旧pin `7c81389f0d5158b6073c91f940a64e429a95d8c4a120ba358f24e096bfe39734` 变为当前v2 pin `7ff89d8baec9d48c8ed5084a878e5dbbc5aaf6549fe061845deb7952d4996d94`；当前全文SHA为 `4a107a28ae3d2dd8aa8d67a1f6e72359936003a1ee36002916b7e9d7a25091b6`。最后核对旧reading-ledger的该页记录，旧worker实读1–122行的完整正文SHA也恰为这一值。因此实际变化是登记对象记录修订，数学正文没有变化；旧worker已经读过这份全参数证明。本轮按当前v2已证合同重新核对其量词、完整推导和旧关系用途，不把既有证明冒作新发现。七组原程序重放只是原作者已保存的有限证据，不是本worker的新运行。

当前正确量词是：每个整数 `q≥a≥1`，三名单位提供者，三行各a客户与两色各q客户，共 `3a+2q` 客户，六个真实不同的Cartesian标签。此族不是固定八客户实例；本族最小a=q=1为五客户，a=1,q=2为七客户。八客户三人强iid反例是另一星核花瓣目录，不能以客户数或同名机制混并。

对所有43个有序决策历史，现行登记源给同一固定策略：首人(0,0)，第二人见(i,c)取(i,1−c)，末人取最小未用行；过去同色时取另一色，异色且同行时取首人的色，异色且异行时取第二人的色。末人未用行得a，已用行至多a/2；过去同色取新色得q而旧色q/3，过去异色两色均q/2，故各末节点都联合最佳。第二人指定同行异色得a/2+q；同行同色仅a/2+q/2，任一异行行动得a+q/2，因此所有真实联合偏离增益至多(a−q)/2≤0。根每个强制标签都由同一策略续成收益(a+q)/2。该完整证明支付全部历史，而非冻结实际后继的静态NE检查。

actual为 `((0,0),(0,1),(1,0))`，收益 `((a+q)/2,a/2+q,a+q/2)`，故W=2a+2q；合法三主题可覆盖三行两色，OPT=3a+2q。单独行游戏中第二人改取未用行得a，重复仅a/2，末人再取未用行，故每份行SPE福利3a；单独色游戏在末人之前或末人时必覆盖两色，每份色SPE福利2q。由此只需存在性便有

`min_joint W ≤ 2a+2q < 3a+2q = min_row W + min_color W`。

不宣称所给joint策略是最差的，不宣称枚举了joint全部均衡。其行投影终局(0,0,1)不是单独行SPE：中间人换行本可增a/2，却触发色坐标的可信末位平局，损q/2。独立变化各个分量的策略与这种依赖其它坐标历史的coupled continuations，具有不同量词。

## ALL whole边仍完整成立

旧 `ca90ad-p1-p3-imply-specified-product-price-budget` 的输入是P1与P2/P3的ALL共同前提，目标是P4自身的条件保持定理。P1给定每个分量的完整SPE，在每个联合有序历史逐坐标跟随各自同一完整策略；任一联合偏离的各坐标收益增益皆非正，故其和非正。它构造指定独立乘积SPE，不分解任意joint SPE。

P2的各坐标边际均有同一总质量t；t>0时 `z_(A1,…,Ak)=prod_j z^j_Aj/t^(k−1)` 同时实现各最优边际，t=0直接取零。因此F_prod(t)=ΣF_j(t)。P3由共同最大点的非负支持斜率给达到的价格下卷积；v=0共同饱和，最大点t*=0时给各坐标至少右斜率再分配剩余价格。所有这些都是菜单优化，仍不受joint策略是否耦合影响。

P4另有它自身的输入if：每个已选分量均满足B_j(a_j)≤W_j，其中a_j=min_i u_i^j。令a=min_iΣ_j u_i^j，逐i有a≥Σ_j a_j；各分量最小者无需相同。B非增与P3可行拆分给

`B_prod(a) ≤ B_prod(Σa_j) ≤ ΣB_j(a_j) ≤ ΣW_j = W`。

最优m查询是质量m的可行覆盖，故 `OPT_m≤F_prod(m)≤B_prod(a)+ma≤2W`，最后用ma≤Σ_i u_i=W。旧whole_result恰保这整条if定理，因此unconditional关系是完整证明目标自身的条件定理，不是把普遍分量预算当成已证。当前反例没有否定旧关系，旧边无需改ID、文字、条件或绑定。

对现行反例族还可直接算价而不用投影均衡。`F(t)=a min(t,3)+q min(t,2)`；令实际最小收益v=(a+q)/2，F−vt在(0,2)斜率(a+q)/2>0、(2,3)斜率(a−q)/2≤0、3后严格负。因此 `B_prod(v)=a+q=W/2`；q=a时整个[2,3]达到。投影自身甚至满足 `B_row(a/2)=3a/2≤2a`、`B_color(q/2)=q≤2q`，只是本族直接计算，不赋予投影SPE身份。共同价格补偿候选的任意coupled-SPE预算仍open；本族的通过不建立普遍定理，也不造成该候选的反例。

真正三人整数静态安全值又是另一个量：均匀六主题查询在行相同/不同的两背景下分别得7a/9与2a/3，在色相同/不同下得2q/3与q/2；对偶均匀取不同有序行及相反色的12背景元组，逐纯query恰给 `v_static=2a/3+q/2`。所以 `W−3v_static=q/2>0`。该query独立的静态背景不同于看完真实历史再续行的σ，也不同于保根完整m槽的额外query菜单。

## 9条旧边逐项处置及whole/step/context

所有旧边的当前端点pin和承重证据均按精确绑定核对，保原作者审读署名；没有新造相同关系，没有将已有边的原程序运行记为本轮运行。

|旧edge_id|实际作用及刷新结论|
|---|---|
|ca90ad-p1-p3-imply-specified-product-price-budget|whole；ALL P1+P2/P3 ⇒ P4自身if定理，推导如上，保持。|
|ca90ad-component-data-contribute-integer-ej-target|step；ALL R7+P1，任意非空整数s,t的固定目标u=((s+2t)/2,same,s+2t)、W=2s+4t、OPT=3s+4t、B_repair=s+4t；任意终局加性不要求前两位SPE。M1/M2及全历史控制器仍由整数定理另证，保持。|
|ca90ad-integer-ej-contributes-dictionary-attainment|step；s2,t1给M=(2,3)、target(2,2,4)、B6+C3=9，除3得x2/3处新预算3。同权旧11/3与旧全局7/2分开；全τ四H、V形下界和唯一性未由单点代证，保持。|
|ca90ad-fixture-contributes-optimal-pastmass-deficit|step；同22客户fixture另取最优HTB，源5=current4+末D输入1；HAD六客户D均匀改标输出2·(1/6)/2+4/6=5/6，缺1/6。一般PAST-MASS由逐客户1+future=c_A−past另证。补AD两券各1/12只是局部守恒，源current同钱包可使AD各13/12；不反cap2或half，保持。|
|ca-r34-bank-minimax-refutes-full-root|whole；每m≥4的同一完整银行σ，min_Q max KQ=2−1/m−1/[3(m−1)]；超根u=1+1/(m−1)，差(3m−1)(m−3)/[3m(m−1)]>0，直接否定B10的∃共同Q，保持。|
|ca-r34-two-queries-refute-full-root|whole；固定两query各半，对全部真实根列的下界4/3+1/(2m)>u，任意Q被同一个query分布分离；不是仅找到一个高值对称NE，保持。|
|iid-star-family-specializes-eight-customer-strong-gap|whole；星族n3/K2特化为八客户完整SPE、W6/OPT8/v44/23，并以根式iid均衡Z3>6给强桥分离；不是Cartesian三行两色族，保持。|
|iid-star-security-contributes-n30-and-true-security-boundary|step；n30/K100的严格弱iid端点及该族W−mv=2m/(201m+400)>0；不从n30外推m20或全m≥41阈值，保持。|
|exact-381-client-saddle-closes-older-menu-evidence-gap|context；同381客户完整三槽菜单的原始/对偶输入补齐，值239604/3169<137是固定节点正校准；不作支持B10全称的逻辑覆盖，保持。|

保根完整菜单要求每列B是沿同一σ强制根后保留该根和全部真实后继的m槽，查询抽样独立于列Q。银行反FM、星族固定σ的正校准、381固定节点证书，均不等于真正静态m−1槽安全值，亦不能把福利非可加性当作它们的推导前提。本次m4短算术独立得Mfull=59/36、u=4/3、差11/36；两query下界35/24、差1/8。程序算术是交叉核数，数学依据仍是上面全列/全历史推导及原成熟证明。

## 14核心覆盖和旧比较保全

新receipt维持9 linked、5 isolated-after-review。M11/R7、P4/P2P3/P1、pastmass/nonoptimal、star、B10由以上8条逻辑边准确覆盖；381 context不增加linked。旧已实读的merge有限核、多源signed债、36客户尾部归一、64人直方图/支持外hub及具名浮点搜索，所有对应对象pin与正文SHA均未变，本轮按旧receipt/review的数学处置复用，不声称新全量读取或运行。

对M9还补核现行反例的准确界：OPT−W=a，最小实际收益(a+q)/2，故 `3 min_i u_i−(OPT−W)=(a+3q)/2>0`，并未反驳逐人净gap候选。对merge的signed债与广播券仍没有同实例、同σ、同source、同context的核映射。36客户theta归一、静态安全v与一般最小价格桥仍分别保域；支持平均的失败不否定所有iid/security；有限浮点零松弛仍无有理对偶或普遍桥。因此五个isolated处置保留。

本任务context_plan没有声明overlap_comparisons，故当前 `closed_overlaps=[]`、`follow_up_tasks=[]`。旧任务中B10/银行低值自洽peer的一项已闭合比较完整保存在旧receipt及新 `carried_forward_closed_overlaps`，不误填成当前未声明pair：旧同一矩阵Jensen下界对每个Q成立并超u(m≥4)，加现有两canonical反证已经闭合，无新3B/3C义务。其数学证据未变，原closure的全文阅读信用仍属于旧worker。

14份旧assets逐项retained且SHA全同：4条旧本包边、5条外部canonical边、2份独立audit说明、旧review/ledger/manifest。后三者是旧任务的历史阅读及绑定记录，不覆盖本次刷新记录；新review/ledger/manifest明确当前输入，保历史没有重复运行或新证明的含义。完整supersession逐项理由见新receipt。

## 交付边界

没有新逻辑边，没有source/registry修改，没有Git、队列、claim/read-add/done或edge-bind写入。仅在本任务write_paths写本次审读及receipt；现有9边可原样消费。Root仍须按当前远端任务definition核receipt，完成其串行checkpoint/push/done。完整资产SHA清单不自引用manifest或receipt，以免hash循环。
