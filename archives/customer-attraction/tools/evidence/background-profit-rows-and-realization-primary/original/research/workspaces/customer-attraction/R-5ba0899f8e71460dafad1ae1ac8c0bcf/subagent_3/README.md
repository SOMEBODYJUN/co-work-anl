# 六人：低阶背景利润行族的精确停界

2026-10-27。个人研究材料，**不是六人半覆盖证明，不是目标反例**。

本目录保存了一个有理可行的必要条件松弛点：即使同时使用全部位置的单题最坏负载安全行，以及末两人税和末三、四人合法背景利润定理，并允许这些后缀比较混入全部实际主题、不同或重复的最优查询索引，该指定行族仍容许 `O=1,W=28273/72900<1/2`。

将该点逐客户严格实现为一个 12 主题、2187000 单位客户的原模型目录后，规范全集逆推显示**每一份完整历史纯 SPE 都全覆盖**。因此低福利 profile 不可实现为 SPE；这一条精确反例仅针对下述行族的充分性。

正文与重放：

- `background_profit_relaxation_note.md`：全部行定义、系数压缩、九个有理支持点和局限。
- `background_profit_relaxation.py`：生成 439 行；`--audit` 独立从 Fraction 公式重新生成支持列的每个系数，核验全部行；`--solve` 实现真实目录并运行规范 ExactSPESolver。
- `background_profit_relaxation_exact_point.json`：有理点、439 个精确 slack，不主张浮点 LP 的最优值已被有理双证书认证。
- `background_profit_realized_instance.json`、`background_profit_realization_replay.json`：原模型目录和完整有理逆推范围。

根目录重放：

```sh
PYTHONPATH=. python research/workspaces/customer-attraction/R-5ba0899f8e71460dafad1ae1ac8c0bcf/subagent_3/background_profit_relaxation.py --audit --solve
```

探索中提出的聚合末位收益 cap `2W≥(m+1)u_m` 已由父方指出是仓库现有 FALSE 桥（三人收益 `(5,6,12)`），本目录没有采用或重新推广它。完整策略锥交替搜索与 research_4 已有实现重合，已停止重复实现。
