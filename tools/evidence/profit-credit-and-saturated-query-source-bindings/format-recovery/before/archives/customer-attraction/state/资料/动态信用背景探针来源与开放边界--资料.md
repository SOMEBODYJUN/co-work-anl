---
id: "customer-attraction/dynamic-credit-background-probe"
kind: "resource"
type_tag: "资料"
title: "动态信用背景探针：末位余项来源与开放边界"
status: "integrated-source-map; q-cag-half-open"
truth_status: "source-read-route-record; no-general-half-result"
review_level: "full-read-three-source-cross-comparison"
scope: "customer-attraction dynamic_credit/background_probe README, terminal remainder note and exact JSON output"
summary: "完整读取 2026-10-23 个人探索 README：固定非负整数背景的末位利润精确余项扩展 two_remaining_tax §6；候选的 r·min_i u_i 与 (r−1)·min_i u_i 版本仍未证；已证的是以真实末位收益 v 为基准的版本及恰两人推论。README 明确 Q-CAG-HALF 仍 OPEN，终端证书不能替代早期真实离轨菜单的信用支付。"
source_refs:
  - "clean:6bacca03ff57d72f3a8d:dynamic_credit_background_readme.md"
  - "clean:a329e42732730bc0f9d6:terminal_profit_remainder.md"
  - "clean:af18a968e70a74bbba3c:terminal_profit_remainder_exact.json"
evidence_paths:
  - "archives/customer-attraction/tools/evidence/dynamic-credit-background-probe-20261031/original/README.md"
  - "archives/customer-attraction/tools/evidence/dynamic-credit-background-probe-20261031/original/terminal_profit_remainder.md"
  - "archives/customer-attraction/tools/evidence/dynamic-credit-background-probe-20261031/original/terminal_profit_remainder_exact.json"
  - "archives/customer-attraction/tools/evidence/dynamic-credit-background-probe-20261031/comparisons/comparison-notes.md"
related_objects:
  - "archives/customer-attraction/state/引理/末位收益税诊断--引理.md"
  - "archives/customer-attraction/state/引理/固定背景两人税界--引理.md"
  - "archives/customer-attraction/state/资料/动态信用背景探针来源与开放边界--资料.md"
  - "archives/customer-attraction/state/引理/任意背景的末位利润精确余项分解--引理.md"
  - "archives/customer-attraction/state/计算/任意背景末位利润余项精确审计--计算.md"
  - "archives/customer-attraction/tools/evidence/dynamic-query-credit-primary/README.md"
  - "archives/customer-attraction/tools/evidence/customer-attraction-direct-cover-readme-20261031/original/README.md"
---

# 来源身份和核心处置

本页对应 dynamic_credit/background_probe 的三份来源：README（1,250 B）、末位利润余项正文（6,149 B）和 exact JSON（639 B）。三份原字节均完整复制到同一 evidence 目录，逐源 SHA 与读取范围保存在各自 receipt；跨源比较记录在 `comparisons/comparison-notes.md`。

README 把本批定位为 2026-10-23 个人探索资产，并明确一般 Q-CAG-HALF 仍为 `OPEN`。它将 `terminal_profit_remainder.md` 描述为任意固定非负整数背景、任意实际终局、只用末位最佳回应的精确非负余项分解；将 `audit_terminal_profit_remainder.py` 和 exact JSON 定位为独立 Fraction 核验及输出。脚本源码不在本批三个来源中，不能把 README 的指向当作本轮已读取或重新运行脚本。

本资料处置为 `integrated` 来源地图。其独有价值是把末位余项正文、有限 JSON 和未完成信用义务放在同一身份下；它不构成定理本身，也不改变任何 Q-CAG-HALF、direct-cover 或 dynamic-query-credit 对象的状态。

# 已证、候选与停止边界

README 明确区分四种内容：

* 已证：以实际末位收益 (v) 为基准的背景余项版本；
* 已有特例：恰两人时，由现行两人税定理推出 (F_2(b)-Plemin(u_1,u_2))；
* 未证候选：(F_r(b)-Ple rmin_i u_i) 及更强的 ((r-1)min_i u_i)；
* 未完成义务：末位收益过高时，要从早期真实离轨菜单支付余项，不能只靠末位证书。

因此不能把“真实最小收益在末位时强版本成立”扩展成完整 SPE 中末位总是最小，也不能把一个 69 客户样例的余量写成任意人数的半覆盖结果。README 还要求继续使用早期真实离轨菜单和一个已知非 SPE 模板的缺口，说明终端余项只是后续路线的入口。

# 与现有对象的关系

现有[末位收益与前缀税的根诊断](../引理/末位收益税诊断--引理.md)给出空背景下只用末位 BR 的 (operatorname{OPT}_mle m v+	au)，并强调末位高于平均只是根税反例的必要过滤，不是充分反例。本批把这一末位证书推广到任意固定非负背景，但保留相同的“不能替代早期激励”边界。

现有[固定背景下恰两名剩余玩家的税界](../引理/固定背景两人税界--引理.md)使用同一完整策略的真实末位回复和三个 SPE 比较，得到任意背景两人更强税界；本批 README 明确 (r=2) 只作为该结果的推论，不把它扩为一般 (r) 的归纳。

现有 `dynamic-query-credit-primary` 把每个实际节点的静态信用 (L_i) 和自适应罚项 (Q_i) 分开，且 HALF?/SHARP? 仍未证；direct-cover README 则把弱匹配、弱平均和旧强平均分成不同支付接口。本批只处理固定背景的终端 (L+K+J) 余项，不计算跨节点 (Q_i)，不把互斥真实分支合成一个共同钱包。

# 当前接续

下一步必须从完整策略的早期真实偏离菜单构造非循环支付，或更换信用目标；单纯把终端 `v` 替换为 (min_i u_i)、重复静态 LP 或增加随机样本都不能闭合一般 Q-CAG-HALF。三源不迁移到 unrelated-machines，也不产生外部新颖性、完整 SPE、一般福利上界或六人结论。
