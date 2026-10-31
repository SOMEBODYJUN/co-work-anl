# literature_review_protocol 实读比较记录

- Claim/source ID：`ad8ddf8cdd1a700ec049`
- 原路径：`research/weighted_congestion_frontier/upstream/polish_skill/problem-driven-literature-review/references/literature_review_protocol.md`
- inventory blob：`2972c5bd49e44fc37ae902b72975dce89968d2a7`
- SHA-256：`f3c66ab4d820c5598951d344e5729f22b042e784253c5049ff9564b7f969fb33`
- 大小：14,796 B

## 与 SKILL 的关系

`cleanup/workspaces/Boss3/root/literature_review_skill.md`（5,574 B，SHA `16d6b89118cc838a613e08ba0de56361e5a40276343857a0692c67028426d592`）已提供 scope、tool delegation、verification mode、S-R-L-H-G-M-C-V 核心、workflow、质量门和 output。协议源是 SKILL 指向的完整 reference，本轮首次在该 source ID 下逐字节读取并保存原文；它新增：

- Infer Before Asking 的 venue/paper type/contribution/audience/validation 变量；
- 完整 S-R-L-H-G-M-C-V worksheet；
- requirement→existing capability→hidden assumption→boundary→bridge 五步段落骨架；
- reference-role taxonomy：FND、SUR、REP、SOTA、COMP、BOUND、BENCH、THEO、APP、ADJ；
- seed/backward/forward/requirement 检索顺序；
- `check_references.py`、`--strict`、`--online --title-search` 和 protected-title-term 参数；
- direct-competitor、negative-claim、review-experiment、citation-integrity、reference-metadata 五类质量门；
- method/theory/benchmark/system/application 五种贡献类型示例和最终 checklist。

## 与相邻资料的关系

- 与 `论文论证重构与主张证据对齐`：protocol 只负责 related work/background 的文献路线、隐藏假设、引用角色和 gap；argument reconstruction 负责整篇稿件的故事线与 claim-to-evidence 结构。
- 与 `科研想法新颖性风险审计`：protocol 不执行四层 novelty threat、危险 baseline 或 reviewer attack；它假定每条文献事实先写成 claim，再以来源角色支撑。
- 与 `贡献地图`：protocol 把 L/H/G/M/C/V 接到 reference roles；contribution map 提供 primary/secondary/non-claims/risks/reviewer-objections 字段。
- 与 `反防御审计` 和 `genre_profiles`：protocol 约束综述句的证据和否定卫生；二者分别负责句子功能和文类依赖。
- 与 `TeX-safe polishing`：protocol 不改 TeX 或数字；最终 reference metadata 和句子需另过 TeX/preservation workflow。
- 与 `BibTeX引用元数据检查器解析、规则与Crossref边界`：checker 只做静态/可选在线元数据卫生，不做 citation support、direct-competitor coverage 或 S-R-L-H-G-M-C-V 语义判断。

## 当前 UM 边界

协议可以帮助把 UM 的真实输入、近似/整数输出、sound FAIL、decoder、位复杂度、LST/ST/configuration LP/support 等写成 S/R/L/H/G/M/C/V，但它不证明这些对象，更不把“未搜索到”升级为“无人做过”。本轮没有执行 `check_references.py`、Crossref、DOI 或文献覆盖搜索；没有取得外部论文，所有新颖性和优先权仍需 source-bound 或明确 needs-source。
