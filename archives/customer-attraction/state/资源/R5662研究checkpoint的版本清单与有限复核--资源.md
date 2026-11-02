---
id: customer-attraction/r5662-checkpoint-versions-and-finite-replay
kind: resource
type_tag: 资源
title: R5662研究checkpoint的版本清单与有限复核
status: complete
truth_status: historical-manifest-and-finite-replay-not-new-proof
summary: 完整保存174项研究资产清单、7项父方复放与依赖封包检查、18主题总势必要点回放；172项与冻结清单同字节、两入口版本不同，不把封包或有限输出当一般六人结论。
source_refs:
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/checkpoint_manifest.json
- source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/checkpoint_manifest.json
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/checkpoint_verification.json
- source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/checkpoint_verification.json
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/potential_menu_replay.json
- source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/potential_menu_replay.json
---

# 三份资源的身份与准确用途

本页全文读取R-5662工作区的checkpoint_manifest、checkpoint_verification和potential_menu_replay三份冻结JSON，逐项区分路径/SHA/字节清单、父方历史复放声明与必要点的精确数值。它们不是三个新的福利命题。原件及双冻结版本身份见[源清单](../../tools/evidence/r566-checkpoint-metadata-primary/source-manifest.json)。本批未运行所列7个历史入口，也没有从manifest推定其174个成员均已读、均已清洗或数学成立。

## 174项manifest的覆盖与版本边界

原manifest的scope是“Curated research checkpoint; conditional proofs, exact inputs and explicitly labeled unfinished interfaces. No target proof or counterexample claimed.” snapshot_commit=b48a7563106808df5ff95bcc0160a8dd9b864ba1，note明确哈希对应该snapshot的内容，而非后来改稿。174个路径互异，总声明大小17,810,557B；清单本身不含自己，不能把174称全部工作区文件。

本批逐项以冻结inventory的(path,SHA256,size)三元组比较，172项有相同冻结版本；两个入口是旧版本：FRONTIER.md声明8086B/SHA228ae0...，README.md声明3221B/SHAd57fc5...，与本次冻结同路径版本不同。完整SHA、所有匹配source ID与两项差异保存在[逐项比较](../../tools/evidence/r566-checkpoint-metadata-primary/manifest-inventory-comparison.json)。这里只核已知冻结元数据，没有取回snapshot b48的全树或伪造那两份旧稿，也不推定版本不同意味着内容错误。

清单覆盖研究₁到研究₆的发现器、原始/精确输入、候选接口、审查和父方回放。四copy threshold脚本等后续文件不在这174项中，不能借manifest替它们认证。原件保每项全部SHA和字节，下面逐项给恢复用途的路径与大小：

|序号|工作区内路径|声明字节|
|---:|---|---:|
|0|`FRONTIER.md`|8086|
|1|`README.md`|3221|
|2|`action_quotient_replay.json`|636|
|3|`audit_containment.json`|405|
|4|`audit_containment.py`|3118|
|5|`audit_tail3_B_projection.py`|1416|
|6|`audit_threefold.json`|1861|
|7|`audit_threefold.py`|3409|
|8|`checkpoint_verification.json`|2027|
|9|`coordination.md`|15960|
|10|`dense_seven_scope_audit.json`|578|
|11|`fourcopy_threshold_replay.json`|2293|
|12|`potential_menu_replay.json`|1561|
|13|`research_1/B_menu_actual_price_separation.json`|719|
|14|`research_1/B_reply_menu_actual_prices.md`|3028|
|15|`research_1/HANDOFF.md`|4591|
|16|`research_1/README.md`|2547|
|17|`research_1/audit_B_menu_actual_prices.py`|1592|
|18|`research_1/audit_seed_actual_prefix.py`|1942|
|19|`research_1/bigint_controller_attack.py`|5852|
|20|`research_1/bigint_controller_report.json`|2708|
|21|`research_1/full18_cone_attack.py`|6548|
|22|`research_1/full18_exact_bi.json`|1511|
|23|`research_1/full18_exact_bi.py`|2238|
|24|`research_1/full18_vertex_recovery.json`|211|
|25|`research_1/full18_vertex_seed.json`|16045|
|26|`research_1/reset_swap_minimum_rows.md`|3997|
|27|`research_1/seed18_Rdiag_actual_prefix_audit.json`|5199|
|28|`research_1/seed18_Rdiag_report.json`|1111|
|29|`research_1/seed18_Zdiag_report.json`|1111|
|30|`research_1/swap_B_L_visible_projection.py`|4695|
|31|`research_1/swap_B_coupling_projection.py`|4956|
|32|`research_2/B_family_oracle.py`|3898|
|33|`research_2/B_menu_prices_master.py`|3541|
|34|`research_2/HANDOFF.md`|3969|
|35|`research_2/README.md`|8136|
|36|`research_2/all_menu_prices_exact.json`|1441208|
|37|`research_2/branch_family_lp.py`|4554|
|38|`research_2/combine_old702.py`|1543|
|39|`research_2/coupled_B_branch_master.md`|3475|
|40|`research_2/coupled_B_branch_master.py`|4508|
|41|`research_2/coupled_B_families_exact.json`|1001167|
|42|`research_2/coupled_B_families_master.py`|4820|
|43|`research_2/coupled_B_master_exact.json`|844597|
|44|`research_2/early_B_projection_certificate.json`|138135|
|45|`research_2/early_B_projections.md`|5738|
|46|`research_2/early_B_projections.py`|3799|
|47|`research_2/export_root_lines.py`|2520|
|48|`research_2/last_three_lp.py`|2336|
|49|`research_2/lift_old_point.py`|2917|
|50|`research_2/max_branch_lp.py`|4213|
|51|`research_2/maxroot_identity_exact.json`|1440157|
|52|`research_2/maxroot_identity_master.py`|4684|
|53|`research_2/nested_branch_lp.py`|4647|
|54|`research_2/old702_plus_B_families.py`|3282|
|55|`research_2/prefix_floor_lp.py`|2064|
|56|`research_2/root_copy_lp.py`|2839|
|57|`research_2/root_lines_certificate_v2.json`|5565|
|58|`research_2/tail3_B_projection.md`|4806|
|59|`research_2/tail3_B_projection.py`|3075|
|60|`research_2/tail3_B_projection_certificate.json`|36617|
|61|`research_2/verify_root_lines.py`|2652|
|62|`research_3/HANDOFF.md`|5503|
|63|`research_3/all_reply_actual_floors.py`|4342|
|64|`research_3/all_reply_floors_exact.json`|815347|
|65|`research_3/all_reply_mixed_pair_exact.json`|816556|
|66|`research_3/all_reply_query_cuts_exact.json`|815911|
|67|`research_3/audit_cross_source_basic.py`|3019|
|68|`research_3/capacity_master_price_cuts.json`|5134|
|69|`research_3/continuous_old_query_cuts.json`|15013|
|70|`research_3/continuous_old_query_cuts.py`|4531|
|71|`research_3/continuous_refinement_cuts.json`|3252|
|72|`research_3/continuous_refinement_exact.json`|816661|
|73|`research_3/coupled_pending_cuts.json`|3013|
|74|`research_3/cross_source_basic_review.md`|2210|
|75|`research_3/early_reply_requery_cuts.py`|4424|
|76|`research_3/early_reply_requery_master_all_queries.json`|6165|
|77|`research_3/mixed_pair_reply_rows.py`|1527|
|78|`research_3/new_reply_floor_rows.md`|2721|
|79|`research_3/old_query_cuts.json`|2130|
|80|`research_3/old_query_reply_cuts.py`|4128|
|81|`research_3/refine_continuous_queries.py`|3324|
|82|`research_3/refine_terminal_portfolio.py`|3600|
|83|`research_3/replay_stationary_successor_transfer.py`|701|
|84|`research_3/shared_terminal_portfolio.md`|3942|
|85|`research_3/stationary_successor_transfer.md`|3644|
|86|`research_3/terminal_capacity_refinement_cuts.json`|11523|
|87|`research_3/terminal_capacity_refinement_exact.json`|819848|
|88|`research_3/terminal_portfolio_cuts.py`|5223|
|89|`research_3/terminal_portfolio_refinement_cuts.json`|2838|
|90|`research_3/terminal_portfolio_refinement_exact.json`|815964|
|91|`research_3/weighted_early_reply_requery.md`|2869|
|92|`research_4/README.md`|4009|
|93|`research_4/minimum_reply_commutation.md`|4766|
|94|`research_4/minimum_reply_commutation_report.json`|590|
|95|`research_4/verify_minimum_reply_commutation.py`|2779|
|96|`research_5/B_menu_actual_last_price_check.json`|320|
|97|`research_5/HANDOFF.md`|7276|
|98|`research_5/README.md`|9164|
|99|`research_5/check_B_menu_actual_last_price.py`|916|
|100|`research_5/combined_branch_latest_exact.json`|823005|
|101|`research_5/combined_branch_local_exact.json`|822687|
|102|`research_5/combined_branch_master.md`|5032|
|103|`research_5/combined_branch_master.py`|4621|
|104|`research_5/combined_branch_master_exact.json`|816453|
|105|`research_5/coupled_latest_exact.json`|842782|
|106|`research_5/coupled_latest_master.py`|2010|
|107|`research_5/cross_branch_slab.py`|12196|
|108|`research_5/cross_branch_slab_ablation.json`|643|
|109|`research_5/cross_branch_slab_status.json`|446|
|110|`research_5/cross_source.md`|5147|
|111|`research_5/cross_source_graph.py`|4371|
|112|`research_5/cross_source_priced_optimum_exact.json`|815736|
|113|`research_5/diagonal_basic_check.py`|3061|
|114|`research_5/early_reply_exact.json`|815384|
|115|`research_5/early_reply_floors_exact.json`|815400|
|116|`research_5/early_reply_prices.py`|3921|
|117|`research_5/joint_local_cuts.json`|3121|
|118|`research_5/joint_local_v2_cuts.json`|6533|
|119|`research_5/materialize_diagonal_seeds.py`|4475|
|120|`research_5/nested_reply_cuts.json`|2568|
|121|`research_5/nested_reply_projection.py`|4993|
|122|`research_5/pair_closure.py`|6572|
|123|`research_5/pair_closure_exact.json`|114803|
|124|`research_5/pair_cross_exact.json`|127211|
|125|`research_5/pair_master_exact.json`|158498|
|126|`research_5/review_terminal_portfolio.json`|320|
|127|`research_5/review_terminal_portfolio.md`|2493|
|128|`research_5/review_terminal_portfolio.py`|1913|
|129|`research_5/seed18_Rdiag.json`|38200|
|130|`research_5/seed18_Zdiag.json`|49732|
|131|`research_5/split_basic_exact.json`|814800|
|132|`research_5/split_basic_graph.py`|4563|
|133|`research_5/tail_r1_pair_identity.py`|561|
|134|`research_5/tail_reply_cuts.json`|1671|
|135|`research_5/tail_reply_cuts.py`|5035|
|136|`research_5/tail_reply_subset.py`|5730|
|137|`research_5/tail_reply_subset_cuts.json`|534|
|138|`research_5/zz_cross_exact.json`|124405|
|139|`research_5/zz_direct.py`|2017|
|140|`research_5/zz_split_exact.json`|112746|
|141|`research_5/zz_threshold_closure.py`|8353|
|142|`research_5/zz_threshold_exact.json`|136130|
|143|`research_6/HANDOFF.md`|3226|
|144|`research_6/audit_potential_menu_joint.json`|2184|
|145|`research_6/audit_potential_menu_joint.py`|5937|
|146|`research_6/audit_potential_menu_joint_private.json`|2033|
|147|`research_6/catalog_completion_probe.json`|25991|
|148|`research_6/catalog_completion_probe.py`|3820|
|149|`research_6/large_catalog_menu_priced_target_attack.json`|1263|
|150|`research_6/large_catalog_menu_target_attack.json`|1635|
|151|`research_6/large_catalog_target_attack.json`|2590|
|152|`research_6/large_catalog_target_attack.py`|12474|
|153|`research_6/make_target_attack_seeds.py`|2244|
|154|`research_6/paired_esm_candidate.md`|2661|
|155|`research_6/potential_menu_joint.json`|4966|
|156|`research_6/potential_menu_joint.md`|6876|
|157|`research_6/potential_menu_joint.py`|7080|
|158|`research_6/potential_menu_joint_private.json`|4346|
|159|`research_6/private_shared_omission_tradeoff.md`|2899|
|160|`research_6/seed_full18.json`|15753|
|161|`research_6/seed_reply_representatives8.json`|4205|
|162|`research_6/seed_union8.json`|3609|
|163|`research_6/seed_union_actual8.json`|3459|
|164|`research_6/target_attack_seed_index.json`|436|
|165|`review_action_quotient.md`|3871|
|166|`review_dense_seven_scope.md`|2634|
|167|`review_stationary_transfer.md`|1694|
|168|`review_tail3_B_projection.md`|1862|
|169|`review_threefold.md`|3176|
|170|`stationary_transfer_replay.json`|259|
|171|`tail3_B_projection_review.json`|403|
|172|`terminal_closure_replay.json`|432|
|173|`workspace.json`|150|

## 父方verification的全部内容与责任分层

原scope自称“Parent replay of saved authors implementations; not a second complete matrix reconstruction or external review.” 以下完整保留7项checks、curation_dependency_check及peer_author_replays；程序通过字段是这份历史报告的声明，本批不把它改称新盲审、第二套实现或外审。502条链接通过与git diff通过只检查封包/编辑，不认证数学。三套母矩阵5692/5112/5277行的最小余量0，只属于列明矩阵；commutation的1024策略/5个SPE/1/5差值，只属于该有限例。最终main_target明确OPEN且没有完整SPE反例。

```json
{
  "scope": "Parent replay of saved authors implementations; not a second complete matrix reconstruction or external review.",
  "checks": [
    {
      "entry": "research_2/B_menu_prices_master.py --all-families --verify",
      "rows": 5692,
      "columns": 4849,
      "minimum_slack": "0",
      "passed": true
    },
    {
      "entry": "research_3/refine_terminal_portfolio.py --capacity --verify",
      "rows": 5112,
      "minimum_slack": "0",
      "passed": true
    },
    {
      "entry": "research_5/coupled_latest_master.py --verify",
      "rows": 5277,
      "columns": 2033,
      "minimum_slack": "0",
      "passed": true,
      "known_later_cuts": true
    },
    {
      "entry": "research_4/verify_minimum_reply_commutation.py",
      "complete_two_tail_policies": 1024,
      "SPE_policies": 5,
      "strict_gap": "1/5",
      "passed": true
    },
    {
      "entry": "research_1/audit_B_menu_actual_prices.py",
      "passed": true,
      "scope": "strictly separates saved old5259 necessary point"
    },
    {
      "entry": "research/check_active_research.py",
      "links": 502,
      "passed": true
    },
    {
      "entry": "git diff --check",
      "passed": true
    }
  ],
  "curation_dependency_check": {
    "method": "Copy only previously tracked actor files plus curated selected paths to separate directory; other repository actors remain at original existing sources.",
    "entry": "research_2/B_menu_prices_master.py --all-families --verify",
    "passed": true,
    "rows": 5692,
    "scope": "Checks selected own-file dependency closure; does not independently reconstruct coefficients."
  },
  "peer_author_replays": {
    "seven_maxima_two_singleton": {
      "columns_each": 3904,
      "minimum_with_final": "34955/3308688",
      "minimum_without_final": "30253/9473184"
    },
    "mixed_singleton_constants": "all seven omitted labels passed",
    "incidence_tau_endpoint": "1006430343355/2012347307572"
  },
  "main_target": "OPEN; no complete SPE counterexample"
}
```

## 18主题总势回放的全部数值与真实缺口

这份potential_menu_replay声明scope为partial late-menu obstruction，明确not complete SPE。完整数据如下；六人实际收益向量、十八分量argmax和全部十八条倒二support slack均保留，不能只报0的三类末位检查：

```json
{
  "scope": "partial late-menu obstruction, not complete SPE",
  "scale": 27677343603300,
  "unit_customer_count": 56723525995500,
  "customer_types": 114,
  "potential_multisets": 100947,
  "maximum_potential": "189078419985/92257812011",
  "budget_W_plus_C": "189078419985/92257812011",
  "argmax": [
    0,
    0,
    0,
    0,
    0,
    0,
    1,
    1,
    1,
    1,
    1,
    1,
    0,
    0,
    0,
    0,
    0,
    0
  ],
  "actual_payoffs": [
    "1289542201617/9225781201100",
    "1289542201617/9225781201100",
    "1178243381667/9225781201100",
    "314576211408/2306445300275",
    "2065229163251/9225781201100",
    "536229851829/2306445300275"
  ],
  "actual_last_minimum_slack": "0",
  "optimal_source_minimum_slack": "0",
  "reply_full_catalog_minimum_slack": "0",
  "penultimate_all_alternatives_support_slack": [
    "34225705614/461289060055",
    "34225705614/461289060055",
    "91947828773/922578120110",
    "8824801061/92257812011",
    "77980023056/2306445300275",
    "-168357318739/9225781201100",
    "0",
    "0",
    "0",
    "0",
    "0",
    "0",
    "-480277410963/9225781201100",
    "-480277410963/9225781201100",
    "-480277410963/9225781201100",
    "-480277410963/9225781201100",
    "-480277410963/9225781201100",
    "-480277410963/9225781201100"
  ],
  "audit_source_sha256": "ff1536b0667244ca05a49ab1ea76a291dba50784524921e0dd5028c4b9364ec5",
  "int64_potential_upper_bound": 8338358321338500,
  "review_scope": "parent rerun of author independent materialization audit; no independent full row implementation"
}
```

最大势与W+C同为189078419985/92257812011；100947恰是18主题六槽允许重复多重集合数。scale=27677343603300展开为56723525995500单位客户、114类型；这没有产生新的完整策略。actual_last、optimal_source和reply_full_catalog三类最小余量0并未检查所有倒二偏离：索引5余量−168357318739/9225781201100，索引12至17均为−480277410963/9225781201100，故该必要点不能补成保持原实际倒二的SPE。完整解释已在[整终局势与真倒二菜单联合停界](../障碍/整终局势与真倒二菜单联合停界--障碍.md)与[四复制研究种子身份](../审查/四复制与末回复研究的原运行及种子身份--审查.md)中保存。

版本同样承重：此父方回放的audit_source_sha256=ff1536b0667244ca05a49ab1ea76a291dba50784524921e0dd5028c4b9364ec5，而174manifest声明research₆/audit_potential_menu_joint.py的SHA为245483e74f526dccfb0e0bcf5346afb0fdabd2d91a09fa7592bea3dd83becdf3。二者不能未经比对称同一代码版本；本页只保父方所报的执行身份，不拿冻结当前脚本冒作其逐字节生成器。int64上界8338358321338500属于实现数值范围检查，非均衡或复杂度定理。

## 接续与对象关系

清单用于定位文件/版本，verification用于理解当时复放范围，potential回放用于检查一种必要系统仍缺真实倒二偏离。它们可作为相应正文的来源、实现和有限检查关系，不能从“封包完整”或“未找到反例”推出一般half。第三阶段据这些解释逐边处理；本页不将174个路径自动导入为证明图。

## 冻结入口版本与既有有限输出的进一步对应

174条manifest和本次冻结inventory的完整(path,SHA256,size)比较仍为172条同版、2条另版、0条缺路径。两个入口的完整差异如下；它们是版本身份差异，不表示入口内容数学错误：

|入口|manifest所报snapshot版本|本次冻结同路径版本|
|---|---|---|
|FRONTIER.md|8086B；SHA256 `228ae0b1edbf4b9f8f2c01aa4884ecb46d7ef1b6305bc1ea97f5a5b911f077ed`|source ID `bbe87642e2efce14d63c`；9820B；SHA256 `6e89b1a05e7def262dae3612a6b5bfee17763a114acb2a7f52d22f48a08f53c7`|
|README.md|3221B；SHA256 `d57fc596b071189c7e99c2acde812beafa303f5004b1d975753297c3d4279a37`|source ID `2febc458086d3c08984e`；3913B；SHA256 `e8b0dbe0aa9f95a5836777cf55eacf9edb37fe35a840960c534d9bf57c71e30b`|

现有[普通点有限审计输出](../../tools/evidence/potential-menu-joint/replay/audit_normal.json)为2184B，SHA256 `cf0adfcdd698eb91cadeab684da3734c49b884889cf9af7928e2080955201946`，与manifest所列`research_6/audit_potential_menu_joint.json`同版。它与本页父方potential replay恰有13个共享顶层字段，全部精确相同：scope、scale、unit_customer_count、customer_types、potential_multisets、maximum_potential、budget_W_plus_C、argmax、actual_payoffs、三类minimum_slack以及完整penultimate_all_alternatives_support_slack。普通audit另外保有势超额0及私有谱失败数据；父方replay另有执行代码SHA、int64上界与review_scope。两份报告的字段差异不抹去各自来源。

现保存的5937B[审计代码](../../tools/evidence/potential-menu-joint/replay/audit_potential_menu_joint.py)与manifest同为SHA256 `245483e74f526dccfb0e0bcf5346afb0fdabd2d91a09fa7592bea3dd83becdf3`；它不是父方replay所报`ff1536b0667244ca05a49ab1ea76a291dba50784524921e0dd5028c4b9364ec5`的逐字节版本。共享数值相同只说明保存输出吻合，不能取代该历史执行版本的代码追溯。

这些报告的小量算式也相容：C(23,6)=100947，十八分量argmax和为6，六实际收益之和W=1，最大势减W+C为0；十八倒二support slack恰5正、6零、7负。潜势整数上界8338358321338500恰为单位客户数56723525995500乘60H6=147，低于有符号int64上界。这是转写与标量相容性复核，没有重新运行历史入口、遍历全部势多重集、重构矩阵或给完整SPE认证。

本轮逐项复核的[完整结果](../../tools/evidence/r566-checkpoint-metadata-primary/review-20261101/verification.json)与[复核入口](../../tools/evidence/r566-checkpoint-metadata-primary/review-20261101/verify_metadata.py)保留来源/转写/标量检查；它们不执行原数学研究入口。

## 174项版本身份与七项历史检查的后继证据

checkpoint_manifest.json 的全部174条(path,SHA256,bytes)已重新从冻结 inventory 独立比较，仍为172同版、FRONTIER/README两条另版、零缺路径；结果与本页既有逐项比较完全相同。174条路径全部处于R-5662工作区内，故清单不是完整仓库依赖清单。特别，verification列出的 `research/check_active_research.py` 在工作区外，其他研究者的原模块也不会因本actor清单而获得版本封包认证。manifest的 `snapshot_commit` 和 `note` 是所列文件的版本定位，不能补出未记录的旧运行时点、完整argv或依赖加载记录。

下表逐条解释历史 `passed`，并将现有后继证据与旧报告区分。五个数学入口的现保存源码均已逐字节核为manifest所列版本；本次只读取源码、既有输出和执行记录，没有再次运行这些入口。

|历史check|历史字段与准确含义|现保存的后继对应及边界|
|---|---|---|
|`research_2/B_menu_prices_master.py --all-families --verify`|5692行、4849列、minimum_slack=0、passed=true；固定16hist必要系统的保存点回代。|[四菜单证据](../../tools/evidence/b-family-menu-prices-boss3/README.md)保一次同SHA原入口、exit0、5692/4849/min0；是原row builder回代，另有独立28新价/列合同检查，非全矩阵第二实现。|
|`research_3/refine_terminal_portfolio.py --capacity --verify`|5112行、minimum_slack=0、passed=true；不是5692或5277点。|[容量证据](../../tools/evidence/terminal-capacity-refinement-boss3/README.md)保一次同SHA原入口，stdout记base5083+29=5112/min0；独立29行/1905列比较另有范围，无需重跑。|
|`research_5/coupled_latest_master.py --verify`|5277行、2033列、minimum_slack=0、passed=true、known_later_cuts=true。|[5277证据](../../tools/evidence/coupled-latest-menu-check-boss3/README.md)保后继原builder完整回代及接口核；该后继事件明确没有调用原master的main/verify，不能倒填为旧命令的原始运行日志。它还给普通Y末价负值，原已列行通过与遗漏合法行严格分离可同时成立。|
|`research_4/verify_minimum_reply_commutation.py`|1024份完整两人尾策略、5份尾SPE、strict_gap=1/5、passed=true。|[局部枚举证据](../../tools/evidence/minimum-reply-commutation-program/README.md)保一次同SHA未改原main及590B stdout；stdout与manifest所列原报告同SHA。实例是15客户、四主题、固定(0,1,1,3)前缀后的两人尾，不是六人根完整SPE。|
|`research_1/audit_B_menu_actual_prices.py`|passed=true；scope为严格分离保存的old5259必要点。|同SHA源码默认读 `coupled_B_master_exact.json`，输入SHA `6269be5cbcd61d397c33e19ce2ac31ace3f73aeec22c978426d8f3b30b0fada7` 时断言第六价余量为负。这里的passed是成功发现遗漏真价，不是所有价格可行，更不能把该负值移给后来重排的5692点。|
|`research/check_active_research.py`|502条链接、passed=true。|保为历史链接检查声明；该JSON没有其当时源码/命令环境/输出绑定，不能据502推数学正确或依赖完整。|
|`git diff --check`|passed=true。|保为历史编辑检查声明；它检查diff格式，不证明定理、输入可行性、完整SPE或全仓清洗完成。|

`curation_dependency_check` 的method明确是把原已跟踪的actor文件与所选路径复制到独立目录，**其他actor仍使用原来既有来源**；其5692行passed只检查这次所选own-file整理没有打断该入口依赖，不表示所有仓库依赖均独立打包，也不独立重构系数。现后继封包有自己的物化清单与运行事件，不能回填为当年该次复制的日志。

`peer_author_replays` 三组字段也保各自量词：七极大至多两个singleton-block的两轨各3904列，余项分别34955/3308688和30253/9473184，是该结构子类的有理证书；`mixed_singleton_constants = all seven omitted labels passed` 只是该原报告对条件常数检查的文字声明，不取消mixed-singleton条件；incidence端点1006430343355/2012347307572是六项和在τ=149/50处的数值。标量重算确有

$$\sum_{r=1}^{6}\frac1{6+(149/50-1)r}=\frac{1006430343355}{2012347307572}>\frac12,$$

与报告相符，但这个算式不证明相应动态预算接口。既有分数覆盖预算已包含其τ-only半覆盖范围，带共同核的加法式另保原条件，不能从一个端点数推出任意目录结论。peer字段没有在本次重新运行底层审计。

这些后继核对补充的是版本和责任边界。原verification全部字段已在本页完整转写，`main_target = OPEN; no complete SPE counterexample` 保持原义；不从现封包、同SHA源码、同数值输出或局部有限证书合成一般六人half证明。
