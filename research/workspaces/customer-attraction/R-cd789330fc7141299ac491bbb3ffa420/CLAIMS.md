# 本桌面精确Claim及状态

共同对象一律采用仓库CAG-MODEL：有限单位客户、有限非空共同目录、单位提供者、全部有序历史纯SPE；空主题、重复主题、零客户和任意历史依赖平局不被省略。改变模型的加权实参数只作代数延拓，原单位客户结论取整数参数。无外审或新颖性认证。

## Q-CAG-HALF（原身份不变，OPEN）

对每个实例、任意m>=1和每个上述完整SPE，2W>=OPT_m。所有新结果均不解决或反驳它。

## B10-CYCLIC-TERMINAL-BR-NO-v1（解析障碍，独立内审）

八主题i mod8，连续三标签块各a名客户、对径二标签块各b名客户，a,b正整数。三槽菜单Z_i=(i,i+4,i+1)的根/两尾收益为b/2+2a、b/2+3a、b+2a，末位为真正BR；静态v4=(10b+23a)/16。当9a/2<b<=25a/2时根<v4且全部尾>=v4。故根比较、尾部过线及全部列末位BR不足以推出extra-one。菜单非SPE，第二位真实偏离可盈利。依赖：逐客户均分、离散凸性静态上下界；证据与反对范围见[正文](relay_transport/last_br_threshold_menu_boundary.md)及[独审](credible_shared/review_terminal_br_menu.md)。

## B10-CYCLIC-CREDIBLE-v1（同族完整分类，root独立重构）

同一整数族的所有完整三人SPE中，首位收益最小值为b<=a时2a+b/2，b>a时5a/2+b。两段均严格大于v4；b>a时所有完整SPE均福利最优。全历史达到策略在正文给出。依赖：全部末位BR集合、第二人的真实可信阈值L=b+5a/2、旋转策略；不依赖一般EI。见[完整分类](relay_transport/cyclic_family_complete_spe.md)、[root独立审计](parent/audit_cyclic_credibility.py)。范围是本族，不是固定人数一般定理或无界人数支付。

## B10-MENU-SORT-ODD-NO-v1（无界人数模板障碍，独立重构）

环k客户，主题A_i={i-1,i}；r=2h+1,h>=1，菜单每根A_i后各h个A_(i-1)、A_(i+1)。根u=2/(h+1)，每尾比根多1/[h(h+1)]。对n>=2,k>=max(7,2(n-1))，静态v_n=2-2(n-1)/k；取k增大可使v_n/u趋h+1。即使严格收益排序也不给人数无关乘法近似。菜单末位有盈利偏离，不是SPE。精确静态上下界及证据在[正文](global_mechanism/cycle_threshold_obstruction.md)。

## B10-GAP-SUMMARY-NO-v1（无界人数归纳摘要障碍）

对每个k>=3，r=(k-1)^2+1，r个不交k客户主题。每根a列取a^k加r-k个不同非a主题。所有根收益1；每孩子F_(r-1)-P_tail=(r-1)min u_tail，但父F_r-P_root=k(k-1)>r min u_root，差k-2。任意预先固定深度的真实末尾也能补全。仅否定“孩子gap标量+根最优性(+固定末深)”闭合；这些孩子整体不是SPE。一般GAP-r仍OPEN。见[正文§2](tail_credit/gap_and_deletion_obligations.md)。

## B10-HARD-DELETE-DEFICIT-NO-v1（真实完整SPE信用障碍，独立内审）

复用旧13人、6主题、36单位客户完整SPE。对每个0<ε<=1/24，t=5/2+ε；全部真实根收益5/2<t，每个真实tail平均>=t。实际根P后删除低于t的11名尾部，根收益返还Γ=45/2而低尾总亏空11ε。因此对任意固定有限K不存在普遍Γ<=K sum(t-u)_+；同理任何在零亏空向量连续且取零的纯亏空函数都失败。t自由是承重；不反驳t绑定安全值的不同合同、分数删除或一般half。来源、守恒公式、完整DAG证据和[独审](global_mechanism/tail_credit_independent_review.md)见[正文§3–4](tail_credit/gap_and_deletion_obligations.md)。

## B10-SHARED-NEAR-TWO-v1（完整SPE压力族，独立内审）

任意m>=2,a>=1；A有ma+1客户含不同x,y，m-1个不交A外块Q_j各a客户，目录A、Q_j+x、Q_j+y。全历史恒A为SPE，W=ma+1，OPT=(2m-1)a+1；全部遗漏恰属两个极大主题，最优并集覆盖全部客户。固定m比率趋2-1/m，m无界可趋2。依赖恒A判据，已知根饱和机制明确复用，不认领新半覆盖定理。[正文](credible_shared/shared_omission_near_two.md)、[独审](mixed_menus/review_shared_family.md)。

## B10-MAX-STANDALONE-HUB-NO-v1（完整SPE规则反例，独立内审）

偶k>=12，M=C(k,k/2)，半子集核心客户与每外围M/2-1私有客户组成hub族。hub是唯一最大单独收益主题，但每个hub根末BR给3M/4<lambda3。真正两人完整SPE根选外围，末位不同外围。否定最大单独收益选择规则；不否定extra-one、Mfull或原q平均真实偏离（后者本族大于lambda3）。[正文](mixed_menus/max_standalone_hub_boundary.md)、[独审](shared_seats/hub_family_independent_review.md)。

## 候选（未提升）

- **EI**：任意合法背景b、剩r人，每份完整后缀SPE首位u>=v_(r+1)(b)。合法背景嵌入及最小r归约正确；任意菜单替代已经失败。
- **GAP-r**：同背景最优剩余利润F_r(b)与真实剩余利润P满足F_r-P<=r min u；r<=2成立，一般OPEN。上述伪菜单不反驳它。
- **P-seat-v2**：平行遗漏块每块可由合法主题实现，每主题U截面为空或恰一整块；容量阈值R>=r是否给所有后继收益>=z。r<=2已重构，一般OPEN。v1漏可实现性，r1可假，已留修订记录。

## 接续阶段精确身份

- **CA-FRACTIONAL-TAIL-WATERFILL-v1（共享已整理，核心独立内审）**：任意有限终局、背景、根、尾与t≥0，存在同一辅助分数尾权重，原高尾保1、覆盖支撑不变、正权unit密度过线；同一全客户H≤Σ(t−u_j)_+同时控制全部Q/J查询。精确守恒保留背景返还；不声称SPE继承或半覆盖。
- **B10-ENDOGENOUS-WATERFILL-SHARP-v1（完整解析族，独立内审）**：固定53客户四人完整SPE加c共同客户，真实静态v4=t0+c/4，t0=28481/2924；唯一低尾亏空D=647/8772，低尾水位根返还Γ/D趋1。原根收益始终高于阈值；不主张在最小反例类锐。
- **B10-HIGH-TAIL-FIXED-CREDIBILITY-NO-v1（精确真实SPE阻断，独立内审）**：同一族中原高尾必须保持1且查询信用≤D时，不能同时保持原完整策略，也不能让原实际叶来自任意重新选择续局的加权SPE。窄合同是承重；允许高尾同步缩权已有所有c的正修复。
- **B10-UNIFORM-CONTRACTION-INTERFACE-v1（新解析充分接口，正在独审）**：固定保留根背景及全目录共同核心，若同一原尾SPE在全部有序历史规定行动均避开非核心背景，则任意共同正权λ≤1保留整棵尾SPE。额外S≤a*条件给实际叶水位H≤D。条件未证明普遍，不自动让所有离轨叶同时过线。

PI、混合弱推送、全树水位信用均为OPEN候选，不从有限回归推断成立。新颖性、外审及一般主目标未认证/未闭合。
