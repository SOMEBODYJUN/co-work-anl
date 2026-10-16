# 同权类前沿全覆盖编译器的独立重构与冻结攻击

## 审查结论与身份

**审查对象：WC-CLASS-FRONT-ALLSTATE-COMPILER-v1。** 对所写精确输入合同，
一般条件编译结论、标准预算及保前沿精确抵消预算均未发现尚成立的 fatal
objection。此为 complete stated-scope proof、independently reconstructed and
exactly audited、unrefereed；不包含新颖性认证。

结论仅是：若每个 product-front 已有保 product-front 的严格 alpha 改善，
则追加指定同权、固定首位锚定三元资源可得到全状态严格改善覆盖。它不证明
任意严格 sweep 环满足这个前提，不给出增长族，也不解决 WC-TARGET。

审查者先只接收 MODEL 和精确待证 statement，不读取作者 clock/front 正文，
自主重构触发刻画、非法修复和预算。第一独立重构使用“最右侧、此前有反位的
首位同位玩家”作修复；随后单独核对作者的“最早反位玩家”修复，两者均成立。
保 front 抵消精化由主研究者提出后，再由审查者独立重构并逐资源攻击。
其后才读取下列冻结节和原始 fixture；完成独立 literal 实现与全状态重算后，
最后读取、运行作者 audit 交叉核验。

## 冻结范围和指纹

本次不审查同文件前面三个 Claim 的全部旧证明。冻结攻击范围是
[循环窗口前沿正文](../../../current/weighted_congestion/class_front_phase_quotient.md)
末尾“条件编译接口：全部同权类前沿出口到全状态非存在”整节，以及为解释
fixture 所需的第1节 literal 资源关联。

| 对象 | SHA256 |
| --- | --- |
| 完整冻结正文 | `2dbb74c727f1d54abdbaa80cec74e5fb1c6c0c47bba1a0cda9217fee7348b342` |
| 新增节独立冻结副本 | `6fdd32f7eaaed9e96e519ea67ca5174eff434f290c0aab2fd6c807aca68ff9b1` |
| 原始有理 fixture | `9baa739bd6193277d11afe1366aabf32134cedfc508c689ed3c00b560347b0bc` |
| 作者 audit | `3c08f5bc28b3261bbd55e0aa801ee31ab5b0e9c08f62af120140ec97cdff3ebb` |
| 独立 literal audit | `3875a534e33827c9d269c456952ab8c8ec69df704ecab4f70b64b2e6cc260bba` |

审查时底座 HEAD 为 `0c5a97b68ae086f7a4ae0d23a1e9dc811980cbb1`；新增节尚未
提交，因此正文的准确审查版本由内容 hash 而非该 HEAD 识别。新增节冻结副本
位于本轮 scratch 的 `front_compiler_section.md`。独立代码和首次 fixture
输出分别来自 `front_reconstruction/check_anchored_class_front.py` 与
`front_reconstruction/fixture_independent_output.json`；首次输出 hash 为
`7e7be9fd8e28d646a67e8c1d086a51801a6954325ea69c4b0a466fc53be996b2`。
规范迁入代码应保留相同源码字节；规范输出路径/command 可以不同，并应重新
生成新的冻结输出，不能原位改写首次输出以追认新 hash。

## 精确对象和一般证明的独立重构

玩家按非空有序类划分，每类内有相同正权，各类间权比任意。每人恰有两个
互异资源子集动作，标签 0/1。base 成本非负，所有状态、玩家的有限最大成本
为 B。front 是相邻 bit 变化至多一次，故每个类均有保 front 翻位；
product-front 有限非空。FC1 的 min-max 正性确实等价于每个 front 存在所述
严格改善。选择一条达到内部最大值的出口，令其公共 margin 下界为 eta。
有限性及前提给出 `0<eta<=B`，不需要把任何费用比写成 0/0。

对同类三元 `(0,j,k)` 加两条 fresh 资源，两动作的相位为 010/101 互补，
同费 `M[x/(3w_a)]^D`。资源系数 `M/(3w_a)^D` 在任意实数正权下合法，
不要求有理或跨类相近。负载是 `0,w_a,2w_a,3w_a` 中之一，没有外类用户。
每个非锚点参与 `n_a-2` 对，每个锚点参与 `binom(n_a-1,2)` 对，因此
`L=max_a binom(n_a-1,2)` 是逐玩家参与对数上界，不能误用为资源总数。

一个类非 front 当且仅当存在锚定 `b,1-b,b` 子序列。取第一个反于锚点的
位置 i；其后必有同锚点位置。对 i 参与的全部三元逐项看真实翻位：

| i 在三元中的位置 | 其他 bit 条件 | i 自己所用资源的用户数变化 |
| --- | --- | --- |
| 中间 | 末位同锚点 | `3 -> 1` |
| 中间 | 末位反锚点 | `2 -> 2` |
| 末位 | 中位在 i 之前，必同锚点 | `2 -> 2` |

至少一项为 `3->1`；没有新 incident 满载。修复后不必马上成为 front，
证明只需这条合法单人严格改善。其他玩家、其他类不同时重置。

令 `M=2 alpha B`、`delta=(2/3)^D`。标准条件

    delta <= eta/(4 alpha^2 B L)

给出保 front 所选边 margin 至少 `eta-alpha L M delta >= eta/2`，以及非法
修复边 margin 至少

    M-alpha B-alpha L M delta >= alpha B-eta/2 >= eta/2.

这里忽略的旧 base 和旧 clock 项都非负，因此不等式方向正确。两种状态
覆盖完整的原两动作纯状态空间，故是全状态非存在，强于只展示改善环。

## 抵消精化、端点和退化攻击

在任一保 front 边的参与三元中，mover 翻位前后各自资源的用户数为 n 与
`4-n`：他始终使用一侧，另外两位各在互补两侧之一。两端皆非触发，排除
`n=3` 与 `4-n=3`，所以两端精确为 `2->2`。这也覆盖锚点翻位，不仅覆盖
前沿的非锚点端点。两侧同费与同类同权均承重。

因此真实 clock margin 恰为 `-(alpha-1)r_i M delta`，`r_i<=L`。FC9 的

    delta <= 1/(4 alpha L),
    (alpha-1)L M delta <= eta/2

分别保证非法修复 margin 至少 `alpha B/2` 和保 front margin 至少 `eta/2`。
`alpha=1` 时第二式恒真，没有除以 `alpha-1`；D 可以不依赖 eta。
标准条件确实同时蕴含这两式，因为 `eta<=B` 且 `alpha-1<=alpha`。

已攻击并处理的边界：

- `n_a=1,2` 无锚定三元且所有局部状态皆 front；`L=0` 时 base 假设本身
  就是全状态严格改善覆盖，不应试算含 L 的对数。
- `B=0` 时全部 base margin 为0，严格前提不成立，不能把它代入构造。
- 允许某些零资源、旧空动作、常数资源。非负性保留；正 eta 防止全零实例
  偷入前提。只含常数费用的 base 在有限 front 图上有总个人成本的极小点，
  不会满足严格 front-cover 前提；条件定理在该类是空前提。
- 类权可相同，也可极端不等；时钟隔离及按自身类权归一化消去新增 D 的
  独立跨类权比参数。没有证明 B/eta 本身不受权谱影响。
- 保留全部旧资源，故原两动作互异仍然互异。没有借助重复标签制造偏离。
- 新增资源与旧资源及其他三元资源均 fresh。不能把该结论套到混用资源、
  不同费 pair、类内不同权或非固定首位锚点的任意三元集合。
- 总费用次数是 `q=max(p,D)`。不能把新增 D 单独称为输出次数。

## 独立 literal 计算与作者交叉

规范输入为
[全前沿出口有理输入](../../../../examples/weighted_congestion/class_front_allstate_compiler.json)。
独立代码不导入作者 audit、旧时钟实现、压缩相位表或发现 LP。它用 class-major
玩家编号，作者用 clone-major 编号，双方按同一 literal 定义独立生成 incidence；
独立代码显式生成每条资源、每名玩家的两套资源子集，并按所有真实当前用户
重新求和负载、费用和偏离后成本。

首次运行命令：

```bash
python3 /workspace/scratch/2600475f1aa1/front_reconstruction/check_anchored_class_front.py --input /workspace/scratch/2600475f1aa1/co-work-anl-boss3/examples/weighted_congestion/class_front_allstate_compiler.json --output /workspace/scratch/2600475f1aa1/front_reconstruction/fixture_independent_output.json
```

规范重放入口为
`tests/audits/weighted_congestion/cyclic_clone/independent_front_allstate_compiler.py`；
`--input` 指向显式 fixture，`--output` 必须为新路径，程序拒绝覆盖已有记录。
有理幂逐项比较选择 D，没有浮点对数或舍入证书。

独立重算得到 `B=16553910168/815730721` 和
`eta=1410469765084842635603/1070401852096200000000`，与正文一致。基体确有
36个资源、512个状态，其中216个 front 全有出口；基体仍有16个 alpha-PNE，
因此新增时钟的全状态覆盖不是无效的空演示。

| 预算 | 最小满足该预算的正整数 D | 实际输出次数 | 时钟资源数 | 全态 alpha-PNE 数 |
| --- | --- | --- | --- | --- |
| 标准 uniform | 11 | 11 | 6 | 0 |
| 分离 refined | 4 | 8 | 6 | 0 |

每套都直接核验4608条真实偏离，并检查216条按 base 最大 margin 选择的
front 出口，以及384条逐非法类修复边的 margin 至少 eta/2。
两套全状态最佳 margin 的最小值分别为

    1384101225510570635603/1070401852096200000000,
    959938545952554635603/1070401852096200000000.

完成独立输出后才读取作者代码，并把作者 audit 输出保存到新的 scratch 路径。
双方 `B,eta,base_resources,front_states,D,q` 及上述两条最小最佳 margin 完全一致。
独立审计额外对8组参数分别运行 standard/refined：包括1/2/3/4/5大小的类、多类、
跨类权比达到 `10^80`、`alpha=1,5/4,3/2,7/3,10`，并对每条保 front 边验证
逐资源 `2w->2w` 恒等式，对每条非法修复边验证 `3->1` 或 `2->2`。
零费用与私有常数费用边界也用实际资源集重算，而非把任意成本表当成拥塞博弈。

这些有限结果只审计代码、输入与一般证明的边界；全实数权、任意类宽、任意
base 的一般结论仍由上述证明承担。没有以有限搜索替代证明。

## 增长义务与最终状态

本节没有提供满足以下要求的增长族：全部 product-front 出口、正真实余量、
以及输出实际次数 q 下 `alpha ln(q)/q` 无界。正文列出的充分效率目标
`alpha->infinity, p=O(alpha), ln(alpha^2 B L/eta)=O(alpha)` 的条件蕴含正确：
标准预算给 `q=O(alpha)`，而 `L>=1, eta<=B` 又给
`D>=ln(4alpha^2)/ln(3/2)->infinity`；因此
`alpha ln(q)/q >= c ln(q)->infinity`。它是未实现的充分目标，不是对任何现有
输入族的参数估计，也不声称必要性。

**Scope PASS。** 未发现冻结范围内尚成立的实质反驳。Truth 是一般条件接口，
Value 是把全状态覆盖转移到前沿覆盖并给出可核验次数预算，Mechanism 是
同类等权的触发修复与保前沿精确抵消。外审、新颖性与增长族均未获得；唯一
全类匹配上界判定保持 OPEN。

## 规范集成后的最终复核

正文完整 SHA256 仍为
`2dbb74c727f1d54abdbaa80cec74e5fb1c6c0c47bba1a0cda9217fee7348b342`，
与本次冻结攻击对象相同，没有在审查后改写数学陈述。
独立 canonical 源与原 scratch 源逐字节相同，仍为
`3875a534e33827c9d269c456952ab8c8ec69df704ecab4f70b64b2e6cc260bba`。

作者 canonical 源增加了且只增加了三行：从已计算的全部 base 状态中按
真实全部偏离筛出 base alpha-PNE、断言它们全部在 product-front 之外、输出
其数量和状态列表。删去这三行后的源码 SHA256 精确恢复为首次审查的
`3c08f5bc28b3261bbd55e0aa801ee31ab5b0e9c08f62af120140ec97cdff3ebb`，
所以补增不包含任何费用计算、参数选择或原断言的隐式修改。actual coefficient
核对和指定出口 margin 至少 eta/2 的断言已存在于首次审查版本中。

审查者已运行两条 canonical audit 向新的 scratch 路径重放；与以下 canonical
冻结输出比较，只去掉运行命令 `command` 字段后，全 JSON 完全相同。
还把作者 clone-major 编号下的16个 base PNE 列表转为独立实现的 class-major
编号，逐态重新按实际资源和所有偏离重建，集合完全一致，且全部非 front。
两路规范输出中的共同精确参数和所有全状态最小最佳 margin 同样一致。

| 最终规范对象 | SHA256 |
| --- | --- |
| 作者 audit `verify_front_allstate_compiler.py` | `680ef3a91de571c9b319d4c5f58f455cfbe6120bf1ae49ad7a6ee38ba28937b2` |
| 独立 audit `independent_front_allstate_compiler.py` | `3875a534e33827c9d269c456952ab8c8ec69df704ecab4f70b64b2e6cc260bba` |
| 作者输出 `front_allstate_compiler_author.json` | `54787908a53620a540ff8d5d8d61afe93bcdca75d17dd0fa1d8446927ed4cfbb` |
| 独立输出 `front_allstate_compiler_independent.json` | `0784881077df88c1b2715cab6f6b4d48f35a9cf540b833e4b7f5a3b4d13cbc01` |

首次正文、源码及输出 hash 仍在前文保留，不由这些集成 hash 替换。最终复核
没有发现新的 fatal objection；Scope PASS 不改变任何增长族或全类问题的状态。
