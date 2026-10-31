---
id: "customer-attraction/r2fc-global-proof-eight-source-audit"
kind: computation
type_tag: "计算"
title: "R-2fc global_proof 八源的精确核查、碰撞自由障碍与有限工具边界"
status: "partial-source-read-with-exact-replays"
truth_status: "finite-evidence-retained; no-general-half-conclusion"
review_level: "two-frozen-sources-read-and-replayed; six-source-blobs-missing-from-local-partial-clones; related-mathematical-texts-compared"
scope: "R-2fc8878b4bdd4328bbc1bcf1df8ca831/global_proof 中八个已认领脚本/JSON；共同目录、单位客户、完整有序历史纯SPE；只保留固定输入、有限枚举和有限浮点探针的量词"
summary: "五客户两人碰撞自由障碍的冻结 JSON 已全文读取并由独立 Fraction 程序复核；背景 Markov-LP 源已全文读取，q=6,r=3,seed=29393 的100棵有限试验重跑无负点。其余六个冻结 blob 在本地 partial clone 缺失，clean show 的 bad-object 失败原样留存；已有 global_proof 正文、独立实现和旧证据提供可比较数学范围，但不冒充六份缺失原文已读。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/global_proof/audit_collision_free_family.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/global_proof/audit_collision_free_obstruction.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/global_proof/audit_truncated_potential.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/global_proof/background_regret_probe.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/global_proof/collision_free_family_audit.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/global_proof/collision_free_obstruction_audit.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/global_proof/collision_free_ratio_best.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/global_proof/collision_free_ratio_probe.py"
evidence_packet: "../../tools/evidence/R-2fc-global-proof-a-20261031/"
related_objects:
  - "../反例/三人碰撞自由族福利障碍--反例.md"
  - "../计算/背景首步反例发现与精确重放--计算.md"
  - "../反例/三人均衡调和势低于最优覆盖的十一客户证书--反例.md"
  - "../资源/无拥挤完整均衡族原稿与有限探索的准确范围--资源.md"
---

# 读取边界与来源身份

本对象对应同一路径下的八份库存源。用户消息把背景程序的 ID 写成 `3086d1200c57312720a`；冻结 inventory 的实际 ID 是 `3086d1200c57312720e2`，本对象按 inventory 保留后者。八源在 legacy-cleanup 与 main 两个冻结提交中均有同一路径版本；库存大小和 SHA 见本批 [source-summary.json](../../tools/evidence/R-2fc-global-proof-a-20261031/metadata/source-summary.json)。

先逐源执行 `GIT_NO_LAZY_FETCH=1 python work.py clean show ID --out ...`。`background_regret_probe.py`（3186 B，SHA-256 `0d2e76e18c540183ac37f52559f5a57f427517822d01a25ad81533c4e49c2cb9`）和 `collision_free_obstruction_audit.json`（954 B，SHA-256 `dd946143d6d4aee7f381b69b6ab59be775ea2a35029aee42fb841ef9661287e9`）返回码 0，全文原字节保存于 evidence 的 `source/` 和 `clean-show/`。另外六个 blob（family 审计程序、obstruction 程序、truncated 程序、family JSON、ratio JSON、ratio 程序）在本地 partial clone 中未物化；`clean show` 原始输出是 `fatal: bad object ...`，逐条保存于 `clean-show/*.log`。没有把已有的不同 SHA 独立实现当作冻结原件，也没有伪造缺失尾部。

已有 related 文本和独立实现被全文读取用于比较：`global_proof/README.md`、`collision_free_three_halves_family.md`、`collision_free_occupancy_obstruction.md`、`promoted_punishment_family_failure.md`、`harmonic_potential_obstruction.md`，以及当前证据包中的 `audit_collision_free_family_independent.py/.json` 与 `audit_collision_free_occupancy_independent.py/.json`。这些文件的 SHA 与路径在 evidence `related/` 保留；它们是关联材料，不能替代六份缺失 blob 的 `full_file_reviewed=true` 声明。

# 八源逐项数学范围

## 1. `audit_collision_free_family.py` 与 `collision_free_family_audit.json`

关联正文给出的对象是：对每个整数 (kge1)，有 (k+1) 名单位提供者、每组两名核心客户 (X_i)、一个私有客户 (a_i)、公共客户 (b,d)，主题为
(A_i=X_icup{a_i})、(B_i=X_icup{b})、(C_i=X_i)、(D={b,d})。存在完整纯 SPE 走 (C_1,ldots,C_k,D)，实际福利 (W=2k+2)，而 (k+1) 个主题的最优覆盖为 (OPT=3k+2)，比率 ((3k+2)/(2k+2)	o3/2)。Q/B 状态递归允许多个旧 (A)，并用 B 状态处理 fresh (B) 偏离；这是存在一个完整纯 SPE 的构造，不是所有 SPE 都走该路径，也不是六人 half 反例。

当前相关独立程序只覆盖 (k=1,2,3)，逐有序历史做精确 `Fraction` 比较，输出 (k=1,2,3) 的历史/比较数分别为 (5/20,57/399,1111/11110)，路径分别为 `(2,3)`, `(2,5,6)`, `(2,5,8,9)`，福利/OPT 分别为 (4/5,6/8,8/11)。我实际运行该关联实现，退出码 0，输出 JSON 与其冻结关联报告逐字节一致；这验证了有限替代实现的结果，没有把它写成缺失原脚本的字节级重放。缺失的冻结 family 程序与 1344 B JSON 仍需可访问 blob 才能完成原源全文核验。

## 2. `audit_collision_free_obstruction.py` 与 `collision_free_obstruction_audit.json`

冻结 JSON 全文记录四主题
(S_0={x_0,x_1,a})、(S_1={x_0,x_1,b})、(S_2={x_0,x_1})、(S_3={b,d})，五名单位客户，根动作 (S_2)，末位回复为 `(1,0,3,0)`。四个根分支收益都是 2，实际路径 `(2,3)` 的两个主题不相交，(W=4)，而 (OPT_2=5)。20 个含自身比较中 15 个为非自身比较、9 个严格，最小 slack 为 0，负载直方图为一名未覆盖、四名负载一，(Phi=4)，二层占用量也是 4。

`clean show` 可直接全文读 JSON；我另运行已有独立 Fraction 审计并执行不同实现的 `independent_verify.py`，两者均退出码 0、结果 JSON 与冻结文件逐字节一致，核验所有五个决策历史及 20 项比较。该证据足以否定“所有完整纯 SPE 的实际占用函数（只要 (f(0)=0,f(1)=1)）都支配 (OPT)”这一加强桥，也否定普通/截断调和势和二层占用支配桥；但 (2W=8>5)，所以它不是一般 half 反例。冻结的 `audit_collision_free_obstruction.py` 源程序本身缺失，不能声称原程序全文已读；独立重放仅核验同一数学数据。

## 3. `audit_truncated_potential.py`

关联 global_proof README 说明该程序审计的是 78 客户发现点，目标为随机真实 Markov 策略下的调和/截断势桥失败候选。关联 `harmonic_potential_obstruction.md` 进一步说明随后通过整数压缩得到 11 客户精确点：三名提供者、六主题、实际路径 `(1,5,5)`，(W=8)、(OPT_3=11)，实际负载为三个一和五个二，因此普通与截断调和势均为 (21/2<11)。其审计量词是给定客户输入、给定完整策略、全部 43 个有序决策历史的 Fraction 比较；关联稿报告 258 项含自身比较、188 项严格。这是一个精确障碍，仍满足 (2W>OPT)，不构成 half 反例。

原 `audit_truncated_potential.py` 的 2472 B blob 无法从当前 partial clone 读到，78 客户 JSON 也未在本批物化。因此 11 客户关联点和相关审计不能被表述成对该缺失源的原字节重放；该源的正确处置是保留为有限势障碍工具，保留缺失 blob 边界，待可访问冻结对象后再完成源级核验。

## 4. `background_regret_probe.py`

这是本批唯一完整可读的程序源之一。源码使用非空掩码类型、随机前缀、固定 Markov 完整策略和 `scipy.optimize.linprog`，在固定策略的所有单步激励差上施加线性约束，然后比较一个终局的“利润 + fresh 新覆盖”与候选比较主题的 fresh 覆盖。它明确是浮点 LP 发现器，发现点必须另做精确审计，且不搜索任意历史依赖的所有纯 SPE。

按关联 README 的原默认范围，(q=6,r=3)、seed=29393、100 棵随机策略树，每棵至多 12 个比较主题没有找到负点。为避免写入源码默认的候选输出，我在独立副本执行同一入口 `--q 6 --r 3 --trials 100 --seed 29393`，退出码 0、stderr 为空、stdout 逐字保存于 `replay/background_regret/`，最后为 `completed 100 q 6 r 3 best 0.0`。另执行 20 棵同参数 smoke run，结果同样为 0。该“无负点”只属于有限浮点筛查，不能推出背景整体候选普遍成立；其合法过去可达性也需另证。

## 5. `collision_free_ratio_probe.py` 与 `collision_free_ratio_best.json`

关联 global_proof README 记录该程序对 (q=6,m=3) 的 500 棵随机完整 Markov 策略施加实际负载 (le1)，最高浮点候选约 1.116279，未改善已知的五客户 (5/4) 点。它是无拥挤路径的有限比率探针，不是全策略优化器，不能给无拥挤最坏比率上界，也不构成趋 2 反例或一般 half 结果。

本批 `ratio_probe.py` 和 `ratio_best.json` 的冻结 blob 均缺失；没有把关联 README 的约数写成“原 JSON 已复跑”，只把该有限范围作为 related comparison。待源可访问时，需要读取随机策略生成、负载筛选、目标定义、浮点容差和最佳点完整字段，再核其输出是否真对应该 README。

# 可确立的数学结论与未闭合义务

1. 五客户两人例是当前最强的定义级无拥挤占用障碍：完整纯 SPE 的实际终局可无碰撞而 (W=4<OPT_2=5)，所以仅按实际负载构造的 (f(0)=0,f(1)=1) 证书不能支付最优覆盖缺口；它仍不否定 (2Wge OPT)。
2. 碰撞自由 (k)-族给出存在型完整纯 SPE 的 (OPT/W	o3/2)，迫使任何普适纯负载支配桥满足 (f(1)ge3/2)；这只是必要条件，不是 (f(1)=3/2) 的充分证明，也不是一般 half 反例。
3. 十一客户三人调和障碍给出 (Phi=Psi=21/2<OPT_3=11)，但 (2W=16>11)；它否定调和势支配桥，不改变 half 状态。
4. 背景 Markov-LP 的 100 棵有限负搜索无反点，既不证明 (P+Deltage O_r) 的全局命题，也不反驳合法背景首步失败对象。已有 23/488 客户首步反例与后续 52 客户全局反例必须分别按其对象正文阅读，不能由本探针替代。
5. 直接把 (t=2) 碰撞自由族推广到 (t>2) 的指定无碰撞终局被末位 (A_i) 偏离以 (2t-1>t) 击穿；这只排除该参数族，不排除别的趋 2 构造。
6. 一般六人 Q-CAG-HALF 仍 OPEN。八源没有提供一般证明、一般反例、所有 SPE 量词、合法目录全空间枚举或外部同行/新颖性认证。

# 复现与工具限制

证据目录 `../../tools/evidence/R-2fc-global-proof-a-20261031/` 保存两次成功 `clean show` 的原字节、六次 bad-object 日志、库存摘要、关联文本、背景 LP 100/20 棵输出、碰撞自由 family 的关联替代重放和五客户障碍的独立 Fraction 核验。`source-summary.json` 明确标记六个缺失 blob，并保留源 ID、Git blob、冻结 SHA、大小和两个冻结提交。

当前批次未改写全局图、未提交 Git、未调用 `clean done`；缺失原文意味着本批仅“证据包已准备”，不是源级 checkpoint-ready。恢复后优先顺序是：取回六个 blob，逐源 `clean show` 全文读取；对原 family/truncated/ratio 程序逐行核输入、默认值和输出写入 replay；最后用同一回执更新六条源的 `full_file_reviewed` 与处置状态。用户消息中误写的背景 ID 只在 receipt/source-summary 中校正为冻结 inventory 的 `...20e2`，不创建伪 ID。
