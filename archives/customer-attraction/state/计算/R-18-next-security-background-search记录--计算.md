---
id: "customer-attraction/R-18-next-security-background-search"
kind: computation
type_tag: 计算
title: "R-18 next-security background search 记录"
status: "finite-background-security-records"
truth_status: "finite-experimental-security-values; no-universal-CAG-result"
review_level: "full-823-848-byte-read"
summary: "两份 background search JSON 的 ratio 均为浮点 1，P/v 分别 171.25/57.0833 与 70/17.5；均为有限搜索端点，未构造 CAG SPE 或一般 security theorem。"
source_refs:
  - "clean:294d323a2f01440fe2bc:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/next_security/background_search_best6.json"
  - "clean:0f9f80cbc75446bd5b78:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/next_security/background_search_best6_r4.json"
  - "local:archives/customer-attraction/tools/evidence/R-18-next-security-20261031/comparisons/comparison-notes.md"
source_identity:
  note: "IDs/hashes/source blobs preserved in receipts."
evidence_paths:
  - "archives/customer-attraction/tools/evidence/R-18-next-security-20261031/original/background_search_best6.json"
  - "archives/customer-attraction/tools/evidence/R-18-next-security-20261031/original/background_search_best6_r4.json"
  - "archives/customer-attraction/tools/evidence/R-18-next-security-20261031/comparisons/comparison-notes.md"
---

两份 JSON 完整读取，raw 与 `original/` 副本逐字一致。`best6` 的 SHA-256 为 `b76c9232008d9739467ea5780de7fa80a70656817feaf554110ffd125e6feee8`，记录 ratio=`0.9999999999999999`、iteration=4163、topics=6、remaining=3、P=171.25、v=57.08333333333334、all_root_outcomes=2；`best6_r4` 的 SHA-256 为 `43592e90fd7e41b8db5cc1108118c544611ac541cacea886a5fb3e52d3c41128`，记录 ratio=`0.9999999999999998`、iteration=16126、remaining=4、P=70.0、v=17.500000000000004、all_root_outcomes=2。weights、background、outcome 和 security_p 都是有限实验字段，没有 CAG `Instance`、完整 strategy/certificate、客户级 W/OPT 字段。

令 `r=remaining`。脚本语义中 `P` 是有限递归保留根结果中的利润，`v` 是静态安全值 LP，故 `ratio=P/(r·v)`；浮点值贴近 1 只说明这两个有限参数实例未发现严格 `<1`。它们与既有 R-18 k=5,r=3 background search 记录属于同一探针的不同主题/剩余人数配置，与 R-18 高背景条件和根背景缺口相接；新增两个 k=6 记录没有给出根空背景的承重桥。

因此这些文件更接近静态背景安全值/潜在势的搜索输出，不是顺序 CAG 的完整 SPE、福利 W/OPT 记录。与既有 aggregate-security/LAST 对象比较时，只能保留为有限候选，不能把 ratio=1 当作一般安全值恒等式、`P≥r·v` 定理或 Q-CAG-HALF 证明。
