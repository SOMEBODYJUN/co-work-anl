# 任意设施数共同目录：因子二存在、有限构造与高效算法前沿

研究对象是任意数量带标签设施共享同一有限位置目录、正权原子客户及完整精确客户续局。主证明在途允许同址设施内独立均匀混合，离轨允许不对称纯客户均衡；不能强制两侧使用同一对称菜单。精确条件成本、客户可达与默认续局从 [模型](model.md)读取。

本分支已给**所有设施数的因子二存在性**和**任意规范贪心占位的完整盒均衡有限构造**。一般二进制有理输入的位多项式构造仍开放；最佳普遍常数仍未确定。证明完成度、内部审查、代码与外审彼此分开；外部同行评审和包括未取得的后续学位论文在内的优先权核查尚未完成。

## 主要结论与证据状态

| 成果 | 精确结论与证明链 | 证据及实现边界 |
| --- | --- | --- |
| SC-K-2-E | 全局字典序极大 → 精确在轨 NE 与转移预算；结合原子装箱、离轨上界和完整续局，得所有 k 的因子二 | 完整内部证明、逆向重构和精确独立检查；有限构造不等于多项式算法 |
| SC-K-GREEDY-BOX-EXISTS / FINITE-2 | 重客户与单选客户冻结；交错阈值截断负载和归家计数势控制改善与修复微步，完整盒始终存在精确 NE | 独立内部审查完成；一般终止步数未证多项式；不留轨迹时有限实现用多项式空间 |
| SC-K-BOX-STRUCTURED-POLY-2 | 全盒存在性加个体关联 DP 或局部权值 DP，再接 BOX-TO-2 | 固定参数类的数学位多项式构造；DP 与导入的多项式离轨调度器尚无规范实现；旧命题保留原范围 |
| 等重轻客户流 | 无约束全局势极小自动满足完整盒与 H；与旧下盒流的优化解集相同 | 规范 Bellman–Ford 在轨选择器已有完整位界，拒绝不等可移动轻权；实际 CLI 离轨/默认仍有限改善 |
| 一般高效构造 | 已分离在轨选择、离轨补全、全局优化困难和局部 PLS 搜索 | 全局字典序或精确盒势最优困难不证明找任意因子二证书困难；一般输入问题保持开放 |
| 共单例保真接口 | 共单例仿射游戏实现于真实贪心盒；所有合法状态自动保盒、严格保 H，并保留偏离与指定动力学 | 两速度有普通源位多项式搜索归约；一般重数显式计入设施数，抽象有界输出带另论；不是求解器或困难性结论 |

## 按数学成果族阅读

1. 理解普遍因子二：读 [模型](model.md) → [统一存在证明](uniform_two.md) → [逆向审查](reverse_review.md)。丢失单设施源地点的客户必须保留，不能删掉 orphan-aware 预算。共同目录双设施下界仅因本类包含双设施而给普遍下界端；当前最佳常数处于 φ 与二之间。
2. 做一般高效算法：读 [算法前沿](polytime_frontier.md)与[贪心全盒有限构造](greedy_box_global_progress.md)，再按输入结构选流、DP、类型压缩、星或链。新版普遍全盒存在已取代旧深度二/两选项存在性假设；这些旧证明和快算法仍各自保留。
3. 改离轨补全：先读 BOX-TO-2 与单设施原池重置，再读 [自适应重置](adaptive_reset_floor.md) 和 [冻结超载](frozen_overload_completion.md)。后者允许静止设施超出偏离者上界，不要求全局统一 cap。
4. 判断某条路线是否被反例排除：先查固定占位、对称菜单、深度三势、盒内字典序和混合相关链的准确障碍，再选其他占位或证书。它们没有否定全盒存在性，也没有给一般搜索困难性。

## 全部分支数学正文

| 中文资产名 | 文件 | 数学内容与读取时机 |
| --- | --- | --- |
| [任意设施数共同目录的模型与完整续局量词](model.md) | `model.md` | 固定带标签设施、真实条件成本、同址独立均匀随机化和默认续局；所有多设施结论的定义入口。 |
| [任意设施数因子二及算法边界的精确命题账本](claims.md) | `claims.md` | 逐项给命题身份、依赖、证据与范围；区分普遍存在、有限构造、结构类多项式算法和障碍。 |
| [任意设施数因子二存在性的完整证明](uniform_two.md) | `uniform_two.md` | 以全局字典序极大、转移预算、原子装箱及离轨精确均衡组装完整续局；不声称一般多项式构造。 |
| [因子二存在证明的逆向重构与实质异议审查](reverse_review.md) | `reverse_review.md` | 从目标离轨上界反推证明义务，记录独立实现证据和异议；不等于外部同行评审。 |
| [任意规范贪心占位的完整盒均衡与有限构造](greedy_box_global_progress.md) | `greedy_box_global_progress.md` | 交错阈值势与归家计数证明完整盒总有精确客户 NE，修复过程有限终止；一般步数无多项式界。 |
| [因子二位多项式构造的算法族、接口与障碍](polytime_frontier.md) | `polytime_frontier.md` | 分开在轨选择与离轨补全；集中登记全局优化困难、PLS 局部搜索、贪心预算、重数类算法及具体反例。 |
| [等重可移动轻客户的无约束流均衡构造](equal_light_flow.md) | `equal_light_flow.md` | 证明无约束全局势最小解自动保完整盒和 H，给规范 Bellman–Ford 实现与位界；不同轻权仍开放。 |
| [盒均衡的客户类型压缩与参数化精确算法](type_compression.md) | `type_compression.md` | 以目录和权值类型压缩客户状态，给固定参数选择及有界目录、权值多样性的 XP 因子二构造。 |
| [有界关联树宽与客户度的盒均衡动态规划](bounded_incidence_box.md) | `bounded_incidence_box.md` | 在固定个体关联树宽和双侧客户度下精确选择完整盒 NE；站点邻接有界不能替代个体度约束。 |
| [站点树宽与局部权值多样性下的盒均衡动态规划](local_weight_box_dp.md) | `local_weight_box_dp.md` | 固定站点 primal 树宽和每站点关联轻权种类时给精确位多项式选择；每条边客户数可无界。 |
| [开站有向轻图深度至多二的盒均衡存在性](height_two_box.md) | `height_two_box.md` | 覆盖分叉、汇合和不等轻权；给存在论而非一般多项式受限势选择器，后由全盒定理扩展。 |
| [三站不等轻权开站链的盒均衡存在性](three_site_chain_box.md) | `three_site_chain_box.md` | 用上游原客户池的势交换证明盒内均衡；不独立给多项式选择器。 |
| [三轻客户汇合四站路径的有界步盒均衡构造](converging_path_box.md) | `converging_path_box.md` | 在汇合点下盒紧等条件下给有限步构造，处理非单向链取向；与后续四步扩展分别保留。 |
| [汇合四站轻路径的四步严格改善构造](converging_four_moves.md) | `converging_four_moves.md` | 在每边一名轻客户条件下移除旧构造的汇合点紧等与部分重数相等假设。 |
| [指向晚开中心的不等轻权星形盒均衡算法](inward_star_box.md) | `inward_star_box.md` | 以队列处理朝晚开中心的轻边；容许中心任意多不同轻权，补足另一取向星形算法。 |
| [自适应原池重置与强制客户下界的离轨补全](adaptive_reset_floor.md) | `adaptive_reset_floor.md` | 由纯均衡的强制客户 floor 放宽源删除上界，严格扩展双 LPT 识别；无全输入识别保证。 |
| [冻结静止超载与偏离者专属上界的多项式补全](frozen_overload_completion.md) | `frozen_overload_completion.md` | 允许非偏离设施保留高负载客户，以剩余强制 floor 和保持最大值的修复完成离轨均衡。 |
| [共单例仿射搜索到真实贪心盒的保真归约](complement_search_reduction.md) | `complement_search_reduction.md` | 保留重数、偏离和指定动力学；两速度有源位多项式归约，一般输出带区间另论，不提供通用求解器。 |
| [混合设施重数不能直接当作相关并行链速度](restricted_related_link_boundary.md) | `restricted_related_link_boundary.md` | 对比真实条件成本与相关链成本并给整数不一致例；正确共单例接口不等于一般复杂度下界。 |
| [固定字典序极大占位本身可逼近因子二](lexmax_boundary.md) | `lexmax_boundary.md` | 即使改选全部客户均衡和离轨续局，该选定占位仍可接近因子二，而另一占位有精确 SPE。 |
| [对称续局菜单的无界假威胁反例](symmetric_menu_obstruction.md) | `symmetric_menu_obstruction.md` | 全重数族使对称菜单威胁无界但原模型最优倍率为一，排除把菜单受限失败当作模型下界。 |
| [深度三贪心树击败完整盒势最小选择器](depth_three_box_boundary.md) | `depth_three_box_boundary.md` | 给盒内均衡存在但特定受限势选择器失败的严格实例；不反驳贪心盒普遍存在性。 |
| [完整盒内字典序极大分配未必是客户均衡](boxed_lexmax_boundary.md) | `boxed_lexmax_boundary.md` | 给严格贪心输入的特定字典序选择反例，限定在轨选择器而非一般因子二目标。 |

## 高效算法族之间的关系

[算法前沿](polytime_frontier.md)集中保留等重数、全异址、分量等重数、跨重数 range 检查、两站混合重数、all-or-one、嵌套锚、锚星、单向路径、原池重置及双 LPT。它们是不同充分条件，不可去掉条件后拼成一般算法：

- 等重数分量可导入受限相同链 Nashification；全异址已有因子二，早期因子三仍按历史身份保留。跨重数 range 证书放宽旧单站分量限制，容许部分轻客户跨重数。
- 两站不等重数分量用一次降权遍历；all-or-one 允许每个客户仅一个或整个分量的选项；嵌套锚再允许真正部分交叠，但逆序选项会击败无约束 list 规则，仍可能另有 NE。
- 等轻权流覆盖任意部分交叠与混合重数；普通下盒势直接扩到不等轻权会溢出上盒。星边、单向路径及汇合四步算法覆盖其他明确子类，不能由结构名猜测它们互相包含。
- 个体关联 DP 同时约束树宽与双侧个体度；局部权值 DP 约束站点 primal 树宽与每站点轻权种类，允许每边任意多客户。类型压缩另给参数化精确选择和有界目录/权值种类的 XP 构造。
- 单设施源重置使任何已供给的完整盒在轨 NE 都能接多项式离轨补全，无需旧 singleton 私有储备。自适应强制客户 floor 严格扩大原双 LPT 测试；冻结静止超载又扩大只管全局 cap 的接口。识别所有输入的有效证书仍无证明。

## 反例的准确否定范围

固定字典序极大占位可在所有客户均衡选择下逼近二，而另一占位有精确 SPE；因此亚二证明须允许改占位。标量装箱的等重饱和也只限制该接口。对称续局可制造无界表观威胁，却不妨碍原模型精确 SPE。

贪心修复的任意严格改善、最重改善优先、仅向更低重数移动、固定占位字典序最大及精确势全局最小，都有各自严格反例。某些坏在轨 NE 令真实偏离在所有混合离轨 NE 中超过二，但同一占位仍有其他好 NE；因此这些证据排除具体选择器。静态原站装箱的失败要求允许跨站重排，不能称为贪心占位失败。深度三和盒内 lexmax 反例同理。

混合重数的真实条件为 `(W_t−w_i)/q_t ≤ W_v/q_v`，不同于把 `q_t` 当相关链速度的公式；整数差异与文献适用边界见[专页](restricted_related_link_boundary.md)。[共单例归约](complement_search_reduction.md)给正确替代接口，但没有一般求解器。

## 规范程序、冻结证据与复核入口

规范包为 [multi_facility_spe](../../../multi_facility_spe)，核心 [two_exists.py](../../../multi_facility_spe/two_exists.py) 与 [CLI](../../../multi_facility_spe/__main__.py) 不改变双设施 API。普遍定理的实装和论文导入子程序分开：`greedy-box` 及 `equal-light-flow` CLI 的实际离轨和默认续局使用有限纯改善，尚未实装文献多项式调度器。

从仓库根运行下列命令，输出写入新文件，勿覆盖冻结证据：

```sh
python3 -m multi_facility_spe examples/multi_facility/greedy_box_global.json --method greedy-box --output greedy_box_certificate.json
python3 -m multi_facility_spe examples/multi_facility/equal_light_flow_complete.json --method equal-light-flow --output equal_flow_certificate.json
python3 -m multi_facility_spe.complement_reduction examples/multi_facility/complement_source_two_speed.json --output compiled_search.json
```

第三条输出是实例/搜索接口，不是 NE。[共单例复合审查](../../reviews/facility/complement_search_reduction.md)记录范围和更正；[等权流审计](../../reviews/facility/equal_weight_light_customer_flow.md)与[因子二证明审查](../../reviews/facility/arbitrary_facility_factor_two.md)分别记录实际增量与内部攻击。

[定义级检查](../../../tests/multi_facility/definition_check.py)直接重算条件成本；[构造审计](../../../tests/multi_facility/run_exact_audit.py)与[不导入构造器的逆向审计](../../../tests/multi_facility/run_reverse_audit.py)分别核对输出和有限小域全部 lexmax 平局/纯 NE。[冻结构造结果](../../../evidence/runs/kfac_two_exact.json)与[逆向结果](../../../evidence/runs/kfac_two_reverse.json)不作为普遍证明前提。

各专题还有 [自适应重置审计](../../../tests/audits/kfac_adaptive_reset.py)、[冻结超载审计](../../../tests/audits/kfac_frozen_overload.py)、[混合重数公式审计](../../../tests/audits/restricted_related_formula.py)、[星形审计](../../../tests/audits/kfac_star_edges.py)、[不等轻权势审计](../../../tests/audits/kfac_two_light_potential.py)及[贪心 cap 审计](../../../tests/audits/kfac_greedy_cap.py)。严格分离实例包括[双 LPT 三角形](../../../examples/multi_facility/greedy_double_lpt_triangle.json)、[星边输入](../../../examples/multi_facility/greedy_star_edges.json)及[两不等轻权势输入](../../../examples/multi_facility/greedy_two_light_potential.json)；修复顺序/最重改善见 examples/multi_facility 中相应输入及算法前沿。有限精确运算不会证明子类算法的普遍定理。

当前全盒来源是保留归属的原证明提取，所附 ZIP 未取得；这一来源缺失不等于现行证明缺失。精确状态查[分支账本](claims.md)、[全仓命题](../claims.md)及[五轴审查](../../review_status.json)。接续任务是[一般位多项式盒内选择](../../questions/greedy_box_polytime.md)，或者改善统一常数；也可换占位、换分配不变量或只控制偏离者的新证书，现有图不是方法白名单。
