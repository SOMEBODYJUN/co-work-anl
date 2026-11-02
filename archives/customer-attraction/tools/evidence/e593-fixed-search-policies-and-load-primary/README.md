# R-e593十八来源与固定五图精确点审计

十八primary共504387B全部实读并保原字节，双冻结各同字节；[来源清单](source-manifest.json)给完整commit/原路径/blob/SHA。五JSON的全部weights/policy/164记录按生成代码定义完整解码，个体报告30项、575B负载点全部字段亦保。[字段阅读表](source-field-reading.json)的指纹只记录读取，不充当数学证明。

正式正文：

- [五保存图的三种解释与单位点](../../../state/计算/五份保存策略图的浮点解释与单位客户校准--计算.md)：真实完整图证明、微小负IC、有限点与全锥最优的区别。
- [负载候选与多尾边界](../../../state/候选/终局负载代理的精确菜单递推与多尾构造边界--候选.md)：ψ候选/精确BI合同、58客户点解析最小proxy、多尾参数被既有更强末位障碍覆盖。
- [个体净缺口三十条合同](../../../state/程序/早期逐人净缺口的原扫描合同与三十条记录--程序.md)：30=1skip+3tested0+26有测试，952 reported tests，不是新LP。
- [多路线资源](../../../state/资源/R-e593多路线入口与程序证据的准确范围--资源.md)：全部18原件、CG成熟复用、客户删除静态保持及不保SPE、原身份与当前开放范围。

## 十八原件

|source ID|原件|
|---|---|
|09a329ef385dd476cd32|[根README](original/09a329ef385dd476cd32/README.md)|
|a6541ac97175f9217565|[search.py](original/a6541ac97175f9217565/search.py)|
|83aeac84ff59ae42a9d6|[m5p7](original/83aeac84ff59ae42a9d6/search_m5p7.json)|
|351b0859f830ed409806|[m5p7_allj](original/351b0859f830ed409806/search_m5p7_allj.json)|
|e18b70bbb8719f4a182c|[m5p7_mix](original/e18b70bbb8719f4a182c/search_m5p7_mix.json)|
|d73387b0668aa5956e1b|[m5p9_mix](original/d73387b0668aa5956e1b/search_m5p9_mix.json)|
|8172fb7830818f6b58f1|[m6p7_mix](original/8172fb7830818f6b58f1/search_m6p7_mix.json)|
|57fe78ad50d90d0f90b6|[CG README](original/57fe78ad50d90d0f90b6/README.md)|
|6ea50599d127a7e8a821|[原CG verifier](original/6ea50599d127a7e8a821/verify_cyclic_gradient_boundary.py)|
|9e185dc68adc7e073ca7|[逐人攻击](original/9e185dc68adc7e073ca7/attack_individual_defect.py)|
|5e9bbf6c89fc8a96a4ff|[逐人30记录](original/5e9bbf6c89fc8a96a4ff/individual_defect_cone_scan.json)|
|078fe153c4645d32b531|[负载入口](original/078fe153c4645d32b531/README.md)|
|486e6af7977dae5da4fd|[退火源码](original/486e6af7977dae5da4fd/anneal_load.py)|
|013122e272e2d1804cf3|[58客户保存点](original/013122e272e2d1804cf3/anneal_p4_m3.json)|
|006a4c4ba3fdec1dda91|[精确负载探针](original/006a4c4ba3fdec1dda91/load_search.py)|
|15bfa0fa66c815ff0e9e|[多惩罚旧private债](original/15bfa0fa66c815ff0e9e/multi_punisher_boundary.md)|
|c3dd81993b52ec565726|[客户删除probe](original/c3dd81993b52ec565726/probe_union_deletion.py)|
|5cefdb10fce624c01c4b|[workspace身份](original/5cefdb10fce624c01c4b/workspace.json)|

## 唯一新增数学事件

[audit_five_saved_graphs.py](audit_five_saved_graphs.py)实际只运行1次，不导入任何原程序，不用NumPy/SciPy、RNG、LP或BI。逐边审保存紧凑策略图，确保每个合法有序历史有唯一展开并达到所记terminal；在三种不同数值输入上分别核实际收益差：原JSON加载二进float精确值、原十进token精确值、另定义大块m/小块1的单位客户点。没有静默修原值。

实际2497紧凑节点，每解释16412个非self比较，三解释49236次；整数路径重数证明覆盖35392有序节点/每解释227114非self偏离，但0次显式整树物化。四五人二进点均保负最小−1/90071992547409920；六人字面点严格通过，所有十进点与另定义整数点通过。完整[报告](fixed-five-001/report.json)、[每节点全部margin压缩表](fixed-five-001/all-compact-node-margins.json.gz)、[stdout](fixed-five-001/stdout.txt)、[stderr](fixed-five-001/stderr.txt)、[事件](fixed-five-001/execution-observation.json)俱全。

内核0.6208742060007353秒、工具墙钟0.868883948秒，exit0、stdout2624B、stderr0，五原件前后字节相同。新整数点不是原历史认证，不把有限可行点叫精确锥最优，也不重演设定100/150/500轮搜索。

复现用证据包副本从任意cwd运行`python3 audit_five_saved_graphs.py`；程序依自身路径定位五原件，已有report时拒绝覆盖。原事件stdout/stderr由唯一启动命令分别重定向捕获；副本复现需同样自行另存输出，不能覆盖保存事件。

## 其它证据全按真实范围复用

[CG绑定](cg-mature-reuse-binding.json)只核本次4847B主源码的指定输入SHA与已归档20517B点，并复用现行43动作/126收益绑定、15环及完整点数学；本批CG原入口/旧数学checker新调用0，不把已有完整阅读冒成新的运行。

[个体完整记录表](individual-records-complete-reading.json)保30原记录及952 reported tests；0本轮LP。[复用依赖](reused-dependencies.json)写明全文、选段或只解析schema/SHA的真实范围，不冒审全部外部策略输入。[关系审查](relationship-review.json)记录准确蕴含/纠错/成熟复用与非蕴含，不改共享图。

[self-check.json](self-check.json)只做交付字节/链接/receipt/事件静态检查，不增加数学入口次数。18份真实read/comparison/decision与targets在父方接收的`agent-b11/receipts.json`。所有Git/claim/done/checkpoint仍由父方串行，本包没有重演原work.py/公屏/旧actor操作。
