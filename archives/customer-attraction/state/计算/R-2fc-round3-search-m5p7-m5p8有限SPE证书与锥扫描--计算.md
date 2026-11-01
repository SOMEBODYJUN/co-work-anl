# R-2fc round3 search：m5p7/m5p8 有限纯 SPE 证书与锥扫描

- **稳定 ID**：R-2fc-round3-search-root-20261031
- **对象类型**：计算（有限实例证书、有限搜索、复现边界）
- **来源**：七个清洗源，详见 `archives/customer-attraction/tools/evidence/R-2fc-round3-search-root-20261031/source-manifest.json`；原始导出来自 `R-2fc8878b4bdd4328bbc1bcf1df8ca831/round3_search/`。
- **模型范围**：五个玩家、七或八个主题、有限非空共同目录、完整有序历史的纯策略 SPE 检验；这是当前六人目标模型的有限探针，不能替代六人命题。

## 逐源结论

### 1. `m5p7_pos1.best.json`（9c75460d08c374607940）

固定五玩家、七主题、35 步、seed `2026102134`、position 1 的完整策略。精确回放验证策略表大小 `1+7+7^2+7^3=2801`，对所有 19607 个“每个决策历史 × 每个单步偏离”比较均通过；当前路径为 `(0,2,0,0,0)`，`W=6`，有限终局穷举得到 `OPT=9`，最小偏离松弛为 0（允许任意平局）。因此这是完整历史纯 SPE 证书，并满足 `2W=12>9=OPT`。

### 2. `m5p7_pos1.json`（de736e9d061300a93280）

同一实例的有限早期攻击/锥扫描报告，`finished_steps=35`、`cones=34`、`records=65`，最佳记录比值为 `9`。报告自身把“没有找到反例”限定为搜索事实；保留为可复现实验边界，不能升格为全称结论。

### 3. `m5p7_pos2_multi.best.json`（089592c096af119504ad）

五玩家、七主题、65 步、seed `2026102137`、`min_support=2`、`mode=min-attacker` 的完整策略。精确重算 2801 个历史动作以及 19607 个单步偏离，实际路径 `(0,0,5,0,0)`，`W=5`、`OPT=9`，最小松弛为 0，故为完整历史纯 SPE 证书；`2W=10>9=OPT`。这条证书的终局工作值低于同批另两条，但仍超过目标一半。

### 4. `m5p7_pos2_multi.json`（3f0db73541b98afb1119）

对应 `min_support=2` 搜索的有限锥报告，`finished_steps=65`、`cones=59`、`records=119`，最佳记录比值为 `9`。只证明给定种子/步数/候选枚举中的记录，不证明不存在其他模型或其他路径上的更差 SPE。

### 5. `m5p8_pos0_multi.best.json`（10f6ed4f50c00ddd45eb）

五玩家、八主题、30 步、seed `2026102138`、`min_support=3`、`mode=max-attacker` 的完整策略。策略表大小 `1+8+8^2+8^3=4681`，对 37448 个单步偏离逐一用 Fraction 检验；实际路径 `(0,7,2,2,0)`，`W=6`、`OPT=9`，最小松弛为 0，满足 `2W=12>9=OPT`。

### 6. `m5p8_pos0_multi.json`（2a2166a3cfd559a80fac）

对应八主题搜索的有限锥报告，`finished_steps=30`、`cones=21`、`records=51`，最佳记录比值为 `9`。同样只保留为有限扫描证据。

### 7. `unit_point_audit.json`（d6bc176f1ca2ecaedc20）

六条单位点审计记录均报告 `full_history_SPE=true`、`violations=[]`，并给出完整历史决策数与非自身偏离数：\n
- 两条四玩家六主题记录：`W=5`、`OPT=7`、`half_gap=3`、259 个决策历史、1295 个非自身偏离；\n- 三条五玩家七主题记录：`W=6,6,5`、`OPT=9`、`half_gap=3,3,1`、2801 个决策历史、16806 个非自身偏离；路径分别为 `(2,0,0,0,0)`、`(0,2,0,0,0)`、`(0,0,5,0,0)`；\n- 一条五玩家八主题记录：`W=6`、`OPT=9`、`half_gap=3`、4681 个决策历史、32767 个非自身偏离，路径 `(0,7,2,2,0)`。\n
## 比较、独有内容与接续

本批独有的强证据是三份完整策略表的逐历史精确复放：它把扫描报告里的候选压缩成可审计的 `W/OPT`、实际路径、动作数量和所有偏离松弛；并将 `unit_point_audit` 的六个固定点与这些复放结果对齐。三份扫描报告保留了搜索参数、步数、候选锥数量和随机种子，供后续扩大实例或寻找半值失败反例；不把“最佳记录为 9”写成普遍下界。\n
后续可接续方向：把这些证书的客户多重集、动作表和 tie 规则与六人模型的完整历史状态编码逐一比对；再做六人、六提供者、完整有序历史的独立精确验证。任何要宣称普遍 `W >= OPT/2` 的论证仍需处理空主题、重复主题、零客户、离轨历史及任意平局，当前七源没有覆盖这些全称量词。\nEOF
cat > cleanup/workspaces/Boss2/receipts-R-2fc-round3-search-root-20261031.json <<'EOF'
[
  {"id":"9c75460d08c374607940","full_file_reviewed":true,"related_material_checked":true,"unique_content_accounted_for":true,"read_note":"完整读取并精确复放 m5p7_pos1.best.json；核对 2801 个动作、19607 个偏离、实例与路径。","comparison_note":"与同实例扫描报告及 unit_point_audit 对齐。","decision_note":"固定实例完整历史纯 SPE 证书，W=6, OPT=9, 2W>OPT。","disposition":"integrated","targets":["archives/customer-attraction/state/计算/R-2fc-round3-search-m5p7-m5p8有限SPE证书与锥扫描--计算.md","archives/customer-attraction/tools/evidence/R-2fc-round3-search-root-20261031/"]},
  {"id":"de736e9d061300a93280","full_file_reviewed":true,"related_material_checked":true,"unique_content_accounted_for":true,"read_note":"完整读取 m5p7_pos1 有限锥扫描报告，核对 finished_steps/cones/records 与 scope caveat。","comparison_note":"与对应 best 证书和六点审计比较。","decision_note":"保留有限搜索边界，明确缺少反例不构成全称证明。","disposition":"retained-as-finite-search","targets":["archives/customer-attraction/state/计算/R-2fc-round3-search-m5p7-m5p8有限SPE证书与锥扫描--计算.md","archives/customer-attraction/tools/evidence/R-2fc-round3-search-root-20261031/"]},
  {"id":"089592c096af119504ad","full_file_reviewed":true,"related_material_checked":true,"unique_content_accounted_for":true,"read_note":"完整读取并精确复放 m5p7_pos2_multi.best.json；核对 2801 个动作、19607 个偏离、实际路径。","comparison_note":"与 min_support=2/mode=min-attacker 扫描及 unit audit 的 W=5 条目比较。","decision_note":"固定实例完整历史纯 SPE 证书，W=5, OPT=9, 2W>OPT。","disposition":"integrated","targets":["archives/customer-attraction/state/计算/R-2fc-round3-search-m5p7-m5p8有限SPE证书与锥扫描--计算.md","archives/customer-attraction/tools/evidence/R-2fc-round3-search-root-20261031/"]},
  {"id":"3f0db73541b98afb1119","full_file_reviewed":true,"related_material_checked":true,"unique_content_accounted_for":true,"read_note":"完整读取 m5p7_pos2_multi 有限锥扫描，核对 65 步、59 cones、119 records。","comparison_note":"与对应 best 证书比较，确认 scope 仍是有限搜索。","decision_note":"保留实验记录，不把有限最佳值提升为定理。","disposition":"retained-as-finite-search","targets":["archives/customer-attraction/state/计算/R-2fc-round3-search-m5p7-m5p8有限SPE证书与锥扫描--计算.md","archives/customer-attraction/tools/evidence/R-2fc-round3-search-root-20261031/"]},
  {"id":"10f6ed4f50c00ddd45eb","full_file_reviewed":true,"related_material_checked":true,"unique_content_accounted_for":true,"read_note":"完整读取并精确复放 m5p8_pos0_multi.best.json；核对 4681 个动作、37448 个偏离、实际路径。","comparison_note":"与八主题有限锥报告和 unit audit 八主题记录比较。","decision_note":"固定实例完整历史纯 SPE 证书，W=6, OPT=9, 2W>OPT。","disposition":"integrated","targets":["archives/customer-attraction/state/计算/R-2fc-round3-search-m5p7-m5p8有限SPE证书与锥扫描--计算.md","archives/customer-attraction/tools/evidence/R-2fc-round3-search-root-20261031/"]},
  {"id":"2a2166a3cfd559a80fac","full_file_reviewed":true,"related_material_checked":true,"unique_content_accounted_for":true,"read_note":"完整读取 m5p8_pos0_multi 有限锥扫描，核对 30 步、21 cones、51 records。","comparison_note":"与对应 best 证书和八主题审计比较。","decision_note":"保留有限搜索边界，明确不支持普遍结论。","disposition":"retained-as-finite-search","targets":["archives/customer-attraction/state/计算/R-2fc-round3-search-m5p7-m5p8有限SPE证书与锥扫描--计算.md","archives/customer-attraction/tools/evidence/R-2fc-round3-search-root-20261031/"]},
  {"id":"d6bc176f1ca2ecaedc20","full_file_reviewed":true,"related_material_checked":true,"unique_content_accounted_for":true,"read_note":"完整读取六条 unit_point_audit；核对每条 full_history_SPE、violations、W/OPT、half_gap 与偏离计数。","comparison_note":"与三份 best 证书和对应扫描报告逐条对齐。","decision_note":"保留六个固定点的精确审计；全部无违规且 2W>=OPT。","disposition":"integrated","targets":["archives/customer-attraction/state/计算/R-2fc-round3-search-m5p7-m5p8有限SPE证书与锥扫描--计算.md","archives/customer-attraction/tools/evidence/R-2fc-round3-search-root-20261031/"]}
]
