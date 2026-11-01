# 本轮精确命题与状态

2026-10-24，个人研究账本；不是共享 canonical 状态升级。
全部玩家与客户均为单位，目录共同且有限非空；纯 SPE 均量化全部有序历史。

## Q-CAG-HALF（原身份不变，OPEN）

对每个有限 N、S⊆2^N、m>=1及每份完整历史纯 SPE sigma，实际终局 B
满足 2W(B)>=OPT_m。允许空主题、重复、零客户及任意历史平局。
本轮没有一般证明或合法目标反例。依赖与完整已知范围仍由共享账本管理。

## TERMINAL-AMOUNT-CAP2-v0（本轮自足证明、独立内审）

**对象及量词。** 任意上述有限客户/目录与 m>=1，任意合法完整叶 B，
任意有限族末位替换叶 W^alpha=(B_<m,T_alpha)。它不要求 B 来自 SPE。
记 p_j(F)=sum_(x∈F_j)1/c_F(x)。对每个 alpha,j<m 任意 lambda>=0，
只假设每个 j 的共同预算 sum_alpha lambda_(alpha,j)p_j(W^alpha)<=p_j(B)。

**结论。** 对标准前缀正价

    q_(alpha,j,m)=sum_(x∈B_j∩(B_m\T_alpha))1/[c_B(x)c_alpha(x)]，

有 sum_(alpha,j<m)lambda q<=2sum_(x∈B_m,c_B(x)>=2)1/c_B(x)<=2p_m(B)。
求和客户保证分母为正；零利润 sender 的全部 q=0，m1为空和。

**依赖/证据。** [自足证明](parent/terminal_amount_cap.md)，仅同客户计数与
AMOUNT，无定理导入；[credible 独立重构](credible/review_terminal_amount_cap.md)、
[independent 先重构后对稿](independent/prefix_and_terminal_amount_review.md)，
父方复核。外审与新颖性未认证。不能删除“仅替换末位”条件。

## AMOUNT-CAP1-v0（FALSE；TERMINAL系数二的锐性）

**被否定身份。** 沿用上一条对象和 AMOUNT，声称所有多孩子合并正价
至多 p_m(B)。更深版本同样包含此特例，因而亦不能统一要求 cap1。

**反例量词。** 对每个整数 n>=3，m=n+1，2n 个互不交块满足
|X_j|=2，|Y_j|=2(n−1)。共同目录 Aj=Xj∪Yj、Tj=Yj、D=∪Xj。
存在全有序历史纯 SPE 实际 A1,...,An,D。实际利润为 2n−1,...,2n−1,n。
对末位强制 Tj 的孩子，仅给 sender j 系数 (2n−1)/(n+1)，每个 AMOUNT
预算恰满，而末位总正价为 n(2n−1)/(n+1)>n。

**Scope及后果。** 列比率 2−3/(n+1) 趋二，故上一条统一系数不能减小。
该族 W=OPT_m=2n²；没有否定 half。只主张给定金额正价合同的锐性，
不主张原福利常数的新下界。

**证据/检查。** [全 n 完整策略证明](coupling/amount_cap1_family.md)，
[独立全 n 攻击](credible/review_amount_cap1_family.md)，父另重构全部
override 类型与根 D 的真实末位比较；另有
[independent 先盲重构后对稿](independent/amount_cap1_family_review.md)。
coupling 程序及父重放 n3 的完整
有序历史审计见同目录；有限审计只验证实现，不承担全 n 证明。
无外审或新颖性认证。

## DEEP-AMOUNT-CAP2-v0（OPEN，尚不是已付half充分桥）

**对象。** 任意完整 SPE 实际叶 B。分支 alpha=(i_alpha,T_alpha) 固定
B 的真实 i_alpha 以前前缀、强制 T_alpha，然后沿同一 sigma 完成 W^alpha。
允许同一切点多个不同主题。对 j<i_alpha 的非负 lambda，要求
sum_(alpha:j<i_alpha)lambda_(alpha,j)p_j(W^alpha)<=p_j(B)。

**候选。** 对每个 l，是否必有

    sum_(alpha:i_alpha<=l)sum_(j<i_alpha)lambda_(alpha,j)
      sum_(x∈B_j∩(B_l\W_l^alpha))1/[c_B(x)c_alpha(x)]<=2p_l(B)？

**证据/obligation。** 末层已证；更深未证、无真实 SPE 反例。选定旧证书
的精确阴性不是一般证据。即使本候选成立，仍须将实际遗漏债务合法化入
其 AMOUNT，并扣除已有 direct/suffix 支出，不能直接宣布 half。
正文及定义级检查器见 [parent](parent/terminal_amount_cap.md)。

## TOTAL-SOURCE-POOL（既有正价分解的基线推论，不认领新机制）

对上一条任意深度的 prefix 相同合法叶，不用 SPE，正价在所有 recipient
上的总和加显式非负保留量，恰为该 sender 的 p_j(W^alpha)。因此若 AMOUNT
已成立，则所有正价金额共同受原 sender 实际利润和控制。它不证明逐列
cap2，不生成 AMOUNT，也不购买含未来强制动作的假 IC。
见 [harmonic 稿](harmonic/positive_source_pool.md)及
[direct 重构](direct/positive_source_pool_review.md)。

## 其余一般候选（均未证明）

- `PREFIX-DIRECT-COVERAGE-FLOOR-v0`：沿用 R-29 原身份，固定原 m 及
  OPT_m，任意合法前缀后的当前利润>=OPT_m/(2m)。本轮只核 min-r>=3
  和同枝外部利润必要式，不作真值提升。见父工作稿及 independent 审查。
- `RESERVE-FLOOR`：任意合法背景 b、r 人子 SPE，背景和实际全部尾部
  都避开 V，且 V 可由 r 个主题覆盖，是否首位利润>=|V|−OPT_(r−1)(V)。
  等价的是任意背景、任意最终遗漏子集的逐期 gap 版本；它强于只量化
  原根实际路径的版本。均未证。见 [direct](direct/residual_gap_working.md)。
- `LAST`：实际末位之前 b 的完整额外一槽菜单值是否<=W/m。仍未接入
  早期真实激励；固定 b 的 Gram 核不能跨重置分支免费共用。见
  [menu](menu/last_menu_working.md)。

父方 [一般工作稿](GENERAL_PROOF_WORKING.md)把这些不同候选与原目标区分。
新增末层工具没有增加一般 half 的已证范围；主线未付义务仍是全树共同覆盖支付。
