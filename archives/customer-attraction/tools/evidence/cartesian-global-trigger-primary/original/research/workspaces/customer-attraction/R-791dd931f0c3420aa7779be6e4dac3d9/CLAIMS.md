# 本轮精确 Claim 身份

共同对象、定义与量词：CAG-MODEL；有限单位客户、有限非空共同主题目录、
单位提供者、全部有序历史的纯 SPE，含任意平局、空主题、重复与零客户。
HALF(5) 与一般 Q-CAG-HALF 均 OPEN；无新无条件福利界或目标反例。
以下没有外审或新颖性认证。

## B13-20261025-TERMINAL-SPECTRUM-v1

- **Exact statement/domain:** 任意 m≥2，任意合法长度 m−1 有序历史，只要求最后玩家真实 BR。
  K 是全目录最大主题大小，M 取到 K，末位收益 v。对任意合法 Q，
  F_M(Q)=|Q\M|+|Q∩M|/m≤[1+m(m−1)/2]v−(m−1)K/2。
  任意 m 比较主题的并集 O、重数和 D 满足正文 TM-SPEC；五人最优菜单给
  4OPT5+D+46K≤275u5。
- **Objects/definitions/scope:** [唯一正文](terminal_maximum_spectrum.md)；不要求此前玩家最优，
  也不假定 M 被实际选择。空主题、重复、任意平局和零客户均保留。
- **Dependencies/evidence:** 末位 BR、共同最大 cap；全 m 逐客户余项
  (m−1−a)(m−2−a)/[2(a+1)]≥0。saturation 分支独立核对五人语义与系数。
- **Status/objections:** 内部解析推导与独立重构；暂无已知致命异议。
  没有外审、完整新颖性检索或二倍付款结论。
- **Open obligation:** 和前三实际来源谱及真回复联合支付 2W−OPT5，仍未解。

## B13-20261025-SPECTRAL-v1

- **Exact statement/domain:** 五名提供者，任意完整 SPE，实际首位收益 u，最大主题大小 K。
  对任意最优五项索引主题的重数 d_x，O=OPT5、D=Σd_x、S2=Σd_x²，
  [正文](saturation/spectral_root_inequalities.md)四条谱整数行全部成立。
- **Assumptions/definitions:** K 必须是同一完整目录的共同上界；取真实最大主题合法。
  最优索引允许重复。正文保留每条原证书的非负乘子和逐客户余项。
- **Conclusion/scope:** 必要关系；不是 HALF(5)，没有证明增强模板的最优值。
- **Dependencies/evidence:** R-bfbfe64dd5f94fa09d36b75198633f2b/five_only 的 maxroot 证书；
  本轮独立重构全部 192 类型，父方另核节点语义、谱及矩转换。
- **Objections/status:** 尚无已知致命异议；内部派生及复核。新增行能否共同支付 2W−O 未解。
- **Related files:** saturation/spectral_root_inequalities.md、audit_spectral_root.py/.json。

## B13-20261025-ROW3-DEFECT-v1

- **Exact statement/domain:** 任意 m≥3、任意固定完整 SPE 的实际位置 i=m−2、任意 q≥1
  个可重复合法比较主题，定义沿原 σ 的真实查询收益和 R_i、并集 O、实际福利 W。
  以 b 为此前实际负载，C_b=W−|O|+Σ_O1/(b+1)，K_b=max_TΣ_T1/(b+1)。
  若 Γ_j 是强制 T_j 后真实末两人相对背景 b+1_Tj 的最优两槽调和势缺口，
  则 R_i≥|O|−W+(C_b−K_b)−ΣΓ_j，且 C_b≥J_b≥K_b。
- **Definitions:** 全部符号及更强税/重叠版本唯一正文为
  [three_remaining_potential_defect.md](query_payment/three_remaining_potential_defect.md)。
  Γ 是势缺口，不能换成剩余利润或另一背景下的缺口。
- **Dependencies:** 精确调和势边际、双查询平均、实际末位最佳回复。
- **Evidence/status:** 作者解析证明，父方独立逐式重构通过；非福利界。
- **Objections/open obligation:** ΣΓ_j 的共同实际付款未证明；不能由 Γ_j≥0 丢掉负债。
- **Scope:** Γ_j 全零时给真正该行 ROW；没有保证这些条件在原 SPE 自动成立。

## B13-20261025-GLOBAL-TRIGGER-v1

- **Exact statement/domain:** 任意共同人数 m≥1，有限个客户集不交的 CAG 分量，
  联合目录为完整 Cartesian 目录。任意局部脚本 a^c，定义 M_c(h) 为
  max_b min_{z∈suffixSPE(hb)} u_i^c(z)，被最小化的是刚行动的 i。
  若每个位置 i 都有 Σ_c[u_i^c(a^c)−M_c(h_i^c)]≥0，则联合脚本可由完整纯 SPE 实现。
- **Assumptions:** 首次任一坐标失配后，所有坐标都选对该当前行动的极小 suffix SPE，
  并永久执行其乘积。完整有序全局历史允许相同局部历史采用不同处罚。
- **Conclusion/scope:** 充分性；不声称必要性、分量 SPE 可分解或 HALF(5)。
- **Evidence:** [独立盲重构](exact_tree/global_trigger_independent_review.md)，相邻验证器直接检查
  90/272 项完整比较及仅处罚改变坐标的明确失败；不以有限例子证明一般接口。
- **Dependencies/open obligation:** 只依赖有限逆向归纳、共同目录及分量可加性。
  尚无满足缺陷条件且 OPT>2W 的种子；有限字典阴性不推广到所有游戏。
- **Status:** 解析充分接口经内部独立重构，无外审。
