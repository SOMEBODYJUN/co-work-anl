# R-171 coupling-pair 三源比较记录

## 来源与重放

| 清洗 ID | 原始路径 | 大小 / SHA-256 | 处置 | 本轮重放 |
|---|---|---:|---|---|
| `af416d25b1181a69b019` | `R-171.../coupling/README.md` | 1621 B / `c30072054fd1b49b6030f6449953fb1e4e9dc1701a25be261bc9ad955e2674a9` | integrated | 逐字阅读；作为路线/量词入口，没有把未导出的正文摘要升级成定理 |
| `78ded6e12066708990fc` | `R-171.../coupling/audit_fixed_population_pair_error.py` | 3160 B / `027c0d1e7d1f7f891b77732fd0282d7c1f0cdced7143889172d07c9cfc9b0443` | integrated | 标准库 Fraction 直接执行，exit 0，输出与冻结 JSON 一致 |
| `c89b2700bb93eab9f0f6` | `R-171.../coupling/fixed_population_pair_error_audit.json` | 344 B / `889b2455633a473395573a7e080e0d136c97e052a9b5b340520f08ba431c3fef` | retained | 逐字段阅读；与脚本 replay stdout 字节一致 |

原始文件位于 `original/`，脚本重放位于 `replay/audit_fixed_population_pair_error.stdout.json`。

## 数学对象

审计脚本定义背景命中 `h`、二值会员 `(a,b)` 和固定人口 `r>s>=1` 的局部误差

\[
E=rs\frac a{h+ra+sb}+r(r-s)\frac b{h+sa+rb}-s^2\frac a{h+sa+rb}-(r-s)\frac b{h+1},
\]

以及宽二 ghost rent

\[
G=h\left(\frac1{h+1}-\frac1{h+1+a+b}\right).
\]

脚本用 Fraction 检查四种 `(a,b)` 的精确表、`0<=E<=(r-s)(r-1)G`，以及 `r=2,s=1` 时 `E=G`。随后在全部 (m\le11) 二值实际路径和两种 `s` 模式下，检查

\[
\sum_j\frac{E_j}{j(r_j-s_j)(r_j-1)}
\le \sum_j\frac{G_j}{j}
\le 1-\frac2{c+1}
\]

（空命中路径右端取 0）。输出计数为 `17280` 个局部会员配置和 `8188` 个固定路径配置，统一比较因子 `(r-s)*(r-1)`。

## 与既有 R-171 对象的去重和接续

- `R-171接续工作区主张边界与开放义务--审查` 已把 `B5-FIXED-POPULATION-PAIR-ERROR-v1` 定位为局部接口：短 pair 终局的收益值不自动等于任意真实续局的激励值。当前三源补充了该接口的独立 Fraction 逐定义重放，不产生新的 Q-CAG-HALF 结论。
- `R-171稀疏槽clock租金与skip-premium分解--引理` 证明 reset 费用 = clock + 非负 skip-premium。连续窗口可由共同拥塞支付，稀疏槽的 premium 仍需另付。pair 因子预算只能作为局部误差上界，不能删除 premium。
- `R-171完整SPE稀疏槽租金障碍--反例` 的两客户 (m=2q) 完整 SPE 族给出 `W=OPT=2` 而稀疏租金调和发散；它是否定“稀疏路径自动有根预算”的边界，当前 pair 审计不改变该状态。
- `R-171共同客户根路径支付与pair预算开放边界--审查` 从 README 保留连续窗口、pair-circuit、遗漏桥和早期激励四者的路线关系。当前 source README 提到的 `fixed_population_pair_error_budget.md` 和 `path_interval_rent_budget.md` 虽在 source inventory 中登记，但未随本批导出；因此本轮没有声称完整阅读未提供的正文。
- 动态信用/直接覆盖对象研究不同的真实路径和付款机制；这里没有把 pair 误差或 ghost rent 迁移成动态信用一步 gap，也没有迁移到 unrelated-machines。

## 结论边界

脚本和 JSON 支持的是定义级精确算术、有限二值路径预算和统一比较因子。它们没有：

1. 构造任意完整有序历史纯 SPE 的共同根支付；
2. 证明所有主题目录、所有客户重数或所有人数的 pair-circuit 运输；
3. 支付 skip-premium、早期中继激励或最优遗漏的选择性残差；
4. 反驳 `2W>=OPT`、给出一般算法/hardness，或产生 unrelated-machines 对象。

因此 README integrated、脚本 integrated、JSON retained；三源按各自数学/证据角色分开存档，没有把重复导航或冻结输出计作新定理。
