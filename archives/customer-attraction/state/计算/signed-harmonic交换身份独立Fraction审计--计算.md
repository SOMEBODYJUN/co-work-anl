---
id: customer-attraction/signed-harmonic-identity-audit
kind: computation
type_tag: 计算
status: finite-exact-audit-passed
truth_status: identities-only; signed-budgets-open
source_refs:
  - clean:2017fbdf608d0350d73d:research/workspaces/customer-attraction/R-12bf6a96d24c48eca828620d6642e203/signed_harmonic/audit_identities.py
---

# signed-harmonic 交换身份独立 Fraction 审计

完整实读 1300 B script（SHA `4108b53ec5b907f688aa042dc232cd1d828e51ce7c028af590fc36eda0dcab5f`）。程序核验 2869 arithmetic cases 与 92256 exchange cases，实际 exit0 PASS。它检查支持交换差、ghost 删除、末位系数和集合恒等式，仅属 exact identities；signed budgets remain open。
