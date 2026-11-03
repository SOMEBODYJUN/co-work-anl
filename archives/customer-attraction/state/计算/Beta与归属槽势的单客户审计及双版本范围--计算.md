---
id: customer-attraction/beta-and-owner-slot-potential-single-client-audit-and-two-versions
kind: computation
type_tag: 计算
title: Beta与归属槽势的单客户审计及双版本范围
status: one-current-original-CLI-reproduced-owner-version-byte-exact; initial-Beta-version-preserved-not-rerun
summary: 7117B当前原码默认m8一次复现865B owner报告；615B初版另保。静态枚举全部owner而前缀仅first-owner，计数是放松单客户incidence/形式边际，不测试全局最优cap、SPE或跨叶支付。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round3/parent/audit_beta_slot_potential.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round3/parent/beta_slot_potential_audit.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round3/parent/owner_slot_potential_audit.json
---

# Beta与归属槽势的单客户审计及双版本范围

## 函数、Beta参数与有限域

7117B原码只用标准库，无模型、求解器、作者程序或外部输入。`beta(a,c)`表示
\[
 \beta(a,c)=\int_0^1p^{a-1}(1-p)^c\,dp=(a-1)!c!/(a+c)!,
\]
第二参数是幂c，不是通常Beta函数的第二形参（等于数学Beta(a,c+1)）。对m个槽，A是该客户比较覆盖槽集，C是profile覆盖槽集，定义
\[
 \phi(A,C)=\begin{cases}H_{|C|},&A=\varnothing,\\0,&A\cap C\ne\varnothing,\\-\beta(|A|,|C|),&\text{其余}.\end{cases}
\]
A空表示O外客户的局部incidence，不是零客户游戏。C可空，原代码不在空C上取1/|C|。

CLI允许`--max-m`在1…12、默认8；本次只按原默认运行一次，实际m1…8。每m全部A,C子集、每i∈C核形式删i边际；每个C的两个未覆盖槽无序对核局部次模方形；每个A非空逐查询索引枚举未来覆盖子集。它不是全部目录、最优组合或SPE枚举，单客户模式之间未强制组成同一个合法最优实例。

## 当前实际检查的代数

令c=|C|≥1，边际$\phi(A,C)-\phi(A,C\setminus\{i\})$与1/c比较。A空恰1/c；若其它slot同槽保护则0；否则i∈A时为β(a,c−1)，i不在A时为β(a+1,c−1)。这些被积式均介于0与$(1-p)^{c-1}$，故单位边际0≤ell≤1/c。每客户总误差在$[0,\mathbf1_{A\ne\varnothing,C\ne\varnothing}]$，O外误差0。局部方形还核gain_small≥gain_large≥0。

静态owner部分对**每个o∈A**分别检查$\phi(\{o\},C)\le\phi(A,C)$：若A与C不交，β(a,c)≤β(1,c)=1/(c+1)；若相交，右端0、左端≤0。这里minorant是未归零的φ，不是加不同常数后的owner F≤Beta F；例如A={0,1},C={0},o0，φ两者0，但归零owner基线1大于Beta基线1/2。

owner边际核o本人1/c、非owner且o在C为0、o不在C为1/[c(c+1)]。每owner再核
\[
 \sum_{i\in C}(1/c-\ell_i)=\mathbf1_{C\ne\varnothing}-\kappa,
 \quad\kappa=\begin{cases}1/c,&o\in C,\\1/(c+1),&o\notin C,C\ne\varnothing,\\0,&C=\varnothing.\end{cases}
\]
这是真实单叶I−κ的逐客户形式，C空κ0，不能在实际κ中为未覆盖客户另加库存1。

## 前缀查询只核first-owner

A非空，i按A升序遍历，固定当前及所有先前A槽，C=这些anchor加任意更晚槽子集。各query的suffix独立选最坏，再累加；没有构造一个共同rollout或游戏策略。首次Beta信用≤1−1/a（a1为0），第s≥2次≤1/s，合≤H_(a−1)。

**owner前缀只取o=min(A)**：首次误差0，后s次≤1/s，合≤H_a−1。静态遍历所有o，不代表前缀也遍历任意o；后来[任意/分数owner前缀预算](../引理/固定最优前缀链的归属端点抵消--引理.md)的更宽解析证明不能回填成此代码功能。这里也没有actual-prefix DIRECT查询、TREE-F/ROLL或全树IC。

## 两冻结版本与真正计数

| 字段 | 615B初版 | 865B当前owner版 / 本次输出 |
|---|---:|---:|
| max_m_regression_only | 8 | 8 |
| profile_client_types | 87380 | 87380 |
| present_slot_marginals | 334962 | 334962 |
| diminishing_return_checks | 563124 | 563124 |
| prefix_query_states | 43435 | 43435 |
| prefix_credit_budgets | 502 | 502 |
| owner_minorant_checks | 无 | 334962 |
| owner_error_identities | 无 | 334962 |
| owner_prefix_states | 无 | 43435 |
| owner_prefix_credit_budgets | 无 | 502 |
| maximum_total_client_error | 1 | 1 |
| claims_checked | 六条 | 原六条+owner minorant/error、first-owner前缀两条 |

精确循环公式为
\[
 \sum_{m=1}^84^m=87380,\quad
 \sum_{m=1}^8m2^{2m-1}=334962,\quad
 \sum_{m=1}^8\binom m2 2^{2m-2}=563124,
\]
\[
 \sum_{m=1}^82^{m-1}(2^m-1)=43435,\qquad
 \sum_{m=1}^8(2^m-1)=502.
\]
owner静态计数也为$\sum_A|A|2^m=\sum m2^{2m-1}$，但每个error identity内还有coverer循环；字段不是原码每个assert总数，更不是这么多游戏/SPE或实际客户。前缀预算502为非空A族，43435为允许各次suffix独立变化的query状态。

原报告status PASS、scope明示`no SPE or half proof`。615B初版10字段、865B当前14字段；去掉当前四owner计数并去claims最后两条后，其余语义与初版相同。这是版本比较，**没有执行初版当时源码**。当前7117B已经含owner逻辑，只新生成865B，不能假称一次原run同时原样生成615B旧版。完整[版本与scope记录](../../tools/evidence/cag-slot-potential-programs-primary/version-and-scope.json)保此区别。

## 一次真实CLI与字节结果

[三primary原件](../../tools/evidence/cag-slot-potential-programs-primary/source-manifest.json)均按冻结SHA保raw；repo/cache预查无同名源码或同SHA成功记录。本次新空replay-potential/source-root镜像原repo相对路径，以Python3.12.14、optimize0真实CLI执行一次当前源码，不传max-m（默认8），仅传新`--output`路径。源码有main guard，输出用`open('x')`拒覆盖，且**不创建output父目录**，父目录由外层新replay预备。没有为取函数再import，未改源码/assert或旧报告。

实际约9.94秒、exit0、stderr空；新报告与stdout均865B，逐字节等owner冻结报告，SHA `589cd541bc68bec9be562d4154cb71652509f44b76c070c9c7fb85fc92856865`。初版615B SHA `1f93c21aeb61d32e6e4b25d1e578ea88ef118e1f0ea35e4f7cbe7b39509fecdf`另保未改。[执行状态](../../tools/evidence/cag-slot-potential-programs-primary/replay-potential/execution-state.json)保真实argv/cwd/解释器/原SHA及一次次数；镜像根不同于冻结物理路径。无外部file input/local程序/第三方库依赖，全部有限输入见[域描述](../../tools/evidence/cag-slot-potential-programs-primary/potential-input-domain.json)。

## 可以证明与不能证明的范围

原程序复核m≤8的单客户函数、形式边际、局部次模、同叶误差与独立suffix前缀折扣；不检全局最优性Φ≤0/F_Q≤OPT、不检共同目录实现、完整SPE、跨叶债或NET付款。数学普遍性由[Beta势定理](../定理/固定最优槽的Beta势与前缀重复信用--定理.md)和[owner单位势](../定理/最优归属势的单位分解与同叶联合预算--定理.md)的合法替槽证明承担，不能用PASS代替。

它与6992B/2717B前批[双程序回归](最优交换与归属插入的双程序精确回归--计算.md)是不同入口、不同计数/依赖，未重复那两程序或挪用它们的18指定IC。已反驳的一般逐人floor/WP与这里仍真的代数部件分别保留；当前五人half他证成立，六人half与一般共同incoming未由本运行闭合。
