# 合法单题背景任意末回复锥探针证据

主源4b92e1ba3e4d5ec1de8a，2412B，SHA-256 `efdfe17ac4a1751fc784c2c833e59d6fb5443935d6fce4c19aca148a5f191a12`。原clean show副本全文实读，当前保存字节与两冻结提交一致；[正式程序正文](../../../state/程序/合法单题背景的任意末回复策略锥探针--程序.md)完整解释背景、客户型、回复图、IC、目标、随机抽样及输出分支。

| 文件 | 身份与范围 |
| --- | --- |
| original/probe_fresh_arbitrary_reply.py | 未改主原码；本轮没有调用run/main或LP。 |
| related/probe_fresh_global_two.py | 全文比较的3601B相邻原探针；策略选择、比较对、去重、背景循环和best更新均不同，未执行。 |
| source-manifest.json | 来源路径/版本/字节及既有H证明、历史数据的绑定。 |
| audit_cone_contract.py | 抽取原初始化和首次构行AST算术块，截在linprog前；另从真实单位份额构造Fraction矩阵和已有H证书余项。 |
| cone-contract-audit.json | 一张明确合成回复图的完整48×127有理矩阵、127目标、精确浮点误差、四乘子及127余项。 |
| audit-execution.json | 实际一次仓外接口核的命令、退出0与身份；没有记录开始时间，不补造历史时间。 |
| self-check.json | 原件、报告、AST、局部链接、回执及计数的静态检查，不重新跑数学核。 |

历史[130B原报告](../fresh-arbitrary-reply-probe-data/original/fresh_arbitrary_probe.json)由配套数据任务统一保存；六字段为q7、cases12000、L1、feasible12000、best0、seconds约32.2597。它没有seed、客户权、回复图或每次目标。本源默认是q6/cases10000/seed71215/L1，不能反推历史使用默认seed。本任务和数据任务都没有重跑12000次原发现。

## 新接口核与原搜索严格分开

新合成输入为q7/L1/seed0，原随机赋值语句产生reply=[6,2,6,3,0,2,4]。只执行原AST算术片段1次，不调用原run，不替换linprog，不让原脚本写witness/probe。它不是历史采样中的一轮重现；源输出没有seed，历史样本不可由现表唯一恢复。

独立一侧对全部127非零客户型，从单位均分生成6223个收益系数、6096个IC系数和127个目标。原AST一侧是NumPy浮点，逐项保存其与精确Fraction值的误差；收益/行最大误差1/54043195528445952，目标最大误差1/27021597764222976，均小于2⁻⁵⁰。没有把浮点减法的舍入差冒成精确系数相等。

四个已有H证书乘子对应该合成矩阵零基行43乘1/2、42乘1、8和9各乘1。逐客户精确验证“目标+四条偏离行”的结果等于两个非负安全保底差和合法H余项，并全非负。全mask127权1的每条IC为0、目标2/3也核同。完整48行及127项账都保报告。

一般L≥1和任意回复图的结论仍由[已有H证书及符号余项](../../../state/计算/背景菜单的有限证书--计算.md)与正文的矩阵对应公式承担，不靠这一个合成例外推。本轮没有重跑该证书的39变量384行发现LP或独立384行审计。

## 关键语义边界

每张固定回复表含全部q个末位历史的BR和首位所有真实偏离，故其精确锥是完整两人子局IC；并未验证H^L在根实际发生。参数q数标签，不数提供者；H/A/B/T/S固定为不同标签，但可以同覆盖，不声称固定q穷尽角色重合型。

随机图有放回抽样、无去重；q7条件ρ(1)=2下共有7⁶=117649张图。best只初始化0，从不更新；负于−10⁻⁸就首次早返，正常返回的0不是精确最优。所有锥都含共同覆盖型的平局可行点，所以feasible12000不是不同实例的覆盖数。

原负候选只保w>10⁻⁸的坐标再限分母有理化，不重验IC/归一化/负号；见到分数格式也不能直接称精确反例。合法H域实际已有解析非负证书，一般52客户多题前缀反例缺少合法并集主题H，不与此冲突。没有由未命中浮点搜索推出全域定理。

如需重做此有限接口核，可以在仓根用新输出：

    python -I archives/customer-attraction/tools/evidence/fresh-arbitrary-reply-probe-program/audit_cone_contract.py --source archives/customer-attraction/tools/evidence/fresh-arbitrary-reply-probe-program/original/probe_fresh_arbitrary_reply.py --output /tmp/new-arbitrary-cone-contract.json

本次运行已保存，正式复制后未重复执行。原run/main/LP均0，原AST算术块1次；任何未来真正搜索须另存输入、事件及候选精确审计，不改写这份历史报告身份。
