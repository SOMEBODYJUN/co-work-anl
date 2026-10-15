# 固定主玩家后的异权轻玩家阈值势

固定hub子游戏的FIP/精确响应存在是Milchtaich(1996)两策略定理的直接应用；本文提供所写拓扑的显式阈值势与one-pass接口重构，不作为新的存在定理。仅给固定hub响应接口，不给全类存在界，未认证阈值表示或选态过程的新颖性。

## 命题身份

- **ID/version：** `WC-FIXED-HUB-LIGHT-THRESHOLD-RESPONSE-v1`。
- **中文数学名称：** 固定主玩家后的异权轻玩家阈值序势与有序删除响应。
- **Objects / Domain：** [共享侧资源正文](shared_side_truncated_potential.md)第1节的有限 unique-light / unique-source 拓扑，但允许hub异权a_v>0，费用次数域为任意整数d>=0。每个hub和light各有两个所写资源子集动作；每条side有唯一light及任意hub用户子集，副本费用相同。所有费用为非负实系数次数至多d的多项式。light权为任意实正数，允许任意多权类。允许空light集、空side hub集、零费用和常数项。
- **Quantifiers / Assumptions：** 对每个该拓扑游戏和每个全部hub动作向量h，固定hub的真实动作，只允许light单方移动；不假设任何UF，不把light约束为全anti。每条side只有唯一light、每light只有唯一main source均为承重条件。
- **Definitions / Scope：** 固定hub后的light子游戏以原真实负载重算light偏离成本。每source在下文按其hub所在副本重新记位0；(1)的W包含偏离者自己的权重。结论只关于冻结hub动作后的子游戏，不是hub与light同时选态的原游戏。
- **Exact Statement / Conclusion：** 该子游戏具有由(2)/(4)逐source相加给出的实值序势，真实严格改善当且仅当势严格下降，真实成本打平当且仅当势打平。因此其每个单light势局部最小点恰为精确light PNE，全部严格light改善路径终止。下述有序删除过程还给一个精确light响应，且每名light至多作一次严格移动。
- **Dependencies：** MODEL真实负载；非恒定非负系数多项式在非负半轴严格递增；有限实数有序集合；二次式展开；有限状态局部最小。下文显式重构不靠外部存在定理来完成证明，但存在/FIP部分的文献身份必须另记为Milchtaich(1996)已知定理的直接应用。multi-light反边界复用已有异权side-only审查§4；hub重选不能lift的边界复用共享侧正文§9.17。
- **Evidence：** 下述全实参数自足重构，作者literal `Fraction`审计（全部资源直接重建、所有light边、局部最小点及one-pass路径），及已逐项核对的primary文献两策略FIP与正权扩展；独立审查另行记录，先重构后冻结攻击及精确核验状态见末节。
- **Counterevidence / Objections：** 多light共享side时固定hub的exact light响应可失败；精确light响应的存在及重选后hub成本的稳定均不保证真实冻结light的hub偏离稳定。尚无可累加hub重置预算。
- **Status：** complete reconstruction of a known existence/FIP corollary; independently reconstructed and exactly audited; unrefereed。Truth仅上述冻结子游戏；Value为无UF真实light选态接口；Mechanism为异权阈值序势和非降阈值删除；Novelty未认证，存在/FIP明确不是新结论；Ambition保留唯一全类题OPEN。
- **Related Files：** 本稿及`fixed_hub_light_threshold.py`；规范正文`research/current/weighted_congestion/shared_side_truncated_potential.md`；已有范围攻击`research/reviews/weighted_congestion/heterogeneous_hub_sorted_side_review.md`§4。实际冻结审查及规范代码/证据见本稿末节。

## 精确陈述与证明概览

采用共享侧资源正文第1节的 unique-light / unique-source 拓扑：每条 side 只有唯一 light，但可含任意多个 hub；hub 可异权；所有费用均为非负系数多项式，允许次数零、零费用与常数项。不假设任何 UF。固定所有 hub 的实际动作后，light 子博弈具有一个显式有限阈值二次广义序势，因此每条严格 light 改善路径终止，且至少有一个所有 light 均精确稳定的状态。

各 source 的 light 集彼此不相互作用：主资源按 source 分离，每条 side 只有唯一 light。所以下面只证明一组 source。该结论对多 light 共享 side 不作断言。

## 任意单 source 的精确构造

把该 source hub 的动作重新标为0，其权为 a>0；该 source light 集为 I，正权 w_i，总权 W。固定其他所有 hub 位后，light i 在动作 b 的全部 side 成本是确定常数 q_i^b>=0：每条 side 的实际负载是 w_i 加该副本上固定 hub 权之和，不依赖任何其他 light。

若其他 light 在动作0上的总权为 x，则 i 使用0与使用1的真实成本差恰为

    D_i(x)=F(a+x+w_i)+q_i^0-F(W-x)-q_i^1.           (1)

只在有限可达集合 X_i={sum_{j in S}w_j:S subset I\{i}} 上使用它。这里 W-x 是 i 偏离到1以后包括自身的真实主资源负载，不能替换成 W-w_i-x。

若 F 非常数，非负系数使 F 在非负半轴严格递增，因此 D_i(x) 严格递增。于是可选实数 t_i，使对每个 x in X_i，sgn(x-t_i)=sgn(D_i(x))：若某个 D_i(x)=0，取 t_i=x；否则取最大负值点与最小正值点之间任一点，缺负值点时取小于 min X_i，缺正值点时取大于 max X_i。若有非空负/正两部分，其端点有严格间隙。

对 light 动作0的集合 S，令 L(S)=sum_{i in S}w_i，并定义

    Psi(S)=L(S)^2/2-sum_{i in S}w_i(t_i+w_i/2).     (2)

对 i notin S，令 x=L(S)，直接展开给出

    Psi(S union {i})-Psi(S)=w_i(x-t_i).             (3)

其符号与真实成本差 D_i(x) 相同。反向移除的符号相反。因此 (2) 是严格意义的序势：严格改善当且仅当势严格下降，成本打平当且仅当势打平。有限空间中每个单 light 局部最小点恰是该 source 子游戏的精确 PNE。

若 F 为常数（包含 F=0），主资源费用抵消，令 d_i=q_i^0-q_i^1。取

    Psi(S)=sum_{i in S}d_i.                        (4)

加入 i 的势差恰为真实成本差 d_i；这同时覆盖 d_i=0 的全平情形，不能硬套二次阈值来伪造平局。

将各 source 的 Psi 相加即得固定全部 hub 位的整个 light 子游戏序势。无 light 的 source 贡献零。

## 每名轻玩家至多移动一次的有序删除选态

不必优化二次势或运行反复最佳响应。非常数 F 的每组先将全部 light 放在动作0，按 t_i 非降排列（打平任意），记当前动作0总权 L。扫描 i：若 L>t_i+w_i，就把 i 移到1；否则保留。每次删除确为真实严格改善，由 D_i(L-w_i)>0；每名 light 至多移动一次。

被保留的 i 在被扫描时满足 L<=t_i+w_i；以后 L 只降，因此最终不想移出。被移出的 i 在当时删除后有新 L>t_i；以后若删除 j，由扫描次序 t_j>=t_i，删除后的新 L>t_j>=t_i；所以 i 始终不会想移回，最终有 L>=t_i。所有 light 都精确稳定。常数 F 时逐名独立选 q_i^b 较小动作即可。

这个选态过程只用已确定阈值及排序，最多 |I| 次严格移动；不是输入位复杂度的多项式时间断言。有限可达集合构造阈值本身可指数大，实系数的根/排序也不能凭符号写法默认可计算。

## multi-light side 的精确反边界

直接复用已有`heterogeneous_hub_sorted_side_review.md`§4的异权side-only例，而非另造一个近义资产。将其中三名hub重标为3名light，权为(1,2,3)；增添一个任意正权hub，所有light的source均为它，主费用F=0，新hub不参加任何side。三个互补side副本对的light用户集依次为{1,2}、{1,3}、{2,3}，费用依次为2100x²、1130x²、499x²。每个light位b都用其所参加side的1-b副本；统一交换两副本名字保持原side-only全部真实成本。该实例合法属于正文§8.1的multi-light拓扑，但不满足任何正强迫UF。

整体补位对称下，四个代表状态的真实成本和严格改善为：

| light状态 | 全成本(C1,C2,C3) | 指定改善者 | 当前/偏离成本 |
| --- | --- | --- | --- |
| 000 | (36980,31375,30555) | 1 | 3698/323 |
| 001 | (20030,20896,14661) | 2 | 20896/20875 |
| 010 | (20180,10396,22571) | 1 | 2018/2003 |
| 011 | (3230,20875,22645) | 3 | 22645/22571 |

逐玩家枚举确认实例最佳均衡因子仍恰为已有20896/20875；在该端点有近似PNE，在所有更小倍率无PNE。特别固定全部hub后light子游戏没有exactPNE。这个反例只用于unique-light承重范围，不是新增长下界；每个资源仅2light，旧资源支持定理仍给2PNE。

## 作用和准确缺口

该接口消除了 unique-light side 子类在 UF 失败时“固定 hub 后是否存在真实稳定 light 选态”的局部义务，允许任意多 light 权类；它不是强迫 light 全 anti。改变 hub 位后，q_i^b 与阈值 t_i 都会改变，Psi_h 是不同势，不能无证望远镜求和。

更关键的是，hub 的真实单方偏离冻结 light 动作；先把 light 重置到另一个精确均衡后再比较 hub 成本，是另一种偏离合同。共享侧资源正文§9.17的两玩家无精确PNE实例已经给出反例：每个固定hub位都有精确light响应，重置后的hub成本由整体补位对称性相同，但真实冻结light的hub翻位仍严格改善。因此“约化后hub稳定”不能直接lift。需要控制冻结响应与重置响应的真实预算，或为每个 h 的多值light均衡选择证明新的兼容机制。

## 文献事实、精确应用与本文件的重构用途

独立审查者指出文献入口后，作者于2026-10-15自行打开并核对Igal Milchtaich, *Congestion Games with Player-Specific Payoff Functions*, Games and Economic Behavior 13 (1996), 111–124，primary扫描PDF：https://www.cs.cornell.edu/courses/cs684/2005fa/milchtaich.pdf 。

**Paper Fact：** §4 Theorem1印刷页114证明共同策略数为2的player-specific singleton congestion games具有FIP。§8印刷页121引入任意正实权beta_i，以同策略玩家权和作为拥塞，并明确该Theorem1证明仍适用；印刷页123汇总表的weighted/two-strategies格也登记FIP。这里不把§6仅无权的一般多策略存在定理外推到有权多策略。

**Interpretation / 精确应用：** 固定全部hub后，对某source组，把每light在副本0/1的player-specific单资源成本分别写成

    f_i0(z)=F(a+z)+q_i0,  f_i1(z)=F(z)+q_i1,

其中z是选择同副本的light总权，包含自己。它们均非减；取负号即文献的非增payoff，任意正w_i对应beta_i；每名light可用同两个副本，无跨source light耦合。故每组直接满足文献weighted two-strategies合同，FIP和exact response存在是已知定理的推论。费用可零/常数、payoff可打平与文献弱单调合同相容；空组直接处理。

**本稿重构用途：** 式(1)至(4)在该拓扑下把已知FIP机制显式写成可审计二次阈值势，并给阈值排序后的单向删除过程；不将已知存在性包装成新定理。没有对该显式表示或过程做完全球新颖性检索。

另查过primary入口Mavronicolas–Milchtaich–Monien–Tiemann, *Congestion Games with Player-Specific Constants*, MFCS2007，作者PDF https://econ.biu.ac.il/sites/econ/files/shared/staff/u36/papers/constants.pdf ，其引言区分weighted/player-specific singleton模型，§3研究并行链。此处不把其三资源结论无证外推。上述自足证明并不需要这篇后续文献来完成。

## 复验

配套 `fixed_hub_light_threshold.py` 使用 Fraction，只在可达其他玩家总权上构造有理 t_i，逐状态核验式(1)、(3)、真实成本差与势差符号、全部局部最小点、有向改善图，以及有序删除的每步严格改善和最终响应。它从完整资源逐项重建成本，不只验证抽象阈值式。有限实验不是实参数证明。

## 规范审查与复验路径

本稿的数学冻结为 `4a071681b6ddbe0babafd6ea3ad03842f6a8da8dba262b4d1de93e2be1c3be60`；正式整合只改临时身份、相对链接、状态和本节路径，成本式、量词、阈值势、删除构造及反边界不变。[独立审查](../../reviews/weighted_congestion/fixed_hub_light_threshold_review.md)先据精确陈述自主重构，再攻击冻结稿并发现Milchtaich的准确文献身份；本稿已据此核实并区分Paper Fact与自足重构。范围内无尚成立fatal objection，未外审，未认证新颖性。

在仓库根运行以下程序，仅向stdout输出JSON，重跑另存临时文件：

- `python3 tests/audits/weighted_congestion/verify_fixed_hub_light_threshold.py`；作者路，冻结结果 `evidence/runs/weighted_congestion/fixed_hub_light_response/author.json`。
- `python3 tests/audits/weighted_congestion/independent_fixed_hub_light_threshold.py`；审查者独立literal与成对势实现，冻结结果 `evidence/runs/weighted_congestion/fixed_hub_light_response/independent.json`。

两份JSON含实际输入、seed、Python、Fraction算术、源码hash及有限覆盖范围，固定hub状态逐一重建资源负载。完整多light反边界只复用既有例，不新立重复反例身份。有限检查不替一般实参数证明。
