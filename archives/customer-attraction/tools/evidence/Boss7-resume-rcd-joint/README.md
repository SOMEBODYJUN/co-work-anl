# 最大根联合块、66原子点与固定边缘lift的证据

拥有正文：

- [联合定价/真实末位合同](../../../state/程序/五人最大根联合块与真实末菜单的浮点定价合同--程序.md)。
- [固定边缘32态lift合同](../../../state/程序/最大根三十二态拆分的两份浮点不可行诊断--程序.md)。
- [66原子/3132行有限点及遗漏菜单](../../../state/计算/最大根三千一百三十二必要行的六十六原子点与尾菜单缺口--计算.md)。

这10个主源全部原字节保于original/；逐源ID、两个冻结commit、原路径、大小、blob与SHA见[source-manifest.json](source-manifest.json)。全文代码与完整数据各自保存，未只留成功摘要。数学上区分：当前joint程序的可分离oracle合同；过去版本的有限audit及未定价停止；固定66点的当前原标量值；两个旧点的浮点lift失败。它们不共用“已证half”身份。

## 所有源记录和主数据

|主源ID|原文件|保留内容及归宿|
|---|---|---|
|97eaa469761253348cb0|audit_max_block.json|128状态/65408系数差及四个真策略case；e5bb旧joint源码绑定|
|0502d33f92ea6b535ba3|audit_max_block.py|向量/标量比较器、四目录全有序历史IC、直接原主题构造|
|601b71090c1b1eb346b6|exact_max_menu_joint_primal.json|完整66个有理质量与类型、3132有理slack、W/O/gap、77零、代码/源SHA|
|8c0ec91d5d96b0977f49|lift_maximum_branch.py|固定边缘32态、AP/root_hist行域、浮点可行/共同松弛诊断及所有阈值|
|8ed42cc22955c47e6a62|max_menu_joint_discovery.json|2434原子及质量全量、3132唯一名字、单轮停止/源版本身份|
|f640f8636aa8f4c9adb7|max_menu_joint_pricing.py|511最大枝行、32态条件分离、旧菜单线性项、LCM限制与发现入口|
|926fc0fdc3d78b846035|max_menu_last_pricing.py|七个末位菜单行及五共同负载层；无保存运行报告|
|6d6810dc4e12454f9e93|maximum_lift_ap_binary_discovery.json|72支持/540行的全行名、HiGHS不可行、共同松弛及两浮点诊断权|
|87356422b10716fcd192|maximum_lift_exact_optimum_primal_joint_terminal_noap.json|65支持/236行、无AP、全部同类记录；source_exact不升级LP|
|61864d39e0494b346b45|omitted_tail_menu_slacks.json|28个真最大枝后继查询的全部有理值，含两负末位行|

[complete-record-reading.md](complete-record-reading.md)逐项列全部类型字段池、76个32态块及2锚、66非零float、66精确质量和全部28遗漏值；[complete-field-projection.json](complete-field-projection.json)还保全部3132行名/原slack、顶层字段和无损索引。`read_projection.py`是只读JSON并写无损阅读视图的程序，不导入科学包。前448发现原子携带14个旧exact_mass并不代表当前2434维质量；当下float只取primal_float，精确点另有66个自己的有理质量。

## 已发生的两次进程事件

第一次固定输入资格核在第一原子断言`list(rr)==row_names`失败，exit1、stdout0B、stderr442B、墙时0.16730791800000588秒。完整当时driver、stdout、stderr及event留first-attempt/。3132个唯一行名的集合相同，插入顺序不同；随后driver按名字核长度/集合并点积，没有删除/替换行。

修正后一次成功：exit0、墙时3.106708534000063秒、stdout1123B、stderr0B。当前`check_fixed_66.py` SHA `2ea354d392a1cef21d39ad1e5dff50f51774c123ed7d550132fd398bab7cabd0`；loader SHA `563b9b7048fc68e1a80bcc67c860e1889a7e4831c399e2d00d9f3c5211ea2fbd`。成功汇总、真实输出和事件分别为fixed-66-qualification.json、qualification.stdout.txt、qualification.stderr.txt、qualification-process-event.json。

已完成的206712=66×3132个Fraction标量行系数、1848=66×28个尾菜单系数带来：全部3132保存值相等且非负、77零、W1、O/gap相等，全部28遗漏值相等且恰两负。逐项数据为all-3132-row-equalities.json、all-28-omitted-row-equalities.json、all-66-atom-metrics.json；selected-original-scalar-AST.json保存所有抽取语法树、源SHA与选区SHA。

这不是独立系数实现：loader与[AP/tuple证据包](../Boss7-resume-rcd-ap-tuple/README.md)共用十份标量定义/atom_rows白名单，仅换固定66点输入。函数抽取避开原导入、构造器及CLI；无原Universe初始化、LP、BI、price、完整SPE或全类型余项证明。本次续稿未再次执行两次核或原程序。源audit/CG/lift的历史seconds只保原字段，不计作本轮运行。

## 依赖、路径与复用

`check_fixed_66.py`只用Python标准库和qualified_scalar_loader.py；检查时显式输入兄弟AP/tuple证据根：

```sh
python archives/customer-attraction/tools/evidence/Boss7-resume-rcd-joint/check_fixed_66.py --shared-evidence archives/customer-attraction/tools/evidence/Boss7-resume-rcd-ap-tuple
```

这是交付后可执行的**合同**，不是本轮新增执行。它会覆盖本目录all-*.json、selected-original-scalar-AST.json和fixed-66-qualification.json，将来请先复制到隔离目录，保原事件和输出。事件JSON中的绝对stage路径是当时实际位置，搬运后不改写为伪历史argv。loader执行`load`时需要AP/tuple包的以下十份定义文件，完整字节/SHA/选区在selected-original-scalar-AST.json，不能以同名新脚本代替：

- related/five_indexed.py、offdiagonal_closure.py、partition_pair_closure.py、full_pricing.py、cross_pair_pricing.py；
- original/95ae42780dac898a9c0d/menu_ap_pricing.py、original/1f4560c9319c2a285e47/max_menu_tuple_pricing.py；
- related/lift_maximum_branch.py、max_menu_joint_pricing.py、exact_primal.py。

lm/joint两份SHA与本包主源相同。上述源每个只选明定函数/常量/atom_rows；原完整科学模块没有被import。将来若AP包移动文件，须同步显式--shared-evidence及相对布局，不能把路径错误报告当数学反例。

四份原程序的真正CLI还需要历史研究根、规范customer_attraction、NumPy/SciPy和传递定价模块；它们不是本10文件的独立可运行套件。原audit、run和lift会覆写邻接JSON，复跑应隔离原件，先恢复准确源码及依赖。没有保存max_menu_last_discovery.json，e5bb旧joint生产版本亦未取回。原两lift无精确Farkas，全型dual和真实共同策略都未从文件名补造。

## 相关比较和关系边界

同一66点先前在最大根1414耦合查询审查中作为related输入保原，71条负值另有归宿；本次补其主源done并完整资格核，不重复认领该审查五源。另一个61点虽与本点O分数相同，输入SHA、原子和4007行域不同。固定旧72/65点的lift、共同最大主题61乘子普遍上界，以及当前五人half证书的域/量词也不同。三篇正文各给相应链接，阶段三只可按这些解释建立“实现”“有限检查”“新增必要行排点”“模板强弱范围”关系，不由代码导入关系伪造逻辑蕴含。
