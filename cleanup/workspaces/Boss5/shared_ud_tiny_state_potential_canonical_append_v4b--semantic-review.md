---
source_id: "0eb8b34fa84864a54169"
source_path: "history/source/notes/unrelated_machines/sol_general_repair_shared_ud_tiny_state_potential_canonical_append_v4b.md"
source_sha256: "1e3710870c8fbef4d4235cf2f90fe2d8ec6ca84b99ec6cd234464cc9d260df44"
source_size_bytes: 22847
status: "full-read; v4 candidate canonical append; fresh-independent-review-still-required"
disposition: "integrated-version-boundary"
target:
  - "archives/unrelated-machines/state/审查/Boss11共享UD叶tiny-home-k二次扩域三源审查--审查.md"
  - "archives/unrelated-machines/state/审查/全局行基数过滤与多外层单态小home双源审查--审查.md"
  - "archives/unrelated-machines/tools/evidence/shared-ud-tiny-home-v4b-20261031/manifest.json"
---

# 来源身份与读取范围

clean show 0eb8b34fa84864a54169 完整读取了冻结的 22,847 字节追加稿。来源路径是 history/source/notes/unrelated_machines/sol_general_repair_shared_ud_tiny_state_potential_canonical_append_v4b.md，SHA-256 为 1e3710870c8fbef4d4235cf2f90fe2d8ec6ca84b99ec6cd234464cc9d260df44；同一字节定位于 legacy-cleanup 与 main 冻结提交。正文明确前 175 行 v1 身份不被复制或改写，未发布 v2/v3 只保留历史字节；本文件新增身份是 UM-MULTI-OUTER-SINGLE-STATE-TINY-HOME-19-10-APPROX-v4 的 canonical append v4b。

同时回读结果树中的相关对象和审查：全局行基数过滤与多外层单态小home双源审查--审查.md 已将 v1、v4、v5 分开；Boss11共享UD叶tiny-home-k二次扩域三源审查--审查.md 已核对 v3/v4 Exact 与 proof_v3；多outer tiny-home作者证明v1读后与完整算法范围增量--审查.md 承载旧 k4 v1。它们支持版本关系和域边界，但不能替代 v4b 自身应有的 fresh Exact-first 复核。

# v4b 的精确候选域

输入是完整 typed normalized-flat Q 与全部 ordinary P(Q) 原任务。每个 outer 只有一个 indexed state，正 home 权重和为一，homes 全局物理互异；每个 home 有一个 own-unit helper。helper 可有任意显式 shared B-fallback normalized states；另允许任意多个仅支持于 B 的 exact-threshold-UD leaves。所有菜单非空、显式、indexed；zero/incidence/duplicate/unused 内容必须保留，不能把未选 payload 删除。

- k=1 不再另加 home tiny 上界，只保正权归一化。
- k>=2 要求每个 home 正权最大值 nu <= 1/(16384 k^2)。
- leaves 使用固定 epsilon=15/16 的 E_l 与尾和 b_l<epsilon 条件；叶值至少 epsilon 当且仅当 bundle 命中 E_l。
- 量词对所有完整显式 Q 成立；算法只接收 Q，没有 OPT、可行点、joint law、target profile、精度参数或 scheduling oracle。
- 候选目标是输出全部原 jobs 的原 finite endpoints assignment，并满足 Cmax <= (19/10) OPT；sound FAIL 必须有 actual V<15/16 的反证。

该域仍严格排除 multi-state outer、home 重叠、home 上 extra leaves、一般 non-UD groups 和一般 unrelated-machines。它不是六人 SPE 客户模型。

# 证明和算法链条（来源自述的候选内容）

来源把 v4 分成两条分支。k1 用 helper 顺序上的标准单调次模 greedy，不使用 tiny 或 prefix 损失；k>=2 用固定 profile 的 matching linear oracle、凹 deficit potential、稳定 profile exchange、rational Frank-Wolfe 和整数 lower-bound circulation。

1. 值桥和 leaf 过滤：normalized-flat bridge 给 OPT=2-V。没有完整 leaf matching 时，exact threshold-UD iff 直接推出 V<15/16，全 private baseline 峰值至多 2，比例 32/17 小于 19/10。有叶匹配时，helper profile 的可实现 welfare region 是 matching/transversal matroid 网络多面体。
2. k1 greedy：对 helper options 与 empty 逐个做 matching oracle 的单调次模 greedy，取得 profile optimum 的 1/2；若 welfare 小于 1/4，则由共同 benchmark 反证 V<15/16，否则从 W>=1/4 得 Good helper home weight z>1/10，再以叶匹配和原 endpoint 回填得到 19/10。
3. k>=2 势与单替换：固定 c=5/16、theta=1/32、xi=1/(2^20 H^2)、tau=1/(2048H) 和停止阈值 25/128。势为 (theta/k) sum W_i 减去 sum (c-W_i)_+^2。稳定交换声称 helper 替换可找到同一线性最优面的新点，并将 tiny 上界转成 B_j 总和控制；若真实 V>=15/16 且 deficit 足够大，则存在单 helper 替换使 profile potential 增加至少 rho/H。
4. 有理后端与停止：每个 profile 的势用 matching linear oracle 的固定次数 rational Frank-Wolfe 近似；若无候选达到 tau 的近似增量则声称真实 V<15/16并输出 baseline，否则有限次接受替换后所有 W_i>=25/128。
5. prefix-flow 和原 jobs 回填：把 fractional resource claims 与叶行放入 lower-bound circulation，按每个 outer 的 a_iu 排序约束整数前缀计数；得到完整叶匹配和整数 fallback bundles。Good helper 的 chosen-state 值 Q_j>=1/10，k>=2 的 nu 损失仍保 W_i>19/100，k1 由 greedy 保证更强边界。选择每组 state 后只把对应正 incidences 放 resource，其余全部原 jobs 留 private，得到 Cmax<=2-1/10=19/10。

来源强调 FAIL 必须由 actual V<15/16 的反证支持，不能把 profile 线性优化失败、必要点失败或近似后端停止直接命名为 FAIL。

# 证据层级、版本差异与缺口

v4b 自称 v4 的 self-contained canonical append，但同时明确 v4 新 Exact 的独立 Exact-first、author read-after 和最终完整审查尚待补齐；它把前身 k4 Exact/Proof、k2 informed audit、作者 self-audit 和小型 exchange 枚举列为相关证据，不能把这些前身或作者自审自动升级为 v4 fresh proof。有限程序仅覆盖 3 helpers/2 outers、4/5 resources 等小型 stable-exchange 例，不运行完整 profile search、FW、prefix-flow、k1 greedy、tiny-domain输入或全部 UM jobs 输出。

准确状态是“候选扩域 canonical append，包含详细算法和承重不等式，待独立后置审查”。不能写成已通过外审、已实现端到端或一般 UM 的 19/10 算法。若 fresh review 发现 stable coupling、actual-target 强制进展、FW 位复杂度或 prefix-flow 缺口，应保留 v4b 为候选版本并标出问题。

与现有审查的接续：

- v4 Exact 与 proof_v3 的量词和 k2 曲率已有独立版本页；本源新增解除 k1 tiny 后的完整 greedy 分支、共享 UD leaves 的 canonical 回填和 v4b 的全算法自足叙述。
- 旧 v1 的 k4 CDF/MW/条件期望证明不能替代 v4b；v4b 不回写 v1，也不把 v1 的有限 backend 当 v4 端到端证据。
- v5 的 1/(1024k) 域与 v4b 保持独立身份；不能因两者都写 19/10 就合并量词。
- 一般 UM-TARGET-v1、任意 multi-state outer、home overlap、non-UD 叶和六人 SPE 目标仍 OPEN。

# 处置

本源应 integrated 为 v4 版本 provenance/候选算法范围，原字节与 SHA 进入新的 evidence manifest；正式数学结论继续由现有 v4 审查对象承接，但状态保留 fresh independent review pending / no end-to-end implementation。第三阶段可建立 v4b canonical append 到 v4 restricted candidate 的版本关系边，不得建立 v4b 到 general UM 或 Q-CAG-HALF 的无条件边。
