# 全鲜广播与定义级审计四源核读

四主源为16669字节all_fresh_submarkov_elimination.md、1831字节review_role_price_envelope.md、3098字节audit_fresh_profit_normalization.py、461字节fresh_profit_normalization_audit.json，共22059字节。前三个新取回原件（数学长稿/源码/冻结报告）本批全文实读；1831字节审查复用前批全文实读并核同SHA。缺少副本的三源只用本地Git cat-file读取冻结blob，无Git写、网络或认证；原件均按inventory的SHA和字节数核同。完整source_refs保两个冻结commit/path。

源码没有外部输入文件：所有U/V/background/K有限计数和两层fixture都在3098字节代码内，本批已完整读过这些输入定义。未把“无输入文件”写成缺失依赖。程序只用标准库Fraction/Path/json。

## 实际执行与无重复运行

执行前按完整代码SHA、报告SHA和原程序/报告名查询全仓archives/cleanup及已知external缓存，没有同SHA当前成功run；命中为inventory/claim/候选，不是执行证据。于是将未改代码复制进新的空replay目录，实际执行一次普通Python，assert启用、exit0、stderr空。461字节新报告与旧报告全部字节相同，stdout JSON对象也相同。实际命令、cwd、起止UTC和完整SHA在replay/execution.json。

原程序用out.open("x")，因此任何再次复现必须新建另一个空运行目录，只复制原代码后执行；保存的replay已含输出报告，不能直接在那里重跑。没有覆盖原冻结报告，没有第二次运行，也没有新实现或SPE扫描。

精确有限覆盖：n=0…4的全部U/V子集与background=0…3共1364组；全部K共18724项；Y的3值和e的2值给8184项退款。非零两层fixture给beta=(2,1)、future金额1/2、质量与signed账均1，实际assert beta1>1。它不是CAG实例或SPE证书，不证明原模型cap失败或half反例；程序不动态测试nu=0空行动，零域由数学证明处理。报告明确certifies_global_fee_bound=false。

## 全仓比较与后续校正

本批先全文读长稿§1—10，比较此前已完整读且同SHA保留的SAFE/HIT、仅鲜利润源费用、局部行价格、controlled-positive审查、源时间双重构、变量p/同客户密度及固定P Hall钱包。之后用NET-CANCEL、PAST-DEFICIT、C-LEDGER、COUPON-LEDGER、SLACK-LEDGER、submarkov文件名及代码/报告SHA作全仓文字定位。宽泛v.*chi检索产生无关review/machines词匹配，未据此假称读过无关文献或建立数学关系；精确字面检索另作范围判断。

- 原长稿的完整v分母鲜正边只消去fresh广播，剩C-only X−Y signed迁移；后来的仅鲜利润nu图没有正X/past出口但beta可能更大，两图不合领预算。
- 原长稿全客户升级的past只能actual终点，future仍严格DAG；原§5尚未证明N/e安全非负退券，后续SAFE已证明同context当前整行可退，故新正文明确修正其当前状态。最终共同cap仍未证。
- 同客户NET-CANCEL保客户局部恒等式，先去past；PAST-DEFICIT只剩actual前缀多于off前缀的负载缺额。与跨客户最大标量CLIP不同，不混旧退款与新删边收益。
- 原区间[k,i)、下一代[i,l)只是past差异区间互不重叠；当前whole行在i已收费，下一代past仍可含i，因此不是所有费用单谱系不重复，更不是所有源共同钱包。
- 可选chi≤min(ell,kappa(v−P))仅保严格sub-Markov和带−chi的signed账，原SUBSET/PRICE数值常数不能无条件继承；不证明净费用改善。
- 1831字节价格审查首次读稿已含证明，非盲。局部凸包与基线和式通过只说明固定核结构，不提供actual单券/同角色cap或新half。
- 3098字节本次审计与长稿§10的9721字节audit_submarkov_elimination.py是不同程序。原稿历史记载的1584 IC、2411子集、1916past域、初版/v2及root_tax非零all-customer probe，均仅作为原稿历史范围保存；本批未恢复/执行未认领旧程序及其两fixture/报告，不冒称这些原件已实读或其run已重放。原OPT-owner零传播及两fixture均无正fresh边的限制保留。

## 三对象与四来源的去向

1. 完整利润鲜广播消元与同客户取消--定理：完整保§1—9模型/两真实slack、fresh全体客户计数/子集PRICE、有限DAG、C-LEDGER、合法INIT、全客户past域/新流/券账、同客户取消/缺额、谱系区间的收费限制、可选chi；§10保原自核历史身份，链接本次不同定义级程序证据。没有只留下摘要。
2. 鲜利润计数与非零两层图的精确复现--计算：源码、所有输入域、全部报告字段、计数推导、两层每个有理数及真实执行/相同字节/零域限制均保全。脚本源和报告源各自receipt，不以报告passed代替源码理解。
3. 净券局部凸包与终点价格的非盲核对--审查：保原1831字节逐式核对的边际和基线等价展开、全图HIT必要性、边界、固定核/适应排除和准确非盲身份；不是仅metadata或新福利定理。

所有正文自足说明其假设、量词、证明、范围、未证项及接续；共同实际容量、ROLE/OWNER-NET和无条件六人half没有升级。没有改前批三页或本代理紧前四页。Boss另实读3098字节原程序、461字节旧报告及新完整利润正文，核有限计数和非SPE边界；这是本批内部读稿核验，不是外审或独立数学实现。

关系判断和逐源receipts见workspace；本批不新建代理、不扩领、不做Git写/claim/done/checkpoint。三个新增对象可交付，旧§10三回归资源留下一次另批处理，不将未认领资源计done。
