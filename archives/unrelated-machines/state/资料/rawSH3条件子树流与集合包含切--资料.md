---
id: "unrelated-machines/raw-sh3-conditional-subtree-flow-inclusion-cut"
kind: "bridge"
type_tag: "资料"
title: "raw SH3 条件子树流与集合包含容量切"
status: "proved-necessary-flow-with-explicit-sound-fail-scope"
summary: "在分层 DAG、完整 home-budget-one jobs、unit-only entries、共同 degree≤6 raw functional、M3/CONFIG first-pair 与 global degree-two load localizers的明确 SH3 合同下，正入口可导出 canonical first-moment subtree flow；一族集合包含实例给出可计算必要容量切和可靠 FAIL。该桥不生成实际 forest、不保持原高阶矩、不构成 near-two gap 或一般UM算法。"
source_refs:
  - "clean:69b54480b55976701857"
  - "clean:a083b5f2d1a594ab06f8"
  - "clean:1444ad7e876999f0a6ff"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_raw_sh3_canonical_subtree_flow_addendum_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_raw_sh3_conditional_flow_and_inclusion_capacity_canonical_draft_v2.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_raw_sh3_inclusion_entry_cut_author_proof_v1.md"
---

# 对象与输入合同

三份来源共同处理 raw SH3 条件子树流和 inclusion-entry 容量切。输入是有限分层 DAG：每内部机器 v 有 k_v≥1 枚 unique-home 原 jobs，每枚 home 时间 1/k_v，其余后层端时间一；另有 unit-only entry jobs；sink 只有 unit capacity，没有 home jobs。全部原 jobs 必须完整分配，不把 k_v 数值免费展开。固定 1≤T<2，同一 functional L 作用于全部 endpoint 变量，次数至多六，满足 Boolean/one-hot ideals、global M3、每机 CONFIG(T) first/pair 和每行 global degree-two load localizers。

| clean ID | 原路径 | SHA-256 | 大小 | 实读性质 |
|---|---|---|---:|---|
| `69b54480b55976701857` | `history/source/notes/unrelated_machines/sol_raw_sh3_canonical_subtree_flow_addendum_v1.md` | `12175c728c43af4deab644bfa91281676717500d67c3e8182d43adf8e257e869` | 6,326 B | canonical first-moment flow addendum |
| `a083b5f2d1a594ab06f8` | `history/source/notes/unrelated_machines/sol_raw_sh3_conditional_flow_and_inclusion_capacity_canonical_draft_v2.md` | `011eab0db7ecc5f0b52e09b6d61b1241d46661711bbc1a76565f02f05cbef10d` | 14,977 B | 条件子树流、inclusion cut、CONFIG(1)证书和精度边界 |
| `1444ad7e876999f0a6ff` | `history/source/notes/unrelated_machines/sol_raw_sh3_inclusion_entry_cut_author_proof_v1.md` | `d418c68c558b7c3de5e47ecaacf0b20b085061b44b1f2afc3b77d1b11fa3513a` | 9,982 B | 作者证明；projection/null、局部切、二项式界与完整 jobs |

证据原件和 manifest 位于 `archives/unrelated-machines/tools/evidence/raw-sh3-inclusion-cut-20261031/`，回执草稿在 `cleanup/workspaces/Boss2/raw-sh3-inclusion-cut-receipts-20261031.json`。

# 1. M3 投影支付与正入口子树流

T<2 使同一 unit row 中任意两个不同 incoming endpoint 的 pair moment 为零。其 degree-two product 是 M3 null，乘至三次多项式仍 null，因此可把零关系推广到 degree≤4；Boolean reductions 总次数≤6。于是 unit occupancy C_v 与任意 incoming subset 的乘积是 idempotent projection；至多三个此类 projection/补 projection 的乘积 P 满足 `L(P)=L(P²)≥0`，这是 paid M3 结果，不是任意跨机器矩的非负假设。

取一个原 unit entry E，p=L(E)>0。定义 b_u=L(E C_u)、y_(u,j,w)=L(E C_u x_(u,j,w))、S_u=sum y。局部 projection 与 unit-cap 给

`0≤b_u≤p`，
`sum_w y_(u,j,w)≤b_u`（每原 job），
`sum_j y_(u,j,w)≤b_u`（每原 arc）。

load localizer q=E R 逐 job 求和给 `S_u≥r_u b_u`，其中 `r_u=k_u(2−T)>0`。DAG 上从 a_v=p 开始按拓扑序设 a_u 为构造的 incoming flux；由 arc cap 有 a_u≤b_u。若 b_u>0 取 `f=(a_u/b_u)y`，否则置零；得到每顶点活动≤p、每原 token/arc flux≤a_u、每内部行 export≥r_u a_u。除以 p 后是根活动一的 canonical first-moment subtree flow。

该 flow 是新的可行 flow，不保持 raw point 的一阶/二阶/高阶矩，也不是 actual forest；不为其它原 jobs、selectors 或上游端点免费补 joint schedule。可直接由显式原菜单建立 ordinary rational subtree LP；若某入口 LP infeasible，所有原共同点中的对应 endpoint first moment 都为零，结合 mandatory one-hot 可 sound FAIL。可迭代删除被证明零的端点，但不删除原 job/home。

若 `(T−1)k_u` 是整数，活动 home marginal 落在 h_u-subset hypersimplex，可分解为恰 h_u 枚 home 的一阶 CONFIG；一般非整数不取 ceil，也不声称完整 CONFIG 二阶匹配。k_u=1 还有额外同 row incoming/home pair zero，可使该行精确走一条 unit corridor；没有这项条件时不扩展。

# 2. 集合包含容量切实例

取 q 为正四倍数、m≥100q，N=C(m,q)、C=C(m−q,q)、K=C(2q,q)、G=C(m,2q)=NC/K。物理机器三层：每 q-set S 一个 U_S，每 2q-set W 一个 B_W，每 q-set R 一个 Z_R。U_S 有 selector 和 d1 枚 home 1/d1 的 f jobs，f 可去包含 S 的 B_W；B_W 有 d2 枚 home 1/d2 的 e jobs，e 可去 R⊂W 的 Z_R；其它端无穷。

固定 U_S 的 selector endpoint A，p=L(A)>0。原 localizer 给 `sum_(W⊃S)b_W≥δ d1 p`；B_W 的 outgoing first/pair 给 `sum_R y_W,R≥δ d2 b_W`，每 y≤b_W；terminal unit cap 给 `sum_W y_W,R≤p`。令 H_S={R:|R∩S|≥q/4}，其大小 H；每 W⊃S 有 M terminals outside H_S。故

`δ d1 (δ d2−M) ≤ H`。

若反向严格违反，所有 selector endpoints p 必为零，违反 selector one-hot，故 raw SH3 infeasible。实际 schedule 也有同一完整-job计数：选 U_S 后至少 δd1 个 f 到不同 B，每 B 至少 δd2 个 e 到不同 terminals，H_S 只有 H 个 unit slots，其余 exports 只消耗容量。无需 SDP solver。

显式 CONFIG(1) witness 可列：U selector 质量 1/N；f home 1−1/N、各 eligible B 1/(NC)；e home 1−K d1/(NC)、各 eligible Z 质量 K d1/(NCK)；各 terminal 总质量 d1d2/N≤1。所有原 jobs 覆盖一、配置 load≤1，selector unit 给 CONFIG optimum=1。实际任取 S⊂W、R⊂W 的路径 assignment，其他 jobs 全回 home，峰≤max(1,2−1/d1,2−1/d2)；这是上界，不把有限 q 下它称精确最优。

# 3. 二项式界、取整和位复杂度

有限估计给 H/C 指数下降：`H/C< (8/49)^(q/4)`；M/K≤多项式(q)·(256/729)^(q/4)；K/C≤(4/99)^q。d1=floor(C/(K s1))、d2=floor(K/s2) 的 floors 由 e1=Ks1/C、e2=s2/K 支付；固定 s1≤q^a、s2≤q^b 时，切左端仍≥δ²/(4q^(a+b))，而 H/C 指数小，最终严格 FAIL。所有二项式整数 O(m) bits，H/M O(q) 项，精确整数比较无需浮点或开方。

源码另有 finite audit（120 组精确二项式 case、85 FAIL，以及 q=2 小矩）但本轮不把脚本执行当作普适证明；m≥100q 的渐近反证由上述公式承担。

# 4. 来源关系与未完成义务

该桥使用 raw SH3 的共同 M3、CONFIG first/pair 与 global degree-two localizers；不把 Bamas assignment-LP subtree 的一般 shadow 直接当作 parent-bounded flow。它给出的 canonical subtree LP 是 necessary/sound FAIL 接口，仍不能生成实际 integer forest，也不能保证 shared integer owners 不冲突。老 shared three-block 核心在 binary target 可有 canonical first flow 而无实际 binary forest，故主 near-two gap 仍开放。

本结果不提供一般 UM 固定小于二算法、不提供 hardness source、也不证明 raw SH3 的 near-two gap。若继续推进，需解决流到 shared integer ownership 的完整 coupling，并支付 growing-depth terminal overlap。原件和 manifest 在 evidence，正文归档为资料，回执草稿单列。
