---
id: cag-petal-weak-iid-three-source-proof-and-replay-contracts
kind: review
type_tag: 审查
title: 多花瓣弱iid原稿的三方证明与运行合同
status: 五份主稿完整实读及全仓比较完成；actualclaim与owner/SHA核验通过
summary: 作者7482B、独审7943B和父审2037B共享同一完整SPE族，但短利润切口、窄根覆盖证书和无限族覆盖证明并非同一审计；精确复用现有m20与53/100成功，新运行只核独审独有有理比较。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d321c149379b425493c5e8a5e03c6f39/security/weak_iid_bridge_counterexample.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d321c149379b425493c5e8a5e03c6f39/credible/weak_iid_independent_review.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d321c149379b425493c5e8a5e03c6f39/parent/weak_iid_parent_review.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/README.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round4_security/README.md
---

本次五MD共28379B全部读完、各size/SHA256/Git blob SHA1核验；没有因原稿曾作旁读就先记primary完成。原源均为两个冻结分支同字节版本，rawsource保原路径/身份/程序名，不删失效历史状态。原稿“blind”“作者/父独立重构”保为**历史自述的审查关系**；当前已读三稿及前后修订，不能自称未见证明，也不能把本轮多次阅读当新增外审或新颖性认证。

## 三份证明逐项对齐

| 对象 | 7482B作者 | 7943B独审 | 2037B父审 |
|---|---|---|---|
| 实例与OPT | 任意m≥2,J≥2；W2m、OPT2m+min(J,m−1) | 同族，J固定100，策略证明仍只需J≥2 | 同一实例与OPT；明确不是总客户 |
| 全历史策略 | 根A；中间B；末位按small次数及唯一small类型 | 先只见构造后从定义重建同四类；不同花瓣可选最小/循环 | 作者正文前按构造重建四类，再读稿 |
| 唯一对称iid Nash | 零A、全部花瓣正且均分、B正、单调唯一根 | 独立逐步排缺支持/非均匀，给完整覆盖Z式 | 采用单调唯一内根给Nash，不声称重建所有非对称均衡 |
| m20精确证书 | r̄25/27、F<−13/13500、利润余量[7−20007(2/27)^20]/500 | 窄括号92579/100000<r<4629/5000，覆盖>8209/200、弱余量151/8000；后读作者并核其更短证书 | Fraction重算作者25/27短证，不应冒称核独审窄括号 |
| 每m≥41 | 利润切口1−3/(2m)，Am−2m/(m−1/2)>1/m²，几何小尾被压住 | 先同一根上界，另证根>1/2，逐core/B漏损和私有覆盖得到Z>2m+823/800 | 复核作者利润身份、尾界与严格Taylor常数 |
| 真静态背景 | Q₁,B^{m−2}，查询A/B/Q₁/其他Q为1/2/3⁄2/2 | A,B^{m−2}，查询A/B/任意Q为1/2/2 | 用作者背景；都只得v_m≤2，不声称取等 |

作者策略穷尽所有有序历史，独审同一分类能证明完整SPE；不靠m20的有限状态检查代替量词。私有重复只会降低小主题收益，m2唯一Q中间节点不出现，因此m−2分母不在m2被使用。J1缺另一花瓣，不在范围内。两静态背景都合法且不观察查询，不能误解成按查询另挑竞争者。

作者m20和全m≥41利润证据已完整保存于[既有反例](../反例/独立同分布福利支付--反例.md)，本次作者/父的核心数学可重复路由该对象。独审新增覆盖论证与窄根比较写入[自足覆盖式证明](../证明/花瓣弱iid分离的覆盖式审查证书--证明.md)。根9824B与安全1093B入口的全部工作分支/版本状态，另写[接续账本](../资源/末位标量与索引必要行的接续版本账本--资源.md)。不是把五source都压成一句已知反例。

## 原审计、成功复用和新独有运行

原作者weak_iid_bridge_audit.py称展开m20/J100的140名不同单位客户，按完备状态分类核全部可区分偏离类、全部102静态查询、有理切口、二项式恒等式、根区间和统一常数；没有枚举102^{19}个完整历史。独审audit_weak_iid_independent.py称J2/3、m2…6展开全部有序树，再Fraction核窄根和有理常数，不导入发现器/规范solver/verifier。前一个是压缩分类、后一个是小参数完整树，不能因“精确”就合并动作数。当前无法读原py/json，不虚构小树合计节点或比较数。

安全helper只查三个**首次**必要本地blob：作者3592B py、独审2696B py及2371B JSON，全部缺；精确ID/size/SHA见[依赖清单](../../tools/evidence/weak-iid-original-reviews-and-research-ledger-primary/dependency-safe-local-export-manifest.json)。没有网络/认证/lazyfetch或缺件重试。根安全子入口其余旧GX缺件只引用旧记录，不再找替代凭据或拉取。父2037B没有邻接独立weak审计文件，不能把同目录另一个强iid父审当弱iid代码。

已有成功的两个不同输入版本已核原代码、对应JSON和SHA后复用：

| 现有程序与输出 | 实际已核合同 | 本轮次数 |
|---|---|---:|
| continuation-security/check_iid_examples.py + replay-iid.json | 八客户84比较/安全双证/Q[t]；m20/J100的25/27短证；全部m≥41所用统一常数 | 0重跑；full-history家族仍由解析文字承担 |
| common-iid-mixture-and-petal-threshold-primary/check_new_petal_threshold_certificates.py + new-petal-threshold-certificates.json | 不同参数切片m=J100、每m=J≥53的两个多项式/移位/Taylor和切口 | 0重跑；不冒本稿m20/固定J100的同一数值证据 |

**旧m100输出有一项字段勘误。** 第二组固定m100块先令s=31/2000、t=1−s=1969/2000，F100/G100及Taylor都在这里正确求值；后续for m in (53,100)复用t，末次t=197/200，最终写JSON的new_fixed100.t于是错标197/200。旧正文切口1969/2000正确，旧输出原字节保留，不能称其每个字段均正确；该元数据错误不影响已算固定100值及189/2000余量。精确路径/旧SHA/代码赋值与最小future变量改名建议见[独立metadata erratum](../../tools/evidence/weak-iid-original-reviews-and-research-ledger-primary/prior-success-metadata-erratum.json)。本轮不改旧文件、不重跑成功入口。

复用的是这两份实际成功、输入与实现均可读的exact版本，不是凭“旧source称审计通过”就完成原脚本认证。首份既有程序仅枚举八客户完整树，不会把作者原1540状态/4738比较或独审J2/3小树的原运行据为本轮；第二份也未新枚举花瓣完整树。

本轮唯一新增[标准库入口](../../tools/evidence/weak-iid-original-reviews-and-research-ledger-primary/check_independent_coverage_certificate.py)一次成功、0失败，仅核7943B独审尚未在上述成功输出出现的窄根符号、覆盖>8209/200、151/8000及823/800>82/81。输出全部Fraction，无根求解、浮点、solver、原CLI、旧25/27或53/100重跑。原稿普通近似Z20约41.0457919727只作定位，不作严格证书。

## 不可升级的结论和仍可复用的接口

静态定理m v_m≤Z_m及OPT_m≤(2m−1)Z_m/m解释弱桥为什么足以推出half。一个完整SPE违反它只否这个辅助桥；本族W≥m v_m、OPT/W<3/2，明显满足half。弱iid失败也不否[弱CCE候选](../候选/较弱CCE福利桥的占用LP表示与边界--候选.md)：本族有PNE Q₁B^{m−1}，福利2m+1，故(1−1/(2m))C_m<W。共同iid及latent混合失败不排不同边缘product背景，更不排所有静态安全对偶。

m20/J100与每m≥41固定J100并不是新实例；m=J≥53、m=J100是另参数版本，最早充分阈值非最小阈值。三方审查都没有外审或新颖性认证。一般六人/全目录half与真正聚合静态安全支付仍须新的真实跨分支预算，不由有限精确值、势最大者或minimax存在自动闭合。

当前包在独立stage，完整原claim及本5子集/owner/SHA已核，语义receipt可供Root先推正文再登记；worker没有共享Git、claim或done操作，成熟交付本身不称已推送成果。
