# MathLab ARCHITECTURE 实读比较记录

- Claim：`2cebad9493b8dd3a535f`
- 原路径：`research/weighted_congestion_frontier/upstream/mathlab/docs/ARCHITECTURE.md`
- 冻结 blob：`d94d2a6ad186b963f33af1d0fa912e6fc8bcbcf7`
- 源 SHA-256：`86caef32120dc9ec8a322f4f6fb917c6131122172d7659b8394f99e9b6906235`
- 大小：2078 B

## 已有相关资料

`archives/weighted-congestion/state/资料/接题来源映射与文献导入的版本边界--资料.md` 和 `archives/weighted-congestion/state/资料/冻结上游清单的五组选集与归档边界--资料.md` 已把 `adamisntdead/mathlab` 固定提交 `f2beac493aff1868b92b8233fd4427c467812ebe` 作为上游来源，并记录 `ARCHITECTURE.md`、`prompts.py`、MIT LICENSE 的选集边界。`archives/weighted-congestion/tools/evidence/restored-upstream-manifest/` 保留的是上游 manifest 元数据和缺失比较记录，不是 ARCHITECTURE 原文副本；因此本 claim 的实际完整阅读和原文 evidence 是新增事实，不把旧来源映射当成逐文件实读。

## 独有内容与当前流程比较

ARCHITECTURE 独有的是 MathLab 的研究软件架构：handoff→持久黑板→并行研究岛；Cartographer/Director/worker/Verifier/Seminar/RA 角色；SQLite 与项目文件的崩溃恢复；`.mathlab/extensions/manifest.json` 的热加载扩展协议；以及 `IDEA → CONJECTURED → COMPUTATIONALLY_VERIFIED → PROVISIONAL_PROOF → INDEPENDENTLY_VERIFIED → FORMALLY_VERIFIED` 状态阶梯和 `REFUTED`/`DISPUTED` 旁路。

当前 unrelated-machines 阶段二使用 `work.py` 的独立 clone、Git checkpoint、board 消息、clean claim/show/done 和逐源 receipt。两者都强调持久证据、独立复核和失败保留，但 MathLab 角色、SQLite 黑板、Verifier 自动管线和扩展 API 没有在本结果分支部署，也不替代本题的 Git/receipt 语义。MathLab 状态词不能直接映射成本题 `integrated/retained/duplicate/retired`，更不能把 `PROVISIONAL_PROOF` 作为数学证明。
