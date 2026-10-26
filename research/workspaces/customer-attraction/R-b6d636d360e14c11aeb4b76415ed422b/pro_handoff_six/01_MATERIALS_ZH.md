# 材料说明

本包是主题精选材料，不是整仓库。所有 `source/` 内原文、程序和数据取自 `MANIFEST.json` 指明的同一 Git 提交，除根定位占位文件外保持原字节。长 JSON 和旧程序依赖放在原目录，仅供需要时核验；没有要求先读完或沿用这些方法。

## 模型、已证结果与一般工具

下表 `current/` 指 `source/research/current/customer_attraction/`，`five/` 指 `source/customer_attraction/proofs/half5_exact_v1/`。

| 材料 | 内容与状态 |
| --- | --- |
| `current/model.md` | 精确模型、全部历史量词、收益与客户类型表示。 |
| `current/three_player_sharp.md`、`four_player_bound.md` | 三人锐界 5/3、四人界 1499/750；是任意目录的已证固定人数结果，不是人数归纳定理。 |
| `current/five_player_half.md` | 五人半覆盖的现行定理入口与审查边界。 |
| `five/PROOF_ZH.md` | 完整五人证明：真实策略分支、53 个正乘子、全类型非负恒等式。 |
| `five/ACTIVE_ROWS_ZH.md` | 最终各行对应哪些真实节点和偏离。 |
| `five/LOCAL_LEMMAS_ZH.md`、`MAXROOT_LEMMA_ZH.md` | 局部比较、隐藏回复投影、最大主题根分支关系的原始证明。 |
| `five/certificate.json`、`row_manifest.json`、`components/`、核验程序 | 原五人完整精确支持文件。有限的是覆盖任意实例的系数类型域，不是客户数或目录规模抽样。 |
| `current/two_remaining_tax.md`、`four_remaining_profit_bound.md`、`tail_profit_lift.md` | 带背景的尾局利润工具及合法提升；剩余利润和全局覆盖是不同量。 |
| `current/priced_hidden_reply_projection.md` | 任意人数的共同末位报价、隐藏回复投影、人数压缩、强末对和同菜单互查；局部引理已证，六人及一般共同付款未证。 |
| `current/same_source_reply_requery.md` | 同源强制选择后，再查询真实回复的通用关系；已证局部工具，不是六人定理。 |
| `current/fractional_cover_path_budget.md`、`oblivious_security.md` | 真实前缀分数覆盖预算、静态安全值比较；相应动态聚合桥尚未闭合。 |
| `current/strategy_cone.md`、`exact_solver.md` | 固定完整策略的精确重数锥、保留全部可实现续局的集合值逆向归纳。 |
| `current/optimal_first_action_branch_gap.md`、`general_half_proof.md` | 已证恒等式与一般工作稿；其中明确标记的缺口和候选仍是缺口、候选。 |
| `source/research/customer_attraction/FAILED_ROUTES.md` | 按机制列出的精确失败合同、来源及仍有效部分。辅助桥失败只否定其写明的范围。 |

五人完整包由用户以已完成资产提供，当前仓库贡献是入库、复跑和内部审查，见 `source/research/reviews/customer_attraction/five_player_half_import.md`。原 `PROOF_ZH.md` 有两份实现的历史说明；本包不据此声称取得并重跑了第二个独立主域程序。现有可运行主域程序、局部程序及其实际复跑边界以该审查页为准。没有记录外部同行评审。

## 六人已有信息与方法边界

以下完整路径都在 `source/research/workspaces/customer-attraction/` 下。目录名只是保留原始引用和可运行依赖，并非要求恢复任何角色。

| 材料位置 | 内容与准确范围 |
| --- | --- |
| `R-a8ee6fdb155c47da95540775b4a6a2db/closure/README.md` | 27 个完整共同 R/Z 会员原子，满足指定必要条件图仍有 W/O≈0.49397351073；还能在相同实际收益和 K 上接入 336 族最大根图。这证明这些**指定关系**不足，不是游戏、SPE、目标反例或最优比例。 |
| 同目录 `joint_atoms_exact.json`、`root_extension_exact.json` 及核验依赖 | 上述共同可行见证的精确数据与可重放程序。3949 含辅助约束；原始族为 1143，二者不是同一种行数。程序依赖旧库的部分保留原审查等级，不冒称全部有第二独立实现。 |
| `R-a8ee6fdb155c47da95540775b4a6a2db/parent/suffix_envelope_boundary.md` 及输入、核验器 | 十二主题、6000 客户的指定路径满足全部实际后缀的势包络与前缀安全行，覆盖比 49%；因真实倒二盈利偏离而不是 SPE。只证明这些包络不足以直接推出 half，不否定势候选本身。 |
| `R-23ab27f8efb44f1faca2699d45886250/general_n/zero_regret_promotion_reset.md` 及独立程序 | 七客户、三人、四主题的完整 SPE：提前原末主题可令势下降 1，源 IC 及指定回放链 IC 余量全为零。否定特定局部支付桥，不否定 half；是小型真实全历史反例。 |
| `R-d1fe1e0c444e40d68b6813bf88db8fba/six_difficulty/README.md` | 五人表原位搬到六人的一客户反例，以及部分系数域可精确压缩的独立诊断。没有证明六人必有本质难度跃迁。 |
| `R-c4f1ef099fad483c9f81283b61eb0b53/parent/potential_copy_candidate.md` | 调和势与有序自复制税候选，OPEN。它既不是已证引理，也不是 half 的完整等价表述。 |
| `R-a8ee6fdb155c47da95540775b4a6a2db/potential/exclusion_safety_margin.md` | 势排除损失与实际安全余量候选；最后两位已证，较早位置未证；即使成立仍另有覆盖收尾。 |

程序依赖中保留的旧行生成器和必要 JSON 是为了复现上述确切见证，不构成对旧模板继续研究的建议。未附全部逐轮 LP 输出、扫描日志、协作公屏、角色规则、其他课题、Git 历史或凭据。某个原文中的相对链接可能指向未入选的历史资产；所列核验入口的运行依赖另外经过解压测试。

## 程序与证据

`source/customer_attraction/` 另含精确实例、全集 SPE 求解器和完整策略核验器。它们适用于有限输入；没有据有限搜索证明本包六人全称命题。

`02_REPRODUCTION_ZH.md` 是运行说明。`MANIFEST.json` 标明每个入选源文件的原路径、字节数、SHA-256 与冻结版本；`SELECTION.json` 列出分组。包内新增文件只是本次导航与核验启动器，没有新增数学定理。
