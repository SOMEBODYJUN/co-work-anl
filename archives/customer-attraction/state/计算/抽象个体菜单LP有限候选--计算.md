---
id: "customer-attraction/abstract-individual-menu-lp-finite-candidate"
kind: "computation"
type_tag: "计算"
title: "抽象个体菜单 LP 有限候选"
status: "finite-floating-candidate-read"
truth_status: "broader anonymous-potential candidate; not CAG"
review_level: "full-1980-byte-read-and-abstract-model-comparison"
scope: "3-player, 3-topic abstract policy/query candidate"
source_refs:
  - "clean:7602e2c5ca5f41dd5ca1:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/next_global/abstract_individual_counterexample.json"
  - "clean:27a5d7f2345a66599b11:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/next_global/abstract_menu_lp.py"
  - "clean:d383c884dbeeca1cc424:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/next_global/audit_abstract_menu.py"
source_identity:
  inventory_blob: "e620174cc7abdc304e2351df3e3cb099460ba134"
  source_sha256: "59f0ae8525cd426e6d3ac375ef5249a6ab7e229e95d01ebf167ae62c712199e9"
  source_size_bytes: 1980
evidence_paths:
  - "archives/customer-attraction/tools/evidence/abstract-menu-next-boss-20261031/original/abstract_individual_counterexample.json"
  - "archives/customer-attraction/tools/evidence/abstract-menu-next-boss-20261031/comparisons/7602e2c5ca5f41dd5ca1.md"

# 抽象个体菜单 LP 有限候选

JSON 完整读取 1,980 B。它保存三人三主题策略、每个玩家的 query 分布、匿名 F/G 表、`status=0/Optimal`、`delta=0.1167840674842906`、actual `(0,2,2)` 和四个 menus。该文件是 `abstract_menu_lp.py` 的数值发现记录，不是有理证书，也没有把自身对象声明为 CAG。

关联 LP 源的模型是更宽的匿名势游戏：`u(a,B)=F(B+a)-G(B)`，F/G 是任意匿名表；这与 CAG 客户分母收益没有同构映射。因而 `delta>0` 只能作为抽象固定策略菜单候选，不能解释为 customer-attraction 的 `OPT/W`、SPE bridge 或 half 反例。

本批 Fraction auditor `audit_abstract_menu.py` 是另一份硬编码有理 exact-potential witness（实际 `(B,C,C)`、W=2、menu cap=3/4），没有读取本 JSON 的浮点 F/G；二者保留独立身份。对象处置为 integrated 有限候选记录，不迁移到 unrelated-machines。
