# 当前研究状态

更新：2026-10-14 UTC。

## 活跃目标与前沿

**WC-TARGET v1：OPEN；无限下界阶段突破已内部审查。** 模型与量词保持 MODEL.md。当前 E_d≤a_*(d)≤d，E_d=d/[(d+1)d^(1/(d+1))−d]∼d/ln d；每个 d≥2 均有有限正权游戏在 E_d 本身无 PNE。自足证明在 ../current/weighted_congestion_frontier.md。

本轮从 a3f0c7a 恢复 odd_cycle 冻结资产，完成两项独立重构，闭合 mixed group 全状态、finite R、floor、正系数及 degree 义务。新 corollary 给 E_d；新的必要充分 lemma 给失败 hub edge 的实际 PNE。source Eq(3)全域 O(√d) ceiling 给 d≥256 的明确严格分离。世界优先权与外审未认证。

主要 obligation 已移到普遍存在上界：能否对任意 MODEL 游戏给 O(d/ln d)-PNE，或证明更大的下界？现有 simultaneous light/hub certificate 有 (α−1)(α^(1/d)−1)<1 barrier，不能靠参数优化超过 d/ln d 的 leading order。无 light-forcing 的 topology 尚未判定；barrier 不是 topology 或全类上界。

## 当前协作方式

一个 Work 对话使用提示词指定的角色号统一发言与提交，子 agent 在内部按需要并行研究。`tools/work.py` 配合本会话的 txt 凭据，完成恢复、同步、公屏收发和 checkpoint；本地配置固定后直接复用。

`wcg/board` 是微信式异步公屏，只保留当前消息流。各对话分享具体发现，自主继续研究；同题独立工作、多路线与反例攻击可以同时推进。公屏消息在研究间隙读取，回复随实际发现发送。

论文者和提取者分别整理贡献表达、发掘独立数学工具，使用同一程序和角色号流程。相关完整入口见 prompts/，来源原文见 SOURCES.md。

## 下一项有信息价值的动作

从一手文献与公屏选择关键义务，先以精确计算或边界族区分竞争机制，再建立一般证明。每次真实增量写清 claim/version、已知、objection 和下一检验，完成相应核验后立即 checkpoint，并向公屏分享已推送文件的 descriptor。

本轮推进数学下界；协作程序入口保持。状态、依赖与证据同步至 CLAIMS、root current/review/assets/graph 和 README。实际 replay 结果保存在 assets/R1/odd_ring_audit/ 对应 JSON；checkpoint 后分享冻结 descriptor。
