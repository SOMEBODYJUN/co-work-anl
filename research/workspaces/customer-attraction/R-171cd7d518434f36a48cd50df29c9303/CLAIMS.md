# 本轮精确数学身份与开放义务

所有CAG结论都采用原 CAG-MODEL，保留单位客户、共同目录、任意有序历史及任意
历史依赖平局。**Q-CAG-HALF仍OPEN**；个人备份不自动成为共享canonical，外审与
新颖性均未认证。

## B5-OPTIMAL-OMISSION-EXISTENCE-NO-v1

- **Statement / domain / quantifiers:** 存在二人、六个两两不同客户集合的共同目录及完整
  纯SPE，使对每个达到OPT的主题组合，其最优并集O均有|O\C_actual|>W。
  更具体地，对全部整数k>=3，正文12类单位客户重数及指定完整策略给
  W=13k-4、OPT=14k-4、唯一最优无序主题集合{T,Q}、遗漏U=14k-6>W。
- **Definitions / scope:** C_actual是实际覆盖，G=|C_actual\O|=13k-6；真正效率差额
  OPT-W=U-G=k，原half余量为12k-4>0。它只否定可选择最优组合的遗漏支付桥。
- **Dependencies / evidence:** 两人精确均分公式；全部六个末位节点及根真实比较；
  全部21个允许重复主题对的覆盖。作者展开单位客户Fraction审计及一般线性公式。
- **Objections / status / files:** 独立研究员正在从输入和策略重构；不宣称最小性、
  外审或新颖性。[正文](global/optimal_omission_exchange_counterexample.md)及其audit。

## B5-EARLY-MENU-LOAD-DEFECT-v1

- **Objects / quantifiers:** 任意原模型完整纯SPE、任意至少余两人的有序历史，任意
  当前行动T对应原策略的真实中继负载l_T和真实末位R_T；d=p+l_A。
  对所有q_x in [0,1]及eta>=0成立，目录、人数、客户均无固定上界。
- **Definitions:** B_q(c)是截断分数覆盖的Lagrange价格值；xi、zeta为d相对于p+l_T
  的两种倒数差；epsilon(mu)及epsilon_*为正文(1)的连续二次函数及紧单纯形最大值。
- **Conclusion:** B_q(v+epsilon_*)<=eta*w+sum_x(q_x-t_eta(x))_+；精确有符号版本
  保留tau*epsilon(mu)。仅中继卸载时epsilon_*<=3P_middle/8。
  根实际非末位i有OPT<=W+(m-1/2)u_i+m epsilon_i；若某最低收益非末位玩家的
  全部偏离中继负载不变，或满足正文有方向的零缺陷条件(10)，则原half成立。
- **Dependencies / evidence:** 当前真实偏离、实际末位比较和偏离后的末位真实比较；
  不冻结中继，不把多个后继当一名玩家。父方独立展开G0=G-tau*epsilon；
  全参数双线性角点及范围上界解析证明，作者Fraction审计，独立审查进行中。
- **Objection / status / files:** 一般中继缺陷没有全局支付，不能删去该项或零缺陷假设。
  [正文](prices/early_menu_load_defect.md)、[独审](independent/early_price_review.md)。

## B5-PATH-INTERVAL-RENT-v1

- **Objects / domain / quantifiers:** 任意有限主题路径S_1,...,S_m（无需SPE）；任意
  紧接前缀j的连续未来窗口I_j、固定全行权theta_j>=0、实reserve rho>0。
  令b_j为前缀客户负载，q_j为窗口负载，c为最终负载，Gamma=max_t sum_{j:t in I_j}j theta_j。
- **Exact conclusion:** sum_j theta_j sum_x b_j[1/(rho+b_j)-1/(rho+b_j+q_j)]
  <=Gamma sum_{c_x>0}[1/(rho+1)-1/(rho+c_x)]<=Gamma W/(rho+1)。
  宽二、theta=1/j、rho=1给至多W。
- **Dependencies / evidence:** 每客户实际hit排名的精确倒数差分摊，首hit系数零，b_j<=j。
  作者与父方独立解析重构、两份互不导入的Fraction审计。
- **Sharp boundary:** 若允许任意未来单槽代替连续窗口，m=2q、唯一客户hits在1及
  q+1,...,2q，I_j={q+j}、theta=1/j时Gamma=W=1，费用H_q/[(rho+1)(rho+2)]无界。
- **Scope / objections / status:** 没有证明一般离轨运输满足窗口条件。虚拟reserve只是
  代数，不调用非法主题SPE；固定人数使用ghost终局时另查总人数。内部独立检查通过；
  [正文](coupling/path_interval_rent_budget.md)、[父审](parent/interval_rent_independent_review.md)。

## B5-POOLED-RESPONSE-LOAD-INTERFACE-v1

- **Objects / definitions:** 原任意m完整SPE，在实际第i节点改b后的真实终局删去偏离者
  所得背景B_i(b)，令H(p)=(1/m)sum_i E_{b~p}load(B_i(b))，P(p)=sum_x p(x)/(1+H_x(p))。
- **Exact proved content:** W-mP=sum_i(u_i-D_i)+sum_i(D_i-C_i)+mJ，J为正文精确非负
  Jensen余项；若全p的POOL预算W>=mP成立，则自由分数安全值minimax给
  OPT_m<=(2-1/m)W。旧36客户实例指定p上信用严格修复旧去相关坏点。
- **Open / scope:** POOL预算本身未证，有限锥无分离不提升它；没有证明W>=m v_m。
  [正文](security/pooled_response_loads.md)及audit；尚待独立审查。
