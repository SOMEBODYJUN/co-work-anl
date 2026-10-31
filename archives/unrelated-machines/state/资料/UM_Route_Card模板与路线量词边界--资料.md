---
id: "unrelated-machines/route-card-template-and-route-boundaries"
kind: resource
type_tag: 资料
title: "UM Route Card 模板与研究路线操作边界"
status: integrated-navigation-contract
truth_status: "source-read-operational-template; no-mathematical-claim"
review_level: "full-read-2518-byte-template-cross-archive-history-comparison"
scope: "research/unrelated_machines/ROUTE_CARD_TEMPLATE.md, P0-F/R0-R route contracts, blind-attack order, historical prompt compatibility and current CAG entry"
summary: "85dbb6… 是 unrelated-machines 研究存档的可选 Route Card 模板。它定义成熟候选进入 canonical/跨线合并前所需的身份、义务、攻击、oracle/位复杂度和状态字段，并固定 P0-F 与 R0-R 两条路线的成功/失败量词。本文保存其操作语义、稳定入口、历史去审批边界和缺口；该文件不是数学定理、不是默认任务、不是审批门槛。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/unrelated_machines/ROUTE_CARD_TEMPLATE.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/unrelated_machines/ROUTE_CARD_TEMPLATE.md"
related_objects:
  - "archives/unrelated-machines/README.md"
  - "archives/unrelated-machines/prompts/README.md"
  - "archives/weighted-congestion/tools/evidence/history-transition-prompts-20261031/TEAM.md"
  - "archives/weighted-congestion/state/资料/历史共同研究提示词TEAM兼容入口与量词边界--资料.md"
  - "archives/unrelated-machines/tools/evidence/history-transition-status-20261031/README.md"
  - "archives/unrelated-machines/tools/evidence/history-transition-status-20261031/RESEARCH_STATE.md"
evidence_paths:
  - "archives/unrelated-machines/tools/evidence/route-card-template-20261031/original/ROUTE_CARD_TEMPLATE.md"
source_sha256: "b73c97253bad6a559150fb9dfae158ff2e9a4401b45611084b8a28ef3e5ae893"
source_size: 2518
---

# 1. 来源身份与默认入口边界

本轮完整读取 85dbb6a62aace9a2c6ed 的 ROUTE_CARD_TEMPLATE.md，2518 字节，SHA-256 为 b73c97253bad6a559150fb9dfae158ff2e9a4401b45611084b8a28ef3e5ae893。原文开头明确：当前全仓主攻是 Q-CAG-HALF（customer-attraction），Route Card 只用于显式选择 unrelated-machines 旧题对话，不是新会话默认任务。

因此该文件不是用户指令、不是默认研究目标、不是 claim 注册或审批门槛。它是研究存档的可选整理模板：探索可以完全不填；只有候选已经比较成熟、准备进入 canonical、跨线合并或升级状态时，才用它整理身份、攻击范围和下步义务。

# 2. 必填字段和稳定 ID

模板要求成熟候选至少整理下列字段：

| 字段 | 作用 |
|---|---|
| ID/version | 稳定 claim/版本身份 |
| route | P0-F 或 R0-R |
| builder/owner | 构造/维护责任 |
| blind attacker | 必须不同于 builder，且先不读 proof |
| integrator | 负责合并状态与证据 |
| 唯一承重义务 O | 共同容量、全机整数输出、sound FAIL、统一余量、位复杂度等 |
| 候选 Claim/问题入口 | 精确对象入口 |
| 相比 LST/ST/configuration-LP 的新增信息 | 防止已知基线换名 |
| 首个可判别输入族 | 最小攻击/验证族 |
| 成功条件 | 量词和输出合同 |
| 失败条件与 kill line | 明确停止标准 |
| oracle/阈值搜索/位复杂度假设 | 输入、调用和时间边界 |
| 本轮交付物 | 正文、代码、证据、地图等 |
| 状态 | closes / partial / blocked / salvage / retire |
| 下一动作 | 后续研究或停止 |

这些字段是 provenance 与研究管理信息，不自动构成数学证明。Builder、blind attacker、integrator 角色也不是排他名额或审批流程；它们用于防止同一人把自己的证明读后冒充独立攻击。

# 3. P0-F：任意输入共同容量桥

P0-F 的固定合同是：对任意合法普通 UM 输入 P,T，从输入本身产生共同状态 S(P,T)。成功必须同时满足：

1. 若 OPT<=T，产生具体的全机整数分配，并满足固定统一余量；
2. 若 OPT>T，给出独立可验证的 FAIL 证书，且 FAIL=>OPT>T。

首轮攻击族固定包括两树配置 gap、{1/2,1} 唯一 tiny 选择障碍和 shared-sink/block escape。若 S 只是逐机 probe、H+small 精确 oracle、已知最优支撑或给定 home/sink 分组，则只属于局部接口，不算 P0-F 完成。

P0-F 的关键范围是共同状态和全机整数输出：不能把逐机 feasibility、给定配置点或小规模枚举替代全局共同合同；不能只证明一个资源/一条 row 的局部余量；不能将 unknown OPT、oracle 或隐式最优支撑当作输入免费提供。

# 4. R0-R：近二真实整数 gap 与 decoder

R0-R 的固定合同是：给一个严格小于 2 的目标比例，构造真实调度 YES/NO 族。要求同时满足：

- NO 侧压低所有中间 quota 层，不能只压最低层或最高层；
- YES 侧保留完整真实整数可行性；
- 任意低于目标比例的真实调度，都能在位多项式时间解码为源问题 YES；
- 解码使用实际原任务和端点，不把 relaxation、局部配置或平均支撑当成真实 output。

以下任一情况立即登记为障碍并停止扩大参数：

- 中间 quota 层出现逃逸；
- 复制使 NO 变成 YES；
- 低负载实际调度无法解码；
- 解码只适用于一个预先指定的 schedule/oracle；
- 位复杂度依赖参数数值而非输入编码长度。

R0-R 不是“发现一个坏实例”或“看到一个有限 ratio”；没有完整 YES/NO、真实 schedule 和 decoder，就不能登记 close。

# 5. 成熟候选的 Blind attack 顺序

在读取 Builder 的证明正文前，blind attacker 必须独立提交三项：

1. 最小边界与退化输入；
2. 量词、oracle、FAIL 语义和总位复杂度攻击；
3. 现有已知族是否已击穿候选。

随后才读取证明，标记 passes / fatal / unresolved。Integrator 只有在独立材料和证明材料都存在时才登记 canonical；否则候选留在个人工作区或 questions。

这个顺序是历史研究记录，不声称完全无背景：攻击者必须披露已知的旧对象、旧 prompt 和已读路径，不得把知情 read-after 改写成 blind。有限代码、样本和根 replay 可以作为证据，但不能替代量词证明。

# 6. 历史版本和后续关系

全仓历史 TEAM 兼容材料明确：Route Card、ACTIVE_ROUTES、BOSS_RESEARCH_BRIEF 等是导航和可选记录，不是名额、审批、排他认领或暂停条件。所有 boss 可以直接进行证明、构造、反例、文献核查和代码实验；成熟结果再做独立攻击和状态登记。路线可以临时改变，不能因没有 Route Card 就停止研究。

当前清洗中各 substantive 对象（private sink、shared sink、PDM、Min-Rep、normalized menu 等）均应以自己的 Exact/Proof/审查/证据为准。Route Card 不能替代它们的数学正文、receipt、source hash 或 checkpoint/done 状态；也不能把历史 ROUTE_CARD 的旧 P0-F/R0-R 目标写成当前用户的新任务。

# 7. 实际缺口与处置

该文件没有定义一个新的 UM theorem、算法、gap、hardness 或外部文献结论。其可用内容是：

- 给成熟候选分配稳定 ID、承重义务、攻击和停止字段；
- 将共同容量桥（P0-F）与真实整数 gap/decoder（R0-R）分开；
- 强制记录中间层逃逸、复制变 YES、decoder 失败和位复杂度问题；
- 规范 Builder→blind attacker→Proof→Integrator 的读序和证据角色；
- 保留当前主攻 Q-CAG-HALF 的默认入口边界。

处置为 integrated-navigation-contract：原文已复制到 evidence，正式资料正文保存实际操作语义、历史去审批边界、路线量词和稳定 ID 要求。它不创建数学对象，不改变 UM-TARGET-v1 状态，不替代任何现有候选的 proof、有限 audit 或外部新颖性审查。
