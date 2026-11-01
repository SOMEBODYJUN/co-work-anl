# R-275 credible search comparison notes

本批 20 源按四层处置：

1. `acyclic_review_stdout.txt`、`audit_stdout.txt`、`certificate_audit.json`：完整历史精确证书/独立回放，整合为 finite SPE witnesses；不升级为普遍 half。
2. `symmetric_dag.py` 及九个 symmetric JSON：浮点 MILP 候选、exact cone recovery、symmetric scaling 与 time-limit 边界；保留 exact candidate 的 canonical verification 和 `universal_claim_proved=false`。
3. `indexed_projection.py`、`indexed_projection_instance.json`、`indexed_projection_completion.json`：单一 actual-unit-customer projection；对照 R275 background-exchange 与 R216 forest/necessary projection，明确 target unreachable 和缺失相对依赖。
4. `submodular_path.py/json`、`submodular_joint.py/json`：broader common-submodular Shapley / moment relaxations；1470 coefficient rows、30 path cuts 和 exact values 只作外部压力测试，不回写客户吸引模型。

所有 20 个源都有正文或 evidence 去向。已有 9/5、33/20、52/47 等有限证书与旧页存在数值重叠，但本批独有的是同一 R275 credible_search 目录下的 symmetric orbit、indexed projection 和 submodular necessary cut 的并排量词比较；原始源仍完整保存。
