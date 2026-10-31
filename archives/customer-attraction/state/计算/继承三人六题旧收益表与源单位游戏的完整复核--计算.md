---
id: customer-attraction/inherited-three-player-six-topic-old-table-and-source-unit-game-audit
kind: computation
type_tag: 计算
title: 继承三人六题旧收益表与源单位游戏的完整复核
status: 原4669B验证器在真实21199B旧输入上首次完整一次exit0；0LP
summary: 补足KO/LH仅两J行之外的旧全表和真实源游戏检查，旧53三支持违反与新56精确区分，全部原有理点/动作/客户类型与真实stdout事件保全。
source_refs:
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-fa8dd4ddea574a74a634ebc71e6f9ccb/tree_coupling/all_pair_identities_obstruction_candidate.json
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-fa8dd4ddea574a74a634ebc71e6f9ccb/continue_coupling/verify_all_pair_obstruction.py
---

# 继承三人六题旧收益表与源单位游戏的完整复核

## 精确输入及先前证据没有核的内容

OLD为21199B/n3/p6/seed6611/trial206 JSON，SHA256 `2b7b872eca61c5fb4f23a6b8ee6791bea0853b57e2e8adae60f9b407a6cd8aee`。它的126有理收益、43动作、63源客户重数全部完整实读，原字节见[源清单](../../tools/evidence/inherited-obstruction-and-coordination-interfaces-primary/source-manifest.json)。原4669B verifier SHA256 `423ee2e9a47f5cf781ea4dbd36e3a3b769db565f5de2367e99c73ec77069236d`只有标准库，不导生成器/优化器/规范CAG核心。

KO/LH先前从这张旧表只取两J行作平方−3/13；它们未执行helper.main。其新CG点完整审计的56三支持违反也不是这张OLD的全表检查。本次主源需要补齐旧代码其余明确任务，故在一个新空run/source-root保原research/workspaces/R-fa8…/continue_coupling与tree_coupling布局，原main**实际一次**exit0/约0.222秒，stderr空，源/输入前后SHA相同，显式PYTHONOPTIMIZE0启用断言。见[完整事件](../../tools/evidence/inherited-obstruction-and-coordination-interfaces-primary/runs/inherited-old-pair/event.json)。没有原LP、随机、网络或子Git。

## 同一动作表在两种收益资料上的作用

主题编号0…5，根行动5；第二位在首动作0/1/2/3/4/5后分别3/3/3/5/3/3。末位完整表如下，每格为动作：

| 首/次 | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|---:|
| 0 | 3 | 3 | 3 | 2 | 3 | 3 |
| 1 | 3 | 3 | 3 | 2 | 3 | 3 |
| 2 | 3 | 3 | 3 | 0 | 3 | 3 |
| 3 | 2 | 2 | 0 | 0 | 2 | 3 |
| 4 | 3 | 3 | 3 | 2 | 3 | 3 |
| 5 | 3 | 3 | 3 | 4 | 3 | 3 |

1+6+36=43有序节点，actual534，root计数000111。表对全部离轨历史指定动作，不只是计数型选择器。source_customer_weights按mask1…63顺序给不同单位客户重数，下列完整数组即真实源游戏输入（mask二进制第a位表示喜欢主题a）：

```json
[0, 0, 1, 0, 0, 0, 0, 8, 7, 0, 0, 3, 0, 9, 0, 0, 4, 7, 3, 0, 0, 0, 0, 6, 4, 3, 0, 6, 3, 4, 0, 0, 0, 0, 0, 7, 3, 0, 9, 0, 0, 0, 5, 6, 0, 0, 7, 0, 0, 0, 0, 0, 4, 0, 7, 0, 9, 0, 0, 0, 6, 0, 0]
```

原代码验证63项均非负整数。对当前已经占用的主题a，源游戏利润为Σ_(B含a)w_B/q(B)，分母正。抽象y是另一份126字段收益表，不等于这份源游戏利润。它们共用动作表；真实源游戏IC通过不能把抽象y自动变成真实游戏输入，抽象y的W1/目标27/13也不是源游戏福利/OPT声明。

## 原代码的完整检查

reconstruct列全3人6题的56计数，126(q,a)占用顶点；校验y唯一完整、非负，动作历史集合完整/动作范围合法。对每个非末历史h与每动作a，沿同一动作表真正terminal，不冻结actual后缀，分别检查抽象y的IC和上述真实source游戏IC。

锐稀释对同题的每个有序不同终局q/r，以全部63非空membership模式取κ=max r(B)/q(B)，核κy_(r,a)−y_(q,a)≥0。对每个(q,a)按support检查q·y只依并集支持（126检查含同终局不同占用题的重复），对二支持用3r y_(q,a)=rK_a+s(K_ab−K_b)。三支持按逐客户signed恒等式收集非零残差。实际输出：

| 旧输入任务 | 精确结果 |
|---|---:|
| 顶点/全部有序节点 | 126 / 43 |
| 抽象图IC（含self） | 258条，均非负 |
| 真实源单位游戏IC（含self） | 258条，均非负 |
| 同题锐稀释 | 2520条，均非负 |
| 二支持身份 | 60条，均零 |
| 按顶点支持守恒 | 126次，均零 |
| 根抽象W / 比较target012覆盖 | 1 / 27/13 |
| 非零三支持身份 | **53条**，首013/a0为−8/13 |

原main只print完整JSON，本次包装另存report.json，不说原代码自己写相邻报告。它输出全部53残差列表，原stdout及解析副本完整保于[run](../../tools/evidence/inherited-obstruction-and-coordination-interfaces-primary/runs/inherited-old-pair/report.json)，不是只保first。不存在同版旧冻结stdout/报告可供逐字节对比，故不虚称原历史report byte-match；只确认实际源/输入同冻结SHA和这一明确新事件成功。

## 与NEW的精确版本区别

NEW仍同43动作，126顶点相同，却修改13个收益字段，详见[完整字段差](../../tools/evidence/inherited-obstruction-and-coordination-interfaces-primary/old-new-exact-field-comparison.json)。OLD三支持失败53，NEW在先前独审中失败56，首残差恰都−8/13；不能因首值/根值/目标值相同合并数组或认证范围。NEW另含21势并通过420势行；本次旧helper不检查OLD的那些势，它本来无这组字段。旧平方−3/13已另排共同非负，三支持失败进一步排共同signed表示。

因此：同一动作表确为source单位游戏完整纯SPE；OLD抽象点也满足它的全部形式图/稀释/二支持条件；但OLD没有共同signed客户实现，绝不是一份单位客户half反例。一般客户几何和全SPE付款仍需额外结构，不以一次3人6题验证证明任意策略/人数/目录。原seed/trial仅生成来源字段，未重演随机发现过程或证明LP最优。
