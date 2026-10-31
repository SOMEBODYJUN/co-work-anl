# 覆盖矩表示、真实行的线性空间及正性边界

Boss7研究备份，2026-10-21。一般 Q-CAG-HALF 仍 **OPEN**。本目录不修改共享数学身份；下列命题为内部研究证明。CR-2/CR-3已有从定义重构的[独立审查](../independent_mechanism/coverage_representation_independent_review.md)，并已按其边界意见修订；无外审或全球新颖性认证。

- `coverage_moment_geometry.md`：固定人数终局收益的覆盖矩表示；任意完整策略的全部真实比较行具有同一个余维一线性空间；全数值资料的非负生成器障碍；合法SPE上的OPT外客户消除障碍；允许依实例稀疏化的一般归约；末层不等式虽span充分却无法代替全树激励的精确方向例。
- `audit_coverage_geometry.py`：标准库 Fraction 从定义核验收益、势、覆盖空间的精确秩、正系数积分、暴露函数、完整策略行和合法不交主题实例。
- `coverage_geometry_audit.json`：上述脚本的冻结输出。
- `positive_moment_locality.md`：后续独立备份PM-1–PM-3。给任意规模anchor正矩dual；固定m=2的全部真子目录都可实现、全局却不可实现的无界标签族；精确说明此全局正预算无法由真子目录正预算非负相加得到。一般half仍缺真实跨分支乘子λ，未因此闭合。
- `audit_positive_moment_locality.py`、`positive_moment_locality_audit.json`：从覆盖定义枚举r=1,…,6的21,834个非空类型，明确构造两类局部有理客户模型并核验502个单/双矩；独立于已冻结coverage审计。

来源核查：旧 `R-7e9f44beea424d469713364afe7dd180/full_tree_dual/` 当前含收益图/SCC稿，未找到所提coverage-span稿，故不据消息把它认作已核验资产。共享 `mobius_compiler.md` 已有Boolean势的双Möbius反演、正偏置编译及固定人数匿名势约束；本稿引用其势—收益恒等式背景，不声称谐和势工具或覆盖线性表示有外部新颖性。新研究重点是**任意完整策略的行span不依策略**及**准确区分线性压缩与非负实现**。

接续：一般half仍需要真实比较行的**非负乘子锥**，本稿不把线性span、暴露极射线或有限秩核验当成其证明。若下一步只要求新的客户资料满足同一σ的SPE不等式，而不要求每行数值保持，本稿的精确资料障碍不适用；第6节给出明确成功折叠例。

最新接续：正矩局部族已经给出可核验的无限精确障碍，不再继续扩张类似局部族。应回到真实σ，寻找(覆盖坐标) `2e_R−e_O=G_σ^Tλ+a` 的共同构造，要求 `λ≥0`、`a∈K_m^*`；目前尚无此机制。PM-1仅提供全局非负余项候选，不替代λ。`independent_mechanism`已另从定义心算复核PM-2的全部公式并无异议，未另写独立审查文件；这与已有CR-2/3成文独审分开。
