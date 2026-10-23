# 可信编译、真正 half 成本及锐停界

2026-10-23。Q-CAG-HALF 仍 OPEN。此目录均为本组个人资产，尚待独立攻击，未改共享
结论或进行 Git 操作。解析证明承重全称，有限 Fraction 审计只审计所列范围。

## 优先读取

1. `padded_insurer_statement.md`：仅精确陈述，可给未看证明者独立重构。
2. `padded_insurer_repair.md`：任意 m>=2、任意 root-only 缺陷 Delta 的完整可信修复。
   在旧二主题保险旁加 m-2 个大小 Delta 的未覆盖叶，实际保险 W=(m+1)Delta，
   OPT=(2m-1)Delta，真正 half 稀释量从 (m+1)Delta 降到 **3Delta**。
   旧计划若 `OPT_old-2W_old>3Delta` 即会生成原目标反例；未找到这种旧计划。
3. `disjoint_insurer_three_sharp.md`：不交极大花瓣、内部任意子主题的同根保险，
   designated 高首人收益分支满足 `2W-OPT_m>=3×收益跨度`，且常数3对每个m锐。
   任意多个此类独立坐标也不能降3；根后跨坐标耦合不在停界范围。
4. `disjoint_insurer_spread.md`：总客户成本的另一精确对象。任意多不交极大花瓣、
   任意内部子主题的同根 suffix-SPE 首人跨度至多 C/(m+1)，因而总客户成本不能
   低于(m+1)Delta；这不阻止第2项对 half 稀释量的改进。
5. `effective_margin_frontier.md`：任意交叠保险的真正幅度为h−M，M是所有全深度SPE
   的最低首人收益。此次接续没有闭合新的overlap构造；已排范围、需要的跨分支
   双负载机制及明确停止点均记录于此，未继续旧cone扩样。

## 精确核验

- `audit_padded_insurer.py`、`padded_insurer_audit.json`：独立显式单位客户、m2..5、
  全部 11744 个有序决策历史及 116068 项合法联合动作比较通过，最小slack0。
  旧seed有真正Delta1，非零修复；程序不导入仓库模型/求解器/验证器。
- `padded_insurer_m{2,3,4,5}_certificate.json`：每个有序历史动作及显式单位客户。
- `audit_disjoint_insurer.py`、`disjoint_insurer_audit.json`：340个有内部子主题的结构
  案例，1499个固定root、323对正跨度、51403个计数状态；集合值BI、全部suffix
  PNE偏离、总客户range和3稀释界均用Fraction通过。
- `three_theme_insurer.py/json`：m3p3所有81张完整suffix策略、6561对同根锥；每个LP
  精确原始/对偶检查通过，最大range恰C/4。只处理这个有限m,p，不作一般外推。
- `three_theme_dilution.py/json`：同一有限m3p3全锥上改攻真正half成本，精确最大
  `3spread-2W_H+OPT_3`为0（此处OPT_3=C）。一般三主题交叠没有在此有限范围突破3；
  不推出一般交叠保险停界，不构成继续扩样的理由。
- `old_two_theme_certificate_replay.json`：实际重跑旧源的独立逐客户回放，四份完整
  旧证书1808项比较通过。传闻“+2总主题”未在源中恢复；真实旧编译是2p主题。

## 下一步

现在应攻击旧 root-only 计划是否存在 `OPT-2W>3Delta`，或真正利用重叠保险/根后
耦合突破3。反复调不交保险大小或增加独立坐标已有一般停界，不值得再扫描。
第一个义务与每个固定m原half精确等价，见修复正文第6节；这不是无条件简化成
更容易的问题，但提供了可直接编译的另一反例接口。
