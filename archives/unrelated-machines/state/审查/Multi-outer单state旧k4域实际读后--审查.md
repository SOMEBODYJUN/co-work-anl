---
id: "unrelated-machines/multi-outer-single-state-k4-tiny-home-review"
kind: "review"
type_tag: "审查"
title: "Multi-outer 单 state 旧 k⁴ 域实际读后"
status: "legacy-typed-domain-read-separated-from-v4-v5"
summary: "实读 v1 review 确认 multi-outer single-state tiny-home 的 k⁴ typed contract：互异 positive homes、own-unit helper、共享 normalized B fallback、wmax≤1/(4096k⁴)，以共同 point/平方势/conditional-expectation 输出 19/10 actual assignment。其有限软件仅后端校准；v4/v5 k²/O(1/k) 是独立版本，一般 UM 仍 OPEN。"
source_refs:
  - "clean:0980342ad6b3fa9485bc"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/multi_outer_single_state_tiny_home_rounding_review.md"
---

# 版本与读域

`0980342ad6b3fa9485bc`（SHA `580fd70104dedde68e46db672361c1c230d3d72223409df52fecde811cf92366`）是 v1 旧 k⁴ 域的完整 review。它绑定最终 175 行正文 SHA `84d603…`，只覆盖原 `UM-MULTI-OUTER-SINGLE-STATE-TINY-HOME-19-10-APPROX-v1`；后续 v4 k²/shared-UD 与 v5 O(1/k) 另有版本，不可由同页链接扩域。原件/manifest 在 `archives/unrelated-machines/tools/evidence/multi-outer-shared-ud-20261031/`，receipt 草稿在 `cleanup/workspaces/Boss2/multi-outer-shared-ud-receipts-20261031.json`。

# 1. v1 typed contract 与双向桥

输入有 k 个 single-state outer，positive homes 全局互异，每 home 有 own-unit helper；B 上 arbitrary normalized fallback；tiny 条件 `wmax≤1/(4096k⁴)`；输入仅显式 Q，不给 LP/OPT/actual allocation oracle，保留全部 indexed states、selectors、incidence、zero/inactive jobs，输出全部原 jobs。定义共享叶 matching 值 V，证明 `OPT=2−V`；全叶 matching 不存在时 `V<15/16`，ordinary baseline 全 jobs C=2 给 ratio≤32/17<1.9。

own singleton 的整化只需同一 SA1 二阶点，得到全部 helpers 的共享 packing cap1 与各 outer ε benchmark；不能把每个 outer 复制 B 容量。每轮使用固定公共分母和有理 MW/CE，次数和分母位长按输入多项式；selector/incidence 请求必须与实际 winner 一起回填，不能在 CE 后重新加入未请求 clause。

# 2. 两类算法身份与证明范围

独立 Exact-first 路线是 floored-simplex 强凸势、可计算投影 subgradient、fixed-states allocation LP 删除少量 split items；作者路线是 MW+平方势、全 k 求和 Efron–Stein variance 和 conditional expectation。review 明确分别审查，不能用独立算法代签作者方案。共同数学结论是：在 k⁴ tiny、single-state、互异 home、shared normalized B 域内，确定性总位多项式可构造每 outer 均值/实际 winner，实际峰≤1.9。

有限软件只实现后端 winner/moment 枚举：两个固定小例，约 2048/2916 outcomes，核对单/双 resource moments 与 CE 势；没有实现 Rε、MW、tiny 输入、全原 jobs 或端到端算法。因此软件 JSON 是后端校准，不是 v1 全称算法认证；数学正确性来自证明和独立 read-after。

# 3. 边界、P≠NP 与后续版本

来源中的 typed-domain source 只排“全部输出此域、YES actualOPT≤1/NO≥2−γ、固定 γ<.1”的 NP 归约；不排一般 normalized menu、一般 UM 或主目标。多-state outer、重 home、任意 non-UD leaves、跨域 shared resource decoder 都未覆盖。

v4 的 k² shared-UD 与 v5 的 O(1/k) relative-curvature 实际 allocation 是独立版本：它们修改 tiny/vacancy 常数、算法 backend 与读序，不能把 v1 的 `wmax≤1/(4096k⁴)` 或旧软件事实静默升级到新合同。反过来也不能用 v4/v5 的证明覆盖本 v1 未读正文。仓库本轮已有 v4/v5 review 与 Exact/Proof 来源，此页只保存 v1 source-ID 的实际读后和版本边界。

# 4. 处置与未决义务

本源处置为 `legacy-typed-domain-read-separated-from-v4-v5`：保留 v1 k⁴ typed algorithm 与 finite backend 范围，明确与后续 k²/O(1/k) 版本分离，不外推一般 UM 近二算法、通用 source reduction、外审或新颖性。后续引用须注明 v1 175 行、single-state、互异 home、tiny k⁴、shared normalized fallback 和 software backend-only 校准。
