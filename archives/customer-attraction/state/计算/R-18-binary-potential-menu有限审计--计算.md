---
id: "customer-attraction/R-18-binary-potential-menu"
kind: computation
type_tag: 计算
title: "R-18 binary potential menu 有限审计"
status: "finite-policy-infeasibility-with-found-gap"
truth_status: "finite-anonymous-binary-game-experiment; not-CAG-theorem"
review_level: "full-2211-byte-read-and-n4-replay"
summary: "脚本枚举 n<=4 的全部 ordered binary policies，LP 搜索 signed potential；n=4,pA=.5 全 limit=32768 时在 code17427 找到 gap=.25，payoffs=[-1,1,0,1,1,1,0,-1]。这是匿名两动作抽象实验，不能迁移成 CAG 反例。"
source_refs:
  - "clean:deadef6bc35b00f54164:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/next_security/binary_potential_menu.py"
  - "clean:b5ac195f8c2ea25aa0af:research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/next_security/binary_potential_menu_n4.json"
  - "local:archives/customer-attraction/tools/evidence/R-18-next-security-20261031/original/binary_potential_menu.py"
  - "local:archives/customer-attraction/tools/evidence/R-18-next-security-20261031/original/binary_potential_menu_n4.json"
  - "local:archives/customer-attraction/tools/evidence/R-18-next-security-20261031/replay/binary_potential_menu_n4.stdout.txt"
  - "local:archives/customer-attraction/tools/evidence/R-18-next-security-20261031/replay/binary_potential_menu_n4.stderr.txt"
  - "local:archives/customer-attraction/tools/evidence/R-18-next-security-20261031/replay/binary_potential_menu_n4_replay.json"
  - "local:archives/customer-attraction/tools/evidence/R-18-next-security-20261031/comparisons/comparison-notes.md"
source_identity:
  note: "IDs/hashes/source blobs preserved in receipts."
evidence_paths:
  - "archives/customer-attraction/tools/evidence/R-18-next-security-20261031/original/binary_potential_menu.py"
  - "archives/customer-attraction/tools/evidence/R-18-next-security-20261031/replay/binary_potential_menu_n4.stdout.txt"
  - "archives/customer-attraction/tools/evidence/R-18-next-security-20261031/replay/binary_potential_menu_n4.stderr.txt"
  - "archives/customer-attraction/tools/evidence/R-18-next-security-20261031/replay/binary_potential_menu_n4_replay.json"
  - "archives/customer-attraction/tools/evidence/R-18-next-security-20261031/comparisons/comparison-notes.md"
---

脚本完整实读 2,211 B，SHA-256 为 `b11a4596339c80bd7c619a19bc0df7786d8730c995078483128a7838a153e78a`。它枚举二元匿名政策，payoff vector `((a_1,…,a_n,b_0,…,b_{n-1}))` 可正可负且不受 CAG 客户目录约束，构造完整有序历史的 deviation rows 和固定 pA 的 menu rows，再用 `[-1,1]` payoff box 下的 bounded LP 搜索 signed-potential gap。n=4,pA=.5 的策略域大小是 32,768；本次按代码顺序在首次 witness 处停止，实际测试 17,428 个，在 `code=17427` 找到 `gap=.25`、`path=[1,0,0,0]`、`menu_countsA=[0,2,3]`、`payoffs=[-1,1,0,1,1,1,0,-1]`。冻结 n4 JSON（388 B，SHA-256 `f96f7fefd9671fdd72a7f2b97282f11765931102d91397dafb3335caf283fd2b`）与本次 replay 的 `players,pA,full_policies,tested,found` 字段逐项相等；计时字段随运行环境变化。

这是匿名两动作抽象的有限障碍，缺少 CAG 的客户类型、共同主题、均分收益、完整 SPE/OPT/W 量词；不能把 LP gap 当 CAG 反例。与既有任意整数势菜单探针（m=3,p=3 有限抽样未找到 gap）和匿名计数势客户相容性障碍对照后，仍只能说明抽象势路线的参数化差异。处置为 integrated 有限实验；stdout/stderr 和 JSON 输出均已保留。
