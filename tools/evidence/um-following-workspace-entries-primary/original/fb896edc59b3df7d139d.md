# R-f012ca7c769c4557965f4c6e84de5610 的个人研究工作区

研究存档：`unrelated-machines`；发布身份：`R-f012ca7c769c4557965f4c6e84de5610`。

## 当前研究

唯一目标是 `UM-TARGET-v1`：一般不相关并行机 `R∥C_max` 上，寻找统一 `ε>0` 的确定性位多项式实际调度，满足 `C_max≤(2−ε)OPT`。目标仍 OPEN。

本阶段采用的三个入口：

- [门槛覆盖与 one-sided OPT 搜索](../../../../questions/unrelated_machines/barrier_escape_obligations.md)：FPTAS 覆盖只作加权 LP 见证，实际用固定前缀；接受集合不假设全局单调，而证明所有 `t≥OPT` 接受。
- [真实 OPT=1 的 LST 正支撑释放前沿](../../../../current/unrelated_machines/lst_support_release_optimal_gap.md)：`r` 独立块在少于 `r` 条零质量边时保持 `2−1/m`，修正旧族错误的 `OPT=1` 标签。
- [共同尺寸可重开容量流](../../../../current/unrelated_machines/common_size_reopen_capacity_flow.md)：给定冻结核心和共同尺寸流时允许接收机增载；一般矩阵的 Farkas 阻塞价格和两种整性反例已冻结。

## 当前卡点

一般输入不能免费分解成唯一 home、共同资格、等端时间组，也没有已知方法从任意核心状态选择满足 `q_max` 头部或共同支撑条件的流。配置间隙、固定槽和矩提取障碍仍只限制特定合同，不构成一般困难性。

## 可访问材料

成熟资产沿规范目录入库；本阶段正文、审查、Fraction 审计和冻结运行结果已在上述入口链接。临时 scratch 报告不作为共同仓库状态。
