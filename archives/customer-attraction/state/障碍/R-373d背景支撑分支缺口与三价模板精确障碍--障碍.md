# R-373d 背景支撑分支缺口与三价模板精确障碍

- **稳定 ID**：R-373d-background-20261031
- **类型**：障碍（精确代数边界、有限搜索、命名模板 Farkas 障碍）
- **来源**：八个冻结源，详见 `archives/customer-attraction/tools/evidence/R-373d-background-20261031/source-manifest.json`。

## 精确代数审计

`audit_max_theme_branch_capacity.py` 不调用均衡求解器，只用 Fraction 检查 `m=3..100`、`c=1..m` 的 5047 个恒等式。旧根系数与新根系数的差为
\[
\frac{m^2-3m+3}{m^2(2m-1)(m^2-m-1)}>0,
\]
因此在审计范围内新根系数严格高于旧系数。三玩家值为新 `11/75`、旧 `2/15`、差 `1/75`；对应整数缺口倍率 `30/11<3`。输出明确称为 author audit，不能把系数改善直接当成 SPE 或六人 half 结论。

## 有限 ExactSPE 缺口探针

`deficit_probe.py` 生成有限客户实例，调用 `ExactSPESolver` 枚举终局策略，检查
`gap = OPT - W - players * minimum_payoff`。固定 seed `343734` 的 1000 个四主题四玩家实例最大 gap 为 `-7`；5000 个五主题四玩家实例最大 gap 为 `-24`。两个 JSON 均由源与独立重放逐字段相同。结果只说明这两组有限随机探针未找到正 gap；没有把 no-hit 写成一般不等式。

## 三价模板的精确障碍

`three_price_template.py` 把三名剩余玩家的对称查询乘子模板写成 LP，`bgmax=30` 扫描显示 `n=1,2` 可行，而 `n=3,4,5,10,20,100` 的命名模板 infeasible。`three_price_template_obstruction.py` 对 `n=3,bg=0` 的 11 个乘子使用浮点 LP 找候选，再用 Fraction 恢复；输出给出 700 个整数类型的 multiplicity、逐行非负 slack，目标整数尺度 `-1399`。这证明的是该命名线性模板的 Farkas 障碍，脚本没有构造支付、客户分配或完整历史 SPE。

## 比较与接续

这八源的独有内容是把背景支撑分支的系数改善、有限 `OPT-W` 缺口探针与三价模板失败放在同一证据包中，同时保留它们的逻辑层级：精确代数恒等式、有限随机搜索、命名模板障碍。后续若要进入六人 CAG 主线，必须把系数关系重新嵌入六提供者完整有序历史与覆盖者均分价值，补足空主题、重复、零客户、离轨历史和任意平局的量词；当前对象不承担这些全称步骤。
