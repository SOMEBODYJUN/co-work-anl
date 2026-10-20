# 选题前沿

状态：六线广搜与首轮精读正在进行，尚未选定最终数学主目标。

当前优先方向为原子博弈、Nash均衡、近似公平分配、广义指派近似算法。本次恢复自2ff22b9；六个gpt-6.1-sol / ultra已实际启动，并完整读取含用户全部本轮原话的共同指导。当前六线为：

- atomic_pne：近似纯均衡、势函数和结构扩类；
- nash_dynamics：player-specific singleton均衡选择、随机动态和结构化Nash比较；
- fair_goods：goods侧WEFX/MMS与公平—效率边界；
- fair_chores：chores/mixed及冲突/类别约束；
- gap_rounding：MaxGAP、成本保持依赖舍入与hard-budget公平；
- gap_structure：多资源MinGAP、结构参数和容量扩张。

前一轮六线名称只作当时分工，不视为已保存候选。当前跨线battle已启动；以实际卡片、原文和精确实验为准，不用公屏口头计数替代资产。此前连续优化候选保留，暂不主攻。

首个新范围内可恢复试攻是[公平—分数效率兼容探针](notes/fair_fpo_compatibility_boundary.md)：已知两代理两物品类型反例由两种独立Fraction oracle复现。不是新反例或新定理；作用是排除未经核实的一般兼容目标，检验参数分类是否还有值得研究的差额。

需要减少的不确定性：原文是否明确提出；最新是否已解；候选是否只是直接推论；最小toy能否暴露核心机制；小结果能否扩成完整而不虚构价值的成果包。

下一行动：收齐独立卡片，交叉battle，核验前排来源与实际实验。不要把paper count、打分或通过软件检查称为数学进展。

## 首个实质试攻：CS-THETA-EXACT-v1

[等长多路theta图相关间隙](notes/combinatorial_equal_theta_correlation.md)已有覆盖所有整数路径数和共同长度的有限有理公式及证明草案。核心是原文Thm4.3的支持紧性、删除桥、路径内AM–GM及两坐标平方差凸性；全base约化曾遗漏restrictions，已由交叉攻击修正。状态是证明候选，新颖性和后置全面审查未完成。

[root独立探针](probes/equal_theta_independent.py)使用union-find逐子集秩、Fraction精确期望、所有rank不等式及全联合分布LP，与路径公式分开重构；[冻结输出](probes/results/equal_theta_independent_20261020.json)保存正常/零/自由拟阵/非法图边界与环境。有限核查不证明全公式。

六路仍在扩充不同论文族并写候选卡；不要将该首个可推导细胞直接变成唯一主目标。下一义务是跨线比较完整成果包，核验更一般series-extension覆盖，再决定投入。

## 本轮恢复后已核实的保存缺口

远端基线528c8d6含theta候选和探针，尚无完整候选池与六线比较正文。历史口头的“共同最坏分布”“幂网络误差界”不足以恢复精确身份，须重查原文，不能臆补。当前六个gpt-6.1-sol ultra研究员已实际启动，分别完整读取用户指导，正在及时写lanes/。先行随机鲁棒卡已发现固定均值W∞球凸序极值被Gerhold–Gülüm Prop.3.2覆盖；W1及历史标签仍待独立核验。

即时动作：逐批保存稳定候选卡；对前排做原文与后续核查，收到具体跨线异议后更新排序。旧题、旧口头候选数和模型赞同不作为本轮已保存成果。
