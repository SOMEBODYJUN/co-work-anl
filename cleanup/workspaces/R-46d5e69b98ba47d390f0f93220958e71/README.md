# 共同目录模型、三人界与局部税的语义清洗

发布身份：R-46d5e69b98ba47d390f0f93220958e71。结果分支rebuild/research-v2；本对话独立clone，角色cleaner。

## 本批范围与恢复入口

正式认领12个源版本，均已逐份读完。它们每项都在legacy-cleanup与main中有两个定位，实际Git对象字节重算SHA-256均相同，按冻结清单只计一个版本。
正文与复现依赖在[客户吸引存档README](../../../archives/customer-attraction/README.md)的“已整理的数学正文”；本批形成7份新数学/资源对象、4脚本、4原始报告、4本轮复跑和manifest。
已按顺序完成：正文与依赖checkpoint返回pushed（本轮提交fb7709f9a3217a75cf02d3d1578cca2bccaa4433，远端确认HEAD 6257396404b0ef732191156d74c5f05701d7851b）；随后12项clean done全部返回pushed，完成记录远端提交9dd04b5d02f272b9c416f593b9f315a225723527；随后sync确认。逐项真实阅读、相关比较与目标见本工作室receipts.json及cleanup/progress对应ID。本批没有needs-decision或未释放的领取。

| 源ID | 冻结路径 | 本批保留单位 |
| --- | --- | --- |
| f3713036893d6d430c7d | research/current/customer_attraction/model.md | 模型定义 |
| 3248e8da0ea722454971 | research/current/customer_attraction/two_remaining_tax.md | 两人引理、条件归纳障碍、末位诊断、有序重排族 |
| d55d97a783ab48b34a18 | research/current/customer_attraction/three_player_bound.md | 完整三人证明 |
| a8e35e3facf8c983c221 | research/current/customer_attraction/three_player_sharp.md | 完整三人证明 |
| 20a20c443f5ab8186c48 | tests/audits/customer_attraction_three_player.py | 独立审计资源及原输出 |
| b92abbabac3dd0f0a053 | tests/audits/customer_attraction_three_player_sharp.py | 独立审计资源及原输出 |
| 5955ca29046d890a69b9 | evidence/runs/2026-10-09/customer_attraction_three_player.json | 独立审计资源及原输出 |
| c14e40cdfcbfb433adc3 | evidence/runs/2026-10-09/customer_attraction_three_player_sharp.json | 独立审计资源及原输出 |
| a282d206c0083eacdfa5 | tests/audits/customer_attraction_tax.py | 独立审计资源及原输出 |
| 8cd8dee0c0ae2e9d3f5a | evidence/runs/2026-10-09/customer_attraction_tax.json | 独立审计资源及原输出 |
| 9e713d9d72f736763f13 | tests/audits/customer_attraction_ordered_tax_boundary.py | 独立审计资源及原输出 |
| db25db242893a12ef978 | evidence/runs/2026-10-10/customer_attraction_ordered_tax_boundary_certified.json | 独立审计资源及原输出 |

## 真实比较与未做的范围

全仓冻结源检索使用three_player_sharp、CA-THREE-SHARP-5-3、CA-THREE-UPPER-142-81、CA-TWO-REMAINING-TAX、142/81、CA-ROOT-TAX-NO等精确关键词；未把检索命中视为阅读完成。
实际完整阅读并用于比较的相关正文（以下均在冻结68fad804ec5946cb296f77dc5b336308a66abf12）：

- research/current/model.md：主动客户设施模型的客户NE和存在续局量词；阻止同名模型混入。
- customer_attraction/model.py与research/current/customer_attraction/exact_solver.md：单位客户重数、标签扩展、集合计数缓存与全部有序历史重构。
- research/current/customer_attraction/continuation_lemmas.md：14客户末位高于平均、同负载不同平局、SPE非静态PNE。
- three_remaining_profit_bound.md：后续任意合法背景三人利润界及完整多项式系数表，量不同于根覆盖。
- four_player_bound.md：四人证明直接依赖两人税，不依赖三人福利界。
- tax_bridge_counterexample.md、general_tax_counterexample.md、root_tax_counterexample.md：分别反驳首步桥、合法背景总税、真实有序根税；都不反驳half。
- prefix_balance_family.md：另一n≥4负前缀余额族，使用总覆盖补全，不是背景剩余利润；没有和重排族合并ID。
- five_player_half.md及2026-10-25的cleanup_evidence_audit.md：旧审计“五人尚未half”已被后续证书入口更新；本批不认证或复跑五人完整包。
- 根CLAIMS.md、RESEARCH_STATE.md、FAILED_ROUTES.md的冻结来源：用于恢复身份与当前六人边界，未把导航摘要当证明。

上述相关文件不因被本批阅读就自动计入本批勾选。三类税反例已由同期另一批完成独有数学和复现归档；其余相关源仍待后续按实际清单领取，本批不冒领覆盖。
对方已发布的固定背景剩余收益与税--定义.md完整覆盖原税页§4的条件归纳、拼接和分母障碍；本批采用该共享正文作为目标，移除未发布的重复障碍稿，不再造重复对象。
另一清洗者R-bad32597e284486cb1f0080aa3ed39c6已发布三个税反例及其依赖，并完成其12项done。我已读取其正式正文、定向沟通并采用直接链接，避免重复稳定对象。

## 并发导航合并

同步时双方同时修改archives/customer-attraction/README.md发生真实内容冲突。程序保留本地完整stash备份d5ac996d508d09a8ad9cd8057ec4ca66db795047；我逐段保留对方6个税接口导航与本批7条模型/三人/局部税导航，未覆盖任何一方正文、未强推。
已读对方新发布的三个完整反例和税定义，改用正式相对链接；他们12项done不计入本批12项。

## 自查、证据与状态

四份Fraction脚本均已源码实读并复跑。三人两份原JSON与复跑完全一致；两人税只变运行版本/HEAD等元信息；重排报告的exact_audit与新输出一致。
原重排报告所引税证明哈希是早期版本，当前冻结税正文的哈希不同；新manifest明确分别保存，不冒称旧报告认证当前正文。
较弱三人源末段“与5/3仍有间隙”的旧状态已纠正；税页“根税开放”的残留措辞按61客户实际反例消歧。
真值、完成度、审查和scope分别标注；本轮重构不新增外审或新颖性认证。

## 剩余与接续

本批只处理12项，不是10921项全仓清洗。六人Q-CAG-HALF-6仍OPEN，未部署数学Agent/正式研究提示词，未复制旧图或建立阶段三超边。
下一批可领取三人背景利润扩展的完整审计/证据，或其他实际数学对象；不把本批路线设为方法边界。
其他未认领源、学习/历史/设计/程序目录仍须逐源语义判断，不能按目录整类退役。
第三阶段可读正文内具体依赖/非依赖说明，逐边核对，不把本批7个新对象数量当成图完成。

## 最终本批核对

- 12项本人来源处置全部在远端由本人持有且为integrated或retained；正文目标先推后勾。
- 7个新对象各有稳定ID、kind/type_tag、完成度、truth_status、review_level和scope；相关税定义直接复用他人已发布对象。
- 四份数学精确审计均已通过；原字节脚本和原报告保留，本轮JSON另存。
- 所有本批Markdown相对链接、数学分隔符、冲突标记与对象结构检查通过；map check只验证结构，不等于数学或图已完成。
- README真实冲突已保留双方并合并，未强推；本地完整stash备份仍留着。
- 当前只有局部语义整理，无全仓清洗完成声明、六人证明、数学Agent部署或第三阶段超图完成声明。
