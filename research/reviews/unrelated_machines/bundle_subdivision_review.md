# 成束任务强化与细分障碍的独立重构及冻结攻击

本次由boss2汇集内部子研究者`coupling_hierarchy`、`constructive_exchange`与主研究者的实际推导。先分别重构关键瓶颈，再审冻结稿；不是赞同投票。UM-TARGET-v1仍OPEN。

## 冻结对象与覆盖

基线来源提交：`176ecd8b1051009aee19b8433e1b961ce66ae72b`。最终正文/代码SHA256：

| 路径 | SHA256 |
| --- | --- |
| `research/current/unrelated_machines/bundle_coupling_subdivision_barrier.md` | `f923212d74e42ac3b32c09d73e15382dd656e90e10b39ea22bc4fa29559cd894` |
| `tests/audits/unrelated_machines/pair_coupling_subdivision.py` | `6d488c8edc2b2c597a24f063468ff1714ef55c052ab529d2ce60df5dd9e64148` |
| `tests/audits/unrelated_machines/cardinality_closure.py` | `ce176ca14d24e9f9b3ebda3eddba65dbbb851a23811729b1a6c9e7d9f9f7ee37` |
| `tests/audits/unrelated_machines/independent_pair_coupling.py` | `801e016e773f5abfd4d33f511a2f0d6e1d97d3889edcf177033fafab39ed3945` |

独立重构先于正文：coupling_hierarchy先只依据精确目标重建了末端bundle的二阶互补等式、非负支撑强制、单共享任务的条件耦合、细分压回与零值限制；其后阅读第2、4、5节。第一次被审正文hash为`875f6d1193674affa84af48ee1b0f3e22fb7add984d37567cd3f01c9ec94640b`；后续第3节由计数过滤器作者改为forced residual版本，主研究者独立重构并逐步攻击新增单调性与总复杂度。最终增加的二分下界与同行重叠说明由主研究者复核，不能宣称最初审查者看过这些新增段落。

## 承重攻击与结论

* 二阶约束：逐任务指示恒等式有效；聚合右侧为0确实强制父端每个正支撑配置含至少k−1条small。阈值严格小于θ时不含incoming，之后逐层覆盖矛盾，θ端点由真实调度达到。没有把期望界当逐支撑结论。
* 删边健全性：候选任务j必须从自身强制负载和全部束中排除；不同v只对域恰为{i,v}的任务收费，互不重叠。使用R_v=T−F_v，阈值为严格大于；零值与等号不错误强制。同步轮每个删边均单独安全，最多E次成功删边。
* 单调性：h从二元束被迫到v时，以q降为q−1保留旧reserve，关键不等式(R_v−p_vh)/q<R_v/(q+1)正确；被迫到i时强制负载补偿原reserve损失。j自身域收缩不造成重复计算。用T直接代替R_v虽然仍健全，却不保证目标单调，已放弃该弱版本而未静默沿用它的二分结论。
* 位复杂度：审查分别核对轮数、每轮候选/束/q/排序项数、分母积位长、整数二分次数。下界B不是调度输出，不升级为近似算法。
* 两机器耦合：零概率条件块质量为0；逐行逐列边际重算正确。每对有联合分布并不推出全局分布；本文未误作该推断。
* 细分：必须以C<2H压回，H≤OPT≤2H时保OPT；OPT<H的等式不成立，正文给原OPT0、新OPT1反例。T≥H才能提升配置。目标阈值只给T_PAIR≤T_k，分母方向与supremum论证正确。

在以上最终正文实际声明范围内，主研究者未发现仍成立的fatal objection。第2、4、5节有另一子研究者独立重构与冻结攻击；第3节有主研究者对作者推导的独立重建和精确oracle检查，不冒称整个包经历外部同行评审。

## 实际执行的有限证据

规范审计展开k=2,3,4；k=2,3对细分实例分别枚举1024和16384个全部合法调度，并逐一核验C<2时的压回；k=4检查真实243机器338任务配置证书及全部29403个机器对的coupling，未枚举该实例整数最优值。原bundle单对残差也由实际配置计算。

过滤器审计枚举7689个矩阵与7个目标，共53823合同；逐一保留115799个T可行实际调度，记录7232次边删除。另含空任务、全零、单可用机器、大分母和二分下界。对原/全细分VW k=2,3,4检验给定阈值，前两参数全分配独立oracle；k=4只使用正文的一般上下界证明。

独立程序不导入规范舍入、细分或耦合核心：260个小实例逐调度求OPT，113个H≤OPT≤2H的实例保持OPT；5个概率边界；k=4,…,12枚举全部局部bitmask和阈值断点/内部点。经典baseline也另行重跑，作为未改动地基的复现而不是新Claim证据。

完整参数、版本、命令、实际JSON及哈希在`evidence/runs/unrelated_machines/bundle_subdivision_audit.json`。有限计算不证明一般命题。

## 非致命限制与来源关系

规范expanded_exhaustive只接受本次调用H=1；certificate/pair_distribution是受控审计组件，不是完整外部输入验证产品。条件耦合、细分等属于基本工具，原创性与独立论文价值未认证。boss4的长链推广是同存档独立重叠发现，应交叉引用并复用其更强共同结果，而不重复宣称另一新反例族。该消息不涉及多机器overlap一致性的全部hierarchy。

## 安全同步后的复核

同步合入同行`8701a61`，逐条阅读long_path_coalition_gap.md与其冻结审查。源账本中不同ID/path的新增条目均保留；数学身份无合并改写。本文末尾新增共同更强结果的交叉引用，未变更第2–5节推导。最终正文SHA256为`bbbfb292f4ce3cd02eb87864524add850075f20b938f3b9aaef0a2e54b765222`；前表及冻结证据保留引用前版本的准确哈希，不冒称字节未变。数学状态仍仅为已声明范围内内部可用。
