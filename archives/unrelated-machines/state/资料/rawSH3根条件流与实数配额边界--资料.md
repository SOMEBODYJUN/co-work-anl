---
id: "unrelated-machines/raw-sh3-root-conditioned-flow-real-quota"
kind: "bridge"
type_tag: "资料"
title: "raw SH3 根条件流与实数配额边界"
status: "proved-conditional-flow-with-real-quota-and-k1-boundary"
summary: "在 raw SH3 的共同 degree≤6 functional、M3、CONFIG first/pair 与 global degree-two load localizers下，任意正 unit-entry endpoint 可构造 root-conditioned canonical first flow，真实配额 r=k(2−T) 不得向上取整；k=1 在额外同row incoming/home pair zeros下可实现无衰减单位走廊。该桥不提供实际 integer forest、SDP finder或近二主定理。"
source_refs:
  - "clean:a7bebf2d06d729998e93"
  - "clean:7f98df8bd98a2d7034a4"
  - "clean:dd2cdd7f839a901fbbfa"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_raw_sh3_inclusion_entry_cut_exact_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_raw_sh3_root_conditioned_layer_flow_boundary_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_raw_sh3_subtree_flow_threshold_precision_v1.md"
---

# 来源身份与范围

三份来源分别是集合包含容量切 Exact、root-conditioned layered flow boundary 和实数 quota/k=1 precision note。它们共同补足 raw SH3 条件流的必要接口，但不生成 integer forest，不声称 exact SDP finder、不提供 general UM approximation 或 near-two gap。

| clean ID | 原路径 | SHA-256 | 大小 | 实读性质 |
|---|---|---|---:|---|
| `a7bebf2d06d729998e93` | `history/source/notes/unrelated_machines/sol_raw_sh3_inclusion_entry_cut_exact_v1.md` | `0b8815af7ded08ed5fd85efdf06c10691b683aa54c66ed1caa4b61377b77c41d` | 5,404 B | Exact 对象、容量切、完整 jobs、CONFIG(1) 和量词 |
| `7f98df8bd98a2d7034a4` | `history/source/notes/unrelated_machines/sol_raw_sh3_root_conditioned_layer_flow_boundary_v1.md` | `8fa31b0efd1969a00cb466d49040738387b09c47274394a5b857a71809876e50` | 8,100 B | genuine-law 与 M3 extension、layer product、k=1 separator |
| `dd2cdd7f839a901fbbfa` | `history/source/notes/unrelated_machines/sol_raw_sh3_subtree_flow_threshold_precision_v1.md` | `d612e2ec9c00a3b9ad639712c6f4d387a12659cb8dc42ef58b42c7851ce358e6` | 3,537 B | real quota 与 k=1 corridor precision |

证据原件和 manifest 在 `archives/unrelated-machines/tools/evidence/raw-sh3-root-flow-20261031/`，回执草稿在 `cleanup/workspaces/Boss2/raw-sh3-root-flow-receipts-20261031.json`。

# 1. Raw SH3 正入口与条件子树流

内部行 v 有 k_v 个 unique-home jobs，每枚 home 时间 1/k_v、后层 alternatives 时间一；H_v+O_v=k_v，load=C_v+H_v/k_v，slack `g_v=T−1−C_v+O_v/k_v`。固定 T<2。共同 L 满足 degree≤6 ideals、M3、CONFIG first/pair 和 global degree-two load localizers。

unit-row incoming pair zeros 使任意两个不同 R_jR_j′ 为 M3 null；null-vector 正交性把它推广到所需三/四次乘子。对任一正入口 E，令 p=L(E)、b_u=L(E C_u)、y_(u,j,w)=L(E C_u x_(u,j,w))。支付得到

`0≤b_u≤p`，
`sum_w y_(u,j,w)≤b_u`，
`sum_j y_(u,j,w)≤b_u`，
`sum_(j,w)y_(u,j,w)≥k_u(2−T)b_u`。

在 DAG 上由 a_v=p 开始，按拓扑序令 a_u 为构造的 incoming flux；若 b_u>0 取 `f=(a_u/b_u)y`，否则置零。于是 activity≤p、每 token/arc flux≤activity、每行 export≥r_u activity，其中 `r_u=k_u(2−T)`。该 flow 是新的一阶 canonical flow，不保持原 raw point 的矩；没有免费补上其他 jobs、selectors 或真实 joint forest。

若 canonical subtree LP 对正入口不可行，则所有 raw SH3 点中该入口 first mass 必为零；结合 selector one-hot 可形成 sound FAIL。拒绝单点/单入口不等于整个实例 infeasible，必须用全体 mandatory endpoints 的量词。

# 2. 真 law 与 M3 extension、layer product

若 L 是真实 complete assignment law，unit pair zeros 给 C_v≤1 almost surely，因而对任意 affine q 有 `L(g_v q²)≥0` 时，(2.1)–(2.2) 直接由点态 load、unit capacity 得到。若 L 仅为共同 M3 functional，`L(A x(1−C_v))≥0` 由 degree-three null 和 M3 norm 支付；不能用 common M2 单独替代。

分层 component 的每层 unit arrivals 满足原 job identity `sum_next C=sum_prev O`。若 selector A 在 layer zero 有正质量，重复应用正入口流得到

`product_i [k_i(2−T)]≤N_terminal`。

在原两层 diluted family、T=1+1/k 时，需要 `(k−1)²≤k`；k≥3 即排除 raw SH3 extension。更深层不只是拉长 bad event，必须给足终端宽度。layer product 是必要切，不是实际 forest 或 hardness。

T=1+s/k 的 integer s 仍给 `(k−s)²≤Dk` 一类必要条件；如果所有 selector endpoints 都违反该切，M3/SH3 系统整体无点。不得把一条被拒绝的 point 直接称作 OPT>T。

# 3. 实数 quota 不能向上取整

`r=k(2−T)` 是 rational real demand。实际整数 schedule 需要 O≥ceil(r)，但 raw first-moment inequality 仅给 real `O_expectation≥r·activity`；不能先取 ceil 再调用整数 half-star theorem。只有当 `(T−1)k` integral 时，active home marginal sum 恰为 integer h，可在 hypersimplex 中分解成完整一阶 CONFIG。一般 grid 不得静默整数化。

# 4. k=1 的额外非衰减 corridor

k=1 行唯一 home endpoint Y 时间也是一。完整 same-row CONFIG pair zeros 给 `L(R_jY)=0` 对每个 incoming endpoint。于是对任意正入口 E，`L(E C Y)=0`、`L(E C O)=L(E C)`；canonical outgoing weights 可按 activity 精确缩放，不损失 `2−T` 系数。任意显式长度的 k=1 corridor 因而一阶流不衰减；merge 仍受 unit capacity。

该结论依赖额外 incoming/home pair zeros；仅有 incoming/incoming pair 时不成立。混合网络可在 k=1 rows 用 coefficient 1，在一般 rows 用 r_u；仍不形成 actual integer forest。

# 5. 集合包含切实例与完整 job certificate

集合族以 q-sets、2q-sets 和 terminals 构造 U_S→B_W→Z_R 三层。定义 H_S={R:|R∩S|≥q/4}、M 为每个 W 外部 H_S 的 q-subsets。对 selector mass p>0 的 U_S，原 SH3 localizers 给 `sum_(W⊃S)b_W≥δd1p`、B exports `sum_R y_W,R≥δd2b_W`、terminal cap `sum_W y_W,R≤p`。因此

`δ d1 (δ d2−M)≤H`。

若显式 rational inequality 严格反向，则所有 selector first mass 必为零，和 one-hot 冲突，故系统 sound FAIL；实际 schedule 亦有同一计数含义。CONFIG(1) 有显式一阶 witness：U selectors、f/e home 和 eligible destinations 的统一 weights，terminal total≤1；因此 CONFIG optimum=1，而实际路径 assignment 峰值≤max(1,2−1/d1,2−1/d2)。

H/C、M/K、K/C 的二项式 bounds 和 floors 支付固定 s1≤q^a、s2≤q^b 的渐近 strict FAIL；所有 integers O(m) bits、O(q) 项，比较和证书生成 bit-polynomial。finite audit 只作辅助，不替代族证明。

# 6. 范围与未完成义务

本桥正确关闭的是：raw SH3 正入口的一阶 canonical flow、real quota 边界、k=1 额外 corridor、集合包含容量切与 sound FAIL。它没有：

- 保留原 raw point 的完整 higher moments；
- 给 flow 一个共享 integer owner/forest decoder；
- 证明每条 rejected endpoint 都对应实际 OPT>T，除非全体 mandatory endpoints 量词闭合；
- 提供 exact SDP/CONFIG solver、near-two hardness 或一般 UM 算法。

继续主目标仍需解决 shared integer ownership after low-degree conditional flows；path-length heuristics和terminal count单独不足。原件和 manifest 在 evidence，正文归档为资料，回执草稿单列。
