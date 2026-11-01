---
id: "customer-attraction/abstract-menu-lp-finite-candidate"
kind: "computation"
type_tag: "计算"
title: "抽象菜单 LP 有限候选"
status: "discovery-tool-read-and-short-replay"
truth_status: "broader anonymous-potential discovery only"
review_level: "full-4949-byte-read-and-20-sample-replay"
scope: "Anonymous symmetric potential game; fixed ordered histories; floating LP discovery"
source_refs:
  - "clean:27a5d7f2345a66599b11:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/next_global/abstract_menu_lp.py"
  - "clean:7602e2c5ca5f41dd5ca1:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/next_global/abstract_individual_counterexample.json"
  - "clean:942a8d255dd34753318b:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/next_global/abstract_menu_counterexample.json"
  - "local:archives/customer-attraction/state/审查/R18缺口锥LP与静态机制--审查.md"
source_identity:
  inventory_blob: "3c13ce0c39f98a0edba2b2116b1ba5b3d057adf9"
  source_sha256: "c28c051d95900b0fda9032e47df213557477d7001fcf7074c2ca5f46c3f41bbb"
  source_size_bytes: 4949
evidence_paths:
  - "archives/customer-attraction/tools/evidence/abstract-menu-next-boss-20261031/original/abstract_menu_lp.py"
  - "archives/customer-attraction/tools/evidence/abstract-menu-next-boss-20261031/replay/abstract_menu_lp.stdout"
  - "archives/customer-attraction/tools/evidence/abstract-menu-next-boss-20261031/replay/abstract_menu_lp_individual.stdout"
  - "archives/customer-attraction/tools/evidence/abstract-menu-next-boss-20261031/comparisons/27a5d7f2345a66599b11.md"

# 抽象菜单 LP 有限候选

完整读取 4,949 B 源。它明确把模型扩展到任意匿名 F/G 势表，保留全部有序历史；`solve` 用浮点 LP 检查固定策略、固定 query 和菜单 cap，并可选 `individual` 与 nonnegative 约束。目标 discovery-only，未生成精确对偶或 CAG 客户实例。

本次短 replay：`--players 3 --topics 3 --samples 20 --seed 317` 输出 `checked=20,best=-0.0`；加 `--individual` 输出 `checked=20,best=0.0`。原 JSON 中的正 `delta` 来自另一有限发现记录，不能由短 replay 重新认证。

该工具不编码 CAG 客户克隆关系；它只支持“更宽抽象势证明路线需要额外条件”的诊断。对象处置为 integrated 资源/有限搜索记录，不迁移到 unrelated-machines。
