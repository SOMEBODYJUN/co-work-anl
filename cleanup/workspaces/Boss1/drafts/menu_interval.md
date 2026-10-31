# Boss1：菜单缺陷与区间租金清洗稿

本稿只处理两个冻结来源：

* `67dd19b565beb22ad3db`：`research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/parent/interval_independent_audit.json`；
* `2413e95a47f7e647a302`：`research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/prices/early_menu_load_defect_audit.json`。

两份菜单/区间相关来源及其相关程序和正文均从冻结提交 `68fad804ec5946cb296f77dc5b336308a66abf12` 读取，并与全仓已归档的原文、脚本、报告和审查页交叉核对。池包探针 `4c52f58685795cdfcf9e` 已由 Boss1 另一份独立审查处理，本稿不重复处置。

## 1. 区间独立审计（`67dd19b565beb22ad3db`）

### 对象和量词

模型是任意有限实际主题路径 $S_1,\ldots,S_m$ 和单位客户；路径不要求来自 SPE，允许空主题、重复主题、相等主题和零客户。对每个前缀 $j<m$ 选一个与客户无关的非负全行权 θ_j、正实代数 reserve ρ，以及必须紧接前缀的窗口 $I_j=\{j+1,\ldots,j+\ell_j\}$。令 $b_j(x)$ 为客户在前缀中的负载，$q_j(x)$ 为窗口负载，$c_x$ 为全路径命中数，$W=|\{x:c_x>0\}|$，并令

\[
D_t=\sum_{j:t\in I_j}j\theta_j,
\qquad \Gamma=\max_tD_t.
\]

审计对应的租金项是

\[
E_j^{(\rho)}=\sum_x b_j(x)\left(\frac1{b_j(x)+\rho}-\frac1{b_j(x)+q_j(x)+\rho}\right).
\]

这里的窗口连续性是“从实际前缀终点后立即开始并包含中间全部槽位”，不只是集合论意义上的区间或单点集合；ρ 只是代数 reserve，不是目录中的合法行动，也不调用其 SPE 最优性。
ho\) 只是代数 reserve，不是目录中的合法行动，也不调用其 SPE 最优性。

### 它实际支持的结论

既有父方正文给出了逐客户命中排名的普遍证明：窗口内的命中正好对应排名 $b_j+1,\ldots,b_j+q_j$，首个真实命中因 $b_j=0$ 不收费，其余排名使用 $b_j\le j$ 和槽位拥塞 Γ 控制。因此对任意上述路径、窗口、权和 ρ>0，

\[
\sum_j\theta_jE_j^{(\rho)}
\le
\Gamma\sum_{x:c_x>0}\left(\frac1{\rho+1}-\frac1{\rho+c_x}\right)
\le \frac{\Gamma W}{\rho+1}.
\]

这是真正的任意规模代数引理；`interval_independent_audit.json` 本身只是对该推导及边界的有限实现核对。

### 冻结证据与程序范围

JSON 状态为 `independent exact finite audit; universal proof in review`，`cases=151586`、`seed=171021`。对应的独立定义级程序（标准库 `Fraction`，不导入作者实现）穷举 $m\le6$ 的全部二元路径和全部窗口长度，加入非整数 reserve、非均匀行权及 500 条较长随机路径；另外直接计算稀疏未来槽位和 rank-2 边界。冻结 JSON 的关键输出是：

* `rank2_cost=1/4`；
* 稀疏族 $q=1,2$ 与错误细界相等，$q=3$ 给 $11/36-3/10=1/180$，$q=8$ 和 $q=64$ 继续为正差；
* $q=64$ 的输出仍是精确有理数，不是浮点近似。

该 JSON 的归档回放位于 `archives/customer-attraction/tools/evidence/interval-rent-independent-20261031/replay/interval_independent_audit.json`，stdout 与 JSON 一致；本轮读取并比对冻结内容，没有把回放当作新的普遍证明。

全仓还有另一份较早的 `audit_path_interval_rent.py`/`path_interval_rent_audit.json`，报告 `147456` 单窗口、`51384` 全宽配置、`4094` 宽二路径和 `2000` 随机案例。两组计数属于不同脚本和不同测试设计，不能相加或互换；它们均只核验有限实现，不替代逐排名证明。

### 失败机制和边界

父方试过的“第二次命中只能被一个非零背景窗口收费”的加强是错的：`1010` 路径的两个宽二窗口可同时收费，定义级费用为 $1/6+1/12=1/4$。这只撤回该加强，不攻击 Γ 原界。

去掉“紧接前缀”的连续性后，取 $m=2q$，单客户命中模式

\[
(1,0,\ldots,0,1,\ldots,1),
\]

对 $j=1,\ldots,q$ 只选未来单槽 $I_j=\{q+j\}$，取 $\theta_j=1/j$。每个槽位只出现一次，故 $\Gamma=1$、$W=1$，但费用为

\[
\frac{H_q}{(\rho+1)(\rho+2)}\to\infty.
\]

这是任意路径的稀疏跳过反例，不是 SPE 反例；它说明“只控制每槽使用次数”不能替代连续命中排名。相关完整 SPE 两客户族已经在归档反例页中重构，但其福利仍为 $W=OPT=2$，所以也不是 Q-CAG-HALF 反例。

### 与既有正文的差异和处置

既有 `path_interval_rent_budget.md`、`interval_rent_independent_review.md` 及“连续窗口与稀疏命中租金”审查页已承载普遍证明、rank-2 撤回和稀疏障碍。本 JSON 的独有内容是父方有限审计的冻结摘要（151586、seed 171021、精确边界表）；它没有新的 SPE、福利或全树运输结论。保留为 `integrated` 的有限证据，正文继续把连续窗口引理写成路径级代数接口；不得把稀疏族或有限报告升级为全树反例。

## 2. 早期菜单加载缺陷审计（`2413e95a47f7e647a302`）

### 对象和量词

模型是有限单位客户、有限非空共同主题目录、任意玩家数 $m$、全部有序历史上的完整纯 SPE；空主题、重复选择和历史依赖平局均保留。固定任意合法历史 $h$，当前真实主题为 $A$，最后一名真实主题为 $B$，中间有 $k\ge0$ 名真实中继。对每个合法偏离主题 $T$，沿同一完整策略真实重放中继 $M_T$ 和末位回复 $R_T$；中继可以随 $T$ 改变，不能冻结为 $M_A$。

对客户 $x$，令 $p_x$ 为历史负载，$d_x=p_x+\ell_A(x)$、
$\Delta_T(x)=\ell_T(x)-\ell_A(x)$，其中 $\ell_T$ 是该偏离分支的中继负载。审计核对任意概率向量 μ、总权 τ（含 τ<1 的缩放边界）、逐客户权 $q_x\in[0,1]$、η≥0 和价格 $c\ge0$。

### 它实际支持的结论

核心是参考背景与真实偏离背景之间的精确缺陷恒等式。逐客户设

\[
\xi_T=\frac1{d+1}-\frac1{d+\Delta_T+1},\qquad
\zeta_T=\frac1{(d+1)(d+2)}-
\frac1{(d+\Delta_T+1)(d+\Delta_T+2)}.
\]

按真实末位回复 $r_T$、当前主题 $s_T$ 和 $e=E_\mu r_T$ 定义 $\epsilon(\mu)$。有限审计核对

\[
G_0=G-\tau\epsilon(\mu),
\qquad
\delta(\mu)=\epsilon(\mu)-V/\tau^2,
\]

以及参考背景余项的角点包络、Γ 范围界、“全卸载”时的 $\epsilon_*\le3P_M/8$、根包络和给定单调条件下的零缺陷。既有正文由此得到的是条件性价格转移：统一价格 $v+\epsilon_*$（或更紧的 $v+\delta_*$）能继承末位阈值包络；它没有给出一般 ε 的实际福利支付，也没有完成 Q-CAG-HALF。

### 冻结证据与程序范围

冻结 JSON 状态为 `all exact local algebra checks passed`，并明确 `finite implementation audit, no SPE claim and no general welfare proof`。其五个计数为：

* `identity_and_envelope_cases=14288`（12288 个小参数组合加 2000 个随机 Fraction 案例）；
* `parametric_corner_cases=540`；
* `relaxed_range_sharpness_cases=300`；
* `unloading_actual_rent_cases=352`；
* `global_actual_residue_cases=80`；
* `seed=202610215`。

相关加强版程序的归档回放位于 `archives/customer-attraction/tools/evidence/early-menu-price-independent-20261031/replay/audit_early_price_review.stdout`；它是不同脚本/版本，明确标作有限恒等式、边界和两个固定完整 SPE 的 `passed`，不能回填为本 JSON 的一般结论。

对应脚本不调用作者审计或 SPE 求解器，检查的是有限局部恒等式、角点和范围包络，因而这些数字不能证明任意 SPE 的全球福利结论。

全仓另有不同版本的独立 Fraction 回放：报告 `scalar_identities=43776`、`range_bounds=14592`、`remainder_bounds=10944`、`scalings=648`、`spe_rows=288`、`real_menus=71`、`real_inequalities=852`、`relay_payment_bounds=256`、`root_envelope_points=60`、`zero_defect_menus=3256`，状态 `passed`，范围为“有限恒等式/边界 + 两个固定完整 SPE”。它是加强版相关证据，不应回填成冻结 JSON 的原始计数。

### 失败机制和边界

缺陷来自偏离主题改变真实中继负载：若 Δ 不为零，冻结中继时的参考背景 $d$ 与真实分支的 $d+\Delta_T$ 不同，$G_0-G$ 正好留下带符号 ε。真实末位的跨菜单 slack 只提供 $\delta=\epsilon-\mathrm{V}/\tau^2$ 的条件减免；它不自动消除 ε。中继负载不变、特定单调方向或全部卸载时可得到零缺陷/范围支付，但一般负载方向和全树耦合仍未解决。

### 与既有正文的差异和处置

`early_menu_load_defect.md`、`early_price_review.md` 和归档“早期真实菜单负载缺陷引理独立审查”已包含完整对象、ε/δ/Γ 推导及条件半覆盖推论。本 JSON 是实现级有限审计摘要；它不新增模型量词、SPE 证明或实际福利支付。保留为 `integrated` 计算证据；正文继续标记一般支付义务、全树运输和 Q-CAG-HALF 为 OPEN。

## 3. 统一处置建议

| 来源 | 保留内容 | 不能宣称 | 建议状态 |
|---|---|---|---|
| `67dd19b565beb22ad3db` | 连续窗口路径级命中排名审计；稀疏跳过和 rank-2 边界的精确数值 | SPE、全树运输、Q-CAG-HALF 反例；把有限 151586 例当普遍证明 | `integrated` 有限 exact evidence |
| `2413e95a47f7e647a302` | 早期真实菜单的 ε/δ 恒等式、角点、卸载和零缺陷条件的有限 Fraction 核验 | 一般实际福利支付、任意 SPE 的全球桥、half 结论 | `integrated` 计算证据 |

后续若要升级任何一项，区间方向需要真实全树的连续/clock 运输或显式支付所有 skip-premium；菜单方向需要把 ε/δ 与真实中继福利在同一全树量词下支付。两份冻结源本身都没有完成这些升级。
