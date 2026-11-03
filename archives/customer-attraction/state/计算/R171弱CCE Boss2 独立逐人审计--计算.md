---
id: "customer-attraction/r171-weak-cce-boss2-independent-audit"
kind: "computation"
type_tag: "计算"
title: "R-171 弱 CCE Boss2 独立逐人审计"
status: "finite-exact-audit-passed"
truth_status: "finite-family-calibration; no minimum-CCE or general bridge claim"
review_level: "full-2760-byte-read-and-exit0-replay"
scope: "Boss2 weak-iid family; m=2..12,k=2..6 plus (53,53),(100,100); 57 Fraction cases"
source_refs:
  - "clean:6678221a19976d2929df:research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/continuation/independent/audit_weak_cce_boss2.py"
  - "local:archives/customer-attraction/state/审查/R171独立接续工作区与稀疏租金弱CCE边界--审查.md"
  - "local:archives/customer-attraction/state/计算/静态CCE福利分离的初次策略锥证据--计算.md"
  - "local:archives/customer-attraction/state/反例/三人顺序SPE低于全部静态CCE福利--反例.md"
source_identity:
  inventory_blob: "ca6adf873c2b8cf82625fdfce6784641a49253da"
  source_sha256: "b4ca4d0a38816d7a1eda83645aa85c6d91adc8125f910c5252711120b2ec41fe"
  source_size_bytes: 2760
evidence_paths:
  - "archives/customer-attraction/tools/evidence/R-171-independent-20261031/original/audit_weak_cce_boss2.py"
  - "archives/customer-attraction/tools/evidence/R-171-independent-20261031/replay/audit_weak_cce_boss2.stdout"
  - "archives/customer-attraction/tools/evidence/R-171-independent-20261031/replay/weak_cce_boss2_audit.json"
  - "archives/customer-attraction/tools/evidence/R-171-independent-20261031/comparisons/6678221a19976d2929df.md"

# R-171 弱 CCE Boss2 独立逐人审计

## 程序对象和复跑

完整实读 2760 字节 Python。程序用 `Fraction` 与 `Counter` 定义标签 `B=-1`、`C=0`、花瓣 `1,...,K` 的 Boss2 弱 iid 族；`utility` 直接根据终局负载重算每个玩家收益，`aggregate_slack` 对每个玩家逐一替换为固定查询，再把偏离收益相加。它不调用旧稿的 `b_m` 聚合捷径，也不把顺序 SPE 后继当作静态 CCE 偏离。

冻结源 SHA-256 为 `b4ca4d0a38816d7a1eda83645aa85c6d91adc8125f910c5252711120b2ec41fe`，blob 为 `ca6adf873c2b8cf82625fdfce6784641a49253da`。程序复制到 `tmp/r171/run/` 执行，exit 0，stdout 报告 `status=passed`、`cases=57`；README 虽列出 `weak_cce_boss2_audit.json`，但本次五源导出中没有该 JSON 原件；仅由隔离复跑生成的 JSON 与 stdout 保存在 evidence `replay/`，没有把复跑结果冒充冻结源文件。复跑未改动其余原件。

## 检查的两个族和量词

每个 `audit(m,k)` 先建立纯 Nash 配置 `[1]+[-1]*(m-1)`，直接核对福利 `2m+1`、所有玩家对所有固定查询的收益不增，以及
\[
  \frac{2m-1}{2m}(2m+1)<2m.
\]
对于 `m\ge3`，程序再构造三个状态：`[0]+[-1]^{m-1}`、`[0,0]+[-1]^{m-2}` 与均匀分配的花瓣状态；以 `p_0,p_1,p_2` 的 Fraction 权重核对总质量、期望福利 `2m+p_1`，并逐查询检查 aggregate slack 非负。除查询 `0` 外 slack 被精确核为零。

参数集是 `m=2..12,k=2..6` 的 55 组，加上 `(m,k)=(53,53),(100,100)` 两组，共 57 组；隔离复跑 JSON 保存每组的有理权重与 slack；README 所列冻结 JSON 未随本次导出。该数据支持“旧弱 CCE 桥在这一族上的校准”，也支持 Boss2 低福利 PNE 与三状态分布的有限构造，但不求所有静态 CCE 的最小福利、不证明 CCE 下界锐值，也不证明任意共同目录的弱 CCE 结果。

## 与既有 CCE 对象的关系

已归档的三人八客户/十三客户对象给出了不同实例中“完整顺序 SPE 福利低于全部静态 CCE 福利”的有理证书；初次策略锥页保存的是另一个 43,426 单位客户实例。R-171 Boss2 脚本没有复现那些对偶下界，也没有把弱 iid 族的 `2m+1` 当成全局最小 CCE。它只是独立逐人的 Fraction 审计，避免把聚合公式或旧摘要升级为新定理。本页与 R-171 稀疏租金和 signed-δ 审查并列，三者量词互不替换。

对象处置为 integrated 计算记录。有限 PASS 不迁移到 unrelated-machines，也不改变 Q-CAG-HALF 仍 OPEN 的状态。
