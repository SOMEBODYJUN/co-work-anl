---
id: customer-attraction/parent-actual-incumbent-independent-audit
kind: computation
type_tag: 计算
status: source-read-frozen-audit; rerun-blocked-by-missing-input-paths
truth_status: independent-audit-source; frozen-report-separate
review_level: full-2649-byte-read
source_refs:
  - clean:5a6dbc90d1b5d8e04c50:research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/parent/audit_actual_incumbent_independent.py
  - local:archives/customer-attraction/state/反例/父方实际incumbent独立全历史审计报告--反例.md
---

# 父方实际 incumbent 完整历史独立审计

脚本完整实读 2649 B（SHA `0183840fe184afe470ef495cd5d274443ba63220d442d5e0b491839a1cf4ccad`）。它不导入 CAG solver：直接读取 frozen actual-root certificate 和 instance，重建全历史终局、Fraction 收益、所有末位 BR，并检查 259 histories、1295 non-self deviations、实际路径 `(1,0,0,5)`、root minimum 9、BA child minimum 13 及 3/4 bridge gap。

本清洗 checkout 没有脚本引用的原始 certificate/instance 路径，因此本批不冒称重新执行。冻结 PASS report 单独保存并与已有四人实际前缀反例对象对照；源程序是独立审计入口，不能把缺少依赖的静态读取升级为本批 fresh replay。
