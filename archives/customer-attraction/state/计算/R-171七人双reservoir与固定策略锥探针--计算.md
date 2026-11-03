---
id: "customer-attraction/r171-seven-player-reservoir-and-fixed-cone-probe"
kind: "calculation"
type_tag: "计算"
title: "R-171 七人双 reservoir 与固定策略锥探针"
status: "finite-exact-reservoir-and-floating-fixed-cone-diagnostic"
truth_status: "finite-observation-only; no-half-theorem-or-counterexample"
review_level: "full-source-read-and-source-output-cross-comparison"
scope: "m=7 reservoir family output plus a separate m=13 fixed packet FTA probe"
summary: "三份冻结源分别给出七人九主题 reservoir 有限精确探针、其源码和十三人固定自动机的浮点策略锥探针源码。最高观测 OPT/W=7/4；packet 浮点 gap 为负。二者模型、输入和量词均独立，不能外推为六人 half 结论。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/credible/reservoir_m7.json#source"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/credible/reservoir_search.py#source"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/parent/full_terminal_packet_probe.py#source"
evidence_paths:
  - "archives/customer-attraction/tools/evidence/R-171-reservoir-20261031/original/reservoir_m7.json"
  - "archives/customer-attraction/tools/evidence/R-171-reservoir-20261031/original/reservoir_search.py"
  - "archives/customer-attraction/tools/evidence/R-171-reservoir-20261031/original/full_terminal_packet_probe.py"
  - "archives/customer-attraction/tools/evidence/full-terminal-packet-probe-20261031/original/full_terminal_packet_probe.json"
related_objects:
  - "archives/customer-attraction/state/算法/完整历史纯SPE终局全集--算法.md"
  - "archives/customer-attraction/state/审查/R-171可信低根接续与有限候选边界--审查.md"
  - "archives/customer-attraction/state/引理/R-171池化响应负载Jensen信用与条件接口--引理.md"
---

# 1. 七人九主题 reservoir 源

冻结报告 `e1f1b683928e2e2cae42` 是 8,889 字节、SHA-256 `40007056b608343a591c3c36b466626c6d0c4c48ff948496dabb2a2f40da3d38` 的 `reservoir_m7.json`；源码 `ad0cf87b18bf7f1afd33` 是 1,933 字节、SHA-256 `8dcab36e0fb94bdb4f24892b38fdc05920153656571177bceabd51d7be9b8625`。源码的 `make(m,a,b,x)` 固定 `b=1`，本批 `m=7`、`k=m-1=6`，主题为六个私有 `P_j` 加 `R,B,C`，客户为 `{R,B}`、`{R,C}` 与每个 `{P_j}`、`{P_j,B,C}` 类型。对 `a,x` 的 45 个有限配置，报告保留 `W`、`OPT`、SPE 终局计数数目和一个最坏计数向量。

选择六个私有主题与 `R` 可覆盖全部客户，因此每行的 `OPT=6a+6+2x`；程序仍以 exact SPE solver 逐实例计算。`ratio=OPT/W` 的最大观测值为 `7/4`，出现在 `a=2,x=5` 与 `a=4,x=13`；这只是 45 个配置中的有限观测，未枚举所有完整策略，`one_worst` 也不是完整历史证书。报告没有 `ratio>=2`，但该阴性不证明该族全参数或六人模型满足 half。

Exact solver 的终局集合允许重复主题和历史依赖平局；`SPE_outcomes` 是终局计数向量集合，不是完整策略集合。该对象保持共同目录、单位客户、均分收益和所有有序历史的量词，不迁移到异构设施、弱 CCE 或混合 SPE。

# 2. 十三人固定 packet 的 FTA 浮点探针

冻结源码 `3258071a267ea42b55b3` 大小 4,918 字节、SHA-256 `088ee78780ce8399b6d2ac778dda64c4fef51ee5aa4431c05c3693ed48d8efa8`。它读取已有 13 人、6 主题、27,243 节点的完整 packet，逆计数序重建每个节点真实子终局，保留有序历史的 Gamma 行，再沿根在轨路径用 `linprog` 选固定策略 IC 锥内的客户权重，用 SLSQP 更新两个查询分布 `p`。它是固定策略锥（FTA）的浮点诊断，不搜索全部 SPE。

已有 packet 输出 `full_terminal_packet_probe.json` 的状态为 `finite floating discovery only`，`gamma_rows=31454`，归一化 `gap=-0.07142857142787729`（约 `-1/14`），权重只在六主题全兴趣 mask=63 上非零。负 gap 只表示这次局部交替优化没有找到正 pooled-query 分离；它不是精确有理下界，更不能推出一般 POOL 或 half 结论。该 packet 与七人 reservoir 的客户、人数和策略身份不同，不能把 `W=1` 归一化值或 Gamma 行数合并解释。

# 3. 处置与接续

三源均集成为本计算对象和 `R-171-reservoir-20261031` 原始证据目录。其独有内容是七人双 reservoir 的 exact 有限输出、源码定义域和十三人固定策略锥的浮点接口；不新建定理或反例对象。若要继续攻击 Q-CAG-HALF，应直接覆盖 `m=6` 的参数并为每个高比率实例保存完整策略、所有偏离比较、真实 OPT 和独立有理重放；若要继续攻击 packet，应固定数值环境并有理化所有 Gamma 行与 LP/SLSQP 结果。当前六人 half、一般 POOL、真实 SPE 福利桥和全局安全支付仍开放。
