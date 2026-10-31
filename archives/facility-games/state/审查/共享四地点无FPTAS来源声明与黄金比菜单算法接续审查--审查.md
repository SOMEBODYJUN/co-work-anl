---
id: "facility-games/shared-four-site-fptas-and-menu-source-review-20261031"
kind: "review"
type_tag: "审查"
title: "共享四地点无FPTAS来源声明与黄金比菜单算法接续审查"
status: "complete-source-read-cross-object-comparison-no-new-runtime"
truth_status: "four-site-gap-integrated-from-existing-proof; menu-proof-transfer-integrated-with-finite-runtime-boundaries"
review_level: "clean-show-full-read-source-hash-cross-commit-and-scope-audit"
scope: "两份 history/source/notes/shared 来源：用户完整证明来源摘录 four_site_no_fptas_user_statement_2026-10-09.md 与共同目录黄金比有限菜单 menu_algorithm.md"
summary: "四地点来源是用户完整证明的身份与结论摘录，明确缺少原审计包和本轮复现；它与仓库已有 SC-FOUR-NO-FPTAS 定理/证明逐项一致，保留 13/10 对 PARTITION 的逆多项式 gap 及所有量词边界。菜单来源是固定 P/H/T/C witness menu 的 polynomial proof transfer，补足 global proof 中每个 equilibrium/minimum 调用的替代见证、复杂度与输出合同；与既有黄金比算法和菜单量词审计合并，不把 753 有限运行记录或内部证明写成外部认证。"
source_refs:
  - "source:3db6a0e2bfe4e2f13cb3:history/source/notes/shared/four_site_no_fptas_user_statement_2026-10-09.md"
  - "source:71ccfb6f9c76b9bb5968:history/source/notes/shared/menu_algorithm.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/shared/four_site_no_fptas.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/shared/four_site_no_fptas.md"
related_objects:
  - "../定理/四共同地点实例最优倍率的无FPTAS间隙--定理.md"
  - "../证明/四地点无FPTAS间隙的全支持与编码核算--证明.md"
  - "../计算/小目录硬度构造器与五地点样本的精确合同--计算.md"
  - "../subarchives/common-two/state/算法/黄金比有限菜单与完整续局证书--算法.md"
  - "../subarchives/common-two/state/审查/菜单量词与强弦实现审计--审查.md"
  - "../subarchives/common-two/state/定理/共同目录黄金比存在与有理构造--定理.md"
  - "../subarchives/common-two/state/定义/共同目录精确续局与菜单模型--定义.md"
evidence_paths:
  - "archives/facility-games/tools/evidence/shared-source-notes-20261031/four_site_no_fptas_user_statement_2026-10-09.md"
  - "archives/facility-games/tools/evidence/shared-source-notes-20261031/menu_algorithm.md"
  - "archives/facility-games/tools/evidence/shared-source-notes-20261031/source-manifest.json"
---

# 1. 来源身份与全量阅读

本批两个来源先用 `clean claim` 正式认领，再用 `clean show --out` 导出原字节并从头到尾读取。inventory 元数据与原件如下：

| ID | 冻结路径 | blob | 字节 | SHA-256 | 两个 source commit |
|---|---|---|---:|---|---|
| `3db6a0e2bfe4e2f13cb3` | `history/source/notes/shared/four_site_no_fptas_user_statement_2026-10-09.md` | `54622ec54365a564d23ba836ba91088621d7418f` | 1,875 | `5763dcb744150fe3e38a913125aaa7a32c43dfec5e906f227431a64df4063316` | `68fad804...`、`aefc58ea...` |
| `71ccfb6f9c76b9bb5968` | `history/source/notes/shared/menu_algorithm.md` | `52d18bba8075294f15585459733715ba82ffc051` | 14,872 | `3af0dca2346bc166b6f41cd86d42e44fa2286fba5bb098979b6efa349993dbc6` | `68fad804...`、`aefc58ea...` |

直接从两冻结提交取 blob 后，两份来源各自逐字相同；它们是同一历史版本的 legacy/main 双路线，不计为四份独立材料。证据目录 `shared-source-notes-20261031/` 保存原文副本和 `source-manifest.json`，并记录相关现行正文与运行边界。

两源属于两设施共享目录模型：客户有正有理原子权，客户在设施之间独立混合并最小化包含自身权重的实际负载期望，设施最大化服务权；完整规则对每个带标签设施布局指定精确客户 NE。该模型与 CAG 六名顺序提供者、主题覆盖者间均分价值模型无共同定义域，本批不跨模型迁移结论。

# 2. 四地点来源：它记录证明身份，不能冒充未取得的审计包

## 2.1 来源的准确身份

`four_site_no_fptas_user_statement_2026-10-09.md` 只有 26 行。开头明确说明它是“2026-10-09 用户在当前会话粘贴的完整九节证明”的来源与精确命题摘录，不是逐字附件备份；原链接审计包和单独证明文件未取得。它自报 65 个实例、17 YES、48 NO、41,481 支持记录、520,240 成本比较，但没有附运行输出或脚本。因此这些计数不能被本批标为已复现结果。

该来源的独有内容是命题身份与来源边界：原稿研究基线为 `97d2805cdd6c4de4ce6eca25770a19a6783419ab`，原稿声称在 P≠NP 下，四共同地点、两家带标签设施、正二进制整数原子权、强制服务、精确独立混合客户完整续局的实例最优稳定倍率不存在题设加性 FPTAS；同一 gap 也排除标准乘性 FPTAS。这里“来源摘录”是证据等级，不是对其内部数字的二次核验。

## 2.2 归约结论和全称量词

摘录中的归约从正整数 PARTITION 列表 (b_1,ldots,b_t) 出发，令

\[
n=2\max\{t,2\}.
\]

恰四地点的实例满足：

\[
\text{YES}:\quad \alpha^*=13/10,
\qquad
\text{NO}:\quad \alpha^*\ge13/10+\frac1{100n^2}.
\]

NO 的量词覆盖所有纯设施布局、所有在轨精确独立混合客户 NE、所有完整精确续局；算法输出的完整合同要求显式二进制有理概率。来源特别指出“不排除 PTAS、不证明强 NP 难、不处理近似客户 NE 或相关策略”。随机算法的复杂度假设也不能由这段摘要自动改写为 P≠NP 下的排除，除非另行处理 NP/BPP 关系。

## 2.3 证明机制的准确内容

来源摘录给出近单位变量权编码

\[
w_i=1+\frac{na_i-T}{16n^2T},
\]

其中补零列表 (a) 使 (n) 偶且 (T=sum b_i)。参数为

\[
M=5n/2,\quad \tau=1/(2n),\quad q=13/(20n),\quad
V=11n/2,
\]

\[
R=(143n^2+13)/(40n),\qquad d=27n/10.
\]

客户角色是：覆盖全部四地点的大客户；覆盖 (B,C) 的变量客户；覆盖 (A,B) 的交叉客户；(B,C,A,D) 私有客户。客户类型、参数关系和支持恒等式

\[
(1-m)\Delta=a-b+z
\]

构成归约核心：恰一名真正混合者等价于精确等分；NO 情况中其余支持与目标 (	au) 保持至少 (3/(8n)) 的差距。其他带标签布局由唯一 NE 或同址守卫排除，核心 (BC/CB) 的两个替代偏离把差值空隙转换成 (1/(100n^2)) 的稳定倍率 gap。

现行 `archives/facility-games/state/定理/四共同地点实例最优倍率的无FPTAS间隙--定理.md` 与 `四地点无FPTAS间隙的全支持与编码核算--证明.md` 已将上述机制展开为自足正文：补零、正权、全部 16 个带标签布局、任意实概率支持、整数化位长和加性/乘性 FPTAS 区分均有逐式推导。两份正文的来源是 `research/current/shared/four_site_no_fptas.md`，不是把本批 26 行用户摘录误当成完整证明附件；本批将摘录保留为命题来源和量词证据，并把可验证数学内容接到现行正文。

## 2.4 与五地点资产和有限审计的边界

既有 `小目录硬度构造器与五地点样本的精确合同--计算.md` 处理另一种五共同地点、固定 (ain(1,\phi)) 的弱 NP 困难构造与小样本重放；本四地点来源的逆多项式 gap、PARTITION 编码和全局 16 布局守卫不同。五地点有限实例表中的 `source_yes`、`full_diagonal_enumeration`、有限支持计数不能作为本四地点来源的审计替代。

本批没有取得四地点原始脚本、65 实例审计包或外部文献证明，也没有重跑 65 实例计数。正确处置是“来源声明 + 现行正文接续”，不是“本批独立复现 FPTAS 不存在”。

# 3. 共同目录黄金比菜单算法来源：固定 P/H/T/C witness transfer

## 3.1 算法命题与客户 NE 语义

`menu_algorithm.md` 的标题是“固定 polynomial witness menu for the shared-catalog golden-ratio theorem”。它声称：对于有限显式客户、正二进制有理权、有限非空共同目录、客户独立最小化实际负载期望、设施最大化客户权，可以在输入位长多项式时间内构造一个精确客户 NE 的纯设施位置 (phi)-SPE，其中

\[
\phi=(1+\sqrt5)/2.
\]

保守算术复杂度为 (O(|S|^2(n+1)^4))，输出包含有理在轨概率、至多 (2|S|-2) 个单方偏离续局，以及其余标记位置的多项式默认纯 NE 程序。它只构造一个满足 (phi) 上界的续局，不优化所有完整 SPE，也不计算每对位置所有客户 NE 的精确最小负载。客户 NE 必须对原始权重精确成立，不使用权重舍入或近似客户均衡。

源稿明确写出底层全局证明仍是内部审计的 research draft，尚无外部同行评审；因此本批沿用“内部数学证明/有限执行证据”的真值等级。

## 3.2 四类有限菜单

对物理位置对 ((s,t))，设私有负载 (A,B)，共同客户权 (w_1,ldots,w_k)，共同总重 (W)，reach 为 (R_s=A+W,R_t=B+W)。源稿要求固定、非自适应菜单：

### P：全放一侧与 singleton 种子

枚举所有共同客户放在一侧的两个种子，以及每个指定共同客户单独放一侧的种子。若种子已是纯 NE 就保留；否则只有当初始低侧每个共同客户权至少达到初始负载间隙时，才运行最大严格改善客户的受保护修复，并在第一次负载顺序反转或无改善时停止。该 guard 保证输出纯 NE 且保留低侧负载下界；每个客户最多移动一次。全放一侧种子保证 P 非空。

### H：等 reach 对半

当 (A=B) 时，每个共同客户独立以 (1/2) 选择两侧；两侧期望负载相等，客户全部无差异。该菜单在同址位置提供平衡见证。现有算法正文将该家族记为 E；本源记为 H，属于命名差异，不是不同算法。

### T：指定两名混合者

对每个共同客户对 (h,j)，把其他共同客户放在高 reach 端，令低/高私有负载为 (a\le b)，并置

\[
D=b-a+Z,
\]

其中 (Z) 是其余共同客户总重。若 (D\le\min(w_h,w_j))，让两指定客户在低侧的概率分别为

\[
(1+D/w_h)/2,\qquad (1+D/w_j)/2.
\]

这使两指定客户无差异，其余客户选择低期望成本侧；等 reach 时保留两种方向。菜单大小至多 (2\binom{k}{2}) 个此类输出。

### C：reach-based strong chord

当 reach 满足 (r>\phi R/2)、(W<r/\phi)、最大共同权不超过 ((1-1/\phi)R) 时，调用多项式 `astra_local.construct.construct`，得到两侧负载分别至少 (r/\phi) 和 (R/\phi) 的精确 NE。C 的输入只依赖两侧 reach 与共同权列表，不依赖威胁值 (d)、响应环或之后的 quota；等 reach 反射也保留。

P/H/T/C 均先在固定菜单中生成并逐项验证客户 NE，再计算菜单最小值；源稿禁止在看到坏环后临时换取另一个 NE，因为这会改变菜单最小值和边界量词。

## 3.3 菜单最小值与正确边量词

对固定菜单定义

\[
u(s,t)=\min_{e\in F(s,t)}L_s(e),
\qquad d(t)=\max_{s\in S}u(s,t).
\]

若某菜单成员在 ((s,t)) 的两侧负载满足 (x\ge d(t)/\phi)、(y\ge d(s)/\phi)，则选取每次单方偏离后的菜单最小惩罚，便得到 (phi)-SPE；两类设施偏离的标记布局不冲突，其余布局使用默认纯 NE。该判据是对**全体真实客户 NE**的充分条件，不声称必要性。

若不存在满足条件的菜单成员，则在选定响应环 (s\to t=b(s)) 上，必须对菜单中的每一成员使用

\[
P\ge d(s),qquad Q<d(t)/\phi,
\]

而不是声称对所有未列出的真实客户 NE 都有该界。随后全局证明中的每一步都必须由 P、H、T 或 C 中的具体 witness 支撑。源稿逐表审计 Sections 2--13：删除未在后续使用的 leveling/extremal selection；P 覆盖 pure repair、heavy singleton、return rule、two-anchor；T 覆盖 same-large-pair 两混合；C 覆盖 arbitrary-mixer strong chord、no-h chord 和 cycle closure。

## 3.4 两处“全体真实 NE 唯一性”如何保留

源稿特别处理两处不能只靠菜单最小值的调用：

1. 若某边 (u(t,s)>R_s)，P 的全体种子和修复迫使 responder exclusive mass (E>R_s)。随后每个共同客户严格偏好 (s)，客户 NE 唯一，故菜单最小值确实等于该唯一 NE 的 responder load。这恢复 global proof 的 return rule。
2. common-h transport 中，纯 P 与反向 singleton P 先推出 (sigma<R_s-R_t)，再由严格成本差推出指定 (h) 在所有真实 NE 中必去 responder，其余共同客户必留 incumbent。于是实际客户 NE 唯一，菜单最小值与真实收益一致，two-anchor 代数可合法使用。

因此源稿没有把“有限菜单最小值”偷换成“真实客户 NE 最小值”；只有在这两处严格支配成立时才恢复全体 NE 唯一性。

## 3.5 复杂度、精确性与输出合同

源稿给出：P 每个 seed 的受保护修复至多 (O((k+1)^2))，T 有 (O(k^2)) 候选并逐个 (O(k)) 验证，H 线性，C 为 (O((k+1)^4))；全目录菜单生成和威胁计算为 (O(|S|^2(n+1)^4)) 有理运算，概率与中间整数的位长保持多项式。黄金比比较使用

\[
z^2+z-1\le0
\]

的精确有理测试，不用浮点 (phi) 或 NE 容差。输出保存有理在轨概率、至多 (2|S|-2) 偏离续局和其余布局的默认纯修复；验证器必须从输入重新读取覆盖关系、客户顺序、条件成本和每个标记偏离，不能信任证书中预填的菜单威胁或收益。

源稿声称历史运行验证了 753 个完整 exact certificates（750 个有理随机、3 个定向全局实例），最大观测菜单因子为 (2013/1508)，并含三混合强弦样例；这些计数与仓库已有 `共享目录原始输入与四种子入口的接续复核--计算.md` 中的冻结运行记录相符。它们是有限运行证据，不是外部同行评审，也不能替代 P/H/T/C 全局证明。当前 checkout 没有 canonical `facility_spe` 生产模块和完整 tests 入口，因此本批没有重新运行该 suite，也不把源稿计数冒称新执行。

## 3.6 与既有算法、审查和定理的对应

现行 `黄金比有限菜单与完整续局证书--算法.md` 已将 P/E/T/C 菜单、搜索伪代码、证书验证最小语义、位长和精确比较整理成正式算法对象；`菜单量词与强弦实现审计--审查.md` 则逐节列出 global proof 的每一个 equilibrium/minimum 调用，明确删除未使用的 leveling section，并证明 return rule 与 common-h uniqueness 的严格支配接口。源稿的独有内容是把这些替代见证按 global proof Sections 2--13 逐项映射，给出完整 proof-transfer 叙述、输出大小 `2|S|-2` 和“本地 NP-hardness 不受影响”的复杂度解释；因此处置为现有算法/审查对象的增量，而非再建一个黄金比定理。

菜单来源所说的 local NP-hardness 不受影响：构造使用的是可实现的上界 (u(s,t)\ge m(s,t)) 和有限 witness correspondence，不要求精确求出所有客户 NE 的最小负载，也不解决任意 quota feasibility。该边界与现有局部 NP-hardness/完整菜单审查一致；它不能外推到异构设施目录、CAG 或任意客户成本。

# 4. 证据、处置与第三阶段接续

| 来源 | 实读内容 | 独有内容 | 归档去向 | 处置 |
|---|---|---|---|---|
| `3db6a0e2bfe4e2f13cb3` | 26 行来源声明、PARTITION gap、客户角色、支持恒等式、审计/复现边界 | 用户证明的命题身份和“65 实例等未取得”限制 | 本审查、`shared-source-notes-20261031/four_site_no_fptas_user_statement_2026-10-09.md`、现行四地点定理/证明 | integrated-as-source-statement |
| `71ccfb6f9c76b9bb5968` | 273 行完整菜单算法/证明转移、P/H/T/C、边量词、唯一性、复杂度、753 运行声明 | 逐 Sections 2--13 的 witness 映射、(2|S|-2) 输出合同、local NP-hardness 边界 | 本审查、`shared-source-notes-20261031/menu_algorithm.md`、现行黄金比算法/菜单量词审计 | integrated-as-algorithm-proof-transfer |

第三阶段可建立以下关系边：四地点来源摘录 → `SC-FOUR-NO-FPTAS` 现行定理（source-statement / proof-identity）；菜单算法来源 → 黄金比有限菜单算法（proof-transfer / quantifier-audit）；菜单算法 → 局部强弦定理（constructor dependency）；四地点 gap ↔ 菜单 local NP-hardness（complexity-boundary comparison）。这些边都必须保留模型、设施数、目录大小、客户 NE 语义和内部审查状态，不得把两设施四地点 gap 与 CAG 六名顺序提供者 half 目标相连为数学蕴含。

本批真实运行边界：四地点来源没有附审计包或可执行原稿，本批没有声称重跑其 65 个实例；菜单来源的 canonical implementation 不在当前 checkout，本批没有重新运行 753 suite。两源均已完成全文阅读、SHA/双提交比较、全仓相关对象对读和独有内容去向登记；父 Boss 可在确认 checkpoint/pushed 后逐源 done。
