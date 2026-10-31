# Multiple-facilities proof-review tracker

## 归属、来源与读取边界

本组是任意设施数共同目录模型 SC-K-2-E 的历史内部逐引理审查记录：带标签设施、正权原子客户、线性实际负载成本、精确客户均衡及存在型完整续局。它不属于顺序客户吸引 Q-CAG-HALF 的证明；该目标仍 OPEN。

本次仅归位并登记既有记录，未重新完成其中声称的两轮证明审查，未升级现有命题或外审状态。下表的 `closed: verified as written` 是原记录在其所述版本上的内部判断。原稿定位见 [main.tex](../../../manuscripts/multiple_facilities/main.tex)，原第二轮报告见 [REFEREE_REPORT_round2_proof.md](../../../manuscripts/multiple_facilities/REFEREE_REPORT_round2_proof.md)；行号属于原记录版本，不保证与后续排版行号相同。原记录提及的 `skills_sources/math-proof-review/scripts/lint-notes.py` 不在当前仓库，不能据此宣称本轮已重放该 linter。

| Target | Proof lines | Required chunks | Blueprint | Note file | Gate deps | Status |
| --- | --- | --- | --- | --- | --- | --- |
| `lem:onpath` | `research/manuscripts/multiple_facilities/main.tex:88-100` | `1` | `N` | [lem-onpath.md](lem-onpath.md) | `none` | `closed: verified as written` |
| `lem:transfer` | `research/manuscripts/multiple_facilities/main.tex:120-132` | `1` | `N` | [lem-transfer.md](lem-transfer.md) | `none` | `closed: verified as written` |
| `lem:packing` | `research/manuscripts/multiple_facilities/main.tex:142-149` | `1` | `N` | [lem-packing.md](lem-packing.md) | `none` | `closed: verified as written` |
| `lem:capped` | `research/manuscripts/multiple_facilities/main.tex:156-168` | `1` | `N` | [lem-capped.md](lem-capped.md) | `none` | `closed: verified as written` |
| `lem:deviation` | `research/manuscripts/multiple_facilities/main.tex:178-198` | `2` | `N` | [lem-deviation.md](lem-deviation.md) | `lem:transfer, lem:packing, lem:capped` | `closed: verified as written` |
| `thm:main` | `research/manuscripts/multiple_facilities/main.tex:206-208` | `1` | `N` | [thm-main.md](thm-main.md) | `lem:onpath, lem:deviation` | `closed: verified as written` |
| `prop:certificate` | `research/manuscripts/multiple_facilities/main.tex:217-221` | `1` | `N` | [prop-certificate.md](prop-certificate.md) | `thm:main, lem:packing, lem:capped` | `closed: verified as written` |

## 归位来源记录

下表记录归位前的仓库相对路径与原字节 SHA-256。八份 note 保持原字节；本 tracker 只更新导航并添加本节及上述范围说明。旧个人工作区日志中的路径是当时记录，未改写。

| 原路径 | 现文件 | 原字节 SHA-256 |
| --- | --- | --- |
| `docs/proof-review/appendix-notes/_external-lemmas.md` | [_external-lemmas.md](_external-lemmas.md) | `45e626ac8d556d0aa1dfa63f6a854ecf24fd324fa61b04864bc773eefae0fc39` |
| `docs/proof-review/appendix-notes/lem-capped.md` | [lem-capped.md](lem-capped.md) | `a1f0c44b5f6786b21c921912e46dc249d517b1adb54fe0a90af1eddc0a9d7ed5` |
| `docs/proof-review/appendix-notes/lem-deviation.md` | [lem-deviation.md](lem-deviation.md) | `bbb6f26af98d7e80b1bf1831cd5ef94cce3fa13da124ac05d24c83bdbd59dcfc` |
| `docs/proof-review/appendix-notes/lem-onpath.md` | [lem-onpath.md](lem-onpath.md) | `5b30f38bc13a0cb7211016bf700c1bb7dbf85d09f17f62aa95d1a65be5be1297` |
| `docs/proof-review/appendix-notes/lem-packing.md` | [lem-packing.md](lem-packing.md) | `a92f925152c3286dbb94172f89516134720f4a7325239ad95210f2bf3b609bde` |
| `docs/proof-review/appendix-notes/lem-transfer.md` | [lem-transfer.md](lem-transfer.md) | `641e8c6c320905bd7bac3b904ad3d1393198f5f4ba338db85eb46af1a226c641` |
| `docs/proof-review/appendix-notes/prop-certificate.md` | [prop-certificate.md](prop-certificate.md) | `57db9bb34a442996c7d8ea4131494121eb5cf012e7c9ac34905bf4689fefc7c8` |
| `docs/proof-review/appendix-notes/thm-main.md` | [thm-main.md](thm-main.md) | `cdbe6897e74514792bcd21a67906ffa5cc90f7a9ee2b46fd353fe82a1f753c03` |
| `docs/proof-review/appendix-review-tracker.md` | [appendix-review-tracker.md](appendix-review-tracker.md) | `2065b8a3afeb800638bc74c7c574991f12a93cf7823145f02ad2055c467bff18` |
