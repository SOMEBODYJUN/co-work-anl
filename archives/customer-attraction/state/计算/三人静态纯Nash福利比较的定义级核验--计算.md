---
id: "customer-attraction/static-pne-welfare-definition-audit"
kind: "computation"
type_tag: "计算"
title: "三人静态纯Nash福利比较的定义级核验"
status: "complete"
truth_status: "finite-exact-replay-passed"
review_level: "full-source-and-output-comparison"
summary: "原字节Fraction审计展开16客户，检查84项有序SPE比较与20个静态计数全部偏离；重放与冻结全报告相同。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/customer_attraction_worst_pne_welfare.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:examples/customer_attraction/worst_pne_welfare_failure.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/2026-10-20/customer_attraction_worst_pne_welfare.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/customer_attraction/worst_pne_welfare.md"
---

# 三人静态纯Nash福利比较的定义级核验

数学结论、客户类型、完整策略和可手核的表格见[反例正文](../反例/三人顺序SPE低于全部静态纯Nash福利--反例.md)。本资源是有限证书重放，不是对一般half的算法证明。

原件放于[original目录](../../tools/evidence/worst-pne-welfare/original/)，[manifest](../../tools/evidence/worst-pne-welfare/manifest.json)列六个源ID、两个完整冻结commit、blob及SHA256；所有字节保持原样。审计只实际读取examples输入和evidence/certificates策略，未导入规范模型、求解器或其他验证器。它把兴趣类型重数展开为16份单位客户，直接按每个客户的覆盖者均分重算收益；收益缓存没有合并策略历史。

对0、1、2长度全部有序历史，程序核对策略定义域恰有21节点，沿同一策略分别完成四个候选行动，检查84项含自身比较。静态部分使用4主题3人全部20组非负计数，每一组每个位置每个候选主题均做盈利偏离检查。静态匿名收益允许只枚举排序终局；这是静态穷尽归约，不用于顺序策略。两个PNE计数是(0,1,1,1)、(0,1,0,2)，W=OPT=16；顺序路径(0,3,3)，收益(17/3,14/3,14/3)，W=15。

本轮实际复跑：

```sh
python3 archives/customer-attraction/tools/evidence/worst-pne-welfare/original/tests/audits/customer_attraction_worst_pne_welfare.py --output /tmp/worst-pne-new-report.json
```

`--output`拒绝覆盖既有文件，使用一个尚不存在的路径。[本轮完整输出](../../tools/evidence/worst-pne-welfare/replay.json)与[冻结完整结果](../../tools/evidence/worst-pne-welfare/original/evidence/runs/2026-10-20/customer_attraction_worst_pne_welfare.json)逐字段全等；84比较与20静态记录均包括在比较内，不只比较摘要的PASS。

原[内部审查](../../tools/evidence/worst-pne-welfare/original/research/reviews/customer_attraction/worst_pne_welfare.md)记录最初boss证书路径及首次独立定义级复核；部署后的审计默认读取规范examples/certificates，实际重放据代码而非历史相邻路径执行。审查的独立性是相对规范求解器/证书验证器未导入，不等于外部评审或另一数学模型。本批只确认这六份冻结来源的实际内容与有限结论，没有扫描或冒认所有同题研究工作室。
