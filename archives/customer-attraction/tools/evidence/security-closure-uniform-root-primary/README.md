# 真实查询重复归约与弱根菜单的五主源证据

本目录对应正式pushed认领f8aec6ba937b8d78e8c31f77a54296dc03f2df0f，唯一原capture为boss4-r3-next15aa-claim.json。实际actor为Boss4，期望五源全在实际ids中，local_sync为synced。工作区claim-observation.json及claim-receipt.json保留本批身份；旧同名capture与旧776eb…认领没有被用成本批证据。

五主源共22303B：security入口1917B、root弱报告11973B、工作室README3001B、重复攻击原码3955B及报告1457B。全部正式确认后全文读取，按inventory SHA保存，并核68fad804…与aefc58ea…两个冻结定位的字节。primary-manifest.json只含这五源；runtime-manifest.json保11项真实依赖共488699B；合并source-manifest.json共16项，依赖阅读不产生额外primary receipt。

正式正文是[端点与归一化引理](../../../state/引理/真实查询均匀接口的支持端点归约--引理.md)、[重复均匀接口有限攻击](../../../state/计算/重复比较均匀接口的固定动作表攻击--计算.md)、[自由根菜单弱模式](../../../state/计算/自由根菜单弱安全值的交替锥探测--计算.md)。它们分别承担精确归约、334次固定动作表浮点筛查、65次交替LP有限结果，不能合并为一般UP或安全桥定理。

## 原件和真实依赖

original/保持全部源相对路径。uniform入口依赖四个证书的strategy.actions和tests/audits/customer_attraction_strategy_lp.py。该helper会导入customer_attraction的四个模块，故完整保__init__/model/exact/certificate；入口没有调用规范solver、证书验证器、helper.main或self_test。root入口只依赖同一4990B原generic代码与372216B旧13人封闭自动机gzip。所有依赖SHA、字节、两冻结来源和角色见manifest，未改导入路径以假装不需要原依赖。

uniform-input-structure.json保四输入的全部动作表、字典序分层、完整历史数量和根路径。前两输入有不同文件字节及元数据，却拥有完全相同的43行动表；四次输入处理对应三份不同完整动作表。程序没有读取证书内原客户与安全结论来作LP约束，改变客户质量的锥不可与原单一实例的精确证书混同。

## 本轮仅两次原入口

replay-tree/是未改码、完整相对路径的新隔离树，不预放两个输出。以下入口各一次，由工作区prepare_and_run.py保唯一执行记录，已有execution文件时拒绝重跑：

| 入口 | 次数与耗时 | 输出及一致性 |
|---|---|---|
| cone_security_probe.py --mode root --weak | 1次，21.869602918624878秒，exit0 | 11973B，SHA808949fb8b52dbe3b58045cd6e406e9cccf1f477aa573e0cbc62f21fe4473c67，全字节同冻结 |
| attack_multisets.py（原默认四证书） | 1次，3.143134593963623秒，exit0 | 1457B，SHA345505c7e481eeb87406aa6f472f5931af91f861f4a16510e62341ae679baa39，全字节同冻结 |

环境为Python3.12.14、numpy2.3.5、scipy1.17.0；两次stderr均空，输入代码执行前后未变。root为16起点/32trace/65LP，全部落到全兴趣点，精确解释只给可行值−1/26。uniform为56+56+111+111=334LP，没有正候选、没有触发有理恢复，也没有输出负/零最优值的精确对偶。本批没有重跑all/onpath、stationary原审计、helper self_test或其他旧批入口，亦不把本次运行回填为旧批当时已执行。

replay-root-weak/与replay-uniform/各保新输出、stdout/stderr及execution.json。工作区validate_delivery.py另做本批传输/结构和Fraction端点分解检查，只读已完成输出，不调用原main；其有限结果不是普遍数学证明。全称归约和W归一化由正式引理承担。没有扩大固定策略域、没有新的half反例或一般不可能性证明。

## 来源入口与接续

两个README中的独有历史、源作者团队运行声明、静态强弱桥/指定核/自由菜单区分、八个研究目录的不同开放状态，均保在自由根菜单正文末两节。六名指定内部研究员运行和恢复点属于作者历史陈述，本批没有认证这些调用或把它们变成本批独立盲审。五人half当前另有独立证明；旧一般OPEN不可覆盖新状态，六人half继续开放。

关系判断与数学自查在同名cleanup工作区。全仓比较页的路径/哈希保在related-material.json；源原件与运行依赖的保存不是对这些依赖另记done。当前目录不声称远端已保存本交付；串行复制、checkpoint和done均由Boss处理。
