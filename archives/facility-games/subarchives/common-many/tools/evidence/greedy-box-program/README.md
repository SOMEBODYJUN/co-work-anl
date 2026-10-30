# 规范贪心程序的固定依赖与报告字段适配

本目录对应[程序接口对象](../../../state/计算/规范贪心完整续局程序与选择器接口--计算.md)。本批正式清洗的唯一原源码为4e4efdb8c30ab03aee8b，multi_facility_spe/greedy_box.py，冻结提交68fad804ec5946cb296f77dc5b336308a66abf12。

## 三种身份保持分开

| 身份 | 文件与指纹 | 当前用途 |
| --- | --- | --- |
| 冻结原件 | [greedy_box.py](../greedy-box-finite-progress/source/multi_facility_spe/greedy_box.py)，SHA-256 b3b391f6e4c1efd8e56c036d3d588f191959504aede58e686c3bfcb291f6ef35 | 原版代码及历史定位基准；本批没有新运行原构造 |
| 局部适配report-bound-decimal/v1 | [greedy_box_decimal_bound.py](greedy_box_decimal_bound.py)，SHA-256 a50ea29a2506d9890d0773e69747a18e4127516d781a4750b1f757af3462f91c | 仅将assignment_move_bound输出换成非负整数分块十进制转换 |
| 验证辅助 | [validate_report_adaptation.py](validate_report_adaptation.py) | 核固定依赖和AST差异，再比较格式化及调用一次适配版在轨构造 |

原源码不被替换。[report_bound_decimal.patch](report_bound_decimal.patch)给出原件到适配版的精确差分，不作为自动修改原树的动作。新增函数按10^9分块输出，零值直接处理；每个小块至多九位，不更改解释器的进程级十进制转换限值。源码内标明适配身份、基础冻结源及同仓equal_light_flow小块转换的比较出处；未把流模块引作默认方法的新依赖。

除一处报告调用外，所有原有可执行AST与冻结原件相同；新函数不参与NE、势、选择、归位、离轨或默认计算。输出字段仍为精确十进制字符串，schema未更名。它不修复任意巨大Fraction的输入/输出，也不修复下游直接int(超长字符串)。

## 完整四文件Python API快照

[snapshot_manifest.json](snapshot_manifest.json)固定下列原相对路径树，共39,939字节：

| 文件 | 源ID | 用途 |
| --- | --- | --- |
| multi_facility_spe/__init__.py | 3185703b41c7540715bc | 原包身份/说明；已逐源清洗保存 |
| multi_facility_spe/two_exists.py | a7a1f7d850e620474411 | Instance、装箱、有限纯修复、续局查询；已逐源清洗保存 |
| multi_facility_spe/greedy_box.py | 4e4efdb8c30ab03aee8b | 本批原程序 |
| multi_facility_spe/equal_light_flow.py | e19c1dd1197f68906d4a | 可选等重在轨方法的原依赖；本批仅全文比较和重建 |

每项有完整SHA-256和字节数。该树支持Python API的默认及equal-light-flow入口、完整有限构造与继承的续局查询。它不含CLI、测试树、输入示例或历史报告，也没有把可选依赖的源清点状态变成done。

复用此前已保存的[固定源重建器](../factor-two-audit-suite/reconstruct_snapshot.py)，显式指定本manifest即可：

~~~sh
python3 archives/facility-games/subarchives/common-many/tools/evidence/factor-two-audit-suite/reconstruct_snapshot.py --work-py work.py --destination cleanup/workspaces/reproduce-greedy-api --manifest archives/facility-games/subarchives/common-many/tools/evidence/greedy-box-program/snapshot_manifest.json
~~~

本批实际运行这一重建器，目标为cleanup/workspaces/Boss3/facility/round10/rebuilt-api；成功形成4文件树，逐文件长度和SHA全部吻合。 这四个文件现也以相同字节保存在本目录的[source/](source/)树中，供离线重建和逐文件核验；它们不是新的未经来源确认的实现。[reconstruction_check.json](reconstruction_check.json)保存成功调用后的指纹记录，audits_executed=false。只读clean show导出可在首次未缓存时访问网络；不做claim、done、提交或推送。已有相同字节可复用，已有不同字节拒绝覆盖。

这比此前19文件lexmax审计树的范围不同：它补入当前greedy和可选flow，但不包含那19文件中的审计、证书或示例。不把任一局部树冒称完整旧仓库。

## 必要验证：实际做了什么

[adaptation_check.json](adaptation_check.json)是一次实际新适配验证记录：

- Python3.12.14，十进制转换限值前后都为4,300，冻结原件指纹前后未变。
- 删除新增函数并将唯一assignment_move_bound调用还原成str后，全部原有可执行AST相同。
- 八个非负整数格式化样本与独立Decimal转换相同：零、一、10^9左右边界、10^18及带零块值、2^15000−1。
- **原版construct_on_path调用0次；适配版调用1次**。该次使用此前确认的两地点/三设施/15,000轻客户零步输入。
- 适配版返回布局(0,0,1)、γ=2、0改善、0归家、0批，四项最终数学验证true；上界精确等于2^15000−1，长度4,516字符。
- 对该输出调用既有形式int(bound_text)仍实际抛ValueError。这是下游宿主限制，适配没有伪称消除。
- 完整construct、equal-light-flow、离轨和默认查询均运行0次。

验证器在运行时的字节指纹为 `d67dac0f0f18222f013bc29b2d4d0f1723a87c331e4a4012fca6e1bd357e1d30`；为通过本仓库的空白检查，本目录随后只去掉了文件末尾的多余空行，当前保存的验证器字节指纹为 `5fd5810981768a9eda4d6fb307d328f3002ceb4ea4b6198970ebff0e60d56298`。没有用未重新运行的规范化副本改写上述实际运行记录。

此前的[两次原版故障定位记录](../greedy-box-finite-progress/integer_bound_serialization_check.json)继续作为原版证据，不重复运行，不与本次一次适配调用合并成三次原版运行。此适配验证不证明所有分支或所有原始输入已可运行；普遍数学结论仍来自正文证明。

如需重做这个有限验证，从结果仓库根使用新的输出路径：

~~~sh
python3 archives/facility-games/subarchives/common-many/tools/evidence/greedy-box-program/validate_report_adaptation.py --core-root cleanup/workspaces/reproduce-greedy-api --original cleanup/workspaces/reproduce-greedy-api/multi_facility_spe/greedy_box.py --adapted archives/facility-games/subarchives/common-many/tools/evidence/greedy-box-program/greedy_box_decimal_bound.py --output cleanup/workspaces/reproduce-greedy-api/report-adaptation-check.json
~~~

验证器在导入前核四个固定依赖、原件和适配版指纹；禁用-O，禁写pyc，并拒绝覆盖已有报告。该命令实际运行新适配版一次，不运行冻结原版。若未来修改适配版本，须建立新的指纹及验证记录，不能把不同字节称作本适配已测版本。

## 后续比较与处置边界

本批另全文比较greedy全局审计ea34d2bb6de57b31bb46、快速入口f7b7c253e44ac41e8fb1、flow代码e19c1dd1197f68906d4a及其回归6a46403cd2d684fe1ab8；只读关联数学源8907788ebccde4e91d10的§1–7承重证明。没有把它们自动done，没有跑这些回归或完整审计，也没有复制旧报告数字冒充新执行。

源码的有限算法、固定参数数学结果、等重选择器、多项式离轨数学接口和当前程序中的报告修复分别具有自己的范围。当前一般位多项式总时间缺口保持不变。
