---
id: "unrelated-machines/route-card-template-and-route-boundaries"
kind: resource
type_tag: 资料
title: "UM Route Card 模板与研究路线操作边界"
status: integrated-navigation-contract
truth_status: "source-template; corrected-open-mathematical-contract"
review_level: "full-read-2518-byte-template-cross-archive-history-comparison"
scope: "research/unrelated_machines/ROUTE_CARD_TEMPLATE.md, P0-F/R0-R route contracts, blind-attack order, historical prompt compatibility and current CAG entry"
summary: "历史模板只保来源定位；可复用数学已落到统一整数输出与全调度解码问题，修正不必拒绝所有OPT>T阈值。"
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

# 共同输出与全调度解码的开放合同

原 `ROUTE_CARD_TEMPLATE.md` 为 2518 字节，SHA-256 `b73c97253bad6a559150fb9dfae158ff2e9a4401b45611084b8a28ef3e5ae893`，两个冻结提交同字节，原件保存在 `evidence_paths` 所列路径。其角色、盲审顺序、注册字段与历史默认题路由不作为数学前提。

正式合同见[不相关机的统一整数输出与全调度解码](../问题/不相关机的统一整数输出与全调度解码--问题.md)：P0-F 对任意合法 P,T 输出统一负载界下的完整调度，或 sound FAIL⇒OPT>T；OPT>T 时仍允许返回放宽调度。R0-R 对任意低于已知绝对阈值的完整原矩阵调度提供源解码，并须覆盖每个固定改善量。一般目标仍 OPEN。

该模板自身未给共同状态生成器、实际全机舍入算法、可靠失败证书或源归约。它列出的两树配置间隙、唯一 tiny 选择、shared-sink/block escape 是攻击族；中间 quota、复制使NO变YES、原任务身份丢失、只对指定调度解码或按参数数值循环，是具体接口的失败条件，均不构成一般困难性。给定 home/sink、最优支撑或好调度的局部接口仍须明列附加输入。

数学内容由上述正式问题及其精确模型承接；冻结模板仅提供来源定位，不再复制角色/流程字段。
